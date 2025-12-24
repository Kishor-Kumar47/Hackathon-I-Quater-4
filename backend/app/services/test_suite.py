from typing import List, Dict, Any
from datetime import datetime
import time
import json
from pathlib import Path
from .test_runner import test_runner
from .test_query_repository import test_query_repository
from .metrics_service import metrics_service


class ComprehensiveTestSuite:
    """
    Comprehensive test suite that validates all functionality.
    """

    def __init__(self, report_path: str = None):
        self.test_runner = test_runner
        self.test_query_repository = test_query_repository
        self.metrics_service = metrics_service

        # Set up report storage path
        if report_path is None:
            project_root = Path(__file__).parent.parent.parent
            self.report_path = project_root / "test_reports"
        else:
            self.report_path = Path(report_path)

        # Create report directory if it doesn't exist
        self.report_path.mkdir(parents=True, exist_ok=True)

        print(f"ComprehensiveTestSuite initialized with reports at: {self.report_path}")

    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """
        Run the comprehensive test suite covering all functionality.

        Returns:
            Dictionary with comprehensive test results and report
        """
        print("Starting comprehensive test suite...")

        start_time = time.time()

        # Step 1: Create test queries
        print("Creating test queries...")
        test_queries = self.test_query_repository.create_test_queries(num_queries=7)
        print(f"Created {len(test_queries)} test queries")

        # Step 2: Run validation tests
        print("Running validation tests...")
        test_results = self.test_runner.run_validation_tests(test_queries)
        print(f"Completed {len(test_results)} validation tests")

        # Step 3: Validate relevance
        print("Validating relevance...")
        validation_summary = self.test_runner.validate_relevance(test_results)
        print(f"Validation completed with {validation_summary['pass_rate']:.2%} pass rate")

        # Step 4: Generate comprehensive report
        print("Generating comprehensive report...")
        report = self.test_runner.generate_test_report(test_results)

        # Step 5: Add additional metrics to report
        report["additional_metrics"] = self.metrics_service.get_current_metrics()

        # Step 6: Calculate execution time
        execution_time = time.time() - start_time
        report["execution_time_seconds"] = execution_time

        # Step 7: Save report to file
        report_filename = f"comprehensive_test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report_filepath = self.report_path / report_filename

        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        report["report_file"] = str(report_filepath)

        print(f"Comprehensive test suite completed in {execution_time:.2f} seconds")
        print(f"Report saved to: {report_filepath}")

        return report

    def run_specific_validation_tests(self, categories: List[str] = None, num_queries_per_category: int = 3) -> Dict[str, Any]:
        """
        Run validation tests for specific categories.

        Args:
            categories: List of categories to test. If None, tests all categories.
            num_queries_per_category: Number of queries to test per category

        Returns:
            Dictionary with test results for specific categories
        """
        print(f"Running validation tests for categories: {categories or 'all'}")

        start_time = time.time()

        # If no categories specified, use default set
        if categories is None:
            categories = [
                "AI Fundamentals",
                "Machine Learning",
                "Retrieval Systems",
                "RAG Systems",
                "Embeddings",
                "Neural Networks",
                "NLP"
            ]

        all_test_results = []
        all_validation_summaries = {}

        for category in categories:
            print(f"Testing category: {category}")

            # Create test queries for this category
            category_queries = self.test_query_repository.create_test_queries(num_queries=num_queries_per_category)
            # Filter to only include queries from the specific category
            category_queries = [q for q in category_queries if q.category == category][:num_queries_per_category]

            if not category_queries:
                # If we don't have pre-defined queries for this category, create generic ones
                category_queries = []
                for i in range(num_queries_per_category):
                    query = self.test_query_repository.create_test_queries(num_queries=1)[0]
                    query.category = category
                    category_queries.append(query)

            # Run tests for this category
            category_results = self.test_runner.run_validation_tests(category_queries)
            all_test_results.extend(category_results)

            # Validate relevance for this category
            category_summary = self.test_runner.validate_relevance(category_results)
            all_validation_summaries[category] = category_summary

        # Generate comprehensive report
        report = self.test_runner.generate_test_report(all_test_results)
        report["validation_summaries_by_category"] = all_validation_summaries

        # Add additional metrics
        report["additional_metrics"] = self.metrics_service.get_current_metrics()

        # Calculate execution time
        execution_time = time.time() - start_time
        report["execution_time_seconds"] = execution_time

        # Save report to file
        report_filename = f"category_test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report_filepath = self.report_path / report_filename

        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        report["report_file"] = str(report_filepath)

        print(f"Category-specific test suite completed in {execution_time:.2f} seconds")
        print(f"Report saved to: {report_filepath}")

        return report

    def run_performance_tests(self, num_iterations: int = 10) -> Dict[str, Any]:
        """
        Run performance-focused tests to measure system performance.

        Args:
            num_iterations: Number of iterations to run for performance testing

        Returns:
            Dictionary with performance test results
        """
        print(f"Running performance tests with {num_iterations} iterations...")

        start_time = time.time()

        # Create a simple test query for performance testing
        test_query = self.test_query_repository.create_test_queries(num_queries=1)[0]
        test_query.query_text = "What is artificial intelligence?"
        test_query.category = "Performance Test"

        performance_results = []

        for i in range(num_iterations):
            print(f"Performance iteration {i+1}/{num_iterations}")

            # Run a simple test and capture metrics
            iteration_start = time.time()

            # Use the metrics service directly to measure performance
            result_with_latency = self.metrics_service.measure_latency(
                self.test_runner.retrieval_service.retrieve,
                test_query.query_text,
                k=5
            )

            iteration_time = time.time() - iteration_start

            performance_results.append({
                "iteration": i+1,
                "query_time_seconds": iteration_time,
                "retrieval_latency_ms": result_with_latency["latency_data"]["latency_ms"],
                "retrieved_count": len(result_with_latency["result"]),
                "timestamp": datetime.utcnow().isoformat()
            })

        # Calculate performance metrics
        query_times = [r["query_time_seconds"] for r in performance_results]
        retrieval_latencies = [r["retrieval_latency_ms"] for r in performance_results]

        performance_summary = {
            "total_iterations": num_iterations,
            "average_query_time_seconds": sum(query_times) / len(query_times),
            "min_query_time_seconds": min(query_times),
            "max_query_time_seconds": max(query_times),
            "average_retrieval_latency_ms": sum(retrieval_latencies) / len(retrieval_latencies),
            "min_retrieval_latency_ms": min(retrieval_latencies),
            "max_retrieval_latency_ms": max(retrieval_latencies),
            "results": performance_results
        }

        # Add to metrics service for tracking
        for latency in retrieval_latencies:
            self.metrics_service.record_metric("performance_test_latency", latency)

        execution_time = time.time() - start_time
        performance_summary["total_execution_time_seconds"] = execution_time

        # Save performance report
        report_filename = f"performance_test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report_filepath = self.report_path / report_filename

        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(performance_summary, f, indent=2, ensure_ascii=False, default=str)

        performance_summary["report_file"] = str(report_filepath)

        print(f"Performance tests completed in {execution_time:.2f} seconds")
        print(f"Average query time: {performance_summary['average_query_time_seconds']:.3f}s")
        print(f"Average retrieval latency: {performance_summary['average_retrieval_latency_ms']:.2f}ms")

        return performance_summary

    def generate_final_validation_report(self) -> Dict[str, Any]:
        """
        Generate a final validation report combining all test results.

        Returns:
            Dictionary with final validation report
        """
        print("Generating final validation report...")

        # Run comprehensive test suite
        comprehensive_report = self.run_comprehensive_test_suite()

        # Run performance tests
        performance_report = self.run_performance_tests(num_iterations=5)

        # Get current metrics
        current_metrics = self.metrics_service.get_current_metrics()

        # Combine all information into a final report
        final_report = {
            "report_id": f"final_validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.utcnow().isoformat(),
            "comprehensive_test_results": comprehensive_report,
            "performance_test_results": performance_report,
            "current_metrics": current_metrics,
            "validation_summary": {
                "total_tests_run": comprehensive_report["total_tests_run"],
                "overall_pass_rate": comprehensive_report["summary"]["pass_rate"],
                "average_precision": comprehensive_report["summary"]["average_precision"],
                "average_recall": comprehensive_report["summary"]["average_recall"],
                "average_f1_score": comprehensive_report["summary"]["average_f1_score"],
                "average_response_time_ms": current_metrics["aggregated_data"]["latency_metrics"]["avg_latency_ms"],
                "system_status": "validated" if comprehensive_report["summary"]["pass_rate"] >= 0.8 else "requires_attention"
            }
        }

        # Save final report
        report_filename = f"final_validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report_filepath = self.report_path / report_filename

        with open(report_filepath, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)

        final_report["report_file"] = str(report_filepath)

        print(f"Final validation report generated and saved to: {report_filepath}")
        print(f"Overall pass rate: {final_report['validation_summary']['overall_pass_rate']:.2%}")
        print(f"System status: {final_report['validation_summary']['system_status']}")

        return final_report


# Global test suite instance
comprehensive_test_suite = ComprehensiveTestSuite()