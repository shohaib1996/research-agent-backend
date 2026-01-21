# 🎯 Step 2: Understanding LangGraph Basics (Theory First!)

## What We're Doing in This Step
Learning what LangGraph is and creating the SIMPLEST possible graph with just ONE node.

**Time Estimate:** 15-20 minutes

---

## Part A: What is LangGraph? 🤔

### Simple Explanation

Think of LangGraph as a **flowchart for AI agents**.

**Normal chatbot:**
```
User asks question → LLM answers → Done
```

**LangGraph (our research assistant):**
```
User asks question 
  → Planner Agent (breaks it down)
  → Researcher Agent (finds info)
  → Analyst Agent (combines info)
  → Critic Agent (checks quality)
  → Done (or loop back if quality is low)
```

### Key Concepts

**1. State** 
- Like a shared notebook that all agents can read and write to
- Holds: user question, research results, confidence scores, etc.

**2. Nodes**
- Each agent is a "node" (like a step in the flowchart)
- Example: "Planner node", "Research node"

**3. Edges**
- Connections between nodes (arrows in flowchart)
- Can be conditional: "If quality > 0.8, go to END, else go to Refine"

**4. Graph**
- The complete flowchart with all nodes and edges

---

## Part B: Install LangGraph 📦

### 1. Update `requirements.txt`

Add these NEW lines to your existing `requirements.txt`:

```txt
# requirements.txt (add these to what you already have)

# === LangGraph & LangChain ===
langgraph==0.2.28
langchain==0.1.20
langchain-core==0.1.52
langchain-openai==0.0.8

# === OpenAI ===
openai==1.12.0
```

**What each package does:**

- **`langgraph`** - The state machine framework (main star!)
- **`langchain`** - Helper tools for LLMs
- **`langchain-core`** - Core LangChain functionality
- **`langchain-openai`** - OpenAI integration for LangChain
- **`openai`** - Official OpenAI Python SDK

### 2. Install

```bash
pip install -r requirements.txt
```

This will take 30-60 seconds.

### 3. Verify Installation

```bash
python -c "import langgraph; print('LangGraph version:', langgraph.__version__)"
```

Should output: `LangGraph version: 0.2.28` (or similar)

---

## Part C: Get OpenAI API Key 🔑

### Why Do We Need This?

LangGraph uses LLMs (like GPT-4) to power the agents. We need an API key to access OpenAI's models.

### Steps:

1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### Add to `.env` File

Open your `.env` file and add:

```env
# .env

OPENAI_API_KEY=sk-your-actual-key-here

# Other settings
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

**⚠️ IMPORTANT:** 
- Never commit this file to Git!
- Never share your API key!
- Keep it secret!

---

## Part D: Create Your First State 📝

### What is State?

State is a dictionary that flows through your graph. All agents read from and write to it.

### 1. Create `src/graph/state.py`

```python
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
```

**What's happening:**
- `TypedDict` = A dictionary with specific keys and types
- `question: str` = Must have a "question" key with string value
- `answer: str` = Must have an "answer" key with string value

Simple, right? 😊

---

## Part E: Create Your First Node 🎯

### What is a Node?

A node is a Python function that:
1. Takes in the State
2. Does something
3. Returns updated State

### 1. Create `src/graph/simple_graph.py`

```python
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
    initial_state = {
        "question": "What is machine learning?",
        "answer": ""
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Print result
    print("Question:", result["question"])
    print("Answer:", result["answer"])
```

---

## Part F: Test It! 🧪

### Run Your Simple Graph

```bash
python -m src.graph.simple_graph
```

**Expected Output:**
```
Question: What is machine learning?
Answer: You asked: 'What is machine learning?'. This is a placeholder answer!
```

**🎉 Congratulations!** You just created your first LangGraph!

---

## Part G: Understanding What Just Happened 🤓

Let's break down the code:

### 1. The Node Function
```python
def answer_node(state: ResearchState) -> ResearchState:
    question = state["question"]
    answer = f"You asked: '{question}'. This is a placeholder answer!"
    state["answer"] = answer
    return state
```

- Takes state as input
- Reads `question` from state
- Creates an `answer`
- Updates state with the answer
- Returns updated state

### 2. Building the Graph
```python
graph = StateGraph(ResearchState)  # 1. Create graph
graph.add_node("answer", answer_node)  # 2. Add node
graph.set_entry_point("answer")  # 3. Set start
graph.add_edge("answer", END)  # 4. Connect to END
return graph.compile()  # 5. Compile
```

**Visualize it:**
```
START → [answer_node] → END
```

### 3. Running the Graph
```python
app = create_simple_graph()
initial_state = {"question": "...", "answer": ""}
result = app.invoke(initial_state)
```

- Create the graph
- Provide initial state
- Run it with `.invoke()`
- Get back the final state

---

## Part H: Integrate with FastAPI 🔗

### Update `main.py`

Replace the placeholder research endpoint:

```python
# main.py (UPDATE the research_query function only)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import logging

# NEW IMPORT
from src.graph.simple_graph import create_simple_graph

load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Research Assistant",
    description="AI-powered research assistant using LangGraph",
    version="0.2.0"  # Updated version!
)

# Models (same as before)
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    max_sources: int = Field(5, ge=1, le=20)


class QueryResponse(BaseModel):
    success: bool
    answer: str
    metadata: dict = {}


# Create graph once (reuse for all requests)
research_graph = create_simple_graph()


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Agentic Research Assistant API",
        "version": "0.2.0"
    }


@app.post("/api/research", response_model=QueryResponse)
def research_query(request: QueryRequest):
    """
    Research endpoint - now using LangGraph!
    """
    try:
        logger.info(f"Research request: {request.question}")
        
        # Create initial state
        initial_state = {
            "question": request.question,
            "answer": ""
        }
        
        # Run the graph!
        result = research_graph.invoke(initial_state)
        
        # Return response
        response = QueryResponse(
            success=True,
            answer=result["answer"],
            metadata={
                "max_sources": request.max_sources,
                "graph_version": "simple_v1"
            }
        )
        
        logger.info("Research completed")
        return response
        
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/info")
def get_info():
    return {
        "features": ["LangGraph integration", "Single node graph"],
        "status": "step_2_complete"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Part I: Test the Full System 🎉

### 1. Start the Server

```bash
python main.py
```

### 2. Test via Browser

Go to: http://localhost:8000/docs

- Click on `POST /api/research`
- Click "Try it out"
- Enter:
```json
{
  "question": "What is artificial intelligence?",
  "max_sources": 5
}
```
- Click "Execute"

### 3. Test via Curl

```bash
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?", "max_sources": 5}'
```

**Expected Response:**
```json
{
  "success": true,
  "answer": "You asked: 'What is Python?'. This is a placeholder answer!",
  "metadata": {
    "max_sources": 5,
    "graph_version": "simple_v1"
  }
}
```

---

## ✅ Step 2 Complete!

### What You Accomplished:

✅ Installed LangGraph and LangChain  
✅ Got OpenAI API key  
✅ Created your first State schema  
✅ Created your first Node function  
✅ Built a simple LangGraph (1 node)  
✅ Integrated it with FastAPI  
✅ Tested the full system  

### Your Project Structure Now:

```
agentic-research-assistant/
├── venv/
├── src/
│   ├── __init__.py
│   └── graph/
│       ├── __init__.py
│       ├── state.py          ← NEW!
│       └── simple_graph.py   ← NEW!
├── main.py                   ← UPDATED!
├── requirements.txt          ← UPDATED!
├── .env                      ← UPDATED!
└── .gitignore
```

---

## 🎯 What's Next in Step 3?

In Step 3, we'll:
1. Add a REAL LLM to the node (using OpenAI)
2. Make the answer intelligent (not just placeholder)
3. Still keep it simple - just 1 node, but with AI! 🤖

---

## 💡 Key Takeaways

**LangGraph Basics:**
- **State** = Shared data dictionary
- **Node** = Function that processes state
- **Graph** = Connected nodes forming a workflow
- **Flow** = START → Node → Node → END

**Simple Graph Structure:**
```python
graph = StateGraph(StateType)
graph.add_node("name", function)
graph.set_entry_point("name")
graph.add_edge("name", END)
app = graph.compile()
result = app.invoke(initial_state)
```

---

## 🧪 Quick Test Checklist

- [ ] LangGraph installed successfully
- [ ] OpenAI API key added to `.env`
- [ ] `src/graph/state.py` created
- [ ] `src/graph/simple_graph.py` created
- [ ] Test script runs: `python -m src.graph.simple_graph`
- [ ] FastAPI updated and runs
- [ ] API endpoint works at `/api/research`

---

**Great job!** This was much smaller and focused. Take a break, then let me know when you're ready for Step 3! ☕

Any questions about Step 2? 🤔
