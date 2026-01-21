"""
Simplified deployment script for Agent Engine

This script deploys a single multi-skilled agent to Google Cloud Agent Engine.
"""

import argparse
import sys
import vertexai
from vertexai import agent_engines
from config.deployment_config import DeploymentConfig
from main_simple import create_root_agent


def deploy_agent(config: DeploymentConfig, enable_tracing: bool = True):
    """
    Deploy the multi-skilled agent to Agent Engine.

    Args:
        config: Deployment configuration
        enable_tracing: Enable tracing for debugging (default: True)

    Returns:
        Deployed AgentEngine instance
    """
    print("=" * 60)
    print("Agent Engine Deployment (Simplified)")
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
    print("Creating multi-skilled agent...")
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


def main():
    """Main deployment script."""
    parser = argparse.ArgumentParser(
        description="Deploy multi-skilled agent to Agent Engine"
    )
    parser.add_argument(
        "--action",
        choices=["deploy"],
        default="deploy",
        help="Action to perform (default: deploy)"
    )
    parser.add_argument(
        "--project-id",
        help="GCP project ID (or set GOOGLE_CLOUD_PROJECT env var)"
    )
    parser.add_argument(
        "--location",
        default="europe-west1",
        help="GCP region (default: europe-west1)"
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

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease provide configuration via:")
        print("  1. Command line arguments (--project-id, --staging-bucket)")
        print("  2. Environment variables (GOOGLE_CLOUD_PROJECT, STAGING_BUCKET)")
        sys.exit(1)

    except Exception as e:
        print(f"\nDeployment Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
