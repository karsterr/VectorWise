"""
VectorWise - Performance Benchmark Suite
Measures latency and Recall@10 for the ANN search service.
"""

import numpy as np
import faiss
import time
import requests
import json
from typing import Tuple, List
import statistics

# Configuration
API_URL = "http://localhost:8000/search"
N_QUERIES = 1000  # Number of test queries
K = 10            # Number of neighbors to retrieve
DIM = 128         # Vector dimension

print("=" * 70)
print("VectorWise - Performance Benchmark")
print("=" * 70)

# Step 1: Load data and indexes
print("\n[1/4] Loading vectors and indexes...")
vectors = np.load('vectors.npy')
print(f"✓ Loaded {len(vectors):,} vectors")

# Load HNSW index
hnsw_index = faiss.read_index('index.faiss')
print(f"✓ Loaded HNSW index with {hnsw_index.ntotal:,} vectors")

# Create brute-force index for ground truth
print("   Creating brute-force index for ground truth...")
bf_index = faiss.IndexFlatL2(DIM)
bf_index.add(vectors)
print(f"✓ Created brute-force index")

# Step 2: Generate test queries
print("\n[2/4] Generating test queries...")
np.random.seed(123)
query_indices = np.random.randint(0, len(vectors), N_QUERIES)
queries = vectors[query_indices].copy()

# Add some noise to make it more realistic
queries += np.random.randn(N_QUERIES, DIM).astype('float32') * 0.1
faiss.normalize_L2(queries)
print(f"✓ Generated {N_QUERIES:,} test queries")

# Step 3: Measure Latency (API Response Time)
print("\n[3/4] Measuring API latency...")
print("   Warming up API...")

# Warm-up requests
for i in range(10):
    query = queries[i].tolist()
    try:
        response = requests.post(API_URL, json={"query_vector": query, "k": K})
        if response.status_code != 200:
            print(f"   Warning: Warm-up request {i+1} failed")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API at", API_URL)
        print("   Make sure the service is running:")
        print("   $ docker-compose up -d")
        print("   OR")
        print("   $ uvicorn api.main:app --reload")
        exit(1)

print("   Benchmarking latency...")
latencies = []

for i in range(N_QUERIES):
    query = queries[i].tolist()
    
    start_time = time.time()
    response = requests.post(API_URL, json={"query_vector": query, "k": K})
    latency = (time.time() - start_time) * 1000  # Convert to ms
    
    if response.status_code == 200:
        latencies.append(latency)
    
    if (i + 1) % 100 == 0:
        print(f"   Progress: {i+1}/{N_QUERIES} queries")

# Calculate latency statistics
avg_latency = statistics.mean(latencies)
median_latency = statistics.median(latencies)
p95_latency = np.percentile(latencies, 95)
p99_latency = np.percentile(latencies, 99)

print(f"\n✓ Latency Metrics:")
print(f"   - Average:   {avg_latency:.2f} ms")
print(f"   - Median:    {median_latency:.2f} ms")
print(f"   - P95:       {p95_latency:.2f} ms")
print(f"   - P99:       {p99_latency:.2f} ms")

# Step 4: Measure Recall@10
print("\n[4/4] Measuring Recall@10...")

# Get ground truth from brute-force search
print("   Computing ground truth (brute-force)...")
_, gt_indices = bf_index.search(queries, K)

# Get HNSW results
print("   Computing HNSW results...")
_, hnsw_indices = hnsw_index.search(queries, K)

# Calculate recall
recalls = []
for i in range(N_QUERIES):
    gt_set = set(gt_indices[i])
    hnsw_set = set(hnsw_indices[i])
    recall = len(gt_set.intersection(hnsw_set)) / K
    recalls.append(recall)

avg_recall = statistics.mean(recalls)
min_recall = min(recalls)
max_recall = max(recalls)

print(f"\n✓ Recall@{K} Metrics:")
print(f"   - Average:   {avg_recall*100:.2f}%")
print(f"   - Min:       {min_recall*100:.2f}%")
print(f"   - Max:       {max_recall*100:.2f}%")

# Step 5: Display HNSW Parameters
print("\n" + "=" * 70)
print("HNSW INDEX PARAMETERS")
print("=" * 70)
if hasattr(hnsw_index, 'hnsw'):
    print(f"M (connections per layer):      {hnsw_index.hnsw.max_level}")
    print(f"efConstruction (build-time):    200")
    print(f"efSearch (search-time):         {hnsw_index.hnsw.efSearch}")

# Step 6: Performance Summary
print("\n" + "=" * 70)
print("PERFORMANCE SUMMARY")
print("=" * 70)
print(f"Dataset Size:           {len(vectors):,} vectors")
print(f"Vector Dimension:       {DIM}")
print(f"Test Queries:           {N_QUERIES:,}")
print(f"Neighbors Retrieved:    {K}")
print()
print(f"📊 Latency (Average):   {avg_latency:.2f} ms")
print(f"📊 Latency (P95):       {p95_latency:.2f} ms")
print(f"🎯 Recall@{K}:           {avg_recall*100:.2f}%")
print()

# Trade-off analysis
if avg_recall >= 0.95:
    print("✅ PERFORMANCE TARGET MET: Recall@10 ≥ 95%")
else:
    print(f"⚠️  PERFORMANCE WARNING: Recall@10 ({avg_recall*100:.2f}%) < 95%")
    print("   Consider increasing efSearch or efConstruction parameters")

print()
print("💡 Trade-off Insight:")
if avg_latency < 5:
    print("   Excellent latency with high recall - well optimized!")
elif avg_latency < 10:
    print("   Good balance between latency and recall.")
else:
    print("   High latency - consider decreasing efSearch for faster queries.")

print("\n" + "=" * 70)
print("Benchmark complete!")
print("=" * 70)

# Save results to file
results = {
    "dataset_size": len(vectors),
    "dimension": DIM,
    "n_queries": N_QUERIES,
    "k": K,
    "latency_ms": {
        "average": round(avg_latency, 2),
        "median": round(median_latency, 2),
        "p95": round(p95_latency, 2),
        "p99": round(p99_latency, 2)
    },
    "recall_at_k": {
        "average": round(avg_recall * 100, 2),
        "min": round(min_recall * 100, 2),
        "max": round(max_recall * 100, 2)
    }
}

with open('benchmark_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n📁 Results saved to 'benchmark_results.json'")
