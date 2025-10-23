# VectorWise: Scalable Approximate Nearest Neighbor (ANN) Search Engine

## 🚀 Project Overview
This project focuses on building a high-performance **Approximate Nearest Neighbor (ANN)** search engine crucial for modern applications like Retrieval-Augmented Generation (RAG) and recommender systems. By leveraging algorithms like HNSW and advanced libraries such as **Faiss** and **Annoy**, we demonstrate how to achieve sub-millisecond retrieval latency on massive, high-dimensional vector datasets, significantly outperforming brute-force k-NN search.

The repository includes the full pipeline from embedding generation to serving the optimized search index via a RESTful API.

## ⚙️ Key Technologies
* **Python, NumPy:** Core implementation and vector handling.
* **Faiss / Annoy:** ANN index creation and querying.
* **FastAPI:** Serving the search engine as a low-latency API endpoint.
* **Docker:** Ensuring reproducible deployment.
* **Algorithms:** HNSW (Hierarchical Navigable Small World) or other tree-based structures.

## 📋 Project Scope and Deliverables
1.  **Embedding Generation:** Generating [NUMBER] dimensional embeddings from the **[DATASET NAME]** dataset.
2.  **Index Optimization:** Implementing and comparing different ANN index types (e.g., `IndexHNSWFlat`, `IndexIVFFlat`) and optimizing parameters like the number of clusters and quantization methods.
3.  **API Development:** Creating a `/search` endpoint that accepts a query vector and returns the top-K closest neighbors.
4.  **Performance Analysis:** Benchmarking the retrieval speed (QPS) and search accuracy (Recall@K) against a baseline brute-force method.

## 📊 Results and Benchmarks
The optimized ANN engine achieved a **[RECALL VALUE]% Recall@10** while processing queries at **[QPS VALUE] Queries Per Second (QPS)**, demonstrating a **[X]-fold** speedup over brute-force k-NN on a dataset of [DATASET SIZE] vectors.

## 🏃 Getting Started
1.  Clone the repository: `git clone [YOUR REPO URL]`
2.  Build and run the search service: `docker-compose up --build`
3.  The API will be accessible at `http://localhost:8000`. Refer to `api/search_test.py` for example query formats.
