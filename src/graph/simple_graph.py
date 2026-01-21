# src/graph/simple_graph.py

from langgraph.graph import StateGraph, END
from src.graph.state import ResearchState


def answer_node(state: ResearchState) -> ResearchState:
    """
    This is our simplest possible node.
    It just creates a dummy answer.

    Args:
        state: Current state with the user's question

    Returns:
        Updated state with an answer
    """

    # Get the question from state
    question = state["question"]

    # Create a simple answer (no AI yet, just practice!)
    answer = f"You asked: '{question}'. This is a placeholder answer!"

    # Update the state
    state["answer"] = answer

    # Return updated state
    return state


# Create the graph
def create_simple_graph():
    """
    Creates the simplest possible LangGraph.

    Flow: START → answer_node → END
    """

    # Step 1: Create a graph with our state type
    graph = StateGraph(ResearchState)

    # Step 2: Add our node
    graph.add_node("answer", answer_node)

    # Step 3: Set the starting point
    graph.set_entry_point("answer")

    # Step 4: Add edge from answer node to END
    graph.add_edge("answer", END)

    # Step 5: Compile the graph
    return graph.compile()


# Test function
if __name__ == "__main__":
    # Create the graph
    app = create_simple_graph()

    # Create initial state
    initial_state = {"question": "What is machine learning?", "answer": ""}

    # Run the graph
    result = app.invoke(initial_state)

    # Print result
    print("Question:", result["question"])
    print("Answer:", result["answer"])
