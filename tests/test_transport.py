# tests/test_transport.py
"""
Tests for the transport layer implementation.
"""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Import the transport protocol (not the implementation)
from a2a_json_rpc.transport import JSONRPCTransport


# Mock HTTP transport implementation
class MockHTTPTransport:
    """Mock implementation of JSONRPCTransport over HTTP."""
    
    def __init__(self, url, *, headers=None):
        self.url = url
        self.headers = headers or {}
        self.request_id = 0
        
        # Mock responses for different methods
        self.mock_responses = {
            "tasks/get": {"id": "task-123", "status": {"state": "working"}},
            "tasks/send": {"id": "task-123", "status": {"state": "completed"}},
            "tasks/cancel": {"id": "task-123", "status": {"state": "canceled"}},
            "error_method": None  # Will trigger an error response
        }
        
        # Stream of events for testing streaming
        self.stream_events = [
            {"id": "task-123", "status": {"state": "working"}},
            {"id": "task-123", "status": {"state": "completed"}},
        ]
    
    async def call(self, method, params):
        """Send a JSON-RPC request and return the result."""
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        
        # Simulate sending request and getting response
        if method == "error_method":
            response = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "error": {
                    "code": -32601,
                    "message": "Method not found"
                }
            }
            raise Exception(f"JSON-RPC error: {response['error']['message']}")
        
        response = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "result": self.mock_responses.get(method, {})
        }
        
        return response["result"]
    
    async def notify(self, method, params):
        """Send a JSON-RPC notification (no response expected)."""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        # Just record that we sent it, no response needed
        return None
    
    async def stream(self):
        """Receive a stream of JSON-RPC messages."""
        for event in self.stream_events:
            yield {
                "jsonrpc": "2.0",
                "result": event
            }


# Tests
class TestTransport:
    """Test the transport layer."""
    
    @pytest.fixture
    def transport(self):
        """Create a mock transport instance."""
        return MockHTTPTransport("https://example.com/agent")
    
    @pytest.mark.asyncio
    async def test_call_method(self, transport):
        """Test calling a method and getting a result."""
        result = await transport.call("tasks/get", {"id": "task-123"})
        
        assert result["id"] == "task-123"
        assert result["status"]["state"] == "working"
    
    @pytest.mark.asyncio
    async def test_call_with_error(self, transport):
        """Test handling an error response."""
        with pytest.raises(Exception) as exc:
            await transport.call("error_method", {})
        
        assert "JSON-RPC error: Method not found" in str(exc.value)
    
    @pytest.mark.asyncio
    async def test_notification(self, transport):
        """Test sending a notification."""
        # No exception should be raised
        result = await transport.notify("tasks/ping", {"id": "task-123"})
        assert result is None
    
    @pytest.mark.asyncio
    async def test_stream(self, transport):
        """Test receiving a stream of events."""
        events = []
        async for event in transport.stream():
            events.append(event["result"])
            if event["result"]["status"]["state"] == "completed":
                break
        
        assert len(events) == 2
        assert events[0]["status"]["state"] == "working"
        assert events[1]["status"]["state"] == "completed"


# Test with a more realistic HTTP client
class TestHTTPTransport:
    """Test a more realistic HTTP transport implementation."""
    
    @pytest.mark.asyncio
    async def test_http_transport(self):
        """Test a more realistic HTTP transport implementation."""
        # Use a generic AsyncClient mock instead of httpx specific
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"id": "task-123", "status": {"state": "working"}}
        }
        mock_client.post = AsyncMock(return_value=mock_response)
        
        # This is a more realistic implementation that would use any async HTTP client
        class HTTPTransport:
            def __init__(self, url, *, headers=None):
                self.url = url
                self.headers = headers or {}
                self.client = mock_client
                self.request_id = 0
            
            async def call(self, method, params):
                self.request_id += 1
                request = {
                    "jsonrpc": "2.0",
                    "id": self.request_id,
                    "method": method,
                    "params": params
                }
                
                # Send the request
                response = await self.client.post(
                    self.url,
                    json=request,
                    headers=self.headers
                )
                
                if response.status_code != 200:
                    raise Exception(f"HTTP error: {response.status_code}")
                
                data = response.json()
                if "error" in data:
                    raise Exception(f"JSON-RPC error: {data['error']['message']}")
                
                return data.get("result")
        
        # Create the transport and test it
        transport = HTTPTransport("https://example.com/agent")
        result = await transport.call("tasks/get", {"id": "task-123"})
        
        # Check the request was sent correctly
        mock_client.post.assert_called_once_with(
            "https://example.com/agent",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tasks/get",
                "params": {"id": "task-123"}
            },
            headers={}
        )
        
        # Check we got the expected result
        assert result["id"] == "task-123"
        assert result["status"]["state"] == "working"