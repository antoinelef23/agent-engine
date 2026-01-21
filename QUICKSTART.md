# Quick Start Guide

Get your multi-agent system deployed to Agent Engine in 5 minutes!

## Prerequisites Check

- [ ] Python 3.9-3.13 installed
- [ ] GCP project with billing enabled
- [ ] `gcloud` CLI installed

## Step-by-Step Deployment

### 1. Authenticate (1 minute)

```bash
gcloud auth application-default login
```

### 2. Configure Project (1 minute)

```bash
# Copy the environment template
cp .env.example .env

# Edit with your details
export GOOGLE_CLOUD_PROJECT="your-project-id"
export STAGING_BUCKET="gs://your-project-id-agent-staging"
```

Or edit `.env` file directly:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
STAGING_BUCKET=gs://your-project-id-agent-staging
```

### 3. Install Dependencies (1 minute)

```bash
make install
```

### 4. Setup GCP (1 minute)

```bash
# This enables APIs and creates the staging bucket
make setup
```

### 5. Deploy! (1-2 minutes)

```bash
# Deploy and test
make deploy
```

## What Happens During Deployment?

1. ✅ Vertex AI initialization
2. ✅ Agent compilation and packaging
3. ✅ Upload to Agent Engine
4. ✅ Deployment and health checks
5. ✅ Automated testing

## Test Your Agent

After deployment, you'll see output like:
```
Agent Engine ID: projects/YOUR_PROJECT/locations/us-central1/agents/12345
```

Save this ID! You can test your agent:

### Python
```python
import vertexai
from vertexai import agent_engines

vertexai.init(project="YOUR_PROJECT", location="us-central1")
agent = agent_engines.AgentEngine("YOUR_AGENT_ID")
session = agent.create_session()

response = session.send_message("What is AI?")
print(response.content)
```

### Command Line
```bash
# Test locally first
python main.py

# Test deployed version
make test-remote RESOURCE_NAME="YOUR_AGENT_ID"
```

## Example Queries to Try

```python
# Research questions
"What is quantum computing?"
"Explain the theory of relativity"

# Analysis tasks
"Analyze this trend: 100, 150, 225, 340, 510"
"What's the pattern in: 1, 1, 2, 3, 5, 8, 13?"

# Code generation
"Write a Python function to find prime numbers"
"Create a REST API endpoint in Flask"
```

## Troubleshooting

### Error: "Project not found"
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Error: "API not enabled"
```bash
gcloud services enable aiplatform.googleapis.com
```

### Error: "Bucket does not exist"
```bash
gsutil mb -p YOUR_PROJECT gs://your-bucket-name
```

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🔧 Customize agent instructions in `agents/`
- 🧪 Run tests: `pytest tests/`
- 📊 Monitor in [GCP Console](https://console.cloud.google.com/vertex-ai)

## Need Help?

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Agent Engine Guide](https://google.github.io/adk-docs/deploy/agent-engine/)

---

**Time to deployment: ~5 minutes** ⚡
