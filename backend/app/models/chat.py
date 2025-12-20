# backend/app/models/chat.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentQueryRequest(BaseModel):
    query: str = Field(..., description="The user's question or query.")
    context: Optional[str] = Field(None, description="Optional: User-provided text context for the query. If provided, the agent uses this instead of retrieving from the vector database.")

class AgentResponse(BaseModel):
    answer: str = Field(..., description="The agent's answer to the query, grounded in the provided context.")

class RetrievalToolInput(BaseModel):
    query: str = Field(..., description="The query string used for retrieval from the vector database.")
    k: int = Field(5, description="The number of top relevant chunks to retrieve.")

class RetrievedDocument(BaseModel):
    id: str = Field(..., description="Unique identifier of the document chunk.")
    content: str = Field(..., description="The text content of the document chunk.")
    score: float = Field(..., description="Similarity score from the vector database.")
    metadata: Dict[str, Any] = Field({}, description="Additional metadata associated with the chunk.")
