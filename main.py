# main.py (UPDATE these parts)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import logging
from src.graph.multi_agent_graph import create_research_graph

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Research Assistant",
    description="Multi-agent AI research with quality control",
    version="0.5.0",
)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)


class QueryResponse(BaseModel):
    success: bool
    answer: str
    quality_score: float
    iterations: int
    research_plan: str = ""


# Create graph
research_graph = create_research_graph()


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Multi-Agent Research Assistant with Quality Control",
        "version": "0.5.0",
        "agents": ["Planner", "Researcher", "Analyst", "Critic", "Refiner"],
    }


@app.post("/api/research", response_model=QueryResponse)
def research_query(request: QueryRequest):
    """
    Multi-agent research with self-improvement.
    """
    try:
        logger.info(f"Research request: {request.question}")

        initial_state = {
            "question": request.question,
            "research_plan": "",
            "sub_questions": [],
            "search_results": "",
            "answer": "",
            "quality_score": 0.0,
            "needs_improvement": False,
            "critic_reasoning": "",
            "iteration_count": 0,
        }

        result = research_graph.invoke(initial_state)

        response = QueryResponse(
            success=True,
            answer=result["answer"],
            quality_score=result["quality_score"],
            iterations=result["iteration_count"],
            research_plan=result["research_plan"],
        )

        logger.info(
            f"Research completed - Quality: {result['quality_score']:.2f}, Iterations: {result['iteration_count']}"
        )
        return response

    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
