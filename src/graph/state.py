# src/graph/state.py

from typing import TypedDict, List


class ResearchState(TypedDict):
    """
    Enhanced state with quality control.
    """

    # Input
    question: str

    # Planning phase
    research_plan: str
    sub_questions: List[str]

    # Research phase
    search_results: str

    # Analysis phase
    answer: str

    # NEW: Quality control
    quality_score: float  # 0.0 to 1.0
    needs_improvement: bool  # True if we should refine
    critic_reasoning: str  # Critic's feedback on what needs improvement
    iteration_count: int  # How many times we've tried
