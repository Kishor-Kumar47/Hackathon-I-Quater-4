import pytest
import time
from unittest.mock import Mock, patch
from retrieval_validation.models.data_models import QueryRequest, RetrievedChunk
from retrieval_validation.services.query_embedder import QueryEmbedder
from retrieval_validation.services.qdrant_retriever import QdrantRetriever
from retrieval_validation.services.json_formatter import JSONFormatter


class TestAcceptanceScenarios:
    """
    Acceptance tests to validate the key scenarios for the retrieval system.
    """

    def test_validate_acceptance_scenario_execute_search_and_return_relevant_content(self):
        """
        Validate acceptance scenario: Execute search query and return relevant content with similarity scores
        """
        # Mock the Cohere client
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Set up mock responses
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_search_result = [
                Mock(id="chunk1", score=0.85, payload={"text": "Relevant content text", "source": "doc1", "category": "test"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            # Create service instances
            embedder = QueryEmbedder()
            retriever = QdrantRetriever()
            formatter = JSONFormatter()

            # Create a query request
            query_request = QueryRequest(
                query_text="What is artificial intelligence?",
                collection_name="test_collection",
                top_k=5
            )

            # Generate embedding
            embedding = embedder.embed_query(query_request.query_text)

            # Validate embedding
            assert embedder.validate_embedding(embedding) is True

            # Retrieve similar chunks
            retrieved_chunks = retriever.retrieve_similar(embedding, query_request)

            # Verify we got results
            assert len(retrieved_chunks) == 1
            assert isinstance(retrieved_chunks[0], RetrievedChunk)
            assert retrieved_chunks[0].text == "Relevant content text"
            assert retrieved_chunks[0].score == 0.85
            assert retrieved_chunks[0].source == "doc1"

            # Format results
            formatted_result = formatter.format_retrieved_chunks(retrieved_chunks, query_request)

            # Verify the formatted result contains the relevant content with scores
            assert "retrieved_chunks" in formatted_result
            assert len(formatted_result["retrieved_chunks"]) == 1
            assert formatted_result["retrieved_chunks"][0]["text"] == "Relevant content text"
            assert formatted_result["retrieved_chunks"][0]["score"] == 0.85
            assert formatted_result["retrieved_chunks"][0]["source"] == "doc1"

    def test_validate_acceptance_scenario_performance_thresholds(self):
        """
        Validate acceptance scenario: Return results within acceptable performance thresholds
        """
        # Mock the Cohere client
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Set up mock responses
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_search_result = [
                Mock(id="chunk1", score=0.85, payload={"text": "Content 1", "source": "doc1"}),
                Mock(id="chunk2", score=0.75, payload={"text": "Content 2", "source": "doc2"}),
                Mock(id="chunk3", score=0.65, payload={"text": "Content 3", "source": "doc3"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            # Create service instances
            embedder = QueryEmbedder()
            retriever = QdrantRetriever()

            # Create a query request
            query_request = QueryRequest(
                query_text="Performance test query",
                collection_name="test_collection",
                top_k=5
            )

            # Measure time for embedding generation
            start_time = time.time()
            embedding = embedder.embed_query(query_request.query_text)
            embedding_time = time.time() - start_time

            # Measure time for retrieval
            start_time = time.time()
            retrieved_chunks = retriever.retrieve_similar(embedding, query_request)
            retrieval_time = time.time() - start_time

            # Performance thresholds (in seconds)
            EMBEDDING_THRESHOLD = 5.0  # 5 seconds for embedding
            RETRIEVAL_THRESHOLD = 5.0  # 5 seconds for retrieval

            # Verify performance thresholds are met
            assert embedding_time <= EMBEDDING_THRESHOLD, f"Embedding took {embedding_time}s, which exceeds threshold of {EMBEDDING_THRESHOLD}s"
            assert retrieval_time <= RETRIEVAL_THRESHOLD, f"Retrieval took {retrieval_time}s, which exceeds threshold of {RETRIEVAL_THRESHOLD}s"

            # Verify we got the expected number of results
            assert len(retrieved_chunks) == 3

            # Verify results are sorted by score (highest first)
            scores = [chunk.score for chunk in retrieved_chunks]
            assert scores == sorted(scores, reverse=True), "Results should be sorted by score in descending order"

    def test_validate_acceptance_scenario_no_relevant_matches(self):
        """
        Validate acceptance scenario: Return appropriate response when no relevant matches found
        """
        # Mock the Cohere client
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Set up mock responses
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results - empty list for no matches
            mock_qdrant.return_value.search.return_value = []

            # Create service instances
            embedder = QueryEmbedder()
            retriever = QdrantRetriever()
            formatter = JSONFormatter()

            # Create a query request
            query_request = QueryRequest(
                query_text="Very specific query with no matches",
                collection_name="test_collection",
                top_k=5
            )

            # Generate embedding
            embedding = embedder.embed_query(query_request.query_text)
            assert embedder.validate_embedding(embedding) is True

            # Retrieve similar chunks (should be empty)
            retrieved_chunks = retriever.retrieve_similar(embedding, query_request)

            # Verify we got no results
            assert len(retrieved_chunks) == 0

            # Format results
            formatted_result = formatter.format_retrieved_chunks(retrieved_chunks, query_request)

            # Verify the formatted result has appropriate structure even with no matches
            assert "retrieved_chunks" in formatted_result
            assert len(formatted_result["retrieved_chunks"]) == 0
            assert formatted_result["total_results"] == 0
            assert formatted_result["query_text"] == query_request.query_text

            # Verify output validation passes even with no results
            assert formatter.validate_output(formatted_result) is True

    def test_threshold_filtering_functionality(self):
        """
        Additional test to verify threshold filtering works properly.
        """
        # Mock the Cohere client
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Set up mock responses
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results with various scores
            mock_search_result = [
                Mock(id="chunk1", score=0.90, payload={"text": "High relevance", "source": "doc1"}),
                Mock(id="chunk2", score=0.75, payload={"text": "Medium relevance", "source": "doc2"}),
                Mock(id="chunk3", score=0.40, payload={"text": "Low relevance", "source": "doc3"}),
                Mock(id="chunk4", score=0.20, payload={"text": "Very low relevance", "source": "doc4"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            # Create service instances
            embedder = QueryEmbedder()
            retriever = QdrantRetriever()

            # Create a query request
            query_request = QueryRequest(
                query_text="Threshold test query",
                collection_name="test_collection",
                top_k=10
            )

            # Generate embedding
            embedding = embedder.embed_query(query_request.query_text)

            # Retrieve similar chunks
            retrieved_chunks = retriever.retrieve_similar(embedding, query_request)

            # Apply a threshold of 0.5
            threshold_filtered = retriever.apply_thresholds(retrieved_chunks, threshold=0.5)

            # Verify threshold filtering worked
            assert len(threshold_filtered) == 2  # Only chunks with score >= 0.5
            assert all(chunk.score >= 0.5 for chunk in threshold_filtered)
            assert threshold_filtered[0].score == 0.90  # Highest scoring item
            assert threshold_filtered[1].score == 0.75  # Second highest scoring item