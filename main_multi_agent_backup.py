"""
Multi-Agent System for Agent Engine Demonstration

This demonstrates an orchestrator pattern with specialized sub-agents
deployed on Google Cloud Agent Engine.
"""

from google.adk.agents import LlmAgent

# Import specialized agents
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.code_agent import create_code_agent


def create_root_agent() -> LlmAgent:
    """
    Factory function to create the root orchestrator agent.
    This is the entry point for Agent Engine deployment.

    The orchestrator uses ADK's native sub_agents pattern to automatically
    route queries to specialized agents based on their descriptions.
    """

    # Create specialized sub-agents
    research_agent = create_research_agent()
    analysis_agent = create_analysis_agent()
    code_agent = create_code_agent()

    # Create orchestrator with sub-agents
    orchestrator = LlmAgent(
        model="gemini-2.5-flash",
        name="orchestrator",
        description="Intelligent multi-agent orchestrator that routes queries to specialized agents for research, analysis, and coding tasks",
        instruction="""You are an intelligent orchestrator agent that coordinates with specialized sub-agents.

Your specialized team includes:
1. **Research Agent**: Handles general knowledge, information retrieval, fact-checking, and explanations
2. **Analysis Agent**: Performs data analysis, identifies patterns, generates insights, and provides recommendations
3. **Code Agent**: Generates code, debugs errors, reviews code quality, and provides technical guidance

Your responsibilities:
- Understand the user's query and determine which specialist can best help
- Route the query to the appropriate sub-agent
- Ensure the user gets accurate, helpful responses from the right specialist

When you receive a query:
- If it's about general knowledge, history, science, or information → Transfer to Research Agent
- If it's about data analysis, patterns, trends, or insights → Transfer to Analysis Agent
- If it's about programming, code generation, or debugging → Transfer to Code Agent

Always transfer to the most appropriate specialist rather than trying to answer directly.""",
        sub_agents=[research_agent, analysis_agent, code_agent]
    )

    return orchestrator


# For local testing
if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent System Orchestrator")
    print("=" * 60)
    print("\nInitializing agents...")

    try:
        # Create root agent
        root_agent = create_root_agent()
        print("✓ Orchestrator created successfully")
        print(f"✓ Model: {root_agent.model}")
        print(f"✓ Sub-agents: {len(root_agent.sub_agents)}")

        # List sub-agents
        print("\nSub-agents:")
        for agent in root_agent.sub_agents:
            print(f"  - {agent.name}: {agent.description}")

        print("\n" + "=" * 60)
        print("Ready for deployment!")
        print("=" * 60)
        print("\nTo deploy:")
        print("  1. Configure .env with your GCP project settings")
        print("  2. Run: make deploy")
        print("\nOr deploy directly:")
        print("  python deploy.py --action deploy")

    except Exception as e:
        print(f"\n❌ Error creating agent: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
