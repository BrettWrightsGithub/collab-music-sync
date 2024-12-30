from ytmusicapi import YTMusic

def setup_youtube_auth():
    print("YouTube Music Authentication Setup")
    print("----------------------------------")
    print("1. Open YouTube Music in your browser")
    print("2. Right-click anywhere on the page and select 'Inspect'")
    print("3. Go to the 'Network' tab")
    print("4. Click on any request (or refresh the page)")
    print("5. Look for 'Request Headers' and copy everything AFTER 'accept: */*'")
    print("\nWhen ready, the setup process will begin...")
    input("Press Enter to continue...")
    
    try:
        YTMusic.setup(filepath='headers_auth.json')
        print("\nAuthentication successful! Created headers_auth.json")
    except Exception as e:
        print(f"\nError during setup: {str(e)}")

if __name__ == "__main__":
    setup_youtube_auth()
