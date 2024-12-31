"""Base client interface for music platform APIs."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.playlist import Playlist, Track

class BaseMusicClient(ABC):
    """Abstract base class for music platform clients."""
    
    @abstractmethod
    def authenticate(self) -> None:
        """Authenticate with the music platform."""
        pass
    
    @abstractmethod
    def get_playlist(self, playlist_id: str) -> Playlist:
        """Get a playlist by its ID.
        
        Args:
            playlist_id: The platform-specific playlist ID
            
        Returns:
            Playlist object with all track information
        """
        pass
    
    @abstractmethod
    def create_playlist(
        self,
        name: str,
        description: Optional[str] = None,
        public: bool = True
    ) -> str:
        """Create a new playlist.
        
        Args:
            name: Name of the playlist
            description: Optional description
            public: Whether the playlist should be public
            
        Returns:
            ID of the created playlist
        """
        pass
    
    @abstractmethod
    def add_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Add tracks to a playlist.
        
        Args:
            playlist_id: The platform-specific playlist ID
            tracks: List of tracks to add
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def remove_tracks(self, playlist_id: str, tracks: List[Track]) -> bool:
        """Remove tracks from a playlist.
        
        Args:
            playlist_id: The platform-specific playlist ID
            tracks: List of tracks to remove
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def search_track(
        self,
        title: str,
        artist: str,
        album: Optional[str] = None
    ) -> List[Track]:
        """Search for tracks matching the given criteria.
        
        Args:
            title: Track title
            artist: Artist name
            album: Optional album name
            
        Returns:
            List of matching tracks
        """
        pass
    
    @abstractmethod
    def update_playlist_details(
        self,
        playlist_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[bool] = None
    ) -> bool:
        """Update playlist metadata.
        
        Args:
            playlist_id: The platform-specific playlist ID
            name: New name (optional)
            description: New description (optional)
            public: New public/private status (optional)
            
        Returns:
            True if successful, False otherwise
        """
        pass
