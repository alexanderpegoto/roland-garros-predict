import os
from datetime import datetime
import glob
import pandas as pd
from config import *


# Import our modules
from src.elo_system import update_elo_ratings, calculate_k_factor
from src.data_utils import parse_score, parse_tournament_date, clean_player_name
from src.player_utils import (
    initialize_player, add_or_update_player, get_player_rating, 
    update_player_rating, apply_rating_decay
)
from src.rankings import (
    get_active_players_from_rankings, get_top_players_by_surface, 
    format_rankings_display, get_surface_specialists
)
from config import *

def process_historical_matches():
    # Init players dict
    players_dict = {}
    
    #Create a list with data folders
    csv_files = glob.glob(os.path.join("data", "atp_matches_*.csv"))
    
    total_matches_processed = 0
    
    for file in csv_files:
        df = pd.read_csv(file)
        
        # Process each match
        for index, match in df.iterrows():
            winner_id = match['winner_id']
            loser_id = match['loser_id']
            winner_name = match['winner_name']
            loser_name = match['loser_name']
            surface = match['surface']
        
        # Parse tournament date
            match_date = parse_tournament_date(match['tourney_date'])
            if match_date is None:
                continue
        
        
        if surface not in VALID_SURFACES:
                continue