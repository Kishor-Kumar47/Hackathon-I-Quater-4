# backend/validation.py

import os
import json
from typing import List, Dict

import cohere
import qdrant_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Placeholder for functions to be added in subsequent tasks

def get_cohere_embedding(text: str, model_name: str = "embed-english-light-v3.0") -> List[float]:
    """
    Generates a vector embedding for a given text using Cohere.

    Args:
        text: The input text.
        model_name: The name of the Cohere model to use.

    Returns:
        A list of floats representing the embedding.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[text],
        model=model_name,
        input_type="search_query"
    )
    return response.embeddings[0]


def search_qdrant(embedding: List[float], top_k: int) -> List[Dict]:
    """
    Performs a similarity search in Qdrant.

    Args:
        embedding: The query vector.
        top_k: The number of results to retrieve.

    Returns:
        A list of dictionaries, each representing a retrieved chunk.
    """
    client = qdrant_client.QdrantClient(
        host=os.getenv("QDRANT_HOST"), 
        api_key=os.getenv("QDRANT_API_KEY")
    )

    search_result = client.search(
        collection_name=os.getenv("QDRANT_COLLECTION"),
        query_vector=embedding,
        limit=top_k,
        with_payload=True
    )

    retrieved_chunks = []
    for point in search_result:
        retrieved_chunks.append({
            "id": point.id,
            "document_id": point.payload.get("document_id"),
            "text": point.payload.get("text"),
            "score": point.score
        })
    return retrieved_chunks


def run_validation_suite(test_cases: List[Dict], top_k: int = 10) -> List[Dict]:
    """
    Iterates through test cases, queries Qdrant, and returns results.

    Args:
        test_cases: A list of dictionaries, each conforming to the GoldenTestCase model.
        top_k: The number of results to retrieve from Qdrant.

    Returns:
        A list of result dictionaries, each conforming to the ValidationResult model.
    """
    results = []
    for i, case in enumerate(test_cases):
        print(f"Running test case {i+1}/{len(test_cases)}: {case['query']}")
        query = case["query"]
        expected_doc_id = case["expected_document_id"]

        embedding = get_cohere_embedding(query)
        retrieved_chunks = search_qdrant(embedding, top_k)

        retrieved_ids = [chunk["document_id"] for chunk in retrieved_chunks]
        is_present = expected_doc_id in retrieved_ids
        rank = retrieved_ids.index(expected_doc_id) + 1 if is_present else None

        result = {
            "query": query,
            "expected_document_id": expected_doc_id,
            "is_present_in_top_k": is_present,
            "rank": rank,
            "retrieved_ids": retrieved_ids
        }
        results.append(result)

        if not is_present:
            print(json.dumps({
                "query": query,
                "expected_document_id": expected_doc_id,
                "is_present_in_top_k": False,
                "rank": None,
                "retrieved_ids": retrieved_ids
            }, indent=2))

    return results


def calculate_summary_metrics(results: List[Dict], top_k: int) -> Dict:
    """
    Calculates Recall@K and MRR from a list of validation results.

    Args:
        results: A list of ValidationResult dictionaries.
        top_k: The 'K' value used for the run.

    Returns:
        A dictionary containing the summary report fields.
    """
    total_cases = len(results)
    if total_cases == 0:
        return {
            "Total Test Cases": 0,
            f"Recall@K (K={top_k})": 0,
            "Mean Reciprocal Rank (MRR)": 0
        }

    recall_count = sum(1 for r in results if r["is_present_in_top_k"])
    recall = recall_count / total_cases

    mrr_sum = sum(1 / r["rank"] for r in results if r["rank"] is not None)
    mrr = mrr_sum / total_cases

    return {
        "Total Test Cases": total_cases,
        f"Recall@K (K={top_k})": recall,
        "Mean Reciprocal Rank (MRR)": mrr
    }




