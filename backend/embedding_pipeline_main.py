import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openai
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client for embeddings
openai_api_key = os.getenv("OPENROUTER_API_KEY")
if not openai_api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")
client = OpenAI(
    api_key=openai_api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")
qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)


def get_sitemap_urls(sitemap_url):
    """
    Get all URLs from the sitemap.xml file.

    Args:
        sitemap_url (str): The URL of the sitemap.xml file

    Returns:
        list: List of all URLs found in the sitemap
    """
    logger.info(f"Fetching sitemap from {sitemap_url}")
    urls = set()

    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)

            # Handle both regular sitemaps and sitemap indexes
            if root.tag.endswith('sitemapindex'):
                # This is a sitemap index, need to fetch individual sitemaps
                for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    sitemap_loc = sitemap.text.strip()
                    logger.info(f"Processing sitemap: {sitemap_loc}")
                    sub_response = requests.get(sitemap_loc, timeout=10)
                    if sub_response.status_code == 200:
                        sub_root = ET.fromstring(sub_response.content)
                        for url in sub_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                            urls.add(url.text.strip())
            else:
                # This is a regular sitemap
                for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    urls.add(url.text.strip())
    except Exception as e:
        logger.error(f"Error fetching sitemap {sitemap_url}: {e}")
        logger.info("Falling back to crawling method")
        # Fallback to the original crawling method
        return get_all_urls_from_base_url(sitemap_url.replace('/sitemap.xml', ''))

    urls_list = list(urls)
    logger.info(f"Found {len(urls_list)} URLs from sitemap")
    return urls_list


def get_all_urls_from_base_url(base_url):
    """
    Get all URLs from the deployed website by crawling internal links (fallback method).

    Args:
        base_url (str): The base URL of the deployed website

    Returns:
        list: List of all URLs found on the website
    """
    logger.info(f"Starting to crawl {base_url}")
    urls = set()
    visited = set()

    def crawl_url(url):
        if url in visited:
            return
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Add current URL to the list
                urls.add(url)

                # Find all internal links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)

                    # Only add internal links from the same domain
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        if full_url not in visited and full_url not in urls:
                            urls.add(full_url)
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")

    # Start with the base URL
    crawl_url(base_url)

    # For a more thorough crawl, we could recursively visit found URLs
    # But for now, we'll just get links from the main page
    urls_list = list(urls)
    logger.info(f"Found {len(urls_list)} URLs")
    return urls_list


def get_all_urls(base_url):
    """
    Get all URLs from the deployed website, using sitemap if available.

    Args:
        base_url (str): The base URL of the deployed website

    Returns:
        list: List of all URLs found on the website
    """
    sitemap_url = base_url.rstrip('/') + '/sitemap.xml'
    logger.info(f"Attempting to fetch sitemap from {sitemap_url}")

    # Try to get URLs from sitemap first
    urls = get_sitemap_urls(sitemap_url)

    # If sitemap didn't return any URLs, fall back to crawling
    if not urls:
        logger.info("No URLs found from sitemap, falling back to crawling method")
        urls = get_all_urls_from_base_url(base_url)

    return urls


def extract_text_from_url(url):
    """
    Extract clean text content from a given URL.

    Args:
        url (str): The URL to extract text from

    Returns:
        str: Clean text content from the URL
    """
    logger.info(f"Extracting text from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        logger.info(f"Extracted {len(text)} characters from {url}")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return ""


def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Split text into chunks with overlap.

    Args:
        text (str): The text to chunk
        chunk_size (int): Maximum size of each chunk
        overlap (int): Number of characters to overlap between chunks

    Returns:
        list: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward by chunk_size - overlap
        start = end - overlap

        # If the remaining text is less than chunk_size, take it all
        if len(text) - start < chunk_size:
            if start < len(text):
                chunks.append(text[start:])
            break

    logger.info(f"Text chunked into {len(chunks)} chunks")
    return chunks


def embed(texts):
    """
    Generate embeddings for a list of texts using OpenRouter.

    Args:
        texts (list): List of texts to embed

    Returns:
        list: List of embeddings
    """
    logger.info(f"Generating embeddings for {len(texts)} texts")
    try:
        # Use OpenRouter embeddings API - using a common embedding model
        response = client.embeddings.create(
            model="text-embedding-3-small",  # Using OpenAI's newer embedding model
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        logger.info("Embeddings generated successfully")
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []


def create_collection(collection_name="rag_embedding"):
    """
    Create a Qdrant collection for storing embeddings.

    Args:
        collection_name (str): Name of the collection to create
    """
    logger.info(f"Creating Qdrant collection: {collection_name}")
    try:
        # Check if collection already exists
        try:
            qdrant_client.get_collection(collection_name)
            logger.info(f"Collection {collection_name} already exists")
            return
        except:
            # Collection doesn't exist, so create it
            pass

        # Create the collection - OpenAI ada-002 embeddings are 1536-dimensional
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1536,  # OpenAI ada-002 model outputs 1536-dimensional vectors
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Collection {collection_name} created successfully")
    except Exception as e:
        logger.error(f"Error creating collection {collection_name}: {e}")


def save_chunk_to_qdrant(text_chunk, embedding, url, collection_name="rag_embedding"):
    """
    Save a text chunk with its embedding to Qdrant.

    Args:
        text_chunk (str): The text chunk
        embedding (list): The embedding vector
        url (str): The source URL
        collection_name (str): Name of the collection to save to
    """
    logger.info(f"Saving chunk to Qdrant collection: {collection_name}")
    try:
        # Create a point for Qdrant
        point = models.PointStruct(
            id=len(qdrant_client.scroll(collection_name=collection_name, limit=1)[0]) + 1,  # Simple ID generation
            vector=embedding,
            payload={
                "text": text_chunk,
                "url": url,
                "timestamp": time.time()
            }
        )

        # Upsert the point to Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[point]
        )
        logger.info("Chunk saved to Qdrant successfully")
    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {e}")


def main():
    """
    Main function to execute the embedding pipeline.
    """
    logger.info("Starting embedding pipeline")

    # Use the deployed URL provided - try the main URL
    deployed_url = "https://hackathon-i-quater-4.vercel.app/"

    # Step 1: Get all URLs from the deployed website
    urls = get_all_urls(deployed_url)

    # Step 2: Process each URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from URL
        text = extract_text_from_url(url)
        if not text:
            continue  # Skip if no text was extracted

        # Chunk the text
        chunks = chunk_text(text)

        # Process each chunk
        for j, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {j+1}/{len(chunks)} for URL: {url}")

            # Generate embedding for the chunk
            embeddings = embed([chunk])
            if not embeddings or len(embeddings) == 0:
                continue  # Skip if no embeddings were generated

            embedding = embeddings[0]  # Get the first (and only) embedding

            # Save to Qdrant
            save_chunk_to_qdrant(chunk, embedding, url)

    logger.info("Embedding pipeline completed")


if __name__ == "__main__":
    main()