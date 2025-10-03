# tests/protocol_formats/test_agent_card.py
"""
Tests for A2A Agent Card formats based on the specification.

This file contains tests that validate the request and response formats
for agent card operations as defined in the A2A specification.
"""
import pytest
import json
from uuid import uuid4

from a2a_json_rpc.protocol import JSONRPCProtocol


# Helper function to generate UUIDs for tests
def generate_uuid():
    return str(uuid4())


class TestAgentCardFormat:
    """Test the Agent Card formats."""

    def test_agent_card_structure(self):
        """Test the basic agent card structure."""
        # Example agent card based on the current spec
        agent_card = {
            "name": "Test Agent",
            "description": "A test agent for validation",
            "version": "1.0.0",
            "protocolVersion": "1.0.0",
            "url": "https://example.com",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": "test-skill",
                    "name": "Test Skill",
                    "description": "A skill for testing",
                    "tags": ["test", "validation"]
                }
            ],
            "capabilities": {
                "pushNotifications": True,
                "taskOperations": ["create", "execute"]
            },
            "securitySchemes": [
                {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            ]
        }
        
        # Validate required fields
        assert "name" in agent_card
        assert "description" in agent_card
        assert "version" in agent_card
        assert "protocolVersion" in agent_card
        assert "url" in agent_card
        assert "defaultInputModes" in agent_card
        assert "defaultOutputModes" in agent_card
        assert "skills" in agent_card
        assert "capabilities" in agent_card
        
        # Validate capabilities structure
        assert isinstance(agent_card["capabilities"], dict)
        assert "pushNotifications" in agent_card["capabilities"]
        assert "taskOperations" in agent_card["capabilities"]
        
        # Validate skills structure
        assert isinstance(agent_card["skills"], list)
        for skill in agent_card["skills"]:
            assert "id" in skill
            assert "name" in skill
            assert "description" in skill
            assert "tags" in skill
            assert isinstance(skill["tags"], list)

    def test_agent_card_with_optional_fields(self):
        """Test agent card with optional fields."""
        agent_card = {
            "name": "Advanced Test Agent",
            "description": "An advanced test agent with optional fields",
            "version": "2.0.0",
            "protocolVersion": "1.0.0",
            "url": "https://example.com/agent",
            "defaultInputModes": ["text", "voice"],
            "defaultOutputModes": ["text", "voice", "image"],
            "skills": [
                {
                    "id": "advanced-skill",
                    "name": "Advanced Skill",
                    "description": "An advanced skill with all fields",
                    "tags": ["advanced", "comprehensive"],
                    "examples": [
                        {
                            "input": "Test input",
                            "output": "Test output"
                        }
                    ],
                    "security": [
                        {
                            "type": "apiKey",
                            "in": "header",
                            "name": "X-API-Key"
                        }
                    ],
                    "inputModes": ["text"],
                    "outputModes": ["text"]
                }
            ],
            "capabilities": {
                "pushNotifications": True,
                "taskOperations": ["create", "execute", "cancel"],
                "extensions": [
                    {
                        "name": "customExtension",
                        "version": "1.0.0",
                        "required": False
                    }
                ]
            },
            "securitySchemes": [
                {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                },
                {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            ],
            "preferredTransport": "http",
            "additionalInterfaces": [
                {
                    "transport": "websocket",
                    "url": "wss://example.com/ws"
                }
            ],
            "supportsAuthenticatedExtendedCard": True,
            "signatures": {
                "cardSignature": "signature-string",
                "algorithm": "RS256"
            }
        }
        
        # Validate optional fields
        assert "preferredTransport" in agent_card
        assert "additionalInterfaces" in agent_card
        assert "supportsAuthenticatedExtendedCard" in agent_card
        assert "signatures" in agent_card
        assert "securitySchemes" in agent_card
        
        # Validate additional interfaces
        for interface in agent_card["additionalInterfaces"]:
            assert "transport" in interface
            assert "url" in interface
        
        # Validate security schemes
        for scheme in agent_card["securitySchemes"]:
            assert "type" in scheme
        
        # Validate capabilities extensions
        assert "extensions" in agent_card["capabilities"]
        for extension in agent_card["capabilities"]["extensions"]:
            assert "name" in extension
            assert "version" in extension
            assert "required" in extension

    def test_minimal_agent_card(self):
        """Test minimal agent card with only required fields."""
        minimal_card = {
            "name": "Minimal Agent",
            "description": "A minimal agent with only required fields",
            "version": "1.0.0",
            "protocolVersion": "1.0.0",
            "url": "https://minimal.example.com",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": "minimal-skill",
                    "name": "Minimal Skill",
                    "description": "A minimal skill",
                    "tags": ["minimal"]
                }
            ],
            "capabilities": {
                "pushNotifications": False,
                "taskOperations": ["create"]
            }
        }
        
        # Validate all required fields are present
        required_fields = [
            "name", "description", "version", "protocolVersion", "url",
            "defaultInputModes", "defaultOutputModes", "skills", "capabilities"
        ]
        
        for field in required_fields:
            assert field in minimal_card, f"Required field '{field}' is missing"
        
        # Validate skill required fields
        for skill in minimal_card["skills"]:
            skill_required_fields = ["id", "name", "description", "tags"]
            for field in skill_required_fields:
                assert field in skill, f"Required skill field '{field}' is missing"

    def test_agent_card_transport_validation(self):
        """Test agent card transport and interface validation."""
        agent_card = {
            "name": "Transport Agent",
            "description": "An agent with transport configuration",
            "version": "1.0.0",
            "protocolVersion": "1.0.0",
            "url": "https://transport.example.com",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": "transport-skill",
                    "name": "Transport Skill",
                    "description": "A skill with transport",
                    "tags": ["transport"]
                }
            ],
            "capabilities": {
                "pushNotifications": True,
                "taskOperations": ["create", "execute"]
            },
            "preferredTransport": "http",
            "additionalInterfaces": [
                {
                    "transport": "websocket",
                    "url": "wss://transport.example.com/ws"
                },
                {
                    "transport": "grpc",
                    "url": "grpc://transport.example.com:443"
                }
            ]
        }
        
        # Validate transport fields
        assert agent_card["preferredTransport"] in ["http", "websocket", "grpc"]
        
        for interface in agent_card["additionalInterfaces"]:
            assert interface["transport"] in ["http", "websocket", "grpc"]
            assert interface["url"].startswith(("http://", "https://", "ws://", "wss://", "grpc://"))

    def test_agent_card_security_schemes(self):
        """Test various security scheme configurations."""
        agent_card = {
            "name": "Secure Agent",
            "description": "An agent with comprehensive security",
            "version": "1.0.0",
            "protocolVersion": "1.0.0",
            "url": "https://secure.example.com",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [
                {
                    "id": "secure-skill",
                    "name": "Secure Skill",
                    "description": "A secure skill",
                    "tags": ["security"],
                    "security": [
                        {
                            "type": "oauth2",
                            "flows": {
                                "clientCredentials": {
                                    "tokenUrl": "https://secure.example.com/token",
                                    "scopes": {
                                        "read": "Read access",
                                        "write": "Write access"
                                    }
                                }
                            }
                        }
                    ]
                }
            ],
            "capabilities": {
                "pushNotifications": True,
                "taskOperations": ["create", "execute"]
            },
            "securitySchemes": [
                {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                },
                {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                },
                {
                    "type": "oauth2",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://secure.example.com/auth",
                            "tokenUrl": "https://secure.example.com/token",
                            "scopes": {
                                "read": "Read access",
                                "write": "Write access"
                            }
                        }
                    }
                }
            ]
        }
        
        # Validate security schemes
        for scheme in agent_card["securitySchemes"]:
            assert "type" in scheme
            scheme_type = scheme["type"]
            
            if scheme_type == "http":
                assert "scheme" in scheme
            elif scheme_type == "apiKey":
                assert "in" in scheme
                assert "name" in scheme
            elif scheme_type == "oauth2":
                assert "flows" in scheme