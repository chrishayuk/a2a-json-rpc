# tests/test_json_rpc_errors.py
"""
Standard JSON-RPC 2.0 error definitions.
"""
from typing import Any, Dict, Optional

from a2a_json_rpc.json_rpc_error_codes import JsonRpcErrorCode


class JSONRPCError(Exception):
    """Base for all JSON-RPC errors."""
    CODE: JsonRpcErrorCode

    def __init__(self, message: Optional[str] = None, *, data: Any = None) -> None:
        self.message: str = message or self.__class__.__doc__ or self.__class__.__name__
        self.data: Any = data
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a JSON-RPC error object."""
        err: Dict[str, Any] = {"code": int(self.CODE), "message": self.message, "data": self.data}
        return err


class ParseError(JSONRPCError):
    """Invalid JSON was received by the server."""
    CODE = JsonRpcErrorCode.PARSE_ERROR


class InvalidRequestError(JSONRPCError):
    """The JSON sent is not a valid Request object."""
    CODE = JsonRpcErrorCode.INVALID_REQUEST


class MethodNotFoundError(JSONRPCError):
    """The method does not exist / is not available."""
    CODE = JsonRpcErrorCode.METHOD_NOT_FOUND


class InvalidParamsError(JSONRPCError):
    """Invalid method parameter(s)."""
    CODE = JsonRpcErrorCode.INVALID_PARAMS


class InternalError(JSONRPCError):
    """Internal JSON-RPC error."""
    CODE = JsonRpcErrorCode.INTERNAL_ERROR