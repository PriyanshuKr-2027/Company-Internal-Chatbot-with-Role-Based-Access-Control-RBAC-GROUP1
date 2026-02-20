"""RAG Pipeline Test Cases - Module 6 Deliverable"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag.rag_pipeline import RAGPipeline


class TestRAGPipeline:
    """Test suite for RAG Pipeline functionality"""
    
    def __init__(self):
        self.pipeline = RAGPipeline()
        self.test_results = []
    
    def run_test(self, test_name: str, query: str, role: str, expected_confidence: str = None):
        """
        Run a single test case
        
        Args:
            test_name: Name of the test
            query: User query to test
            role: User role for RBAC
            expected_confidence: Expected confidence level (optional)
        """
        print(f"\n{'='*80}")
        print(f"TEST: {test_name}")
        print(f"{'='*80}")
        print(f"Query: {query}")
        print(f"Role: {role}")
        print()
        
        try:
            result = self.pipeline.query(query, role)
            
            print(f"✓ Query executed successfully")
            print(f"\nANSWER:\n{result['answer']}")
            print(f"\nSOURCES ({len(result['sources'])}):")
            for source in result['sources']:
                print(f"  [{source['rank']}] {source['source']} - {source['section']}")
                print(f"      Relevance: {source['relevance_percent']} ({source['quality']})")
            
            print(f"\nCONFIDENCE:")
            print(f"  Level: {result['confidence']['level']}")
            print(f"  Score: {result['confidence']['score']:.1%}")
            print(f"  Reasoning: {result['confidence']['reasoning']}")
            
            print(f"\nMETADATA:")
            print(f"  Query Type: {result['metadata']['query_type']}")
            print(f"  Results Found: {result['metadata']['num_results']}")
            
            # Validate confidence if expected
            test_passed = True
            if expected_confidence and result['confidence']['level'] != expected_confidence:
                print(f"\n⚠️ WARNING: Expected {expected_confidence} confidence, got {result['confidence']['level']}")
                test_passed = False
            
            self.test_results.append({
                "name": test_name,
                "passed": test_passed,
                "confidence": result['confidence']['level']
            })
            
            if test_passed:
                print(f"\n✅ TEST PASSED")
            else:
                print(f"\n⚠️ TEST COMPLETED WITH WARNINGS")
                
        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            self.test_results.append({
                "name": test_name,
                "passed": False,
                "error": str(e)
            })
    
    def run_all_tests(self):
        """Execute all test cases"""
        
        print("=" * 80)
        print("RAG PIPELINE TEST SUITE - MODULE 6")
        print("=" * 80)
        
        # Test 1: Finance Role - Factual Query
        self.run_test(
            test_name="Finance Role - Quarterly Results",
            query="What were the financial results for Q4 2024?",
            role="finance"
        )
        
        # Test 2: Marketing Role - Summary Query
        self.run_test(
            test_name="Marketing Role - Campaign Overview",
            query="Summarize the marketing campaigns in 2024",
            role="marketing"
        )
        
        # Test 3: Engineering Role - Technical Query
        self.run_test(
            test_name="Engineering Role - Architecture",
            query="What is the microservices architecture design?",
            role="engineering"
        )
        
        # Test 4: Employee Role - General Query
        self.run_test(
            test_name="Employee Role - Remote Work Policy",
            query="What is the company policy on remote work?",
            role="employee"
        )
        
        # Test 5: HR Role - Employee Information
        self.run_test(
            test_name="HR Role - Employee Statistics",
            query="How many employees are in the engineering department?",
            role="hr"
        )
        
        # Test 6: Admin Role - Cross-Department Query
        self.run_test(
            test_name="Admin Role - Company Overview",
            query="What are the key initiatives across all departments?",
            role="admin"
        )
        
        # Test 7: RBAC Enforcement - Finance accessing Marketing
        self.run_test(
            test_name="RBAC Test - Finance Role on Marketing Query",
            query="What was the marketing budget for Q4?",
            role="finance"  # Should get no/limited results
        )
        
        # Test 8: Comparison Query
        self.run_test(
            test_name="Comparison Query - Quarterly Performance",
            query="Compare Q3 and Q4 2024 financial performance",
            role="finance"
        )
        
        # Test 9: No Results Scenario
        self.run_test(
            test_name="No Results Test - Out of Scope",
            query="What is the weather forecast for tomorrow?",
            role="employee"
        )
        
        # Test 10: Multi-source Integration
        self.run_test(
            test_name="Multi-source Query - Company Performance",
            query="How did the company perform overall in 2024?",
            role="admin"
        )
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.get("passed", False))
        failed = total - passed
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        print(f"\nDetailed Results:")
        for result in self.test_results:
            status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
            confidence = result.get("confidence", "N/A")
            print(f"  {status} - {result['name']} (Confidence: {confidence})")
            if "error" in result:
                print(f"         Error: {result['error']}")


def main():
    """Run all RAG pipeline tests"""
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env file")
        print("Please create a .env file with your API key")
        return
    
    # Run tests
    tester = TestRAGPipeline()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
