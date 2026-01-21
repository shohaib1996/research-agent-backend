# src/agents/researcher_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from src.tools.web_search import WebSearchTool


class ResearcherAgent:
    """
    Agent that searches the web for information.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=0.3, api_key=os.getenv("OPENAI_API_KEY")
        )

        self.search_tool = WebSearchTool()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a research analyst. Summarize the search results to answer the question.",
                ),
                (
                    "user",
                    """Question: {question}

Search Results:
{search_results}

Provide a clear, concise summary based on these results.""",
                ),
            ]
        )

    def research(self, questions: list) -> str:
        """
        Research multiple questions.

        Args:
            questions: List of questions to research

        Returns:
            Combined research findings
        """
        all_findings = []

        for question in questions:
            # Search the web
            search_results = self.search_tool.search(question, max_results=3)

            # Summarize with LLM
            chain = self.prompt | self.llm
            response = chain.invoke(
                {"question": question, "search_results": search_results}
            )

            all_findings.append(f"Q: {question}\nA: {response.content}\n")

        return "\n".join(all_findings)
