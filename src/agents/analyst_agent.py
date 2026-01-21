# src/agents/analyst_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class AnalystAgent:
    """
    Agent that synthesizes research into final answer.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=0.5, api_key=os.getenv("OPENAI_API_KEY")
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a research analyst. Create a comprehensive answer based on the research findings.

Your answer should:
- Be well-structured
- Cite key findings
- Be accurate and informative""",
                ),
                (
                    "user",
                    """Original Question: {question}

Research Plan: {plan}

Research Findings:
{findings}

Provide a comprehensive answer to the original question.""",
                ),
            ]
        )

    def analyze(self, question: str, plan: str, findings: str) -> str:
        """
        Synthesize final answer.

        Args:
            question: Original question
            plan: Research plan
            findings: Research findings

        Returns:
            Final comprehensive answer
        """
        chain = self.prompt | self.llm
        response = chain.invoke(
            {"question": question, "plan": plan, "findings": findings}
        )

        return response.content
