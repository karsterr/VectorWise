"""
VectorWise - FastAPI ANN Search Service
High-performance vector similarity search using Faiss HNSW index.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import faiss
import numpy as np
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="VectorWise",
    description="Scalable ANN Search Engine powered by Faiss",
    version="1.0.0"
)

# Global index variable
index = None
DIM = 128

# Request/Response models
class SearchRequest(BaseModel):
    query_vector: List[float] = Field(..., description="Query vector (128-dimensional)")
    k: int = Field(..., gt=0, le=100, description="Number of nearest neighbors to return")

class SearchResult(BaseModel):
    indices: List[int] = Field(..., description="Indices of nearest neighbors")
    distances: List[float] = Field(..., description="Distances to nearest neighbors")

@app.on_event("startup")
async def load_index():
    """Load Faiss index into memory on startup"""
    global index
    try:
        logger.info("Loading Faiss index from 'index.faiss'...")
        index = faiss.read_index('index.faiss')
        
        # Set search-time parameter for HNSW
        if hasattr(index, 'hnsw'):
            index.hnsw.efSearch = 64  # Trade-off between speed and recall
        
        logger.info(f"✓ Index loaded successfully: {index.ntotal:,} vectors")
        logger.info(f"✓ Index type: {type(index).__name__}")
        
    except Exception as e:
        logger.error(f"Failed to load index: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "VectorWise",
        "status": "healthy",
        "vectors_indexed": index.ntotal if index else 0
    }

@app.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    """
    Perform k-NN search on the Faiss index.
    
    Args:
        request: SearchRequest containing query_vector and k
        
    Returns:
        SearchResult with indices and distances of top-k neighbors
    """
    if index is None:
        raise HTTPException(status_code=503, detail="Index not loaded")
    
    # Validate query vector dimension
    if len(request.query_vector) != DIM:
        raise HTTPException(
            status_code=400,
            detail=f"Query vector must have dimension {DIM}, got {len(request.query_vector)}"
        )
    
    try:
        # Convert query to numpy array and reshape
        query = np.array(request.query_vector, dtype='float32').reshape(1, -1)
        
        # Normalize query vector (must match training normalization)
        faiss.normalize_L2(query)
        
        # Perform search
        distances, indices = index.search(query, request.k)
        
        # Convert to lists for JSON serialization
        return SearchResult(
            indices=indices[0].tolist(),
            distances=distances[0].tolist()
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get index statistics"""
    if index is None:
        raise HTTPException(status_code=503, detail="Index not loaded")
    
    stats = {
        "total_vectors": index.ntotal,
        "dimension": DIM,
        "index_type": type(index).__name__
    }
    
    if hasattr(index, 'hnsw'):
        stats["hnsw_m"] = index.hnsw.max_level
        stats["hnsw_efSearch"] = index.hnsw.efSearch
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
