"""Repository for managing track matches in the database."""
import json
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .schema import TrackMatch, FailedMatch
from ..models.playlist import Track

class TrackMatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_match(
        self,
        source_track: Track,
        target_platform: str,
        min_confidence: float = 0.7,
        max_age_days: int = 30
    ) -> Optional[Track]:
        """Get a matching track from the database if it exists and is recent enough."""
        min_date = datetime.utcnow() - timedelta(days=max_age_days)
        
        match = self.session.query(TrackMatch).filter(
            and_(
                TrackMatch.source_platform == source_track.platform,
                TrackMatch.source_platform_id == source_track.platform_id,
                TrackMatch.target_platform == target_platform,
                TrackMatch.confidence_score >= min_confidence,
                TrackMatch.last_verified >= min_date
            )
        ).first()

        if match:
            return Track(
                title=match.target_title,
                artists=json.loads(match.target_artists),
                platform=match.target_platform,
                platform_id=match.target_platform_id,
                album_name=match.target_album
            )
        return None

    def save_match(
        self,
        source_track: Track,
        target_track: Track,
        confidence_score: float,
        manually_verified: bool = False
    ) -> TrackMatch:
        """Save a track match to the database."""
        match = TrackMatch(
            source_platform=source_track.platform,
            source_platform_id=source_track.platform_id,
            source_title=source_track.title,
            source_artists=json.dumps([a.name for a in source_track.artists]),
            source_album=source_track.album_name,
            
            target_platform=target_track.platform,
            target_platform_id=target_track.platform_id,
            target_title=target_track.title,
            target_artists=json.dumps([a.name for a in target_track.artists]),
            target_album=target_track.album_name,
            
            confidence_score=confidence_score,
            manually_verified=manually_verified
        )
        
        self.session.add(match)
        self.session.commit()
        return match

    def save_failed_match(
        self,
        source_track: Track,
        target_platform: str,
        error_reason: str
    ) -> FailedMatch:
        """Save a failed match attempt for analysis."""
        failed = FailedMatch(
            source_platform=source_track.platform,
            source_platform_id=source_track.platform_id,
            source_title=source_track.title,
            source_artists=json.dumps([a.name for a in source_track.artists]),
            target_platform=target_platform,
            error_reason=error_reason
        )
        
        self.session.add(failed)
        self.session.commit()
        return failed

    def get_match_statistics(self) -> dict:
        """Get statistics about track matches."""
        total_matches = self.session.query(TrackMatch).count()
        verified_matches = self.session.query(TrackMatch).filter(
            TrackMatch.manually_verified == True
        ).count()
        failed_matches = self.session.query(FailedMatch).count()
        
        return {
            "total_matches": total_matches,
            "verified_matches": verified_matches,
            "failed_matches": failed_matches
        }

    def update_match_verification(
        self,
        match_id: int,
        verified: bool = True
    ) -> Optional[TrackMatch]:
        """Update the verification status of a match."""
        match = self.session.query(TrackMatch).get(match_id)
        if match:
            match.manually_verified = verified
            match.last_verified = datetime.utcnow()
            self.session.commit()
        return match
