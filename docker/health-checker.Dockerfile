# System Health Checker - Production Dockerfile
# Author: Joshua
# Description: Multi-stage build for minimal container size

# Stage 1: Builder
FROM python:3.11-slim as builder

LABEL maintainer="Joshua"
LABEL description="DevOps System Health Checker"
LABEL version="2.0"

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY scripts/python/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY scripts/python/system_health_checker_v2.py .
COPY scripts/python/config.example.json ./config.json

# Create directories for reports and logs
RUN mkdir -p /app/reports /app/logs

# Add Python packages to PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python system_health_checker_v2.py --quiet || exit 1

# Default command
CMD ["python", "system_health_checker_v2.py"]
