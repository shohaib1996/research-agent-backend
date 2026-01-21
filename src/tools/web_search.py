# src/tools/web_search.py

from tavily import TavilyClient
import os


class WebSearchTool:
    """
    Web search with caching support.
    """

    def __init__(self, db_helper=None):
        api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=api_key)
        self.db_helper = db_helper  # Optional database helper

    def search(self, query: str, max_results: int = 3, use_cache: bool = True) -> str:
        """
        Search with caching.

        Args:
            query: Search query
            max_results: Number of results
            use_cache: Whether to use cached results

        Returns:
            Formatted search results
        """

        # Check cache first
        if use_cache and self.db_helper:
            cached = self.db_helper.get_cached_search(query)
            if cached:
                print(f"   💾 Using cached results for: {query[:50]}...")
                return cached

        try:
            # Perform search
            print(f"   🌐 Searching web for: {query[:50]}...")
            response = self.client.search(query=query, max_results=max_results)

            # Format results
            results = []
            for i, result in enumerate(response.get("results", []), 1):
                title = result.get("title", "No title")
                content = result.get("content", "No content")
                url = result.get("url", "")

                results.append(f"{i}. {title}\n{content}\nSource: {url}\n")

            formatted_results = "\n".join(results) if results else "No results found"

            # Cache the results
            if self.db_helper:
                self.db_helper.cache_search_result(query, formatted_results)

            return formatted_results

        except Exception as e:
            return f"Search failed: {str(e)}"
