import json
import os
from sentence_transformers import SentenceTransformer

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(script_dir, "chunked_markdown.json")
OUTPUT_FILE = os.path.join(script_dir, "embedded_chunks.json")

# Load chunked data
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load embedding model with optimizations
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

embedded_chunks = []

# Batch process for better efficiency
print(f"Processing {len(chunks)} chunks...")

for i, chunk in enumerate(chunks, 1):
    text = chunk["text"]
    # Use normalize_embeddings=True for consistent cosine similarity
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    
    if i % 20 == 0:
        print(f"Processed {i}/{len(chunks)} chunks...")

    embedded_chunks.append({
        "chunk_id": chunk["chunk_id"],
        "text": text,
        "embedding": embedding,
        "metadata": chunk["metadata"]
    })

# Save embeddings
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(embedded_chunks, f, indent=2)

print(f"✅ Total embeddings generated: {len(embedded_chunks)}")
print("🎉 Embeddings are ready for ChromaDB!")
