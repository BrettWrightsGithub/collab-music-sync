import unittest
import tempfile
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.schema import Base, TrackMatch, FailedMatch
from src.database.track_match_repository import TrackMatchRepository
from src.models.playlist import Track, Artist

class TestTrackMatchRepository(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_url = f"sqlite:///{self.temp_db.name}"
        self.engine = create_engine(self.db_url)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Create repository
        self.repo = TrackMatchRepository(self.session)
        
        # Create sample tracks for testing
        self.spotify_track = Track(
            title="Hey Ya!",
            artists=[Artist(name="OutKast", id="spotify_artist_id")],
            platform="spotify",
            platform_id="spotify_track_id",
            album_name="Speakerboxxx/The Love Below"
        )
        
        self.youtube_track = Track(
            title="Hey Ya",
            artists=[Artist(name="Outkast", id="youtube_artist_id")],
            platform="youtube",
            platform_id="youtube_track_id",
            album_name="Speakerboxxx / The Love Below"
        )

    def tearDown(self):
        # Close session and remove temporary database
        self.session.close()
        os.unlink(self.temp_db.name)

    def test_save_and_get_match(self):
        """Test saving and retrieving a track match."""
        # Save match
        match = self.repo.save_match(
            source_track=self.spotify_track,
            target_track=self.youtube_track,
            confidence_score=0.95
        )
        
        # Get match
        retrieved_track = self.repo.get_match(
            source_track=self.spotify_track,
            target_platform="youtube"
        )
        
        self.assertIsNotNone(retrieved_track)
        self.assertEqual(retrieved_track.platform_id, self.youtube_track.platform_id)
        self.assertEqual(retrieved_track.title, self.youtube_track.title)

    def test_get_match_with_confidence_threshold(self):
        """Test that matches below confidence threshold are not returned."""
        # Save low confidence match
        self.repo.save_match(
            source_track=self.spotify_track,
            target_track=self.youtube_track,
            confidence_score=0.6
        )
        
        # Try to get match with higher confidence requirement
        retrieved_track = self.repo.get_match(
            source_track=self.spotify_track,
            target_platform="youtube",
            min_confidence=0.7
        )
        
        self.assertIsNone(retrieved_track)

    def test_get_match_with_age_limit(self):
        """Test that old matches are not returned."""
        # Save match with old timestamp
        match = self.repo.save_match(
            source_track=self.spotify_track,
            target_track=self.youtube_track,
            confidence_score=0.95
        )
        
        # Manually update the last_verified timestamp to be old
        old_date = datetime.utcnow() - timedelta(days=31)
        match.last_verified = old_date
        self.session.commit()
        
        # Try to get match with 30-day age limit
        retrieved_track = self.repo.get_match(
            source_track=self.spotify_track,
            target_platform="youtube",
            max_age_days=30
        )
        
        self.assertIsNone(retrieved_track)

    def test_save_failed_match(self):
        """Test saving and retrieving failed match information."""
        failed = self.repo.save_failed_match(
            source_track=self.spotify_track,
            target_platform="youtube",
            error_reason="No matches found"
        )
        
        # Verify failed match was saved
        saved_failed = self.session.query(FailedMatch).first()
        self.assertIsNotNone(saved_failed)
        self.assertEqual(saved_failed.source_platform_id, self.spotify_track.platform_id)
        self.assertEqual(saved_failed.error_reason, "No matches found")

    def test_match_statistics(self):
        """Test getting match statistics."""
        # Save some matches
        self.repo.save_match(
            source_track=self.spotify_track,
            target_track=self.youtube_track,
            confidence_score=0.95,
            manually_verified=True
        )
        
        self.repo.save_match(
            source_track=self.youtube_track,
            target_track=self.spotify_track,
            confidence_score=0.90
        )
        
        self.repo.save_failed_match(
            source_track=self.spotify_track,
            target_platform="youtube",
            error_reason="Test failure"
        )
        
        stats = self.repo.get_match_statistics()
        self.assertEqual(stats["total_matches"], 2)
        self.assertEqual(stats["verified_matches"], 1)
        self.assertEqual(stats["failed_matches"], 1)
