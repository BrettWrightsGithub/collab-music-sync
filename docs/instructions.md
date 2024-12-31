# Developer Instructions

This document serves as a guide for developers building and maintaining the **Cross Platform Playlist Sharing** project. It combines details from the Product Requirements Document (PRD) with the existing project structure and functionality already in place.

---

## Table of Contents

1. [Overview](#overview)  
2. [Directory Structure](#directory-structure)  
3. [Existing Functionality](#existing-functionality)  
4. [Dependencies](#dependencies)  
5. [Setup & Usage](#setup--usage)  
6. [Key Technical Requirements (From PRD)](#key-technical-requirements-from-prd)  
7. [Implementation Roadmap](#implementation-roadmap)  
8. [Troubleshooting & Support](#troubleshooting--support)

---

## 1. Overview

The **Cross Platform Playlist Sharing** project aims to **automate and synchronize playlist conversion** between different music streaming platforms (e.g., Spotify, YouTube Music). Users should be able to:

- **Fetch** playlist details from a source platform (Spotify/YouTube Music).  
- **Convert** the playlist to a target platform’s format.  
- **Maintain** consistent track order and metadata.  
- Optionally **synchronize** changes in near real-time (bidirectional sync).

This **Developer Instructions** file explains how the project is organized and what’s already built so you can quickly get up to speed. For more details about requirements and background context, refer to **PRD.md** in the root directory.

---

## 2. Directory Structure

Below is the high-level layout of the repository:

```
├─ .env.local              # Local environment configuration
├─ .env.template           # Template for environment variables
├─ .gitignore              # Git ignore rules
├─ README.md               # Project documentation and setup instructions
├─ requirements.txt        # Python dependencies
├─ headers_auth.json       # Authentication headers for API requests
├─ docs/
│  ├─ instructions.md      # Usage and setup instructions (this file)
│  └─ …
├─ PRD.md                  # Product Requirements Document
├─ spotify-authAndPlaylist.md   # Spotify authentication and playlist details
├─ samples/
│  ├─ youtube_music_playlist_sample.json
│  └─ spotify-get-playlist-response.json
├─ src/
│  ├─ google_play/         # Contains modules for Google Play Music (if needed)
│  ├─ spotify/             # Contains modules for Spotify
│  ├─ youtube_music/       # Contains modules for YouTube Music
│  └─ get_playlist_details.py   # Fetches playlist details from YouTube Music
└─ …
```

### Key Files & Directories

- **.env.local** / **.env.template**: Environment variables for API keys/secrets.  
- **requirements.txt**: Python libraries needed for API interactions and data processing.  
- **docs/**: Documentation assets (including this instructions file).  
- **samples/**: Contains sample response data from platforms, helpful for testing.  
- **src/**: Source code for the project, including platform-specific modules.

---

## 3. Existing Functionality

1. **Authentication**  
   - Scripts and configurations to handle API authentication for each platform (Spotify and YouTube Music).  
   - `headers_auth.json` for storing or referencing authentication headers.

2. **Data Fetching**  
   - `get_playlist_details.py` (in `src/youtube_music/` or the root of `src`) demonstrates how to fetch playlist details from YouTube Music.  
   - Similar approach under `src/spotify/` for fetching Spotify playlist details.

3. **Synchronization Logic**  
   - Initial scaffolding for comparing and updating playlists across platforms. This might currently exist as functions or placeholders within each platform’s module.

---

## 4. Dependencies

All dependencies are listed in **requirements.txt**. Key libraries might include:
- **Requests** (or **httpx**) for HTTP requests.  
- **python-dotenv** for managing environment variables.  
- **OAuth2** libraries for API token management.

Please ensure you install dependencies via:

```bash
pip install -r requirements.txt


5. Setup & Usage
	1.	Clone the Repository

    git clone <repo-url>
cd cross-platform-playlist-sharing

2. Set Up Environment
	•	Duplicate .env.template to .env.local and fill in required credentials (Spotify/YouTube Music client IDs, secrets, etc.).
	•	Ensure .env.local is listed in .gitignore to avoid committing secrets.

  3.  Install Dependencies


	4.	Run Script
	•	For YouTube Music:  python src/get_playlist_details.py --playlist_id <ID>
For Spotify (example):
python src/spotify/get_spotify_playlist.py --playlist_id <ID>


	•	More specific instructions for each script can be found in docs/ or each module’s README if available.

	5.	Check Sample Data
	•	Look at samples/youtube_music_playlist_sample.json or samples/spotify-get-playlist-response.json to understand the expected API response format.


----- 

6. Key Technical Requirements (From PRD)
	1.	Playlist Conversion
	•	Must handle direct metadata mapping (title, artist, album) and track ordering.
	2.	Bidirectional Sync (optional first MVP)
	•	Listen for changes or poll each platform for updated track listings.
	3.	Edge Case Handling
	•	Missing tracks, restricted songs, or partial matches.
	•	Rate limits from streaming platforms.
	4.	Security & Permissions
	•	Use OAuth best practices.
	•	Do not store sensitive tokens in plain text or in code.

For a full breakdown, refer to PRD.md.

7. Implementation Roadmap

Below is a suggested roadmap to build upon what’s already done:
	1.	Refine Authentication Flow
	•	Verify and streamline OAuth flows for Spotify/YouTube Music.
	•	Store refresh tokens securely.
	2.	Expand Data Fetching
	•	Ensure both Spotify and YouTube modules can handle large playlists and paging mechanisms.
	•	Implement robust error handling (e.g., timeouts, rate limit responses).
	3.	Build Conversion Module
	•	Create a utility function that takes a generic “playlist object” and converts it into platform-specific formats.
	•	Integrate fuzzy matching or direct track ID matching for better accuracy.
	4.	Sync & Update (Phase 2 / Optional)
	•	Decide on approach: webhooks (if available) vs. periodic polling.
	•	Implement partial updates if only certain tracks are modified.
	5.	Front-End or CLI
	•	If a user interface is desired, build a minimal UI or enhance the existing CLI scripts.
	•	Show progress and handle user input for mismatch resolution.
	6.	Testing
	•	Write unit tests for each module, especially for conversion logic.
	•	Conduct integration tests using sample playlists from both platforms.