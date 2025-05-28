from datetime import datetime
import pandas as pd
from src.config import *

def initialize_player(player_id, player_name):
    """Initialize a new player with starting ratings and metadata"""
    return {
        'name': player_name,
        'ratings': {surface: STARTING_RATING for surface in VALID_SURFACES},
        'matches_played': {surface: 0 for surface in VALID_SURFACES},
        'total_matches': 0,
        'last_match_date': None,
        'peak_rating': {surface: STARTING_RATING for surface in VALID_SURFACES},
        'peak_rating_date': {surface: None for surface in VALID_SURFACES}
    }
    
def update_player_after_match(player_data, surface, new_rating, match_date):
    """Update player data after a match"""
    # Update rating
    player_data['ratings'][surface] = new_rating
    
    # Update match counts
    player_data['matches_played'][surface] += 1
    player_data['total_matches'] += 1
    
    # Update last match date
    current_last_date = player_data.get('last_match_date')
    if current_last_date is None or match_date > current_last_date:
        player_data['last_match_date'] = match_date
    
    # Check for new peak rating
    if new_rating > player_data['peak_rating'][surface]:
        player_data['peak_rating'][surface] = new_rating
        player_data['peak_rating_date'][surface] = match_date
    
def apply_rating_decay(players_dict, current_date=None, starting_rating=1500):
    """
    Applies decay to player Elo ratings based on inactivity.
    Uses DECAY_RATE and STRONG_DECAY_RATE depending on time since last match.
    """

    if current_date is None:
        current_date = datetime.now()

    for player_id, player_data in players_dict.items():
        last_date = player_data.get('last_match_date')
        if last_date is None:
            continue

        days_inactive = (current_date - last_date).days

        # Decide decay strength
        if days_inactive > STRONG_DECAY_THRESHOLD:
            decay_rate = STRONG_DECAY_RATE
        elif days_inactive > DECAY_THRESHOLD:
            decay_rate = DECAY_RATE
        else:
            continue  # No decay applied

        # Apply exponential decay based on time
        decay_factor = decay_rate ** (days_inactive / 365)

        # Update all ratings (surface-specific)
        for surface in player_data['ratings']:
            old_rating = player_data['ratings'][surface]
            new_rating = starting_rating + (old_rating - starting_rating) * decay_factor
            player_data['ratings'][surface] = new_rating
            
        