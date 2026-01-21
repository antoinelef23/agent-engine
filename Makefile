.PHONY: help install setup deploy test clean

help:
	@echo "Multi-Agent System for Agent Engine"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make setup        - Set up GCP environment (enable APIs, create bucket)"
	@echo "  make deploy       - Deploy agent to Agent Engine"
	@echo "  make test-local   - Test agent locally"
	@echo "  make test-remote  - Test deployed agent (requires RESOURCE_NAME)"
	@echo "  make clean        - Clean up Python cache files"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

setup:
	@echo "Setting up GCP environment..."
	@if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
		echo "Error: GOOGLE_CLOUD_PROJECT not set"; \
		exit 1; \
	fi
	@echo "Enabling required APIs..."
	gcloud services enable aiplatform.googleapis.com --project=$$GOOGLE_CLOUD_PROJECT
	gcloud services enable storage.googleapis.com --project=$$GOOGLE_CLOUD_PROJECT
	@echo "Creating staging bucket..."
	gsutil mb -p $$GOOGLE_CLOUD_PROJECT $$STAGING_BUCKET 2>/dev/null || true
	@echo "✓ Setup complete"

deploy:
	@echo "Deploying to Agent Engine..."
	@if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
		echo "Error: GOOGLE_CLOUD_PROJECT not set"; \
		echo "Please set environment variables or use .env file"; \
		exit 1; \
	fi
	python deploy.py --action deploy --test
	@echo "✓ Deployment complete"

test-local:
	@echo "Testing agent locally..."
	python main.py
	@echo "✓ Local test complete"

test-remote:
	@if [ -z "$$RESOURCE_NAME" ]; then \
		echo "Error: RESOURCE_NAME not set"; \
		echo "Usage: make test-remote RESOURCE_NAME=projects/.../agents/..."; \
		exit 1; \
	fi
	python deploy.py --action test --resource-name $$RESOURCE_NAME

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Clean complete"
