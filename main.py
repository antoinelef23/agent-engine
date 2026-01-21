"""
Single Agent System for Agent Engine Demonstration

This demonstrates a single multi-skilled agent that can handle
research, analysis, and coding tasks - optimized for Agent Engine deployment.
"""

from google.adk.agents import LlmAgent


# Tool functions for specialized tasks
def research_query(topic: str) -> str:
    """
    Research general knowledge topics and provide informative answers.

    Args:
        topic: The topic or question to research

    Returns:
        Research findings and explanations
    """
    return f"Researching topic: {topic}"


def analyze_data(data_description: str) -> str:
    """
    Analyze data patterns, trends, and generate insights.

    Args:
        data_description: Description of the data or pattern to analyze

    Returns:
        Analysis results with insights and recommendations
    """
    return f"Analyzing data: {data_description}"


def generate_code(requirements: str, language: str = "python") -> str:
    """
    Generate code based on requirements in various programming languages.

    Args:
        requirements: Description of what the code should do
        language: Programming language (default: python)

    Returns:
        Generated code with explanations
    """
    return f"Generating {language} code for: {requirements}"


def create_root_agent() -> LlmAgent:
    """
    Factory function to create the multi-skilled agent.
    This is the entry point for Agent Engine deployment.
    """

    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="multi_skilled_agent",
        description="A versatile AI agent capable of research, data analysis, and code generation",
        instruction="""You are a highly capable AI assistant with expertise in three main areas:

**1. Research & Knowledge**
- Answer questions about history, science, culture, technology, and more
- Provide accurate, well-researched information
- Explain complex topics in clear, understandable terms
- Use the research_query tool when you need to gather information

**2. Data Analysis**
- Analyze trends, patterns, and datasets
- Perform statistical analysis and generate insights
- Identify correlations, anomalies, and trends
- Provide actionable recommendations based on data
- Use the analyze_data tool when analyzing numerical data or patterns

**3. Code Generation & Programming**
- Write clean, efficient code in multiple programming languages (Python, JavaScript, Java, Go, etc.)
- Debug code and identify errors
- Explain programming concepts
- Follow best practices and design patterns
- Use the generate_code tool when creating code

**Your Approach:**
- Determine what type of task the user needs help with
- Use the appropriate tool(s) to assist them
- Provide comprehensive, helpful, and accurate responses
- Ask clarifying questions if the request is ambiguous

**Guidelines:**
- For general knowledge questions → Use research_query tool
- For data/trend analysis → Use analyze_data tool
- For programming tasks → Use generate_code tool
- Combine tools if the task requires multiple capabilities""",
        tools=[research_query, analyze_data, generate_code]
    )

    return agent


# For local testing
if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Skilled Agent System")
    print("=" * 60)
    print("\nInitializing agent...")

    try:
        # Create root agent
        root_agent = create_root_agent()
        print("✓ Agent created successfully")
        print(f"✓ Model: {root_agent.model}")
        print(f"✓ Tools: {len(root_agent.tools)}")

        # List tools
        print("\nAvailable tools:")
        for tool in root_agent.tools:
            tool_name = tool.__name__ if hasattr(tool, '__name__') else str(tool)
            print(f"  - {tool_name}")

        print("\n" + "=" * 60)
        print("Ready for deployment!")
        print("=" * 60)
        print("\nTo deploy:")
        print("  python deploy_simple.py --action deploy")

    except Exception as e:
        print(f"\n❌ Error creating agent: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
