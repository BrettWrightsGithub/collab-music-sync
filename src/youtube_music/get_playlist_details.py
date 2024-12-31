from ytmusicapi import YTMusic
import json
import os

def get_playlist_details(playlist_id):
    """
    Get detailed information about a specific playlist
    """
    try:
        # Initialize YTMusic with our authentication
        yt = YTMusic('headers_auth.json')
        
        # Get playlist details
        playlist = yt.get_playlist(playlist_id, limit=None)
        
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
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Family playlist ID
    playlist_id = "PLkKimNAb9bUAIlOJFE_xUFJNmpnt-DZKq"
    get_playlist_details(playlist_id)
