"""
Unit tests for the multi-agent system
"""

import pytest
from google.adk.sessions import InMemoryChatSession
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.code_agent import create_code_agent
from main import create_root_agent


class TestResearchAgent:
    """Tests for the Research Agent."""

    def test_create_research_agent(self):
        """Test that research agent can be created."""
        agent = create_research_agent()
        assert agent is not None
        assert agent.name == "research_agent"

    def test_research_agent_response(self):
        """Test that research agent can respond to queries."""
        agent = create_research_agent()
        session = InMemoryChatSession(agent=agent)
        response = session.send_message("What is Python?")
        assert response is not None
        assert len(response.content) > 0


class TestAnalysisAgent:
    """Tests for the Analysis Agent."""

    def test_create_analysis_agent(self):
        """Test that analysis agent can be created."""
        agent = create_analysis_agent()
        assert agent is not None
        assert agent.name == "analysis_agent"

    def test_analysis_agent_response(self):
        """Test that analysis agent can respond to queries."""
        agent = create_analysis_agent()
        session = InMemoryChatSession(agent=agent)
        response = session.send_message("Analyze the trend: 1, 2, 4, 8, 16")
        assert response is not None
        assert len(response.content) > 0


class TestCodeAgent:
    """Tests for the Code Agent."""

    def test_create_code_agent(self):
        """Test that code agent can be created."""
        agent = create_code_agent()
        assert agent is not None
        assert agent.name == "code_agent"

    def test_code_agent_response(self):
        """Test that code agent can respond to queries."""
        agent = create_code_agent()
        session = InMemoryChatSession(agent=agent)
        response = session.send_message("Write a function to add two numbers")
        assert response is not None
        assert len(response.content) > 0


class TestOrchestratorAgent:
    """Tests for the Orchestrator Agent."""

    def test_create_orchestrator(self):
        """Test that orchestrator can be created."""
        agent = create_root_agent()
        assert agent is not None
        assert agent.name == "orchestrator"

    def test_orchestrator_routing(self):
        """Test that orchestrator can route queries."""
        agent = create_root_agent()
        session = InMemoryChatSession(agent=agent)

        # Test research query
        response = session.send_message("What is artificial intelligence?")
        assert response is not None
        assert len(response.content) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
