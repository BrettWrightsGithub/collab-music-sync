import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

def setup_spotify_auth():
    print("Spotify Authentication Setup")
    print("----------------------------")
    print("Before running this script, you need to:")
    print("1. Go to https://developer.spotify.com/dashboard")
    print("2. Log in with your Spotify account")
    print("3. Create a new application")
    print("4. Get your Client ID and Client Secret")
    print("5. Add 'http://localhost:8888/callback' to your Redirect URIs in the app settings")
    print("\nThen, create a .env file with the following:")
    print("SPOTIFY_CLIENT_ID=your_client_id")
    print("SPOTIFY_CLIENT_SECRET=your_client_secret")
    print("SPOTIFY_REDIRECT_URI=http://localhost:8888/callback")
    
    input("\nPress Enter once you've completed these steps...")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if environment variables are set
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        if not all([client_id, client_secret, redirect_uri]):
            print("\nError: Missing environment variables. Please check your .env file.")
            return
        
        # Initialize Spotify client with full access scope
        scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))
        
        # Test the connection
        user = sp.current_user()
        print(f"\nAuthentication successful!")
        print(f"Connected as: {user['display_name']} ({user['email']})")
        
    except Exception as e:
        print(f"\nError during setup: {str(e)}")

if __name__ == "__main__":
    setup_spotify_auth()
