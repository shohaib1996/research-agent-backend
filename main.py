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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Research Assistant",
    description="AI-powered research assistant using LangGraph",
    version="0.2.0",  # Updated version!
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
        "version": "0.2.0",
    }


@app.post("/api/research", response_model=QueryResponse)
def research_query(request: QueryRequest):
    """
    Research endpoint - now using LangGraph!
    """
    try:
        logger.info(f"Research request: {request.question}")

        # Create initial state
        initial_state = {"question": request.question, "answer": ""}

        # Run the graph!
        result = research_graph.invoke(initial_state)

        # Return response
        response = QueryResponse(
            success=True,
            answer=result["answer"],
            metadata={"max_sources": request.max_sources, "graph_version": "simple_v1"},
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
        "status": "step_2_complete",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
