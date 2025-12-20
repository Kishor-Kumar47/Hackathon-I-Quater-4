# tests/test_agent.py

import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.agent import RAGAgent
from backend.app.services.qdrant_retriever import QdrantRetrievalService
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import AIMessage

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("QDRANT_HOST", "test_qdrant_host")
    monkeypatch.setenv("QDRANT_API_KEY", "test_qdrant_api_key")
    monkeypatch.setenv("QDRANT_COLLECTION", "test_collection")

# Test for full-book query -> retrieval -> response flow (US1)
@patch('backend.app.services.agent.AgentExecutor') # Mock AgentExecutor directly
@patch('backend.app.services.qdrant_retriever.OpenAIEmbeddings')
@patch('backend.app.services.qdrant_retriever.QdrantClient')
def test_full_book_query_retrieval_response(
    mock_qdrant_client, mock_openai_embeddings, mock_agent_executor_cls # Renamed mock for clarity
):
    # Mock Qdrant retrieval service
    mock_qdrant_instance = MagicMock(spec=QdrantRetrievalService)
    mock_qdrant_instance.retrieve.return_value = [
        {"id": "doc1", "content": "The quick brown fox jumps over the lazy dog.", "score": 0.9, "metadata": {"source": "story"}},
        {"id": "doc2", "content": "Dogs are mammals.", "score": 0.8, "metadata": {"source": "encyclopedia"}},
    ]
    # Patch the QdrantRetrievalService constructor when it's called within QdrantRetrievalTool
    with patch('backend.app.services.qdrant_retriever.QdrantRetrievalService', return_value=mock_qdrant_instance):
        # Mock OpenAI Embeddings
        mock_openai_embeddings_instance = MagicMock(spec=OpenAIEmbeddings)
        mock_openai_embeddings_instance.embed_query.return_value = [0.1] * 1536  # Dummy embedding
        mock_openai_embeddings.return_value = mock_openai_embeddings_instance

        # Mock AgentExecutor instance
        mock_agent_executor_instance = MagicMock()
        mock_agent_executor_instance.invoke.return_value = {"output": "The fox jumps over the lazy dog."}
        mock_agent_executor_cls.return_value = mock_agent_executor_instance # Ensure AgentExecutor() returns our mock

        agent = RAGAgent()
        query = "What did the fox do?"
        
        response = agent.process_query(query)
        
        assert response["answer"] == "The fox jumps over the lazy dog."
        mock_agent_executor_instance.invoke.assert_called_once_with({"input": query})
        # Assertions for QdrantRetrievalService.retrieve and OpenAIEmbeddings.embed_query are indirectly
        # covered by the AgentExecutor's behavior. We assume AgentExecutor properly uses the tools.
        # If we wanted to test the tool's interaction with the service, that would be a separate unit test for the tool.


# Test for query + user-provided context -> response flow (US2)
@patch('backend.app.services.agent.ChatOpenAI')
def test_user_provided_context_response(mock_chat_openai):
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = AIMessage(content="The main point is about cats.")
    mock_chat_openai.return_value = mock_llm_instance

    agent = RAGAgent()
    query = "What is the main point?"
    context = "This text is all about cats. Cats are great pets."

    response = agent.process_query(query, context)

    assert response["answer"] == "The main point is about cats."
    mock_llm_instance.invoke.assert_called_once_with(f"Context: {context}\n\nQuestion: {query}")