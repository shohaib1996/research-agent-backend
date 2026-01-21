# src/agents/refiner_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class RefinerAgent:
    """
    Agent that refines and improves answers based on critic feedback.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.4,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a research question specialist. Generate 2-3 refined research questions to improve answer quality.

Based on the current answer's weaknesses, create better sub-questions that will:
- Fill knowledge gaps
- Add more depth and detail
- Address unclear or incomplete areas
- Improve overall answer quality

Format your response as a numbered list:
1. [first refined question]
2. [second refined question]
3. [third refined question if needed]""",
                ),
                (
                    "user",
                    """Original Question: {question}

Current Answer:
{answer}

Quality Feedback: {reasoning}

Generate 2-3 refined research questions to improve this answer.""",
                ),
            ]
        )

    def refine(self, question: str, answer: str, reasoning: str) -> list:
        """
        Generate refined research questions based on quality feedback.

        Args:
            question: Original question
            answer: Current answer that needs improvement
            reasoning: Feedback on what needs improvement

        Returns:
            List of refined research questions
        """
        chain = self.prompt | self.llm
        response = chain.invoke(
            {
                "question": question,
                "answer": answer,
                "reasoning": reasoning,
            }
        )

        # Parse numbered list into questions
        content = response.content
        questions = []

        for line in content.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                # Extract question (remove numbering)
                q = line.split(".", 1)[-1].strip()
                if q:
                    questions.append(q)

        # Fallback to original question if parsing fails
        return questions if questions else [question]
