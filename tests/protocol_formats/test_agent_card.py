# tests/protocol_formats/test_agent_card.py
"""
Tests for A2A Agent Card format based on the specification.

This file contains tests that validate the format of Agent Cards
as defined in the A2A protocol specification.
"""
import pytest
import json
from uuid import uuid4


class TestAgentCardFormat:
    """Test the Agent Card format."""

    def test_agent_card_format(self):
        """Test the agent card format matches the specification."""
        # Example from the spec
        agent_card = {
            "name": "Google Maps Agent",
            "description": "Plan routes, remember places, and generate directions",
            "url": "https://maps-agent.google.com",
            "provider": {
                "organization": "Google",
                "url": "https://google.com"
            },
            "version": "1.0.0",
            "authentication": {
                "schemes": "OAuth2"
            },
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain", "application/html"],
            "capabilities": {
                "streaming": True,
                "pushNotifications": False
            },
            "skills": [
                {
                    "id": "route-planner",
                    "name": "Route planning",
                    "description": "Helps plan routing between two locations",
                    "tags": ["maps", "routing", "navigation"],
                    "examples": [
                        "plan my route from Sunnyvale to Mountain View",
                        "what's the commute time from Sunnyvale to San Francisco at 9AM",
                        "create turn by turn directions from Sunnyvale to Mountain View"
                    ],
                    "outputModes": ["application/html", "video/mp4"]
                },
                {
                    "id": "custom-map",
                    "name": "My Map",
                    "description": "Manage a custom map with your own saved places",
                    "tags": ["custom-map", "saved-places"],
                    "examples": [
                        "show me my favorite restaurants on the map",
                        "create a visual of all places I've visited in the past year"
                    ],
                    "outputModes": ["application/html"]
                }
            ]
        }
        
        # Basic validation
        assert "name" in agent_card
        assert "description" in agent_card
        assert "url" in agent_card
        assert "version" in agent_card
        assert "capabilities" in agent_card
        assert "skills" in agent_card
        
        # Capability validation
        assert "streaming" in agent_card["capabilities"]
        assert "pushNotifications" in agent_card["capabilities"]
        
        # Skills validation
        for skill in agent_card["skills"]:
            assert "id" in skill
            assert "name" in skill
            assert "description" in skill
            assert "tags" in skill
            
        # Validate skill details
        planner_skill = agent_card["skills"][0]
        assert planner_skill["id"] == "route-planner"
        assert "examples" in planner_skill
        assert len(planner_skill["examples"]) > 0
        assert "outputModes" in planner_skill
        assert "video/mp4" in planner_skill["outputModes"]