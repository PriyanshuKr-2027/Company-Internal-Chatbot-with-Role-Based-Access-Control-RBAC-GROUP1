"""Generate embeddings for HR data and add to existing vector store"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure sentence-transformers and chromadb are installed")
    sys.exit(1)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load HR chunks
hr_chunks_file = os.path.join(script_dir, "chunked_hr.json")
print(f"📂 Loading HR chunks from: {hr_chunks_file}")

with open(hr_chunks_file, "r", encoding="utf-8") as f:
    hr_chunks = json.load(f)

print(f"✓ Loaded {len(hr_chunks)} HR chunks")

# Load embedding model
print("\n🔄 Loading embedding model...")
try:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("\nTrying alternative approach...")
    # If model loading fails, we'll use the backend API instead
    sys.exit(1)

# Generate embeddings for HR chunks
print(f"\n🔄 Generating embeddings for {len(hr_chunks)} HR chunks...")

embedded_hr_chunks = []
for i, chunk in enumerate(hr_chunks, 1):
    text = chunk["text"]
    embedding = model.encode(text, normalize_embeddings=True).tolist()
    
    if i % 20 == 0:
        print(f"  ⏳ Generated {i}/{len(hr_chunks)} embeddings...")
    
    embedded_hr_chunks.append({
        "chunk_id": chunk["chunk_id"],
        "text": text,
        "embedding": embedding,
        "metadata": chunk["metadata"]
    })

print(f"✓ Generated {len(embedded_hr_chunks)} embeddings")

# Initialize ChromaDB
persist_dir = os.path.join(script_dir, "..", "vectorstore", "chroma")
print(f"\n🔄 Connecting to ChromaDB at: {persist_dir}")

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

print(f"✓ Current collection size: {collection.count()} vectors")

# Prepare data for insertion
documents = []
metadatas = []
ids = []
embeddings = []

for chunk in embedded_hr_chunks:
    documents.append(chunk["text"])
    ids.append(chunk["chunk_id"])
    embeddings.append(chunk["embedding"])
    
    # Create metadata with role flags
    meta = chunk["metadata"]
    metadatas.append({
        "chunk_id": chunk["chunk_id"],
        "source_document": meta["source_document"],
        "department": meta["department"],
        "section_title": meta["section_title"],
        "allowed_roles": ",".join(meta["allowed_roles"]),
        "token_length": str(meta["token_length"]),
        "role_finance": False,
        "role_engineering": False,
        "role_marketing": False,
        "role_hr": True,
        "role_general": False,
        "role_admin": True
    })

# Add to ChromaDB
print(f"\n🔄 Adding {len(documents)} HR vectors to ChromaDB...")
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"\n✅ HR data indexed successfully!")
print(f"📦 Total vectors in collection: {collection.count()}")

# Test the HR data
print(f"\n🧪 Testing HR search...")
test_results = collection.query(
    query_texts=["Krishna Malhotra employee information"],
    n_results=3,
    where={"role_hr": True}
)

if test_results["documents"][0]:
    print(f"✓ Found {len(test_results['documents'][0])} results for test query")
    for i, meta in enumerate(test_results['metadatas'][0], 1):
        print(f"  {i}. {meta['section_title']}")
else:
    print("⚠ No results found for test query")

# Show department breakdown
print(f"\n📊 Verifying department distribution:")
all_data = collection.get()
dept_counts = {}
for meta in all_data['metadatas']:
    dept = meta.get('department', 'unknown')
    dept_counts[dept] = dept_counts.get(dept, 0) + 1

for dept in sorted(dept_counts.keys()):
    print(f"   - {dept}: {dept_counts[dept]} vectors")

print(f"\n✅ HR data processing complete!")
print(f"🔄 Please restart the backend server for changes to take effect.")
