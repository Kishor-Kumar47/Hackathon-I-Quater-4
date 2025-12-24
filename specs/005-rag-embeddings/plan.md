# Implementation Plan: RAG Embeddings System

**Feature**: 005-rag-embeddings
**Created**: 2025-12-23
**Status**: Draft
**Spec**: specs/005-rag-embeddings/spec.md

## Technical Context

This implementation will create a system to extract content from a deployed Docusaurus website, generate embeddings using the Cohere API, and store them in a Qdrant Cloud vector database. The system will be built as a pipeline with the following components:

- **Web Scraper**: Extracts content from Docusaurus pages
- **Content Chunker**: Splits content into appropriate chunks for embedding
- **Embedding Generator**: Uses Cohere API to generate vector embeddings
- **Vector Storage**: Stores embeddings in Qdrant Cloud with metadata
- **Verification System**: Tests retrieval capabilities

## Constitution Check

Based on the project constitution principles:
- **Test-First**: All components will have comprehensive unit and integration tests
- **Observability**: Structured logging will be implemented throughout the pipeline
- **Simplicity**: Start with basic implementation and add complexity as needed

## Gates

- **Security**: API keys will be handled securely via environment variables
- **Performance**: System will implement batching and rate limiting for API calls
- **Reliability**: Error handling and retry mechanisms will be implemented throughout

---

## Phase 0: Research & Analysis

### Research Tasks

#### R0.1: Web Scraping Technology Selection
**Research**: Compare BeautifulSoup vs Playwright for Docusaurus content extraction

**Decision**: Use Playwright for better JavaScript rendering support in modern Docusaurus sites
**Rationale**: Docusaurus sites often use client-side rendering, requiring a browser-based scraper
**Alternatives considered**:
- BeautifulSoup with requests (simpler but may miss dynamic content)
- Selenium (heavier than needed)

#### R0.2: Token Counting Method
**Research**: Determine accurate token counting for content chunking

**Decision**: Use tiktoken library to count tokens similar to how Cohere counts them
**Rationale**: Ensures chunks stay within API limits and are optimally sized
**Alternatives considered**:
- Character-based chunking (less accurate)
- Simple word count (not precise enough)

#### R0.3: Qdrant Cloud Configuration
**Research**: Best practices for Qdrant collection setup and vector indexing

**Decision**: Create collection with cosine similarity and appropriate vector dimensions
**Rationale**: Cosine similarity is standard for embedding comparisons
**Alternatives considered**:
- Euclidean distance (less suitable for high-dimensional embeddings)

---

## Phase 1: Design & Architecture

### Data Model: data-model.md

#### DocumentChunk Entity
- **id**: Unique identifier for the chunk
- **content**: The text content of the chunk (string)
- **embedding**: Vector representation of the content (float array)
- **source_url**: URL of the original document (string)
- **title**: Title of the source document (string)
- **headings**: Hierarchy of headings in the document (string array)
- **created_at**: Timestamp of creation (datetime)
- **metadata**: Additional metadata (key-value pairs)

#### EmbeddingVector Entity
- **vector_id**: Unique identifier for the vector
- **vector**: The embedding vector values (float array)
- **document_id**: Reference to the source document chunk
- **collection_name**: Name of the Qdrant collection

#### ProcessingStatus Entity
- **job_id**: Unique identifier for the processing job
- **status**: Current status (pending, processing, completed, failed)
- **progress**: Progress percentage (0-100)
- **total_chunks**: Total number of chunks to process
- **processed_chunks**: Number of chunks processed
- **error_message**: Error details if status is failed

### API Contracts

#### Cohere Embedding Service
```yaml
# OpenAPI 3.0 specification
openapi: 3.0.0
info:
  title: Cohere Embedding Service
  version: 1.0.0

paths:
  /embed:
    post:
      summary: Generate embeddings for text chunks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                texts:
                  type: array
                  items:
                    type: string
                  description: Text chunks to generate embeddings for
                model:
                  type: string
                  default: "embed-multilingual-v2.0"
      responses:
        '200':
          description: Embeddings generated successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  embeddings:
                    type: array
                    items:
                      type: array
                      items:
                        type: number
                        format: float
        '429':
          description: Rate limit exceeded
        '500':
          description: Server error
```

#### Qdrant Storage Service
```yaml
# OpenAPI 3.0 specification
openapi: 3.0.0
info:
  title: Qdrant Storage Service
  version: 1.0.0

paths:
  /store:
    post:
      summary: Store embeddings in Qdrant
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                vectors:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      vector:
                        type: array
                        items:
                          type: number
                          format: float
                      payload:
                        type: object
                        description: Metadata for the vector
      responses:
        '200':
          description: Vectors stored successfully
        '500':
          description: Storage error
```

### Quickstart Guide

#### Setup
1. Install dependencies: `pip install cohere qdrant-client playwright python-dotenv`
2. Configure environment variables in `.env`:
   ```
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   DOCUSAURUS_URL=https://your-docusaurus-site.com
   ```
3. Install Playwright browsers: `playwright install`

#### Usage
1. Run content extraction: `python -m rag_embeddings.scraper`
2. Process and chunk content: `python -m rag_embeddings.chunker`
3. Generate embeddings: `python -m rag_embeddings.embedder`
4. Store in Qdrant: `python -m rag_embeddings.storage`

### Agent Context Update

The following technologies have been added to the agent context:
- Cohere API for embedding generation
- Qdrant Cloud for vector storage
- Playwright for web scraping
- Environment configuration with python-dotenv

---

## Phase 2: Implementation Tasks

### Task 1: Setup & Dependencies
**Component**: Setup
**Description**: Install dependencies and configure environment
**Inputs**:
- List of required packages (cohere, qdrant-client, playwright, beautifulsoup4/python-dotenv)
- Environment configuration template
**Outputs**:
- requirements.txt with dependencies
- .env template file
- Configured project structure
**Key Functions**:
- setup_dependencies(): Install required packages
- create_env_template(): Generate .env file template
- verify_installation(): Check all dependencies are available
**Dependencies**: None
**Acceptance Criteria**:
- [ ] All required packages are listed in requirements.txt
- [ ] .env template includes all necessary environment variables
- [ ] Dependencies can be installed successfully
- [ ] Basic import tests pass for all libraries

### Task 2: Web Content Scraper
**Component**: Scraper
**Description**: Extract text from all book pages at GitHub Pages URL
**Inputs**:
- Docusaurus website URL
- Configuration for scraping (selectors, allowed paths)
**Outputs**:
- List of DocumentChunk objects with extracted content
- Source URLs and metadata
- Error logs for failed pages
**Key Functions**:
- scrape_docusaurus_site(): Main scraping function
- extract_page_content(): Extract content from individual page
- get_all_page_urls(): Discover all pages on the site
**Dependencies**: Playwright, requests
**Acceptance Criteria**:
- [ ] All public pages are discovered and scraped
- [ ] Content extraction preserves text, headings, and structure
- [ ] Error handling for network issues and timeouts
- [ ] Respects robots.txt and rate limits

### Task 3: Content Chunker
**Component**: Chunker
**Description**: Split text into 500-1000 token chunks with overlap
**Inputs**:
- List of DocumentChunk objects with full content
- Configuration (chunk size, overlap size)
**Outputs**:
- List of smaller DocumentChunk objects (500-1000 tokens each)
- Metadata preserved for each chunk
- Chunking statistics and logs
**Key Functions**:
- chunk_content(): Split content into appropriate chunks
- count_tokens(): Count tokens in text using tiktoken
- create_overlapping_chunks(): Handle overlap between chunks
**Dependencies**: tiktoken
**Acceptance Criteria**:
- [ ] Chunks are within 500-1000 token range
- [ ] Overlap is maintained between consecutive chunks
- [ ] Original metadata is preserved for each chunk
- [ ] Edge cases handled (very short/long documents)

### Task 4: Embedding Generator
**Component**: Embedder
**Description**: Batch generate embeddings via Cohere API (96 texts/call)
**Inputs**:
- List of DocumentChunk objects to embed
- Cohere API configuration
**Outputs**:
- DocumentChunk objects with embedding vectors added
- API usage statistics
- Error logs for failed embeddings
**Key Functions**:
- generate_embeddings_batch(): Process chunks in batches of 96
- handle_rate_limiting(): Implement backoff for API limits
- validate_embeddings(): Verify embedding quality
**Dependencies**: Cohere API client
**Acceptance Criteria**:
- [ ] Embeddings generated for all content chunks
- [ ] API rate limits handled with proper backoff
- [ ] Batch processing uses maximum allowed batch size (96)
- [ ] Failed requests are retried appropriately

### Task 5: Vector Storage
**Component**: Storage
**Description**: Create Qdrant collection, upload vectors with metadata
**Inputs**:
- DocumentChunk objects with embeddings
- Qdrant configuration
**Outputs**:
- Embeddings stored in Qdrant Cloud collection
- Verification of successful storage
- Storage statistics and logs
**Key Functions**:
- create_qdrant_collection(): Initialize collection with proper settings
- upload_vectors_batch(): Upload embeddings in batches
- verify_storage(): Confirm vectors are searchable
**Dependencies**: Qdrant client
**Acceptance Criteria**:
- [ ] Qdrant collection created with appropriate settings
- [ ] All embeddings uploaded successfully
- [ ] Metadata properly associated with vectors
- [ ] Vectors are searchable in the collection

### Task 6: Verification System
**Component**: Verify
**Description**: Test retrieval of sample embeddings
**Inputs**:
- Stored embeddings in Qdrant
- Test queries for retrieval
**Outputs**:
- Retrieval results for test queries
- Performance metrics (latency, accuracy)
- Verification report
**Key Functions**:
- test_similarity_search(): Perform vector similarity searches
- measure_performance(): Track retrieval performance
- validate_retrieval_accuracy(): Check result relevance
**Dependencies**: Qdrant client
**Acceptance Criteria**:
- [ ] Similarity search returns relevant results
- [ ] Retrieval performance meets requirements
- [ ] Test queries return expected content
- [ ] Verification report confirms system functionality

## Phase 3: Integration & Testing

### Integration Tasks
- Integrate all components into a cohesive pipeline
- Implement end-to-end error handling
- Add comprehensive logging and monitoring
- Create command-line interface for easy execution

### Testing Strategy
- Unit tests for each component
- Integration tests for pipeline flow
- Performance tests for large datasets
- Error scenario testing

## Success Criteria Verification

All success criteria from the feature specification will be verified:
- SC-001: 95% of content extracted within 30 minutes
- SC-002: 1000+ chunks processed with 99% success rate
- SC-003: API rate limits handled with <5% failure rate
- SC-004: Developer implementation success rate of 90%
- SC-005: Comprehensive logging and error reporting