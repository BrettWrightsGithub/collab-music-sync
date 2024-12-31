"""Configuration settings for the track matcher."""

# Matching weights for different components
MATCHER_WEIGHTS = {
    'title_weight': 0.5,
    'artist_weight': 0.3,
    'album_weight': 0.2,
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    'high': 0.9,    # Consider this a definite match
    'medium': 0.7,  # Potentially a match, but might need verification
    'low': 0.5,     # Probably not a match
}

# Common words to ignore in comparisons
COMMON_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but',
    'feat', 'ft', 'featuring',
    'with', 'vs', 'versus',
}

# Version indicators that might appear in titles
VERSION_INDICATORS = [
    r'\(.*remix.*\)',
    r'\(.*edit.*\)',
    r'\(.*version.*\)',
    r'\(.*live.*\)',
    r'\(.*remaster.*\)',
    r'\(.*mix.*\)',
    r'\(.*radio.*\)',
    r'\(.*extended.*\)',
    r'\(.*original.*\)',
    r'\[.*remix.*\]',
    r'\[.*edit.*\]',
    r'\[.*version.*\]',
    r'\[.*live.*\]',
    r'\[.*remaster.*\]',
]

# Special characters to handle in normalization
SPECIAL_CHARS_MAP = {
    '&': 'and',
    '+': 'and',
    '@': 'at',
    '$': 's',
    '£': 'pounds',
    '€': 'euros',
    '%': 'percent',
}
