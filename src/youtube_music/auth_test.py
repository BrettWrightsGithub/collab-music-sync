from ytmusicapi import YTMusic
import os
import json
from pathlib import Path

def create_manual_auth_file():
    """
    Create a headers_auth.json file manually with the required structure
    """
    headers_template = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "x-client-data": "CI22yQEIo7bJAQjEtskBCPqcygEIqZ3KAQ==",
        "x-youtube-client-name": "1",
        "x-youtube-client-version": "2.20231219.09.00",
        "Cookie": "YOUR_COOKIE_HERE"  # This needs to be replaced with actual cookie
    }
    
    with open('headers_auth.json', 'w') as f:
        json.dump(headers_template, f, indent=2)
    
    print("\nCreated headers_auth.json template.")
    print("\nTo complete setup:")
    print("1. Open YouTube Music (https://music.youtube.com)")
    print("2. Make sure you're logged in")
    print("3. Press F12 to open Developer Tools")
    print("4. Go to Network tab")
    print("5. Refresh the page")
    print("6. Click on any request (like 'browse' or 'next')")
    print("7. In the request headers, find and copy the entire 'Cookie' header value")
    print("8. Open headers_auth.json and replace 'YOUR_COOKIE_HERE' with the copied cookie")
    print("\nAfter updating the file, run this script again to test the authentication.")

def test_youtube_auth():
    """
    Test YouTube Music authentication and basic API functionality
    """
    # Use absolute path for auth file
    auth_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'headers_auth.json')
    
    print("YouTube Music Authentication Test")
    print("--------------------------------")
    
    # Check if auth file exists
    if not Path(auth_file).exists():
        print("\nNo authentication file found. Creating template...")
        create_manual_auth_file()
        return
    
    try:
        # Try to initialize with auth
        print("\nTesting authenticated access...")
        ytmusic = YTMusic(auth_file)
        
        # Test getting library playlists (requires auth)
        playlists = ytmusic.get_library_playlists()
        print(f"\nSuccess! Found {len(playlists)} playlists in your library.")
        
        if playlists:
            print("\nYour playlists:")
            for playlist in playlists:
                print(f"- {playlist['title']}")
        
        print("\nAuthentication test completed successfully!")
        
    except Exception as e:
        print(f"\nError testing authentication: {str(e)}")
        print("Please ensure you're logged into YouTube Music and the cookie in headers_auth.json is valid.")
        print("You may need to update the cookie value if it has expired.")

if __name__ == "__main__":
    test_youtube_auth()
