from ytmusicapi import YTMusic
import json
import os
import time
from typing import Optional, Dict, Any
import random

class RateLimitError(Exception):
    """Raised when we detect rate limiting from the API"""
    pass

def exponential_backoff(attempt: int, max_delay: int = 32) -> float:
    """Calculate delay with exponential backoff and jitter"""
    delay = min(max_delay, 2 ** attempt)
    jitter = random.uniform(0, 0.1 * delay)
    return delay + jitter

def get_playlist_with_retry(yt: YTMusic, playlist_id: str, limit: Optional[int] = None, max_retries: int = 3) -> Dict[str, Any]:
    """
    Get playlist details with retry logic and exponential backoff
    """
    last_attempt = 0
    min_time_between_requests = 2  # minimum seconds between requests
    
    for attempt in range(max_retries):
        # Rate limiting
        time_since_last = time.time() - last_attempt
        if time_since_last < min_time_between_requests:
            time.sleep(min_time_between_requests - time_since_last)
        
        try:
            last_attempt = time.time()
            return yt.get_playlist(playlist_id, limit=limit)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            error_msg = str(e).lower()
            if "quota" in error_msg or "rate" in error_msg:
                raise RateLimitError("YouTube Music API rate limit reached")
                
            delay = exponential_backoff(attempt)
            print(f"Request failed, retrying in {delay:.1f} seconds...")
            time.sleep(delay)
    
    raise Exception("Failed to get playlist after maximum retries")

def get_playlist_details(playlist_id: str, limit: Optional[int] = None):
    """
    Get detailed information about a specific playlist with rate limiting and error handling
    
    Args:
        playlist_id: The YouTube Music playlist ID
        limit: Maximum number of tracks to fetch (None for all tracks)
    """
    try:
        # Remove VL prefix if present
        if playlist_id.startswith("VL"):
            playlist_id = playlist_id[2:]
            
        # Initialize YTMusic with our authentication
        yt = YTMusic('headers_auth.json')
        
        # Get playlist details with retry logic
        playlist = get_playlist_with_retry(yt, playlist_id, limit=limit)
        
        # Create samples directory if it doesn't exist
        samples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'samples')
        os.makedirs(samples_dir, exist_ok=True)
        
        # Save raw response to samples file
        samples_file = os.path.join(samples_dir, 'youtube_music_playlist_sample.json')
        with open(samples_file, 'w') as f:
            json.dump(playlist, f, indent=2)
            
        print(f"\nPlaylist: {playlist.get('title', 'Unknown')}")
        print("-" * 50)
        print(f"Description: {playlist.get('description', 'No description')}")
        print(f"Track count: {playlist.get('trackCount', 'Unknown')}")
        print(f"\nTracks:")
        
        for i, track in enumerate(playlist.get('tracks', []), 1):
            if not track:
                continue
                
            print(f"\n{i}. {track.get('title', 'Unknown Title')}")
            
            # Handle artists
            artists = []
            for artist in track.get('artists', []) or []:
                if artist and isinstance(artist, dict):
                    artists.append(artist.get('name', 'Unknown Artist'))
            print(f"   Artist: {', '.join(artists) if artists else 'Unknown Artist'}")
            
            # Handle album
            album = track.get('album')
            album_name = album.get('name') if album and isinstance(album, dict) else 'N/A'
            print(f"   Album: {album_name}")
            
            print(f"   Duration: {track.get('duration', 'N/A')}")
            print(f"   Video ID: {track.get('videoId', 'N/A')}")
            
        print(f"\nRaw response saved to: {samples_file}")
            
    except RateLimitError as e:
        print(f"Error: {str(e)}")
        print("Please wait a few minutes before trying again.")
    except Exception as e:
        print(f"Error fetching playlist: {str(e)}")

if __name__ == "__main__":
    # Family playlist ID
    playlist_id = "PLkKimNAb9bUBoLdTRV45z9MYWWmEVZ_s8"  # Removed VL prefix
    get_playlist_details(playlist_id)
