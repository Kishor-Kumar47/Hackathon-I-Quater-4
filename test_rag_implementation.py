import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables from backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

# Add backend to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_rag_agent():
    """Test the RAG agent functionality"""
    try:
        from backend.app.services.agent import RAGAgent

        print("Testing RAG Agent...")

        # Initialize the agent
        agent = RAGAgent()

        # Test query without context
        print("\n1. Testing query without context:")
        response = agent.process_query("What is this document about?")
        print(f"Response: {response['answer']}")

        # Test query with context
        print("\n2. Testing query with context:")
        context = "This is a sample context about artificial intelligence and machine learning."
        response = agent.process_query("What is this text about?", context)
        print(f"Response: {response['answer']}")

        print("\n[SUCCESS] RAG Agent tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error testing RAG Agent: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qdrant_retrieval():
    """Test the Qdrant retrieval functionality"""
    try:
        from backend.app.services.qdrant_retriever import QdrantRetrievalService

        print("\nTesting Qdrant Retrieval...")

        # Initialize the retrieval service
        retrieval_service = QdrantRetrievalService()

        # Test retrieval
        print("\n3. Testing retrieval from Qdrant:")
        documents = retrieval_service.retrieve("test query", k=2)
        print(f"Retrieved {len(documents)} documents")
        for i, doc in enumerate(documents):
            print(f"  Document {i+1}: {doc.get('content', '')[:100]}...")

        print("\n[SUCCESS] Qdrant Retrieval tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error testing Qdrant Retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running RAG Implementation Tests...\n")

    success1 = test_rag_agent()
    success2 = test_qdrant_retrieval()

    if success1 and success2:
        print("\n[SUCCESS] All tests passed! RAG implementation is working correctly.")
    else:
        print("\n[ERROR] Some tests failed. Please check the implementation.")