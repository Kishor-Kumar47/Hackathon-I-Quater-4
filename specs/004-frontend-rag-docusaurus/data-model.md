# Data Model: Frontend-Backend Integration for RAG Chatbot

**Version**: 1.0
**Date**: 2025-12-18

This document defines the data structures used for communication between the Docusaurus frontend and the FastAPI RAG backend, referencing the existing backend data models where applicable.

---

### 1. FrontendQueryRequest

Represents the data sent from the Docusaurus frontend to the FastAPI backend. This directly maps to the `AgentQueryRequest` Pydantic model defined in the backend.

-   **Source**: Docusaurus frontend UI interaction.
-   **Backend Mapping**: `backend/app/models/chat.AgentQueryRequest`
-   **Schema**:
    ```typescript
    interface FrontendQueryRequest {
      query: string; // The user's question or query.
      context?: string | null; // Optional: User-provided text context.
    }
    ```
-   **Fields**:
    -   `query`: The user's question.
    -   `context`: Optional user-selected text.

---

### 2. BackendAgentResponse

Represents the data received by the Docusaurus frontend from the FastAPI backend. This directly maps to the `AgentResponse` Pydantic model defined in the backend.

-   **Source**: FastAPI backend API response.
-   **Backend Mapping**: `backend/app/models/chat.AgentResponse`
-   **Schema**:
    ```typescript
    interface BackendAgentResponse {
      answer: string; // The RAG agent's answer.
    }
    ```
-   **Fields**:
    -   `answer`: The agent's generated answer.

---

### 3. Frontend Chat State (Internal)

Represents the internal state managed by the Docusaurus chat UI component.

-   **Source**: Docusaurus frontend React component.
-   **Schema**:
    ```typescript
    interface ChatMessage {
      id: string; // Unique identifier for the message
      sender: 'user' | 'agent'; // Who sent the message
      text: string; // The content of the message
      mode?: 'Full Book Search' | 'Context from Selection'; // Visual indicator (FR-004)
      timestamp: Date; // When the message was sent
    }

    interface ChatState {
      messages: ChatMessage[];
      inputQuery: string;
      selectedContext: string | null; // User-selected text from the page
      isLoading: boolean;
      error: string | null;
    }
    ```
-   **Fields**:
    -   `messages`: Array of chat messages.
    -   `inputQuery`: Current text in the input field.
    -   `selectedContext`: User-selected text from the page.
    -   `isLoading`: Boolean to indicate if a backend request is in progress.
    -   `error`: Any error message to display.
