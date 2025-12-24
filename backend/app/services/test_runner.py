from typing import List, Dict, Any
from datetime import datetime
import time
from .test_query_repository import TestQuery, test_query_repository
from .qdrant_retriever import QdrantRetrievalService
from .metrics_service import metrics_service


class TestRunner:
    """
    TestRunner for executing validation tests.
    """

    def __init__(self):
        self.retrieval_service = QdrantRetrievalService()
        self.metrics_service = metrics_service

    def run_validation_tests(self, test_queries: List[TestQuery] = None) -> List[Dict[str, Any]]:
        """
        Execute all validation tests.

        Args:
            test_queries: Optional list of TestQuery objects to run. If None, uses default test queries.

        Returns:
            List of test results
        """
        if test_queries is None:
            # Generate default test queries if none provided
            test_queries = test_query_repository.create_test_queries(num_queries=5)

        print(f"Running validation tests on {len(test_queries)} queries...")

        test_results = []

        for i, test_query in enumerate(test_queries):
            print(f"Running test {i+1}/{len(test_queries)}: {test_query.query_text[:50]}...")

            try:
                # Run the test using the retrieval service
                result = self._run_single_test(test_query)
                test_results.append(result)
            except Exception as e:
                print(f"Error running test {i+1}: {str(e)}")
                test_results.append({
                    "test_id": test_query.id,
                    "query_text": test_query.query_text,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })

        print(f"Completed {len(test_results)} validation tests")
        return test_results

    def _run_single_test(self, test_query: TestQuery) -> Dict[str, Any]:
        """
        Run a single test query against the retrieval system.

        Args:
            test_query: TestQuery object to run

        Returns:
            Test result dictionary
        """
        # Update the last run timestamp
        test_query.last_run = datetime.utcnow()

        # Use the metrics service to measure latency
        result_with_latency = self.metrics_service.measure_latency(
            self.retrieval_service.retrieve,
            test_query.query_text,
            k=min(5, len(test_query.expected_chunks) + 2)  # Get slightly more than expected
        )

        retrieved_chunks = result_with_latency["result"]
        latency_data = result_with_latency["latency_data"]

        # Calculate accuracy metrics
        accuracy_metrics = self.metrics_service.calculate_accuracy_metrics(
            retrieved_chunks,
            test_query.expected_chunks
        )

        # Determine if test passed based on accuracy
        # For now, consider it passed if we have reasonable precision/recall
        passed = accuracy_metrics.get("f1_score", 0) >= 0.5  # 50% F1 score threshold

        result = {
            "test_id": test_query.id,
            "query_text": test_query.query_text,
            "category": test_query.category,
            "status": "passed" if passed else "failed",
            "retrieved_chunks": retrieved_chunks,
            "expected_chunks": test_query.expected_chunks,
            "accuracy_metrics": accuracy_metrics,
            "latency_data": latency_data,
            "timestamp": datetime.utcnow().isoformat()
        }

        return result

    def validate_relevance(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare expected vs actual results to validate relevance.

        Args:
            test_results: List of test results from run_validation_tests

        Returns:
            Dictionary with validation summary
        """
        if not test_results:
            return {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "pass_rate": 0,
                "average_precision": 0,
                "average_recall": 0,
                "average_f1_score": 0,
                "timestamp": datetime.utcnow().isoformat()
            }

        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result["status"] == "passed")

        # Calculate average metrics
        precisions = [result["accuracy_metrics"].get("precision", 0) for result in test_results]
        recalls = [result["accuracy_metrics"].get("recall", 0) for result in test_results]
        f1_scores = [result["accuracy_metrics"].get("f1_score", 0) for result in test_results]

        avg_precision = sum(precisions) / len(precisions) if precisions else 0
        avg_recall = sum(recalls) / len(recalls) if recalls else 0
        avg_f1_score = sum(f1_scores) / len(f1_scores) if f1_scores else 0

        validation_summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "average_precision": avg_precision,
            "average_recall": avg_recall,
            "average_f1_score": avg_f1_score,
            "timestamp": datetime.utcnow().isoformat()
        }

        print(f"Validation summary: {validation_summary['pass_rate']:.2%} pass rate, "
              f"F1: {validation_summary['average_f1_score']:.3f}")

        return validation_summary

    def generate_test_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create validation summary report.

        Args:
            test_results: List of test results from run_validation_tests

        Returns:
            Dictionary with comprehensive test report
        """
        validation_summary = self.validate_relevance(test_results)

        # Get detailed metrics
        detailed_metrics = self.metrics_service.aggregate_performance_data()

        report = {
            "report_id": f"test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "summary": validation_summary,
            "detailed_metrics": detailed_metrics,
            "test_results": test_results,
            "generated_at": datetime.utcnow().isoformat(),
            "total_tests_run": len(test_results)
        }

        print(f"Generated test report with {len(test_results)} test results")

        return report


# Global test runner instance
test_runner = TestRunner()