# Retrieval Pipeline Testing and Validation System

This system provides tools for querying Qdrant vector database, retrieving relevant content chunks, and verifying the complete pipeline works correctly before agent integration.

## Features

- Query Qdrant vector database based on semantic similarity
- Return retrieved content with appropriate metadata and scores
- Validate complete embedding pipeline from storage to retrieval
- Test retrieval accuracy by comparing expected vs actual outputs
- Handle database connectivity issues gracefully
- Include comprehensive logging and diagnostics
- Provide performance metrics for query execution
- Validate content integrity in stored embeddings
- Support configurable similarity thresholds

## Prerequisites

- Python 3.8+
- Qdrant vector database
- Cohere API key (for embeddings)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` file:
   ```
   QDRANT_HOST=your_qdrant_host
   QDRANT_PORT=6333
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_URL=your_qdrant_url
   COHERE_API_KEY=your_cohere_api_key
   LOG_LEVEL=INFO
   DEBUG=false
   ```

## Usage

### Command Line Interface

The system provides a command-line interface for various operations:

#### Query a single query
```bash
python -m app.main query --text "What is artificial intelligence?" --top-k 5
```

#### Run validation tests
```bash
python -m app.main validate --type comprehensive
```

#### Generate performance metrics
```bash
python -m app.main metrics
```

#### Start a new retrieval session
```bash
python -m app.main session
```

### As a Library

You can also use the system as a library in your Python code:

```python
from app.services.qdrant_retriever import QdrantRetrievalService

# Initialize the retrieval service
retrieval_service = QdrantRetrievalService()

# Retrieve similar content
results = retrieval_service.retrieve("Your query here", k=5)

# Process the results
for result in results:
    print(f"Content: {result['content']}")
    print(f"Score: {result['score']}")
    print(f"Metadata: {result['metadata']}")
```

## Architecture

The system is organized into the following components:

- `services/` - Core services for retrieval, validation, and metrics
- `models/` - Data models and schemas
- `api/` - API endpoints (if any)
- `tests/` - Test suites and validation tools

## Validation and Testing

The system includes comprehensive validation capabilities:

- Test queries covering various book topics
- Accuracy metrics (precision, recall, F1 score)
- Performance metrics (latency, throughput)
- End-to-end integration tests
- Functional requirements verification

## Performance Metrics

The system tracks various performance metrics:

- Query latency (average, median, 95th percentile, 99th percentile)
- Accuracy metrics (precision, recall, F1 score)
- Throughput measurements
- Time-series metrics for trend analysis

## Success Criteria

The system meets the following success criteria:

- 95% of test queries return relevant content within 2 seconds response time
- System validates 100% of stored embeddings with 99% integrity verification rate
- Retrieval accuracy meets or exceeds 90% relevance threshold in test scenarios
- Backend developers can successfully validate the complete pipeline with 95% success rate
- System provides comprehensive logging and diagnostic information for all validation processes

## Troubleshooting

If you encounter issues:

1. Check that all environment variables are properly set
2. Verify that the Qdrant database is accessible
3. Ensure that your Cohere API key is valid
4. Check the logs for detailed error information

## License

[Specify license information here]