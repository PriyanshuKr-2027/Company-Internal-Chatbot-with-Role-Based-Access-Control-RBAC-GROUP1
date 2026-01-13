import json
import uuid
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(script_dir, "cleaned_markdown.json")
OUTPUT_FILE = os.path.join(script_dir, "chunked_markdown.json")

# Department → allowed roles mapping
DEPARTMENT_ROLE_MAP = {
    "engineering": ["engineering", "admin"],
    "finance": ["finance", "admin"],
    "hr": ["hr", "admin"],
    "marketing": ["marketing", "admin"],
    "general": ["employee", "admin"]
}

# Explicit document → department mapping (PRODUCTION SAFE)
DOCUMENT_DEPARTMENT_MAP = {
    "financial_summary.md": "finance",
    "quarterly_financial_report.md": "finance",
    "engineering_master.md": "engineering",
    "engineering_master_doc.md": "engineering",
    "marketing_strategy.md": "marketing",
    "employee_handbook.md": "general",
    "market_report_q4_2024.md": "marketing",
    "marketing_report_2024.md": "marketing",
    "marketing_report_q1_2024.md": "marketing",
    "marketing_report_q2_2024.md": "marketing",
    "marketing_report_q3_2024.md": "marketing"
}

# Load cleaned markdown JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len
)

chunks = []

for source_file, sections in data.items():

    # Safety check
    if not isinstance(sections, list):
        continue

    # Resolve department explicitly (default → general)
    department = DOCUMENT_DEPARTMENT_MAP.get(source_file, "general")
    allowed_roles = DEPARTMENT_ROLE_MAP[department]

    for section in sections:
        content = section.get("content", "").strip()
        title = section.get("title", "")

        # Skip empty sections (ROOT etc.)
        if not content:
            continue

        split_texts = text_splitter.split_text(content)

        for text in split_texts:
            token_len = len(text)

            # Enforce chunk quality (300–512 chars)
            if token_len < 300:
                continue

            chunks.append({
                "chunk_id": f"{department}_{uuid.uuid4().hex[:8]}",
                "text": text,
                "metadata": {
                    "source_document": source_file,
                    "section_title": title,
                    "department": department,
                    "allowed_roles": allowed_roles,
                    "token_length": token_len
                }
            })

# Save chunked output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"✅ Total chunks created: {len(chunks)}")
print("🎉 Chunking + Metadata attachment complete!")
