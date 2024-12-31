from ytmusicapi import YTMusic

def list_playlists():
    """
    List all playlists in your YouTube Music library
    """
    try:
        # Initialize YTMusic with our authentication
        yt = YTMusic('headers_auth.json')
        
        # Get all playlists
        playlists = yt.get_library_playlists(limit=None)
        
        print("\nYour YouTube Music Playlists:")
        print("-" * 50)
        
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist['title']}")
            print(f"   - {playlist.get('count', 'N/A')} tracks")
            print(f"   - ID: {playlist['playlistId']}")
            print()
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_playlists()
