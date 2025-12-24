from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import time
import statistics
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class MetricRecord:
    """Represents a single metric record."""
    timestamp: datetime
    metric_type: str
    value: float
    labels: Optional[Dict[str, str]] = None


class MetricsService:
    """
    Service class for collecting and tracking performance metrics in the backend.
    """

    def __init__(self, storage_path: Optional[str] = None):
        # Store metrics data
        self.query_latency_history = deque(maxlen=1000)  # Keep last 1000 measurements
        self.accuracy_metrics_history = deque(maxlen=1000)
        self.performance_data = defaultdict(list)

        # Time-series metrics
        self.metrics_buffer = deque(maxlen=10000)  # Buffer for real-time metrics
        self.hourly_aggregates = defaultdict(list)
        self.daily_aggregates = defaultdict(list)

        # Storage path for persistence
        if storage_path is None:
            project_root = Path(__file__).parent.parent.parent
            self.storage_path = project_root / "metrics_data"
        else:
            self.storage_path = Path(storage_path)

        # Create storage directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)

        print(f"MetricsService initialized with storage at: {self.storage_path}")

    def measure_latency(self, query_func, *args, **kwargs) -> Dict[str, Any]:
        """
        Track query execution time.

        Args:
            query_func: The function to execute and measure
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Dictionary with latency metrics and function result
        """
        start_time = time.time()

        try:
            # Execute the function
            result = query_func(*args, **kwargs)

            # Calculate latency
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000

            # Store latency metric
            latency_data = {
                "latency_ms": latency_ms,
                "timestamp": datetime.utcnow().isoformat(),
            }

            self.query_latency_history.append(latency_data)

            # Record in time-series metrics
            self.record_metric("query_latency", latency_ms, {"endpoint": "retrieval"})

            # Return both the result and latency data
            return {
                "result": result,
                "latency_data": latency_data
            }

        except Exception as e:
            print(f"Error measuring latency: {str(e)}")
            raise

    def calculate_accuracy_metrics(self, retrieved_chunks: List[Dict], expected_chunks: List[Dict] = None) -> Dict[str, float]:
        """
        Calculate retrieval accuracy metrics.

        Args:
            retrieved_chunks: List of chunks actually retrieved
            expected_chunks: List of expected chunks for comparison (optional)

        Returns:
            Dictionary with accuracy metrics
        """
        try:
            if expected_chunks is None or len(expected_chunks) == 0:
                # If no expected chunks, calculate basic metrics based on retrieved chunks
                metrics = {
                    "total_retrieved": len(retrieved_chunks),
                    "avg_score": statistics.mean([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "max_score": max([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "min_score": min([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "precision": 0,  # Can't calculate without expected
                    "recall": 0,     # Can't calculate without expected
                    "f1_score": 0    # Can't calculate without expected
                }
            else:
                # Calculate precision, recall, F1 based on expected vs actual
                expected_ids = {chunk.get("id") for chunk in expected_chunks if chunk.get("id")}
                actual_ids = {chunk.get("id") for chunk in retrieved_chunks if chunk.get("id")}

                true_positives = len(expected_ids.intersection(actual_ids))
                false_positives = len(actual_ids - expected_ids)
                false_negatives = len(expected_ids - actual_ids)

                precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
                recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
                f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

                metrics = {
                    "total_retrieved": len(retrieved_chunks),
                    "total_expected": len(expected_chunks),
                    "true_positives": true_positives,
                    "false_positives": false_positives,
                    "false_negatives": false_negatives,
                    "avg_score": statistics.mean([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "max_score": max([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "min_score": min([chunk.get("score", 0) for chunk in retrieved_chunks]) if retrieved_chunks else 0,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score
                }

            # Store accuracy metric
            accuracy_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": metrics
            }
            self.accuracy_metrics_history.append(accuracy_data)

            # Record in time-series metrics
            if "precision" in metrics:
                self.record_metric("precision", metrics["precision"])
            if "recall" in metrics:
                self.record_metric("recall", metrics["recall"])
            if "f1_score" in metrics:
                self.record_metric("f1_score", metrics["f1_score"])

            return metrics

        except Exception as e:
            print(f"Error calculating accuracy metrics: {str(e)}")
            raise

    def aggregate_performance_data(self) -> Dict[str, Any]:
        """
        Summarize metrics data.

        Returns:
            Dictionary with aggregated performance metrics
        """
        try:
            # Aggregate latency metrics
            if self.query_latency_history:
                latencies = [item["latency_ms"] for item in self.query_latency_history]
                latency_metrics = {
                    "count": len(latencies),
                    "avg_latency_ms": statistics.mean(latencies),
                    "median_latency_ms": statistics.median(latencies),
                    "min_latency_ms": min(latencies),
                    "max_latency_ms": max(latencies),
                    "p95_latency_ms": self._calculate_percentile(latencies, 95) if len(latencies) > 1 else 0,
                    "p99_latency_ms": self._calculate_percentile(latencies, 99) if len(latencies) > 1 else 0
                }
            else:
                latency_metrics = {
                    "count": 0,
                    "avg_latency_ms": 0,
                    "median_latency_ms": 0,
                    "min_latency_ms": 0,
                    "max_latency_ms": 0,
                    "p95_latency_ms": 0,
                    "p99_latency_ms": 0
                }

            # Aggregate accuracy metrics
            if self.accuracy_metrics_history:
                precisions = [item["metrics"]["precision"] for item in self.accuracy_metrics_history]
                recalls = [item["metrics"]["recall"] for item in self.accuracy_metrics_history]
                f1_scores = [item["metrics"]["f1_score"] for item in self.accuracy_metrics_history]

                accuracy_metrics = {
                    "count": len(self.accuracy_metrics_history),
                    "avg_precision": statistics.mean(precisions),
                    "avg_recall": statistics.mean(recalls),
                    "avg_f1_score": statistics.mean(f1_scores),
                    "min_precision": min(precisions) if precisions else 0,
                    "max_precision": max(precisions) if precisions else 1,
                    "min_recall": min(recalls) if recalls else 0,
                    "max_recall": max(recalls) if recalls else 1,
                    "min_f1_score": min(f1_scores) if f1_scores else 0,
                    "max_f1_score": max(f1_scores) if f1_scores else 1
                }
            else:
                accuracy_metrics = {
                    "count": 0,
                    "avg_precision": 0,
                    "avg_recall": 0,
                    "avg_f1_score": 0,
                    "min_precision": 0,
                    "max_precision": 0,
                    "min_recall": 0,
                    "max_recall": 0,
                    "min_f1_score": 0,
                    "max_f1_score": 0
                }

            # Create aggregated result
            aggregated_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "latency_metrics": latency_metrics,
                "accuracy_metrics": accuracy_metrics,
                "total_queries_measured": len(self.query_latency_history),
                "total_accuracy_measurements": len(self.accuracy_metrics_history)
            }

            return aggregated_data

        except Exception as e:
            print(f"Error aggregating performance data: {str(e)}")
            raise

    def _calculate_percentile(self, data: List[float], percentile: float) -> float:
        """
        Calculate percentile of a data set.

        Args:
            data: List of numeric values
            percentile: Percentile to calculate (e.g., 95 for 95th percentile)

        Returns:
            Calculated percentile value
        """
        if not data:
            return 0

        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)

        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index

            if upper_index >= len(sorted_data):
                return sorted_data[lower_index]

            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight

    def record_metric(self, metric_type: str, value: float, labels: Optional[Dict[str, str]] = None, timestamp: Optional[datetime] = None):
        """
        Record a metric value with optional labels and timestamp.

        Args:
            metric_type: Type of metric (e.g., 'query_latency', 'accuracy_score')
            value: Numeric value of the metric
            labels: Optional labels to attach to the metric
            timestamp: Optional timestamp for the metric (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        metric_record = {
            "timestamp": timestamp.isoformat(),
            "metric_type": metric_type,
            "value": value,
            "labels": labels or {}
        }

        # Add to buffer
        self.metrics_buffer.append(metric_record)

        # Also store in time-bucketed aggregates
        hour_key = timestamp.strftime("%Y-%m-%d-%H")  # YYYY-MM-DD-HH
        day_key = timestamp.strftime("%Y-%m-%d")      # YYYY-MM-DD

        # Add to hourly aggregates
        self.hourly_aggregates[hour_key].append(metric_record)

        # Add to daily aggregates
        self.daily_aggregates[day_key].append(metric_record)

    def get_recent_metrics(self, metric_type: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get recent metrics of a specific type.

        Args:
            metric_type: Type of metric to retrieve
            hours: Number of hours to look back

        Returns:
            List of metric records
        """
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            recent_metrics = []

            for record in self.metrics_buffer:
                record_time = datetime.fromisoformat(record["timestamp"])
                if record_time >= cutoff_time and record["metric_type"] == metric_type:
                    recent_metrics.append(record)

            return recent_metrics

        except Exception as e:
            print(f"Error getting recent metrics: {str(e)}")
            return []

    def get_hourly_aggregates(self, metric_type: str, days: int = 7) -> Dict[str, Dict[str, float]]:
        """
        Get hourly aggregated metrics for the specified number of days.

        Args:
            metric_type: Type of metric to aggregate
            days: Number of days to look back

        Returns:
            Dictionary with hourly aggregates
        """
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
            hourly_aggregates = {}

            for hour_key, records in self.hourly_aggregates.items():
                # Check if this hour is within our lookback period
                hour_date = hour_key.split('-')[:3]  # Get YYYY-MM-DD part
                hour_date_str = "-".join(hour_date)

                if hour_date_str >= cutoff_date:
                    # Filter records for this metric type
                    metric_records = [r for r in records if r["metric_type"] == metric_type]

                    if metric_records:
                        values = [r["value"] for r in metric_records]
                        hourly_aggregates[hour_key] = {
                            "count": len(values),
                            "avg": statistics.mean(values),
                            "min": min(values),
                            "max": max(values),
                            "p95": self._calculate_percentile(values, 95) if len(values) > 1 else values[0] if values else 0,
                            "p99": self._calculate_percentile(values, 99) if len(values) > 1 else values[0] if values else 0
                        }

            return hourly_aggregates

        except Exception as e:
            print(f"Error getting hourly aggregates: {str(e)}")
            return {}

    def get_daily_aggregates(self, metric_type: str, days: int = 30) -> Dict[str, Dict[str, float]]:
        """
        Get daily aggregated metrics for the specified number of days.

        Args:
            metric_type: Type of metric to aggregate
            days: Number of days to look back

        Returns:
            Dictionary with daily aggregates
        """
        try:
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
            daily_aggregates = {}

            for day_key, records in self.daily_aggregates.items():
                if day_key >= cutoff_date:
                    # Filter records for this metric type
                    metric_records = [r for r in records if r["metric_type"] == metric_type]

                    if metric_records:
                        values = [r["value"] for r in metric_records]
                        daily_aggregates[day_key] = {
                            "count": len(values),
                            "avg": statistics.mean(values),
                            "min": min(values),
                            "max": max(values),
                            "p95": self._calculate_percentile(values, 95) if len(values) > 1 else values[0] if values else 0,
                            "p99": self._calculate_percentile(values, 99) if len(values) > 1 else values[0] if values else 0
                        }

            return daily_aggregates

        except Exception as e:
            print(f"Error getting daily aggregates: {str(e)}")
            return {}

    def save_metrics_to_file(self, filename: Optional[str] = None) -> bool:
        """
        Save current metrics buffer to a file.

        Args:
            filename: Optional filename to save as (without extension)

        Returns:
            True if save was successful, False otherwise
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"metrics_{timestamp}"

            filepath = self.storage_path / f"{filename}.json"

            # Convert metrics buffer to list for JSON serialization
            metrics_data = list(self.metrics_buffer)

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, indent=2, ensure_ascii=False)

            print(f"Saved metrics to {filepath}")

            return True

        except Exception as e:
            print(f"Failed to save metrics to file: {str(e)}")
            return False

    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics snapshot.

        Returns:
            Dictionary with current metrics
        """
        current_metrics = {
            "query_latency_history_size": len(self.query_latency_history),
            "accuracy_metrics_history_size": len(self.accuracy_metrics_history),
            "aggregated_data": self.aggregate_performance_data(),
            "last_updated": datetime.utcnow().isoformat()
        }

        return current_metrics

    def reset_metrics(self):
        """
        Reset all collected metrics.
        """
        self.query_latency_history.clear()
        self.accuracy_metrics_history.clear()
        self.metrics_buffer.clear()
        self.hourly_aggregates.clear()
        self.daily_aggregates.clear()
        print("Metrics reset successfully")


# Global metrics service instance
metrics_service = MetricsService()