import math
import numpy
from src.data_utils import parse_score
from src.config import *

def calculate_k_factor(matches_played):
    """Calculate dynamic K-factor based on player experience"""
    return K_BASE / (matches_played + K_OFFSET) ** K_SHAPE

def calculate_expected_score(rating_a, rating_b):
    """Calculate expected score for player A vs player B"""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))


def tournament_weight(tourney_level):
    return TOURNAMENT_WEIGHTS.get(tourney_level,1)

def mov_multiplier(winner_games,loser_games):
    """Calculate margin of victory multiplier from game counts"""
    if winner_games is None:
        return 1.0
    
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
    
def calculate_experience_penalty(total_matches_played, penalty_type="plateau"):
    """
    Apply penalty based on career matches played
    Veteran players need to work harder to maintain ratings
    """
    if total_matches_played < 150:  # Newcomers get no penalty
        return 1.0
    
    excess_matches = total_matches_played - 150
    
    if penalty_type == "exponential":
        # Harsh penalty: 1.0 -> 2.0 over career
        penalty = 1 + (excess_matches / 400) ** 1.3
        return min(2.0, penalty)  # Cap at 2x penalty
    
    elif penalty_type == "logarithmic":
        # Gentle penalty: 1.0 -> 1.4 over career
        penalty = 1 + 0.25 * math.log10(1 + excess_matches / 300)
        return min(1.4, penalty)  # Cap at 1.4x penalty

    elif penalty_type == "plateau":
        # Penalty increases then plateaus around 1.15-1.2x
        penalty = 1 + 0.15 * (1 - math.exp(-excess_matches / 400))
        return min(1.2, penalty)  # Much lower cap
    
    return 1.0

def update_elo_ratings(winner_rating, loser_rating, winner_matches, loser_matches, tourney_level):
    """Update ELO ratings after a match"""
    # Calculate expected scores
    expected_winner = calculate_expected_score(winner_rating, loser_rating)
    expected_loser = 1 - expected_winner
    
    # Calculate dynamic K-factors
    k_winner = calculate_k_factor(winner_matches)
    k_loser = calculate_k_factor(loser_matches)
    
    # Optional: Apply tournament weight (minimal impact)
    t_weight = tournament_weight(tourney_level)
    k_winner = k_winner * t_weight
    k_loser = k_loser * t_weight
    
    winner_penalty = calculate_experience_penalty(winner_matches)
    loser_penalty = calculate_experience_penalty(loser_matches)
    
    # Calculate rating changes with experience penalties
    winner_gain = k_winner * (1 - expected_winner) / winner_penalty  # Veterans gain less
    loser_loss = k_loser * (0 - expected_loser) * loser_penalty     # Veterans lose more
    
    # Calculate new ratings
    new_winner_rating = winner_rating + winner_gain
    new_loser_rating = loser_rating + loser_loss
    
    return new_winner_rating, new_loser_rating
