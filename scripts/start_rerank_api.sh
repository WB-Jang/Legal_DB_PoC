#!/bin/bash

# Script to start the rerank API server
# Usage: ./scripts/start_rerank_api.sh

echo "Starting Rerank API Server on port 8082..."
echo "Make sure you have activated the Poetry environment or are running inside Docker"
echo ""

# Check if running in poetry environment
if command -v poetry &> /dev/null; then
    echo "Using Poetry to run the server..."
    poetry run uvicorn app.rerank_api:app --host 0.0.0.0 --port 8082
else
    echo "Using system Python to run the server..."
    uvicorn app.rerank_api:app --host 0.0.0.0 --port 8082
fi
