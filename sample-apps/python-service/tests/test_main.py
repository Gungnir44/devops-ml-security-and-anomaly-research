"""Tests for the Python Data Processing Service"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Python Data Processing Service"
        assert data["status"] == "running"

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime_seconds" in data

@pytest.mark.asyncio
async def test_process_data():
    """Test single data processing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {"value": 10.0}
        response = await client.post("/api/v1/process", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["original_value"] == 10.0
        assert data["processed_value"] == 20.0
        assert data["operation"] == "multiply_by_2"

@pytest.mark.asyncio
async def test_batch_process():
    """Test batch data processing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = [
            {"value": 5.0},
            {"value": 10.0},
            {"value": 15.0}
        ]
        response = await client.post("/api/v1/batch-process", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["processed_value"] == 10.0
        assert data[1]["processed_value"] == 20.0
        assert data[2]["processed_value"] == 30.0

@pytest.mark.asyncio
async def test_batch_process_size_limit():
    """Test batch processing size limit"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create batch larger than limit (100)
        payload = [{"value": float(i)} for i in range(101)]
        response = await client.post("/api/v1/batch-process", json=payload)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_analytics_summary():
    """Test analytics summary endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_processed" in data
        assert "average_processing_time_ms" in data
        assert "success_rate" in data
        assert "last_24h" in data

@pytest.mark.asyncio
async def test_metrics():
    """Test Prometheus metrics endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/metrics")
        assert response.status_code == 200
        assert "http_requests_total" in response.text
