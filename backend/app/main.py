import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv(dotenv_path)

# Create the main FastAPI application
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based chatbot using OpenAI and Qdrant",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add exposed headers to allow all headers to be read by frontend
    allow_origin_regex=None,
    # Add max age to cache preflight requests
    max_age=600,
)

# Include API routes
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RAG Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)