from ytmusicapi import YTMusic
import os
from dotenv import load_dotenv

def test_youtube_music_connection():
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize YouTube Music API in unauthenticated mode first
        ytmusic = YTMusic()
        
        # Test by searching for a song
        search_results = ytmusic.search("Test", filter="songs", limit=1)
        if search_results:
            print("Successfully connected to YouTube Music API!")
            print(f"Found song: {search_results[0]['title']} by {search_results[0]['artists'][0]['name']}")
            
            print("\nNote: To access your personal playlists, you'll need to set up authentication.")
            print("Run the following in a Python shell to set up:")
            print("from ytmusicapi import YTMusic")
            print("YTMusic.setup(filepath='headers_auth.json')")
            print("This will create a headers_auth.json file with your credentials.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_youtube_music_connection()
