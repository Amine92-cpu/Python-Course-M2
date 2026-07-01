# tests/test_metrics.py
"""Unit tests for the system metrics module."""
import pytest
from api.metrics import get_system_metrics


def test_metrics_returns_dict():
    """get_system_metrics() must return a dict."""
    result = get_system_metrics()
    assert isinstance(result, dict)


def test_metrics_has_required_keys():
    """All expected keys must be present in the metrics snapshot."""
    result = get_system_metrics()
    required_keys = {
        "cpu_percent",
        "memory_percent",
        "memory_total_gb",
        "memory_used_gb",
        "disk_percent",
        "disk_total_gb",
        "disk_used_gb",
    }
    assert required_keys.issubset(result.keys()), (
        f"Missing keys: {required_keys - result.keys()}"
    )


def test_cpu_percent_in_range():
    """CPU percent must be between 0 and 100."""
    result = get_system_metrics()
    assert 0.0 <= result["cpu_percent"] <= 100.0


def test_memory_percent_in_range():
    """Memory percent must be between 0 and 100."""
    result = get_system_metrics()
    assert 0.0 <= result["memory_percent"] <= 100.0


def test_disk_percent_in_range():
    """Disk percent must be between 0 and 100."""
    result = get_system_metrics()
    assert 0.0 <= result["disk_percent"] <= 100.0


def test_memory_used_not_exceed_total():
    """Used memory must not exceed total memory."""
    result = get_system_metrics()
    assert result["memory_used_gb"] <= result["memory_total_gb"]


def test_disk_used_not_exceed_total():
    """Used disk space must not exceed total disk space."""
    result = get_system_metrics()
    assert result["disk_used_gb"] <= result["disk_total_gb"]
