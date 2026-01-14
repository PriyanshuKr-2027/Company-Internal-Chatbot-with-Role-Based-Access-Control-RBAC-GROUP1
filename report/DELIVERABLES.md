# RAG/RBAC Deliverables Snapshot

_Date: 2026-01-14_

## Highlights
| Area | Detail |
|------|--------|
| Pipeline | clean → chunk → embed → index (persistent Chroma) |
| Embeddings | all-MiniLM-L6-v2 · 384 dims · **135** vectors total |
| RBAC | `role_*` flags per chunk; enforced via Chroma `where` filters |
| Normalization | strip + lowercase + collapse whitespace before encoding |
| Interfaces | Terminal demo + Streamlit demo (`demo preview/`) |

## Data Coverage (Chunks)
| Department | Count |
|------------|-------|
| Engineering | 39 |
| Marketing | 49 |
| Finance | 36 |
| General | 11 |

## RBAC Implementation
- Hierarchy: **admin > finance/engineering/hr/marketing > employee**
- Metadata: `allowed_roles` plus boolean `role_*` flags stored on each chunk
- Enforcement: query-time filtering (`role_<dept>=True`) with validation tests blocking cross-department access

## Validation & QA
- RBAC checks: `tests/verify_rbac.py`
- Chroma metadata checks: `tests/verify_chromadb.py`
- Embedding dimensions/counts: `tests/verify_embeddings.py`

## Deliverables Status
| Deliverable | Status | Location |
|-------------|--------|----------|
| Embedding generation module | ✅ Completed | processing/generate_embeddings.py |
| Populated vector DB with indexed docs | ✅ Completed | vectorstore/chroma |
| Semantic search + query interface | ✅ Completed | query/query_engine.py; demo preview/demo_* |
| Search quality/performance benchmarking report | ✅ Completed | report/benchmark_search.py; report/BENCHMARK.md |
| RBAC filtering module | ✅ Completed | rbac/rbac_filter.py |
| Query processing + normalization | ✅ Completed | query/query_engine.py |
| Role hierarchy definition | ✅ Completed | rbac/rbac_filter.py |
| RBAC validation tests | ✅ Completed | tests/verify_rbac.py; tests/verify_chromadb.py |

## What’s Next
- Optional: expand benchmark set and add relevance ground-truth checks.

---