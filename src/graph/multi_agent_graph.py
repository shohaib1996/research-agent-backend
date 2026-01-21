# src/graph/multi_agent_graph.py

from langgraph.graph import StateGraph, END
from src.graph.state import ResearchState
from src.agents.planner_agent import PlannerAgent
from src.agents.researcher_agent import ResearcherAgent
from src.agents.analyst_agent import AnalystAgent
from src.agents.critic_agent import CriticAgent
from src.agents.refiner_agent import RefinerAgent
from src.database.db_helper import DatabaseHelper

# Create database helper
db_helper = DatabaseHelper()

# Create agents (researcher gets db_helper for caching)
planner = PlannerAgent()
researcher = ResearcherAgent(db_helper=db_helper)  # WITH CACHING
analyst = AnalystAgent()
critic = CriticAgent()
refiner = RefinerAgent()


def plan_node(state: ResearchState) -> ResearchState:
    """Node 1: Planning"""
    print("🎯 Planning research...")

    result = planner.plan(state["question"])

    state["research_plan"] = result["plan"]
    state["sub_questions"] = result["sub_questions"]

    print(f"   Created {len(result['sub_questions'])} sub-questions")

    return state


def research_node(state: ResearchState) -> ResearchState:
    """Node 2: Research"""
    print("🔍 Researching...")

    findings = researcher.research(state["sub_questions"])
    state["search_results"] = findings

    print("   Research complete")

    return state


def is_simple_question(question: str) -> bool:
    """Check if question is simple (skip critique for these)."""
    simple_indicators = ["what is", "who is", "define", "explain", "what are"]
    question_lower = question.lower()
    return any(indicator in question_lower for indicator in simple_indicators)


def analyze_node(state: ResearchState) -> ResearchState:
    """Node 3: Analysis"""
    print("📊 Analyzing findings...")

    answer = analyst.analyze(
        question=state["question"],
        plan=state["research_plan"],
        findings=state["search_results"],
    )

    state["answer"] = answer

    print("   Analysis complete")

    return state


def critique_node(state: ResearchState) -> ResearchState:
    """Node 4: Quality Evaluation (skipped for simple questions)"""

    # Skip critique for simple questions - auto-pass
    if is_simple_question(state["question"]):
        print("⏭️  Skipping critique (simple question)")
        state["quality_score"] = 0.85
        state["needs_improvement"] = False
        return state

    print("🔍 Evaluating quality...")

    evaluation = critic.evaluate(question=state["question"], answer=state["answer"])

    state["quality_score"] = evaluation["score"]
    state["needs_improvement"] = evaluation["needs_improvement"]

    print(f"   Quality Score: {evaluation['score']:.2f}")
    print(f"   Needs Improvement: {evaluation['needs_improvement']}")

    return state


def refine_node(state: ResearchState) -> ResearchState:
    """Node 5: Refinement (if needed)"""
    print("🔄 Refining research approach...")

    # Increment iteration count
    state["iteration_count"] += 1

    # Get refined questions
    new_questions = refiner.refine(
        question=state["question"],
        answer=state["answer"],
        reasoning="Quality below threshold",
    )

    # Replace sub-questions with refined ones
    state["sub_questions"] = new_questions

    print(f"   Created {len(new_questions)} refined questions")
    print(f"   Iteration: {state['iteration_count']}")

    return state


def should_continue(state: ResearchState) -> str:
    """
    Routing function: Decide if we should refine or finish.

    Returns:
        "refine" - if quality is low and iterations < 2
        "end" - if quality is good OR max iterations reached
    """

    # Check if we've tried too many times
    if state.get("iteration_count", 0) >= 2:
        print("   Max iterations reached, finishing...")
        return "end"

    # Check quality
    if state.get("needs_improvement", False):
        print("   Quality needs improvement, refining...")
        return "refine"

    print("   Quality acceptable, finishing...")
    return "end"


def create_research_graph():
    """
    Creates graph with database integration.
    """

    graph = StateGraph(ResearchState)

    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("critique", critique_node)
    graph.add_node("refine", refine_node)

    graph.set_entry_point("plan")

    graph.add_edge("plan", "research")
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", "critique")

    graph.add_conditional_edges(
        "critique", should_continue, {"refine": "refine", "end": END}
    )

    graph.add_edge("refine", "research")

    return graph.compile()


def run_research_with_db(question: str) -> dict:
    """
    Run research and save to database.
    """
    app = create_research_graph()

    initial_state = {
        "question": question,
        "research_plan": "",
        "sub_questions": [],
        "search_results": "",
        "answer": "",
        "quality_score": 0.0,
        "needs_improvement": False,
        "iteration_count": 0,
    }

    # Run research
    result = app.invoke(initial_state)

    # Save to database
    session_id = db_helper.save_session(result)
    result["session_id"] = session_id

    return result


if __name__ == "__main__":
    app = create_research_graph()

    initial_state = {
        "question": "What is artificial intelligence?",
        "research_plan": "",
        "sub_questions": [],
        "search_results": "",
        "answer": "",
        "quality_score": 0.0,
        "needs_improvement": False,
        "iteration_count": 0,
    }

    print("Starting research with caching...\n")
    result = app.invoke(initial_state)

    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    print(f"Quality Score: {result['quality_score']:.2f}")
    print(f"Iterations: {result['iteration_count']}")
    print(f"\nAnswer:\n{result['answer']}")
