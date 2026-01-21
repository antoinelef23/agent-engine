# Multi-Agent System for Google Cloud Agent Engine

A demonstration of a sophisticated multi-agent system deployed on Google Cloud's Agent Engine, showcasing orchestration patterns and specialized agent capabilities.

## 🏗️ Architecture

This project implements an **orchestrator pattern** with three specialized sub-agents:

```
┌─────────────────────────────────────────┐
│      Orchestrator Agent                 │
│  (Routes queries to specialists)        │
└─────────────┬───────────────────────────┘
              │
       ┌──────┴──────┬─────────────┐
       │             │             │
       ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Research │  │ Analysis │  │   Code   │
│  Agent   │  │  Agent   │  │  Agent   │
└──────────┘  └──────────┘  └──────────┘
```

### Agent Capabilities

1. **Orchestrator Agent**
   - Intelligently routes user queries to appropriate specialists
   - Analyzes query intent and context
   - Coordinates responses from sub-agents

2. **Research Agent**
   - General knowledge and information retrieval
   - Fact-checking and explanations
   - Historical, scientific, and cultural queries

3. **Analysis Agent**
   - Data analysis and statistical insights
   - Pattern recognition and trend identification
   - Visualization recommendations

4. **Code Agent**
   - Code generation in multiple languages
   - Debugging and code review
   - Algorithm design and best practices

## 📋 Prerequisites

- **Python**: 3.9 to 3.13
- **GCP Project**: With billing enabled
- **APIs Enabled**:
  - Vertex AI API
  - Cloud Storage API
- **Tools**:
  - `gcloud` CLI installed and authenticated
  - `make` utility

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the project
cd "agent engine"

# Copy environment template
cp .env.example .env

# Edit .env with your GCP project details
nano .env  # or your preferred editor
```

### 2. Configure Environment

Edit `.env`:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
STAGING_BUCKET=gs://your-project-id-agent-staging
```

### 3. Install Dependencies

```bash
# Install Python dependencies
make install

# Or manually:
pip install -r requirements.txt
```

### 4. Set Up GCP Environment

```bash
# Authenticate with GCP
gcloud auth application-default login

# Enable required APIs and create staging bucket
make setup
```

### 5. Deploy to Agent Engine

```bash
# Deploy the multi-agent system
make deploy

# This will:
# - Deploy the orchestrator and sub-agents
# - Run initial tests
# - Display the resource name for future reference
```

## 🧪 Testing

### Local Testing

Test the agent locally before deployment:

```bash
make test-local
```

Or run directly:
```bash
python main.py
```

### Test Deployed Agent

After deployment, test the remote agent:

```bash
# Set the resource name from deployment output
export RESOURCE_NAME="projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID"

# Run remote tests
make test-remote RESOURCE_NAME=$RESOURCE_NAME
```

## 📦 Project Structure

```
agent engine/
├── main.py                      # Orchestrator agent entry point
├── deploy.py                    # Deployment script
├── requirements.txt             # Python dependencies
├── Makefile                     # Automation commands
├── .env.example                 # Environment template
├── README.md                    # This file
├── agents/                      # Specialized agents
│   ├── __init__.py
│   ├── research_agent.py       # Research specialist
│   ├── analysis_agent.py       # Analysis specialist
│   └── code_agent.py           # Code specialist
├── config/                      # Configuration modules
│   ├── __init__.py
│   └── deployment_config.py    # Deployment settings
└── tests/                       # Unit tests
    ├── __init__.py
    └── test_agents.py          # Agent tests
```

## 🔧 Usage

### Using the Deployed Agent

#### Python SDK

```python
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(
    project="YOUR_PROJECT_ID",
    location="us-central1"
)

# Connect to deployed agent
agent = agent_engines.AgentEngine("YOUR_RESOURCE_NAME")

# Create session
session = agent.create_session()

# Send queries
response = session.send_message("What is quantum computing?")
print(response.content)

response = session.send_message("Analyze this trend: 10, 20, 40, 80")
print(response.content)

response = session.send_message("Write a Python function to sort a list")
print(response.content)
```

#### REST API

```bash
# Create session
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID/sessions" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"

# Send message
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT/locations/us-central1/agents/YOUR_AGENT_ID/sessions/SESSION_ID:query" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

### Example Queries

The orchestrator will automatically route these to the appropriate agent:

**Research Queries:**
- "What is the history of the internet?"
- "Explain photosynthesis"
- "Who invented the telephone?"

**Analysis Queries:**
- "Analyze this sales trend: 100, 150, 225, 340"
- "What patterns do you see in: 2, 4, 8, 16, 32?"
- "Compare performance of product A (1000 units @ $10) vs product B (500 units @ $25)"

**Code Queries:**
- "Write a Python function to check if a string is a palindrome"
- "Debug this code: def add(a, b): return a + b + c"
- "Create a JavaScript function to validate email addresses"

## 🛠️ Development

### Running Tests

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agents --cov=config
```

### Modifying Agents

1. **Edit agent instructions**: Modify the instructions in `agents/*_agent.py`
2. **Add new actions**: Create new functions and add them to agent actions
3. **Add new agents**: Create new agent files and import them in `main.py`
4. **Test locally**: Run `make test-local` before deploying

### Deployment Options

```bash
# Deploy with custom configuration
python deploy.py \
  --project-id your-project \
  --location us-central1 \
  --staging-bucket gs://your-bucket

# Deploy without tracing (for production)
python deploy.py --no-tracing

# Deploy and test
python deploy.py --test
```

## 🔍 Monitoring and Debugging

### View Logs

```bash
# View deployment logs
gcloud logging read "resource.type=aiplatform.googleapis.com/Agent" \
  --project YOUR_PROJECT \
  --limit 50

# View with filtering
gcloud logging read "resource.type=aiplatform.googleapis.com/Agent AND severity>=ERROR" \
  --project YOUR_PROJECT
```

### Enable Tracing

Tracing is enabled by default and helps debug agent behavior:

```python
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True  # Enable detailed tracing
)
```

## 🧹 Cleanup

### Delete Deployed Agent

```bash
# Using deploy script
python deploy.py --action delete --resource-name YOUR_RESOURCE_NAME

# Using Python
from vertexai import agent_engines
agent = agent_engines.AgentEngine("YOUR_RESOURCE_NAME")
agent.delete(force=True)
```

### Clean Local Files

```bash
make clean
```

## 📚 Additional Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Agent Engine Guide](https://google.github.io/adk-docs/deploy/agent-engine/)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [ADK Python Repository](https://github.com/google/adk-python)

## 💡 Tips and Best Practices

1. **Start with local testing** before deploying to Agent Engine
2. **Use tracing** during development for better debugging
3. **Monitor costs** as Agent Engine incurs charges based on usage
4. **Version your agents** by keeping track of deployment configurations
5. **Test each sub-agent independently** before integrating with orchestrator
6. **Use clear instructions** for each agent to improve routing accuracy

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors:**
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**API Not Enabled:**
```bash
gcloud services enable aiplatform.googleapis.com
```

**Staging Bucket Doesn't Exist:**
```bash
gsutil mb -p YOUR_PROJECT gs://your-staging-bucket
```

**Import Errors:**
```bash
pip install --upgrade google-cloud-aiplatform[adk,agent_engines]
```

## 📄 License

This is a demonstration project for educational purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and customize for your needs!

---

**Built with Google ADK and Agent Engine** | **Powered by Gemini 2.0**
