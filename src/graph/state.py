# src/graph/state.py

from typing import TypedDict


class ResearchState(TypedDict):
    """
    This is our 'shared notebook' that flows through all agents.

    Think of it like a form that gets filled out step by step:
    - User writes the question
    - Planner adds research plan
    - Researcher adds findings
    - etc.
    """

    # Input from user
    question: str

    # Output (what we'll return to user)
    answer: str


# That's it for now! We'll add more fields later.
