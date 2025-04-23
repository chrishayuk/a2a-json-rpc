# tests/test_task_operations.py
"""
Integration tests for task operations using mocked transport.
"""
import json
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

# Core protocols and models
from a2a_json_rpc.protocol import JSONRPCProtocol
from a2a_json_rpc.models import Request, Response

# Error types
from a2a_json_rpc.a2a_errors import TaskNotFoundError, TaskNotCancelableError
from a2a_json_rpc.json_rpc_errors import MethodNotFoundError

# A2A-specific models
from a2a_json_rpc.spec import Message, TextPart


# Mock task data
MOCK_TASK = {
    "id": "task-123",
    "sessionId": "session-456",
    "status": {
        "state": "working",
        "timestamp": datetime.now().isoformat()
    },
    "artifacts": []
}

# Define mock protocol for testing
class MockProtocol(JSONRPCProtocol):
    """Protocol with built-in mock handlers for testing."""
    
    def __init__(self):
        super().__init__()
        
        # Register the mock handlers
        self.register("tasks/get", self.get_task)
        self.register("tasks/send", self.send_task)
        self.register("tasks/cancel", self.cancel_task)
    
    async def get_task(self, method, params):
        """Mock implementation of tasks/get."""
        task_id = params.get('id')
        if task_id == "task-123":
            return MOCK_TASK
        elif task_id == "nonexistent":
            raise TaskNotFoundError("Task not found", data={"id": task_id})
        else:
            return None
    
    async def send_task(self, method, params):
        """Mock implementation of tasks/send."""
        task_id = params.get('id')
        message = params.get('message')
        
        # Just echo the message back
        if message and message.get('role') == 'user':
            text_content = ""
            for part in message.get('parts', []):
                if part.get('type') == 'text':
                    text_content = part.get('text', '')
                    break
            
            response_message = {
                "role": "agent",
                "parts": [{"type": "text", "text": f"Echo: {text_content}"}]
            }
            return {
                "id": task_id,
                "status": {
                    "state": "completed",
                    "message": response_message,
                    "timestamp": datetime.now().isoformat()
                }
            }
        return None
    
    async def cancel_task(self, method, params):
        """Mock implementation of tasks/cancel."""
        task_id = params.get('id')
        if task_id == "task-123":
            return {
                "id": task_id,
                "status": {
                    "state": "canceled",
                    "timestamp": datetime.now().isoformat()
                }
            }
        elif task_id == "nonexistent":
            raise TaskNotFoundError("Task not found", data={"id": task_id})
        elif task_id == "uncancelable":
            raise TaskNotCancelableError("Task cannot be canceled", data={"id": task_id})
        else:
            return None

# Mock protocol handlers replaced with MockProtocol class above


@pytest.fixture
def protocol():
    """Create a protocol instance with mock task handlers."""
    return MockProtocol()


class TestTaskOperations:
    """Integration tests for A2A task operations."""
    
    @pytest.mark.asyncio
    async def test_get_task(self, protocol):
        """Test getting a task."""
        # Valid task
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/get",
            "params": {"id": "task-123"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["result"]["id"] == "task-123"
        assert response["result"]["status"]["state"] == "working"
        
        # Nonexistent task
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tasks/get",
            "params": {"id": "nonexistent"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert response["error"]["code"] == -32001  # TaskNotFoundError
        assert "not found" in response["error"]["message"].lower()
        assert response["error"]["data"]["id"] == "nonexistent"
    
    @pytest.mark.asyncio
    async def test_send_task(self, protocol):
        """Test sending a message to a task."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/send",
            "params": {
                "id": "task-123",
                "message": {
                    "role": "user",
                    "parts": [
                        {"type": "text", "text": "Hello, world!"}
                    ]
                }
            }
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["result"]["id"] == "task-123"
        assert response["result"]["status"]["state"] == "completed"
        assert response["result"]["status"]["message"]["role"] == "agent"
        assert "Echo: Hello, world!" in response["result"]["status"]["message"]["parts"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_cancel_task(self, protocol):
        """Test canceling a task."""
        # Valid cancellation
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/cancel",
            "params": {"id": "task-123"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["result"]["id"] == "task-123"
        assert response["result"]["status"]["state"] == "canceled"
        
        # Nonexistent task
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tasks/cancel",
            "params": {"id": "nonexistent"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert response["error"]["code"] == -32001  # TaskNotFoundError 
        assert "not found" in response["error"]["message"].lower()
        
        # Uncancelable task
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tasks/cancel",
            "params": {"id": "uncancelable"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert response["error"]["code"] == -32002  # TaskNotCancelableError
        assert "cannot be canceled" in response["error"]["message"]
    
    @pytest.mark.asyncio
    async def test_unknown_method(self, protocol):
        """Test calling an unknown method."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/unknown",
            "params": {"id": "task-123"}
        }
        
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["error"]["code"] == -32601  # MethodNotFoundError
        assert "not found" in response["error"]["message"].lower()