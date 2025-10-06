# tests/protocol_formats/test_conversation_formats.py
"""
Tests for A2A Multi-turn Conversation formats based on the specification.

This file contains tests that validate the request and response formats
for multi-turn conversations as defined in the A2A specification.
"""
import pytest
import json
from uuid import uuid4

from a2a_json_rpc.protocol import JSONRPCProtocol


# Helper function to generate UUIDs for tests
def generate_uuid():
    return str(uuid4())


class TestMultiTurnConversationFormat:
    """Test the Multi-turn Conversation format."""

    def test_multi_turn_conversation_sequence(self):
        """Test the multi-turn conversation sequence format."""
        task_id = generate_uuid()
        session_id = generate_uuid()
        
        # First request (user initiates the task)
        request1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "kind": "text",
                        "text": "request a new phone for me"
                    }]
                },
                "metadata": {}
            }
        }
        
        # First response (agent requires input)
        response1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "contextId": session_id,
                "status": {
                    "state": "input-required",
                    "message": {
                        "role": "agent",
                        "parts": [{
                            "kind": "text",
                            "text": "Select a phone type (iPhone/Android)"
                        }]
                    }
                },
                "metadata": {}
            }
        }
        
        # Second request (user provides input)
        request2 = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "message/send",
            "params": {
                "id": task_id,
                "contextId": session_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "kind": "text",
                        "text": "Android"
                    }]
                },
                "metadata": {}
            }
        }
        
        # Second response (task completed)
        response2 = {
            "jsonrpc": "2.0",
            "id": 2,
            "result": {
                "id": task_id,
                "contextId": session_id,
                "status": {
                    "state": "completed"
                },
                "artifacts": [{
                    "name": "order-confirmation",
                    "parts": [{
                        "kind": "text",
                        "text": "I have ordered a new Android device for you. Your request number is R12443"
                    }],
                    "metadata": {}
                }],
                "metadata": {}
            }
        }
        
        # Validate request1
        assert request1["jsonrpc"] == "2.0"
        assert request1["method"] == "message/send"
        assert "id" in request1["params"]
        assert "message" in request1["params"]
        
        # Validate response1
        assert response1["jsonrpc"] == "2.0"
        assert "result" in response1
        assert "id" in response1["result"]
        assert "contextId" in response1["result"]
        assert "status" in response1["result"]
        assert response1["result"]["status"]["state"] == "input-required"
        assert "message" in response1["result"]["status"]
        
        # Validate request2
        assert request2["jsonrpc"] == "2.0"
        assert request2["method"] == "message/send"
        assert "id" in request2["params"]
        assert "contextId" in request2["params"]
        assert "message" in request2["params"]
        
        # Validate response2
        assert response2["jsonrpc"] == "2.0"
        assert "result" in response2
        assert "id" in response2["result"]
        assert "contextId" in response2["result"]
        assert "status" in response2["result"]
        assert response2["result"]["status"]["state"] == "completed"
        assert "artifacts" in response2["result"]
        assert len(response2["result"]["artifacts"]) > 0

    def test_task_state_transitions(self):
        """Test the various task state transitions in the A2A protocol."""
        # Valid task states according to the spec
        valid_states = [
            "submitted",
            "working",
            "input-required",
            "completed",
            "canceled",
            "failed",
            "unknown"
        ]
        
        # Create a status update for each state
        status_updates = []
        for state in valid_states:
            status_updates.append({
                "state": state,
                "timestamp": "2025-04-02T16:59:25.331844"
            })
            
        # Validate each state
        for i, update in enumerate(status_updates):
            assert update["state"] == valid_states[i]
            assert "timestamp" in update