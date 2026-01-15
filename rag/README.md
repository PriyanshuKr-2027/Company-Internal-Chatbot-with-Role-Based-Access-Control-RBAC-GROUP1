# RAG Pipeline - Module 6 Implementation

## Overview

Complete Retrieval-Augmented Generation (RAG) pipeline with Role-Based Access Control (RBAC), LLM integration, and source attribution.

## Components

### 1. RAG Pipeline (`rag_pipeline.py`)
**Complete RAG workflow implementation**

Flow:
```
User Query → Role Authentication → RBAC Filtering → Semantic Search → 
Context Augmentation → LLM Generation → Source Attribution → Response
```

Key Features:
- ✅ User authentication and role validation
- ✅ RBAC-filtered document retrieval
- ✅ Context augmentation with top-k documents
- ✅ LLM response generation
- ✅ Source citation and attribution
- ✅ Confidence scoring

### 2. Prompt Templates (`prompt_templates.py`)
**Centralized prompt engineering and context formatting**

Features:
- System prompts for RAG responses
- Context formatting from search results
- Query type detection (factual, comparison, summary)
- Template selection based on query type
- Citation formatting

Query Types Supported:
- **Factual**: Direct answers with specific details
- **Comparison**: Side-by-side analysis
- **Summary**: Comprehensive overviews
- **General**: Standard RAG responses

### 3. Confidence Scorer (`confidence_scorer.py`)
**Confidence scoring based on retrieval relevance**

Metrics:
- **Relevance Score**: Based on vector similarity (0-1)
- **Confidence Level**: HIGH / MEDIUM / LOW / VERY LOW
- **Source Quality**: Per-document relevance classification
- **Confidence Thresholds**:
  - HIGH: ≥ 0.7
  - MEDIUM: ≥ 0.5
  - LOW: ≥ 0.3
  - VERY LOW: < 0.3

Features:
- Automatic confidence disclaimers for low-confidence answers
- Individual source scoring
- Result count adjustment

## Usage

### Basic Usage

```python
from rag.rag_pipeline import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline()

# Simple query
answer = pipeline.query_simple(
    user_query="What were the Q4 2024 results?",
    user_role="finance"
)
print(answer)

# Query with sources
response = pipeline.query_with_sources(
    user_query="What were the Q4 2024 results?",
    user_role="finance"
)
print(response)
```

### Advanced Usage

```python
# Full result with metadata
result = pipeline.query(
    user_query="What were the Q4 2024 results?",
    user_role="finance",
    n_results=5,
    include_citations=True,
    max_tokens=400
)

# Access components
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']['level']} ({result['confidence']['score']:.1%})")

for source in result['sources']:
    print(f"[{source['rank']}] {source['source']} - {source['relevance_percent']}")
```

### Role-Based Access

```python
# Different roles get different documents
admin_result = pipeline.query("Company overview", user_role="admin")  # All docs
finance_result = pipeline.query("Budget info", user_role="finance")   # Finance docs only
employee_result = pipeline.query("Policies", user_role="employee")    # General docs only
```

## Response Format

```json
{
  "answer": "Generated answer with citations...",
  "sources": [
    {
      "rank": 1,
      "source": "quarterly_financial_report.md",
      "section": "Q4 2024 Results",
      "relevance_score": 0.852,
      "relevance_percent": "85.2%",
      "quality": "Highly Relevant"
    }
  ],
  "confidence": {
    "score": 0.823,
    "level": "HIGH",
    "reasoning": "Multiple highly relevant documents found",
    "details": {
      "avg_relevance": 0.823,
      "num_results": 5,
      "top_relevance": 0.852
    }
  },
  "metadata": {
    "query": "What were the Q4 2024 results?",
    "role": "finance",
    "num_results": 5,
    "query_type": "factual"
  }
}
```

## Testing

Run comprehensive test suite:

```bash
python tests/test_rag_pipeline.py
```

Test cases include:
1. Finance role queries (factual, comparison)
2. Marketing role queries (summary)
3. Engineering role queries (technical)
4. Employee role queries (general)
5. HR role queries (employee data)
6. Admin role queries (cross-department)
7. RBAC enforcement tests
8. No-results scenarios
9. Multi-source integration
10. Query type detection

## Module 6 Deliverables

✅ **LLM Integration and API Management Module**
- OpenRouter API integration ([llm/llm_engine.py](../llm/llm_engine.py))
- Environment-based API key management ([.env](../.env))
- Model configuration ([llm/config.py](../llm/config.py))

✅ **RAG Pipeline Implementation**
- Complete pipeline ([rag_pipeline.py](rag_pipeline.py))
- User authentication → RBAC → Retrieval → Generation
- Error handling and fallbacks

✅ **Prompt Templates and Augmentation Logic**
- Centralized templates ([prompt_templates.py](prompt_templates.py))
- Query type detection
- Context formatting
- Citation formatting

✅ **Source Attribution and Citation System**
- Source tracking in responses
- Relevance scoring per source
- Quality classification
- Citation formatting in LLM prompts

✅ **Confidence Scoring**
- Relevance-based confidence ([confidence_scorer.py](confidence_scorer.py))
- Confidence levels (HIGH/MEDIUM/LOW/VERY LOW)
- Automatic disclaimers
- Source-level scoring

✅ **RAG Functionality Test Cases**
- Comprehensive test suite ([../tests/test_rag_pipeline.py](../tests/test_rag_pipeline.py))
- 10 test scenarios
- Role-based testing
- Query type coverage

## Architecture

```
RAGPipeline
├── QueryEngine (Semantic Search + RBAC)
├── LLMEngine (OpenRouter API)
├── PromptTemplates (Prompt Engineering)
└── ConfidenceScorer (Quality Metrics)
```

## Configuration

Environment variables (`.env`):
```env
OPENROUTER_API_KEY=your-api-key-here
DEFAULT_LLM_MODEL=mistral-7b
```

Pipeline settings ([config.py](../llm/config.py)):
```python
LLM_CONFIG = {
    "max_tokens": 500,
    "temperature": 0.7,
}

ANSWER_GENERATION_CONFIG = {
    "max_tokens": 300,
    "temperature": 0.5,
}
```

## Performance

- **Semantic Search**: ~20ms average
- **LLM Generation**: ~1-3 seconds (depends on model)
- **Total Pipeline**: ~1.5-3.5 seconds end-to-end
- **Confidence Accuracy**: Based on vector similarity metrics

## Error Handling

- Invalid role → Error message
- No documents found → Graceful fallback
- LLM API error → Error message with details
- Missing API key → Clear error message

## Future Enhancements

- Query expansion and reformulation
- Multi-query retrieval
- Hybrid search (BM25 + semantic)
- Response caching
- Streaming responses
- Multi-turn conversations
