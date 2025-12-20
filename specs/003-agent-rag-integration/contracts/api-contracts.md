# API Contracts: Agent & Retrieval Integration

**Version**: 1.0
**Date**: 2025-12-17

This document defines the API endpoints and their contracts for the Agent-Based RAG Chatbot.

---

### 1. Chat Endpoint

This endpoint allows users to interact with the RAG agent by sending queries and receiving generated answers.

-   **Path**: `/chat`
-   **Method**: `POST`
-   **Description**: Receives a user query and optionally a context snippet, then uses an agent with retrieval capabilities to generate a grounded response.
-   **Request Body**: `AgentQueryRequest` (from `data-model.md`)
    ```json
    {
      "query": "string",
      "context": "string | null"
    }
    ```
-   **Responses**:
    -   **200 OK**: Successful response with the agent's answer.
        -   **Body**: `AgentResponse` (from `data-model.md`)
            ```json
            {
              "answer": "string"
            }
            ```
    -   **400 Bad Request**: Invalid input or missing required fields.
        -   **Body**: Standard FastAPI error response (e.g., `{"detail": "Validation Error"}`)
    -   **500 Internal Server Error**: An unexpected error occurred on the server.
        -   **Body**: Standard FastAPI error response.
