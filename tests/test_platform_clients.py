import unittest
from unittest.mock import patch, Mock, MagicMock
from src.clients.spotify_client import SpotifyClient
from src.clients.youtube_client import YouTubeMusicClient
from src.models.playlist import Track, Artist, Playlist

class TestSpotifyClient(unittest.TestCase):
    def setUp(self):
        """Set up test client with mock credentials."""
        self.client = SpotifyClient(
            client_id="test_id",
            client_secret="test_secret"
        )
        
        # Sample track data
        self.sample_track = {
            "track": {
                "id": "track123",
                "name": "Test Track",
                "artists": [{"id": "artist123", "name": "Test Artist"}],
                "album": {"id": "album123", "name": "Test Album"},
                "duration_ms": 300000,
                "explicit": False
            }
        }
        
        # Sample playlist data
        self.sample_playlist = {
            "id": "playlist123",
            "name": "Test Playlist",
            "description": "Test Description",
            "owner": {"id": "owner123"},
            "public": True,
            "tracks": {
                "items": [self.sample_track]
            }
        }

    @patch('spotipy.Spotify')
    def test_authenticate(self, mock_spotify):
        """Test Spotify client authentication."""
        self.client.authenticate()
        self.assertIsNotNone(self.client.client)

    @patch('spotipy.Spotify')
    def test_get_playlist(self, mock_spotify):
        """Test fetching a playlist from Spotify."""
        # Setup mock
        mock_instance = mock_spotify.return_value
        mock_instance.playlist.return_value = self.sample_playlist
        
        # Initialize client
        self.client.client = mock_instance
        
        # Get playlist
        playlist = self.client.get_playlist("playlist123")
        
        # Verify response
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.id, "playlist123")
        self.assertEqual(playlist.platform, "spotify")
        self.assertEqual(len(playlist.tracks), 1)
        
        # Verify track data
        track = playlist.tracks[0]
        self.assertEqual(track.platform_id, "track123")
        self.assertEqual(track.platform, "spotify")
        self.assertEqual(track.title, "Test Track")

    @patch('spotipy.Spotify')
    def test_search_track(self, mock_spotify):
        """Test searching for tracks on Spotify."""
        # Setup mock response
        mock_instance = mock_spotify.return_value
        mock_instance.search.return_value = {
            "tracks": {
                "items": [{
                    "id": "track123",
                    "name": "Test Track",
                    "artists": [{"id": "artist123", "name": "Test Artist"}],
                    "album": {"id": "album123", "name": "Test Album"},
                    "duration_ms": 300000,
                    "explicit": False
                }]
            }
        }
        
        # Initialize client
        self.client.client = mock_instance
        
        # Search for tracks
        tracks = self.client.search_track("test query")
        
        # Verify response
        self.assertEqual(len(tracks), 1)
        track = tracks[0]
        self.assertIsInstance(track, Track)
        self.assertEqual(track.platform, "spotify")
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.platform_id, "track123")

class TestYouTubeMusicClient(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.client = YouTubeMusicClient(headers_path="test_headers.json")
        
        # Sample track data
        self.sample_track = {
            "videoId": "video123",
            "title": "Test Track",
            "artists": [{"id": "artist123", "name": "Test Artist"}],
            "album": {"name": "Test Album"},
            "duration_seconds": 300,
            "isExplicit": False
        }
        
        # Sample playlist data
        self.sample_playlist = {
            "id": "playlist123",
            "title": "Test Playlist",
            "description": "Test Description",
            "author": {"id": "author123"},
            "tracks": [self.sample_track]
        }

    @patch('ytmusicapi.YTMusic')
    def test_authenticate(self, mock_ytmusic):
        """Test YouTube Music client authentication."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            self.client.authenticate()
            self.assertIsNotNone(self.client.client)

    @patch('ytmusicapi.YTMusic')
    def test_get_playlist(self, mock_ytmusic):
        """Test fetching a playlist from YouTube Music."""
        # Setup mock
        mock_instance = mock_ytmusic.return_value
        mock_instance.get_playlist.return_value = self.sample_playlist
        
        # Initialize client
        self.client.client = mock_instance
        
        # Get playlist
        playlist = self.client.get_playlist("playlist123")
        
        # Verify response
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.id, "playlist123")
        self.assertEqual(playlist.platform, "youtube")
        self.assertEqual(len(playlist.tracks), 1)
        
        # Verify track data
        track = playlist.tracks[0]
        self.assertEqual(track.platform_id, "video123")
        self.assertEqual(track.platform, "youtube")
        self.assertEqual(track.title, "Test Track")

    @patch('ytmusicapi.YTMusic')
    def test_search_track(self, mock_ytmusic):
        """Test searching for tracks on YouTube Music."""
        # Setup mock response
        mock_instance = mock_ytmusic.return_value
        mock_instance.search.return_value = [{
            "resultType": "song",
            "videoId": "video123",
            "title": "Test Track",
            "artists": [{"id": "artist123", "name": "Test Artist"}],
            "album": {"name": "Test Album"},
            "duration_seconds": 300
        }]
        
        # Initialize client
        self.client.client = mock_instance
        
        # Search for tracks
        tracks = self.client.search_track("test query")
        
        # Verify response
        self.assertEqual(len(tracks), 1)
        track = tracks[0]
        self.assertIsInstance(track, Track)
        self.assertEqual(track.platform, "youtube")
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.platform_id, "video123")
