import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunked data
with open(os.path.join(script_dir, "embedded_chunks.json"), "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Initialize ChromaDB with persistence
persist_dir = os.path.join(script_dir, "..", "vectorstore", "chroma")
os.makedirs(persist_dir, exist_ok=True)

client = chromadb.PersistentClient(
    path=persist_dir,
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=False
    )
)

collection = client.get_or_create_collection(
    name="company_documents",
    metadata={"hnsw:space": "cosine"}
)

# Prepare data for insertion (excluding finance)
documents = []
metadatas = []
ids = []
embeddings = []
skipped_count = 0
indexed_count = 0

for chunk in chunks:
    # Index all departments including finance
    documents.append(chunk["text"])
    ids.append(chunk["chunk_id"])
    
    # Create comprehensive metadata
    meta = chunk["metadata"]
    metadatas.append({
        "chunk_id": chunk["chunk_id"],
        "source_document": meta["source_document"],
        "department": meta["department"],
        "section_title": meta["section_title"],
        "allowed_roles": ",".join(meta["allowed_roles"]),
        "token_length": str(meta["token_length"]),
        "role_finance": "finance" in meta["allowed_roles"],
        "role_engineering": "engineering" in meta["allowed_roles"],
        "role_marketing": "marketing" in meta["allowed_roles"],
        "role_hr": "hr" in meta["allowed_roles"],
        "role_general": "general" in meta["allowed_roles"] or "employee" in meta["allowed_roles"],
        "role_admin": "admin" in meta["allowed_roles"]
    })
    
    # Use pre-computed embeddings from embedded_chunks.json
    embeddings.append(chunk["embedding"])
    indexed_count += 1
    
    # Progress indicator
    if indexed_count % 10 == 0:
        print(f"  ⏳ Indexed {indexed_count} vectors...")

# Insert into ChromaDB
print(f"\n🔄 Indexing {indexed_count} vectors into ChromaDB...")
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"\n✅ Embeddings indexed successfully!")
print(f"📦 Total vectors in collection: {collection.count()}")

# Show statistics
dept_stats = {}
for meta in metadatas:
    dept = meta["department"]
    dept_stats[dept] = dept_stats.get(dept, 0) + 1

print(f"\n📊 Department breakdown in ChromaDB:")
for dept in sorted(dept_stats.keys()):
    print(f"   - {dept}: {dept_stats[dept]} vectors")

# Test the collection with a sample query
print(f"\n🧪 Testing semantic search...")
test_results = collection.query(
    query_texts=["marketing campaigns and customer acquisition"],
    n_results=3,
    where={"department": "marketing"}
)

print(f"   Sample query results (from marketing dept):")
for i, (doc, meta) in enumerate(zip(test_results["documents"][0], test_results["metadatas"][0]), 1):
    print(f"   {i}. {meta['section_title']} - {doc[:60]}...")

print(f"\n✅ ChromaDB indexing complete and verified!")

