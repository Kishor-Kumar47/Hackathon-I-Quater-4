
# from backend.app.api.auth import router as auth_router
# from backend.app.services.qdrant_service import get_qdrant_collections

# from fastapi import FastAPI


# app = FastAPI()

# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# @app.get("/")
# async def root():
#     return {"message": "Physical AI Book Backend"}

# @app.get("/api/qdrant/collections")
# async def get_collections_endpoint():
#     collections = get_qdrant_collections()
#     return {"collections": collections.collections}




# ...........................................................................................................



import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere

from dotenv import load_dotenv
import os

load_dotenv()



# -------------------------------------
# CONFIG
# -------------------------------------
# Your Deployment Link:
SITEMAP_URL = "https://hackathon-i-quater-4.vercel.app/sitemap.xml"
COLLECTION_NAME = "ai_book"

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
EMBED_MODEL = "embed-english-v3.0"

# Connect to Qdrant Cloud
qdrant = QdrantClient(
    url="https://0c88e8c5-47c1-47b3-97f1-0c64f1d8a959.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.nzUI8Ugt8CouKq6w1J5fCHjqFhdsgl-MJJh0f9fuTgA", 
)

# -------------------------------------
# Step 1 — Extract URLs from sitemap
# -------------------------------------
# def get_all_urls(sitemap_url):
#     xml = requests.get(sitemap_url).text
#     root = ET.fromstring(xml)

#     urls = []
#     for child in root:
#         loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
#         if loc_tag is not None:
#             urls.append(loc_tag.text)

#     print("\nFOUND URLS:")
#     for u in urls:
#         print(" -", u)

#     return urls




def get_all_urls(sitemap_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(sitemap_url, headers=headers, timeout=20)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    urls = []

    for child in root:
        loc = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None:
            urls.append(loc.text)

    return urls






# -------------------------------------
# Step 2 — Download page + extract text
# -------------------------------------
# def extract_text_from_url(url):
#     html = requests.get(url).text
#     text = trafilatura.extract(html)

#     if not text:
#         print("[WARNING] No text extracted from:", url)

#     return text




def extract_text_from_url(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            print("[WARNING] Failed to fetch:", url)
            return None

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False
        )

        if not text or len(text.strip()) < 100:
            print("[WARNING] No meaningful text extracted from:", url)
            return None

        return text

    except Exception as e:
        print("[ERROR] Extraction failed:", url, e)
        return None





# -------------------------------------
# Step 3 — Chunk the text
# -------------------------------------
def chunk_text(text, max_chars=1200):
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos:]
    chunks.append(text)
    return chunks


# -------------------------------------
# Step 4 — Create embedding
# -------------------------------------
# def embed(text):
#     response = cohere_client.embed(
#         model=EMBED_MODEL,
#         input_type="search_query",  # Use search_query for queries
#         texts=[text],
#     )
#     return response.embeddings[0]  # Return the first embedding


def embed(text):
    res = cohere_client.embed(
        model=EMBED_MODEL,
        input_type="search_document",
        texts=[text],
    )
    return res.embeddings[0]




# -------------------------------------
# Step 5 — Store in Qdrant
# -------------------------------------
def create_collection():
    print("\nCreating Qdrant collection...")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
        size=1024,        # Cohere embed-english-v3.0 dimension
        distance=Distance.COSINE
        )
    )

def save_chunk_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "url": url,
                    "text": chunk,
                    "chunk_id": chunk_id
                }
            )
        ]
    )


# -------------------------------------
# MAIN INGESTION PIPELINE
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)

    create_collection()

    global_id = 1

    for url in urls:
        print("\nProcessing:", url)
        text = extract_text_from_url(url)

        if not text:
            continue

        chunks = chunk_text(text)

        for ch in chunks:
            save_chunk_to_qdrant(ch, global_id, url)
            print(f"Saved chunk {global_id}")
            global_id += 1

    print("\n✔️ Ingestion completed!")
    print("Total chunks stored:", global_id - 1)


if __name__ == "__main__":
    ingest_book()