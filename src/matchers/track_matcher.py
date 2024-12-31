from typing import List, Tuple, Optional
import re
from difflib import SequenceMatcher
from src.models.playlist import Track, Artist
from src.database.track_match_repository import TrackMatchRepository

class TrackMatcher:
    def __init__(self, 
                 repository: TrackMatchRepository,
                 title_weight: float = 0.5, 
                 artist_weight: float = 0.3, 
                 album_weight: float = 0.2):
        """Initialize the track matcher with configurable weights for different components.
        
        Args:
            repository: Database repository for caching matches
            title_weight: Weight given to title similarity (default: 0.5)
            artist_weight: Weight given to artist similarity (default: 0.3)
            album_weight: Weight given to album similarity (default: 0.2)
        """
        self.repository = repository
        self.title_weight = title_weight
        self.artist_weight = artist_weight
        self.album_weight = album_weight

    def match_tracks(self, track1: Track, track2: Track) -> float:
        """Match two tracks and return a confidence score between 0 and 1."""
        if track1.platform_id == track2.platform_id and track1.platform == track2.platform:
            return 1.0

        title_score = self._compare_titles(track1.title, track2.title)
        artist_score = self._compare_artists(track1.artists, track2.artists)
        album_score = self._compare_albums(track1.album_name, track2.album_name)

        # Calculate weighted average
        total_score = (
            title_score * self.title_weight +
            artist_score * self.artist_weight +
            album_score * self.album_weight
        )

        return total_score

    def _normalize_string(self, s: str) -> str:
        """Normalize string for comparison by removing special characters and converting to lowercase."""
        if not s:
            return ""
        
        # Remove special characters and convert to lowercase
        s = re.sub(r'[^\w\s]', '', s.lower())
        
        # Remove common filler words
        filler_words = {'the', 'a', 'an', 'and', 'or', 'but', 'feat', 'ft', 'featuring'}
        words = s.split()
        words = [w for w in words if w not in filler_words]
        
        return ' '.join(words)

    def _compare_titles(self, title1: str, title2: str) -> float:
        """Compare two track titles and return a similarity score."""
        if not title1 or not title2:
            return 0.0

        # Normalize titles
        norm_title1 = self._normalize_string(title1)
        norm_title2 = self._normalize_string(title2)

        # Check for exact match after normalization
        if norm_title1 == norm_title2:
            return 1.0

        # Remove common suffixes like "(Radio Edit)", "(Live)", etc.
        common_suffixes = [
            r'\(.*remix.*\)',
            r'\(.*edit.*\)',
            r'\(.*version.*\)',
            r'\(.*live.*\)',
            r'\(.*remaster.*\)',
            r'\[.*remix.*\]',
            r'\[.*edit.*\]',
            r'\[.*version.*\]',
            r'\[.*live.*\]',
            r'\[.*remaster.*\]'
        ]
        
        for suffix in common_suffixes:
            norm_title1 = re.sub(suffix, '', norm_title1, flags=re.IGNORECASE).strip()
            norm_title2 = re.sub(suffix, '', norm_title2, flags=re.IGNORECASE).strip()

        # Use sequence matcher for fuzzy matching
        return SequenceMatcher(None, norm_title1, norm_title2).ratio()

    def _compare_artists(self, artists1: List[Artist], artists2: List[Artist]) -> float:
        """Compare two lists of artists and return a similarity score."""
        if not artists1 or not artists2:
            return 0.0

        # Get normalized artist names
        names1 = {self._normalize_string(artist.name) for artist in artists1}
        names2 = {self._normalize_string(artist.name) for artist in artists2}

        # If either list is empty after normalization, return 0
        if not names1 or not names2:
            return 0.0

        # Find best matches for each artist
        matches = []
        for name1 in names1:
            best_match = max(
                (SequenceMatcher(None, name1, name2).ratio() for name2 in names2),
                default=0.0
            )
            matches.append(best_match)

        # Return average of best matches
        return sum(matches) / len(matches)

    def _compare_albums(self, album1: str, album2: str) -> float:
        """Compare two album names and return a similarity score."""
        if not album1 or not album2:
            return 0.5  # Neutral score if album info is missing

        return SequenceMatcher(
            None,
            self._normalize_string(album1),
            self._normalize_string(album2)
        ).ratio()

    def find_best_match(self, track: Track, candidates: List[Track]) -> Tuple[Optional[Track], float]:
        """Find the best matching track from a list of candidates.
        
        Args:
            track: The track to find matches for
            candidates: List of potential matching tracks
            
        Returns:
            Tuple of (best_matching_track, confidence_score)
        """
        # First check the database for a cached match
        if candidates and len(candidates) > 0:
            cached_match = self.repository.get_match(
                source_track=track,
                target_platform=candidates[0].platform
            )
            if cached_match:
                # Find the cached match in candidates if it exists
                for candidate in candidates:
                    if (candidate.platform == cached_match.platform and 
                        candidate.platform_id == cached_match.platform_id):
                        return candidate, 1.0

        # If no cached match found, perform matching
        if not candidates:
            self.repository.save_failed_match(
                source_track=track,
                target_platform=candidates[0].platform if candidates else "unknown",
                error_reason="No candidates available"
            )
            return None, 0.0

        matches = [(t, self.match_tracks(track, t)) for t in candidates]
        best_match = max(matches, key=lambda x: x[1])
        
        # Cache the match if confidence is high enough
        if best_match[1] >= 0.7:
            self.repository.save_match(
                source_track=track,
                target_track=best_match[0],
                confidence_score=best_match[1]
            )
        elif best_match[1] < 0.5:
            self.repository.save_failed_match(
                source_track=track,
                target_platform=candidates[0].platform,
                error_reason=f"Low confidence match: {best_match[1]}"
            )
        
        return best_match
