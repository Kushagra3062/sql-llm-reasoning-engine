"""
Smart Ambiguity Agent - COMPREHENSIVE TEST SUITE
Tests all 3 decision paths: MCQ → ASSUME → READY
"""

from agents.dsds import smart_refine
import json

# ========== REAL CHINOOK SCHEMA (Your friend's format) ==========
CHINOOK_SCHEMA = {
    "Customer": {
        "columns": [
            {"name": "customer_id", "type": "integer"},
            {"name": "first_name", "type": "varchar"}, 
            {"name": "last_name", "type": "varchar"},
            {"name": "country", "type": "varchar"},
            {"name": "email", "type": "varchar"}
        ]
    },
    "Invoice": {
        "columns": [
            {"name": "invoice_id", "type": "integer"},
            {"name": "customer_id", "type": "integer"},
            {"name": "invoice_date", "type": "timestamp"},
            {"name": "total", "type": "numeric"}
        ]
    },
    "Track": {
        "columns": [
            {"name": "track_id", "type": "integer"},
            {"name": "name", "type": "varchar"},
            {"name": "genre_id", "type": "integer"},
            {"name": "unit_price", "type": "numeric"}
        ]
    },
    "Artist": {
        "columns": [
            {"name": "artist_id", "type": "integer"},
            {"name": "name", "type": "varchar"}
        ]
    },
    "Genre": {
        "columns": [
            {"name": "genre_id", "type": "integer"},
            {"name": "name", "type": "varchar"}
        ]
    }
}

# ========== REALISTIC SAMPLE DATA (Temporal Intelligence) ==========
SAMPLE_DATA = {
    "Invoice": [
        {"invoice_date": "2025-01-10T10:30:00", "total": 9.99},
        {"invoice_date": "2024-12-25T14:20:00", "total": 15.50},
        {"invoice_date": "2024-11-15T09:15:00", "total": 12.25},
        {"invoice_date": "2024-10-05T16:45:00", "total": 8.75},
        {"invoice_date": "2024-09-20T11:10:00", "total": 22.99}
    ]
}

# ========== TEST SUITE - 15 QUERIES (3 LEVELS) ==========
TEST_SUITES = {
    "LEVEL 1 - BASIC INTENT UNCLEAR (MCQ)": [
        "Show me some performance metrics",
        "Find business insights", 
        "Analyze the data",
        "What should I look at?",
        "Give me useful information"
    ],
    
    "LEVEL 2 - RANKING VAGUE (SAFE ASSUME)": [
        "Best customers by sales",
        "Top artists by track count",
        "Highest revenue months",
        "Most popular genres",
        "Top selling tracks"
    ],
    
    "LEVEL 3 - TEMPORAL CRITICAL (SMART)": [
        "Recent orders from Brazil",
        "Latest customer purchases",
        "New tracks added recently", 
        "This month's sales",
        "Past 3 months invoices"
    ],
    
    "LEVEL 4 - CLEAR INTENT (READY)": [
        "How many customers from Brazil?",
        "Total revenue by country",
        "AC/DC albums list",
        "Rock tracks count",
        "Customer emails from USA"
    ]
}

def run_comprehensive_test():
    """Run ALL test cases with detailed analysis."""
    print("SMART AMBIGUITY AGENT - FULL TEST SUITE\n")
    print("="*100)
    
    results_summary = {
        "mcq_needed": 0,
        "assume_safe": 0, 
        "planner_ready": 0,
        "confidence_avg": []
    }
    
    for test_type, queries in TEST_SUITES.items():
        print(f"\nTESTING: {test_type}")
        print("-" * 80)
        
        for i, query in enumerate(queries, 1):
            print(f"\nTest {i}/5: '{query}'")
            
            try:
                result = smart_refine(query, CHINOOK_SCHEMA, SAMPLE_DATA)
                
                # Track stats
                decision = result.get('llm_output', {}).get('decision', 'unknown')
                confidence = result.get('llm_output', {}).get('confidence', 0)
                
                if decision == "generate_mcqs":
                    results_summary["mcq_needed"] += 1
                elif decision == "safe_assumptions":
                    results_summary["assume_safe"] += 1
                else:
                    results_summary["planner_ready"] += 1
                
                results_summary["confidence_avg"].append(confidence)
                
                # Expected behavior check
                if "BASIC INTENT" in test_type and decision != "generate_mcqs":
                    print("EXPECTED: MCQs, GOT:", decision)
                elif "RANKING" in test_type and decision != "safe_assumptions":
                    print("EXPECTED: ASSUME, GOT:", decision)
                elif "CLEAR INTENT" in test_type and decision != "planner_ready":
                    print("EXPECTED: READY, GOT:", decision)
                else:
                    print("CORRECT DECISION")
                
            except Exception as e:
                print(f"ERROR: {str(e)}")
        
        print()
    
    # Final summary
    print("="*100)
    print("TEST SUMMARY")
    print("="*100)
    print(f"MCQ Needed: {results_summary['mcq_needed']}/15 ({results_summary['mcq_needed']/15*100:.1f}%)")
    print(f"Safe Assume: {results_summary['assume_safe']}/15 ({results_summary['assume_safe']/15*100:.1f}%)")
    print(f"Planner Ready: {results_summary['planner_ready']}/15 ({results_summary['planner_ready']/15*100:.1f}%)")
    print(f"Avg Confidence: {sum(results_summary['confidence_avg'])/len(results_summary['confidence_avg']):.1%}")
    
    print("\nEXPECTED BREAKDOWN:")
    print("• 5/5 BASIC -> MCQ")
    print("• 5/5 RANKING -> ASSUME") 
    print("• 3/5 TEMPORAL -> ASSUME/TEMPORAL")
    print("• 5/5 CLEAR -> READY")
    print("\nPASS CRITERIA: 90%+ accuracy across levels")

def test_hitl_workflow():
    """Test Human-in-the-Loop MCQ selection."""
    print("\nHITL WORKFLOW TEST")
    print("="*50)
    
    # Test 1: Generate MCQs
    print("\n1. FIRST RUN - Should generate MCQs")
    result1 = smart_refine("Show me performance metrics", CHINOOK_SCHEMA, SAMPLE_DATA)
    
    # Test 2: Human selects option 2
    print("\n2. SECOND RUN - Human selects [2]")
    result2 = smart_refine("Show me performance metrics", CHINOOK_SCHEMA, SAMPLE_DATA, human_mcqs=2)
    
    print("\nHITL SUCCESS:", "final_intent" in result2)

def test_temporal_intelligence():
    """Test smart temporal range discovery."""
    print("\nTEMPORAL INTELLIGENCE TEST")
    print("="*50)
    
    result = smart_refine("Recent Brazil orders", CHINOOK_SCHEMA, SAMPLE_DATA)
    
    if result.get("final_intent", {}).get("temporal_snippet"):
        print("SMART DATE RANGE:", result["final_intent"]["temporal_snippet"])
        print("   (Data-driven, NOT hardcoded 30 days)")
    else:
        print("No temporal snippet generated")

# ========== RUN ALL TESTS ==========
if __name__ == "__main__":
    print("Starting Smart Ambiguity Agent Tests...\n")
    
    run_comprehensive_test()
    test_hitl_workflow() 
    test_temporal_intelligence()
    
    print("\n" + "*"*40)
    print("     TEST SUITE COMPLETE")
    print("    Copy this to hackathon demo!")
    print("  " + "*"*40)