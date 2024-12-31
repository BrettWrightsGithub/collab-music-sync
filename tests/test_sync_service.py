import unittest
from unittest.mock import Mock, patch
from src.models.playlist import Playlist, Track, Artist
from src.services.sync_service import PlaylistSyncService  # To be implemented

class TestPlaylistSyncService(unittest.TestCase):
    def setUp(self):
        self.spotify_client = Mock()
        self.youtube_client = Mock()
        self.sync_service = PlaylistSyncService(
            spotify_client=self.spotify_client,
            youtube_client=self.youtube_client
        )
        
        # Create sample playlists
        self.artist = Artist(name="Test Artist")
        self.track = Track(
            title="Test Track",
            artists=[self.artist],
            platform_id="123"
        )
        self.source_playlist = Playlist(
            id="source123",
            title="Test Playlist",
            tracks=[self.track],
            platform="spotify"
        )

    def test_create_playlist(self):
        """Test creating a new playlist on the target platform."""
        # Mock the target platform's create_playlist response
        self.youtube_client.create_playlist.return_value = "target456"
        
        target_playlist_id = self.sync_service.create_playlist(
            source_playlist=self.source_playlist,
            target_platform="youtube"
        )
        
        self.assertIsNotNone(target_playlist_id)
        self.youtube_client.create_playlist.assert_called_once()

    def test_sync_tracks(self):
        """Test syncing tracks from source to target playlist."""
        # Mock successful track matching and addition
        self.sync_service.sync_tracks(
            source_playlist=self.source_playlist,
            target_playlist_id="target456",
            target_platform="youtube"
        )
        
        self.youtube_client.add_tracks.assert_called_once()

    def test_sync_metadata(self):
        """Test syncing playlist metadata (title, description, etc.)."""
        self.sync_service.sync_metadata(
            source_playlist=self.source_playlist,
            target_playlist_id="target456",
            target_platform="youtube"
        )
        
        self.youtube_client.update_playlist_details.assert_called_once()

    def test_handle_unavailable_tracks(self):
        """Test handling tracks that aren't available on target platform."""
        unavailable_track = Track(
            title="Unavailable Track",
            artists=[self.artist],
            platform_id="999",
            is_available=False
        )
        playlist = Playlist(
            id="source123",
            title="Test Playlist",
            tracks=[unavailable_track],
            platform="spotify"
        )
        
        # Should not throw an error, should log the unavailable track
        self.sync_service.sync_tracks(
            source_playlist=playlist,
            target_playlist_id="target456",
            target_platform="youtube"
        )

    def test_bidirectional_sync(self):
        """Test syncing changes from either platform."""
        source_changes = {
            "added": [self.track],
            "removed": [],
            "reordered": False
        }
        
        self.sync_service.sync_changes(
            source_playlist_id="source123",
            target_playlist_id="target456",
            changes=source_changes,
            source_platform="spotify",
            target_platform="youtube"
        )
        
        self.youtube_client.add_tracks.assert_called_once()
