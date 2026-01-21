"""
Analysis Agent - Specialized in data analysis and insights
"""

from google.adk.agents import LlmAgent


def analyze_data(data_description: str) -> str:
    """
    Analyzes data patterns and provides insights.

    Args:
        data_description: Description of the data to analyze

    Returns:
        Analysis results and insights
    """
    return f"Analyzing: {data_description}\n\nBased on the data description, I'll provide statistical insights, identify patterns, and suggest interpretations."


def create_analysis_agent() -> LlmAgent:
    """
    Creates an analysis agent specialized in data analysis, statistics,
    pattern recognition, and generating insights.
    """

    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="analysis_agent",
        description="Performs data analysis, identifies patterns and trends, generates statistical insights, and provides actionable recommendations",
        instruction="""You are an Analysis Agent, specialized in:

1. **Data Analysis**: Examining datasets, identifying patterns and trends
2. **Statistical Analysis**: Performing statistical calculations and interpretations
3. **Insight Generation**: Extracting meaningful insights from data
4. **Pattern Recognition**: Identifying correlations, anomalies, and trends
5. **Visualization Suggestions**: Recommending appropriate charts and visualizations

Your approach:
- Break down complex data into understandable insights
- Provide statistical context and significance
- Identify key trends and patterns
- Suggest actionable recommendations based on data
- Use the analyze_data tool when explicit analysis is needed

Focus on accuracy, clarity, and actionable insights in all analyses.""",
        tools=[analyze_data]
    )

    return agent


# For standalone testing
if __name__ == "__main__":
    from google.adk.sessions import InMemoryChatSession

    agent = create_analysis_agent()
    session = InMemoryChatSession(agent=agent)

    # Test the analysis agent
    test_queries = [
        "Analyze this trend: sales increased from 100 to 150 to 225 over three quarters",
        "What patterns do you see in these numbers: 2, 4, 8, 16, 32?",
        "Compare the performance of two products: A sold 1000 units at $10, B sold 500 units at $25"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = session.send_message(query)
        print(f"Response: {response.content}")
