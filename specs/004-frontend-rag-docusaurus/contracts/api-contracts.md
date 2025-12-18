# API Contracts: Frontend-Backend Integration for RAG Chatbot

**Version**: 1.0
**Date**: 2025-12-18

This document details the frontend's interaction with the existing FastAPI RAG backend's API endpoints.

---

### 1. Chat Endpoint Interaction

The Docusaurus frontend will communicate with the backend's `/api/chat` endpoint to send user queries and receive agent responses. This directly leverages the backend's `api-contracts.md` (defined in `specs/003-agent-rag-integration/contracts/api-contracts.md`).

-   **Backend Endpoint Reference**: `specs/003-agent-rag-integration/contracts/api-contracts.md`
-   **Frontend Action**: Send `POST` request to `[BACKEND_BASE_URL]/api/chat`
-   **Request Body**: `FrontendQueryRequest` (as defined in `data-model.md`, maps to `AgentQueryRequest` in backend)
    ```json
    {
      "query": "string",
      "context": "string | null"
    }
    ```
-   **Expected Response (200 OK)**: `BackendAgentResponse` (as defined in `data-model.md`, maps to `AgentResponse` in backend)
    ```json
    {
      "answer": "string"
    }
    ```
-   **Error Responses**:
    -   **400 Bad Request**: Indicates invalid input from the frontend.
    -   **500 Internal Server Error**: Indicates an issue with the backend's processing.
    -   Frontend MUST handle these errors and display user-friendly messages (FR-006).

---

### 2. CORS Configuration (Backend)

The FastAPI backend must be configured to allow Cross-Origin Resource Sharing (CORS) requests from the Docusaurus frontend.

-   **Requirement Reference**: FR-005
-   **Policy**: Explicit origin whitelist.
-   **Allowed Origins**:
    -   Local development: `http://localhost:3000` (default Docusaurus dev server).
    -   Production: `[PRODUCTION_FRONTEND_URL]` (configured based on deployment).
-   **Allowed Methods**: `POST`.
-   **Allowed Headers**: `Content-Type`.

---

### 3. HTTPS Enforcement

In production, all communication between the Docusaurus frontend and FastAPI backend MUST occur over HTTPS. This will typically be handled by a reverse proxy (as per research.md).

-   **Requirement Reference**: FR-005
-   **Mechanism**: Reverse proxy configuration (e.g., Nginx, Caddy, cloud load balancer).
