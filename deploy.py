"""
Deployment script for Agent Engine

This script deploys the multi-agent system to Google Cloud Agent Engine.
"""

import argparse
import sys
import vertexai
from vertexai import agent_engines
from config.deployment_config import DeploymentConfig, get_default_config
from main import create_root_agent


def deploy_agent(config: DeploymentConfig, enable_tracing: bool = True) -> agent_engines.AgentEngine:
    """
    Deploy the multi-agent system to Agent Engine.

    Args:
        config: Deployment configuration
        enable_tracing: Enable tracing for debugging (default: True)

    Returns:
        Deployed AgentEngine instance
    """
    print("=" * 60)
    print("Agent Engine Deployment")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Project ID: {config.project_id}")
    print(f"  Location: {config.location}")
    print(f"  Staging Bucket: {config.staging_bucket}")
    print(f"  Tracing: {'Enabled' if enable_tracing else 'Disabled'}")
    print()

    # Initialize Vertex AI
    print("Initializing Vertex AI...")
    vertexai.init(
        project=config.project_id,
        location=config.location,
        staging_bucket=config.staging_bucket
    )

    # Create the root agent
    print("Creating multi-agent orchestrator...")
    root_agent = create_root_agent()

    # Wrap agent for Agent Engine
    print("Wrapping agent for Agent Engine...")
    app = agent_engines.AdkApp(
        agent=root_agent,
        enable_tracing=enable_tracing
    )

    # Deploy to Agent Engine
    print("\nDeploying to Agent Engine...")
    print("This may take several minutes...")
    print("Including local 'agents' package...")

    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "google-cloud-aiplatform[agent_engines]>=1.111",
            "google-adk==1.14.1"
        ]
    )

    print("\n" + "=" * 60)
    print("Deployment Successful!")
    print("=" * 60)
    print(f"\nAgent Engine ID: {remote_app.resource_name}")
    print(f"\nYou can now query your agent using:")
    print(f"  - Python SDK")
    print(f"  - REST API")
    print(f"  - Google Cloud Console")
    print()

    return remote_app


def test_deployed_agent(remote_app: agent_engines.AgentEngine):
    """
    Test the deployed agent with sample queries.

    Args:
        remote_app: Deployed AgentEngine instance
    """
    print("\n" + "=" * 60)
    print("Testing Deployed Agent")
    print("=" * 60)

    test_queries = [
        "What is the speed of light?",
        "Analyze this pattern: 5, 10, 20, 40, 80",
        "Write a Python function to reverse a string"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 60)

        try:
            # Create session
            session = remote_app.create_session()

            # Send query
            response = session.send_message(query)

            print(f"Response: {response.content}")

        except Exception as e:
            print(f"Error: {str(e)}")

    print("\n" + "=" * 60)


def delete_agent(resource_name: str, config: DeploymentConfig):
    """
    Delete a deployed agent from Agent Engine.

    Args:
        resource_name: Resource name of the deployed agent
        config: Deployment configuration
    """
    print(f"\nDeleting agent: {resource_name}")

    # Initialize Vertex AI
    vertexai.init(
        project=config.project_id,
        location=config.location,
        staging_bucket=config.staging_bucket
    )

    # Get the deployed agent
    remote_app = agent_engines.AgentEngine(resource_name)

    # Delete
    remote_app.delete(force=True)

    print("Agent deleted successfully!")


def main():
    """Main deployment script."""
    parser = argparse.ArgumentParser(
        description="Deploy multi-agent system to Agent Engine"
    )
    parser.add_argument(
        "--action",
        choices=["deploy", "test", "delete"],
        default="deploy",
        help="Action to perform (default: deploy)"
    )
    parser.add_argument(
        "--project-id",
        help="GCP project ID (or set GOOGLE_CLOUD_PROJECT env var)"
    )
    parser.add_argument(
        "--location",
        default="us-central1",
        help="GCP region (default: us-central1)"
    )
    parser.add_argument(
        "--staging-bucket",
        help="GCS staging bucket (or set STAGING_BUCKET env var)"
    )
    parser.add_argument(
        "--no-tracing",
        action="store_true",
        help="Disable tracing"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests after deployment"
    )
    parser.add_argument(
        "--resource-name",
        help="Resource name for delete action"
    )

    args = parser.parse_args()

    try:
        # Create configuration
        config = DeploymentConfig(
            project_id=args.project_id,
            location=args.location,
            staging_bucket=args.staging_bucket
        )

        if args.action == "deploy":
            # Deploy agent
            remote_app = deploy_agent(
                config=config,
                enable_tracing=not args.no_tracing
            )

            # Test if requested
            if args.test:
                test_deployed_agent(remote_app)

        elif args.action == "test":
            if not args.resource_name:
                print("Error: --resource-name required for test action")
                sys.exit(1)

            vertexai.init(
                project=config.project_id,
                location=config.location,
                staging_bucket=config.staging_bucket
            )
            remote_app = agent_engines.AgentEngine(args.resource_name)
            test_deployed_agent(remote_app)

        elif args.action == "delete":
            if not args.resource_name:
                print("Error: --resource-name required for delete action")
                sys.exit(1)

            delete_agent(args.resource_name, config)

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease provide configuration via:")
        print("  1. Command line arguments (--project-id, --staging-bucket)")
        print("  2. Environment variables (GOOGLE_CLOUD_PROJECT, STAGING_BUCKET)")
        sys.exit(1)

    except Exception as e:
        print(f"\nDeployment Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
