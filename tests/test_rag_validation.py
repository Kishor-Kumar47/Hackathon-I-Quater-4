# tests/test_rag_validation.py

import json
import os

import pytest
from backend import validation

# Define the path to the golden test dataset
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "rag_validation_dataset.json")

def test_retrieval_pipeline_accuracy():
    """
    Loads the golden dataset, runs validation for each case,
    and asserts that the final metrics meet the acceptance criteria.
    """
    with open(FIXTURE_PATH, 'r') as f:
        golden_dataset = json.load(f)
    
    assert golden_dataset, "Golden dataset could not be loaded or is empty"

    top_k = 10
    results = validation.run_validation_suite(golden_dataset, top_k=top_k)
    summary = validation.calculate_summary_metrics(results, top_k=top_k)

    print("\n\n" + "="*30)
    print("Validation Run Summary:")
    print("="*30)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    print("="*30 + "\n")

    recall_key = f"Recall@K (K={top_k})"
    assert summary[recall_key] >= 0.95, f"Recall@K of {summary[recall_key]} is below the 0.95 threshold."




