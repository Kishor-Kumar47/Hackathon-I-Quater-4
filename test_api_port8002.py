import requests
import json

# Test the health endpoint
print("Testing health endpoint...")
try:
    response = requests.get("http://localhost:8002/health")
    print(f"Health check response: {response.json()}")
    print(f"Status code: {response.status_code}")
except Exception as e:
    print(f"Error testing health endpoint: {e}")

# Test the chat endpoint
print("\nTesting chat endpoint...")
try:
    payload = {
        "query": "What is this document about?",
        "context": "This is a sample context about artificial intelligence and machine learning."
    }

    response = requests.post("http://localhost:8002/api/chat",
                           json=payload,
                           headers={"Content-Type": "application/json"})

    print(f"Chat response: {response.json()}")
    print(f"Status code: {response.status_code}")
except Exception as e:
    print(f"Error testing chat endpoint: {e}")
    print("This is expected if the OpenAI API call fails due to network or API key issues,")
    print("but the server should still be running and the error should be handled gracefully.")