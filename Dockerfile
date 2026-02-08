# Multi-stage Dockerfile for ML model serving
# Stage 1: Build dependencies with uv
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set up working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# ARG for authenticated AIRS PyPI URL (passed at build time, not persisted in image)
ARG AIRS_PYPI_URL

# Create virtual environment and install dependencies
# Configure uv to use AIRS private PyPI for model-security packages
RUN uv venv /app/.venv && \
    if [ -n "$AIRS_PYPI_URL" ]; then \
      uv sync --frozen --no-dev --no-install-project --extra-index-url "$AIRS_PYPI_URL"; \
    else \
      uv sync --frozen --no-dev --no-install-project; \
    fi

# Stage 2: Runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ /app/src/

# Set up Python path and activate venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1

# No model download needed - app calls Vertex AI endpoint for inference

# Expose Cloud Run default port
EXPOSE 8080

# Run uvicorn with host 0.0.0.0 and PORT env var (Cloud Run sets this)
# Default to 8080 if PORT not set
CMD ["sh", "-c", "uvicorn airs_mlops_lab.serving.server:app --host 0.0.0.0 --port ${PORT:-8080}"]
