"""
Test script for embeddings verification
Verifies that embeddings are generated correctly using sentence-transformers
"""
from sentence_transformers import SentenceTransformer
import json
import os
from pathlib import Path

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
processing_dir = project_root / "processing"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("✓ Model loaded successfully")

# Load chunked markdown
json_path = processing_dir / "chunked_markdown.json"
with open(json_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

sample_texts = [chunk["text"] for chunk in chunks[:3]]

embeddings = model.encode(sample_texts)

print(f"✅ Embedding Test Results:")
print(f"   Number of embeddings: {len(embeddings)}")
print(f"   Embedding vector size: {len(embeddings[0])}")
print(f"   Sample text length: {len(sample_texts[0])} characters")
