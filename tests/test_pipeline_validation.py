import pytest
from unittest.mock import Mock, patch, MagicMock
from retrieval_validation.models.data_models import QueryRequest, RetrievedChunk, ValidationResult
from retrieval_validation.services.pipeline_validator import PipelineValidator
from retrieval_validation.services.validation_storage import ValidationStorage


class TestPipelineValidation:
    """
    Tests for pipeline validation functionality.
    """

    def test_pipeline_validator_creation(self):
        """Test that PipelineValidator service can be created with proper dependencies."""
        with patch('cohere.Client'), \
             patch('qdrant_client.QdrantClient'):

            validator = PipelineValidator()
            assert validator.service_name == "PipelineValidator"
            assert validator.qdrant_retriever is not None
            assert validator.query_embedder is not None

    def test_validate_stored_content_empty_collection(self):
        """Test validation when collection is empty."""
        with patch('cohere.Client'), \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock count to return 0 (empty collection)
            mock_count_result = MagicMock()
            mock_count_result.count = 0
            mock_qdrant.return_value.count.return_value = mock_count_result

            validator = PipelineValidator()
            result = validator.validate_stored_content(collection_name="test_collection", sample_size=5)

            assert result.is_valid is False
            assert "No content stored in the collection" in result.validation_message
            assert result.validation_metrics["total_points"] == 0

    def test_run_end_to_end_tests(self):
        """Test running end-to-end tests with sample queries."""
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_search_result = [
                Mock(id="chunk1", score=0.85, payload={"text": "Test content", "source": "doc1"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            validator = PipelineValidator()

            test_queries = ["What is AI?", "Explain ML"]
            result = validator.run_end_to_end_tests(test_queries=test_queries)

            assert isinstance(result, ValidationResult)
            assert result.is_valid is True  # Should be valid if tests run successfully
            assert "tests successful" in result.validation_message
            assert "test_results" in result.validation_metrics

    def test_detect_issues_validation_failure(self):
        """Test issue detection when validation fails."""
        validator = PipelineValidator()

        # Create a validation result that failed
        query_request = QueryRequest(query_text="test", collection_name="test")
        result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=[],
            is_valid=False,
            validation_message="Test validation failed",
            validation_metrics={
                "success_rate": 0.5,  # Below threshold
                "validation_details": [
                    {"query": "test1", "status": "failed", "reason": "test error"}
                ]
            }
        )

        issues = validator.detect_issues(result)

        # Should detect the validation failure and low success rate
        assert len(issues) >= 2
        issue_types = [issue["type"] for issue in issues]
        assert "validation_failure" in issue_types
        assert "low_success_rate" in issue_types

    def test_generate_diagnostics(self):
        """Test generation of diagnostic information."""
        validator = PipelineValidator()

        # Create a validation result
        query_request = QueryRequest(query_text="test", collection_name="test")
        result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=[],
            is_valid=False,
            validation_message="Test validation failed",
            validation_metrics={
                "success_rate": 0.5,
                "total_tests": 10,
                "successful_tests": 5
            }
        )

        diagnostics = validator.generate_diagnostics(result)

        assert "validation_id" in diagnostics
        assert "validation_timestamp" in diagnostics
        assert "metrics" in diagnostics
        assert "detected_issues" in diagnostics
        assert "summary" in diagnostics
        assert diagnostics["is_valid"] is False

    def test_validation_storage_creation(self):
        """Test that ValidationStorage can be created and configured properly."""
        storage = ValidationStorage()
        assert storage.service_name == "ValidationStorage"
        assert storage.storage_path.exists()  # Should be created during initialization

    def test_store_and_retrieve_validation_result(self):
        """Test storing and retrieving a validation result."""
        storage = ValidationStorage()

        # Create a test validation result
        query_request = QueryRequest(query_text="test query", collection_name="test_collection")
        retrieved_chunks = [
            RetrievedChunk(
                chunk_id="chunk1",
                text="Test content",
                score=0.85,
                source="test_source",
                metadata={"category": "test"}
            )
        ]
        validation_result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=retrieved_chunks,
            is_valid=True,
            validation_message="Test validation passed",
            validation_metrics={"test_metric": 1.0}
        )

        # Store the result
        store_success = storage.store_validation_result(validation_result)
        assert store_success is True

        # Retrieve the result
        retrieved_result = storage.retrieve_validation_result(validation_result.validation_id)
        assert retrieved_result is not None
        assert retrieved_result.validation_id == validation_result.validation_id
        assert retrieved_result.is_valid == validation_result.is_valid
        assert retrieved_result.validation_message == validation_result.validation_message
        assert len(retrieved_result.retrieved_chunks) == len(validation_result.retrieved_chunks)

    def test_list_validation_results(self):
        """Test listing validation results."""
        storage = ValidationStorage()

        # Create and store a test validation result
        query_request = QueryRequest(query_text="test query", collection_name="test_collection")
        retrieved_chunks = []
        validation_result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=retrieved_chunks,
            is_valid=True,
            validation_message="Test validation for listing",
            validation_metrics={"test_metric": 1.0}
        )

        storage.store_validation_result(validation_result)

        # List validation results
        results = storage.list_validation_results(limit=10)
        assert len(results) >= 1

        # Check that the result we stored is in the list
        found_result = next((r for r in results if r["validation_id"] == validation_result.validation_id), None)
        assert found_result is not None
        assert found_result["is_valid"] is True
        assert "Test validation for listing" in found_result["validation_message"]

    def test_validation_summary(self):
        """Test getting validation summary."""
        storage = ValidationStorage()

        # Get initial summary
        summary = storage.get_validation_summary()
        assert "total_validations" in summary
        assert "successful_validations" in summary
        assert "failed_validations" in summary
        assert "success_rate" in summary
        assert summary["total_validations"] >= 0  # Could be 0 if no validations stored yet

    def test_delete_validation_result(self):
        """Test deleting a validation result."""
        storage = ValidationStorage()

        # Create and store a test validation result
        query_request = QueryRequest(query_text="test query", collection_name="test_collection")
        retrieved_chunks = []
        validation_result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=retrieved_chunks,
            is_valid=True,
            validation_message="Test validation for deletion",
            validation_metrics={"test_metric": 1.0}
        )

        storage.store_validation_result(validation_result)

        # Verify it's stored
        retrieved_result = storage.retrieve_validation_result(validation_result.validation_id)
        assert retrieved_result is not None

        # Delete the result
        delete_success = storage.delete_validation_result(validation_result.validation_id)
        assert delete_success is True

        # Verify it's deleted
        retrieved_result = storage.retrieve_validation_result(validation_result.validation_id)
        assert retrieved_result is None


class TestAcceptanceScenariosPipeline:
    """
    Acceptance tests for pipeline validation scenarios.
    """

    def test_validate_acceptance_scenario_pipeline_validation(self):
        """
        Validate acceptance scenario: Execute validation tests and verify all stored content can be retrieved
        """
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant count and search
            mock_count_result = MagicMock()
            mock_count_result.count = 5  # Simulate 5 stored items
            mock_qdrant.return_value.count.return_value = mock_count_result

            # Mock scroll for content sampling
            mock_point1 = MagicMock()
            mock_point1.payload = {"text": "Artificial intelligence is a very interesting topic"}
            mock_point2 = MagicMock()
            mock_point2.payload = {"text": "Machine learning involves training models"}

            mock_qdrant.return_value.scroll.return_value = ([mock_point1, mock_point2], None)

            # Mock search results
            mock_search_result = [
                Mock(id="chunk1", score=0.85, payload={"text": "AI content", "source": "doc1"}),
                Mock(id="chunk2", score=0.75, payload={"text": "ML content", "source": "doc2"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            # Create validator and run stored content validation
            validator = PipelineValidator()
            result = validator.validate_stored_content(collection_name="test_collection", sample_size=2)

            # Verify the validation was successful
            assert result.is_valid is True
            assert "validation" in result.validation_message.lower()
            assert "success rate" in result.validation_message.lower()

    def test_validate_acceptance_scenario_end_to_end_tests(self):
        """
        Validate acceptance scenario: Run end-to-end tests and verify content flows correctly
        """
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_search_result = [
                Mock(id="chunk1", score=0.85, payload={"text": "Test content", "source": "doc1"})
            ]
            mock_qdrant.return_value.search.return_value = mock_search_result

            # Create validator and run end-to-end tests
            validator = PipelineValidator()
            test_queries = ["What is AI?", "Explain machine learning"]
            result = validator.run_end_to_end_tests(test_queries=test_queries)

            # Verify the tests were successful
            assert result.is_valid is True
            assert "tests successful" in result.validation_message
            assert result.validation_metrics["total_tests"] == 2
            assert result.validation_metrics["successful_tests"] == 2

    def test_validate_acceptance_scenario_error_reporting(self):
        """
        Validate acceptance scenario: Generate appropriate error reporting and diagnostics when issues occur
        """
        validator = PipelineValidator()

        # Create a validation result with failures
        query_request = QueryRequest(query_text="test", collection_name="test")
        failed_result = ValidationResult(
            query_request=query_request,
            retrieved_chunks=[],
            is_valid=False,
            validation_message="Test validation failed",
            validation_metrics={
                "success_rate": 0.3,  # Low success rate
                "total_tests": 10,
                "successful_tests": 3,
                "validation_details": [
                    {"query": "test1", "status": "failed", "reason": "embedding error"},
                    {"query": "test2", "status": "failed", "reason": "retrieval timeout"}
                ]
            }
        )

        # Generate diagnostics
        diagnostics = validator.generate_diagnostics(failed_result)

        # Verify diagnostics contain appropriate error reporting
        assert "detected_issues" in diagnostics
        assert len(diagnostics["detected_issues"]) > 0

        # Check that issues were properly detected
        issue_types = [issue["type"] for issue in diagnostics["detected_issues"]]
        assert "low_success_rate" in issue_types

        # Verify summary information
        assert "summary" in diagnostics
        assert diagnostics["summary"]["issue_count"] > 0
        assert diagnostics["summary"]["high_severity_issues"] >= 0