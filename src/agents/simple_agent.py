# src/agents/simple_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class SimpleAgent:
    """
    A simple agent that uses GPT to answer questions.
    """

    def __init__(self):
        # Initialize the LLM (GPT-4)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Cheaper, faster model
            temperature=0.7,  # 0 = focused, 1 = creative
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Create a prompt template
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful research assistant. Provide clear, concise answers.",
                ),
                ("user", "{question}"),
            ]
        )

    def answer(self, question: str) -> str:
        """
        Answer a question using GPT.

        Args:
            question: The user's question

        Returns:
            AI-generated answer
        """
        # Create the chain: prompt → LLM
        chain = self.prompt | self.llm

        # Run it
        response = chain.invoke({"question": question})

        # Extract the text
        return response.content
