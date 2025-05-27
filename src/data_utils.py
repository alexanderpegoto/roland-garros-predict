import pandas as pd


def parse_score(score):
    """Parse tennis score to extract total games won by winner and loser"""
    if pd.isna(score) or score == '':
        return None, None
    
    sets = score.split()
    winner_games = 0
    loser_games = 0
    
    for set_score in sets:
        if '-' in set_score:
            games = set_score.split('-')
            if len(games) == 2:
                try:
                    w_games = int(games[0])
                    l_games = int(games[1].split('(')[0])  # Remove tiebreak score
                    winner_games += w_games
                    loser_games += l_games
                except ValueError:
                    continue
    
    return winner_games, loser_games


def parse_tournament_date(date_value):
    """Convert tournament date to datetime object"""
    try:
        date_str = str(int(date_value))
        return pd.to_datetime(date_str, format='%Y%m%d')
    except Exception:
        return None
    
    