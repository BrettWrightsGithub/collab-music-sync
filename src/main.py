"""
Main script for syncing playlists between music platforms.
"""
import os
import sys
import argparse
from dotenv import load_dotenv
from src.clients.spotify_client import SpotifyClient
from src.clients.youtube_client import YouTubeMusicClient
from src.services.sync_service import PlaylistSyncService
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
    parser = argparse.ArgumentParser(description="Sync playlists between Spotify and YouTube Music")
    parser.add_argument("source", choices=["spotify", "youtube"], help="Source platform")
    parser.add_argument("target", choices=["spotify", "youtube"], help="Target platform")
    parser.add_argument("source_playlist_id", help="ID of the source playlist")
    parser.add_argument("--target-playlist-id", help="ID of the target playlist (if it exists)")
    parser.add_argument("--sync-metadata", action="store_true", help="Sync playlist metadata")
    args = parser.parse_args()

    # Load environment variables from .env.local
    if not os.path.exists('.env.local'):
        print("Error: .env.local file not found.")
        print("Please create .env.local with your Spotify API credentials.")
        sys.exit(1)
    load_dotenv('.env.local')

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
        print("\nInitializing clients...")
        spotify = SpotifyClient()  # Will use environment variables automatically
        youtube_auth_path = check_youtube_auth()
        youtube = YouTubeMusicClient(headers_path=youtube_auth_path)
        youtube.authenticate()

        # Create sync service
        sync_service = PlaylistSyncService(spotify, youtube)

        # Get source client and playlist
        source_client = spotify if args.source == "spotify" else youtube
        print(f"\nFetching source playlist from {args.source}...")
        source_playlist = source_client.get_playlist(args.source_playlist_id)
        print(f"Found playlist: {source_playlist.title}")
        print(f"Number of tracks: {len(source_playlist.tracks)}")

        if not args.target_playlist_id:
            # Create new playlist on target platform
            print(f"\nCreating new playlist on {args.target}...")
            target_playlist_id = sync_service.create_playlist(source_playlist, args.target)
            print(f"Created playlist with ID: {target_playlist_id}")
        else:
            target_playlist_id = args.target_playlist_id
            if args.sync_metadata:
                print("\nSyncing playlist metadata...")
                sync_service.sync_metadata(source_playlist, target_playlist_id, args.target)

        # Sync tracks
        print("\nSyncing tracks...")
        sync_service.sync_tracks(source_playlist, target_playlist_id, args.target)
        print("Track sync complete!")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
