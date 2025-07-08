import pytest
from unittest.mock import patch, MagicMock
from kubernetes.config.config_exception import ConfigException
from k8s_client import KubernetesClient, KubeconfigError
from models import IntentModel, EntityModel, PodStatusModel
from pydantic import BaseModel

@patch('k8s_client.config.load_kube_config')
def test_kubernetes_client_init_success(mock_load):
    # Should not raise if kubeconfig loads
    client = KubernetesClient()
    assert isinstance(client, KubernetesClient)

@patch('k8s_client.config.load_kube_config', side_effect=ConfigException("bad config"))
def test_kubernetes_client_init_failure(mock_load):
    # Should raise KubeconfigError if kubeconfig fails
    with pytest.raises(KubeconfigError, match="Failed to load kubeconfig"):
        KubernetesClient()

@patch('k8s_client.config.load_kube_config')
def test_kubernetes_client_api_methods(mock_load):
    client = KubernetesClient()
    # Should return correct types
    from kubernetes.client import CoreV1Api, AppsV1Api
    assert isinstance(client.get_core_v1_api(), CoreV1Api)
    assert isinstance(client.get_apps_v1_api(), AppsV1Api)

def test_execute_command_unknown_intent():
    intent = IntentModel(intent="unknown_intent", entities=[])
    from k8s_client import execute_command
    import pytest
    with pytest.raises(NotImplementedError, match="No handler implemented for intent"):
        execute_command(intent)

def test_extract_parameters_all_present():
    from k8s_client import _extract_parameters
    entities = [EntityModel(type="namespace", value="prod"), EntityModel(type="pod", value="nginx")]
    params = _extract_parameters(entities, ["namespace", "pod"])
    assert params["namespace"] == "prod"
    assert params["pod"] == "nginx"

def test_extract_parameters_missing_required():
    from k8s_client import _extract_parameters
    entities = [EntityModel(type="namespace", value="prod")]
    import pytest
    with pytest.raises(ValueError, match="Missing required parameter: pod"):
        _extract_parameters(entities, ["namespace", "pod"])

def test_extract_parameters_default_namespace():
    from k8s_client import _extract_parameters
    entities = [EntityModel(type="pod", value="nginx")]
    params = _extract_parameters(entities, ["namespace", "pod"])
    assert params["namespace"] == "default"
    assert params["pod"] == "nginx"

def test_handle_get_pod_status_calls_api():
    from k8s_client import _handle_get_pod_status
    entities = [EntityModel(type="namespace", value="test-ns")]
    with patch("k8s_client.KubernetesClient") as mock_client:
        mock_api = MagicMock()
        # Create mock pod objects with required attributes
        mock_pod = MagicMock()
        mock_pod.metadata.name = "nginx"
        mock_pod.metadata.namespace = "test-ns"
        mock_pod.status.phase = "Running"
        cs1 = MagicMock(); cs1.restart_count = 2
        cs2 = MagicMock(); cs2.restart_count = 1
        mock_pod.status.container_statuses = [cs1, cs2]
        mock_pod_list = MagicMock()
        mock_pod_list.items = [mock_pod]
        mock_api.get_core_v1_api.return_value = mock_api
        mock_api.list_namespaced_pod.return_value = mock_pod_list
        mock_client.return_value.get_core_v1_api.return_value = mock_api
        result = _handle_get_pod_status(entities)
        mock_api.list_namespaced_pod.assert_called_once_with(namespace="test-ns")
        assert len(result) == 1
        pod = result[0]
        assert pod.name == "nginx"
        assert pod.namespace == "test-ns"
        assert pod.status == "Running"
        assert pod.restarts == 3

def test_handle_get_pod_status_returns_models():
    from k8s_client import _handle_get_pod_status
    entities = [EntityModel(type="namespace", value="test-ns")]
    with patch("k8s_client.KubernetesClient") as mock_client:
        mock_api = MagicMock()
        # Mock pod item with metadata and status
        mock_pod = MagicMock()
        mock_pod.metadata.name = "nginx"
        mock_pod.metadata.namespace = "test-ns"
        mock_pod.status.phase = "Running"
        cs1 = MagicMock()
        cs1.restart_count = 2
        cs2 = MagicMock()
        cs2.restart_count = 1
        mock_pod.status.container_statuses = [cs1, cs2]
        mock_pod_list = MagicMock()
        mock_pod_list.items = [mock_pod]
        mock_api.get_core_v1_api.return_value = mock_api
        mock_api.list_namespaced_pod.return_value = mock_pod_list
        mock_client.return_value.get_core_v1_api.return_value = mock_api
        result = _handle_get_pod_status(entities)
        assert isinstance(result, list)
        assert isinstance(result[0], PodStatusModel)
        assert result[0].name == "nginx"
        assert result[0].namespace == "test-ns"
        assert result[0].status == "Running"
        assert result[0].restarts == 3

def test_execute_command_valid_intent():
    from k8s_client import execute_command, CommandExecutionError, COMMAND_MAP
    from models import IntentModel, EntityModel, PodStatusModel
    with patch("k8s_client.KubernetesClient") as mock_k8s_client:
        mock_handler = lambda entities: [PodStatusModel(name="nginx", namespace="default", status="Running", restarts=0)]
        COMMAND_MAP["get_pod_status"] = mock_handler
        intent = IntentModel(intent="get_pod_status", entities=[EntityModel(type="namespace", value="default")])
        result = execute_command(intent)
        assert isinstance(result, list)
        assert isinstance(result[0], PodStatusModel)

def test_execute_command_missing_entity():
    from k8s_client import execute_command, CommandExecutionError, COMMAND_MAP
    from models import IntentModel
    with patch("k8s_client.KubernetesClient") as mock_k8s_client:
        def handler(entities):
            raise ValueError("Missing required parameter: namespace")
        COMMAND_MAP["get_pod_status"] = handler
        intent = IntentModel(intent="get_pod_status", entities=[])
        import pytest
        with pytest.raises(CommandExecutionError, match="Missing required parameter"):
            execute_command(intent)

def test_execute_command_api_exception():
    from k8s_client import execute_command, CommandExecutionError, COMMAND_MAP
    from models import IntentModel, EntityModel
    with patch("k8s_client.KubernetesClient") as mock_k8s_client:
        from kubernetes.client.rest import ApiException
        def handler(entities):
            raise ApiException("API error")
        COMMAND_MAP["get_pod_status"] = handler
        intent = IntentModel(intent="get_pod_status", entities=[EntityModel(type="namespace", value="default")])
        import pytest
        with pytest.raises(CommandExecutionError, match="API error"):
            execute_command(intent) 