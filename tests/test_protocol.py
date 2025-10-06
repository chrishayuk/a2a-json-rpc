# tests/test_protocol.py
"""
Tests for the JSONRPCProtocol class.
"""
import pytest
import json
from unittest.mock import MagicMock, AsyncMock

from a2a_json_rpc.protocol import JSONRPCProtocol
from a2a_json_rpc.json_rpc_errors import ParseError, InvalidRequestError, MethodNotFoundError, InternalError


@pytest.fixture
def protocol():
    """Returns a JSONRPCProtocol instance for testing."""
    return JSONRPCProtocol()


class TestJSONRPCProtocol:
    """Tests for the JSONRPCProtocol class."""

    def test_register_method(self, protocol):
        """Test that a method can be registered."""
        def handler(method, params):
            return "test"
        
        protocol.register("test_method", handler)
        assert "test_method" in protocol._methods
        assert protocol._methods["test_method"] == handler

    def test_method_decorator(self, protocol):
        """Test the method decorator for registration."""
        @protocol.method("decorated_method")
        def handler(method, params):
            return "decorated"
        
        assert "decorated_method" in protocol._methods
        assert protocol._methods["decorated_method"] == handler

    def test_create_request(self, protocol):
        """Test creating a JSON-RPC request."""
        request = protocol.create_request("test_method", {"param": "value"}, id="test-id")
        assert request["jsonrpc"] == "2.0"
        assert request["id"] == "test-id"
        assert request["method"] == "test_method"
        assert request["params"] == {"param": "value"}

    def test_create_notification(self, protocol):
        """Test creating a JSON-RPC notification."""
        notification = protocol.create_notification("test_event", {"param": "value"})
        assert notification["jsonrpc"] == "2.0"
        assert "id" not in notification
        assert notification["method"] == "test_event"
        assert notification["params"] == {"param": "value"}

    @pytest.mark.asyncio
    async def test_handle_raw_valid_request(self, protocol):
        """Test handling a valid raw JSON-RPC request."""
        @protocol.method("test_method")
        def handler(method, params):
            return f"processed {params['param']}"
        
        request = '{"jsonrpc": "2.0", "id": 1, "method": "test_method", "params": {"param": "value"}}'
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["result"] == "processed value"

    @pytest.mark.asyncio
    async def test_handle_raw_notification(self, protocol):
        """Test handling a raw notification."""
        handler_mock = MagicMock()
        
        @protocol.method("test_event")
        def handler(method, params):
            handler_mock(params)
        
        notification = '{"jsonrpc": "2.0", "method": "test_event", "params": {"param": "value"}}'
        response = await protocol._handle_raw_async(notification)
        
        assert response is None
        handler_mock.assert_called_once_with({"param": "value"})

    @pytest.mark.asyncio
    async def test_handle_raw_parse_error(self, protocol):
        """Test handling a JSON parse error."""
        invalid_json = '{"jsonrpc": "2.0", "id": 1, "method": "test_method"'
        response = await protocol._handle_raw_async(invalid_json)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] is None
        assert response["error"]["code"] == ParseError.CODE
        assert "Invalid JSON payload" in response["error"]["message"]

    @pytest.mark.asyncio
    async def test_handle_raw_invalid_request(self, protocol):
        """Test handling an invalid request object."""
        invalid_request = '{"jsonrpc": "2.0", "id": 1}'  # Missing 'method'
        response = await protocol._handle_raw_async(invalid_request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] is None
        assert response["error"]["code"] == InvalidRequestError.CODE
        assert "Request validation error" in response["error"]["message"]

    @pytest.mark.asyncio
    async def test_handle_raw_method_not_found(self, protocol):
        """Test handling a request for a non-existent method."""
        request = '{"jsonrpc": "2.0", "id": 1, "method": "nonexistent_method", "params": {}}'
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["error"]["code"] == MethodNotFoundError.CODE
        assert "not found" in response["error"]["message"]

    @pytest.mark.asyncio
    async def test_handle_raw_internal_error(self, protocol):
        """Test handling an internal error in a handler."""
        @protocol.method("error_method")
        def handler(method, params):
            raise ValueError("Something went wrong")
        
        request = '{"jsonrpc": "2.0", "id": 1, "method": "error_method", "params": {}}'
        response = await protocol._handle_raw_async(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["error"]["code"] == InternalError.CODE
        assert "Internal error" in response["error"]["message"]

    @pytest.mark.asyncio
    async def test_async_handler(self, protocol):
        """Test that async handlers are correctly awaited."""
        @protocol.method("async_method")
        async def async_handler(method, params):
            return "async result"
        
        request = '{"jsonrpc": "2.0", "id": 1, "method": "async_method", "params": {}}'
        response = await protocol._handle_raw_async(request)
        
        assert response["result"] == "async result"
