# Quickstart: Agent & Retrieval Integration

**Version**: 1.0
**Date**: 2025-12-17

This guide explains how to set up and run the Agent-Based RAG Chatbot service.

---

## 1. Prerequisites

-   Python 3.11+
-   `uv` package manager (or `pip`)
-   Access to a Qdrant instance with indexed data
-   OpenAI API Key (for agent framework)
-   Cohere API Key (if used for embedding within retrieval tool)

## 2. Setup

### Step 2.1: Initialize Project (UV)

Navigate to the `backend` directory, create a virtual environment, and install dependencies using `uv`.

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows: .\.venv\Scripts\activate
# On macOS/Linux: source ./.venv/bin/activate

# Install dependencies (uv manages dependencies from pyproject.toml)
uv pip install -e .
# Alternatively, if using requirements.txt:
# uv pip install -r requirements.txt
```
*(Note: The `pyproject.toml` or `requirements.txt` file will be updated to include `fastapi`, `uvicorn`, `qdrant-client`, `openai`, `langchain-openai`, `langchain-community`, `python-dotenv`, etc., as part of the implementation.)*

### Step 2.2: Configure Environment Variables

The service requires the following environment variables. Create a `.env` file in the `backend` directory to manage these.

```bash
# .env file

# OpenAI API Key for agent framework
OPENAI_API_KEY="your-openai-api-key"

# Qdrant Configuration for retrieval tool
QDRANT_HOST="your-qdrant-host.com"
QDRANT_API_KEY="your-qdrant-api-key"
QDRANT_COLLECTION="your-collection-name"

# Cohere API Key (if used by retrieval tool for embeddings)
# COHERE_API_KEY="your-cohere-api-key"
```

## 3. Running the Service

After setup and configuration, you can start the FastAPI application.

```bash
# From the backend directory
uvicorn main:app --reload
```
The service will be accessible at `http://127.0.0.1:8000`.

## 4. Interacting with the API

You can interact with the `/chat` endpoint using `curl` or a tool like Postman/Insomnia.

### Example 4.1: Full-Book Query

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What are the stages of physical AI development?"
         }'
```

### Example 4.2: Query with User-Provided Context

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "Summarize this text.",
           "context": "Physical AI development typically involves three main stages: perception, cognition, and action. Perception deals with how the AI gathers information from its environment using sensors. Cognition involves processing this information and making decisions. Action is the execution of these decisions through actuators."
         }'
```
