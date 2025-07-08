from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from src.models import IntentModel, EntityModel, PodStatusModel, PodImageModel
from pydantic import BaseModel
from kubernetes.client.rest import ApiException
from typing import List, Type

class KubeconfigError(Exception):
    """Raised when the Kubernetes configuration cannot be loaded."""
    pass

class CommandExecutionError(Exception):
    """Raised when a command execution fails due to API or input error."""
    pass

class KubernetesClient:
    """
    Manages Kubernetes API client initialization using local kubeconfig.
    Provides access to CoreV1Api and AppsV1Api clients.
    """
    def __init__(self):
        try:
            config.load_kube_config()
        except ConfigException as e:
            raise KubeconfigError(f"Failed to load kubeconfig: {e}")

    def get_core_v1_api(self):
        """Returns a CoreV1Api client instance."""
        return client.CoreV1Api()

    def get_apps_v1_api(self):
        """Returns an AppsV1Api client instance."""
        return client.AppsV1Api()

# Command map: intent string -> handler function
COMMAND_MAP = {}

def execute_command(intent: IntentModel) -> List[BaseModel]:
    """
    Maps intent to handler and executes the corresponding Kubernetes command.
    Handles API and input errors robustly.
    """
    handler = COMMAND_MAP.get(intent.intent)
    if handler is None:
        raise NotImplementedError(f"No handler implemented for intent: {intent.intent}")
    try:
        return handler(intent.entities)
    except (ApiException, ValueError) as e:
        # Log error, return empty list or raise custom error
        # print(f"Command execution error: {e}")
        raise CommandExecutionError(f"Failed to execute command for intent '{intent.intent}': {e}")

def _extract_parameters(entities: List[EntityModel], required_params: List[str]) -> dict:
    """
    Extracts required parameters from entities. Raises ValueError if required param missing.
    Defaults 'namespace' to 'default' if not provided.
    """
    param_map = {e.type: e.value for e in entities}
    params = {}
    for key in required_params:
        if key == 'namespace':
            params[key] = param_map.get('namespace', 'default')
        elif key in param_map:
            params[key] = param_map[key]
        else:
            raise ValueError(f"Missing required parameter: {key}")
    return params 

def _handle_get_pod_status(entities: List[EntityModel]) -> list:
    """
    Handler for 'get_pod_status' intent. Returns list of PodStatusModel.
    Handles API errors and input validation.
    """
    params = _extract_parameters(entities, ["namespace"])
    k8s = KubernetesClient()
    api = k8s.get_core_v1_api()
    try:
        pod_list = api.list_namespaced_pod(namespace=params["namespace"])
    except ApiException as e:
        # print(f"Kubernetes API error: {e}")
        raise
    result = []
    for item in pod_list.items:
        restarts = 0
        containers = []
        if hasattr(item.status, "container_statuses") and item.status.container_statuses:
            restarts = sum(cs.restart_count for cs in item.status.container_statuses if hasattr(cs, "restart_count"))
            # Extract container information
            for container in item.spec.containers:
                containers.append({
                    "name": container.name,
                    "image": container.image
                })
        result.append(PodStatusModel(
            name=item.metadata.name,
            namespace=item.metadata.namespace,
            status=item.status.phase,
            restarts=restarts,
            containers=containers
        ))
    return result

def _handle_get_pod_images(entities: List[EntityModel]) -> list:
    """
    Handler for 'get_pod_images' intent. Returns list of PodImageModel.
    """
    params = _extract_parameters(entities, ["namespace"])
    k8s = KubernetesClient()
    api = k8s.get_core_v1_api()
    try:
        pod_list = api.list_namespaced_pod(namespace=params["namespace"])
    except ApiException as e:
        raise
    result = []
    for item in pod_list.items:
        containers = []
        if hasattr(item.spec, "containers") and item.spec.containers:
            for container in item.spec.containers:
                containers.append({
                    "name": container.name,
                    "image": container.image
                })
        result.append(PodImageModel(
            name=item.metadata.name,
            namespace=item.metadata.namespace,
            containers=containers
        ))
    return result

# Register handler in command map
COMMAND_MAP["get_pod_status"] = _handle_get_pod_status
COMMAND_MAP["get_pod_images"] = _handle_get_pod_images 