from typing import Dict, List, Optional
from src.models.playlist import Playlist, Track
from src.clients.spotify_client import SpotifyClient
from src.clients.youtube_client import YouTubeMusicClient
from src.track_matcher import TrackMatcher

class PlaylistSyncService:
    """Service for syncing playlists between music platforms."""
    
    def __init__(self, spotify_client: SpotifyClient, youtube_client: YouTubeMusicClient):
        """Initialize the sync service with platform clients."""
        self.spotify_client = spotify_client
        self.youtube_client = youtube_client
        self.track_matcher = TrackMatcher()
    
    def create_playlist(self, source_playlist: Playlist, target_platform: str) -> str:
        """Create a new playlist on the target platform."""
        client = self._get_client(target_platform)
        
        # Create playlist with same metadata
        target_playlist_id = client.create_playlist(
            name=source_playlist.title,
            description=source_playlist.description or ""
        )
        
        return target_playlist_id
    
    def sync_tracks(self, source_playlist: Playlist, target_playlist_id: str, target_platform: str):
        """Sync tracks from source playlist to target playlist."""
        client = self._get_client(target_platform)
        
        # Get target platform tracks
        target_tracks = []
        for track in source_playlist.tracks:
            if not track.is_available:
                continue
                
            # Search for matching track on target platform
            query = f"{track.title} {track.artists[0].name if track.artists else ''}"
            matches = client.search_track(query=query)
            
            if matches:
                target_tracks.append(matches[0])
        
        # Add tracks to target playlist
        if target_tracks:
            client.add_tracks(
                playlist_id=target_playlist_id,
                tracks=target_tracks
            )
    
    def sync_metadata(self, source_playlist: Playlist, target_playlist_id: str, target_platform: str):
        """Sync playlist metadata (title, description, etc.)."""
        client = self._get_client(target_platform)
        
        client.update_playlist_details(
            playlist_id=target_playlist_id,
            title=source_playlist.title,
            description=source_playlist.description
        )
    
    def sync_changes(self, source_playlist_id: str, target_playlist_id: str, 
                    changes: Dict, source_platform: str, target_platform: str):
        """Sync changes from source to target playlist."""
        source_client = self._get_client(source_platform)
        target_client = self._get_client(target_platform)
        
        # Handle added tracks
        if changes.get("added"):
            for track in changes["added"]:
                query = f"{track.title} {track.artists[0].name if track.artists else ''}"
                matches = target_client.search_track(query=query)
                if matches:
                    target_client.add_tracks(
                        playlist_id=target_playlist_id,
                        tracks=[matches[0]]
                    )
        
        # Handle removed tracks
        if changes.get("removed"):
            target_client.remove_tracks(
                playlist_id=target_playlist_id,
                tracks=changes["removed"]
            )
        
        # Handle reordering
        if changes.get("reordered"):
            # Get current target playlist
            target_playlist = target_client.get_playlist(target_playlist_id)
            # Reorder tracks to match source playlist
            source_playlist = source_client.get_playlist(source_playlist_id)
            target_client.reorder_tracks(
                playlist_id=target_playlist_id,
                tracks=target_playlist.tracks,
                new_order=[t.platform_id for t in source_playlist.tracks]
            )
    
    def _get_client(self, platform: str):
        """Get the appropriate client for the given platform."""
        if platform == "spotify":
            return self.spotify_client
        elif platform == "youtube":
            return self.youtube_client
        else:
            raise ValueError(f"Unsupported platform: {platform}")
