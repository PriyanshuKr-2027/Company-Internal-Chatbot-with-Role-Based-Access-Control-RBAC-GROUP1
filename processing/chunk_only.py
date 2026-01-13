print("🔥 CORRECT CHUNK SCRIPT IS RUNNING 🔥")

import json
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_FILE = "processing/cleaned_markdown.json"
OUTPUT_FILE = "processing/chunked_markdown.json"

# Department → allowed roles mapping
DEPARTMENT_ROLE_MAP = {
    "engineering": ["engineering", "admin"],
    "finance": ["finance", "admin"],
    "hr": ["hr", "admin"],
    "marketing": ["marketing", "admin"],
    "general": ["employee", "admin"]
}

# Explicit document → department mapping (IMPORTANT)
DOCUMENT_DEPARTMENT_MAP = {
    "financial_summary.md": "finance",
    "quarterly_financial_report.md": "finance"
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

    if not isinstance(sections, list):
        continue

    department = DOCUMENT_DEPARTMENT_MAP.get(source_file, "general")
    allowed_roles = DEPARTMENT_ROLE_MAP[department]

    for section in sections:
        content = section.get("content", "").strip()
        title = section.get("title", "")

        # Skip empty sections
        if not content:
            continue

        split_texts = text_splitter.split_text(content)

        for text in split_texts:
            token_len = len(text)

            # Enforce 300–512 token rule
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
