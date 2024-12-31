import unittest
from unittest.mock import Mock, patch
from src.models.playlist import Track, Artist
from src.matchers.track_matcher import TrackMatcher
from src.database.track_match_repository import TrackMatchRepository

class TestTrackMatcher(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=TrackMatchRepository)
        self.matcher = TrackMatcher(repository=self.mock_repository)
        
        # Create sample tracks
        self.spotify_track = Track(
            title="Hey Ya!",
            artists=[Artist(name="OutKast")],
            album_name="Speakerboxxx/The Love Below",
            platform="spotify",
            platform_id="sp123"
        )
        
        self.youtube_track = Track(
            title="Hey Ya",  # Slightly different title
            artists=[Artist(name="Outkast")],  # Different capitalization
            album_name="Speakerboxxx / The Love Below",  # Spacing difference
            platform="youtube",
            platform_id="yt456"
        )

    def test_exact_match(self):
        """Test matching tracks that are exactly the same."""
        confidence = self.matcher.match_tracks(self.spotify_track, self.spotify_track)
        self.assertEqual(confidence, 1.0)

    def test_near_match_with_minor_differences(self):
        """Test matching tracks with minor differences in title/artist spelling."""
        confidence = self.matcher.match_tracks(self.spotify_track, self.youtube_track)
        self.assertGreater(confidence, 0.9)

    def test_match_with_featuring_artist(self):
        """Test matching tracks with featuring artists."""
        track1 = Track(
            title="Collaboration",
            artists=[Artist(name="Main Artist"), Artist(name="Featured Artist")],
            platform="spotify",
            platform_id="sp789"
        )
        
        track2 = Track(
            title="Collaboration (feat. Featured Artist)",
            artists=[Artist(name="Main Artist")],
            platform="youtube",
            platform_id="yt789"
        )
        
        confidence = self.matcher.match_tracks(track1, track2)
        self.assertGreater(confidence, 0.8)

    def test_match_with_special_characters(self):
        """Test matching tracks with special characters."""
        track1 = Track(
            title="Let's Dance",
            artists=[Artist(name="Artist & Friends")],
            platform="spotify",
            platform_id="sp101"
        )
        
        track2 = Track(
            title="Lets Dance",
            artists=[Artist(name="Artist and Friends")],
            platform="youtube",
            platform_id="yt101"
        )
        
        confidence = self.matcher.match_tracks(track1, track2)
        self.assertGreater(confidence, 0.9)

    def test_match_with_remixes(self):
        """Test matching different versions of the same song."""
        track1 = Track(
            title="Song Name",
            artists=[Artist(name="Artist")],
            platform="spotify",
            platform_id="sp202"
        )
        
        track2 = Track(
            title="Song Name (Radio Mix)",
            artists=[Artist(name="Artist")],
            platform="youtube",
            platform_id="yt202"
        )
        
        confidence = self.matcher.match_tracks(track1, track2)
        self.assertGreater(confidence, 0.7)

    def test_no_match_different_songs(self):
        """Test matching completely different songs."""
        different_track = Track(
            title="Different Song",
            artists=[Artist(name="Different Artist")],
            platform="spotify",
            platform_id="sp303"
        )
        
        confidence = self.matcher.match_tracks(self.spotify_track, different_track)
        self.assertLess(confidence, 0.3)

    def test_find_best_match_with_cache_hit(self):
        """Test finding best match when there's a cache hit."""
        # Setup mock repository to return a cached match
        self.mock_repository.get_match.return_value = self.youtube_track
        
        candidates = [self.youtube_track, self.spotify_track]
        matched_track, confidence = self.matcher.find_best_match(self.spotify_track, candidates)
        
        self.assertEqual(matched_track.platform_id, self.youtube_track.platform_id)
        self.assertEqual(confidence, 1.0)
        self.mock_repository.get_match.assert_called_once()

    def test_find_best_match_with_cache_miss(self):
        """Test finding best match when there's no cache hit."""
        # Setup mock repository to return no cached match
        self.mock_repository.get_match.return_value = None
        
        candidates = [self.youtube_track]
        matched_track, confidence = self.matcher.find_best_match(self.spotify_track, candidates)
        
        self.assertEqual(matched_track.platform_id, self.youtube_track.platform_id)
        self.assertGreater(confidence, 0.9)
        self.mock_repository.save_match.assert_called_once()

    def test_find_best_match_with_no_candidates(self):
        """Test finding best match when there are no candidates."""
        matched_track, confidence = self.matcher.find_best_match(self.spotify_track, [])
        
        self.assertIsNone(matched_track)
        self.assertEqual(confidence, 0.0)
        self.mock_repository.save_failed_match.assert_called_once()

    def test_find_best_match_with_low_confidence(self):
        """Test finding best match when confidence is too low."""
        different_track = Track(
            title="Completely Different",
            artists=[Artist(name="Different Artist")],
            platform="youtube",
            platform_id="yt404"
        )
        
        matched_track, confidence = self.matcher.find_best_match(self.spotify_track, [different_track])
        
        self.assertEqual(matched_track.platform_id, different_track.platform_id)
        self.assertLess(confidence, 0.5)
        self.mock_repository.save_failed_match.assert_called_once()
