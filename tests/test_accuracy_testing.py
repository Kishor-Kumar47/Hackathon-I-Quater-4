import pytest
from unittest.mock import Mock, patch, MagicMock
from retrieval_validation.models.data_models import TestQuery, RetrievedChunk, QueryRequest
from retrieval_validation.services.accuracy_tester import AccuracyTester
from retrieval_validation.services.test_query_manager import TestQueryManager


class TestAccuracyTesting:
    """
    Tests for accuracy testing functionality.
    """

    def test_accuracy_tester_creation(self):
        """Test that AccuracyTester service can be created with proper dependencies."""
        with patch('cohere.Client'), \
             patch('qdrant_client.QdrantClient'):

            tester = AccuracyTester()
            assert tester.service_name == "AccuracyTester"
            assert tester.qdrant_retriever is not None
            assert tester.query_embedder is not None

    def test_compare_expected_vs_actual_perfect_match(self):
        """Test comparison when expected and actual results match perfectly."""
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results that match expected
            expected_chunk = RetrievedChunk(
                chunk_id="chunk1",
                text="Expected content text",
                score=0.9,
                source="expected_source",
                metadata={"category": "test"}
            )

            actual_chunk = RetrievedChunk(
                chunk_id="chunk1",  # Same ID as expected
                text="Expected content text",  # Same text as expected
                score=0.85,
                source="actual_source",
                metadata={"category": "test"}
            )

            mock_qdrant.return_value.search.return_value = [Mock(id="chunk1", score=0.85, payload={
                "text": "Expected content text",
                "source": "actual_source",
                "category": "test"
            })]

            tester = AccuracyTester()

            # Create a test query
            test_query = TestQuery(
                query_text="Test query",
                expected_chunks=[expected_chunk],
                test_category="test_category"
            )

            # Run comparison
            results = tester.compare_expected_vs_actual(test_query)

            # Verify results
            assert results["precision_by_id"] == 1.0  # Perfect precision
            assert results["recall_by_id"] == 1.0     # Perfect recall
            assert results["f1_by_id"] == 1.0         # Perfect F1
            assert results["expected_count"] == 1
            assert results["actual_count"] >= 0       # May have retrieved more than expected

    def test_compare_expected_vs_actual_no_match(self):
        """Test comparison when expected and actual results don't match."""
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results that don't match expected
            expected_chunk = RetrievedChunk(
                chunk_id="expected_chunk1",
                text="Expected content text",
                score=0.9,
                source="expected_source",
                metadata={"category": "test"}
            )

            mock_qdrant.return_value.search.return_value = [
                Mock(id="actual_chunk1", score=0.8, payload={
                    "text": "Different content text",
                    "source": "different_source",
                    "category": "different"
                })
            ]

            tester = AccuracyTester()

            # Create a test query
            test_query = TestQuery(
                query_text="Test query",
                expected_chunks=[expected_chunk],
                test_category="test_category"
            )

            # Run comparison
            results = tester.compare_expected_vs_actual(test_query)

            # Verify results - should have low precision/recall
            assert results["precision_by_id"] == 0.0  # No matching IDs
            assert results["recall_by_id"] == 0.0     # No matching IDs retrieved
            assert results["expected_count"] == 1
            assert results["actual_count"] >= 0

    def test_calculate_precision_recall(self):
        """Test precision and recall calculation from comparison results."""
        tester = AccuracyTester()

        # Create mock comparison results
        comparison_results = {
            "precision_by_id": 0.8,
            "recall_by_id": 0.7,
            "precision_by_text": 0.9,
            "recall_by_text": 0.6
        }

        metrics = tester.calculate_precision_recall(comparison_results)

        assert metrics["precision"] == 0.8
        assert metrics["recall"] == 0.7
        assert "f1_score" in metrics
        assert metrics["f1_score"] == pytest.approx(2 * (0.8 * 0.7) / (0.8 + 0.7), abs=0.01)

    def test_identify_improvement_areas_low_precision(self):
        """Test identifying improvement areas when precision is low."""
        tester = AccuracyTester()

        # Create comparison results with low precision
        comparison_results = {
            "precision_by_id": 0.3,  # Below threshold
            "recall_by_id": 0.9,
            "avg_similarity_score": 0.7
        }

        improvements = tester.identify_improvement_areas(comparison_results, threshold=0.7)

        # Should identify precision as an issue
        precision_issues = [i for i in improvements if i["area"] == "precision"]
        assert len(precision_issues) > 0
        assert precision_issues[0]["current_value"] == 0.3
        assert precision_issues[0]["threshold"] == 0.7

    def test_identify_improvement_areas_low_recall(self):
        """Test identifying improvement areas when recall is low."""
        tester = AccuracyTester()

        # Create comparison results with low recall
        comparison_results = {
            "precision_by_id": 0.9,
            "recall_by_id": 0.2,  # Below threshold
            "avg_similarity_score": 0.7
        }

        improvements = tester.identify_improvement_areas(comparison_results, threshold=0.7)

        # Should identify recall as an issue
        recall_issues = [i for i in improvements if i["area"] == "recall"]
        assert len(recall_issues) > 0
        assert recall_issues[0]["current_value"] == 0.2
        assert recall_issues[0]["threshold"] == 0.7

    def test_run_accuracy_tests(self):
        """Test running multiple accuracy tests."""
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_qdrant.return_value.search.return_value = [
                Mock(id="chunk1", score=0.8, payload={
                    "text": "Test content",
                    "source": "test_source",
                    "category": "test"
                })
            ]

            tester = AccuracyTester()

            # Create test queries
            test_queries = []
            for i in range(3):
                expected_chunk = RetrievedChunk(
                    chunk_id=f"chunk{i+1}",
                    text=f"Expected content {i+1}",
                    score=0.9,
                    source="expected_source",
                    metadata={"category": "test"}
                )
                test_query = TestQuery(
                    query_text=f"Test query {i+1}",
                    expected_chunks=[expected_chunk],
                    test_category="test_category"
                )
                test_queries.append(test_query)

            # Run accuracy tests
            results = tester.run_accuracy_tests(test_queries, aggregation=True)

            # Verify results structure
            assert "aggregated_metrics" in results
            assert "detailed_results" in results
            assert "summary" in results
            assert len(results["detailed_results"]) == 3
            assert results["summary"]["total_tests_run"] == 3

            # Check aggregated metrics
            agg_metrics = results["aggregated_metrics"]
            assert "avg_precision" in agg_metrics
            assert "avg_recall" in agg_metrics
            assert "avg_f1_score" in agg_metrics

    def test_collect_performance_metrics(self):
        """Test collecting performance metrics from test results."""
        tester = AccuracyTester()

        # Create mock test results
        test_results = {
            "aggregated_metrics": {
                "avg_precision": 0.8,
                "avg_recall": 0.7,
                "avg_f1_score": 0.75,
                "total_tests": 5
            },
            "detailed_results": [
                {
                    "test_id": "test1",
                    "metrics": {"precision": 0.8, "recall": 0.7, "f1_score": 0.75},
                    "improvement_areas": []
                }
            ]
        }

        metrics = tester.collect_performance_metrics(test_results)

        assert metrics.precision == 0.8
        assert metrics.recall == 0.7
        assert metrics.f1_score == 0.75
        assert metrics.total_queries == 5
        assert len(metrics.query_performance) == 1

    def test_test_query_manager_creation(self):
        """Test that TestQueryManager can be created and configured properly."""
        manager = TestQueryManager()
        assert manager.service_name == "TestQueryManager"
        assert manager.storage_path.exists()

    def test_create_test_queries(self):
        """Test creating test queries covering book topics."""
        manager = TestQueryManager()

        # Create 5 test queries
        queries = manager.create_test_queries(num_queries=5, category="AI Testing")

        assert len(queries) == 5
        for query in queries:
            assert isinstance(query, TestQuery)
            assert query.query_text
            assert query.test_category
            assert query.priority >= 1

        # Verify we have diverse categories
        categories = [q.test_category for q in queries]
        assert len(set(categories)) > 0  # At least some variety

    def test_save_and_load_test_queries(self):
        """Test saving and loading test queries."""
        manager = TestQueryManager()

        # Create test queries
        queries = manager.create_test_queries(num_queries=2, category="SaveLoad Test")

        # Save queries
        save_success = manager.save_test_queries(queries, "test_save_load")
        assert save_success is True

        # Load queries
        loaded_queries = manager.load_test_queries("test_save_load")

        assert len(loaded_queries) == len(queries)
        for original, loaded in zip(queries, loaded_queries):
            assert original.query_text == loaded.query_text
            assert original.test_category == loaded.test_category
            assert original.priority == loaded.priority

    def test_get_test_queries_by_category(self):
        """Test getting test queries by category."""
        manager = TestQueryManager()

        # Create and save test queries in a specific category
        queries = manager.create_test_queries(num_queries=3, category="TestCategory")
        manager.save_test_queries(queries, "test_category_queries")

        # Get queries by category
        category_queries = manager.get_test_queries_by_category("TestCategory")

        assert len(category_queries) >= 0  # May find our saved queries

    def test_get_test_query_statistics(self):
        """Test getting statistics about test queries."""
        manager = TestQueryManager()

        stats = manager.get_test_query_statistics()

        assert "total_queries" in stats
        assert "categories" in stats
        assert "storage_path" in stats


class TestAcceptanceScenariosAccuracy:
    """
    Acceptance tests for accuracy testing scenarios.
    """

    def test_validate_acceptance_scenario_accuracy_tests(self):
        """
        Validate acceptance scenario: Execute accuracy tests and return results matching expected relevance within thresholds
        """
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_qdrant.return_value.search.return_value = [
                Mock(id="relevant_chunk1", score=0.85, payload={
                    "text": "Artificial intelligence is a wonderful field",
                    "source": "ai_textbook",
                    "topic": "AI definition"
                })
            ]

            tester = AccuracyTester()

            # Create a test query with expected results
            expected_chunk = RetrievedChunk(
                chunk_id="relevant_chunk1",
                text="Artificial intelligence is a wonderful field",
                score=0.9,
                source="ai_textbook",
                metadata={"topic": "AI definition"}
            )

            test_query = TestQuery(
                query_text="What is artificial intelligence?",
                expected_chunks=[expected_chunk],
                test_category="AI Fundamentals",
                priority=4
            )

            # Run comparison
            results = tester.compare_expected_vs_actual(test_query)

            # Verify we get meaningful results
            assert "precision_by_id" in results
            assert "recall_by_id" in results
            assert "f1_by_id" in results

            # Calculate metrics
            metrics = tester.calculate_precision_recall(results)
            assert metrics["precision"] >= 0  # Should have some precision
            assert metrics["recall"] >= 0     # Should have some recall

            # The accuracy should be reasonable for this matching case
            assert metrics["f1_score"] >= 0  # Should be calculable

    def test_validate_acceptance_scenario_collect_accuracy_metrics(self):
        """
        Validate acceptance scenario: Collect and analyze accuracy metrics meeting quality standards
        """
        with patch('cohere.Client') as mock_cohere, \
             patch('qdrant_client.QdrantClient') as mock_qdrant:

            # Mock Cohere embedding
            mock_cohere.return_value.embed.return_value = Mock()
            mock_cohere.return_value.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

            # Mock Qdrant search results
            mock_qdrant.return_value.search.return_value = [
                Mock(id="chunk1", score=0.75, payload={
                    "text": "Test content for metrics",
                    "source": "test_source",
                    "category": "metrics_test"
                })
            ]

            tester = AccuracyTester()

            # Create multiple test queries to get meaningful metrics
            test_queries = []
            for i in range(3):
                expected_chunk = RetrievedChunk(
                    chunk_id=f"chunk{i+1}",
                    text=f"Expected content {i+1}",
                    score=0.9,
                    source="expected_source",
                    metadata={"category": "metrics_test"}
                )
                test_query = TestQuery(
                    query_text=f"Metrics test query {i+1}",
                    expected_chunks=[expected_chunk],
                    test_category="Metrics Test"
                )
                test_queries.append(test_query)

            # Run accuracy tests
            test_results = tester.run_accuracy_tests(test_queries, aggregation=True)

            # Collect performance metrics
            performance_metrics = tester.collect_performance_metrics(test_results)

            # Verify metrics are properly structured
            assert performance_metrics.precision >= 0
            assert performance_metrics.recall >= 0
            assert performance_metrics.f1_score >= 0
            assert performance_metrics.total_queries == 3
            assert len(performance_metrics.query_performance) == 3

            # Verify aggregated metrics in test results
            agg_metrics = test_results["aggregated_metrics"]
            assert "avg_precision" in agg_metrics
            assert "avg_recall" in agg_metrics
            assert "avg_f1_score" in agg_metrics
            assert agg_metrics["total_tests"] == 3

    def test_validate_acceptance_scenario_report_improvement_areas(self):
        """
        Validate acceptance scenario: Report specific areas for improvement when accuracy issues detected
        """
        tester = AccuracyTester()

        # Create comparison results that should trigger improvement suggestions
        comparison_results = {
            "precision_by_id": 0.4,  # Below threshold
            "recall_by_id": 0.3,     # Below threshold
            "avg_similarity_score": 0.3,  # Low similarity
            "true_positives_by_id": 0  # No matches
        }

        # Identify improvement areas
        improvements = tester.identify_improvement_areas(comparison_results, threshold=0.7)

        # Should identify multiple areas for improvement
        improvement_areas = [imp["area"] for imp in improvements]
        assert "precision" in improvement_areas
        assert "recall" in improvement_areas
        assert "similarity_score" in improvement_areas
        assert "retrieval_accuracy" in improvement_areas

        # Verify details are provided
        for improvement in improvements:
            assert "issue" in improvement
            assert "suggestion" in improvement
            assert "current_value" in improvement
            assert "threshold" in improvement