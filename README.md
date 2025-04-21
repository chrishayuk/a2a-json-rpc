# a2a-json-rpc

A JSON-RPC implementation for the A2A (Agent-to-Agent) Protocol.

## Overview

The a2a-json-rpc library provides a lightweight, transport-agnostic implementation of the JSON-RPC 2.0 protocol specifically tailored for A2A (Agent-to-Agent) communication. It includes:

- Complete JSON-RPC 2.0 request/response handling
- A2A-specific error definitions and handling
- Pydantic models for type-safe message processing
- Async/await support via anyio
- Transport abstraction layer

## Installation

```bash
pip install a2a-json-rpc
```

## Quick Start

```python
import asyncio
from a2a_json_rpc.protocol import JSONRPCProtocol
from a2a_json_rpc.models import Json

# Create a protocol instance
protocol = JSONRPCProtocol()

# Register a method handler
@protocol.method("echo")
async def echo_handler(method: str, params: Json) -> Json:
    return params

# Process a request
async def main():
    request = protocol.create_request("echo", {"message": "Hello, A2A!"})
    response = await protocol._handle_raw_async(request)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- **Type Safety**: Built with Pydantic for robust data validation and serialization
- **Async First**: Designed for asynchronous communication patterns
- **Transport Agnostic**: Can be used with HTTP, WebSockets, or any other transport
- **Error Handling**: Comprehensive error types for both JSON-RPC and A2A-specific errors
- **Notifications**: Support for fire-and-forget notifications

## A2A Protocol Support

The library implements the A2A Protocol specification, which defines a standard way for AI agents to communicate with each other. The implementation includes:

- Task management operations
- Push notification handling
- Streaming support
- Message history tracking

## Error Handling

The library provides a comprehensive set of error types:

```python
from a2a_json_rpc.json_rpc_errors import ParseError, InvalidRequestError
from a2a_json_rpc.a2a_errors import TaskNotFoundError, PushNotificationsNotSupportedError

# JSON-RPC standard errors
raise ParseError("Invalid JSON payload")
raise InvalidRequestError("Missing required field")

# A2A-specific errors
raise TaskNotFoundError(data={"id": "task-123"})
raise PushNotificationsNotSupportedError()
```

## Transport Layer

The transport layer is defined as a protocol interface, allowing for different implementations:

```python
from a2a_json_rpc.transport import JSONRPCTransport

class MyTransport(JSONRPCTransport):
    async def call(self, method: str, params: any) -> any:
        # Implementation
        ...
    
    async def notify(self, method: str, params: any) -> None:
        # Implementation
        ...
    
    def stream(self) -> AsyncIterator[Json]:
        # Implementation
        ...
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/a2a-json-rpc.git
cd a2a-json-rpc

# Install development dependencies
make dev-install
```

### Testing

```bash
make test
```

### Building

```bash
make build
```

### Publishing

```bash
make publish
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request