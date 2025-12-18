# Function Contracts: Embedding Pipeline

## get_all_urls(base_url: str) -> List[str]
**Purpose**: Discover and return all valid URLs from a Docusaurus site
**Input**: Base URL of the Docusaurus site
**Output**: List of all discovered URLs
**Error Conditions**:
- Invalid URL format
- Network errors
- Site not accessible
**Side Effects**: None

## extract_text_from_url(url: str) -> Dict
**Purpose**: Extract clean text content from a single URL
**Input**: URL to extract content from
**Output**: Dictionary with 'content', 'title', and 'url' keys
**Error Conditions**:
- URL not accessible
- Content extraction fails
- Invalid HTML structure
**Side Effects**: Makes HTTP request to the provided URL

## chunk_text(text: str, chunk_size: int = 512) -> List[Dict]
**Purpose**: Split text into smaller chunks for embedding
**Input**: Text to chunk and optional chunk size
**Output**: List of dictionaries with 'text', 'start_pos', 'end_pos' keys
**Error Conditions**: None
**Side Effects**: None

## embed(texts: List[str]) -> List[List[float]]
**Purpose**: Generate embeddings for a list of texts using Cohere
**Input**: List of text strings to embed
**Output**: List of embedding vectors (lists of floats)
**Error Conditions**:
- Cohere API errors
- Rate limiting
- Invalid text input
**Side Effects**: Makes API calls to Cohere service

## create_collection(collection_name: str) -> bool
**Purpose**: Create a Qdrant collection for storing embeddings
**Input**: Name of the collection to create
**Output**: True if successful, False otherwise
**Error Conditions**:
- Qdrant connection errors
- Collection already exists
- Insufficient permissions
**Side Effects**: Creates a collection in Qdrant database

## save_chunk_to_qdrant(chunk: Dict, embedding: List[float]) -> bool
**Purpose**: Store a text chunk and its embedding in Qdrant
**Input**: Chunk data (with content and metadata) and its embedding vector
**Output**: True if successful, False otherwise
**Error Conditions**:
- Qdrant connection errors
- Invalid data format
- Storage capacity reached
**Side Effects**: Adds a point to the Qdrant collection

## main() -> None
**Purpose**: Execute the complete embedding pipeline
**Input**: None (reads from environment variables)
**Output**: None (writes to Qdrant database)
**Error Conditions**: Any of the above functions may fail
**Side Effects**: Processes all URLs, extracts content, generates embeddings, stores in Qdrant