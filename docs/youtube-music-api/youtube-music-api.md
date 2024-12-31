# YouTube Music API Integration

This document outlines the integration with YouTube Music API for the music playlist sync application.

## Overview

YouTube Music is Google's current music streaming service, replacing the discontinued Google Play Music. We use the unofficial `ytmusicapi` Python library to interact with YouTube Music.

Repository: [ytmusicapi](https://github.com/sigma67/ytmusicapi)
Documentation: [ytmusicapi.readthedocs.io](https://ytmusicapi.readthedocs.io/)

## Authentication

YouTube Music API requires authentication through browser headers. The process involves:

1. **Initial Setup**
   ```python
   from ytmusicapi import YTMusic
   YTMusic.setup(filepath='headers_auth.json')
   ```
   When running this command:
   - Open YouTube Music in your browser
   - Open Developer Tools (F12)
   - Go to Network tab
   - Look for any request (or refresh the page)
   - Find and copy everything AFTER 'accept: */*' in the request headers
   - Paste when prompted

2. **Using Authentication**
   ```python
   # Initialize with auth
   ytmusic = YTMusic('headers_auth.json')
   
   # Or use without auth (limited functionality)
   ytmusic = YTMusic()
   ```

## Basic Usage

1. **Search for Music**
   ```python
   # Search for a song
   results = ytmusic.search("song name", filter="songs")
   
   # Search for playlists
   playlists = ytmusic.search("playlist name", filter="playlists")
   ```

2. **Playlist Operations**
   ```python
   # Get your playlists
   playlists = ytmusic.get_library_playlists()
   
   # Create a playlist
   playlistId = ytmusic.create_playlist("Playlist Name", "Playlist Description")
   
   # Add songs to playlist
   ytmusic.add_playlist_items(playlistId, [videoId1, videoId2])
   ```

3. **Library Access**
   ```python
   # Get your library
   library = ytmusic.get_library_songs()
   
   # Get liked songs
   liked = ytmusic.get_liked_songs()
   ```

## Important Notes

1. Authentication is required for:
   - Accessing personal playlists
   - Creating/modifying playlists
   - Accessing library content
   - Liking/disliking songs

2. Some operations can be performed without authentication:
   - Searching for songs/albums/playlists
   - Getting public playlist contents
   - Getting song details

3. The `headers_auth.json` file contains sensitive information and should not be committed to version control.

## Error Handling

Common errors and their solutions:

1. **Authentication Failed**
   - Ensure you're logged into YouTube Music in your browser
   - Copy the complete headers after 'accept: */*'
   - Check that headers_auth.json exists and is valid

2. **Rate Limiting**
   - YouTube Music has rate limits
   - Implement appropriate delays between requests
   - Handle 429 (Too Many Requests) errors

## Best Practices

1. Store authentication file securely
2. Implement proper error handling
3. Cache results when appropriate
4. Respect rate limits
5. Validate inputs before making API calls
