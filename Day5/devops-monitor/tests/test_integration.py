# tests/test_integration.py
"""
Integration tests — run against a live container or a local server.

Usage (via Makefile):
    make integration-test

The base URL is read from the INT_BASE_URL environment variable.
Default: http://localhost:8000 (matches docker-compose setup).
"""
import os
import pytest
import httpx

BASE_URL = os.getenv("INT_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "test-secret-key")


@pytest.fixture(scope="module")
def api():
    """Synchronous HTTP client pointed at the live API."""
    with httpx.Client(base_url=BASE_URL, timeout=10) as client:
        yield client


def test_integration_health(api):
    """The live API /health endpoint must return status ok."""
    response = api.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_integration_metrics(api):
    """The live API /metrics endpoint must return system metrics."""
    response = api.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "disk_percent" in data


def test_integration_auth_required(api):
    """POST /servers without API key must be refused (403)."""
    response = api.post(
        "/servers",
        json={"name": "test", "host": "localhost", "port": 8080},
    )
    assert response.status_code == 403


def test_integration_full_crud(api):
    """Full lifecycle: register, list, get, delete a server."""
    # Register
    resp = api.post(
        "/servers",
        json={"name": "integration-server", "host": "httpbin.org", "port": 443},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.status_code == 201
    server_id = resp.json()["id"]

    # List — server must appear
    list_resp = api.get("/servers")
    ids = [s["id"] for s in list_resp.json()]
    assert server_id in ids

    # Get by ID
    get_resp = api.get(f"/servers/{server_id}")
    assert get_resp.status_code == 200

    # Delete
    del_resp = api.delete(
        f"/servers/{server_id}",
        headers={"X-API-Key": API_KEY},
    )
    assert del_resp.status_code == 204

    # Confirm deletion
    confirm = api.get(f"/servers/{server_id}")
    assert confirm.status_code == 404
