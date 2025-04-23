# tests/test_a2a_errors.py
"""
A2A-specific error definitions.
"""
from typing import Any, Dict, Optional

from a2a_json_rpc.a2a_error_codes import A2AErrorCode
from a2a_json_rpc.json_rpc_errors import JSONRPCError


class TaskNotFoundError(JSONRPCError):
    """Task not found."""
    CODE = A2AErrorCode.TASK_NOT_FOUND


class TaskNotCancelableError(JSONRPCError):
    """Task cannot be canceled."""
    CODE = A2AErrorCode.TASK_NOT_CANCELABLE


class PushNotificationsNotSupportedError(JSONRPCError):
    """Push notification is not supported."""
    CODE = A2AErrorCode.PUSH_NOTIFICATIONS_NOT_SUPPORTED


class UnsupportedOperationError(JSONRPCError):
    """This operation is not supported."""
    CODE = A2AErrorCode.UNSUPPORTED_OPERATION