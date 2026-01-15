"""
RAG Pipeline Usage Examples

This file demonstrates how to use the RAG pipeline for different query scenarios.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rag.rag_pipeline import RAGPipeline


def main():
    """Run example queries across different roles"""
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env file")
        print("Please create a .env file with:")
        print("OPENROUTER_API_KEY=your-api-key-here")
        return
    
    # Initialize RAG pipeline
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline()
    print()
    
    # Example 1: Finance Query
    print("=" * 80)
    print("EXAMPLE 1: Finance Role - Quarterly Results")
    print("=" * 80)
    response = pipeline.query_with_sources(
        user_query="What were the financial results for Q4 2024?",
        user_role="finance"
    )
    print(response)
    print()
    
    # Example 2: Marketing Query
    print("=" * 80)
    print("EXAMPLE 2: Marketing Role - Campaign Summary")
    print("=" * 80)
    response = pipeline.query_with_sources(
        user_query="Summarize the marketing campaigns in 2024",
        user_role="marketing"
    )
    print(response)
    print()
    
    # Example 3: Engineering Query
    print("=" * 80)
    print("EXAMPLE 3: Engineering Role - Architecture")
    print("=" * 80)
    response = pipeline.query_with_sources(
        user_query="What is the microservices architecture design?",
        user_role="engineering"
    )
    print(response)
    print()
    
    # Example 4: Employee Query
    print("=" * 80)
    print("EXAMPLE 4: Employee Role - Company Policy")
    print("=" * 80)
    response = pipeline.query_with_sources(
        user_query="What are the core company values?",
        user_role="employee"
    )
    print(response)
    print()
    
    # Example 5: Admin Cross-Department Query
    print("=" * 80)
    print("EXAMPLE 5: Admin Role - Company Overview")
    print("=" * 80)
    response = pipeline.query_with_sources(
        user_query="How did the company perform overall in 2024?",
        user_role="admin"
    )
    print(response)
    print()
    
    # Example 6: Programmatic Access (Get Full Response Object)
    print("=" * 80)
    print("EXAMPLE 6: Programmatic Access - Full Response Object")
    print("=" * 80)
    result = pipeline.query(
        user_query="What was the Q4 revenue?",
        user_role="finance",
        n_results=5,
        include_citations=True
    )
    
    print(f"Answer: {result['answer']}\n")
    print(f"Confidence: {result['confidence']['level']} ({result['confidence']['score']:.1%})")
    print(f"Query Type: {result['metadata']['query_type']}")
    print(f"\nSources ({len(result['sources'])}):")
    for source in result['sources']:
        print(f"  [{source['rank']}] {source['source']} - {source['section']}")
        print(f"      {source['relevance_percent']} - {source['quality']}")
    print()


if __name__ == "__main__":
    main()
