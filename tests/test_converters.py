import unittest
from pathlib import Path
from src.converters.spotify_converter import convert_spotify_to_model
from src.converters.youtube_converter import convert_youtube_to_model
from src.models.playlist import Playlist, Track, Artist

class TestSpotifyConverter(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
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

    def test_convert_spotify_playlist(self):
        """Test converting a Spotify playlist to our model."""
        playlist = convert_spotify_to_model(self.sample_playlist)
        
        # Test playlist attributes
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.platform, "spotify")
        self.assertEqual(playlist.id, "playlist123")
        self.assertEqual(playlist.title, "Test Playlist")
        self.assertEqual(playlist.description, "Test Description")
        self.assertEqual(playlist.owner_id, "owner123")
        self.assertTrue(playlist.is_public)
        self.assertEqual(playlist.track_count, 1)

    def test_convert_spotify_tracks(self):
        """Test converting Spotify tracks to our model."""
        playlist = convert_spotify_to_model(self.sample_playlist)
        
        # Test track list
        self.assertEqual(len(playlist.tracks), 1)
        
        # Test track attributes
        track = playlist.tracks[0]
        self.assertIsInstance(track, Track)
        self.assertEqual(track.platform, "spotify")
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.platform_id, "track123")
        self.assertEqual(track.duration_ms, 300000)
        self.assertEqual(track.album_name, "Test Album")
        self.assertEqual(track.album_id, "album123")
        self.assertFalse(track.is_explicit)
        self.assertTrue(track.is_available)
        
        # Test artist attributes
        self.assertEqual(len(track.artists), 1)
        artist = track.artists[0]
        self.assertIsInstance(artist, Artist)
        self.assertEqual(artist.name, "Test Artist")
        self.assertEqual(artist.id, "artist123")

    def test_convert_empty_spotify_playlist(self):
        """Test converting a Spotify playlist with no tracks."""
        empty_playlist = self.sample_playlist.copy()
        empty_playlist["tracks"]["items"] = []
        
        playlist = convert_spotify_to_model(empty_playlist)
        self.assertEqual(len(playlist.tracks), 0)
        self.assertEqual(playlist.track_count, 0)

class TestYouTubeConverter(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.sample_track = {
            "videoId": "video123",
            "title": "Test Track",
            "artists": [{"id": "artist123", "name": "Test Artist"}],
            "album": {"name": "Test Album"},
            "duration_seconds": 300,
            "isExplicit": False
        }
        
        self.sample_playlist = {
            "id": "playlist123",
            "title": "Test Playlist",
            "description": "Test Description",
            "author": {"id": "author123"},
            "tracks": [self.sample_track]
        }

    def test_convert_youtube_playlist(self):
        """Test converting a YouTube Music playlist to our model."""
        playlist = convert_youtube_to_model(self.sample_playlist)
        
        # Test playlist attributes
        self.assertIsInstance(playlist, Playlist)
        self.assertEqual(playlist.platform, "youtube")
        self.assertEqual(playlist.id, "playlist123")
        self.assertEqual(playlist.title, "Test Playlist")
        self.assertEqual(playlist.description, "Test Description")
        self.assertEqual(playlist.owner_id, "author123")
        self.assertTrue(playlist.is_public)
        self.assertEqual(playlist.track_count, 1)

    def test_convert_youtube_tracks(self):
        """Test converting YouTube Music tracks to our model."""
        playlist = convert_youtube_to_model(self.sample_playlist)
        
        # Test track list
        self.assertEqual(len(playlist.tracks), 1)
        
        # Test track attributes
        track = playlist.tracks[0]
        self.assertIsInstance(track, Track)
        self.assertEqual(track.platform, "youtube")
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.platform_id, "video123")
        self.assertEqual(track.duration_ms, 300000)  # 300 seconds * 1000
        self.assertEqual(track.album_name, "Test Album")
        self.assertFalse(track.is_explicit)
        self.assertTrue(track.is_available)
        
        # Test artist attributes
        self.assertEqual(len(track.artists), 1)
        artist = track.artists[0]
        self.assertIsInstance(artist, Artist)
        self.assertEqual(artist.name, "Test Artist")
        self.assertEqual(artist.id, "artist123")

    def test_convert_empty_youtube_playlist(self):
        """Test converting a YouTube Music playlist with no tracks."""
        empty_playlist = self.sample_playlist.copy()
        empty_playlist["tracks"] = []
        
        playlist = convert_youtube_to_model(empty_playlist)
        self.assertEqual(len(playlist.tracks), 0)
        self.assertEqual(playlist.track_count, 0)

    def test_convert_youtube_track_with_string_artist(self):
        """Test converting a YouTube Music track with a string artist field."""
        track_data = self.sample_track.copy()
        track_data["artists"] = "Test Artist"
        
        playlist_data = self.sample_playlist.copy()
        playlist_data["tracks"] = [track_data]
        
        playlist = convert_youtube_to_model(playlist_data)
        track = playlist.tracks[0]
        
        self.assertEqual(len(track.artists), 1)
        self.assertEqual(track.artists[0].name, "Test Artist")
        self.assertIsNone(track.artists[0].id)
