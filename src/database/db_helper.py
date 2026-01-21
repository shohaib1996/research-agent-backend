# src/database/db_helper.py

from src.database.models import ResearchSession, SearchCache, SessionLocal, init_db
from datetime import datetime
import uuid


class DatabaseHelper:
    """
    Helper class for database operations.
    """

    def __init__(self):
        # Initialize database on first use
        init_db()

    def save_session(self, state: dict) -> str:
        """
        Save research session to database.

        Returns:
            session_id
        """
        db = SessionLocal()

        try:
            # Generate session ID if not exists
            session_id = state.get("session_id") or str(uuid.uuid4())

            # Check if session exists
            session = db.query(ResearchSession).filter_by(session_id=session_id).first()

            if session:
                # Update existing
                session.answer = state.get("answer", "")
                session.quality_score = state.get("quality_score", 0.0)
                session.iterations = state.get("iteration_count", 0)
                session.completed_at = datetime.utcnow()
            else:
                # Create new
                session = ResearchSession(
                    session_id=session_id,
                    question=state.get("question", ""),
                    answer=state.get("answer", ""),
                    quality_score=state.get("quality_score", 0.0),
                    iterations=state.get("iteration_count", 0),
                    research_plan=state.get("research_plan", ""),
                    completed_at=datetime.utcnow(),
                )
                db.add(session)

            db.commit()
            return session_id

        except Exception as e:
            db.rollback()
            print(f"Error saving session: {e}")
            return None
        finally:
            db.close()

    def get_session(self, session_id: str) -> dict:
        """
        Retrieve session by ID.
        """
        db = SessionLocal()

        try:
            session = db.query(ResearchSession).filter_by(session_id=session_id).first()
            return session.to_dict() if session else None
        finally:
            db.close()

    def get_recent_sessions(self, limit: int = 10) -> list:
        """
        Get recent research sessions.
        """
        db = SessionLocal()

        try:
            sessions = (
                db.query(ResearchSession)
                .order_by(ResearchSession.created_at.desc())
                .limit(limit)
                .all()
            )

            return [s.to_dict() for s in sessions]
        finally:
            db.close()

    def cache_search_result(self, query: str, results: str):
        """
        Cache search results.
        """
        db = SessionLocal()

        try:
            # Check if already cached
            cached = db.query(SearchCache).filter_by(query=query).first()

            if cached:
                # Update existing
                cached.results = results
                cached.created_at = datetime.utcnow()
            else:
                # Create new
                cache_entry = SearchCache(query=query, results=results)
                db.add(cache_entry)

            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error caching search: {e}")
        finally:
            db.close()

    def get_cached_search(self, query: str) -> str:
        """
        Get cached search result.

        Returns:
            Cached results or None
        """
        db = SessionLocal()

        try:
            cached = db.query(SearchCache).filter_by(query=query).first()
            return cached.results if cached else None
        finally:
            db.close()
