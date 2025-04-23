# tests/test_model_and_errors.py
"""
High-level tests focused on functionality rather than implementation details.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from a2a_json_rpc.models import Request, Response
from a2a_json_rpc.json_rpc_errors import (
    ParseError, InvalidRequestError, MethodNotFoundError, InternalError
)
from a2a_json_rpc.a2a_errors import TaskNotFoundError, TaskNotCancelableError

from a2a_json_rpc.protocol import JSONRPCProtocol


def test_request_missing_method_raises_validation_error():
    """Test that a Request without method raises validation error."""
    with pytest.raises(ValidationError):
        Request(id=123)


def test_response_missing_id_raises_validation_error():
    """Test that a Response without id raises validation error."""
    with pytest.raises(ValidationError):
        Response(result={"status": "success"})


def test_models_round_trip():
    """Test models can be serialized and deserialized."""
    # Create a request
    request = Request(
        id=123,
        method="test_method",
        params={"param1": "value1"}
    )
    
    # Serialize to dict
    request_dict = request.model_dump(exclude_none=True)
    
    # Deserialize back to Request
    request2 = Request.model_validate(request_dict)
    
    # Compare
    assert request2.id == request.id
    assert request2.method == request.method
    assert request2.params == request.params
    
    # Same for Response
    response = Response(
        id=123,
        result={"status": "success"}
    )
    
    response_dict = response.model_dump()
    response2 = Response.model_validate(response_dict)
    
    assert response2.id == response.id
    assert response2.result == response.result


def test_parse_error_to_dict():
    """Test ParseError to_dict method."""
    error = ParseError("Test parse error")
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32700
    assert error_dict["message"] == "Test parse error"
    # Data field is only included when not None
    assert "data" not in error_dict or error_dict["data"] is None


def test_invalid_request_error_with_data():
    """Test InvalidRequestError with data."""
    data = {"field": "value", "details": "Some details"}
    error = InvalidRequestError("Invalid request", data=data)
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32600
    assert error_dict["message"] == "Invalid request"
    assert error_dict["data"] == data


def test_method_not_found_error_defaults():
    """Test MethodNotFoundError with default message."""
    error = MethodNotFoundError()
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32601
    assert "not found" in error_dict["message"].lower() or "method" in error_dict["message"].lower()


def test_internal_error_and_data():
    """Test InternalError with data."""
    data = {"trace": "Error details"}
    error = InternalError("Internal server error", data=data)
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32603
    assert error_dict["message"] == "Internal server error"
    assert error_dict["data"] == data


def test_a2a_task_errors():
    """Test A2A-specific task errors."""
    error = TaskNotFoundError("Task not found", data={"id": "task-123"})
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32001
    assert "not found" in error_dict["message"].lower()
    assert error_dict["data"] == {"id": "task-123"}
    
    error = TaskNotCancelableError("Task cannot be canceled", data={"id": "task-456"})
    error_dict = error.to_dict()
    
    assert error_dict["code"] == -32002
    assert "cancel" in error_dict["message"].lower()
    assert error_dict["data"] == {"id": "task-456"}


def test_create_request_and_notification():
    """Test creating JSON-RPC request and notification objects."""
    protocol = JSONRPCProtocol()
    
    # Request with auto-generated ID
    request = protocol.create_request("test_method", {"param": "value"})
    assert request["jsonrpc"] == "2.0"
    assert request["method"] == "test_method"
    assert request["params"] == {"param": "value"}
    assert isinstance(request["id"], int)
    
    # Request with specific ID
    request = protocol.create_request("test_method", {"param": "value"}, id="custom-id")
    assert request["jsonrpc"] == "2.0"
    assert request["method"] == "test_method"
    assert request["params"] == {"param": "value"}
    assert request["id"] == "custom-id"
    
    # Notification (no ID)
    notification = protocol.create_notification("test_event", {"event": "value"})
    assert notification["jsonrpc"] == "2.0"
    assert notification["method"] == "test_event"
    assert notification["params"] == {"event": "value"}
    assert "id" not in notification


def test_protocol_batch_not_supported():
    """Test that batch requests are not supported."""
    protocol = JSONRPCProtocol()
    result = protocol.handle_raw([
        {"jsonrpc": "2.0", "id": 1, "method": "test1", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "test2", "params": {}}
    ])
    
    assert result is not None
    assert "error" in result
    assert result["error"]["code"] == -32600  # Invalid request