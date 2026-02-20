"""
Add Finance Vectors Test/Utility
Generates and adds finance vectors to ChromaDB
Note: This is typically run once to add finance vectors to the collection
"""
import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
processing_dir = project_root / "processing"
vectorstore_dir = project_root / "vectorstore" / "chroma"

# Load the chunked data
with open(processing_dir / "chunked_markdown.json", "r") as f:
    all_chunks = json.load(f)

# Filter only finance chunks
finance_chunks = [c for c in all_chunks if c["metadata"]["department"] == "finance"]

print("=" * 80)
print("📊 ADDING FINANCE VECTORS TO CHROMADB")
print("=" * 80)

print(f"\n✓ Found {len(finance_chunks)} finance chunks to index")

# Generate embeddings for finance
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print(f"\n⏳ Generating embeddings for finance chunks...")

documents = []
metadatas = []
ids = []
embeddings = []

for chunk in finance_chunks:
    documents.append(chunk["text"])
    ids.append(chunk["chunk_id"])
    
    # Create comprehensive metadata (same as other departments)
    meta = chunk["metadata"]
    metadatas.append({
        "chunk_id": chunk["chunk_id"],
        "source_document": meta["source_document"],
        "department": meta["department"],
        "section_title": meta["section_title"],
        "allowed_roles": ",".join(meta["allowed_roles"]),
        "token_length": str(meta["token_length"]),
        "role_engineering": "engineering" in meta["allowed_roles"],
        "role_marketing": "marketing" in meta["allowed_roles"],
        "role_general": "general" in meta["allowed_roles"] or "employee" in meta["allowed_roles"],
        "role_finance": "finance" in meta["allowed_roles"],
        "role_admin": "admin" in meta["allowed_roles"]
    })
    
    # Generate embedding
    embedding = model.encode(chunk["text"]).tolist()
    embeddings.append(embedding)
    
    if len(embeddings) % 5 == 0:
        print(f"   ⏳ Processed {len(embeddings)}/{len(finance_chunks)} finance chunks...")

print(f"✅ Generated {len(embeddings)} embeddings")

# Connect to ChromaDB and add finance vectors
print(f"\n🔄 Adding to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(vectorstore_dir),
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=False
    )
)

collection = client.get_or_create_collection(name="company_documents")

# Add finance vectors
collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"✅ Finance vectors added to ChromaDB!")
print(f"\n📦 Collection Statistics:")
print(f"   Total vectors now: {collection.count()}")

# Get breakdown
all_data = collection.get(include=["metadatas"])
dept_breakdown = {}
for metadata in all_data["metadatas"]:
    dept = metadata.get("department", "unknown")
    dept_breakdown[dept] = dept_breakdown.get(dept, 0) + 1

print(f"\n📊 Department Distribution in ChromaDB:")
for dept in sorted(dept_breakdown.keys()):
    count = dept_breakdown[dept]
    pct = (count / collection.count()) * 100
    print(f"   {dept:<15}: {count:3d} vectors ({pct:5.1f}%)")

print(f"\n" + "=" * 80)
print(f"✅ FINANCE VECTORS SUCCESSFULLY ADDED TO CHROMADB")
print("=" * 80)
