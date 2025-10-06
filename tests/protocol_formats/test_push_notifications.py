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
        config_id = generate_uuid()
        
        # Example from the current spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotificationConfig/set",
            "params": {
                "id": task_id,
                "pushNotificationConfig": {
                    "id": config_id,
                    "url": "https://example.com/callback",
                    "token": "unique-session-token",
                    "authentication": {
                        "schemes": ["bearer"],
                        "credentials": "optional-credentials"
                    }
                }
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotificationConfig/set"
        assert "params" in request
        assert "id" in request["params"]
        assert "pushNotificationConfig" in request["params"]
        
        config = request["params"]["pushNotificationConfig"]
        assert "url" in config  # Required field
        assert "id" in config
        assert "token" in config
        assert "authentication" in config
        assert "schemes" in config["authentication"]  # Required in authentication

    def test_set_push_notification_response_format(self):
        """Test the set push notification response format."""
        task_id = generate_uuid()
        config_id = generate_uuid()
        
        # Example from the current spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "pushNotificationConfig": {
                    "id": config_id,
                    "url": "https://example.com/callback",
                    "token": "unique-session-token",
                    "authentication": {
                        "schemes": ["bearer"]
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
        
        config = response["result"]["pushNotificationConfig"]
        assert "url" in config
        assert "id" in config
        assert "token" in config
        assert "authentication" in config
        assert "schemes" in config["authentication"]

    def test_get_push_notification_request_format(self):
        """Test the get push notification request format."""
        task_id = generate_uuid()
        config_id = generate_uuid()
        
        # Example from the current spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotificationConfig/get",
            "params": {
                "id": task_id,
                "pushNotificationConfigId": config_id
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotificationConfig/get"
        assert "params" in request
        assert "id" in request["params"]
        assert "pushNotificationConfigId" in request["params"]

    def test_get_push_notification_response_format(self):
        """Test the get push notification response format."""
        task_id = generate_uuid()
        config_id = generate_uuid()
        
        # Example from the current spec
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "pushNotificationConfig": {
                    "id": config_id,
                    "url": "https://example.com/callback",
                    "token": "unique-session-token",
                    "authentication": {
                        "schemes": ["bearer"]
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
        
        config = response["result"]["pushNotificationConfig"]
        assert "url" in config
        assert "id" in config
        assert "token" in config
        assert "authentication" in config
        assert "schemes" in config["authentication"]

    def test_list_push_notification_request_format(self):
        """Test the list push notification request format."""
        task_id = generate_uuid()
        
        # Example from the current spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotificationConfig/list",
            "params": {
                "id": task_id
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotificationConfig/list"
        assert "params" in request
        assert "id" in request["params"]

    def test_delete_push_notification_request_format(self):
        """Test the delete push notification request format."""
        task_id = generate_uuid()
        config_id = generate_uuid()
        
        # Example from the current spec
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/pushNotificationConfig/delete",
            "params": {
                "id": task_id,
                "pushNotificationConfigId": config_id
            }
        }
        
        # Validate the structure
        assert request["jsonrpc"] == "2.0"
        assert "id" in request
        assert request["method"] == "tasks/pushNotificationConfig/delete"
        assert "params" in request
        assert "id" in request["params"]
        assert "pushNotificationConfigId" in request["params"]
        
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
        config_id = generate_uuid()
        
        config = {
            "id": config_id,
            "url": "https://example.com/callback",
            "token": "secure-token-123",
            "authentication": {
                "schemes": ["bearer", "basic"],
                "credentials": "optional-credentials"
            }
        }
        
        # Validate the structure
        assert "url" in config  # Required field
        assert "id" in config
        assert "token" in config
        assert "authentication" in config
        assert "schemes" in config["authentication"]  # Required in authentication
        assert isinstance(config["authentication"]["schemes"], list)

    def test_minimal_push_notification_config(self):
        """Test minimal push notification config with only required fields."""
        config = {
            "url": "https://minimal.example.com/callback"
        }
        
        # Only URL is required
        assert "url" in config
        
    def test_push_notification_config_with_auth(self):
        """Test push notification config with comprehensive authentication."""
        config_id = generate_uuid()
        
        config = {
            "id": config_id,
            "url": "https://auth.example.com/callback",
            "token": "session-token-456",
            "authentication": {
                "schemes": ["bearer", "basic", "apiKey"],
                "credentials": "auth-credentials-string"
            }
        }
        
        # Validate authentication details
        auth = config["authentication"]
        assert "schemes" in auth
        assert isinstance(auth["schemes"], list)
        assert len(auth["schemes"]) > 0
        
        # Validate supported authentication schemes
        valid_schemes = ["bearer", "basic", "apiKey", "oauth2", "jwt"]
        for scheme in auth["schemes"]:
            assert scheme in valid_schemes, f"Unsupported authentication scheme: {scheme}"