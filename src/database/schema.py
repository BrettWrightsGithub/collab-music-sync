"""Database schema for track matching and synchronization."""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class TrackMatch(Base):
    """Stores matches between tracks across different platforms."""
    __tablename__ = 'track_matches'

    id = Column(Integer, primary_key=True)
    # Source track details
    source_platform = Column(String, nullable=False)
    source_platform_id = Column(String, nullable=False)
    source_title = Column(String, nullable=False)
    source_artists = Column(String, nullable=False)  # JSON string of artist names
    source_album = Column(String)
    
    # Target track details
    target_platform = Column(String, nullable=False)
    target_platform_id = Column(String, nullable=False)
    target_title = Column(String, nullable=False)
    target_artists = Column(String, nullable=False)  # JSON string of artist names
    target_album = Column(String)
    
    # Match metadata
    confidence_score = Column(Float, nullable=False)
    manually_verified = Column(Boolean, default=False)
    last_verified = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TrackMatch {self.source_platform}:{self.source_platform_id} -> {self.target_platform}:{self.target_platform_id}>"

class FailedMatch(Base):
    """Stores information about failed track matches for analysis."""
    __tablename__ = 'failed_matches'

    id = Column(Integer, primary_key=True)
    source_platform = Column(String, nullable=False)
    source_platform_id = Column(String, nullable=False)
    source_title = Column(String, nullable=False)
    source_artists = Column(String, nullable=False)
    target_platform = Column(String, nullable=False)
    error_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FailedMatch {self.source_platform}:{self.source_platform_id}>"

def init_db(db_url: str = 'sqlite:///track_matches.db'):
    """Initialize the database and create tables."""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
