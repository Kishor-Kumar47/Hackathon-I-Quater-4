# main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.app.api import chat

app = FastAPI(
    title="Agent-Based RAG Chatbot",
    description="Backend service for an Agent-Based RAG Chatbot, integrating Qdrant retrieval and Gemini Agents SDK.",
    version="0.1.0",
)

# Define allowed origins for CORS
# In production, replace "http://localhost:3000" with your actual frontend domain
origins = [
    "http://localhost:3000",  # Docusaurus development server
    "[PRODUCTION_FRONTEND_URL]", # Placeholder for your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Agent-Based RAG Chatbot is running!"}

app.include_router(chat.router, prefix="/api")

# Placeholder for API routes