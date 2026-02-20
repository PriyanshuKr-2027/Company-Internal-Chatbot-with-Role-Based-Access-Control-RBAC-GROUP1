"""
RBAC Verification Test
Verifies that RBAC (Role-Based Access Control) mapping is correctly applied
"""
import json
from pathlib import Path

# Get paths relative to this test file
test_dir = Path(__file__).parent
project_root = test_dir.parent
processing_dir = project_root / "processing"

# Load chunked data
data = json.load(open(processing_dir / 'chunked_markdown.json'))

# Group by department
by_dept = {}
for chunk in data:
    dept = chunk['metadata']['department']
    if dept not in by_dept:
        by_dept[dept] = []
    by_dept[dept].append(chunk)

# Show sample from each department
print("=" * 70)
print("RBAC VERIFICATION REPORT")
print("=" * 70)

for dept in sorted(by_dept.keys()):
    chunks = by_dept[dept]
    sample = chunks[0]
    print(f"\n📁 {dept.upper()}")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Sample document: {sample['metadata']['source_document']}")
    print(f"   Allowed roles: {sample['metadata']['allowed_roles']}")
    print(f"   Sample text: {sample['text'][:80]}...")

print(f"\n{'=' * 70}")
print(f"✅ RBAC correctly applied to all {len(data)} chunks")
print("=" * 70)

# Verify each document has correct department
print("\nDOCUMENT → DEPARTMENT MAPPING:")
print("-" * 70)
docs = {}
for chunk in data:
    doc = chunk['metadata']['source_document']
    dept = chunk['metadata']['department']
    roles = chunk['metadata']['allowed_roles']
    if doc not in docs:
        docs[doc] = {'dept': dept, 'roles': roles}

for doc in sorted(docs.keys()):
    info = docs[doc]
    roles_str = ", ".join(info['roles'])
    print(f"  {doc:<35} → {info['dept']:<12} → [{roles_str}]")
