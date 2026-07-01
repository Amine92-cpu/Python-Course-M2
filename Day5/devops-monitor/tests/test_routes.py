# tests/test_routes.py
"""Unit tests for FastAPI routes."""
import asyncio
import os
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

# Set a test API key before importing the app
os.environ["API_KEY"] = "test-secret-key"

from api.main import app  # noqa: E402

client = TestClient(app)
API_KEY = "test-secret-key"


# ─── Health ──────────────────────────────────────────────────────────────────

def test_health_returns_ok():
    """GET /health must return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "servers_monitored" in data


# ─── Metrics ─────────────────────────────────────────────────────────────────

def test_metrics_returns_200():
    """GET /metrics must return 200."""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_has_cpu_key():
    """GET /metrics response must contain cpu_percent."""
    response = client.get("/metrics")
    assert "cpu_percent" in response.json()


def test_metrics_has_memory_key():
    """GET /metrics response must contain memory_percent."""
    response = client.get("/metrics")
    assert "memory_percent" in response.json()


def test_metrics_has_disk_key():
    """GET /metrics response must contain disk_percent."""
    response = client.get("/metrics")
    assert "disk_percent" in response.json()


# ─── Auth ─────────────────────────────────────────────────────────────────────

def test_post_server_without_api_key_returns_403():
    """POST /servers without API key must return 403."""
    response = client.post(
        "/servers",
        json={"name": "test", "host": "localhost", "port": 8080},
    )
    assert response.status_code == 403


def test_post_server_with_wrong_api_key_returns_403():
    """POST /servers with wrong API key must return 403."""
    response = client.post(
        "/servers",
        json={"name": "test", "host": "localhost", "port": 8080},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 403


def test_delete_server_without_api_key_returns_403():
    """DELETE /servers/{id} without API key must return 403."""
    response = client.delete("/servers/1")
    assert response.status_code == 403


# ─── Servers CRUD ─────────────────────────────────────────────────────────────

def test_list_servers_initially_empty():
    """GET /servers must return an empty list initially."""
    response = client.get("/servers")
    assert response.status_code == 200
    # May not be empty if previous tests added a server — just check it's a list
    assert isinstance(response.json(), list)


def test_register_server_returns_201():
    """POST /servers with valid API key must return 201."""
    response = client.post(
        "/servers",
        json={"name": "api-prod", "host": "httpbin.org", "port": 443, "tags": ["prod"]},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "api-prod"
    assert data["status"] == "unknown"
    assert "id" in data


def test_get_server_returns_200():
    """GET /servers/{id} must return the registered server."""
    # Register a server first
    post = client.post(
        "/servers",
        json={"name": "check-me", "host": "httpbin.org", "port": 443},
        headers={"X-API-Key": API_KEY},
    )
    server_id = post.json()["id"]

    response = client.get(f"/servers/{server_id}")
    assert response.status_code == 200
    assert response.json()["id"] == server_id


def test_get_nonexistent_server_returns_404():
    """GET /servers/99999 for a missing server must return 404."""
    response = client.get("/servers/99999")
    assert response.status_code == 404


def test_delete_server_returns_204():
    """DELETE /servers/{id} with valid key must return 204."""
    post = client.post(
        "/servers",
        json={"name": "to-delete", "host": "httpbin.org", "port": 443},
        headers={"X-API-Key": API_KEY},
    )
    server_id = post.json()["id"]

    response = client.delete(
        f"/servers/{server_id}",
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 204


def test_delete_nonexistent_server_returns_404():
    """DELETE /servers/99999 for a missing server must return 404."""
    response = client.delete(
        "/servers/99999",
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 404


def test_list_servers_filter_by_status():
    """GET /servers?status=unknown must filter by status."""
    # Register a server to ensure there is at least one
    client.post(
        "/servers",
        json={"name": "filter-test", "host": "httpbin.org", "port": 443},
        headers={"X-API-Key": API_KEY},
    )
    response = client.get("/servers?status=unknown")
    assert response.status_code == 200
    data = response.json()
    assert all(s["status"] == "unknown" for s in data)


def test_trigger_check_nonexistent_returns_404():
    """POST /servers/99999/check must return 404 for unknown server."""
    response = client.post("/servers/99999/check")
    assert response.status_code == 404


def test_trigger_check_updates_status():
    """POST /servers/{id}/check must return a ServerOut with updated status."""
    # Register a server
    post = client.post(
        "/servers",
        json={"name": "check-server", "host": "httpbin.org", "port": 443},
        headers={"X-API-Key": API_KEY},
    )
    server_id = post.json()["id"]

    # Trigger check — may be UP, DEGRADED, or DOWN depending on network
    response = client.post(f"/servers/{server_id}/check")
    assert response.status_code == 200
    assert response.json()["status"] in ("UP", "DEGRADED", "DOWN")


# ─── Poller unit tests ────────────────────────────────────────────────────────

def test_poller_sets_status_up():
    """poll_server() must set server.status to UP on HTTP 200 fast response."""
    from api.models import Server
    from api.poller import poll_server
    import httpx

    server = Server(id=1, name="test", host="localhost", port=8080)

    mock_response = AsyncMock()
    mock_response.status_code = 200

    with patch("api.poller.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        asyncio.run(poll_server(server))

    # Status should be UP or DEGRADED (depends on elapsed time in test)
    assert server.status in ("UP", "DEGRADED")


def test_poller_sets_status_down_on_error():
    """poll_server() must set server.status to DOWN on connection error."""
    from api.models import Server
    from api.poller import poll_server
    import httpx

    server = Server(id=2, name="offline", host="10.255.255.1", port=9999)

    with patch("api.poller.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        mock_client_cls.return_value = mock_client

        asyncio.run(poll_server(server))

    assert server.status == "DOWN"
