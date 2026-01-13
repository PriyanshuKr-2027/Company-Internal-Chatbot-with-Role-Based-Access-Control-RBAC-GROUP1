from sentence_transformers import SentenceTransformer
import json
import os

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Model loaded successfully")

# Load chunked markdown
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "chunked_markdown.json")
with open(json_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

sample_texts = [chunk["text"] for chunk in chunks[:3]]

embeddings = model.encode(sample_texts)

print("Number of embeddings:", len(embeddings))
print("Embedding vector size:", len(embeddings[0]))
