#!/usr/bin/env bash
# Test script for containerized ML model serving
# Builds, runs, tests, and cleans up the container

set -e

CONTAINER_NAME="airs-test"
IMAGE_NAME="airs-mlops-lab:test"
PORT=8080

echo "=== Container Test Script ==="
echo ""

# Step 1: Build the container
echo "Step 1: Building container..."
docker build -t ${IMAGE_NAME} .
echo "Build complete."
echo ""

# Step 2: Clean up any existing container with the same name
echo "Step 2: Cleaning up any existing container..."
docker rm -f ${CONTAINER_NAME} 2>/dev/null || true
echo ""

# Step 3: Run the container
echo "Step 3: Running container..."
docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}
echo "Container started."
echo ""

# Step 4: Wait for startup (model loading takes time)
echo "Step 4: Waiting for startup (30 seconds for model loading)..."
sleep 30
echo ""

# Step 5: Test /health endpoint
echo "Step 5: Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:${PORT}/health)
echo "Response: ${HEALTH_RESPONSE}"
if echo "${HEALTH_RESPONSE}" | grep -q '"status":"healthy"'; then
    echo "Health check: PASSED"
else
    echo "Health check: FAILED"
    docker logs ${CONTAINER_NAME}
    docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
    exit 1
fi
echo ""

# Step 6: Test /predict endpoint
echo "Step 6: Testing /predict endpoint..."
PREDICT_RESPONSE=$(curl -s -X POST http://localhost:${PORT}/predict \
    -H "Content-Type: application/json" \
    -d '{"texts": ["I love this!"]}')
echo "Response: ${PREDICT_RESPONSE}"
if echo "${PREDICT_RESPONSE}" | grep -q '"label":"POSITIVE"'; then
    echo "Predict check: PASSED"
else
    echo "Predict check: FAILED"
    docker logs ${CONTAINER_NAME}
    docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
    exit 1
fi
echo ""

# Step 7: Stop and remove container
echo "Step 7: Stopping and removing container..."
docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}
echo ""

echo "=== All tests PASSED ==="
exit 0
