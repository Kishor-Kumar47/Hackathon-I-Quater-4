import pytest
import os
from unittest.mock import Mock, patch
from retrieval_validation.models.data_models import QueryRequest, RetrievedChunk
from retrieval_validation.services.query_embedder import QueryEmbedder
from retrieval_validation.services.qdrant_retriever import QdrantRetriever
from retrieval_validation.services.json_formatter import JSONFormatter
from retrieval_validation.api.query_endpoint import QueryEndpoint, QueryRequestModel


class TestQueryFunctionality:
    """
    Tests for query functionality to verify the complete pipeline works correctly.
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Mock environment variables for testing
        os.environ['COHERE_API_KEY'] = 'test-cohere-key'
        os.environ['QDRANT_HOST'] = 'localhost'
        os.environ['QDRANT_PORT'] = '6333'

    def test_query_embedder_creation(self):
        """Test that QueryEmbedder service can be created with proper configuration."""
        # This would normally fail due to missing real API key, but we're testing structure
        with patch('cohere.Client') as mock_client:
            mock_client.return_value = Mock()
            embedder = QueryEmbedder()
            assert embedder.service_name == "QueryEmbedder"
            assert embedder.config is not None

    def test_qdrant_retriever_creation(self):
        """Test that QdrantRetriever service can be created with proper configuration."""
        with patch('qdrant_client.QdrantClient') as mock_client:
            mock_client.return_value = Mock()
            retriever = QdrantRetriever()
            assert retriever.service_name == "QdrantRetriever"
            assert retriever.config is not None

    def test_json_formatter_creation(self):
        """Test that JSONFormatter service can be created."""
        formatter = JSONFormatter()
        assert formatter.service_name == "JSONFormatter"

    def test_format_retrieved_chunks(self):
        """Test formatting of retrieved chunks."""
        formatter = JSONFormatter()

        # Create sample retrieved chunks
        chunks = [
            RetrievedChunk(
                chunk_id="chunk1",
                text="Sample content text",
                score=0.85,
                source="test_source",
                metadata={"category": "test", "page": 1}
            ),
            RetrievedChunk(
                chunk_id="chunk2",
                text="Another sample text",
                score=0.72,
                source="test_source2",
                metadata={"category": "example", "page": 2}
            )
        ]

        query_request = QueryRequest(
            query_text="test query",
            collection_name="test_collection"
        )

        formatted_result = formatter.format_retrieved_chunks(chunks, query_request)

        # Verify the structure of the formatted result
        assert "query_id" in formatted_result
        assert "query_text" in formatted_result
        assert "retrieved_chunks" in formatted_result
        assert "total_results" in formatted_result
        assert len(formatted_result["retrieved_chunks"]) == 2
        assert formatted_result["total_results"] == 2

        # Verify individual chunk structure
        first_chunk = formatted_result["retrieved_chunks"][0]
        assert "chunk_id" in first_chunk
        assert "text" in first_chunk
        assert "score" in first_chunk
        assert "source" in first_chunk
        assert "metadata" in first_chunk

    def test_extract_metadata(self):
        """Test extraction of metadata from retrieved chunks."""
        formatter = JSONFormatter()

        chunks = [
            RetrievedChunk(
                chunk_id="chunk1",
                text="Sample content text",
                score=0.85,
                source="test_source",
                metadata={"category": "test", "page": 1, "author": "test_author"}
            )
        ]

        metadata_list = formatter.extract_metadata(chunks)

        assert len(metadata_list) == 1
        metadata = metadata_list[0]
        assert metadata["chunk_id"] == "chunk1"
        assert metadata["source"] == "test_source"
        assert metadata["score"] == 0.85
        assert metadata["category"] == "test"
        assert metadata["page"] == 1
        assert metadata["author"] == "test_author"

    def test_validate_output_compliance(self):
        """Test validation of output format compliance."""
        formatter = JSONFormatter()

        # Valid output structure
        valid_output = {
            "query_id": "test-query-id",
            "query_text": "test query",
            "retrieved_chunks": [
                {
                    "chunk_id": "chunk1",
                    "text": "Sample content",
                    "score": 0.85,
                    "source": "test_source"
                }
            ],
            "total_results": 1,
            "collection_name": "test_collection",
            "request_timestamp": "2023-01-01T00:00:00"
        }

        assert formatter.validate_output(valid_output) is True

        # Invalid output - missing required key
        invalid_output = {
            "query_id": "test-query-id",
            # Missing query_text
            "retrieved_chunks": [
                {
                    "chunk_id": "chunk1",
                    "text": "Sample content",
                    "score": 0.85,
                    "source": "test_source"
                }
            ],
            "total_results": 1
        }

        assert formatter.validate_output(invalid_output) is False

    def test_query_endpoint_creation(self):
        """Test that QueryEndpoint can be created and integrates all components."""
        with patch('cohere.Client'), \
             patch('qdrant_client.QdrantClient'), \
             patch('retrieval_validation.services.query_embedder.get_config') as mock_config, \
             patch('retrieval_validation.services.qdrant_retriever.get_config') as mock_qdrant_config:

            # Mock config objects
            mock_config.return_value.cohere_api_key = "test-key"
            mock_qdrant_config.return_value.qdrant_host = "localhost"
            mock_qdrant_config.return_value.qdrant_port = 6333

            endpoint = QueryEndpoint()
            assert endpoint.query_embedder is not None
            assert endpoint.qdrant_retriever is not None
            assert endpoint.json_formatter is not None

    def test_query_request_model(self):
        """Test the QueryRequestModel Pydantic model."""
        request_model = QueryRequestModel(
            query_text="test query",
            collection_name="test_collection",
            top_k=5,
            threshold=0.5
        )

        assert request_model.query_text == "test query"
        assert request_model.collection_name == "test_collection"
        assert request_model.top_k == 5
        assert request_model.threshold == 0.5

    def test_query_request_model_defaults(self):
        """Test the QueryRequestModel with default values."""
        request_model = QueryRequestModel(
            query_text="test query"
        )

        assert request_model.query_text == "test query"
        assert request_model.collection_name == "content_chunks"  # default
        assert request_model.top_k == 5  # default
        assert request_model.threshold is None  # default