from typing import List, Dict, Any
from pydantic import BaseModel

class EntityModel(BaseModel):
    """
    Represents an extracted entity from user input.
    Attributes:
        type (str): The type/category of the entity (e.g., 'namespace', 'pod').
        value (str): The value of the entity (e.g., 'default', 'nginx-pod').
    """
    type: str
    value: str

class IntentModel(BaseModel):
    """
    Represents the recognized intent and associated entities from user input.
    Attributes:
        intent (str): The recognized intent (e.g., 'get_pod_status', 'get_pod_images').
        entities (List[EntityModel]): List of extracted entities.
    """
    intent: str
    entities: List[EntityModel]

class PodStatusModel(BaseModel):
    """
    Represents the status of a Kubernetes Pod.
    Attributes:
        name (str): Pod name.
        namespace (str): Namespace of the pod.
        status (str): Current status (e.g., 'Running').
        restarts (int): Number of restarts.
        containers (List[Dict[str, str]]): List of containers with their images.
    """
    name: str
    namespace: str
    status: str
    restarts: int
    containers: List[Dict[str, str]]

class PodImageModel(BaseModel):
    """
    Represents the image(s) used by a Kubernetes Pod.
    Attributes:
        name (str): Pod name.
        namespace (str): Namespace of the pod.
        containers (List[Dict[str, str]]): List of containers with their images.
    """
    name: str
    namespace: str
    containers: List[Dict[str, str]]

class ConversationState(BaseModel):
    """
    Maintains conversational context for a session.
    Attributes:
        session_id (str): Unique session identifier.
        history (List[Dict[str, Any]]): List of previous interactions (queries, intents, entities, etc.).
    """
    session_id: str
    history: List[Dict[str, Any]] 