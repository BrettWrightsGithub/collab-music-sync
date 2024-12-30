# Music Playlist Sync

A Python application that syncs playlists between Spotify and Google Play Music.

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

3. Set up environment variables:
Create a `.env` file with your API credentials:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Project Structure
```
music-sync/
├── docs/
│   ├── googlePlay-api/
│   └── spotify_api/
├── src/
│   ├── google_play/
│   └── spotify/
├── tests/
├── .env
├── requirements.txt
└── README.md
```
