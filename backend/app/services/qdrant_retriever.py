# backend/app/services/qdrant_retriever.py

import os
from typing import List, Dict, Any
import openai
from openai import OpenAI

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from langchain_core.tools import BaseTool

class QdrantRetrievalService:
    def __init__(self):
        # Check if we have the required environment variables
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        qdrant_host = os.getenv("QDRANT_HOST")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION")

        if openrouter_api_key:
            self.openai_client = OpenAI(
                api_key=openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            self.openai_client = None
            print("Warning: OPENROUTER_API_KEY not set, using mock embeddings")

        if qdrant_host and qdrant_api_key:
            self.client = QdrantClient(
                host=qdrant_host,
                api_key=qdrant_api_key
            )
        else:
            self.client = None
            print("Warning: QDRANT_HOST or QDRANT_API_KEY not set, using mock client")

        self.collection_name = collection_name or "test_collection"

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a similarity search in Qdrant and returns the retrieved documents.

        Args:
            query: The search query string.
            k: The number of top relevant documents to retrieve.

        Returns:
            A list of dictionaries, each representing a retrieved document.
        """
        # If we don't have the required clients, return mock data for testing purposes
        if not self.openai_client or not self.client:
            print("Using mock retrieval for testing purposes")
            # Return mock results for testing
            mock_docs = []
            for i in range(min(k, 3)):  # Return up to 3 mock results
                mock_docs.append({
                    "id": f"mock_id_{i}",
                    "content": f"Mock content for query: '{query}'. This is a simulated result for testing purposes.",
                    "score": round(0.8 - (i * 0.1), 2),  # Scores decrease slightly for each result
                    "metadata": {"source": f"mock_source_{i}", "type": "mock"}
                })
            return mock_docs

        # Generate embedding using OpenAI
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            query_embedding = response.data[0].embedding
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []

        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            with_payload=True
        )

        retrieved_docs = []
        for point in search_result:
            retrieved_docs.append({
                "id": point.id,
                "content": point.payload.get("text"), # Assuming 'text' field in payload holds content
                "score": point.score,
                "metadata": {k: v for k, v in point.payload.items() if k != "text"} # Exclude 'text' from metadata
            })
        return retrieved_docs


class QdrantRetrievalTool(BaseTool):
    name: str = "qdrant_retriever"
    description: str = (
        "Useful for retrieving relevant document chunks from Qdrant "
        "based on a user query. Input should be a single string representing the query."
    )

    def _run(self, query: str) -> str:
        retrieval_service = QdrantRetrievalService()
        documents = retrieval_service.retrieve(query)

        if not documents:
            return "No relevant documents found."

        formatted_docs = []
        for doc in documents:
            formatted_docs.append(f"Content: {doc['content']}\nSource: {doc['metadata'].get('source', 'N/A')}")

        return "\n\n".join(formatted_docs)