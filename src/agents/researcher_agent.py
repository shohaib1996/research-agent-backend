# src/agents/researcher_agent.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from src.tools.web_search import WebSearchTool


class ResearcherAgent:
    """
    Researcher with caching support and parallel searches.
    """

    def __init__(self, db_helper=None):
        # Pass db_helper to search tool for caching
        self.search_tool = WebSearchTool(db_helper=db_helper)

    def research(self, questions: list, use_cache: bool = True) -> str:
        """
        Research with parallel searches (no per-question LLM calls).
        """
        all_findings = []

        # Run searches in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_question = {
                executor.submit(
                    self.search_tool.search, question, 3, use_cache
                ): question
                for question in questions
            }

            for future in as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    search_results = future.result()
                    all_findings.append(f"## {question}\n{search_results}\n")
                except Exception as e:
                    all_findings.append(f"## {question}\nSearch failed: {e}\n")

        return "\n".join(all_findings)
