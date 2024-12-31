"""Test YouTube Music client with a real playlist."""
import os
from src.clients.youtube_client import YouTubeMusicClient

def main():
    # Initialize YouTube Music client
    youtube = YouTubeMusicClient()
    
    try:
        # Get playlist
        playlist_id = "PLkKimNAb9bUBoLdTRV45z9MYWWmEVZ_s8"
        print(f"\nFetching YouTube Music playlist {playlist_id}...")
        
        playlist = youtube.get_playlist(playlist_id)
        print(f"\nPlaylist: {playlist.title}")
        print(f"Number of tracks: {len(playlist.tracks)}")
        
        # Print first 5 tracks as a sample
        print("\nFirst 5 tracks:")
        for i, track in enumerate(playlist.tracks[:5], 1):
            print(f"\n{i}. {track.title}")
            print(f"   Artists: {', '.join(a.name for a in track.artists)}")
            if track.album_name:
                print(f"   Album: {track.album_name}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
