#!/bin/bash

# VectorWise Quick Start Script
# This script sets up and runs the entire VectorWise system

set -e  # Exit on error

echo "============================================================"
echo "VectorWise - Quick Start Setup"
echo "============================================================"

# Step 1: Check Python installation
echo ""
echo "[Step 1/4] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Step 2: Install Python dependencies
echo ""
echo "[Step 2/4] Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Step 3: Generate data and build index
echo ""
echo "[Step 3/4] Generating data and building Faiss index..."
echo "This will take a few minutes..."
if [ -f "generate_data.py" ]; then
    python3 generate_data.py
    echo "✓ Data generation complete"
else
    echo "❌ generate_data.py not found"
    exit 1
fi

# Step 4: Check for Docker
echo ""
echo "[Step 4/4] Checking Docker installation..."
if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo "✓ Docker found"
    echo ""
    echo "============================================================"
    echo "Setup Complete! 🎉"
    echo "============================================================"
    echo ""
    echo "To start the service, run:"
    echo "  $ docker-compose up --build -d"
    echo ""
    echo "Or run locally without Docker:"
    echo "  $ uvicorn api.main:app --reload"
    echo ""
    echo "Then test the API:"
    echo "  $ python3 test_api.py"
    echo ""
    echo "Run benchmarks:"
    echo "  $ python3 benchmark.py"
    echo ""
else
    echo "⚠️  Docker not found. You can still run locally:"
    echo "  $ uvicorn api.main:app --reload"
fi

echo "============================================================"
