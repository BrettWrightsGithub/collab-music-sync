"""YouTube Music API client implementation."""
import os
import time
import random
from typing import List, Optional, Dict, Any
from ytmusicapi import YTMusic
from src.models.playlist import Playlist, Track, Artist
from src.converters.youtube_converter import convert_youtube_to_model
from src.clients.base_client import BaseMusicClient

class RateLimitError(Exception):
    """Raised when we detect rate limiting from the API"""
    pass

class YouTubeMusicClient(BaseMusicClient):
    def __init__(self, headers_path: Optional[str] = None):
        """Initialize YouTube Music client.
        
        Args:
            headers_path: Path to headers_auth.json file. If None, uses default location
        """
        self.headers_path = headers_path or "headers_auth.json"
        self.client = None
        self.last_request_time = 0
        self.min_request_interval = 2  # minimum seconds between requests
        
    def authenticate(self) -> None:
        """Authenticate with YouTube Music using headers file."""
        if not os.path.exists(self.headers_path):
            raise FileNotFoundError(
                f"Headers file not found at {self.headers_path}. "
                "Please run setup_auth.py first."
            )
        self.client = YTMusic(self.headers_path)
    
    def _wait_for_rate_limit(self) -> None:
        """Ensure minimum time between requests."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _exponential_backoff(self, attempt: int, max_delay: int = 32) -> float:
        """Calculate delay with exponential backoff and jitter."""
        delay = min(max_delay, 2 ** attempt)
        jitter = random.uniform(0, 0.1 * delay)
        return delay + jitter
    
    def _make_request(self, request_func, *args, max_retries: int = 3, **kwargs) -> Any:
        """Make an API request with retry logic and rate limiting."""
        if not self.client:
            self.authenticate()
            
        for attempt in range(max_retries):
            self._wait_for_rate_limit()
            
            try:
                return request_func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                error_msg = str(e).lower()
                if "quota" in error_msg or "rate" in error_msg:
                    raise RateLimitError("YouTube Music API rate limit reached")
                    
                delay = self._exponential_backoff(attempt)
                print(f"Request failed, retrying in {delay:.1f} seconds...")
                time.sleep(delay)
        
        raise Exception("Failed after maximum retries")
    
    def get_playlist(self, playlist_id: str) -> Playlist:
        """Get a playlist by its ID."""
        # Remove VL prefix if present
        if playlist_id.startswith("VL"):
            playlist_id = playlist_id[2:]
            
        playlist_data = self._make_request(
            self.client.get_playlist,
            playlist_id
        )
        return convert_youtube_to_model(playlist_data)
    
    def create_playlist(
        self,
        name: str,
        description: Optional[str] = None,
        public: bool = True
    ) -> str:
        """Create a new playlist."""
        privacy = "PUBLIC" if public else "PRIVATE"
        return self._make_request(
            self.client.create_playlist,
            title=name,
            description=description,
            privacy_status=privacy
        )
    
    def add_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Add tracks to a playlist."""
        video_ids = [t.platform_id for t in tracks if t.platform_id]
        if not video_ids:
            return False
            
        try:
            self.add_playlist_items(playlist_id, video_ids)
            return True
        except Exception as e:
            print(f"Error adding tracks to YouTube Music playlist: {e}")
            return False
    
    def remove_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Remove tracks from a playlist."""
        video_ids = [t.platform_id for t in tracks if t.platform_id]
        if not video_ids:
            return False
            
        try:
            self.remove_playlist_items(playlist_id, video_ids)
            return True
        except Exception as e:
            print(f"Error removing tracks from YouTube Music playlist: {e}")
            return False
    
    def add_playlist_items(self, playlist_id: str, video_ids: List[str]) -> Dict:
        """Add tracks to a playlist."""
        return self._make_request(
            self.client.add_playlist_items,
            playlist_id,
            video_ids
        )
    
    def remove_playlist_items(self, playlist_id: str, video_ids: List[str]) -> Dict:
        """Remove tracks from a playlist."""
        return self._make_request(
            self.client.remove_playlist_items,
            playlist_id,
            video_ids
        )
    
    def search_track(
        self,
        query: str,
        limit: int = 3,
        filter_singles: bool = True
    ) -> List[Track]:
        """Search for tracks matching the query."""
        results = self._make_request(
            self.client.search,
            query,
            filter="songs",
            limit=limit
        )
        
        tracks = []
        for item in results:
            if not item or item.get("resultType") != "song":
                continue
                
            # Skip results that are marked as singles if filter_singles is True
            if (filter_singles and 
                item.get("album", {}).get("type", "").lower() == "single"):
                continue
                
            try:
                video_id = item.get("videoId")
                if not video_id:
                    continue
                    
                track = Track(
                    title=item.get("title", "Unknown"),
                    artists=[
                        Artist(name=a.get("name", "Unknown Artist"))
                        for a in item.get("artists", [])
                        if isinstance(a, dict)
                    ],
                    platform="youtube",
                    duration_ms=item.get("duration_seconds", 0) * 1000,
                    album_name=item.get("album", {}).get("name"),
                    platform_id=video_id,
                    url=f"https://music.youtube.com/watch?v={video_id}"
                )
                tracks.append(track)
            except Exception as e:
                print(f"Error converting search result: {e}")
                continue
            
        return tracks
    
    def update_playlist_details(
        self,
        playlist_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[bool] = None
    ) -> bool:
        """Update playlist metadata."""
        try:
            privacy = "PUBLIC" if public else "PRIVATE" if public is not None else None
            self._make_request(
                self.client.edit_playlist,
                playlistId=playlist_id,
                title=name,
                description=description,
                privacyStatus=privacy
            )
            return True
        except Exception as e:
            print(f"Error updating playlist details: {e}")
            return False
