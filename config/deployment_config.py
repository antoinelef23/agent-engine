"""
Deployment configuration for Agent Engine
"""

import os
from typing import Optional


class DeploymentConfig:
    """Configuration settings for deploying to Agent Engine."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        staging_bucket: Optional[str] = None
    ):
        """
        Initialize deployment configuration.

        Args:
            project_id: GCP project ID (defaults to env var GOOGLE_CLOUD_PROJECT)
            location: GCP region (defaults to env var GOOGLE_CLOUD_LOCATION or 'us-central1')
            staging_bucket: GCS bucket for staging (defaults to env var STAGING_BUCKET or 'gs://{project_id}-agent-staging')
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        if staging_bucket:
            self.staging_bucket = staging_bucket
        elif os.getenv("STAGING_BUCKET"):
            self.staging_bucket = os.getenv("STAGING_BUCKET")
        else:
            self.staging_bucket = f"gs://{self.project_id}-agent-staging" if self.project_id else None

        # Validate configuration
        self._validate()

    def _validate(self):
        """Validate that required configuration is present."""
        if not self.project_id:
            raise ValueError(
                "project_id must be provided or set via GOOGLE_CLOUD_PROJECT environment variable"
            )

        if not self.staging_bucket:
            raise ValueError(
                "staging_bucket must be provided or set via STAGING_BUCKET environment variable"
            )

    def to_dict(self):
        """Convert configuration to dictionary."""
        return {
            "project_id": self.project_id,
            "location": self.location,
            "staging_bucket": self.staging_bucket
        }

    def __repr__(self):
        return f"DeploymentConfig(project_id={self.project_id}, location={self.location}, staging_bucket={self.staging_bucket})"


# Default configuration instance
def get_default_config() -> DeploymentConfig:
    """Get default deployment configuration from environment variables."""
    return DeploymentConfig()
