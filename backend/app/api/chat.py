# backend/app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.models.chat import AgentQueryRequest, AgentResponse
from backend.app.services.agent import RAGAgent

router = APIRouter()

@router.post("/chat", response_model=AgentResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(request: AgentQueryRequest):
    """
    Handles chat queries for the RAG agent.
    """
    try:
        agent_instance = RAGAgent()
        response = agent_instance.process_query(request.query, request.context)
        return AgentResponse(answer=response["answer"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
