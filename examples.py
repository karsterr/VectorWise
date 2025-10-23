"""
VectorWise Usage Examples
Demonstrates how to interact with the VectorWise API in various scenarios.
"""

import requests
import numpy as np
import json
from typing import List, Dict

# Configuration
API_BASE_URL = "http://localhost:8000"


class VectorWiseClient:
    """Simple client for interacting with VectorWise API"""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def health_check(self) -> Dict:
        """Check if the service is healthy"""
        response = requests.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()

    def get_stats(self) -> Dict:
        """Get index statistics"""
        response = requests.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()

    def search(self, query_vector: List[float], k: int = 10) -> Dict:
        """Search for k nearest neighbors"""
        payload = {"query_vector": query_vector, "k": k}
        response = requests.post(f"{self.base_url}/search", json=payload)
        response.raise_for_status()
        return response.json()


def example_1_basic_search():
    """Example 1: Basic vector search"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Vector Search")
    print("=" * 60)

    client = VectorWiseClient()

    # Generate a random query vector
    np.random.seed(42)
    query = np.random.randn(128).tolist()

    # Search for 5 nearest neighbors
    results = client.search(query, k=5)

    print(f"\nQuery vector (first 5 dims): {query[:5]}")
    print(f"\nTop 5 nearest neighbors:")
    for i, (idx, dist) in enumerate(zip(results["indices"], results["distances"])):
        print(f"  {i+1}. Index: {idx:6d}  Distance: {dist:.4f}")


def example_2_batch_search():
    """Example 2: Batch searching multiple queries"""
    print("\n" + "=" * 60)
    print("Example 2: Batch Search (Multiple Queries)")
    print("=" * 60)

    client = VectorWiseClient()

    # Generate multiple queries
    n_queries = 5
    np.random.seed(123)
    queries = [np.random.randn(128).tolist() for _ in range(n_queries)]

    print(f"\nSearching {n_queries} queries...")

    all_results = []
    for i, query in enumerate(queries):
        result = client.search(query, k=3)
        all_results.append(result)
        print(f"  Query {i+1}: Found {len(result['indices'])} neighbors")

    # Aggregate statistics
    all_distances = [dist for result in all_results for dist in result["distances"]]
    avg_distance = np.mean(all_distances)
    print(f"\nAverage distance across all queries: {avg_distance:.4f}")


def example_3_different_k_values():
    """Example 3: Searching with different k values"""
    print("\n" + "=" * 60)
    print("Example 3: Different K Values")
    print("=" * 60)

    client = VectorWiseClient()

    # Single query vector
    np.random.seed(789)
    query = np.random.randn(128).tolist()

    # Try different k values
    k_values = [1, 5, 10, 20, 50]

    print(f"\nSearching with different k values...")
    for k in k_values:
        result = client.search(query, k=k)
        avg_dist = np.mean(result["distances"])
        max_dist = max(result["distances"])
        print(f"  k={k:2d}: Avg distance: {avg_dist:.4f}, Max distance: {max_dist:.4f}")


def example_4_similarity_threshold():
    """Example 4: Filtering by similarity threshold"""
    print("\n" + "=" * 60)
    print("Example 4: Similarity Threshold Filtering")
    print("=" * 60)

    client = VectorWiseClient()

    np.random.seed(456)
    query = np.random.randn(128).tolist()

    # Search for many neighbors
    result = client.search(query, k=50)

    # Filter by distance threshold
    threshold = 1.0
    filtered = [
        (idx, dist)
        for idx, dist in zip(result["indices"], result["distances"])
        if dist <= threshold
    ]

    print(f"\nTotal neighbors found: {len(result['indices'])}")
    print(f"Neighbors within threshold ({threshold}): {len(filtered)}")
    print(f"\nTop 5 filtered results:")
    for i, (idx, dist) in enumerate(filtered[:5]):
        print(f"  {i+1}. Index: {idx:6d}  Distance: {dist:.4f}")


def example_5_normalized_vectors():
    """Example 5: Working with normalized vectors"""
    print("\n" + "=" * 60)
    print("Example 5: Normalized Vector Search")
    print("=" * 60)

    client = VectorWiseClient()

    # Generate a random vector and normalize it
    np.random.seed(999)
    query = np.random.randn(128)

    # L2 normalize
    query_normalized = query / np.linalg.norm(query)

    print(f"\nOriginal vector norm: {np.linalg.norm(query):.4f}")
    print(f"Normalized vector norm: {np.linalg.norm(query_normalized):.4f}")

    # Search with normalized vector
    result = client.search(query_normalized.tolist(), k=10)

    print(f"\nTop 3 results:")
    for i in range(3):
        idx = result["indices"][i]
        dist = result["distances"][i]
        print(f"  {i+1}. Index: {idx:6d}  Distance: {dist:.4f}")


def example_6_error_handling():
    """Example 6: Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)

    client = VectorWiseClient()

    # Try with invalid dimension
    print("\nTesting with invalid dimension (64 instead of 128)...")
    try:
        invalid_query = np.random.randn(64).tolist()
        result = client.search(invalid_query, k=10)
        print("  ❌ Should have raised an error!")
    except requests.exceptions.HTTPError as e:
        print(f"  ✓ Caught expected error: {e.response.status_code}")
        print(f"    Error message: {e.response.json()['detail']}")

    # Try with invalid k
    print("\nTesting with invalid k (0)...")
    try:
        valid_query = np.random.randn(128).tolist()
        payload = {"query_vector": valid_query, "k": 0}
        response = requests.post(f"{client.base_url}/search", json=payload)
        response.raise_for_status()
        print("  ❌ Should have raised an error!")
    except requests.exceptions.HTTPError as e:
        print(f"  ✓ Caught expected error: {e.response.status_code}")


def main():
    """Run all examples"""
    print("=" * 60)
    print("VectorWise API Usage Examples")
    print("=" * 60)

    try:
        # Check if service is running
        client = VectorWiseClient()
        health = client.health_check()
        print(f"\n✓ Service is running: {health['service']}")

        stats = client.get_stats()
        print(f"✓ Index contains {stats['total_vectors']:,} vectors")

        # Run examples
        example_1_basic_search()
        example_2_batch_search()
        example_3_different_k_values()
        example_4_similarity_threshold()
        example_5_normalized_vectors()
        example_6_error_handling()

        print("\n" + "=" * 60)
        print("All examples completed successfully! ✅")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to VectorWise API")
        print("Make sure the service is running:")
        print("  $ docker-compose up -d")
        print("  OR")
        print("  $ uvicorn api.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
