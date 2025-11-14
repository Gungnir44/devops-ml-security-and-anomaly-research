# Simple Web Dashboard for Health Reports
# Author: Joshua
# Description: Flask-based dashboard to view health check reports

FROM python:3.11-slim

LABEL maintainer="Joshua"
LABEL description="Health Checker Web Dashboard"

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Copy dashboard application
COPY docker/dashboard/ .

# Create reports directory
RUN mkdir -p /app/reports

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]
