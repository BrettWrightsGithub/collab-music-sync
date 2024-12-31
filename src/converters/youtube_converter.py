from typing import Dict, Any, List
from datetime import datetime
from ..models.playlist import Playlist, Track, Artist

def convert_youtube_to_model(youtube_data: Dict[str, Any]) -> Playlist:
    """Convert YouTube Music playlist data to unified model."""
    
    def convert_track(track_data: Dict[str, Any]) -> Track:
        artists = [
            Artist(
                name=artist["name"],
                id=artist.get("id"),
                url=f"https://www.youtube.com/channel/{artist.get('id')}" if artist.get('id') else None
            )
            for artist in track_data.get("artists", [])
        ]
        
        return Track(
            title=track_data["title"],
            artists=artists,
            platform="youtube",
            platform_id=track_data["videoId"],
            album_name=track_data.get("album"),
            is_explicit=track_data.get("isExplicit", False),
            is_available=track_data.get("isAvailable", True),
            url=f"https://www.youtube.com/watch?v={track_data['videoId']}"
        )

    tracks = [convert_track(track) for track in youtube_data.get("tracks", [])]
    
    # Get the highest resolution thumbnail URL if available
    thumbnail_url = None
    if youtube_data.get("thumbnails"):
        thumbnails = sorted(
            youtube_data["thumbnails"],
            key=lambda x: x.get("width", 0) * x.get("height", 0),
            reverse=True
        )
        if thumbnails:
            thumbnail_url = thumbnails[0]["url"]

    return Playlist(
        id=youtube_data["id"],
        title=youtube_data["title"],
        tracks=tracks,
        platform="youtube",
        description=youtube_data.get("description"),
        is_public=youtube_data.get("privacy", "PUBLIC") == "PUBLIC",
        track_count=youtube_data.get("trackCount"),
        thumbnail_url=thumbnail_url,
        last_modified=None  # YouTube API doesn't provide this in the sample
    )
