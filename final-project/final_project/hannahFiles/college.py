from sportsreference.nfl.roster import Player
import matplotlib.pyplot as plt

# players to look at from Wisconsin
jonathon_taylor = "TaylJo02"
james_white = "WhitJa02"
melvin_gordon = "GordMe00"
dare_ogum = "OgunDa00"
corey_clement = "ClemCo00"

jt = Player(jonathon_taylor)
jw = Player(james_white)
mg = Player(melvin_gordon)
do = Player(dare_ogum)
cc = Player(corey_clement)
wisc = [jt, jw, mg, do, cc]
    
def get_yards_per_touch(players):
    """Fetches career yards per touch

    Args:
        players (array): players to retrieve career yards per touch for

    Returns:
        array: array of yards per touch for inputted players
    """
    return [player.yards_per_touch for player in players]

def get_times_pass_target(players):
    """Fetches number of times a player was a pass target in their career

    Args:
        players (array): players to retrieve career times pass target

    Returns:
        array: number of times targeted for a pass for each player
    """
    return [player.times_pass_target for player in players]

def get_rush_yards_per_attempt(players):
    """Fetches the career rush yards per attempt

    Args:
        players (array): players to retrieve rush yards per attempt for

    Returns:
        array: rush yards per attempt for each player
    """
    return [player.rush_yards_per_attempt for player in players]

def get_rush_yards(players):
    """Fetches career rush yards

    Args:
        players (array): players to retrieve rush yards for

    Returns:
        array: rush yards for each player
    """
    return [player.rush_yards for player in players]

def get_rush_td(players):
    """Fetches career rushing touchdowns

    Args:
        players (array): players to retrieve rushing td for

    Returns:
        array: rushing td for each player
    """
    return [player.rush_touchdowns for player in players]

def get_rush_attempts_per_game(players):
    """Fetches career rush attempts per game

    Args:
        players (array): players to retrieve rush attempts per game for

    Returns:
        array: rush attempts per game for each player
    """
    return [player.rush_attempts_per_game for player in players]


def get_rush_attempts(players):
    """Fetches career rush attempts

    Args:
        players (array): players to retrieve rush attempts for

    Returns:
        array: rush attempts for each player
    """
    return [player.rush_attempts for player in players]