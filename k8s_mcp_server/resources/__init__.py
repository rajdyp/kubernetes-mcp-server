"""Kubernetes resource modules"""

from .pods import get_pods_tool, PodInfo

__all__ = [
    "get_pods_tool",
    "PodInfo",
]