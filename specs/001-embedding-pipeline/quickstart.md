# Quickstart: Embedding Pipeline

## Prerequisites
- Python 3.11 or higher
- UV package manager
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   # Or if starting fresh:
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here  # Optional, defaults to localhost
   QDRANT_API_KEY=your_qdrant_api_key_here  # Optional
   TARGET_URL=https://hackathon-i-quater-4.vercel.app/  # The Docusaurus site to process
   ```

4. **Run the pipeline**
   ```bash
   python backend/main.py
   ```

## Configuration

The pipeline can be configured through environment variables:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL of your Qdrant instance (default: http://localhost:6333)
- `QDRANT_API_KEY`: API key for Qdrant authentication (if required)
- `TARGET_URL`: The base URL of the Docusaurus site to process
- `COHERE_MODEL`: Cohere model to use (default: embed-multilingual-v2.0)
- `CHUNK_SIZE`: Size of text chunks (default: 512)

## Usage

The main.py file contains the following key functions:

- `get_all_urls(base_url)`: Discovers all URLs from the Docusaurus site
- `extract_text_from_url(url)`: Extracts clean text content from a single URL
- `chunk_text(text, chunk_size=512)`: Splits text into manageable chunks
- `embed(texts)`: Generates embeddings for a list of texts using Cohere
- `create_collection(collection_name)`: Creates a Qdrant collection named "rag_embedding"
- `save_chunk_to_qdrant(chunk, embedding)`: Stores a chunk and its embedding in Qdrant
- `main()`: Executes the complete pipeline end-to-end

## Example

To run the pipeline with a specific URL:
```bash
TARGET_URL=https://your-docusaurus-site.com python backend/main.py
```

## Verification

After running the pipeline, verify that:
1. All URLs from the target site have been processed
2. Text content has been extracted cleanly
3. Embeddings have been generated successfully
4. Data has been stored in the Qdrant collection named "rag_embedding"