# syntax=docker/dockerfile:1.7
# -----------------------------------------------------------------------------
# Build stage: install deps and run tests
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt requirements-dev.txt ./

# Build wheels for all dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# Copy source and run tests
COPY . .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt && \
    pytest -q

# -----------------------------------------------------------------------------
# Runtime stage: minimal production image
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# Security: set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install curl for healthcheck and create non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app \
    && chown -R app:app /app

# Copy wheels from build stage and install
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application code
COPY --chown=app:app . .

# Remove unnecessary files in runtime
RUN rm -rf tests/ requirements-dev.txt .pytest_cache/ __pycache__/ .git/

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
