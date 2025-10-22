"""Kubernetes client configuration and utilities"""
from functools import lru_cache
from typing import Optional
 
from kubernetes import client, config

from .config import logger


@lru_cache
def get_core_v1_api(context: Optional[str] = None) -> client.CoreV1Api:
    """Loads kubeconfig and returns an initialized CoreV1Api client."""
    logger.debug(f"Loading kubeconfig for context: {context or 'current'}")
    config.load_kube_config(context=context)
    return client.CoreV1Api()


@lru_cache
def get_apps_v1_api(context: Optional[str] = None) -> client.AppsV1Api:
    """Loads kubeconfig and returns an initialized AppsV1Api client."""
    logger.debug(f"Loading kubeconfig for context: {context or 'current'}")
    config.load_kube_config(context=context)
    return client.AppsV1Api()


def get_identity(context: Optional[str] = None) -> str:
    """
    Get current Kubernetes identity from the loaded kubeconfig.

    Args:
        context: The kubeconfig context to check.

    Returns:
        String describing current context and user.
    """
    try:
        contexts, active_context = config.list_kube_config_contexts()

        # If a specific context is requested, find it in the contexts list
        if context:
            for ctx in contexts:
                if ctx.get("name") == context:
                    active_context = ctx
                    break

        if not active_context:
            return "context=n/a, user=n/a"
        context_name = active_context.get("name", "n/a")
        user_name = active_context.get("context", {}).get("user", "n/a")
        return f"context={context_name}, user={user_name}"
    except config.ConfigException as e:
        logger.error(f"Failed to determine identity for context '{context}': {e}")
        return f"context={context or 'unknown'}, user=unknown"