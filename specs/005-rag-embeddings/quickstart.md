# Quickstart Guide: RAG Embeddings System

**Feature**: 005-rag-embeddings
**Created**: 2025-12-23
**Related Plan**: specs/005-rag-embeddings/plan.md

## Overview

This guide will help you set up and run the RAG Embeddings System to extract content from a Docusaurus website, generate embeddings using Cohere API, and store them in Qdrant Cloud.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning the repository)

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
pip install cohere qdrant-client playwright python-dotenv tiktoken
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Configure Environment Variables
Create a `.env` file in the project root with the following content:

```env
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Docusaurus Site Configuration
DOCUSAURUS_URL=https://your-docusaurus-site.com

# Optional Configuration
CHUNK_SIZE_MIN=500
CHUNK_SIZE_MAX=1000
CHUNK_OVERLAP=100
COHERE_MODEL=embed-multilingual-v2.0
QDRANT_COLLECTION_NAME=docusaurus_embeddings
BATCH_SIZE=96
```

## Usage

### 1. Run Content Extraction
```bash
python -m rag_embeddings.scraper
```
This will extract content from all pages of your Docusaurus site specified in `DOCUSAURUS_URL`.

### 2. Process and Chunk Content
```bash
python -m rag_embeddings.chunker
```
This will split the extracted content into appropriately sized chunks (500-1000 tokens).

### 3. Generate Embeddings
```bash
python -m rag_embeddings.embedder
```
This will generate embeddings using the Cohere API in batches of 96.

### 4. Store in Qdrant
```bash
python -m rag_embeddings.storage
```
This will create a Qdrant collection and store the embeddings with metadata.

### 5. Verify the System
```bash
python -m rag_embeddings.verify
```
This will run test queries to verify that embeddings can be retrieved successfully.

## Complete Pipeline
To run the entire pipeline in one command:
```bash
python -m rag_embeddings.pipeline
```

## Configuration Options

### Chunking Configuration
- `CHUNK_SIZE_MIN`: Minimum tokens per chunk (default: 500)
- `CHUNK_SIZE_MAX`: Maximum tokens per chunk (default: 1000)
- `CHUNK_OVERLAP`: Overlap tokens between chunks (default: 100)

### API Configuration
- `BATCH_SIZE`: Number of texts to process per API call (max 96 for Cohere)
- `COHERE_MODEL`: Model name for embedding generation
- `RATE_LIMIT_DELAY`: Delay between API calls to respect rate limits

### Qdrant Configuration
- `QDRANT_COLLECTION_NAME`: Name of the collection to create
- `VECTOR_DISTANCE`: Distance metric (Cosine, Euclid, Dot)

## Error Handling

### Common Issues

1. **API Rate Limits**: The system implements automatic backoff. If you see rate limit errors, ensure your delay settings are appropriate.

2. **Network Issues**: The scraper has built-in retry mechanisms. Check your internet connection and the target site's availability.

3. **Authentication**: Verify that your API keys are correct and have the necessary permissions.

### Logging
The system logs all operations to `logs/` directory. Check these files for detailed information about any issues:

- `logs/scraper.log`: Content extraction logs
- `logs/chunker.log`: Chunking process logs
- `logs/embedder.log`: Embedding generation logs
- `logs/storage.log`: Storage process logs

## Verification

After running the pipeline, verify that:

1. Content was extracted from all expected pages
2. Embeddings were generated for all chunks
3. All embeddings were stored in Qdrant
4. Test queries return relevant results

You can run the verification script to check these conditions automatically:
```bash
python -m rag_embeddings.verify
```

## Next Steps

Once the embeddings are stored in Qdrant, you can:

1. Build a RAG chatbot that queries the stored embeddings
2. Create a search interface that uses vector similarity
3. Implement a content recommendation system