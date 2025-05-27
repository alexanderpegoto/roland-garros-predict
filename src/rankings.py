import pandas as pd
from datetime import datetime

def get_active_players_from_rankings(players_dict, rankings_file="data/atp_rankings_current.csv"):
    """Get active players from ATP rankings file"""
    # Read the rankings file
    rankings_df = pd.read_csv(rankings_file)
    
    # Get unique player IDs from all ranking dates
    unique_player_ids = rankings_df['player'].unique()
    
    # Cross-reference with our players_dict
    active_players = {}
    found_count = 0
    
    for player_id in unique_player_ids:
        if player_id in players_dict:
            active_players[player_id] = players_dict[player_id]
            found_count += 1
    
    print(f"Found {found_count} players from rankings with our ELO database")
    
    return active_players



def get_top_players_by_surface(players_dict, surface='Hard', top_n=20):
    """Get top n players by rating on specific surface"""
    surface_ratings = []
    
    for player_id, player_data in players_dict.items():
        if player_data['total_matches'] >= 20:
            surface_ratings.append({
                'player_id': player_id,
                'name': player_data['name'],
                'rating': player_data['ratings'][surface],
                'last_match': player_data['last_match_date'],
                'total_matches': player_data['total_matches']
            })
    
    # Sort by rating descending
    surface_ratings.sort(key=lambda x: x['rating'], reverse=True)
    
    return surface_ratings[:top_n]





