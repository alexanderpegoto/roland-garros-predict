"""
Configuration file for Tennis ELO Rating System
Adjust these parameters to tune the system behavior
"""

# =============================================================================
# ELO SYSTEM PARAMETERS
# =============================================================================

# Base K-factor for rating changes
BASE_K_FACTOR = 32

# Tournament importance multipliers
TOURNAMENT_WEIGHTS = {
    'G': 1.5,    # Grand Slam
    'M': 1.25,   # Masters 1000
    'A': 1.0,    # ATP 500/250
    'D': 1.0,    # Davis Cup / Other
}

# Margin of Victory thresholds
MOV_THRESHOLDS = {
    'DOMINANT': 0.75,    # 75%+ games won
    'SOLID': 0.65,       # 65%+ games won  
    'CLOSE': 0.55,       # 55%+ games won
    'VERY_CLOSE': 0.55   # Below 55% games won
}

# MOV multipliers
MOV_MULTIPLIERS = {
    'DOMINANT': 1.2,
    'SOLID': 1.1, 
    'CLOSE': 1.0,
    'VERY_CLOSE': 0.9
}

# =============================================================================
# PLAYER MANAGEMENT
# =============================================================================

# Starting rating for new players
STARTING_RATING = 1300

# Valid surfaces
VALID_SURFACES = ['Hard', 'Clay', 'Grass', 'Carpet']

# Surface weights for overall rankings
SURFACE_WEIGHTS = {
    'Hard': 0.5,    # Most common surface
    'Clay': 0.3,    # Second most common
    'Grass': 0.1,   # Limited season
    'Carpet': 0.1   # Rare nowadays
}

# =============================================================================
# RATING DECAY PARAMETERS
# =============================================================================

# Decay rates for inactive players
DECAY_RATE = 0.92           # Normal decay rate
STRONG_DECAY_RATE = 0.85    # For players inactive 2+ years

# Inactivity thresholds (in days)
DECAY_THRESHOLD = 365       # Start decay after 1 year
STRONG_DECAY_THRESHOLD = 730  # Strong decay after 2 years

# How often to apply decay during processing (every N matches)
DECAY_FREQUENCY = 1000

# =============================================================================
# ACTIVE PLAYER FILTERS
# =============================================================================

# Thresholds for considering players "active"
ACTIVE_MONTHS_THRESHOLD = 18    # Must have played in last 18 months
MIN_MATCHES_ACTIVE = 20         # Minimum matches to be considered active

# Thresholds for rankings display
MIN_MATCHES_RANKING = 50        # Minimum matches to appear in rankings
TOP_N_DISPLAY = 20              # How many players to show in rankings

# =============================================================================
# FILE PATHS AND DATA
# =============================================================================

# Data directory and files
DATA_FOLDER = "data"
HISTORICAL_DATA_PATTERN = "atp_matches_*.csv"
RANKINGS_FILE = "atp_rankings_current.csv"
NEW_DATA_FILE = "atp_tennis.csv"  # 2025 data

# Output files
OUTPUT_FILE = "tennis_elo_ratings.json"
RANKINGS_OUTPUT = "current_rankings.json"

# =============================================================================
# DISPLAY AND FORMATTING
# =============================================================================

# Number of players to show for each surface
SURFACE_TOP_N = 10

# Surfaces to display rankings for
DISPLAY_SURFACES = ['Hard', 'Clay', 'Grass']

# Ranking display format
RANKING_NAME_WIDTH = 25
RANKING_RATING_WIDTH = 6

# =============================================================================
# ANALYSIS PARAMETERS
# =============================================================================

# Surface specialist detection
SPECIALIST_MIN_MATCHES = 30
SPECIALIST_RATING_ADVANTAGE = 100  # Points above other surfaces

# Rising player detection
RISING_PLAYER_MONTHS = 6
RISING_PLAYER_MIN_MATCHES = 10
RISING_PLAYER_RATING_THRESHOLD = 1400

# =============================================================================
# DATA PROCESSING
# =============================================================================

# Date format for tournament dates
DATE_FORMAT = '%Y%m%d'

# Name cleaning parameters
UNKNOWN_PLAYER_NAME = "Unknown"

# Match validation
REQUIRED_MATCH_FIELDS = ['winner_id', 'loser_id', 'surface', 'tourney_date']

# =============================================================================
# DEBUGGING AND LOGGING
# =============================================================================

# Print debug information
DEBUG_MODE = False
VERBOSE_PROCESSING = True

# Progress reporting frequency
PROGRESS_FREQUENCY = 5000  # Print progress every N matches

# Validation checks
VALIDATE_RATINGS = True
MAX_RATING_CHANGE = 200  # Flag suspicious rating changes