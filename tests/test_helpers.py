# tests/test_helpers.py
"""
Helper functions and adapters for testing with generated models.
"""
from typing import Any, Dict, List, Optional, TypeVar, cast

from a2a_json_rpc.spec import (
    Artifact, Message, Part, TextPart, FilePart, DataPart,
    Role, TaskStatus, TaskState
)

T = TypeVar('T')

class PartAdapter:
    """Adapter to help test code access Part attributes."""
    
    @staticmethod
    def get_type(part: Any) -> str:
        """Get type from a part."""
        # Since Part is a RootModel, check its root
        if hasattr(part, 'root'):
            root = part.root
            if hasattr(root, 'type'):
                return root.type
        # Direct access for instances of concrete types
        if isinstance(part, (TextPart, FilePart, DataPart)) and hasattr(part, 'type'):
            return part.type
        return ""
    
    @staticmethod
    def get_text(part: Any) -> Optional[str]:
        """Get text from a part."""
        # For TextPart
        if hasattr(part, 'root'):
            root = part.root
            if hasattr(root, 'text'):
                return root.text
        # Direct access
        if hasattr(part, 'text'):
            return part.text
        return None
    
    @staticmethod
    def get_data(part: Any) -> Optional[Dict[str, Any]]:
        """Get data from a part."""
        # For DataPart
        if hasattr(part, 'root'):
            root = part.root
            if hasattr(root, 'data'):
                return root.data
        # Direct access
        if hasattr(part, 'data'):
            return part.data
        return None
    
    @staticmethod
    def get_file(part: Any) -> Optional[Any]:
        """Get file from a part."""
        # For FilePart
        if hasattr(part, 'root'):
            root = part.root
            if hasattr(root, 'file'):
                return root.file
        # Direct access
        if hasattr(part, 'file'):
            return part.file
        return None


class MessageAdapter:
    """Adapter to help test code work with Message."""
    
    @staticmethod
    def get_parts(message: Message) -> List[Any]:
        """Get a list of adapted parts from a message."""
        return [PartAdapter.get_adapted_part(p) for p in message.parts]
    
    @staticmethod
    def get_role_value(message: Message) -> str:
        """Get the string value of a message role."""
        return str(message.role.value)


class ArtifactAdapter:
    """Adapter to help test code work with Artifact."""
    
    @staticmethod
    def get_parts(artifact: Artifact) -> List[Any]:
        """Get a list of adapted parts from an artifact."""
        return [PartAdapter.get_adapted_part(p) for p in artifact.parts]


# Add more adapter classes as needed for other models