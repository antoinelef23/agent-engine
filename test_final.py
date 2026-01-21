"""
Final test script for the deployed agent
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
    print("=" * 70)
    print("🤖 Multi-Agent System - Deployment Test")
    print("=" * 70)

    agent_id = "projects/26282080111/locations/europe-west1/reasoningEngines/4548582847086067712"
    print(f"\n📡 Connecting to: ...{agent_id[-20:]}")

    agent = agent_engines.AgentEngine(agent_id)
    print("✅ Connected successfully!\n")

    # Test queries for each specialized agent
    test_queries = [
        {
            "name": "🔬 Research Agent",
            "query": "What is quantum computing?",
            "expected": "research_agent"
        },
        {
            "name": "📊 Analysis Agent",
            "query": "Analyze this trend: 100, 150, 225, 340, 510. What pattern do you see?",
            "expected": "analysis_agent"
        },
        {
            "name": "💻 Code Agent",
            "query": "Write a Python function to check if a number is prime",
            "expected": "code_agent"
        }
    ]

    for i, test in enumerate(test_queries, 1):
        print("=" * 70)
        print(f"Test {i}/3: {test['name']}")
        print("=" * 70)
        print(f"Query: {test['query']}\n")

        try:
            # Create a session
            session = await agent.async_create_session(user_id="demo_user")
            session_id = session["id"]

            # Send query and collect response
            print("Response:")
            print("-" * 70)

            response_text = ""
            has_response = False

            async for event in agent.async_stream_query(
                user_id="demo_user",
                session_id=session_id,
                message=test['query']
            ):
                if isinstance(event, dict):
                    if 'text' in event and event['text']:
                        print(event['text'], end='', flush=True)
                        response_text += event['text']
                        has_response = True
                    elif 'code' in event:
                        if event['code'] != 200:
                            print(f"\n⚠️  Error code {event['code']}: {event.get('message', 'Unknown error')}")
                    elif event.get('type') == 'content':
                        content = event.get('content', '')
                        if content:
                            print(content, end='', flush=True)
                            response_text += content
                            has_response = True

            if not has_response:
                print("⚠️  No response received")

            print("\n" + "-" * 70)
            print(f"✅ Test {i} complete\n")

        except Exception as e:
            print(f"❌ Error: {e}\n")
            import traceback
            traceback.print_exc()

    print("=" * 70)
    print("🎉 All tests complete!")
    print("=" * 70)

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_agent())
