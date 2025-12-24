# Quickstart Guide: Retrieval Pipeline Testing and Validation System

**Feature**: 006-retrieval-validation
**Created**: 2025-12-23
**Related Plan**: specs/006-retrieval-validation/plan.md

## Overview

This guide will help you set up and use the Retrieval Pipeline Testing and Validation System to validate RAG retrieval functionality by querying the Qdrant vector database and verifying results before agent integration.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning the repository)
- Cohere API key
- Qdrant Cloud access with API key

## Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install cohere qdrant-client python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following content:

```env
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=rag_embedding

# Optional Configuration
RETRIEVAL_TOP_K=5
RETRIEVAL_SIMILARITY_THRESHOLD=0.5
VALIDATION_ACCURACY_THRESHOLD=0.8
```

## Usage

### 1. Run Validation Tests
```bash
python -m retrieval_validation.test_suite
```
This will execute the test suite with predefined queries to validate retrieval accuracy.

### 2. Query the System
```bash
python -m retrieval_validation.query_client --query "Your search query here"
```
This will execute a single query against the vector database and return relevant results.

### 3. Generate Metrics
```bash
python -m retrieval_validation.metrics
```
This will generate performance and accuracy metrics for the retrieval system.

### 4. Run Specific Validation Test
```bash
python -m retrieval_validation.validation --test-query "What is RAG?" --expected-topics "retrieval, augmentation, generation"
```
This will run a specific validation test with expected results.

## Configuration Options

### Retrieval Configuration
- `RETRIEVAL_TOP_K`: Number of results to return (default: 5)
- `RETRIEVAL_SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)
- `VALIDATION_ACCURACY_THRESHOLD`: Minimum accuracy to pass validation (default: 0.8)

### Performance Configuration
- `QUERY_TIMEOUT`: Timeout for individual queries (default: 10 seconds)
- `BATCH_SIZE`: Number of queries to process in parallel (default: 1)

## Validation Process

### Test Suite Execution
The validation system runs 5+ test queries covering various book topics:
1. Technical concepts
2. Procedural instructions
3. Conceptual explanations
4. Code examples
5. Best practices

### Accuracy Measurement
- **Precision**: Percentage of relevant results in the returned set
- **Recall**: Percentage of all relevant results that were retrieved
- **Relevance Score**: Overall similarity between query and results

### Performance Metrics
- **Latency**: Time taken to execute queries
- **Throughput**: Queries processed per second
- **Success Rate**: Percentage of queries that completed successfully

## Verification

After running the validation system, verify that:

1. Queries return relevant content chunks within 2 seconds (SC-001)
2. Stored embeddings are validated with 99% integrity (SC-002)
3. Retrieval accuracy meets or exceeds 90% threshold (SC-003)
4. Complete pipeline validation succeeds at 95% rate (SC-004)

You can run the full validation suite to check these conditions automatically:
```bash
python -m retrieval_validation.full_validation
```

## Next Steps

Once validation is complete and successful:

1. Integrate with the agent system
2. Monitor performance in production
3. Continuously validate as new content is added