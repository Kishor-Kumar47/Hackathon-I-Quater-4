"""
Unit tests for main.py functions
"""
import pytest
from backend.main import validate_url, chunk_text


def test_validate_url_valid():
    """Test URL validation with a valid URL"""
    assert validate_url("https://example.com") == True
    assert validate_url("http://localhost:3000") == True
    assert validate_url("https://docs.example.com/guide") == True


def test_validate_url_invalid():
    """Test URL validation with invalid URLs"""
    assert validate_url("") == False
    assert validate_url("not-a-url") == False
    assert validate_url("ftp://example.com") == True  # Actually valid URL with scheme
    assert validate_url("just-a-string") == False
    assert validate_url("http://") == False


def test_chunk_text():
    """Test text chunking functionality"""
    long_text = "This is a sample text. " * 100  # Create a long text
    chunks = chunk_text(long_text, chunk_size=50)

    # Should have multiple chunks
    assert len(chunks) > 1

    # Each chunk should have text
    for chunk in chunks:
        assert 'text' in chunk
        assert 'start_pos' in chunk
        assert 'end_pos' in chunk
        assert len(chunk['text']) <= 50  # Chunk size limit


def test_chunk_text_empty():
    """Test chunking with empty text"""
    chunks = chunk_text("")
    assert chunks == []


def test_chunk_text_short():
    """Test chunking with text shorter than chunk size"""
    short_text = "Short text"
    chunks = chunk_text(short_text, chunk_size=50)
    assert len(chunks) == 1
    assert chunks[0]['text'] == short_text