# Embedding Pipeline

Backend pipeline to extract text from deployed Docusaurus URLs, generate embeddings using Cohere, and store them in Qdrant for RAG-based retrieval.

## Overview

This pipeline extracts clean text content from Docusaurus documentation sites, generates vector embeddings using Cohere's API, and stores them in Qdrant vector database for RAG-based retrieval systems.

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies using UV package manager:
   ```bash
   uv pip install -r requirements.txt
   # Or if using uv project:
   uv sync
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your API keys and configuration

## Usage

Run the pipeline with:
```bash
python main.py
```

Or specify a custom URL:
```bash
python main.py --url https://your-docusaurus-site.com
```

For verbose logging:
```bash
python main.py --verbose
```

## Configuration

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant instance (default: http://localhost:6333)
- `QDRANT_API_KEY`: API key for Qdrant authentication (if required)
- `TARGET_URL`: The base URL of the Docusaurus site to process
- `COHERE_MODEL`: Cohere model to use (default: embed-multilingual-v2.0)
- `CHUNK_SIZE`: Size of text chunks (default: 512)

## Features

- Docusaurus URL crawling and text extraction
- Content cleaning and preprocessing
- Text chunking for optimal embedding
- Cohere embedding generation
- Qdrant vector storage with metadata
- Error handling and retry mechanisms
- Progress tracking and logging

## Example Usage

Process a specific Docusaurus site:
```bash
python main.py --url https://docusaurus.io/docs
```

Process with verbose output:
```bash
python main.py --url https://example-docusaurus-site.com --verbose
```

## Architecture

The pipeline follows these steps:
1. Discovers all URLs from the target Docusaurus site using sitemap.xml or navigation links
2. Extracts clean text content from each URL, preserving titles and structure
3. Chunks the text into manageable segments for embedding
4. Generates vector embeddings using Cohere's API
5. Stores embeddings in Qdrant with metadata for retrieval