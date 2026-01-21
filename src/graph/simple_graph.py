# src/graph/simple_graph.py

from langgraph.graph import StateGraph, END
from src.graph.state import ResearchState
from src.agents.simple_agent import SimpleAgent
from dotenv import load_dotenv

load_dotenv()


# Create agent once (reuse for all requests)
agent = SimpleAgent()


def answer_node(state: ResearchState) -> ResearchState:
    """
    Node that uses AI to answer the question.
    """

    # Get question from state
    question = state["question"]

    # Use AI agent to answer
    answer = agent.answer(question)

    # Update state
    state["answer"] = answer

    return state


def create_simple_graph():
    """
    Creates a LangGraph with AI-powered node.
    """

    graph = StateGraph(ResearchState)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("answer")
    graph.add_edge("answer", END)

    return graph.compile()


if __name__ == "__main__":
    app = create_simple_graph()

    initial_state = {"question": "What is machine learning?", "answer": ""}

    result = app.invoke(initial_state)

    print("Question:", result["question"])
    print("Answer:", result["answer"])
