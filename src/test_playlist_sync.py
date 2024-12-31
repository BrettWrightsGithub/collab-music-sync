"""Test script for syncing real playlists between platforms."""
import os
import sys
from dotenv import load_dotenv
from src.clients.spotify_client import SpotifyClient
from src.clients.youtube_client import YouTubeMusicClient
from src.models.playlist import Playlist, Track
from src.matchers.track_matcher import TrackMatcher
from src.database.schema import init_db
from src.database.track_match_repository import TrackMatchRepository
from sqlalchemy.orm import Session

def check_youtube_auth():
    """Check if YouTube Music authentication file exists."""
    auth_locations = [
        "headers_auth.json",  # Current directory
        os.path.join(os.path.dirname(__file__), "..", "headers_auth.json"),  # Project root
        os.path.join(os.path.dirname(__file__), "headers_auth.json"),  # src directory
    ]
    
    for location in auth_locations:
        if os.path.exists(location):
            return os.path.abspath(location)
    
    print("Error: YouTube Music authentication file (headers_auth.json) not found.")
    print("Please run 'python src/setup_youtube_auth.py' first to set up authentication.")
    sys.exit(1)

def main():
    # Load environment variables from .env.local
    if not os.path.exists('.env.local'):
        print("Error: .env.local file not found. Please create it with your API credentials.")
        sys.exit(1)
        
    load_dotenv('.env.local')
    
    # Check for required environment variables
    required_vars = ["SPOTIFY_API_CLIENT_ID", "SPOTIFY_API_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env.local file")
        sys.exit(1)
    
    # Check YouTube Music authentication
    youtube_auth_path = check_youtube_auth()
    
    # Initialize database
    try:
        engine = init_db()
        session = Session(engine)
        repository = TrackMatchRepository(session)
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        sys.exit(1)
    
    try:
        # Initialize clients
        print("\nInitializing Spotify client...")
        spotify = SpotifyClient()  # Will use environment variables automatically
        
        print("\nInitializing YouTube Music client...")
        youtube = YouTubeMusicClient(headers_path=youtube_auth_path)
        youtube.authenticate()  # Explicitly authenticate
        print("YouTube Music authentication successful")
        
        # Test playlists to sync
        SPOTIFY_PLAYLIST_ID = "5no9IZk617jVrGH1TgIo5C"
        YOUTUBE_PLAYLIST_ID = "PLkKimNAb9bUBoLdTRV45z9MYWWmEVZ_s8"  # Removed VL prefix
        
        # Get Spotify playlist
        print("\nFetching Spotify playlist...")
        try:
            spotify_playlist = spotify.get_playlist(SPOTIFY_PLAYLIST_ID)
            print(f"Found Spotify playlist: {spotify_playlist.title}")
            print(f"Number of tracks: {len(spotify_playlist.tracks)}")
            
            if len(spotify_playlist.tracks) == 0:
                print("Warning: Spotify playlist is empty")
        except Exception as e:
            print(f"Error fetching Spotify playlist: {str(e)}")
            sys.exit(1)
        
        # Get YouTube playlist
        print("\nFetching YouTube playlist...")
        try:
            youtube_playlist = youtube.get_playlist(YOUTUBE_PLAYLIST_ID)
            print(f"Found YouTube playlist: {youtube_playlist.title}")
            print(f"Number of tracks: {len(youtube_playlist.tracks)}")
            
            if len(youtube_playlist.tracks) == 0:
                print("Warning: YouTube Music playlist is empty")
        except Exception as e:
            print(f"Error fetching YouTube playlist: {str(e)}")
            sys.exit(1)
        
        if len(spotify_playlist.tracks) == 0 or len(youtube_playlist.tracks) == 0:
            print("\nError: One or both playlists are empty. Cannot proceed with matching.")
            sys.exit(1)
        
        # Initialize matcher
        matcher = TrackMatcher(repository=repository)
        
        # Compare playlists
        print("\nComparing playlists...")
        matches = []
        unmatched = []
        
        for i, spotify_track in enumerate(spotify_playlist.tracks, 1):
            print(f"\nProcessing track {i}/{len(spotify_playlist.tracks)}")
            print(f"Looking for: {spotify_track.title} by {', '.join(a.name for a in spotify_track.artists)}")
            
            # Search for track on YouTube with rate limiting
            search_results = youtube.search_track(
                query=f"{spotify_track.title} {spotify_track.artists[0].name if spotify_track.artists else ''}"
            )
            
            if search_results:
                # Find best match
                best_match, confidence = matcher.find_best_match(spotify_track, search_results)
                if best_match and confidence > 0.7:
                    matches.append((spotify_track, best_match, confidence))
                    print(f" Found match: {best_match.title}")
                    print(f"  Confidence: {confidence:.2f}")
                    
                    # Save the match to the database
                    repository.save_match(
                        source_track=spotify_track,
                        target_track=best_match,
                        confidence_score=confidence
                    )
                else:
                    unmatched.append(spotify_track)
                    print(" No good match found")
            else:
                unmatched.append(spotify_track)
                print(" No search results found")
        
        # Print summary
        print("\nMatching Summary:")
        print(f"Total tracks in Spotify playlist: {len(spotify_playlist.tracks)}")
        print(f"Successfully matched: {len(matches)}")
        print(f"Unmatched tracks: {len(unmatched)}")
        
        if matches:
            print("\nMatched Tracks:")
            for spotify_track, youtube_track, confidence in matches:
                print(f"\nSpotify: {spotify_track.title} by {', '.join(a.name for a in spotify_track.artists)}")
                print(f"YouTube: {youtube_track.title} by {', '.join(a.name for a in youtube_track.artists)}")
                print(f"Confidence: {confidence:.2f}")
        
        if unmatched:
            print("\nUnmatched Tracks:")
            for track in unmatched:
                print(f"- {track.title} by {', '.join(a.name for a in track.artists)}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main()
