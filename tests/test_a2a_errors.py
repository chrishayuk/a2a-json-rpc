# tests/test_a2a_errors.py
"""
Tests for A2A-specific error definitions.
"""
import pytest
from a2a_json_rpc.a2a_errors import (
    TaskNotFoundError,
    TaskNotCancelableError,
    PushNotificationsNotSupportedError,
    UnsupportedOperationError,
    TaskRejectedError,
    AuthenticationRequiredError,
)
from a2a_json_rpc.a2a_error_codes import A2AErrorCode


def test_task_not_found_error():
    """Test TaskNotFoundError has correct code."""
    error = TaskNotFoundError("Task 123 not found")
    assert error.CODE == A2AErrorCode.TASK_NOT_FOUND
    assert error.CODE == -32001
    assert error.message == "Task 123 not found"


def test_task_not_cancelable_error():
    """Test TaskNotCancelableError has correct code."""
    error = TaskNotCancelableError("Task cannot be canceled")
    assert error.CODE == A2AErrorCode.TASK_NOT_CANCELABLE
    assert error.CODE == -32002
    assert error.message == "Task cannot be canceled"


def test_push_notifications_not_supported_error():
    """Test PushNotificationsNotSupportedError has correct code."""
    error = PushNotificationsNotSupportedError("Push notifications not supported")
    assert error.CODE == A2AErrorCode.PUSH_NOTIFICATIONS_NOT_SUPPORTED
    assert error.CODE == -32003
    assert error.message == "Push notifications not supported"


def test_unsupported_operation_error():
    """Test UnsupportedOperationError has correct code."""
    error = UnsupportedOperationError("Operation not supported")
    assert error.CODE == A2AErrorCode.UNSUPPORTED_OPERATION
    assert error.CODE == -32004
    assert error.message == "Operation not supported"


def test_task_rejected_error():
    """Test TaskRejectedError has correct code."""
    error = TaskRejectedError("Task was rejected")
    assert error.CODE == A2AErrorCode.TASK_REJECTED
    assert error.CODE == -32005
    assert error.message == "Task was rejected"


def test_authentication_required_error():
    """Test AuthenticationRequiredError has correct code."""
    error = AuthenticationRequiredError("Authentication is required")
    assert error.CODE == A2AErrorCode.AUTHENTICATION_REQUIRED
    assert error.CODE == -32006
    assert error.message == "Authentication is required"


def test_error_to_dict():
    """Test error serialization to dict."""
    error = TaskNotFoundError("Task 123 not found", data={"task_id": "123"})
    error_dict = error.to_dict()
    
    assert error_dict == {
        "code": -32001,
        "message": "Task 123 not found",
        "data": {"task_id": "123"}
    }