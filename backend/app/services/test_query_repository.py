from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path


@dataclass
class TestQuery:
    """Represents a test query for validation."""
    id: str
    query_text: str
    expected_chunks: List[Dict[str, Any]]
    category: str
    priority: int = 3  # 1-5 scale, 3 is default
    created_at: Optional[datetime] = None
    last_run: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class TestQueryRepository:
    """
    Repository for managing test queries used in validation.
    """

    def __init__(self, storage_path: Optional[str] = None):
        # Storage path for test queries
        if storage_path is None:
            project_root = Path(__file__).parent.parent.parent
            self.storage_path = project_root / "test_queries"
        else:
            self.storage_path = Path(storage_path)

        # Create storage directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)

        print(f"TestQueryRepository initialized with storage at: {self.storage_path}")

    def create_test_queries(self, num_queries: int = 5) -> List[TestQuery]:
        """
        Generate 5+ test queries covering book topics as specified in requirements.

        Args:
            num_queries: Number of test queries to generate

        Returns:
            List of TestQuery objects
        """
        # Sample test queries covering book topics
        sample_queries_data = [
            {
                "id": "ai_fundamentals_001",
                "query_text": "What is artificial intelligence and how does it work?",
                "category": "AI Fundamentals",
                "expected_chunks": [
                    {
                        "id": "ai_def_001",
                        "text": "Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
                        "score": 1.0,
                        "source": "ai_textbook_ch1"
                    }
                ]
            },
            {
                "id": "ml_concepts_001",
                "query_text": "Explain machine learning concepts and algorithms",
                "category": "Machine Learning",
                "expected_chunks": [
                    {
                        "id": "ml_concept_001",
                        "text": "Machine learning is a method of data analysis that automates analytical model building.",
                        "score": 1.0,
                        "source": "ml_textbook_ch2"
                    }
                ]
            },
            {
                "id": "vector_search_001",
                "query_text": "How does vector search work in retrieval systems?",
                "category": "Retrieval Systems",
                "expected_chunks": [
                    {
                        "id": "vector_search_001",
                        "text": "Vector search is a technique that finds items similar to a query item based on the similarity of their vector representations.",
                        "score": 1.0,
                        "source": "search_textbook_ch5"
                    }
                ]
            },
            {
                "id": "rag_systems_001",
                "query_text": "What are the key components of a RAG system?",
                "category": "RAG Systems",
                "expected_chunks": [
                    {
                        "id": "rag_components_001",
                        "text": "RAG (Retrieval-Augmented Generation) systems combine information retrieval with text generation to produce more accurate and contextually relevant responses.",
                        "score": 1.0,
                        "source": "rag_textbook_ch3"
                    }
                ]
            },
            {
                "id": "embedding_gen_001",
                "query_text": "Describe the process of embedding generation",
                "category": "Embeddings",
                "expected_chunks": [
                    {
                        "id": "embedding_001",
                        "text": "Embedding generation is the process of converting text, images, or other data types into numerical vectors that represent their semantic meaning.",
                        "score": 1.0,
                        "source": "embedding_textbook_ch4"
                    }
                ]
            },
            {
                "id": "neural_nets_001",
                "query_text": "How do neural networks learn from data?",
                "category": "Neural Networks",
                "expected_chunks": [
                    {
                        "id": "nn_learning_001",
                        "text": "Neural networks learn from data through a process called backpropagation, where the network adjusts its weights based on the error of its predictions.",
                        "score": 1.0,
                        "source": "nn_textbook_ch6"
                    }
                ]
            },
            {
                "id": "nlp_apps_001",
                "query_text": "What are the applications of natural language processing?",
                "category": "NLP",
                "expected_chunks": [
                    {
                        "id": "nlp_apps_001",
                        "text": "Natural Language Processing (NLP) has applications in machine translation, sentiment analysis, chatbots, and text summarization.",
                        "score": 1.0,
                        "source": "nlp_textbook_ch7"
                    }
                ]
            }
        ]

        # Generate the required number of test queries
        test_queries = []
        for i in range(min(num_queries, len(sample_queries_data))):
            query_data = sample_queries_data[i]
            test_query = TestQuery(
                id=query_data["id"],
                query_text=query_data["query_text"],
                expected_chunks=query_data["expected_chunks"],
                category=query_data["category"],
                priority=3  # Default priority
            )
            test_queries.append(test_query)

        # If we need more queries than our sample, create additional generic ones
        while len(test_queries) < num_queries:
            additional_query = TestQuery(
                id=f"additional_query_{len(test_queries) + 1}",
                query_text=f"Additional test query {len(test_queries) + 1}",
                expected_chunks=[],
                category="general",
                priority=2
            )
            test_queries.append(additional_query)

        print(f"Created {len(test_queries)} test queries")

        return test_queries

    def save_test_queries(self, test_queries: List[TestQuery], filename: str = None) -> bool:
        """
        Save test queries to storage.

        Args:
            test_queries: List of TestQuery objects to save
            filename: Optional filename to save as (without extension)

        Returns:
            True if save was successful, False otherwise
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_queries_{timestamp}"

            filepath = self.storage_path / f"{filename}.json"

            # Convert TestQuery objects to dictionaries for JSON serialization
            queries_data = []
            for query in test_queries:
                query_dict = {
                    "id": query.id,
                    "query_text": query.query_text,
                    "expected_chunks": query.expected_chunks,
                    "category": query.category,
                    "priority": query.priority,
                    "created_at": query.created_at.isoformat() if query.created_at else None,
                    "last_run": query.last_run.isoformat() if query.last_run else None
                }
                queries_data.append(query_dict)

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(queries_data, f, indent=2, ensure_ascii=False)

            print(f"Saved {len(test_queries)} test queries to {filepath}")

            return True

        except Exception as e:
            print(f"Failed to save test queries: {str(e)}")
            return False

    def load_test_queries(self, filename: str) -> List[TestQuery]:
        """
        Load test queries from storage.

        Args:
            filename: Name of the file to load (without extension, assumes .json)

        Returns:
            List of TestQuery objects
        """
        try:
            filepath = self.storage_path / f"{filename}.json"

            if not filepath.exists():
                print(f"Test queries file not found: {filepath}")
                return []

            with open(filepath, 'r', encoding='utf-8') as f:
                queries_data = json.load(f)

            test_queries = []

            for query_data in queries_data:
                test_query = TestQuery(
                    id=query_data["id"],
                    query_text=query_data["query_text"],
                    expected_chunks=query_data["expected_chunks"],
                    category=query_data["category"],
                    priority=query_data["priority"],
                    created_at=datetime.fromisoformat(query_data["created_at"]) if query_data["created_at"] else None,
                    last_run=datetime.fromisoformat(query_data["last_run"]) if query_data["last_run"] else None
                )

                test_queries.append(test_query)

            print(f"Loaded {len(test_queries)} test queries from {filepath}")

            return test_queries

        except Exception as e:
            print(f"Failed to load test queries: {str(e)}")
            return []

    def get_test_queries_by_category(self, category: str) -> List[TestQuery]:
        """
        Get all test queries for a specific category.

        Args:
            category: Category to filter by

        Returns:
            List of TestQuery objects matching the category
        """
        try:
            # Get all JSON files in the storage directory
            all_queries = []
            for filepath in self.storage_path.glob("*.json"):
                try:
                    queries = self.load_test_queries(filepath.stem)
                    category_queries = [q for q in queries if q.category == category]
                    all_queries.extend(category_queries)
                except Exception as e:
                    print(f"Error loading queries from {filepath}: {str(e)}")

            print(f"Found {len(all_queries)} test queries for category: {category}")

            return all_queries

        except Exception as e:
            print(f"Failed to get test queries by category: {str(e)}")
            return []

    def update_test_query(self, test_query: TestQuery) -> bool:
        """
        Update an existing test query.

        Args:
            test_query: Updated TestQuery object

        Returns:
            True if update was successful, False otherwise
        """
        try:
            print(f"Updating test query: {test_query.id}")

            # For this implementation, we'll save the updated query to a new file
            # In a more sophisticated implementation, we might have a more complex update strategy
            return self.save_test_queries([test_query], f"updated_{test_query.id}")

        except Exception as e:
            print(f"Failed to update test query: {str(e)}")
            return False


# Global test query repository instance
test_query_repository = TestQueryRepository()