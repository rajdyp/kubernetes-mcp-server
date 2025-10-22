#!/usr/bin/env python3
"""MCP server entry point with kubectl tools"""
from typing import Optional

from fastmcp import FastMCP
from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException

from .config import DEFAULT_NAMESPACE, logger
from .client import get_core_v1_api, get_identity
from .resources import get_pods_tool

# Initialize MCP server
mcp = FastMCP("tiny-k8s-mcp-server")


@mcp.tool()
def health_check(context: Optional[str] = None) -> str:
    """
    Verify kubectl access and return cluster information

    Args:
        context: Optional kubeconfig context to use

    Returns:
        Health check status and cluster info
    """
    try:
        # Get a configured API client. This will raise an exception on failure.
        api = get_core_v1_api(context=context)

        # Get the Kubernetes server version to confirm connectivity
        version_info = api.get_code()
        server_version = version_info.git_version

        # Get current identity from kubeconfig
        identity = get_identity(context=context)

        return (
            f"✓ Health Check Passed\n\n"
            f"Successfully connected to Kubernetes API server.\n"
            f"Server Version: {server_version}\n"
            f"Identity: {identity}"
        )
    except (ApiException, ConfigException) as e:
        return f"✗ Health check failed: Could not connect to Kubernetes.\nError: {e}"
    except Exception as e:
        logger.exception("Health check failed")
        return f"✗ Health check failed: {e}"


@mcp.tool()
def get_pods(
    namespace: str = DEFAULT_NAMESPACE, 
    all_namespaces: bool = False, 
    context: Optional[str] = None
) -> str:
    """
    Get pods from Kubernetes with detailed information
    
    Args:
        namespace: Namespace to query (ignored if all_namespaces=True)
        all_namespaces: If True, list across all namespaces (requires ClusterRole)
        context: Optional kubeconfig context to use
        
    Returns:
        Formatted string with pod information or error message
    """
    return get_pods_tool(namespace, all_namespaces, context)


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()