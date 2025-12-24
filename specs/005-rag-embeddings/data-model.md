
# Data Model: RAG Embeddings System

**Feature**: 005-rag-embeddings
**Created**: 2025-12-23
**Related Plan**: specs/005-rag-embeddings/plan.md

## Entity: DocumentChunk

### Description
Represents a segment of extracted content that will be converted to an embedding vector. This is the primary data structure that flows through the entire pipeline.

### Fields
- **id** (string, required)
  - Unique identifier for the chunk
  - Generated as UUID or hash of content + source
- **content** (string, required)
  - The text content of the chunk
  - Cleaned and processed text ready for embedding
- **source_url** (string, required)
  - URL of the original document
  - Full URL where the content was extracted from
- **title** (string, required)
  - Title of the source document
  - Extracted from page title or heading
- **headings** (array of strings, optional)
  - Hierarchy of headings in the document
  - Ordered from highest to lowest level (e.g., ["Introduction", "Getting Started"])
- **created_at** (datetime, required)
  - Timestamp of chunk creation
  - ISO 8601 format
- **metadata** (object, optional)
  - Additional metadata key-value pairs
  - Can include author, tags, categories, etc.
- **token_count** (integer, optional)
  - Number of tokens in the content
  - Calculated during chunking process

### Validation Rules
- Content must be between 10 and 1500 tokens
- Source URL must be a valid URL format
- Created timestamp must be current or past
- Headings array must not exceed 10 levels deep

### Relationships
- One-to-many with EmbeddingVector (one chunk can have multiple vector representations)
- Belongs to ProcessingJob (tracks which job created this chunk)

## Entity: EmbeddingVector

### Description
Represents the vector embedding of a document chunk, stored in the vector database for similarity search.

### Fields
- **vector_id** (string, required)
  - Unique identifier for the vector in Qdrant
  - Usually matches the DocumentChunk.id
- **vector** (array of floats, required)
  - The embedding vector values
  - Array of float values representing the semantic meaning
- **document_chunk_id** (string, required)
  - Reference to the source DocumentChunk
  - Links back to the original content
- **model_name** (string, required)
  - Name of the model used to generate the embedding
  - e.g., "embed-multilingual-v2.0"
- **created_at** (datetime, required)
  - Timestamp when embedding was generated
  - ISO 8601 format

### Validation Rules
- Vector must have consistent dimensions (e.g., 768, 1024, etc.)
- Document chunk reference must exist
- Model name must be a valid Cohere model

### Relationships
- Belongs to DocumentChunk (the source content)
- Stored in QdrantCollection (the vector database collection)

## Entity: ProcessingJob

### Description
Tracks the progress and status of a full pipeline run from content extraction to vector storage.

### Fields
- **job_id** (string, required)
  - Unique identifier for the processing job
  - Generated as UUID
- **status** (string, required)
  - Current status: "pending", "extracting", "chunking", "embedding", "storing", "completed", "failed"
- **progress** (integer, required)
  - Progress percentage (0-100)
- **total_chunks** (integer, optional)
  - Total number of chunks to process
- **processed_chunks** (integer, optional)
  - Number of chunks processed
- **source_url** (string, required)
  - URL of the Docusaurus site being processed
- **start_time** (datetime, required)
  - When the job started
  - ISO 8601 format
- **end_time** (datetime, optional)
  - When the job completed or failed
  - ISO 8601 format
- **error_message** (string, optional)
  - Error details if status is "failed"
- **stats** (object, optional)
  - Processing statistics (timing, success rates, etc.)

### Validation Rules
- Status must be one of the defined values
- Progress must be between 0 and 100
- Start time must be before end time (if end time exists)
- Total chunks must be >= processed chunks

### Relationships
- One-to-many with DocumentChunk (chunks created by this job)
- One-to-many with EmbeddingVector (vectors created by this job)

## Entity: QdrantCollection

### Description
Represents the vector database collection where embeddings are stored.

### Fields
- **collection_name** (string, required)
  - Name of the Qdrant collection
  - Should follow Qdrant naming conventions
- **vector_size** (integer, required)
  - Dimension of the vectors in this collection
  - Must match the embedding model output size
- **distance_metric** (string, required)
  - Distance metric used: "Cosine", "Euclidean", "Dot"
  - Usually "Cosine" for embeddings
- **created_at** (datetime, required)
  - When the collection was created
  - ISO 8601 format
- **configuration** (object, optional)
  - Additional Qdrant collection configuration
  - Indexing settings, etc.

### Validation Rules
- Collection name must follow Qdrant naming rules
- Vector size must match embedding dimensions
- Distance metric must be supported by Qdrant

### Relationships
- One-to-many with EmbeddingVector (vectors stored in this collection)

## Entity: ScrapingConfig

### Description
Configuration settings for the web scraping process.

### Fields
- **base_url** (string, required)
  - Root URL of the Docusaurus site
- **allowed_paths** (array of strings, optional)
  - URL patterns to include in scraping
  - Default: all paths
- **blocked_paths** (array of strings, optional)
  - URL patterns to exclude from scraping
  - Default: none
- **selectors** (object, optional)
  - CSS selectors for content extraction
  - Default: standard Docusaurus selectors
- **delay_range** (array of floats, optional)
  - Min/max delay between requests (for rate limiting)
  - Format: [min, max] in seconds
- **timeout** (integer, optional)
  - Request timeout in seconds
  - Default: 30

### Validation Rules
- Base URL must be a valid URL
- Delay range values must be positive
- Timeout must be between 5 and 60 seconds

### Relationships
- Used by ProcessingJob (each job uses specific config)

## Entity: EmbeddingConfig

### Description
Configuration settings for the embedding generation process.

### Fields
- **model_name** (string, required)
  - Name of the Cohere embedding model
  - e.g., "embed-multilingual-v2.0"
- **batch_size** (integer, required)
  - Number of texts to process in each API call
  - Maximum: 96 for Cohere
- **truncate** (string, optional)
  - How to handle long texts: "START", "END", "NONE"
  - Default: "END"
- **api_key** (string, required)
  - Cohere API key (stored securely)
- **rate_limit_delay** (float, optional)
  - Delay between batches to respect rate limits
  - Default: 1.0 second

### Validation Rules
- Model name must be a valid Cohere model
- Batch size must be between 1 and 96
- Rate limit delay must be positive

### Relationships
- Used by ProcessingJob (each job uses specific config)

## State Transitions

### ProcessingJob Status Transitions
```
pending → extracting → chunking → embedding → storing → completed
                    ↓              ↓           ↓           ↓
                    → failed ←─────────────────────────────
```

- Jobs can transition to "failed" from any processing state
- Once "failed" or "completed", status is final
- Progress increases monotonically during processing

## Indexes and Performance Considerations

### DocumentChunk
- Index on source_url for quick lookup by source
- Index on created_at for chronological queries
- Full-text index on content for search capabilities

### EmbeddingVector
- Primary index on vector_id (for Qdrant compatibility)
- Index on document_chunk_id for content lookup
- Qdrant automatically creates vector index for similarity search

### ProcessingJob
- Index on status for monitoring active jobs
- Index on start_time for chronological tracking
- Index on source_url for site-specific queries