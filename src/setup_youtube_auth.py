"""Setup script for YouTube Music authentication."""
from ytmusicapi import setup_oauth

def main():
    print("Setting up YouTube Music OAuth...")
    print("This will open your browser to complete the authentication process.")
    print("After authenticating, the headers file will be saved as 'headers_auth.json'")
    
    try:
        setup_oauth("headers_auth.json")
        print("\nSuccess! Authentication headers have been saved to 'headers_auth.json'")
    except Exception as e:
        print(f"Error during setup: {str(e)}")

if __name__ == "__main__":
    main()
