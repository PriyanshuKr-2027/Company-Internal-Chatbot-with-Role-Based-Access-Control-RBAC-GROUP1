"""
Finance Vectors Check Test
Verifies that finance vectors are properly indexed in ChromaDB
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
vectorstore_dir = project_root / "vectorstore" / "chroma"

print("=" * 80)
print("🔍 CHECKING CHROMADB FOR FINANCE VECTORS")
print("=" * 80)

try:
    # Connect to ChromaDB
    client = chromadb.PersistentClient(
        path=str(vectorstore_dir),
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=False
        )
    )
    
    collection = client.get_or_create_collection(name="company_documents")
    
    print(f"\n✓ Connected to ChromaDB")
    print(f"  Collection name: {collection.name}")
    print(f"  Total vectors: {collection.count()}")
    
    # Get all data
    all_data = collection.get(include=["metadatas"])
    
    print(f"\n📊 Department Distribution in ChromaDB:")
    
    dept_breakdown = {}
    for metadata in all_data["metadatas"]:
        dept = metadata.get("department", "unknown")
        dept_breakdown[dept] = dept_breakdown.get(dept, 0) + 1
    
    for dept in sorted(dept_breakdown.keys()):
        count = dept_breakdown[dept]
        pct = (count / len(all_data["metadatas"])) * 100
        print(f"   {dept:<15}: {count:3d} vectors ({pct:5.1f}%)")
    
    # Check specifically for finance
    finance_count = dept_breakdown.get("finance", 0)
    
    print(f"\n" + "=" * 80)
    if finance_count > 0:
        print(f"✅ YES! Finance vectors ARE in ChromaDB: {finance_count} vectors")
        print(f"\n📝 Complete Collection Status:")
        print(f"   - Finance vectors: {finance_count}")
        print(f"   - Engineering vectors: {dept_breakdown.get('engineering', 0)}")
        print(f"   - Marketing vectors: {dept_breakdown.get('marketing', 0)}")
        print(f"   - General vectors: {dept_breakdown.get('general', 0)}")
        print(f"   - Total in ChromaDB: {collection.count()} vectors")
        
        # Show sample finance metadata
        finance_samples = [m for m in all_data["metadatas"] if m.get("department") == "finance"]
        if finance_samples:
            print(f"\n📋 Sample Finance Vector Metadata:")
            sample = finance_samples[0]
            print(f"   Source: {sample.get('source_document')}")
            print(f"   Section: {sample.get('section_title')}")
            print(f"   Allowed Roles: {sample.get('allowed_roles')}")
            print(f"   Token Length: {sample.get('token_length')}")
            
    else:
        print(f"❌ NO Finance vectors found in ChromaDB")
        print(f"   Current total: {collection.count()} vectors")
    
    print(f"\n" + "=" * 80)
    
except Exception as e:
    print(f"\n❌ Error connecting to ChromaDB: {e}")
    print(f"   Vectorstore directory: {str(vectorstore_dir)}")
    print(f"   Directory exists: {vectorstore_dir.exists()}")
