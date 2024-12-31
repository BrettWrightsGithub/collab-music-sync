class TrackMatcher:
    """Class for matching tracks between different platforms."""
    
    def match(self, spotify_track, youtube_track):
        """Match a Spotify track with a YouTube track based on title and artist."""
        # Simple matching logic based on title and first artist
        return (spotify_track.title.lower() == youtube_track.title.lower() and
                spotify_track.artists[0].name.lower() == youtube_track.artists[0].name.lower())
    
    def find_best_match(self, spotify_tracks, youtube_tracks):
        """Find the best match for a list of Spotify tracks in YouTube tracks."""
        matches = []
        for s_track in spotify_tracks:
            for y_track in youtube_tracks:
                if self.match(s_track, y_track):
                    matches.append((s_track, y_track))
                    break
        return matches
