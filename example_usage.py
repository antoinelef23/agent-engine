"""
Example usage of the deployed multi-agent system

This script demonstrates how to interact with a deployed Agent Engine agent.
"""

import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def example_basic_usage():
    """Basic example of using the deployed agent."""

    print("=" * 60)
    print("Basic Usage Example")
    print("=" * 60)

    # Initialize Vertex AI
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)

    # Connect to deployed agent (replace with your actual resource name)
    resource_name = input("Enter your Agent Engine resource name: ")
    agent = agent_engines.AgentEngine(resource_name)

    # Create a session
    session = agent.create_session()
    print(f"\n✓ Session created: {session.resource_name}\n")

    # Send some queries
    queries = [
        "What is artificial intelligence?",
        "Analyze the trend in these sales figures: 100, 125, 155, 195, 240",
        "Write a Python function to check if a number is even"
    ]

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 60)

        response = session.send_message(query)
        print(f"Response: {response.content}\n")


def example_interactive_session():
    """Interactive example allowing user input."""

    print("\n" + "=" * 60)
    print("Interactive Session Example")
    print("=" * 60)
    print("Type 'quit' to exit\n")

    # Initialize
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)

    resource_name = input("Enter your Agent Engine resource name: ")
    agent = agent_engines.AgentEngine(resource_name)

    session = agent.create_session()
    print(f"\n✓ Connected to agent\n")

    # Interactive loop
    while True:
        query = input("You: ")

        if query.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        if not query.strip():
            continue

        try:
            response = session.send_message(query)
            print(f"Agent: {response.content}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def example_with_context():
    """Example showing multi-turn conversation with context."""

    print("\n" + "=" * 60)
    print("Multi-turn Conversation Example")
    print("=" * 60)

    # Initialize
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)

    resource_name = input("Enter your Agent Engine resource name: ")
    agent = agent_engines.AgentEngine(resource_name)

    session = agent.create_session()

    # Multi-turn conversation
    conversation = [
        "What is machine learning?",
        "Can you give me an example?",
        "How would I implement that in Python?",
        "What libraries would I need?"
    ]

    for query in conversation:
        print(f"\nYou: {query}")
        response = session.send_message(query)
        print(f"Agent: {response.content}")


def example_error_handling():
    """Example with proper error handling."""

    print("\n" + "=" * 60)
    print("Error Handling Example")
    print("=" * 60)

    try:
        # Initialize
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT not set in environment")

        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        vertexai.init(project=project_id, location=location)

        resource_name = input("Enter your Agent Engine resource name: ")

        # Connect to agent
        agent = agent_engines.AgentEngine(resource_name)

        # Create session with timeout handling
        session = agent.create_session()

        # Send query
        query = "Explain quantum computing"
        print(f"\nQuery: {query}")

        response = session.send_message(query)
        print(f"Response: {response.content}")

        print("\n✓ Success!")

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set GOOGLE_CLOUD_PROJECT in your .env file")

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your resource name is correct")
        print("2. Verify the agent is deployed: gcloud ai agents list")
        print("3. Ensure you're authenticated: gcloud auth application-default login")


def main():
    """Main function with menu."""

    print("\n" + "=" * 60)
    print("Multi-Agent System - Example Usage")
    print("=" * 60)

    examples = {
        "1": ("Basic Usage", example_basic_usage),
        "2": ("Interactive Session", example_interactive_session),
        "3": ("Multi-turn Conversation", example_with_context),
        "4": ("Error Handling", example_error_handling),
    }

    print("\nSelect an example:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. Quit")

    choice = input("\nYour choice: ").strip()

    if choice.lower() == 'q':
        print("Goodbye!")
        return

    if choice in examples:
        _, example_func = examples[choice]
        example_func()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    # Check for .env file
    if not os.path.exists(".env"):
        print("Warning: .env file not found")
        print("Copy .env.example to .env and configure your settings\n")

    main()
