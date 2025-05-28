import os
from datetime import datetime
import glob
import pandas as pd
from src.config import *
from src.player_utils import *
from src.elo_system import *
import json
from src.elo_system import update_elo_ratings, calculate_k_factor
from src.data_utils import parse_score, parse_tournament_date
from src.rankings import get_active_players_from_rankings, get_top_players_by_surface

def process_match(players_dict, match):
    # Extract match data
    winner_id = match['winner_id']
    loser_id = match['loser_id']
    winner_name = match['winner_name']
    loser_name = match['loser_name']
    surface = match['surface']
    
    # ADD THIS VALIDATION - Check for missing data
    if pd.isna(winner_id) or pd.isna(loser_id):
        return False
    
    if pd.isna(surface) or surface not in VALID_SURFACES:
        return False
        
    # Clean the names
    if pd.isna(winner_name):
        winner_name = "Unknown"
    if pd.isna(loser_name):
        loser_name = "Unknown"


    # Parse date
    match_date = parse_tournament_date(match['tourney_date'])
    if match_date is None:
        return False
    
    # Initialize players if needed
    if winner_id not in players_dict:
        players_dict[winner_id] = initialize_player(winner_id, winner_name)
    if loser_id not in players_dict:
        players_dict[loser_id] = initialize_player(loser_id, loser_name)
    
    # Update names
    players_dict[winner_id]['name'] = winner_name
    players_dict[loser_id]['name'] = loser_name
    
    # Get current data
    winner_rating = players_dict[winner_id]['ratings'][surface]
    loser_rating = players_dict[loser_id]['ratings'][surface]
    winner_matches = players_dict[winner_id]['matches_played'][surface]
    loser_matches = players_dict[loser_id]['matches_played'][surface]
    
    # Calculate new ratings
    new_winner_rating, new_loser_rating = update_elo_ratings(
        winner_rating, loser_rating, 
        winner_matches, loser_matches,
        match['tourney_level']
    )
    
    # Update players
    update_player_after_match(players_dict[winner_id], surface, new_winner_rating, match_date)
    update_player_after_match(players_dict[loser_id], surface, new_loser_rating, match_date)
    
    return True


def save_ratings(players_dict, output_file):
    """Save ratings to JSON file"""
    # Convert datetime objects to strings for JSON serialization
    players_ratings = {}
    for player_id, player_data in players_dict.items():
        # Convert player_id to string for JSON compatibility
        players_ratings[str(player_id)] = {
            'name': player_data['name'],
            'ratings': player_data['ratings'],
            'last_match_date': player_data['last_match_date'].isoformat() if player_data['last_match_date'] else None,
            'total_matches': player_data['total_matches']
        }
    
    with open(output_file, 'w') as f:
        json.dump(players_ratings, f, indent=2)

def main():
    # Process all historical data
    players_dict = {}
    
    # Process files
    csv_files = glob.glob(os.path.join(DATA_FOLDER, HISTORICAL_DATA_PATTERN))
    
    # Apply match counter to apply decay 
    match_counter = 0
    
    for file in csv_files:
        df = pd.read_csv(file)
        # Now safely sort by date
        df = df.sort_values('tourney_date')

        # Process each match
        for index, match in df.iterrows():
            match_counter += 1
            process_success = process_match(players_dict, match)

            if not process_success:
                continue

            if match_counter % DECAY_FREQUENCY == 0:
                current_match_date = parse_tournament_date(match['tourney_date'])
                if current_match_date:
                    apply_rating_decay(players_dict, current_date=current_match_date)
                
            
    # Get and display active players
    active_players = get_active_players_from_rankings(
        players_dict, 
        os.path.join(DATA_FOLDER, RANKINGS_FILE)
    )
    
    if not active_players:
        print("No active players found. Check rankings file.")
        return
    
    for surface in VALID_SURFACES:
        print(f"\nTop 10 {surface} Court Players:")
        print("-" * 40)
        top_players = get_top_players_by_surface(active_players, surface, 10)
        
        for i, player in enumerate(top_players, 1):
            print(f"{i:2d}. {player['name']:<25} {player['rating']:6.0f} "
                f"({player['total_matches']} matches)")
    
    # Save ratings to file
    save_ratings(active_players, "tennis_elo_ratings.json")
    
    print(f"\nFinished!")

if __name__ == "__main__":
    main()

        
        


            