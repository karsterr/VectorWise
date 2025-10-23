"""
VectorWise - Data Generation and Faiss Index Builder
Generates 1M synthetic vectors (128-dim) and builds an optimized HNSW index.
"""

import numpy as np
import faiss
import time

# Configuration
N_VECTORS = 1_000_000  # 1 Million vectors
DIM = 128              # Dimensionality
SEED = 42              # For reproducibility

# HNSW Parameters (optimized for 95%+ Recall@10)
M = 32                 # Number of connections per layer
EF_CONSTRUCTION = 200  # Size of dynamic candidate list during construction

print("=" * 60)
print("VectorWise - Data Generation & Index Building")
print("=" * 60)

# Step 1: Generate synthetic vectors
print(f"\n[1/4] Generating {N_VECTORS:,} vectors of dimension {DIM}...")
np.random.seed(SEED)
vectors = np.random.randn(N_VECTORS, DIM).astype('float32')

# Normalize vectors (optional but often improves search quality)
faiss.normalize_L2(vectors)

print(f"✓ Generated vectors with shape: {vectors.shape}")
print(f"✓ Memory usage: {vectors.nbytes / 1024 / 1024:.2f} MB")

# Step 2: Save vectors to disk
print("\n[2/4] Saving vectors to 'vectors.npy'...")
np.save('vectors.npy', vectors)
print("✓ Vectors saved successfully")

# Step 3: Build Faiss HNSW index
print("\n[3/4] Building Faiss HNSW index...")
print(f"   - M (connections per layer): {M}")
print(f"   - efConstruction: {EF_CONSTRUCTION}")

start_time = time.time()

# Create HNSW index
index = faiss.IndexHNSWFlat(DIM, M)
index.hnsw.efConstruction = EF_CONSTRUCTION

# Add vectors to index
print("   - Adding vectors to index...")
index.add(vectors)

build_time = time.time() - start_time
print(f"✓ Index built in {build_time:.2f} seconds")
print(f"✓ Index contains {index.ntotal:,} vectors")

# Step 4: Save index to disk
print("\n[4/4] Saving index to 'index.faiss'...")
faiss.write_index(index, 'index.faiss')
print("✓ Index saved successfully")

# Display index statistics
print("\n" + "=" * 60)
print("INDEX STATISTICS")
print("=" * 60)
print(f"Total vectors: {index.ntotal:,}")
print(f"Dimension: {DIM}")
print(f"Index type: HNSW")
print(f"M parameter: {M}")
print(f"efConstruction: {EF_CONSTRUCTION}")
print(f"File size: {np.load('vectors.npy').nbytes / 1024 / 1024:.2f} MB (vectors.npy)")

import os
if os.path.exists('index.faiss'):
    index_size = os.path.getsize('index.faiss') / 1024 / 1024
    print(f"File size: {index_size:.2f} MB (index.faiss)")

print("\n✅ Data generation and indexing complete!")
print("=" * 60)
