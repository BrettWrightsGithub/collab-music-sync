from typing import Dict, Any, List
from datetime import datetime
from ..models.playlist import Playlist, Track, Artist

def convert_spotify_to_model(spotify_data: Dict[str, Any]) -> Playlist:
    """Convert Spotify playlist data to unified model."""
    if not spotify_data:
        raise ValueError("No Spotify data provided")
        
    def convert_track(track_data: Dict[str, Any]) -> Track:
        # Handle both direct track data and track wrapper from playlist items
        track = track_data.get("track", track_data)
        if not track:
            raise ValueError("Invalid track data")
            
        # Extract artist information safely
        artists = []
        for artist in track.get("artists", []):
            if not isinstance(artist, dict):
                continue
            artist_id = artist.get("id")
            artists.append(Artist(
                name=artist.get("name", "Unknown Artist"),
                id=artist_id,
                url=f"https://open.spotify.com/artist/{artist_id}" if artist_id else None
            ))
        
        # Extract album information safely
        album = track.get("album", {}) or {}
        
        # Get track ID safely
        track_id = track.get("id")
        if not track_id:
            raise ValueError("Track ID is missing")
            
        return Track(
            title=track.get("name", "Unknown Track"),
            artists=artists,
            platform="spotify",
            duration_ms=track.get("duration_ms"),
            album_name=album.get("name"),
            album_id=album.get("id"),
            platform_id=track_id,
            is_explicit=track.get("explicit", False),
            is_available=True,  # Spotify filters unavailable tracks by market
            url=f"https://open.spotify.com/track/{track_id}"
        )

    # Convert tracks safely
    tracks = []
    
    # Handle both direct track lists and playlist track objects
    items = []
    if "tracks" in spotify_data:
        # This is a playlist object
        items = spotify_data["tracks"].get("items", [])
    else:
        # This is a direct track list
        items = spotify_data.get("items", [])
    
    print(f"Processing {len(items)} tracks from Spotify data")
    for item in items:
        try:
            if item:  # Skip None or empty items
                track = convert_track(item)
                tracks.append(track)
                print(f"Successfully converted track: {track.title}")
        except ValueError as e:
            print(f"Warning: Skipping invalid track: {e}")
            continue
    print(f"Successfully converted {len(tracks)} tracks")

    # Get the highest resolution thumbnail URL if available
    thumbnail_url = None
    images = spotify_data.get("images", [])
    if images and isinstance(images, list):
        valid_images = []
        for img in images:
            if isinstance(img, dict):
                width = img.get("width", 0)
                height = img.get("height", 0)
                url = img.get("url")
                if width and height and url:
                    valid_images.append((width * height, url))
        
        if valid_images:
            # Sort by resolution and get the highest
            thumbnail_url = sorted(valid_images, reverse=True)[0][1]

    # Get playlist ID safely
    playlist_id = spotify_data.get("id")
    if not playlist_id:
        raise ValueError("Playlist ID is missing")

    return Playlist(
        id=playlist_id,
        title=spotify_data.get("name", "Unknown Playlist"),
        tracks=tracks,
        platform="spotify",
        owner_id=spotify_data.get("owner", {}).get("id"),
        description=spotify_data.get("description"),
        is_public=spotify_data.get("public", True),
        track_count=len(tracks),
        thumbnail_url=thumbnail_url,
        last_modified=None  # Spotify doesn't provide this information
    )
