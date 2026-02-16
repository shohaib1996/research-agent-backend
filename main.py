# main.py
# ruff: noqa: E402
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import logging
from src.graph.multi_agent_graph import create_research_graph, run_research_with_db
from src.database.db_helper import DatabaseHelper


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Research Assistant",
    description="Multi-agent AI research with persistence",
    version="0.6.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database helper
db_helper = DatabaseHelper()

# Graph
research_graph = create_research_graph()


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    use_cache: bool = Field(True, description="Use cached search results")


class QueryResponse(BaseModel):
    success: bool
    answer: str
    quality_score: float
    iterations: int
    session_id: str
    research_plan: str = ""


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Research Assistant with Persistence",
        "version": "0.6.0",
        "features": ["Multi-agent", "Quality control", "Caching", "Sessions"],
    }


@app.post("/api/research", response_model=QueryResponse)
def research_query(request: QueryRequest):
    """
    Research with database persistence.
    """
    try:
        logger.info(f"Research request: {request.question}")

        # Run research with database
        result = run_research_with_db(request.question)

        response = QueryResponse(
            success=True,
            answer=result["answer"],
            quality_score=result["quality_score"],
            iterations=result["iteration_count"],
            session_id=result.get("session_id", ""),
            research_plan=result["research_plan"],
        )

        logger.info(f"Session saved: {result.get('session_id')}")
        return response

    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/recent")
def get_recent_sessions(limit: int = 10):
    """
    Get recent research sessions.
    """
    try:
        sessions = db_helper.get_recent_sessions(limit=limit)
        return {"success": True, "count": len(sessions), "sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    """
    Get specific session by ID.
    """
    try:
        session = db_helper.get_session(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"success": True, "session": session}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
