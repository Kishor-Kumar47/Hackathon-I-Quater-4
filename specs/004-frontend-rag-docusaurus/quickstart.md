# Quickstart: Frontend-Backend Integration for RAG Chatbot

**Version**: 1.0
**Date**: 2025-12-18

This guide explains how to set up and run both the Docusaurus frontend and FastAPI RAG backend for local development.

---

## 1. Prerequisites

-   Node.js (LTS version recommended)
-   Python 3.11+
-   `uv` package manager (or `npm`/`yarn`/`pip`)
-   Access to a Qdrant instance with indexed data (backend requirement)
-   OpenAI API Key (backend requirement)

## 2. Setup

### Step 2.1: Backend Setup

Navigate to the `backend` directory and follow its quickstart guide to set up the Python environment and install dependencies.

```bash
# From project root
cd backend
# Refer to backend/quickstart.md for detailed setup instructions
# Example:
# uv venv
# .\.venv\Scripts\activate  # Windows
# source ./.venv/bin/activate # macOS/Linux
# uv pip install -e .
```

### Step 2.2: Frontend Setup (Docusaurus)

Navigate to the `my-website` directory and install its Node.js dependencies.

```bash
# From project root
cd my-website

# Install Node.js dependencies
npm install # or yarn install
```

### Step 2.3: Configure Environment Variables

The backend service requires environment variables. Ensure your `.env` file in the `backend` directory is configured as per the backend's quickstart guide.

```bash
# .env file (located in backend/ directory)

# OpenAI API Key for agent framework
OPENAI_API_KEY="your-openai-api-key"

# Qdrant Configuration for retrieval tool
QDRANT_HOST="your-qdrant-host.com"
QDRANT_API_KEY="your-qdrant-api-key"
QDRANT_COLLECTION="your-collection-name"
```
*(Note: For local development, the Docusaurus frontend will typically access the backend on `http://localhost:8000/api`. Ensure no explicit API key is required from the frontend for local testing unless specifically implemented.)*

## 3. Running Services for Local Development

To test the integration locally, you need to run both the backend and the frontend simultaneously.

### Step 3.1: Run the Backend Service

```bash
# From project root
cd backend
uvicorn main:app --reload
```
The backend will be accessible at `http://127.0.0.1:8000`.

### Step 3.2: Run the Docusaurus Frontend

Open a new terminal window/tab.

```bash
# From project root
cd my-website
npm start
```
The Docusaurus frontend will typically be accessible at `http://localhost:3000`.

## 4. Testing the Integration

-   Navigate to `http://localhost:3000` in your web browser.
-   Locate the integrated chat UI component (once implemented).
-   Type a query into the chat input and observe the response from the RAG agent.
-   (Once implemented) Select text on a Docusaurus page and use the contextual UI to send a query with selected text.
