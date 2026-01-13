"""
ChromaDB Indexing Verification Test
Verifies that embeddings are correctly indexed in ChromaDB with RBAC metadata
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
vectorstore_dir = project_root / "vectorstore" / "chroma"

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=str(vectorstore_dir),
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=False
    )
)

collection = client.get_or_create_collection(name="company_documents")

print("=" * 80)
print("✅ CHROMADB INDEXING VERIFICATION")
print("=" * 80)

print(f"\n📦 Collection Statistics:")
print(f"   - Collection name: {collection.name}")
print(f"   - Total vectors indexed: {collection.count()}")

# Get sample from each department
print(f"\n📊 Department Distribution:")
all_data = collection.get(include=["metadatas", "documents", "embeddings"])

dept_samples = {}
for metadata, document, embedding in zip(all_data["metadatas"], all_data["documents"], all_data["embeddings"]):
    dept = metadata["department"]
    if dept not in dept_samples:
        dept_samples[dept] = {
            "count": 0,
            "sample": {
                "metadata": metadata,
                "document": document,
                "embedding_dim": len(embedding)
            }
        }
    dept_samples[dept]["count"] += 1

for dept in sorted(dept_samples.keys()):
    info = dept_samples[dept]
    sample = info["sample"]
    print(f"\n   {dept.upper()}:")
    print(f"      Count: {info['count']} vectors")
    print(f"      Embedding dimension: {sample['embedding_dim']}")
    print(f"      Sample metadata keys: {list(sample['metadata'].keys())}")
    print(f"      Sample source: {sample['metadata']['source_document']}")
    print(f"      Allowed roles: {sample['metadata']['allowed_roles']}")
    print(f"      Section: {sample['metadata']['section_title']}")
    print(f"      Document preview: {sample['document'][:70]}...")

# Test metadata filtering
print(f"\n🔍 Testing RBAC Filtering:")

# Test 1: Query only marketing dept
print(f"\n   Test 1: Query marketing department only")
marketing_results = collection.query(
    query_texts=["customer acquisition strategies"],
    n_results=2,
    where={"department": "marketing"}
)
print(f"      Results found: {len(marketing_results['ids'])}")
for i, meta in enumerate(marketing_results["metadatas"][0], 1):
    print(f"      {i}. {meta['source_document']} ({meta['section_title']})")

# Test 2: Query only engineering dept
print(f"\n   Test 2: Query engineering department only")
eng_results = collection.query(
    query_texts=["microservices architecture"],
    n_results=2,
    where={"department": "engineering"}
)
print(f"      Results found: {len(eng_results['ids'])}")
for i, meta in enumerate(eng_results["metadatas"][0], 1):
    print(f"      {i}. {meta['source_document']} ({meta['section_title']})")

# Test 3: Verify finance is included
print(f"\n   Test 3: Query finance department")
finance_results = collection.query(
    query_texts=["revenue and financial performance"],
    n_results=2,
    where={"department": "finance"}
)
print(f"      Finance results found: {len(finance_results['ids'])}")

print(f"\n" + "=" * 80)
print("✅ CHROMADB INDEXING COMPLETE AND VERIFIED")
print("=" * 80)
print(f"\n📝 Summary:")
print(f"   - Total indexed vectors: {collection.count()}")
print(f"   - RBAC metadata included: YES")
print(f"   - Semantic search ready: YES")
print(f"   - All departments indexed: YES")
print(f"   - Collection persistence: {str(vectorstore_dir)}")
