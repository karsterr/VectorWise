# VectorWise - Complete Execution Guide

## 🎯 Quick Reference

This guide walks you through the complete execution of the VectorWise project, from data generation to benchmarking.

---

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.11 or higher
- [ ] pip (Python package manager)
- [ ] Docker and Docker Compose (for containerized deployment)
- [ ] At least 2GB of RAM
- [ ] ~1.5GB of disk space

---

## 📋 Execution Steps

### Step 1: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Expected packages:**

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.5.0
- numpy==1.24.3
- faiss-cpu==1.7.4
- requests==2.31.0

**Verification:**

```bash
python -c "import faiss; import fastapi; print('✅ Dependencies installed')"
```

---

### Step 2: Generate Data and Build Index

```bash
# Run the data generation script
python generate_data.py
```

**What this does:**

1. Generates 1,000,000 random vectors (128 dimensions each)
2. Normalizes vectors using L2 normalization
3. Builds HNSW index with M=32, efConstruction=200
4. Saves `vectors.npy` (~500 MB)
5. Saves `index.faiss` (~600 MB)

**Expected output:**

```
============================================================
VectorWise - Data Generation & Index Building
============================================================

[1/4] Generating 1,000,000 vectors of dimension 128...
✓ Generated vectors with shape: (1000000, 128)
✓ Memory usage: 512.00 MB

[2/4] Saving vectors to 'vectors.npy'...
✓ Vectors saved successfully

[3/4] Building Faiss HNSW index...
   - M (connections per layer): 32
   - efConstruction: 200
   - Adding vectors to index...
✓ Index built in 45.23 seconds
✓ Index contains 1,000,000 vectors

[4/4] Saving index to 'index.faiss'...
✓ Index saved successfully

============================================================
INDEX STATISTICS
============================================================
Total vectors: 1,000,000
Dimension: 128
Index type: HNSW
M parameter: 32
efConstruction: 200
File size: 512.00 MB (vectors.npy)
File size: 627.45 MB (index.faiss)

✅ Data generation and indexing complete!
============================================================
```

**Time estimate:** 1-2 minutes on modern hardware

**Verification:**

```bash
ls -lh vectors.npy index.faiss
# Should show both files with sizes ~500MB and ~600MB
```

---

### Step 3: Launch the Service

You have two options:

#### Option A: Docker Compose (Recommended)

```bash
# Build and start the containerized service
docker-compose up --build -d

# Verify the container is running
docker-compose ps

# View logs
docker-compose logs -f vectorwise
```

**Expected output:**

```
[+] Building 15.2s (12/12) FINISHED
[+] Running 1/1
 ✔ Container vectorwise-api  Started

INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Loading Faiss index from 'index.faiss'...
INFO:     ✓ Index loaded successfully: 1,000,000 vectors
INFO:     ✓ Index type: IndexHNSWFlat
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Option B: Local Development

```bash
# Run directly with uvicorn
uvicorn api.main:app --reload
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Loading Faiss index from 'index.faiss'...
INFO:     ✓ Index loaded successfully: 1,000,000 vectors
INFO:     ✓ Index type: IndexHNSWFlat
INFO:     Application startup complete.
```

**Service URL:** http://localhost:8000

---

### Step 4: Test the API

```bash
# Run the test suite
python test_api.py
```

**Expected output:**

```
============================================================
VectorWise API Test Suite
============================================================

[TEST 1] Health Check...
Status: 200
Response: {
  "service": "VectorWise",
  "status": "healthy",
  "vectors_indexed": 1000000
}
✅ Health check passed!

[TEST 2] Index Statistics...
Status: 200
Response: {
  "total_vectors": 1000000,
  "dimension": 128,
  "index_type": "IndexHNSWFlat",
  "hnsw_m": 32,
  "hnsw_efSearch": 64
}
✅ Stats endpoint passed!

[TEST 3] Vector Search...
Status: 200
Found 10 neighbors
Sample indices: [456789, 123456, 789012]
Sample distances: [0.8234, 0.8567, 0.8901]
✅ Search endpoint passed!

[TEST 4] Invalid Dimension Handling...
Status: 400
✅ Invalid dimension handling passed!

============================================================
✅ All tests passed!
============================================================
```

---

### Step 5: Run Benchmarks

```bash
# Run the performance benchmark
python benchmark.py
```

**Expected output:**

```
======================================================================
VectorWise - Performance Benchmark
======================================================================

[1/4] Loading vectors and indexes...
✓ Loaded 1,000,000 vectors
✓ Loaded HNSW index with 1,000,000 vectors
   Creating brute-force index for ground truth...
✓ Created brute-force index

[2/4] Generating test queries...
✓ Generated 1,000 test queries

[3/4] Measuring API latency...
   Warming up API...
   Benchmarking latency...
   Progress: 100/1000 queries
   Progress: 200/1000 queries
   ...
   Progress: 1000/1000 queries

✓ Latency Metrics:
   - Average:   5.23 ms
   - Median:    4.87 ms
   - P95:       8.12 ms
   - P99:       11.45 ms

[4/4] Measuring Recall@10...
   Computing ground truth (brute-force)...
   Computing HNSW results...

✓ Recall@10 Metrics:
   - Average:   96.75%
   - Min:       91.00%
   - Max:       100.00%

======================================================================
HNSW INDEX PARAMETERS
======================================================================
M (connections per layer):      32
efConstruction (build-time):    200
efSearch (search-time):         64

======================================================================
PERFORMANCE SUMMARY
======================================================================
Dataset Size:           1,000,000 vectors
Vector Dimension:       128
Test Queries:           1,000
Neighbors Retrieved:    10

📊 Latency (Average):   5.23 ms
📊 Latency (P95):       8.12 ms
🎯 Recall@10:           96.75%

✅ PERFORMANCE TARGET MET: Recall@10 ≥ 95%

💡 Trade-off Insight:
   Good balance between latency and recall.

======================================================================
Benchmark complete!
======================================================================

📁 Results saved to 'benchmark_results.json'
```

**Time estimate:** 5-10 minutes

**Verification:**

```bash
cat benchmark_results.json | python -m json.tool
```

---

### Step 6: Interactive API Testing

Open your browser and visit:

1. **Swagger UI:** http://localhost:8000/docs

   - Interactive API documentation
   - Try out endpoints directly

2. **ReDoc:** http://localhost:8000/redoc
   - Alternative documentation view

Or use curl:

```bash
# Health check
curl http://localhost:8000/

# Get statistics
curl http://localhost:8000/stats

# Perform search (example with random vector)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
                     0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    "k": 10
  }'
```

---

### Step 7: Run Usage Examples

```bash
# Run comprehensive examples
python examples.py
```

This demonstrates:

- Basic vector search
- Batch searching
- Different k values
- Similarity filtering
- Normalized vectors
- Error handling

---

## 🔄 Service Management

### Stop the Service

```bash
# Docker Compose
docker-compose down

# Local (Ctrl+C to stop uvicorn)
```

### Restart the Service

```bash
# Docker Compose
docker-compose restart

# Local - just run uvicorn again
uvicorn api.main:app --reload
```

### View Logs

```bash
# Docker Compose
docker-compose logs -f vectorwise

# Local - logs appear in terminal
```

### Rebuild After Changes

```bash
# Docker Compose
docker-compose down
docker-compose up --build -d
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'faiss'"

**Solution:**

```bash
pip install faiss-cpu
```

### Issue: "FileNotFoundError: index.faiss"

**Solution:**

```bash
python generate_data.py
```

### Issue: "Connection refused" when testing

**Solution:**

```bash
# Check if service is running
docker-compose ps
# OR
curl http://localhost:8000/
```

### Issue: "Port 8000 already in use"

**Solution:**

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# OR change port in docker-compose.yml
```

---

## 📊 Expected Performance

Based on the implementation:

| Metric           | Target | Expected  |
| ---------------- | ------ | --------- |
| Latency (Avg)    | <10ms  | 4-6ms ✅  |
| Latency (P95)    | <20ms  | ~8ms ✅   |
| Recall@10        | ≥95%   | 95-98% ✅ |
| Index Build Time | <5min  | 1-2min ✅ |
| Memory Usage     | <2GB   | ~1.2GB ✅ |

---

## ✅ Success Criteria

After completing all steps, you should have:

- [x] Generated 1M vectors and built HNSW index
- [x] FastAPI service running on port 8000
- [x] All API tests passing
- [x] Benchmark results showing 95%+ Recall@10
- [x] Average latency under 10ms
- [x] Complete documentation

---

## 🚀 Quick Start (Automated)

For a fully automated setup:

```bash
# Make the script executable (if not already)
chmod +x quickstart.sh

# Run the quick start script
./quickstart.sh
```

---

## 📚 Additional Resources

- **Architecture:** See ARCHITECTURE.md
- **Summary:** See SUMMARY.md
- **API Docs:** http://localhost:8000/docs
- **Examples:** examples.py

---

## 🎓 Next Steps

1. **Optimize Parameters:** Tune M, efConstruction, efSearch for your use case
2. **Scale Up:** Deploy multiple instances with load balancer
3. **Monitor:** Add Prometheus metrics
4. **Secure:** Add authentication and rate limiting
5. **Enhance:** Add batch search endpoint for multiple queries

---

**Need Help?** Check the troubleshooting section in README.md
