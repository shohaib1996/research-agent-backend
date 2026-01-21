# src/database/models.py

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class ResearchSession(Base):
    """
    Stores research sessions.
    """

    __tablename__ = "research_sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    quality_score = Column(Float, default=0.0)
    iterations = Column(Integer, default=0)
    research_plan = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "question": self.question,
            "answer": self.answer,
            "quality_score": self.quality_score,
            "iterations": self.iterations,
            "research_plan": self.research_plan,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
        }


class SearchCache(Base):
    """
    Caches search results to avoid redundant API calls.
    """

    __tablename__ = "search_cache"

    id = Column(Integer, primary_key=True)
    query = Column(String(500), unique=True, index=True)
    results = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "query": self.query,
            "results": self.results,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./research_assistant.db"

engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),  # For sync operations
    echo=False,  # Set True to see SQL queries
)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Initialize database - create all tables.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")


def get_db():
    """
    Get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
