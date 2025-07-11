import json
from typing import Any, List
from google.generativeai import GenerativeModel
from src.models import IntentModel, PodStatusModel, PodImageModel
from pydantic import BaseModel

# You will need to set your Gemini API key in the environment as per google-generativeai docs
# Example: os.environ["GOOGLE_API_KEY"] = "..."

def get_intent(query: str) -> IntentModel:
    """
    Uses Gemini API to extract intent and entities from a natural language query.
    Returns a validated IntentModel.
    Raises ValueError on API or validation errors.
    """
    # Construct prompt for Gemini with explicit few-shot examples and strict instructions
    prompt = (
        "You are an intent recognition engine for a Kubernetes CLI. "
        "Given a user query, extract the intent and entities. "
        "Return a JSON object with: "
        "'intent': <intent_name>, 'entities': [ { 'type': <entity_type>, 'value': <entity_value> }, ... ]\n"
        "\n"
        "Only use the following supported intent names: 'get_pod_status', 'get_pod_images'.\n"
        "If the user asks to list, show, or get pods and their status, use intent: 'get_pod_status'.\n"
        "If the user asks about pod images, container images, or what images are running, use intent: 'get_pod_images'.\n"
        "\n"
        "Examples:\n"
        "User query: 'List all pods'\n"
        "Response: {\"intent\": \"get_pod_status\", \"entities\": [{\"type\": \"resource_type\", \"value\": \"pods\"}]}\n"
        "User query: 'Show pods in default namespace'\n"
        "Response: {\"intent\": \"get_pod_status\", \"entities\": [{\"type\": \"namespace\", \"value\": \"default\"}]}\n"
        "User query: 'Get pod images'\n"
        "Response: {\"intent\": \"get_pod_images\", \"entities\": [{\"type\": \"resource_type\", \"value\": \"pods\"}]}\n"
        "User query: 'What images are the pods using in the default namespace?'\n"
        "Response: {\"intent\": \"get_pod_images\", \"entities\": [{\"type\": \"namespace\", \"value\": \"default\"}]}\n"
        "User query: 'Which container images are running?'\n"
        "Response: {\"intent\": \"get_pod_images\", \"entities\": [{\"type\": \"resource_type\", \"value\": \"pods\"}]}\n"
        "\n"
        f"User query: '{query}'"
    )
    model = GenerativeModel("models/gemini-2.5-pro-preview-03-25")
    try:
        response = model.generate_content(prompt)
        # Gemini may return text, not JSON; extract JSON part
        text = response.text.strip()
        # Try to find JSON in the response
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        if json_start == -1 or json_end == -1:
            raise ValueError(f"No JSON found in Gemini response: {text}")
        json_str = text[json_start:json_end]
        data = json.loads(json_str)
        return IntentModel(**data)
    except Exception as e:
        raise ValueError(f"Failed to get intent from Gemini: {e}")

def generate_response(data: List[BaseModel]) -> str:
    """
    Generates a natural language summary from a list of pydantic models using the Gemini API.
    If the data is a list of PodImageModel, returns a concise summary of pod images only.
    """
    if data and isinstance(data[0], PodImageModel):
        # Directly generate a concise summary for images
        lines = []
        for pod in data:
            if not pod.containers:
                continue
            for container in pod.containers:
                lines.append(
                    f"Pod **{pod.name}** (namespace `{pod.namespace}`): container `{container['name']}` uses image `{container['image']}" )
        return "\n".join(lines) if lines else "No images found in the listed pods."
    # Default: use Gemini for other model types
    serializable = [item.dict() for item in data]
    data_json = json.dumps(serializable, indent=2)
    prompt = (
        "You are a Kubernetes assistant. Given the following structured data, "
        "summarize it in clear, user-friendly natural language. "
        "Include container names and images in your summary. "
        "If the list is empty, say 'No resources found.'\n"
        "Data:\n" + data_json
    )
    try:
        model = GenerativeModel("models/gemini-2.5-pro-preview-03-25")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise ValueError(f"Failed to generate summary from Gemini: {e}") 