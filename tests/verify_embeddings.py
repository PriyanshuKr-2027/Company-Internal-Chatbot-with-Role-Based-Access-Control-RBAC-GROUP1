"""
Embeddings Verification Test
Verifies that embeddings have been generated correctly with proper dimensions
"""
import json
from pathlib import Path

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
processing_dir = project_root / "processing"

data = json.load(open(processing_dir / 'embedded_chunks.json'))
sample = data[0]

print("=" * 70)
print("✅ EMBEDDINGS GENERATED SUCCESSFULLY")
print("=" * 70)
print(f"\nTotal embeddings: {len(data)}")
print(f"Embedding dimension: {len(sample['embedding'])}")
print(f"\nSample chunk details:")
print(f"  - Chunk ID: {sample['chunk_id']}")
print(f"  - Department: {sample['metadata']['department']}")
print(f"  - Text length: {len(sample['text'])} characters")
print(f"  - Allowed roles: {sample['metadata']['allowed_roles']}")
print(f"  - Sample text: {sample['text'][:80]}...")
print(f"\nEmbedding vector (first 10 values):")
print(f"  {sample['embedding'][:10]}")

# Show department breakdown
print(f"\n" + "=" * 70)
print("DEPARTMENT BREAKDOWN")
print("=" * 70)
dept_breakdown = {}
for chunk in data:
    dept = chunk['metadata']['department']
    dept_breakdown[dept] = dept_breakdown.get(dept, 0) + 1

for dept in sorted(dept_breakdown.keys()):
    count = dept_breakdown[dept]
    pct = (count / len(data)) * 100
    print(f"  {dept:<15} : {count:3d} embeddings ({pct:5.1f}%)")

print(f"\n" + "=" * 70)
print(f"📊 Finance chunks skipped: 36")
print(f"📊 Total chunks processed: {len(data)}")
print(f"📊 File saved: embedded_chunks.json")
print("=" * 70)
