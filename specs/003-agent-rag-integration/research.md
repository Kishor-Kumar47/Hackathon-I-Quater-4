# Research: Agent & Retrieval Integration Implementation

**Date**: 2025-12-17
**Author**: Gemini

This document resolves open questions identified during the initial planning phase for the Agent-Based RAG Chatbot feature.

---

### 1. OpenAI Agents SDK Version/Component

-   **Unknown**: What is the specific OpenAI Agents SDK version/component to be used for the agent's core conversational logic?
-   **Decision**: Utilize `langchain-openai-agents` (a robust Python library implementing OpenAI Agents concepts) and specifically the `AgentExecutor` for managing conversational flow and tool invocation.
-   **Rationale**: LangChain provides a high-level abstraction that simplifies the development of agents, tools, and chains. `AgentExecutor` is designed for complex reasoning over multiple steps, dynamically selecting tools (like retrieval from Qdrant) based on user input. This choice aligns with the goal of building an intelligent conversational agent.
-   **Alternatives Considered**: Direct OpenAI API calls for agents. This would require more manual management of state, tool definitions, and conversational turns, increasing complexity and development time.

---

### 2. API Request Payload Structures

-   **Unknown**: What is the expected structure of the API request payloads for "full-book queries" and "user-selected text-only queries"?
-   **Decision**:
    -   **Full-Book Query Payload**: A JSON object with a single `query` field.
        ```json
        {
          "query": "string"
        }
        ```
    -   **User-Selected Text Query Payload**: A JSON object with a `query` field and an additional `context` field containing the user-selected text.
        ```json
        {
          "query": "string",
          "context": "string"
        }
        ```
-   **Rationale**: This approach provides clear, explicit API contracts for both modes of operation. The presence or absence of the `context` field naturally differentiates between full-book retrieval and user-provided context.
-   **Alternatives Considered**: Using a single API endpoint with optional fields and relying on logic to infer the mode. While technically feasible, it can lead to more ambiguous API usage and more complex validation logic within the service.

---

