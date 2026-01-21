"""
Debug test script for the deployed agent
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
    print("Testing Deployed Agent (Debug Mode)")
    print("=" * 60)

    agent_id = "projects/26282080111/locations/europe-west1/reasoningEngines/5971720329335144448"
    print(f"\nConnecting to: {agent_id}")

    agent = agent_engines.AgentEngine(agent_id)
    print("✓ Connected successfully\n")

    # Test a single query
    query = "What is artificial intelligence?"
    print("=" * 60)
    print(f"Query: {query}")
    print("=" * 60)

    try:
        # Create a session
        session = await agent.async_create_session(user_id="demo_user")
        session_id = session["id"]
        print(f"Session ID: {session_id}\n")

        # Send query and stream response
        print("Raw Events:")
        print("-" * 60)
        event_count = 0
        async for event in agent.async_stream_query(
            user_id="demo_user",
            session_id=session_id,
            message=query
        ):
            event_count += 1
            print(f"\nEvent {event_count}:")
            print(f"Type: {type(event)}")
            print(f"Content: {event}")

        print(f"\nTotal events received: {event_count}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_agent())
