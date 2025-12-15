import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_client = cohere.Client("bWYvP3G00QJYeSsIhd7BGzsV8TbTCv5cxkxE2Xdj")

# Connect to Qdrant
qdrant = QdrantClient(
    url="https://0c88e8c5-47c1-47b3-97f1-0c64f1d8a959.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.nzUI8Ugt8CouKq6w1J5fCHjqFhdsgl-MJJh0f9fuTgA", 
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="ai_book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]

# Test
print(retrieve("What data do you have?"))