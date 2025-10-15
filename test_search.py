"""
Test Multi-Engine Search System
"""

from skills.multi_engine_search import search_web_multi_engine

def test_search():
    print("Testing Multi-Engine Search System...")
    print("=" * 50)
    
    # Test queries
    queries = [
        "latest AI news",
        "artificial intelligence developments 2024",
        "machine learning trends"
    ]
    
    for query in queries:
        print(f"\nTesting: {query}")
        print("-" * 30)
        result = search_web_multi_engine(query)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_search()