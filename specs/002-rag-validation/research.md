# Research: Retrieval Pipeline Validation

**Date**: 2025-12-17
**Author**: Gemini

This document resolves open questions identified during the initial planning phase for the RAG retrieval validation feature.

---

### 1. Cohere Embedding Model Selection

-   **Unknown**: What is the specific Cohere embedding model to be used?
-   **Decision**: Use Cohere model `embed-english-light-v3.0`.
-   **Rationale**: This model provides a strong balance of retrieval quality and performance (latency, cost), making it suitable for a validation suite that may be run frequently. The 'light' version is sufficient to prove the pipeline is working.
-   **Alternatives Considered**: `embed-english-v3.0`. This model is more powerful but has higher latency and cost, which is unnecessary for this validation context.

---

### 2. Qdrant Collection Name

-   **Unknown**: What is the name of the Qdrant collection to be queried?
-   **Decision**: The collection name will be supplied via an environment variable: `QDRANT_COLLECTION`.
-   **Rationale**: This decouples the validation logic from environment-specific configuration (e.g., `dev-collection`, `prod-collection`), preventing hardcoded values and improving flexibility.
-   **Alternatives Considered**: Hardcoding the name in the script. This is brittle and would require code changes to run against different collections.

---

### 3. Qdrant Metadata Structure

-   **Unknown**: What is the specific structure of the metadata stored alongside the vectors in Qdrant?
-   **Decision**: The metadata payload in Qdrant must contain at least `document_id` (string) and `text` (string).
-   **Rationale**: The `document_id` is required for matching against the golden dataset. The `text` is essential for logging and debugging, allowing engineers to immediately inspect the content of a retrieved chunk.
-   **Alternatives Considered**: Storing only the `document_id`. This would make debugging failed test cases significantly more difficult, as it would require a separate lookup to get the content.

---

### 4. Golden Test Dataset Location

-   **Unknown**: Where is the golden test dataset located?
-   **Decision**: The dataset will be a JSON file located at `tests/fixtures/rag_validation_dataset.json`.
-   **Rationale**: Co-locating test fixtures with the testing code is a standard practice that improves project organization and discoverability.
-   **Alternatives Considered**: Storing the dataset within the `specs` directory. This blurs the line between specification artifacts and test assets.

---

### 5. Logging Strategy

-   **Unknown**: What is the logging destination and format for failed validation cases?
-   **Decision**: Failed test cases will be logged to `stdout` as a JSON object for each failure.
-   **Rationale**: Logging structured JSON to `stdout` is a modern, CI/CD-friendly approach. It allows for easy redirection, parsing, and integration with other tools without requiring file I/O management.
-   **Alternatives Considered**: Logging to a dedicated file (e.g., `validation.log`). This adds complexity around file path management, rotation, and cleanup.
