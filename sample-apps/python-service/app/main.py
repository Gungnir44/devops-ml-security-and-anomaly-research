"""
Python Data Processing Service
FastAPI application for ML-based DevOps Security Research
"""
import os
import time
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Initialize FastAPI app
app = FastAPI(
    title="Python Data Processing Service",
    description="Data processing and analytics service for DevOps research",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Pydantic models
class DataPoint(BaseModel):
    """Data point for processing"""
    id: Optional[int] = None
    value: float = Field(..., description="Numeric value to process")
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None

class ProcessingResult(BaseModel):
    """Result of data processing"""
    original_value: float
    processed_value: float
    operation: str
    timestamp: datetime

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    uptime_seconds: float
    environment: str

# Application state
start_time = time.time()

# Middleware for metrics
@app.middleware("http")
async def add_metrics(request, call_next):
    """Add Prometheus metrics to requests"""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

# Routes
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "Python Data Processing Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "metrics": "/metrics",
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        uptime_seconds=uptime,
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.post("/api/v1/process", response_model=ProcessingResult, tags=["Processing"])
async def process_data(data: DataPoint):
    """
    Process a single data point

    - **value**: Numeric value to process
    - **metadata**: Optional metadata dictionary
    """
    # Simple processing: multiply by 2 (placeholder for real processing)
    processed = data.value * 2.0

    return ProcessingResult(
        original_value=data.value,
        processed_value=processed,
        operation="multiply_by_2",
        timestamp=datetime.utcnow()
    )

@app.post("/api/v1/batch-process", response_model=List[ProcessingResult], tags=["Processing"])
async def batch_process(data_points: List[DataPoint]):
    """
    Process multiple data points in batch

    - **data_points**: List of data points to process
    """
    if len(data_points) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum batch size is 100 items"
        )

    results = []
    for point in data_points:
        processed = point.value * 2.0
        results.append(ProcessingResult(
            original_value=point.value,
            processed_value=processed,
            operation="multiply_by_2",
            timestamp=datetime.utcnow()
        ))

    return results

@app.get("/api/v1/analytics/summary", tags=["Analytics"])
async def get_analytics_summary():
    """
    Get analytics summary

    Returns summary statistics (mock data for demonstration)
    """
    return {
        "total_processed": 1523,
        "average_processing_time_ms": 12.5,
        "success_rate": 0.987,
        "last_24h": {
            "processed": 342,
            "errors": 5,
            "avg_value": 45.2
        },
        "timestamp": datetime.utcnow()
    }

@app.get("/metrics", response_class=PlainTextResponse, tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint

    Exposes application metrics in Prometheus format
    """
    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
