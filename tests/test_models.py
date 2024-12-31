import unittest
from datetime import datetime
from src.models.playlist import Artist, Track, Playlist

class TestArtistModel(unittest.TestCase):
    def test_artist_creation(self):
        artist = Artist(name="Test Artist", id="123", url="http://example.com")
        self.assertEqual(artist.name, "Test Artist")
        self.assertEqual(artist.id, "123")
        self.assertEqual(artist.url, "http://example.com")

    def test_artist_optional_fields(self):
        artist = Artist(name="Test Artist")
        self.assertEqual(artist.name, "Test Artist")
        self.assertIsNone(artist.id)
        self.assertIsNone(artist.url)

class TestTrackModel(unittest.TestCase):
    def setUp(self):
        self.artist = Artist(name="Test Artist")
        
    def test_track_creation(self):
        track = Track(
            title="Test Track",
            artists=[self.artist],
            duration_ms=300000,
            album_name="Test Album"
        )
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(len(track.artists), 1)
        self.assertEqual(track.duration_ms, 300000)
        self.assertEqual(track.album_name, "Test Album")

    def test_track_defaults(self):
        track = Track(title="Test Track", artists=[self.artist])
        self.assertFalse(track.is_explicit)
        self.assertTrue(track.is_available)
        self.assertIsNone(track.url)

class TestPlaylistModel(unittest.TestCase):
    def setUp(self):
        self.artist = Artist(name="Test Artist")
        self.track = Track(title="Test Track", artists=[self.artist])
        
    def test_playlist_creation(self):
        playlist = Playlist(
            id="123",
            title="Test Playlist",
            tracks=[self.track],
            platform="spotify"
        )
        self.assertEqual(playlist.id, "123")
        self.assertEqual(playlist.title, "Test Playlist")
        self.assertEqual(len(playlist.tracks), 1)
        self.assertEqual(playlist.platform, "spotify")

    def test_playlist_post_init(self):
        playlist = Playlist(
            id="123",
            title="Test Playlist",
            tracks=[self.track, self.track],
            platform="youtube"
        )
        self.assertEqual(playlist.track_count, 2)

    def test_playlist_defaults(self):
        playlist = Playlist(
            id="123",
            title="Test Playlist",
            tracks=[],
            platform="spotify"
        )
        self.assertTrue(playlist.is_public)
        self.assertEqual(playlist.track_count, 0)
        self.assertIsNone(playlist.description)
        self.assertIsNone(playlist.thumbnail_url)
