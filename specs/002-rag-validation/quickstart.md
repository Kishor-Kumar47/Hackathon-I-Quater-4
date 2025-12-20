# Quickstart: RAG Retrieval Validation

**Version**: 1.0
**Date**: 2025-12-17

This guide explains how to set up and run the retrieval pipeline validation suite.

---

## 1. Prerequisites

-   Python 3.11+
-   Access to a Qdrant instance
-   A Cohere API key

## 2. Setup

### Step 2.1: Install Dependencies

Ensure you are in the `backend` directory and install the required Python packages.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```
*(Note: The `requirements.txt` file will be updated to include `qdrant-client` and `cohere` as part of the implementation.)*

### Step 2.2: Configure Environment Variables

The validation suite requires the following environment variables to be set. You can create a `.env` file in the `backend` directory to manage these.

```bash
# .env file

# Qdrant Configuration
QDRANT_HOST="your-qdrant-host.com"
QDRANT_API_KEY="your-qdrant-api-key"
QDRANT_COLLECTION="your-collection-name"

# Cohere Configuration
COHERE_API_KEY="your-cohere-api-key"
```

### Step 2.3: Create Golden Test Dataset

Place your golden test dataset file at the following location. The file must be a JSON array of objects conforming to the `GoldenTestCase` data model.

-   **Path**: `tests/fixtures/rag_validation_dataset.json`

An example entry in this file would be:
```json
[
  {
    "query": "How is the humanoid robot's visual perception system trained?",
    "expected_document_id": "doc_humanoid_vision_training_04",
    "justification": "This chunk specifically details the dataset and augmentation techniques for the vision model."
  }
]
```

## 3. Running the Validation

The validation suite is run using `pytest` from the root of the repository.

```bash
# From the repository root
pytest tests/test_rag_validation.py
```

## 4. Expected Output

A successful run will produce a summary report in your terminal, followed by `pytest`'s standard output.

### On Success

```text
============================= test session starts ==============================
...
tests/test_rag_validation.py::test_retrieval_pipeline_accuracy PASSED   [100%]

Validation Run Summary:
-----------------------
Total Test Cases: 50
Recall@K (K=10): 0.96
Mean Reciprocal Rank (MRR): 0.89
-----------------------

============================== 1 passed in 15.32s ==============================
```

### On Failure

If the `Recall@K` metric falls below the defined threshold, the test will fail. Additionally, any failing test cases will be logged to `stdout` as JSON objects during the run.

```text
...
tests/test_rag_validation.py::test_retrieval_pipeline_accuracy FAILED   [100%]
{"query": "What is the robot's power source?", "expected_document_id": "doc_power_source_01", "is_present_in_top_k": false, "rank": null, "retrieved_ids": ["doc_actuators_03", "doc_sensors_12", ...]}
...
>       assert summary["Recall@K"] >= 0.95
E       assert 0.94 >= 0.95
E        +  where 0.94 = <ValidationSummary>['Recall@K']

tests/test_rag_validation.py:25: AssertionError
```
