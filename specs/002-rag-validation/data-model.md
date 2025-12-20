# Data Model: Retrieval Pipeline Validation

**Version**: 1.0
**Date**: 2025-12-17

This document defines the data structures used in the RAG retrieval validation process, based on the feature specification and research findings.

---

### 1. GoldenTestCase

Represents a single, manually-defined test case used as ground truth for validation.

-   **Source**: `tests/fixtures/rag_validation_dataset.json`
-   **Schema**:
    ```json
    {
      "query": "string",
      "expected_document_id": "string",
      "justification": "string"
    }
    ```
-   **Fields**:
    -   `query`: The natural language question to be tested.
    -   `expected_document_id`: The unique ID of the document chunk that is considered the correct answer.
    -   `justification`: A human-readable note explaining why the document is correct.

---

### 2. RetrievedChunk

Represents a single document chunk as retrieved from the Qdrant vector database.

-   **Source**: Qdrant search result payload.
-   **Schema**:
    ```python
    # Represents the payload of a qdrant_client.models.ScoredPoint
    class RetrievedChunk:
        id: str  # Qdrant point ID
        document_id: str # The custom document ID from the payload
        text: str
        score: float
    ```
-   **Fields**:
    -   `id`: The internal UUID used by Qdrant to identify the point.
    -   `document_id`: The application-specific ID for the document chunk. **This is used to match against `GoldenTestCase.expected_document_id`**.
    -   `text`: The raw text content of the chunk.
    -   `score`: The similarity score returned by Qdrant.

---

### 3. ValidationResult

Represents the outcome of a single test case execution. Failed results are logged to `stdout`.

-   **Format**: JSON (for logging)
-   **Schema**:
    ```json
    {
      "query": "string",
      "expected_document_id": "string",
      "is_present_in_top_k": "boolean",
      "rank": "integer | null",
      "retrieved_ids": ["string"]
    }
    ```
-   **Fields**:
    -   `query`: The original query from the `GoldenTestCase`.
    -   `expected_document_id`: The expected document ID.
    -   `is_present_in_top_k`: `true` if the expected ID was in the top K results, otherwise `false`.
    -   `rank`: The 1-indexed position of the expected document in the search results. `null` if not found.
    -   `retrieved_ids`: A list of the actual `document_id`s retrieved from Qdrant, for debugging.

---

### 4. ValidationSummary

Represents the final summary report after running the entire test suite.

-   **Format**: Text (printed to `stdout` at the end of the run)
-   **Schema**:
    ```text
    Validation Run Summary:
    -----------------------
    Total Test Cases: <integer>
    Recall@K (K=<integer>): <float>
    Mean Reciprocal Rank (MRR): <float>
    -----------------------
    ```
