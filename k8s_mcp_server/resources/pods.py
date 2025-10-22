"""Pod-specific resource operations"""
from dataclasses import dataclass
from typing import Optional

from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException
 
from ..client import get_core_v1_api, get_identity
from ..config import DEFAULT_NAMESPACE, logger
 
@dataclass
class PodInfo:
    """Structured pod information"""
    name: str
    namespace: str
    phase: str
    node: str
    ready: int
    total: int
    restarts: int


def format_pods_output(pods: list[PodInfo], scope: str, identity: str) -> str:
    """
    Format pod data for display
    
    Args:
        pods: List of PodInfo objects
        scope: Description of query scope
        identity: Current k8s identity
        
    Returns:
        Formatted string output
    """
    if not pods:
        return f"No pods found in {scope}\nIdentity: {identity}"
    
    lines = [f"Pods in {scope}\nIdentity: {identity}\n"]
    
    for pod in pods:
        lines.append(
            f"  • {pod.name} (ns: {pod.namespace})\n"
            f"    Status: {pod.phase} | Node: {pod.node}\n"
            f"    Ready: {pod.ready}/{pod.total} | Restarts: {pod.restarts}"
        )
    
    return "\n".join(lines)


def get_pods_tool(
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
    try:
        # Get a configured API client. This is the "frictionless" part.
        api = get_core_v1_api(context=context)
        identity = get_identity(context=context)

        if all_namespaces:
            pod_list = api.list_pod_for_all_namespaces(watch=False)
            scope = "ALL namespaces"
        else:
            pod_list = api.list_namespaced_pod(namespace, watch=False)
            scope = f"namespace '{namespace}'"

        # Parse the native V1Pod objects into your PodInfo dataclass
        pods = []
        for pod in pod_list.items:
            # Gracefully handle missing container statuses
            container_statuses = pod.status.container_statuses or []
            pods.append(PodInfo(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                phase=pod.status.phase,
                node=pod.spec.node_name or "unscheduled",
                ready=sum(1 for s in container_statuses if s.ready),
                total=len(container_statuses),
                restarts=sum(s.restart_count for s in container_statuses)
            ))
        
        return format_pods_output(pods, scope, identity)

    except ApiException as e:
        # Rich, specific error handling from the K8s API
        # e.g., distinguish between 403 Forbidden and 404 Not Found
        logger.error(f"Kubernetes API error: {e.status} {e.reason}")
        return f"Error: API call failed with status {e.status}: {e.reason}\nBody: {e.body}"
    except ConfigException as e:
        # Handle errors from loading the kubeconfig (e.g., context not found)
        logger.error(f"Kubeconfig error: {e}")
        return f"Error: Could not configure Kubernetes client. {e}"
    except Exception as e:
        # Catch-all for other unexpected errors
        logger.exception("An unexpected error occurred in get_pods_tool")
        return f"An unexpected error occurred: {e}"