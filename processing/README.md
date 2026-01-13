# Processing Directory

This directory contains the data processing pipeline for the Company Internal Chatbot with RBAC system.

## Pipeline Overview

The processing pipeline transforms raw markdown documents into indexed embeddings in ChromaDB with RBAC metadata.

### Pipeline Stages

```
Raw Markdown Files
      ↓
   [run_pipeline.py]
      ↓
cleaned_markdown.json (structured sections)
      ↓
   [chunk_only.py]
      ↓
chunked_markdown.json (semantic chunks + RBAC metadata)
      ↓
   [generate_embeddings.py]
      ↓
embedded_chunks.json (vectors for non-finance documents)
      ↓
   [index_embeddings.py]
      ↓
ChromaDB Vector Database
```

## Core Processing Files

### Data Loading & Cleaning

#### `file_loader.py`
Loads markdown and CSV files from source directories.
- Supports .md and .csv formats
- Handles encoding safely

#### `text_cleaner.py`
Cleans and normalizes text data.
- Removes extra whitespace
- Normalizes formatting
- Handles encoding issues

#### `md_parser.py`
Parses markdown into hierarchical sections.
- Extracts headers and content
- Maintains section hierarchy
- Creates structured output

### Pipeline Scripts

#### `run_pipeline.py`
Main cleaning and parsing pipeline.
- Loads markdown from all department folders
- Cleans text content
- Parses into sections
- Outputs: `cleaned_markdown.json`, `cleaned_hr.csv`

#### `chunk_only.py`
Creates semantic chunks with RBAC metadata.
- Splits content into 300-512 character chunks
- Assigns department-specific roles
- Applies RBAC filtering rules
- Outputs: `chunked_markdown.json`

#### `generate_embeddings.py`
Generates vector embeddings for document chunks.
- Uses: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional)
- Skips finance chunks (pre-generated)
- Outputs: `embedded_chunks.json`

#### `index_embeddings.py`
Indexes embeddings into ChromaDB with comprehensive metadata.
- Connects to ChromaDB
- Creates collection with cosine similarity
- Adds comprehensive RBAC metadata
- Supports semantic search with filtering
- Outputs: ChromaDB persistent collection

## Data Files

### Input
- `../data/finance/*.md` - Finance department documents
- `../data/engineering/*.md` - Engineering department documents
- `../data/marketing/*.md` - Marketing department documents
- `../data/general/*.md` - General/HR department documents
- `../data/hr_data.csv` - HR data

### Intermediate
- `cleaned_markdown.json` - Cleaned and sectioned documents
- `chunked_markdown.json` - Semantic chunks with metadata
- `embedded_chunks.json` - Chunks with embeddings (non-finance)
- `cleaned_hr.csv` - Cleaned HR data

### Output
- `../vectorstore/chroma/` - ChromaDB persistent storage

## RBAC Mapping

```python
DOCUMENT_DEPARTMENT_MAP = {
    "financial_summary.md": "finance",
    "quarterly_financial_report.md": "finance",
    "engineering_master_doc.md": "engineering",
    "marketing_report_*.md": "marketing",
    "employee_handbook.md": "general"
}

DEPARTMENT_ROLE_MAP = {
    "engineering": ["engineering", "admin"],
    "finance": ["finance", "admin"],
    "marketing": ["marketing", "admin"],
    "general": ["employee", "admin"],
    "hr": ["hr", "admin"]
}
```

## Metadata Structure

Each indexed vector contains:
- `chunk_id`: Unique identifier (dept_xxxxx)
- `source_document`: Original file name
- `department`: Department classification
- `section_title`: Markdown section title
- `allowed_roles`: Comma-separated roles
- `token_length`: Character count
- `role_engineering`, `role_marketing`, `role_general`, `role_admin`: Boolean filters

## Running the Pipeline

### Full Pipeline (One-Time)
```bash
# 1. Clean and parse markdown
python run_pipeline.py

# 2. Create semantic chunks with RBAC
python chunk_only.py

# 3. Generate embeddings
python generate_embeddings.py

# 4. Index into ChromaDB
python index_embeddings.py
```

### Add Finance Vectors
```bash
# Run from tests folder
python tests/add_finance_vectors.py
```

## Statistics

- **Total Documents**: 9 markdown files
- **Total Chunks**: 135 (with metadata)
- **Total Embeddings**: 135 (including finance)
- **Embedding Dimension**: 384
- **Department Breakdown**:
  - Engineering: 39 vectors
  - Finance: 36 vectors
  - Marketing: 49 vectors
  - General: 11 vectors

## Key Features

✅ Role-Based Access Control (RBAC)
✅ Semantic document chunking
✅ Comprehensive metadata tracking
✅ Persistent ChromaDB storage
✅ Production-safe department mapping
✅ Multi-format support (markdown, CSV)

## Dependencies

- langchain
- sentence-transformers
- chromadb
- pandas
- python-dotenv

## Configuration

All paths are relative to the processing directory. Adjust `MARKDOWN_FOLDERS` in `run_pipeline.py` if source structure changes.
