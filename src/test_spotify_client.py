"""Test Spotify client with a real playlist."""
import os
from dotenv import load_dotenv
from src.clients.spotify_client import SpotifyClient

def main():
    # Load environment variables from .env.local
    load_dotenv('.env.local')
    
    # Initialize Spotify client
    spotify = SpotifyClient(
        client_id=os.getenv("SPOTIFY_API_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_API_CLIENT_SECRET"),
        redirect_uri="http://localhost:8888/callback"
    )
    
    try:
        # Get playlist
        playlist_id = "5no9IZk617jVrGH1TgIo5C"
        print(f"\nFetching Spotify playlist {playlist_id}...")
        
        playlist = spotify.get_playlist(playlist_id)
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
