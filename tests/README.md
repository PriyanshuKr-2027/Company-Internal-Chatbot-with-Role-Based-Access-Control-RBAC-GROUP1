# Tests Directory

This directory contains all test and verification scripts for the Company Internal Chatbot with RBAC system.

## Test Files

### Core Test Files

#### `test_rbac.py`
Tests Role-Based Access Control (RBAC) functionality to ensure role-based document filtering works correctly.

#### `test_embeddings.py`
Verifies that embeddings are generated correctly using the sentence-transformers model.
- Tests model loading
- Validates embedding dimensions (should be 384)
- Checks sample text processing

### Verification Files

#### `verify_rbac.py`
Comprehensive RBAC verification that checks:
- Department mapping for all chunks
- Role assignments per department
- Sample verification from each department
- Document-to-department assignment validation

#### `verify_embeddings.py`
Verifies the generated embeddings:
- Total embeddings count
- Embedding dimensions
- Department breakdown
- Metadata completeness

#### `verify_chromadb.py`
Validates ChromaDB collection indexing:
- Collection statistics
- Vector count per department
- Metadata fields verification
- RBAC filtering tests (marketing, engineering, finance)
- Sample query testing

#### `quick_verify.py`
Quick verification script for ChromaDB status:
- Checks persistence directory
- Verifies embedded chunks file
- Shows metadata sample
- Displays department breakdown

#### `check_finance.py`
Specific verification for finance vectors:
- Checks if finance vectors exist in ChromaDB
- Shows finance department statistics
- Displays sample finance metadata

### Utility Scripts

#### `add_finance_vectors.py`
One-time utility to add finance vectors to ChromaDB:
- Generates embeddings for finance chunks
- Adds them to the existing collection
- Shows final department distribution

## Running Tests

### From processing directory:
```bash
# From tests directory
python test_embeddings.py
python verify_rbac.py
python verify_embeddings.py
python verify_chromadb.py
python check_finance.py
python quick_verify.py
```

### Environment Setup:
- Tests assume Python environment is configured in parent directory
- Tests use relative paths to access data in processing and vectorstore folders
- All tests require sentence-transformers and chromadb packages

## Test Coverage

| Component | Test Coverage |
|-----------|---|
| RBAC Mapping | ✅ verify_rbac.py |
| Embeddings Generation | ✅ test_embeddings.py, verify_embeddings.py |
| ChromaDB Indexing | ✅ verify_chromadb.py, quick_verify.py |
| Finance Data | ✅ check_finance.py, add_finance_vectors.py |
| Data Pipeline | ✅ test_rbac.py |

## Notes

- All test files use relative paths based on `Path(__file__).parent`
- Tests are designed to be run independently
- No test modifications to actual data
- All tests are read-only verification scripts
