print("🔥 CORRECT CHUNK SCRIPT IS RUNNING 🔥")

import json
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter

INPUT_FILE = "processing/cleaned_markdown.json"
OUTPUT_FILE = "processing/chunked_markdown.json"

# Load cleaned markdown JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# LangChain text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len
)

chunks = []

for source_file, sections in data.items():

    # sections must be a list
    if not isinstance(sections, list):
        continue

    for section in sections:
        content = section.get("content", "").strip()
        title = section.get("title", "")

        # Skip empty sections like ROOT
        if not content:
            continue

        split_texts = text_splitter.split_text(content)

        for idx, text in enumerate(split_texts):
            chunks.append({
                "chunk_id": f"{source_file}_{uuid.uuid4().hex[:8]}",
                "source_document": source_file,
                "section_title": title,
                "text": text,
                "char_length": len(text)
            })

# Save chunked output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"✅ Total chunks created: {len(chunks)}")
print("🎉 Chunking complete!")
