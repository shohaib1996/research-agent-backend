# src/agents/critic_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class CriticAgent:
    """
    Agent that evaluates answer quality and decides if improvement needed.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,  # Very focused for evaluation
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a quality evaluator. Rate the answer on a scale of 0.0 to 1.0.

Criteria:
- Completeness: Does it fully answer the question?
- Accuracy: Is the information correct and well-sourced?
- Clarity: Is it easy to understand?
- Depth: Does it provide sufficient detail?

Format your response EXACTLY as:
SCORE: [number between 0.0 and 1.0]
REASONING: [brief explanation]
NEEDS_IMPROVEMENT: [YES or NO]""",
                ),
                (
                    "user",
                    """Original Question: {question}

Answer to Evaluate:
{answer}

Evaluate this answer.""",
                ),
            ]
        )

    def evaluate(self, question: str, answer: str) -> dict:
        """
        Evaluate answer quality.

        Returns:
            dict with 'score', 'reasoning', 'needs_improvement'
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"question": question, "answer": answer})

        content = response.content

        # Parse response
        score = 0.7  # default
        needs_improvement = False
        reasoning = ""

        for line in content.split("\n"):
            if line.startswith("SCORE:"):
                try:
                    score = float(line.replace("SCORE:", "").strip())
                except (ValueError, AttributeError):
                    score = 0.7
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()
            elif line.startswith("NEEDS_IMPROVEMENT:"):
                needs_improvement = "YES" in line.upper()

        return {
            "score": score,
            "needs_improvement": needs_improvement,
            "reasoning": reasoning,
        }
