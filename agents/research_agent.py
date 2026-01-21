"""
Research Agent - Specialized in general knowledge and information retrieval
"""

from google.adk.agents import LlmAgent


def create_research_agent() -> LlmAgent:
    """
    Creates a research agent specialized in answering general knowledge questions,
    providing information, and conducting research tasks.
    """

    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="research_agent",
        description="Answers general knowledge questions, provides information, and conducts research on history, science, culture, and more",
        instruction="""You are a Research Agent, specialized in:

1. **General Knowledge**: Answering questions about history, science, culture, geography, etc.
2. **Information Retrieval**: Finding and synthesizing information on various topics
3. **Fact-Checking**: Providing accurate, well-researched answers
4. **Explanations**: Breaking down complex topics into understandable explanations

Your approach:
- Provide comprehensive yet concise answers
- Cite relevant context when helpful
- Admit when information is outside your knowledge cutoff
- Offer to explore related topics if relevant

Focus on accuracy, clarity, and helpfulness in all responses."""
    )

    return agent


# For standalone testing
if __name__ == "__main__":
    from google.adk.sessions import InMemoryChatSession

    agent = create_research_agent()
    session = InMemoryChatSession(agent=agent)

    # Test the research agent
    test_queries = [
        "What is the capital of France?",
        "Explain photosynthesis in simple terms",
        "Who invented the telephone?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = session.send_message(query)
        print(f"Response: {response.content}")
