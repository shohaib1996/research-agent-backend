# src/agents/planner_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


class PlannerAgent:
    """
    Agent that breaks down complex questions into sub-questions.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,  # Lower = more focused
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a research planner. Break down complex questions into 2-3 simpler sub-questions.

Format your response as:
PLAN: [overall strategy]
SUB-QUESTIONS:
1. [first sub-question]
2. [second sub-question]
3. [third sub-question if needed]""",
                ),
                ("user", "Question: {question}"),
            ]
        )

    def plan(self, question: str) -> dict:
        """
        Create research plan.

        Returns:
            dict with 'plan' and 'sub_questions'
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"question": question})
        content = response.content

        # Parse response
        lines = content.split("\n")
        plan = ""
        sub_questions = []

        for line in lines:
            if line.startswith("PLAN:"):
                plan = line.replace("PLAN:", "").strip()
            elif line.strip() and (line[0].isdigit() or line.startswith("-")):
                # Extract question (remove numbering)
                q = line.split(".", 1)[-1].strip()
                if q:
                    sub_questions.append(q)

        return {
            "plan": plan or "Research the question comprehensively",
            "sub_questions": sub_questions or [question],
        }
