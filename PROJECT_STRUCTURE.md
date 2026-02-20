# Project Structure - Company Internal Chatbot with RBAC

```
Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC-GROUP1/
│
├── README.md                          # Main project documentation
├── requirements.txt                   # Python dependencies
│
├── data/                              # SOURCE DOCUMENTS (RAW)
│   ├── hr_data.csv
│   ├── finance/
│   │   ├── financial_summary.md
│   │   └── quarterly_financial_report.md
│   ├── engineering/
│   │   └── engineering_master_doc.md
│   ├── marketing/
│   │   ├── marketing_report_2024.md
│   │   ├── marketing_report_q1_2024.md
│   │   ├── marketing_report_q2_2024.md
│   │   ├── marketing_report_q3_2024.md
│   │   └── market_report_q4_2024.md
│   └── general/
│       └── employee_handbook.md
│
├── processing/                        # DATA PIPELINE (CORE)
│   ├── README.md                      # Pipeline documentation
│   ├── __init__.py
│   ├── run_pipeline.py                # Stage 1: Clean & parse markdown
│   ├── chunk_only.py                  # Stage 2: Create chunks + RBAC
│   ├── generate_embeddings.py         # Stage 3: Generate embeddings
│   ├── index_embeddings.py            # Stage 4: Index to ChromaDB
│   │
│   ├── file_loader.py                 # Load markdown/CSV files
│   ├── text_cleaner.py                # Text normalization
│   ├── md_parser.py                   # Markdown parsing
│   │
│   ├── cleaned_markdown.json          # Intermediate: Cleaned sections
│   ├── chunked_markdown.json          # Intermediate: Chunks + RBAC
│   ├── embedded_chunks.json           # Intermediate: Non-finance embeddings
│   └── cleaned_hr.csv                 # Intermediate: Cleaned HR data
│
├── vectorstore/                       # VECTOR DATABASE (LOCAL)
│   └── chroma/                        # ChromaDB persistent storage
│       └── [indexed embeddings + metadata]
│
├── rbac/                              # ACCESS CONTROL LOGIC
│   ├── __init__.py
│   └── rbac_filter.py                 # Role hierarchy + filtering
│
├── query/                             # QUERY LAYER
│   ├── __init__.py
│   └── query_engine.py                # Semantic search + RBAC
│
├── api/                               # FASTAPI SERVER
│   ├── __init__.py
│   └── main.py                        # API endpoints
│
├── tests/                             # TEST & VERIFICATION SCRIPTS
│   ├── README.md                      # Test documentation
│   ├── __init__.py
│   ├── test_rbac.py                   # RBAC functionality tests
│   ├── test_embeddings.py             # Embedding generation tests
│   ├── verify_rbac.py                 # RBAC mapping verification
│   ├── verify_embeddings.py           # Embeddings verification
│   ├── verify_chromadb.py             # ChromaDB indexing verification
│   ├── check_finance.py               # Finance vectors check
│   ├── quick_verify.py                # Quick status check
│   └── add_finance_vectors.py         # Utility: Add finance vectors
│
├── scripts/                           # UTILITIES
│   └── reset_vector_db.py             # Reset ChromaDB
│
└── vectordatabase/                    # VECTOR DATABASE CLIENT
    └── chroma_client.py               # ChromaDB connection manager
```

## Directory Purposes

### `data/`
Raw source documents organized by department:
- **finance/**: Financial reports and summaries
- **engineering/**: Technical documentation
- **marketing/**: Marketing reports and strategies
- **general/**: Employee handbook and general docs

### `processing/`
Data pipeline for document processing:
- Load → Clean → Parse → Chunk → Embed → Index
- All intermediate files (JSON) stored here
- Supports full data pipeline automation

### `vectorstore/`
Vector database persistence:
- ChromaDB indexes all document embeddings
- Persistent storage for production deployment
- Contains indexed vectors with RBAC metadata

### `rbac/`
Role-Based Access Control module:
- Enforces role hierarchy
- Filters documents by user role
- Validates permissions

### `query/`
Query and search layer:
- Semantic search implementation
- RBAC filtering on queries
- Response ranking

### `api/`
FastAPI server:
- REST endpoints for chatbot
- Authentication and authorization
- Request/response handling

### `tests/`
Test and verification scripts:
- Unit tests for components
- Verification scripts for data integrity
- RBAC and embedding validation

### `scripts/`
Utility scripts:
- Database management
- Data migrations
- Maintenance tasks

### `vectordatabase/`
Vector database client:
- ChromaDB connection manager
- Vector operations abstraction
- Collection management

## Data Flow

```
Raw Documents
    ↓
run_pipeline.py (clean + parse)
    ↓
cleaned_markdown.json
    ↓
chunk_only.py (semantic chunks + RBAC)
    ↓
chunked_markdown.json
    ↓
generate_embeddings.py (create vectors)
    ↓
embedded_chunks.json
    ↓
index_embeddings.py (index to ChromaDB)
    ↓
ChromaDB (persistent vector store)
    ↓
query_engine.py (semantic search + RBAC)
    ↓
FastAPI Server
    ↓
Client Response
```

## Statistics

- **Total Documents**: 9 markdown files
- **Total Chunks**: 135 semantic chunks
- **Total Embeddings**: 135 (384-dimensional)
- **Departments**: 5 (Engineering, Finance, Marketing, General, HR)
- **Test Files**: 8 verification scripts
- **Pipeline Stages**: 4 automated stages

## Key Features

✅ **RBAC Implementation**: Role-based document filtering
✅ **Semantic Search**: Using sentence-transformers embeddings
✅ **ChromaDB Integration**: Persistent vector database
✅ **Data Pipeline**: Automated document processing
✅ **Comprehensive Testing**: Multiple verification scripts
✅ **Clean Architecture**: Separated concerns by module

## Clean Code Practices

✅ All test/verification files moved to `tests/` folder
✅ Pipeline scripts organized in `processing/` folder
✅ Core logic separated into domain modules (rbac, query, api)
✅ README.md files in each major folder
✅ Consistent naming conventions
✅ No test clutter in production folders
