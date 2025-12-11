"""
Test script for the AI Researcher Agent API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search(topic, max_results=3):
    """Test the search endpoint"""
    print(f"Testing /search endpoint with topic: '{topic}'...")
    response = requests.get(
        f"{BASE_URL}/search",
        params={"topic": topic, "max_results": max_results}
    )
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        entries = data.get("entries", [])
        print(f"Found {len(entries)} papers:")
        for i, paper in enumerate(entries, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
            print(f"   Categories: {', '.join(paper['categories'][:3])}")
            print(f"   PDF: {paper['pdf']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    # Test health endpoint
    test_health()
    
    # Test search endpoint with different topics
    test_search("machine learning", max_results=2)
    test_search("quantum computing", max_results=2)
    test_search("neural networks", max_results=2)
