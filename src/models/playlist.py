from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Artist:
    name: str
    id: Optional[str] = None
    url: Optional[str] = None

@dataclass
class Track:
    title: str
    artists: List[Artist]
    platform: str  # "youtube" or "spotify"
    duration_ms: Optional[int] = None
    album_name: Optional[str] = None
    album_id: Optional[str] = None
    platform_id: Optional[str] = None  # videoId for YouTube, track_id for Spotify
    is_explicit: bool = False
    is_available: bool = True
    url: Optional[str] = None

@dataclass
class Playlist:
    id: str
    title: str
    tracks: List[Track]
    platform: str  # "youtube" or "spotify"
    owner_id: Optional[str] = None
    description: Optional[str] = None
    is_public: bool = True
    track_count: Optional[int] = None
    duration_ms: Optional[int] = None
    thumbnail_url: Optional[str] = None
    last_modified: Optional[datetime] = None
    
    def __post_init__(self):
        if self.track_count is None:
            self.track_count = len(self.tracks)
