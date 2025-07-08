import pytest
from pydantic import ValidationError
from src.models import EntityModel, IntentModel, PodStatusModel, ConversationState, PodImageModel

# EntityModel tests
def test_entity_model_valid():
    m = EntityModel(type="namespace", value="default")
    assert m.type == "namespace"
    assert m.value == "default"

def test_entity_model_invalid():
    with pytest.raises(ValidationError):
        EntityModel(type=123, value=None)

# IntentModel tests
def test_intent_model_valid():
    entities = [EntityModel(type="pod", value="nginx")] 
    m = IntentModel(intent="get_pod_status", entities=entities)
    assert m.intent == "get_pod_status"
    assert m.entities[0].type == "pod"

def test_intent_model_invalid():
    with pytest.raises(ValidationError):
        IntentModel(intent=123, entities="notalist")

# PodStatusModel tests
def test_pod_status_model_valid():
    m = PodStatusModel(
        name="nginx",
        namespace="default",
        status="Running",
        restarts=1,
        containers=[{"name": "nginx", "image": "nginx:1.14.2"}]
    )
    assert m.name == "nginx"
    assert m.status == "Running"
    assert m.containers[0]["image"] == "nginx:1.14.2"

def test_pod_status_model_invalid():
    with pytest.raises(ValidationError):
        PodStatusModel(name=123, namespace=None, status=5, restarts="zero")

# ConversationState tests
def test_conversation_state_valid():
    m = ConversationState(session_id="abc123", history=[{"query": "foo"}])
    assert m.session_id == "abc123"
    assert isinstance(m.history, list)

def test_conversation_state_invalid():
    with pytest.raises(ValidationError):
        ConversationState(session_id=123, history="notalist")

# PodImageModel tests
def test_pod_image_model_valid():
    m = PodImageModel(
        name="nginx",
        namespace="default",
        containers=[{"name": "nginx", "image": "nginx:1.14.2"}]
    )
    assert m.name == "nginx"
    assert m.namespace == "default"
    assert m.containers[0]["image"] == "nginx:1.14.2"

def test_pod_image_model_invalid():
    with pytest.raises(ValidationError):
        PodImageModel(name=123, namespace=None, containers="notalist") 