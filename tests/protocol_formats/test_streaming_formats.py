# tests/protocol_formats/test_conversation_formats.py
"""
Tests for A2A Streaming formats based on the specification.

This file contains tests that validate the request and response formats
for streaming operations as defined in the A2A specification.
"""
import pytest
import json
from datetime import datetime
from uuid import uuid4


# Helper function to generate UUIDs for tests
def generate_uuid():
    return str(uuid4())


class TestStreamingFormat:
    """Test the Streaming format."""

    def test_streaming_request_format(self):
        """Test the streaming request format."""
        task_id = generate_uuid()
        session_id = generate_uuid()
        
        # Example from the spec
        request = {
            "method": "tasks/sendSubscribe",
            "params": {
                "id": task_id,
                "sessionId": session_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "type": "text",
                        "text": "write a long paper describing the attached pictures"
                    }, {
                        "type": "file",
                        "file": {
                            "mimeType": "image/png",
                            "data": "<base64-encoded-content>"
                        }
                    }]
                },
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert "method" in request
        assert request["method"] == "tasks/sendSubscribe"
        assert "params" in request
        assert "id" in request["params"]
        assert "sessionId" in request["params"]
        assert "message" in request["params"]
        assert "role" in request["params"]["message"]
        assert "parts" in request["params"]["message"]
        assert len(request["params"]["message"]["parts"]) == 2
        
        # Validate file part
        file_part = request["params"]["message"]["parts"][1]
        assert file_part["type"] == "file"
        assert "file" in file_part
        assert "mimeType" in file_part["file"]
        assert "data" in file_part["file"]

    def test_streaming_response_format(self):
        """Test the streaming response format sequence."""
        task_id = generate_uuid()
        
        # First chunk - status update
        response1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "status": {
                    "state": "working",
                    "timestamp": "2025-04-02T16:59:25.331844"
                },
                "final": False
            }
        }
        
        # Second chunk - artifact chunk 1
        response2 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "artifact": {
                    "parts": [
                        {"type": "text", "text": "<section 1...>"}
                    ],
                    "index": 0,
                    "append": False,
                    "lastChunk": False
                }
            }
        }
        
        # Third chunk - artifact chunk 2
        response3 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "artifact": {
                    "parts": [
                        {"type": "text", "text": "<section 2...>"}
                    ],
                    "index": 0,
                    "append": True,
                    "lastChunk": False
                }
            }
        }
        
        # Fourth chunk - artifact final chunk
        response4 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": 1,
                "artifact": {
                    "parts": [
                        {"type": "text", "text": "<section 3...>"}
                    ],
                    "index": 0,
                    "append": True,
                    "lastChunk": True
                }
            }
        }
        
        # Fifth chunk - final status
        response5 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": 1,
                "status": {
                    "state": "completed",
                    "timestamp": "2025-04-02T16:59:35.331844"
                },
                "final": True
            }
        }
        
        # Validate status update
        assert response1["jsonrpc"] == "2.0"
        assert "result" in response1
        assert "id" in response1["result"]
        assert "status" in response1["result"]
        assert response1["result"]["status"]["state"] == "working"
        assert "timestamp" in response1["result"]["status"]
        assert "final" in response1["result"]
        assert response1["result"]["final"] is False
        
        # Validate artifact chunks
        for response in [response2, response3, response4]:
            assert response["jsonrpc"] == "2.0"
            assert "result" in response
            assert "id" in response["result"]
            assert "artifact" in response["result"]
            assert "parts" in response["result"]["artifact"]
            assert "index" in response["result"]["artifact"]
            assert "append" in response["result"]["artifact"]
            assert "lastChunk" in response["result"]["artifact"]
        
        # First chunk should not append
        assert response2["result"]["artifact"]["append"] is False
        
        # Middle chunks should append
        assert response3["result"]["artifact"]["append"] is True
        assert response3["result"]["artifact"]["lastChunk"] is False
        
        # Last chunk should be marked as last
        assert response4["result"]["artifact"]["append"] is True
        assert response4["result"]["artifact"]["lastChunk"] is True
        
        # Final status
        assert response5["jsonrpc"] == "2.0"
        assert "result" in response5
        assert "status" in response5["result"]
        assert response5["result"]["status"]["state"] == "completed"
        assert "final" in response5["result"]
        assert response5["result"]["final"] is True


class TestResubscribeFormat:
    """Test the Resubscribe format."""

    def test_resubscribe_request_format(self):
        """Test the resubscribe request format."""
        task_id = generate_uuid()
        
        # Example from the spec
        request = {
            "method": "tasks/resubscribe",
            "params": {
                "id": task_id,
                "metadata": {}
            }
        }
        
        # Validate the structure
        assert "method" in request
        assert request["method"] == "tasks/resubscribe"
        assert "params" in request
        assert "id" in request["params"]

    def test_resubscribe_response_format(self):
        """Test the resubscribe response format sequence."""
        task_id = generate_uuid()
        
        # First response chunk
        response1 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "artifact": {
                    "parts": [
                        {"type": "text", "text": "<section 2...>"}
                    ],
                    "index": 0,
                    "append": True,
                    "lastChunk": False
                }
            }
        }
        
        # Second response chunk
        response2 = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "id": task_id,
                "artifact": {
                    "parts": [
                        {"type": "text", "text": "<section 3...>"}
                    ],
                    "index": 0,
                    "append": True,
                    "lastChunk": True
                }
            }
        }