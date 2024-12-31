"""Test configuration and fixtures."""
import pytest
import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.schema import Base

@pytest.fixture
def sample_spotify_response():
    """Load sample Spotify playlist response."""
    samples_dir = Path(__file__).parent.parent / 'samples'
    with open(samples_dir / 'spotify-get-playlist-response.json') as f:
        return json.load(f)

@pytest.fixture
def sample_youtube_response():
    """Load sample YouTube Music playlist response."""
    samples_dir = Path(__file__).parent.parent / 'samples'
    with open(samples_dir / 'youtube_music_playlist_sample.json') as f:
        return json.load(f)

@pytest.fixture
def db_session():
    """Create a new database session for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)
