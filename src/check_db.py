"""Script to check database contents."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.database.schema import TrackMatch, FailedMatch

def main():
    # Connect to database
    engine = create_engine('sqlite:///track_matches.db')
    session = Session(engine)
    
    # Check track matches
    print("\nTrack Matches:")
    print("-" * 80)
    matches = session.query(TrackMatch).all()
    if matches:
        for match in matches:
            print(f"\nSource: {match.source_platform} - {match.source_title} ({match.source_platform_id})")
            print(f"Target: {match.target_platform} - {match.target_title} ({match.target_platform_id})")
            print(f"Confidence: {match.confidence_score:.2f}")
            print(f"Last Verified: {match.last_verified}")
    else:
        print("No matches found in database")
    
    # Check failed matches
    print("\nFailed Matches:")
    print("-" * 80)
    failed = session.query(FailedMatch).all()
    if failed:
        for fail in failed:
            print(f"\nSource: {fail.source_platform} - {fail.source_title} ({fail.source_platform_id})")
            print(f"Target Platform: {fail.target_platform}")
            print(f"Error: {fail.error_reason}")
            print(f"Created At: {fail.created_at}")
    else:
        print("No failed matches found in database")

if __name__ == "__main__":
    main()
