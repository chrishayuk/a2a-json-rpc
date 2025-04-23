# tests/protocol_formats/test_task_formats.py
"""
Tests for A2A Task operation formats based on the specification.

This file contains tests that validate the request and response formats
for various task operations (send, get, cancel) as defined in the A2A specification.
"""
import pytest
import json
from datetime import datetime
from uuid import uuid4

from a2a_json_rpc.protocol import JSONRPCProtocol
from a2a_json_rpc.models import Request, Response


# Helper function to generate UUIDs for tests
def generate_uuid():
    return str(uuid4())


class TestSendTaskFormat:
    """Test the Send Task format."""

    def test_send_task_request_format(self):
        """Test the send task request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/send",
            "params": {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "type": "text",
                        "text": "tell me a joke"
                    }]
                },
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/send"
        assert "params" in request
        assert "id" in request["params"]
        assert "message" in request["params"]
        assert "role" in request["params"]["message"]
        assert "parts" in request["params"]["message"]
        assert len(request["params"]["message"]["parts"]) > 0
        assert "type" in request["params"]["message"]["parts"][0]
        assert "text" in request["params"]["message"]["parts"][0]

    def test_send_task_response_format(self):
        """Test the send task response format."""
        task_id = generate_uuid()
        session_id = generate_uuid()
        
        # Example from the spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "sessionId": session_id,
                "status": {
                    "state": "completed",
                },
                "artifacts": [{
                    "name": "joke",
                    "parts": [{
                        "type": "text",
                        "text": "Why did the chicken cross the road? To get to the other side!"
                    }]
                }],
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "id" in response["result"]
        assert "sessionId" in response["result"]
        assert "status" in response["result"]
        assert "state" in response["result"]["status"]
        assert "artifacts" in response["result"]
        assert len(response["result"]["artifacts"]) > 0
        
        # Validate artifact structure
        artifact = response["result"]["artifacts"][0]
        assert "parts" in artifact
        assert len(artifact["parts"]) > 0
        assert "type" in artifact["parts"][0]
        assert "text" in artifact["parts"][0]


class TestGetTaskFormat:
    """Test the Get Task format."""

    def test_get_task_request_format(self):
        """Test the get task request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/get",
            "params": {
                "id": task_id,
                "historyLength": 10,
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/get"
        assert "params" in request
        assert "id" in request["params"]
        assert "historyLength" in request["params"]

    def test_get_task_response_format(self):
        """Test the get task response format."""
        task_id = generate_uuid()
        session_id = generate_uuid()
        
        # Example from the spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "sessionId": session_id,
                "status": {
                    "state": "completed"
                },
                "artifacts": [{
                    "parts": [{
                        "type": "text",
                        "text": "Why did the chicken cross the road? To get to the other side!"
                    }]
                }],
                "history": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "type": "text",
                                "text": "tell me a joke"
                            }
                        ]
                    }
                ],
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "id" in response["result"]
        assert "sessionId" in response["result"]
        assert "status" in response["result"]
        assert "state" in response["result"]["status"]
        assert "artifacts" in response["result"]
        assert "history" in response["result"]
        
        # Validate history structure
        assert len(response["result"]["history"]) > 0
        message = response["result"]["history"][0]
        assert "role" in message
        assert "parts" in message
        assert "type" in message["parts"][0]
        assert "text" in message["parts"][0]


class TestCancelTaskFormat:
    """Test the Cancel Task format."""

    def test_cancel_task_request_format(self):
        """Test the cancel task request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/cancel",
            "params": {
                "id": task_id,
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/cancel"
        assert "params" in request
        assert "id" in request["params"]

    def test_cancel_task_response_format(self):
        """Test the cancel task response format."""
        task_id = generate_uuid()
        session_id = generate_uuid()
        
        # Example from the spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "sessionId": session_id,
                "status": {
                    "state": "canceled"
                },
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "id" in response["result"]
        assert "sessionId" in response["result"]
        assert "status" in response["result"]
        assert "state" in response["result"]["status"]
        assert response["result"]["status"]["state"] == "canceled"