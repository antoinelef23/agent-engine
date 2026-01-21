"""
Code Agent - Specialized in programming and software development
"""

from google.adk.agents import LlmAgent


def generate_code(requirements: str, language: str = "python") -> str:
    """
    Generates code based on requirements.

    Args:
        requirements: Description of what the code should do
        language: Programming language (default: python)

    Returns:
        Generated code with explanations
    """
    return f"""Generating {language} code for: {requirements}

I'll provide clean, well-documented code following best practices for {language}."""


def debug_code(code: str, error: str) -> str:
    """
    Helps debug code and fix errors.

    Args:
        code: The code that has issues
        error: Error message or description of the problem

    Returns:
        Debugging suggestions and fixes
    """
    return f"""Debugging the provided code with error: {error}

I'll analyze the code, identify the issue, and provide a fix with explanation."""


def create_code_agent() -> LlmAgent:
    """
    Creates a code agent specialized in programming, code generation,
    debugging, and technical implementation tasks.
    """

    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="code_agent",
        description="Generates clean code in multiple languages, debugs errors, reviews code quality, and provides technical implementation guidance",
        instruction="""You are a Code Agent, specialized in:

1. **Code Generation**: Writing clean, efficient code in various languages
2. **Debugging**: Identifying and fixing code errors
3. **Code Review**: Analyzing code quality and suggesting improvements
4. **Algorithm Design**: Creating efficient algorithms and data structures
5. **Best Practices**: Following language-specific conventions and patterns
6. **Documentation**: Explaining code and providing clear comments

Supported languages: Python, JavaScript, Java, Go, TypeScript, and more.

Your approach:
- Write clean, readable, and well-documented code
- Follow best practices and design patterns
- Explain your implementation choices
- Consider edge cases and error handling
- Provide examples and usage instructions
- Use tools when generating or debugging code

Focus on code quality, maintainability, and clear explanations.""",
        tools=[generate_code, debug_code]
    )

    return agent


# For standalone testing
if __name__ == "__main__":
    from google.adk.sessions import InMemoryChatSession

    agent = create_code_agent()
    session = InMemoryChatSession(agent=agent)

    # Test the code agent
    test_queries = [
        "Write a Python function to check if a number is prime",
        "Debug this code: def add(a, b): return a + b + c",
        "Create a JavaScript function to validate email addresses"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = session.send_message(query)
        print(f"Response: {response.content}")
