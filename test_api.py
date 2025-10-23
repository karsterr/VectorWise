"""
Simple test script to verify the VectorWise API is working correctly.
Run this after starting the service with docker-compose up.
"""

import requests
import numpy as np
import json

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n[TEST 1] Health Check...")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed!")

def test_stats():
    """Test the stats endpoint"""
    print("\n[TEST 2] Index Statistics...")
    response = requests.get(f"{API_BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["total_vectors"] > 0
    print("✅ Stats endpoint passed!")

def test_search():
    """Test the search endpoint"""
    print("\n[TEST 3] Vector Search...")
    
    # Generate a random query vector
    np.random.seed(42)
    query_vector = np.random.randn(128).tolist()
    
    payload = {
        "query_vector": query_vector,
        "k": 10
    }
    
    response = requests.post(f"{API_BASE_URL}/search", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result['indices'])} neighbors")
        print(f"Sample indices: {result['indices'][:3]}")
        print(f"Sample distances: {result['distances'][:3]}")
        assert len(result['indices']) == 10
        assert len(result['distances']) == 10
        print("✅ Search endpoint passed!")
    else:
        print(f"❌ Search failed: {response.text}")

def test_invalid_dimension():
    """Test error handling for invalid dimensions"""
    print("\n[TEST 4] Invalid Dimension Handling...")
    
    # Send a vector with wrong dimension
    payload = {
        "query_vector": [0.1, 0.2, 0.3],  # Only 3 dimensions instead of 128
        "k": 10
    }
    
    response = requests.post(f"{API_BASE_URL}/search", json=payload)
    print(f"Status: {response.status_code}")
    assert response.status_code == 400
    print("✅ Invalid dimension handling passed!")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("VectorWise API Test Suite")
    print("=" * 60)
    
    try:
        test_health_check()
        test_stats()
        test_search()
        test_invalid_dimension()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("Make sure the service is running:")
        print("  $ docker-compose up -d")
        print("  OR")
        print("  $ uvicorn api.main:app --reload")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_all_tests()
