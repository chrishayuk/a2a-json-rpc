# tests/conftest.py
"""
Common test fixtures for A2A protocol tests.
"""
import pytest
import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from a2a_json_rpc.protocol import JSONRPCProtocol

# Add configuration for test markers
def pytest_configure(config):
    config.addinivalue_line("markers", "model_details: mark tests that depend on model implementation details")
    config.addinivalue_line("markers", "slow: mark tests as slow running")

# Add command line option for skipping model details tests
def pytest_addoption(parser):
    parser.addoption(
        "--skip-model-details", 
        action="store_true", 
        default=False,
        help="Skip tests that rely on specific model implementation details"
    )
    parser.addoption(
        "--skip-slow", 
        action="store_true", 
        default=False, 
        help="Skip slow running tests"
    )

# Skip marked tests based on command line option
def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-model-details"):
        skip_model_details = pytest.mark.skip(reason="Test depends on model implementation details")
        for item in items:
            if "model_details" in item.keywords:
                item.add_marker(skip_model_details)
    
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="Test is slow running")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

@pytest.fixture
def protocol():
    """Create a clean protocol instance."""
    return JSONRPCProtocol()


@pytest.fixture
def sample_task():
    """Sample task data."""
    return {
        "id": "task-123",
        "sessionId": "session-456",
        "status": {
            "state": "working",
            "timestamp": datetime.now().isoformat()
        },
        "artifacts": []
    }


@pytest.fixture
def sample_request():
    """Sample JSON-RPC request."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "method": "tasks/get",
        "params": {"id": "task-123"}
    }


@pytest.fixture
def sample_response():
    """Sample JSON-RPC response."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "result": {
            "id": "task-123",
            "status": {
                "state": "working",
                "timestamp": datetime.now().isoformat()
            }
        }
    }


@pytest.fixture
def sample_error_response():
    """Sample JSON-RPC error response."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }


@pytest.fixture
def sample_notification():
    """Sample JSON-RPC notification."""
    return {
        "jsonrpc": "2.0",
        "method": "tasks/notify",
        "params": {"id": "task-123", "event": "status_changed"}
    }



@pytest.fixture
def protocol():
    """Create a clean protocol instance."""
    return JSONRPCProtocol()


@pytest.fixture
def sample_task():
    """Sample task data."""
    return {
        "id": "task-123",
        "sessionId": "session-456",
        "status": {
            "state": "working",
            "timestamp": datetime.now().isoformat()
        },
        "artifacts": []
    }


@pytest.fixture
def sample_request():
    """Sample JSON-RPC request."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "method": "tasks/get",
        "params": {"id": "task-123"}
    }


@pytest.fixture
def sample_response():
    """Sample JSON-RPC response."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "result": {
            "id": "task-123",
            "status": {
                "state": "working",
                "timestamp": datetime.now().isoformat()
            }
        }
    }


@pytest.fixture
def sample_error_response():
    """Sample JSON-RPC error response."""
    return {
        "jsonrpc": "2.0",
        "id": 123,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }


@pytest.fixture
def sample_notification():
    """Sample JSON-RPC notification."""
    return {
        "jsonrpc": "2.0",
        "method": "tasks/notify",
        "params": {"id": "task-123", "event": "status_changed"}
    }