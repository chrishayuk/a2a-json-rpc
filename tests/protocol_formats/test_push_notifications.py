# tests/protocol_formats/test_push_notifications.py
"""
Tests for A2A Push Notification formats based on the specification.

This file contains tests that validate the request and response formats
for push notification operations as defined in the A2A specification.
"""
import pytest
import json
from uuid import uuid4

from a2a_json_rpc.protocol import JSONRPCProtocol
from a2a_json_rpc.a2a_errors import PushNotificationsNotSupportedError


# Helper function to generate UUIDs for tests
def generate_uuid():
    return str(uuid4())


class TestPushNotificationFormat:
    """Test the Push Notification formats."""

    def test_set_push_notification_request_format(self):
        """Test the set push notification request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotification/set",
            "params": {
                "id": task_id,
                "pushNotificationConfig": {
                    "url": "https://example.com/callback",
                    "authentication": {
                        "schemes": ["jwt"]
                    }
                }
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotification/set"
        assert "params" in request
        assert "id" in request["params"]
        assert "pushNotificationConfig" in request["params"]
        assert "url" in request["params"]["pushNotificationConfig"]
        assert "authentication" in request["params"]["pushNotificationConfig"]

    def test_set_push_notification_response_format(self):
        """Test the set push notification response format."""
        task_id = generate_uuid()
        
        # Example from the spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "pushNotificationConfig": {
                    "url": "https://example.com/callback",
                    "authentication": {
                        "schemes": ["jwt"]
                    }
                }
            }
        }
        
        # Validate the structure
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "id" in response["result"]
        assert "pushNotificationConfig" in response["result"]
        assert "url" in response["result"]["pushNotificationConfig"]
        assert "authentication" in response["result"]["pushNotificationConfig"]

    def test_get_push_notification_request_format(self):
        """Test the get push notification request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotification/get",
            "params": {
                "id": task_id
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotification/get"
        assert "params" in request
        assert "id" in request["params"]

    def test_get_push_notification_response_format(self):
        """Test the get push notification response format."""
        task_id = generate_uuid()
        
        # Example from the spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "pushNotificationConfig": {
                    "url": "https://example.com/callback",
                    "authentication": {
                        "schemes": ["jwt"]
                    }
                }
            }
        }
        
        # Validate the structure
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "id" in response["result"]
        assert "pushNotificationConfig" in response["result"]
        assert "url" in response["result"]["pushNotificationConfig"]
        assert "authentication" in response["result"]["pushNotificationConfig"]
        
    def test_push_notification_error_format(self):
        """Test the push notification error format."""
        error = PushNotificationsNotSupportedError("Push notifications are not supported by this agent")
        error_dict = error.to_dict()
        
        # Validate the structure
        assert "code" in error_dict
        assert error_dict["code"] == -32003
        assert "message" in error_dict
        assert "not supported" in error_dict["message"].lower()

    def test_push_notification_config_structure(self):
        """Test the PushNotificationConfig structure."""
        config = {
            "url": "https://example.com/callback",
            "token": "secure-token-123",
            "authentication": {
                "schemes": ["bearer", "jwt"],
                "credentials": "optional-credentials"
            }
        }
        
        # Validate the structure
        assert "url" in config
        assert "token" in config
        assert "authentication" in config
        assert "schemes" in config["authentication"]
        assert isinstance(config["authentication"]["schemes"], list)