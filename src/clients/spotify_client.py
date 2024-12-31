"""Spotify API client implementation."""
import os
from typing import List, Optional, Dict, Any
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.models.playlist import Playlist, Track, Artist
from src.converters.spotify_converter import convert_spotify_to_model
from src.clients.base_client import BaseMusicClient

class SpotifyClient(BaseMusicClient):
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ):
        """Initialize Spotify client.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
        """
        self.client_id = client_id or os.getenv("SPOTIFY_API_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_API_CLIENT_SECRET")
        self.client = None
        
    def authenticate(self) -> None:
        """Authenticate with Spotify using client credentials."""
        if not all([self.client_id, self.client_secret]):
            raise ValueError(
                "Missing Spotify credentials. Please set SPOTIFY_API_CLIENT_ID and "
                "SPOTIFY_API_CLIENT_SECRET environment variables."
            )
            
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
    
    def get_playlist(self, playlist_id: str) -> Playlist:
        """Get a playlist by its ID."""
        if not self.client:
            self.authenticate()
            
        try:
            print(f"\nFetching Spotify playlist with ID: {playlist_id}")
            playlist_data = self.client.playlist(playlist_id)
            print(f"Raw playlist data: {playlist_data.keys()}")
            print(f"Number of tracks in raw data: {len(playlist_data.get('tracks', {}).get('items', []))}")
            
            playlist = convert_spotify_to_model(playlist_data)
            print(f"Converted playlist tracks: {len(playlist.tracks)}")
            return playlist
        except Exception as e:
            print(f"Error in get_playlist: {str(e)}")
            raise
    
    def create_playlist(
        self,
        name: str,
        description: Optional[str] = None,
        public: bool = True
    ) -> str:
        """Create a new playlist."""
        if not self.client:
            self.authenticate()
            
        user_id = self.client.me()["id"]
        playlist = self.client.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            description=description
        )
        return playlist["id"]
    
    def add_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Add tracks to a playlist."""
        if not self.client:
            self.authenticate()
            
        track_uris = [f"spotify:track:{t.platform_id}" for t in tracks if t.platform_id]
        if not track_uris:
            return False
            
        try:
            # Spotify has a limit of 100 tracks per request
            for i in range(0, len(track_uris), 100):
                batch = track_uris[i:i + 100]
                self.client.playlist_add_items(playlist_id, batch)
            return True
        except Exception as e:
            print(f"Error adding tracks to Spotify playlist: {e}")
            return False
    
    def remove_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Remove tracks from a playlist."""
        if not self.client:
            self.authenticate()
            
        track_uris = [f"spotify:track:{t.platform_id}" for t in tracks if t.platform_id]
        if not track_uris:
            return False
            
        try:
            # Spotify has a limit of 100 tracks per request
            for i in range(0, len(track_uris), 100):
                batch = track_uris[i:i + 100]
                self.client.playlist_remove_all_occurrences_of_items(
                    playlist_id,
                    batch
                )
            return True
        except Exception as e:
            print(f"Error removing tracks from Spotify playlist: {e}")
            return False
    
    def search_track(
        self,
        query: str,
        limit: int = 3
    ) -> List[Track]:
        """Search for tracks matching the query."""
        if not self.client:
            self.authenticate()
            
        results = self.client.search(
            q=query,
            type="track",
            limit=limit
        )
        
        tracks = []
        for item in results.get("tracks", {}).get("items", []):
            track = Track(
                title=item.get("name", "Unknown"),
                artists=[
                    Artist(
                        name=artist.get("name", "Unknown Artist"),
                        id=artist.get("id"),
                        url=artist.get("external_urls", {}).get("spotify")
                    )
                    for artist in item.get("artists", [])
                ],
                duration_ms=item.get("duration_ms"),
                album_name=item.get("album", {}).get("name"),
                album_id=item.get("album", {}).get("id"),
                platform_id=item.get("id"),
                url=item.get("external_urls", {}).get("spotify")
            )
            tracks.append(track)
            
        return tracks
    
    def update_playlist_details(
        self,
        playlist_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[bool] = None
    ) -> bool:
        """Update playlist metadata."""
        if not self.client:
            self.authenticate()
            
        try:
            self.client.playlist_change_details(
                playlist_id,
                name=name,
                description=description,
                public=public
            )
            return True
        except Exception as e:
            print(f"Error updating Spotify playlist details: {e}")
            return False
