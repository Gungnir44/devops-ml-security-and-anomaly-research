# DevOps Toolbox - System Health Checker Container
# Author: Joshua
# Description: Containerized system monitoring tool

# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="Joshua"
LABEL description="DevOps system health monitoring container"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ../scripts/python/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY ../scripts/python/system_health_checker.py .

# Create output directory for reports
RUN mkdir -p /app/reports

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the health checker
CMD ["python", "system_health_checker.py"]
