"""Add HR CSV data to existing vector store - Simplified version"""

import json
import uuid
import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load HR data
hr_csv_path = os.path.join(script_dir, "..", "data", "hr_data.csv")
print(f"📂 Loading HR data from: {hr_csv_path}")

df = pd.read_csv(hr_csv_path)
print(f"✓ Loaded {len(df)} employee records")

# Create HR chunks in the same format as chunked_markdown.json
hr_chunks = []

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
Salary: ₹{row['salary']:,.2f}
Leave Balance: {row['leave_balance']} days
Leaves Taken: {row['leaves_taken']} days
Attendance: {row['attendance_pct']}%
Performance Rating: {row['performance_rating']}/5
Last Review Date: {row['last_review_date']}

This employee {row['full_name']} works as a {row['role']} in the {row['department']} department, located in {row['location']}. They joined the company on {row['date_of_joining']} and report to manager {row['manager_id']}. Their current performance rating is {row['performance_rating']} out of 5."""

    # Create chunk
    chunk_id = f"hr_{uuid.uuid4().hex[:8]}"
    
    hr_chunks.append({
        "chunk_id": chunk_id,
        "text": employee_text,
        "metadata": {
            "source_document": "hr_data.csv",
            "section_title": f"Employee: {row['full_name']} ({row['employee_id']})",
            "department": "hr",
            "allowed_roles": ["hr", "admin"],
            "token_length": len(employee_text),
            "employee_id": row['employee_id'],
            "employee_name": row['full_name'],
            "employee_role": row['role'],
            "employee_dept": row['department']
        }
    })
    
    if (idx + 1) % 20 == 0:
        print(f"  ⏳ Processed {idx + 1}/{len(df)} employees...")

# Save as chunked HR data
hr_chunks_file = os.path.join(script_dir, "chunked_hr.json")
with open(hr_chunks_file, "w", encoding="utf-8") as f:
    json.dump(hr_chunks, f, indent=2, ensure_ascii=False)

print(f"\n✅ Created {len(hr_chunks)} HR chunks")
print(f"📁 Saved to: {hr_chunks_file}")
print(f"\n📝 Next step: Run generate_embeddings_hr.py to create embeddings and index them")
