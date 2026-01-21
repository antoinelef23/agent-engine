"""
Quick test script for the deployed agent
"""

import asyncio
import vertexai
from vertexai import agent_engines

# Initialize Vertex AI
vertexai.init(
    project="hack-ai-unified-ai-platform",
    location="europe-west1"
)

async def test_agent():
    """Test the deployed agent with sample queries."""

    # Connect to deployed agent
    print("=" * 60)
    print("Testing Deployed Agent")
    print("=" * 60)

    agent_id = "projects/26282080111/locations/europe-west1/reasoningEngines/7124641833941991424"
    print(f"\nConnecting to: {agent_id}")

    agent = agent_engines.AgentEngine(agent_id)
    print("✓ Connected successfully\n")

    # Test queries
    test_queries = [
        ("Research Agent Test", "What is artificial intelligence?"),
        ("Analysis Agent Test", "Analyze this trend: 100, 150, 225, 340, 510"),
        ("Code Agent Test", "Write a Python function to check if a number is prime")
    ]

    for test_name, query in test_queries:
        print("=" * 60)
        print(f"{test_name}")
        print("=" * 60)
        print(f"Query: {query}\n")

        try:
            # Create a session for this query
            session = await agent.async_create_session(user_id="demo_user")
            session_id = session["id"]
            print(f"Session ID: {session_id}")

            # Send query and stream response
            print("Response:")
            full_response = ""
            async for event in agent.async_stream_query(
                user_id="demo_user",
                session_id=session_id,
                message=query
            ):
                # Collect and display response
                if hasattr(event, 'text'):
                    print(event.text, end='', flush=True)
                    full_response += event.text
                elif isinstance(event, dict) and 'text' in event:
                    print(event['text'], end='', flush=True)
                    full_response += event['text']

            print("\n")

        except Exception as e:
            print(f"Error: {e}\n")

    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_agent())
