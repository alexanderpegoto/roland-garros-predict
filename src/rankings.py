import pandas as pd
from datetime import datetime

def get_active_players_from_rankings(players_dict, rankings_file):
    """Get active players from ATP rankings file"""
    rankings_df = pd.read_csv(rankings_file)
    unique_player_ids = rankings_df['player'].unique()
    
    active_players = {}
    found_count = 0
    
    print(f"Total unique player IDs in rankings: {len(unique_player_ids)}")
    print(f"Total players in players_dict: {len(players_dict)}")
    
    # Check if Zverev ID exists in both
    zverev_id = 100644
    print(f"Zverev ID {zverev_id} in rankings: {zverev_id in unique_player_ids}")
    print(f"Zverev ID {zverev_id} in players_dict: {zverev_id in players_dict}")
    
    for player_id in unique_player_ids:
        if player_id in players_dict:
            active_players[player_id] = players_dict[player_id]
            found_count += 1
            if player_id == zverev_id:
                print(f"SUCCESS: Added Zverev to active_players!")
    
    print(f"Found {found_count} players from rankings with our ELO database")
    return active_players



def get_top_players_by_surface(players_dict, surface='Hard', top_n=20):
    """Get top n players by rating on specific surface"""
    surface_ratings = []
    
    for player_id, player_data in players_dict.items():
        # Debug for Zverev specifically
        if player_id == '100644':
            print(f"DEBUG Zverev: total_matches={player_data['total_matches']}, {surface}_rating={player_data['ratings'][surface]}")
        
        if player_data['total_matches'] >= 20:
            surface_ratings.append({
                'player_id': player_id,
                'name': player_data['name'],
                'rating': player_data['ratings'][surface],
                'last_match': player_data['last_match_date'],
                'total_matches': player_data['total_matches']
            })
    
    # Debug: Check if Zverev made it into the list
    zverev_in_list = any(p['player_id'] == '100644' for p in surface_ratings)
    print(f"Zverev in {surface} ratings list: {zverev_in_list}")
    
    # Sort by rating descending
    surface_ratings.sort(key=lambda x: x['rating'], reverse=True)
    
    # Debug: Show top few ratings
    print(f"Top 3 {surface} ratings:")
    for i, p in enumerate(surface_ratings[:3]):
        print(f"  {i+1}. {p['name']}: {p['rating']}")
    
    return surface_ratings[:top_n]




