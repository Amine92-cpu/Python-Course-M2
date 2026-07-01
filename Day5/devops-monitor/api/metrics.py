# api/metrics.py
import psutil


def get_system_metrics() -> dict:
    """Return a non-blocking snapshot of CPU, memory and disk usage.

    Uses interval=None for cpu_percent to avoid blocking the event loop.

    Returns:
        dict with keys: cpu_percent, memory_percent, disk_percent,
        memory_total_gb, memory_used_gb, disk_total_gb, disk_used_gb
    """
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": cpu,
        "memory_percent": mem.percent,
        "memory_total_gb": round(mem.total / (1024 ** 3), 2),
        "memory_used_gb": round(mem.used / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
    }
