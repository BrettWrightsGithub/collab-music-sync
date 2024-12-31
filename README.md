# Music Playlist Sync

A Python application that syncs playlists between Spotify and YouTube Music.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Spotify API credentials:
Create a `.env.local` file with your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

4. Set up YouTube Music authentication:
```bash
python src/setup_youtube_auth.py
```
This will create a `headers_auth.json` file with your YouTube Music authentication.

## Usage

The application provides a command-line interface for syncing playlists:

```bash
# Create a new playlist on YouTube Music from a Spotify playlist
python src/main.py spotify youtube <spotify_playlist_id>

# Sync to an existing YouTube Music playlist
python src/main.py spotify youtube <spotify_playlist_id> --target-playlist-id <youtube_playlist_id>

# Sync metadata only (title, description) to an existing playlist
python src/main.py spotify youtube <spotify_playlist_id> --target-playlist-id <youtube_playlist_id> --sync-metadata

# Sync from YouTube Music to Spotify
python src/main.py youtube spotify <youtube_playlist_id>
```

## Project Structure
```
music-sync/
├── src/
│   ├── clients/           # Platform-specific API clients
│   ├── converters/        # Data conversion between platforms
│   ├── database/          # Database models and repositories
│   ├── matchers/          # Track matching logic
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── main.py           # Command-line interface
│   └── setup_youtube_auth.py  # YouTube Music authentication setup
├── tests/                 # Test files
├── .env.local            # Environment variables
├── requirements.txt      # Python dependencies
└── README.md
```

## Features

- Sync playlists between Spotify and YouTube Music in either direction
- Smart track matching using title, artist, and album information
- Cache successful matches to improve future syncs
- Sync playlist metadata (title, description)
- Command-line interface for easy usage

## Development

To run tests:
```bash
python -m pytest tests/
