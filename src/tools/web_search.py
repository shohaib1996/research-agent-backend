# src/tools/web_search.py

from tavily import TavilyClient
import os


class WebSearchTool:
    """
    Tool for searching the web using Tavily.
    """

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 3) -> str:
        """
        Search the web and return results as text.

        Args:
            query: Search query
            max_results: Number of results to return

        Returns:
            Formatted search results as string
        """
        try:
            # Search using Tavily
            response = self.client.search(query=query, max_results=max_results)

            # Format results
            results = []
            for i, result in enumerate(response.get("results", []), 1):
                title = result.get("title", "No title")
                content = result.get("content", "No content")
                url = result.get("url", "")

                results.append(f"{i}. {title}\n{content}\nSource: {url}\n")

            return "\n".join(results) if results else "No results found"

        except Exception as e:
            return f"Search failed: {str(e)}"
