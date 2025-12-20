# backend/app/services/qdrant_retriever.py

import os
from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from langchain_core.tools import BaseTool
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class QdrantRetrievalService:
    def __init__(self):
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION")
        self.embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs a similarity search in Qdrant and returns the retrieved documents.

        Args:
            query: The search query string.
            k: The number of top relevant documents to retrieve.

        Returns:
            A list of dictionaries, each representing a retrieved document.
        """
        query_embedding = self.embeddings_model.embed_query(query)
        
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
    name = "qdrant_retriever"
    description = (
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

