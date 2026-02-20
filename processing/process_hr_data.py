"""Process HR CSV data and add to vector store"""

import json
import uuid
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load HR data
hr_csv_path = os.path.join(script_dir, "..", "data", "hr_data.csv")
print(f"📂 Loading HR data from: {hr_csv_path}")

df = pd.read_csv(hr_csv_path)
print(f"✓ Loaded {len(df)} employee records")

# Initialize embedding model
print("\n🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✓ Model loaded")

# Initialize ChromaDB
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

print(f"\n📊 Current collection size: {collection.count()} vectors")

# Process each employee record
documents = []
metadatas = []
ids = []
embeddings = []

print(f"\n🔄 Processing {len(df)} employee records...")

for idx, row in df.iterrows():
    # Create a comprehensive text representation of each employee
    employee_text = f"""Employee Information:
Full Name: {row['full_name']}
Employee ID: {row['employee_id']}
Role: {row['role']}
Department: {row['department']}
Email: {row['email']}
Location: {row['location']}
Date of Birth: {row['date_of_birth']}
Date of Joining: {row['date_of_joining']}
Manager ID: {row['manager_id']}
Salary: {row['salary']}
Leave Balance: {row['leave_balance']} days
Leaves Taken: {row['leaves_taken']} days
Attendance: {row['attendance_pct']}%
Performance Rating: {row['performance_rating']}/5
Last Review Date: {row['last_review_date']}"""

    # Generate embedding
    embedding = model.encode(employee_text, normalize_embeddings=True).tolist()
    
    # Create metadata
    chunk_id = f"hr_{uuid.uuid4().hex[:8]}"
    
    metadata = {
        "chunk_id": chunk_id,
        "source_document": "hr_data.csv",
        "department": "hr",
        "section_title": f"Employee: {row['full_name']}",
        "allowed_roles": "hr,admin",
        "token_length": str(len(employee_text)),
        "role_finance": False,
        "role_engineering": False,
        "role_marketing": False,
        "role_hr": True,
        "role_general": False,
        "role_admin": True,
        "employee_id": row['employee_id'],
        "employee_name": row['full_name'],
        "employee_role": row['role'],
        "employee_dept": row['department']
    }
    
    documents.append(employee_text)
    metadatas.append(metadata)
    ids.append(chunk_id)
    embeddings.append(embedding)
    
    if (idx + 1) % 20 == 0:
        print(f"  ⏳ Processed {idx + 1}/{len(df)} employees...")

# Add to ChromaDB
print(f"\n🔄 Adding {len(documents)} HR records to vector store...")
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
    print(f"  First result: {test_results['metadatas'][0][0]['section_title']}")
else:
    print("⚠ No results found for test query")

print(f"\n✅ HR data processing complete!")
