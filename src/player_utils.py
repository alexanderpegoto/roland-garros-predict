from datetime import datetime
import pandas as pd
from src.config import *

def initialize_player(player_id, player_name):
    """Initialize a new player with starting ratings and metadata"""
    return {
        'name': player_name,
        'ratings': {
            'Hard': 1300,
            'Clay': 1300,
            'Grass': 1300,
            'Carpet': 1300
        },
        'last_match_date': None,
        'total_matches': 0
    }
    
def update_player_match_info(player_data, match_date):
    """Update player's last match date and total matches count"""
    player_data['last_match_date'] = match_date
    player_data['total_matches'] += 1
    
def apply_rating_decay(players_dict, current_date=None, decay_rate=0.92, strong_decay_rate=0.85):
    """Apply exponential decay to players innactivity penalizing not playing vs active players"""
    if current_date is None:
        current_date = datetime.now()
        
    for player_id, player_data in players_dict.items():
        if player_data['last_match_date'] is not None:
            days_inactive = (current_date - player_data['last_match_date']).days
            
            if days_inactive > 365:  # 1 year threshold
                if days_inactive > 730:  # 2+ years = strong decay
                    decay_factor = strong_decay_rate ** (days_inactive / 365)
                else:
                    decay_factor = decay_rate ** (days_inactive / 365)
                    
                for surface in player_data['ratings']:
                    current_rating = player_data['ratings'][surface]
                    player_data['ratings'][surface] = 1300 + (current_rating - 1300) * decay_factor
                    
def add_or_update_player(players_dict, player_id, player_name, match_date):
    """Add new player or update existing player info"""
    if player_id not in players_dict:
        players_dict[player_id] = initialize_player(player_id, player_name)
    else:
        # Update name in case it was "Unknown" before
        players_dict[player_id]['name'] = player_name
    
    update_player_match_info(players_dict[player_id], match_date)
    
def get_player_rating(players_dict, player_id, surface):
    """Get a player's current rating for a specific surface"""
    if player_id in players_dict:
        return players_dict[player_id]['ratings'].get(surface, STARTING_RATING)
    return STARTING_RATING
    

def update_player_rating(player_data, surface, rating_change):
    """Update a player's rating for a specific surface"""
    player_data['ratings'][surface] += rating_change
    
    