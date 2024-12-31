from ytmusicapi import setup as ytsetup
import subprocess

def setup_youtube_auth():
    """
    Set up YouTube Music authentication using request headers from browser
    """
    print("YouTube Music Authentication Setup")
    print("----------------------------------")
    print("1. Open YouTube Music in your browser")
    print("2. Open Developer Tools (Cmd+Option+I)")
    print("3. Go to the Network tab")
    print("4. Filter requests by '/browse' in the search bar")
    print("5. Click on any POST request to music.youtube.com")
    print("6. In 'Request Headers' section, copy everything from 'accept: */*' to the end")
    print("7. The headers are now in your clipboard")
    print("\nRetrieving headers from clipboard...")
    
    try:
        # Use pbpaste to get headers from clipboard
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        headers_str = result.stdout
        
        if not headers_str.strip():
            print("No headers found in clipboard. Please copy the headers and try again.")
            return
            
        print("\nProcessing headers...")
        
        # Set up authentication
        ytsetup(filepath='headers_auth.json', headers_raw=headers_str)
        print("\nAuthentication successful! Created headers_auth.json")
        
        # Test the authentication
        from ytmusicapi import YTMusic
        yt = YTMusic('headers_auth.json')
        print("\nTesting connection...")
        try:
            # Try to get the user's library
            yt.get_library_playlists(limit=1)
            print("Connection test successful!")
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            
    except Exception as e:
        print(f"\nError during setup: {str(e)}")

if __name__ == "__main__":
    setup_youtube_auth()
