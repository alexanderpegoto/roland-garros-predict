import math
import numpy
from data_utils import parse_score


def calculate_expected_score(rating_a, rating_b):
    """Calculate expected score for player A vs player B"""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))


def tournament_weight(tourney_level):
    """Calculate tournament weight multiplier based on tournament level"""
    if tourney_level == 'G':
        multiplier = 1.5
    elif tourney_level == 'A' or tourney_level == 'D':
        multiplier = 1
    elif tourney_level == 'M':
        multiplier = 1.25
    else:
        multiplier = 1.0
    return multiplier

def mov_multiplier(score):
    """Calculate margin of victory multiplier from game counts"""
    winner_games, loser_games = parse_score(score)
    
    if winner_games is None:
        return 1.0  # Default for missing scores
    
    total_games = winner_games + loser_games
    if total_games == 0:
        return 1.0
    
    games_ratio = winner_games / total_games
    
    if games_ratio >= 0.75:  # Very dominant (6-1 6-2 = 12-3)
        return 1.2
    elif games_ratio >= 0.65:  # Solid win (6-4 6-3 = 12-7)
        return 1.1
    elif games_ratio >= 0.55:  # Close win (7-5 6-4 = 13-9)
        return 1.0
    else:  # Very close (7-6 7-6 = 14-12)
        return 0.9
    
def calculate_k_factor(tourney_level, winner_games, loser_games, base_k=32):
    """Calculate adjusted K-factor with all multipliers"""
    t_weight = tournament_weight(tourney_level)
    mov_mult = mov_multiplier(winner_games, loser_games)
    
    # Apply logarithmic dampening to MOV
    mov_dampened = 1 + math.log(1 + abs(mov_mult - 1)) * (1 if mov_mult >= 1 else -1)
    
    return base_k * t_weight * mov_dampened


def update_elo_ratings(winner_rating, loser_rating, k_factor):
    """Update ELO ratings after a match"""
    expected_winner = calculate_expected_score(winner_rating, loser_rating)
    
    new_winner_rating = winner_rating + k_factor * (1 - expected_winner)
    new_loser_rating = loser_rating + k_factor * (0 - (1 - expected_winner))
    
    return new_winner_rating, new_loser_rating