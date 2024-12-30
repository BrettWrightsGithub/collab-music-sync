from gmusicapi import Mobileclient
import os
from dotenv import load_dotenv

def test_google_music_connection():
    # Load environment variables
    load_dotenv()
    
    # Create a mobile client
    api = Mobileclient()
    
    # The first time you run this, it will need to perform OAuth
    # This will open a browser window for authentication
    try:
        # Attempt to login
        logged_in = api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        
        if logged_in:
            print("Successfully logged into Google Play Music!")
            
            # Test by getting all user's playlists
            playlists = api.get_all_user_playlist_contents()
            print(f"Found {len(playlists)} playlists")
            
            # Print first playlist name if any exist
            if playlists:
                print(f"First playlist name: {playlists[0]['name']}")
        else:
            print("Failed to log in")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Always logout
        api.logout()

if __name__ == "__main__":
    test_google_music_connection()
