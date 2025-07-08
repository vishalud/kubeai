import pytest
from unittest.mock import patch, MagicMock
from src.models import IntentModel, PodStatusModel
from src.nlp_core import get_intent, generate_response

@patch('src.nlp_core.GenerativeModel')
def test_get_intent_valid(mock_model):
    # Mock Gemini response with valid JSON
    mock_response = MagicMock()
    mock_response.text = '{"intent": "get_pod_status", "entities": [{"type": "namespace", "value": "default"}]}'
    mock_model.return_value.generate_content.return_value = mock_response
    result = get_intent("show me pods in default")
    assert result.intent == "get_pod_status"
    assert result.entities[0].type == "namespace"
    assert result.entities[0].value == "default"

@patch('src.nlp_core.GenerativeModel')
def test_get_intent_malformed_json(mock_model):
    # Mock Gemini response with no JSON
    mock_response = MagicMock()
    mock_response.text = 'No JSON here!'
    mock_model.return_value.generate_content.return_value = mock_response
    with pytest.raises(ValueError, match="Failed to get intent from Gemini: No JSON found"):
        get_intent("invalid response")

@patch('src.nlp_core.GenerativeModel')
def test_get_intent_invalid_model(mock_model):
    # Mock Gemini response with invalid JSON for IntentModel
    mock_response = MagicMock()
    mock_response.text = '{"intent": 123, "entities": "notalist"}'
    mock_model.return_value.generate_content.return_value = mock_response
    with pytest.raises(ValueError, match="Failed to get intent"):
        get_intent("bad model data")

@patch('src.nlp_core.GenerativeModel')
def test_get_intent_api_error(mock_model):
    # Simulate Gemini API error
    mock_model.return_value.generate_content.side_effect = Exception("API error")
    with pytest.raises(ValueError, match="Failed to get intent"):
        get_intent("api error")

@patch('src.nlp_core.GenerativeModel')
def test_generate_response_serialization(mock_model):
    data = [PodStatusModel(name="nginx", namespace="default", status="Running", restarts=2, containers=[{"name": "nginx", "image": "nginx:1.14.2"}])]
    mock_response = MagicMock()
    mock_response.text = "summary"
    mock_model.return_value.generate_content.return_value = mock_response
    result = generate_response(data)
    assert result == "summary"

@patch('src.nlp_core.GenerativeModel')
def test_generate_response_prompt(mock_model):
    data = [PodStatusModel(name="nginx", namespace="default", status="Running", restarts=2, containers=[{"name": "nginx", "image": "nginx:1.14.2"}])]
    mock_response = MagicMock()
    mock_response.text = "summary"
    mock_model.return_value.generate_content.return_value = mock_response
    result = generate_response(data)
    assert result == "summary"

@patch('src.nlp_core.GenerativeModel')
def test_generate_response_success(mock_model):
    mock_response = MagicMock()
    mock_response.text = "There is 1 pod named nginx running in default."
    mock_model.return_value.generate_content.return_value = mock_response
    data = [PodStatusModel(name="nginx", namespace="default", status="Running", restarts=2, containers=[{"name": "nginx", "image": "nginx:1.14.2"}])]
    result = generate_response(data)
    assert "nginx" in result

@patch('src.nlp_core.GenerativeModel')
def test_generate_response_empty_list(mock_model):
    mock_response = MagicMock()
    mock_response.text = "No resources found."
    mock_model.return_value.generate_content.return_value = mock_response
    result = generate_response([])
    assert result == "No resources found."

@patch('src.nlp_core.GenerativeModel')
def test_generate_response_gemini_error(mock_model):
    mock_model.return_value.generate_content.side_effect = Exception("API error")
    data = [PodStatusModel(name="nginx", namespace="default", status="Running", restarts=2, containers=[{"name": "nginx", "image": "nginx:1.14.2"}])]
    with pytest.raises(ValueError, match="Failed to generate summary from Gemini: API error"):
        generate_response(data) 