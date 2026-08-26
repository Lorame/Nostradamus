import pandas as pd

def build_draw_pots(clubs):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.01
    and Annex D.2.

    The 36 clubs are divided into four pots of nine clubs.
    The pots are composed according to the club coefficient
    rankings established at the beginning of the season.

    Parameters
    
    clubs : pandas.DataFrame
        UCL clubs with their official UEFA coefficient ranking.

    Returns
    
    dict
        Four draw pots containing nine clubs each.
    """
    sorted_clubs = clubs.sort_values("rank").reset_index(drop=True)

    return {
        "pot_1": sorted_clubs.iloc[0:9],
        "pot_2": sorted_clubs.iloc[9:18],
        "pot_3": sorted_clubs.iloc[18:27],
        "pot_4": sorted_clubs.iloc[27:36],
    }
    
def assign_titleholder_seed(pots, titleholder_id):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.01.

    The UEFA Champions League titleholder is the top seed
    in Pot 1.

    Parameters
    ----------
    pots : dict
        Draw pots returned by build_draw_pots().
    titleholder_id : int
        UEFA club identifier of the Champions League titleholder.

    Returns
    -------
    dict
        Updated draw pots with the titleholder placed first in Pot 1.
    """
    pot_1 = pots["pot_1"].copy()

    titleholder = pot_1[pot_1["club_id"] == titleholder_id]

    if titleholder.empty:
        raise ValueError("The titleholder is not present in Pot 1.")

    remaining = pot_1[pot_1["club_id"] != titleholder_id]

    pots["pot_1"] = (
        pd.concat([titleholder, remaining])
        .reset_index(drop=True)
    )

    return pots

def can_play_against(team_a, team_b):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.02.

    In principle, clubs from the same association cannot be
    drawn against each other.

    Parameters
    ----------
    team_a : pandas.Series
        First club.
    team_b : pandas.Series
        Second club.

    Returns
    -------
    bool
        True if the two clubs can be drawn against each other
        based on the association constraint, otherwise False.
    """
    return team_a["country_code"] != team_b["country_code"]

def respects_association_limit(team, opponents, max_opponents=2):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.02.

    Each team may play against a maximum of two opponents
    from any other one association.

    Parameters
    ----------
    team : pandas.Series
        The club for which the opponents are being checked.
    opponents : pandas.DataFrame
        Clubs already selected as opponents.
    max_opponents : int, default=2
        Maximum number of opponents allowed from the same association.

    Returns
    -------
    bool
        True if the association limit is respected, otherwise False.
    """
    opponent_counts = opponents["country_code"].value_counts()

    for country_code, count in opponent_counts.items():
        if country_code == team["country_code"]:
            continue

        if count > max_opponents:
            return False

    return True


def validate_pot_distribution(opponents_by_pot):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.02.

    Each team is drawn against two opponents from each of the
    four pots.

    Parameters
    ----------
    opponents_by_pot : dict
        Dictionary mapping pot names to the list of opponents
        assigned to a team.

    Returns
    -------
    bool
        True if the team has exactly two opponents from each pot,
        otherwise False.
    """
    expected_pots = {"pot_1", "pot_2", "pot_3", "pot_4"}

    if set(opponents_by_pot.keys()) != expected_pots:
        return False

    return all(
        len(opponents_by_pot[pot]) == 2
        for pot in expected_pots
    )


def validate_home_away_distribution(opponents_by_pot):
    """
    UEFA Champions League Regulations 2026/27 — Article 16.02.

    Each team plays one opponent from each pot at home and
    one opponent from each pot away.

    Parameters
    ----------
    opponents_by_pot : dict
        Dictionary mapping pot names to opponents and their
        home/away status.

    Returns
    -------
    bool
        True if every pot contains exactly one home and one
        away opponent, otherwise False.
    """
    expected_pots = {"pot_1", "pot_2", "pot_3", "pot_4"}

    if set(opponents_by_pot.keys()) != expected_pots:
        return False

    for pot in expected_pots:
        matches = opponents_by_pot[pot]

        if len(matches) != 2:
            return False

        home_count = sum(
            match["venue"] == "home"
            for match in matches
        )

        away_count = sum(
            match["venue"] == "away"
            for match in matches
        )

        if home_count != 1 or away_count != 1:
            return False

    return True


def validate_eight_opponents(opponents):
    """
    UEFA Champions League Regulations 2026/27 — Article 17.01.

    Each club plays eight opponents in single-leg ties.

    Parameters
    ----------
    opponents : list
        Opponents assigned to the club.

    Returns
    -------
    bool
        True if exactly eight opponents are assigned and all
        opponents are unique, otherwise False.
    """
    if len(opponents) != 8:
        return False

    opponent_ids = [
        opponent["club_id"]
        for opponent in opponents
    ]

    return len(set(opponent_ids)) == 8


def validate_home_away_balance(opponents):
    """
    UEFA Champions League Regulations 2026/27 — Article 17.01.

    Each club plays four home and four away matches.

    Parameters
    ----------
    opponents : list
        Opponents assigned to the club.

    Returns
    -------
    bool
        True if the club has exactly four home and four away
        matches, otherwise False.
    """
    if len(opponents) != 8:
        return False

    home_count = sum(
        opponent["venue"] == "home"
        for opponent in opponents
    )

    away_count = sum(
        opponent["venue"] == "away"
        for opponent in opponents
    )

    return home_count == 4 and away_count == 4


def validate_no_duplicate_opponents(opponents):
    """
    UEFA Champions League Regulations 2026/27 — Article 17.01.

    Each club plays eight opponents in single-leg ties.
    The same opponent cannot be assigned more than once.

    Parameters
    ----------
    opponents : list
        Opponents assigned to the club.

    Returns
    -------
    bool
        True if every opponent is unique, otherwise False.
    """
    opponent_ids = [
        opponent["club_id"]
        for opponent in opponents
    ]

    return len(opponent_ids) == len(set(opponent_ids))


def validate_matchday_home_away_sequence(matches):
    """
    UEFA Champions League Regulations 2026/27 — Article 17.02.

    In principle:
    - a club does not play more than two home matches in a row;
    - a club does not play more than two away matches in a row;
    - each club plays one home and one away match across the
      first two matchdays;
    - each club plays one home and one away match across the
      last two matchdays.

    This function validates these conditions for a proposed
    eight-match schedule.

    Parameters
    ----------
    matches : list
        Matchday assignments ordered from matchday 1 to matchday 8.
        Each match must contain a "venue" field with either
        "home" or "away".

    Returns
    -------
    bool
        True if the schedule respects the Article 17.02
        constraints, otherwise False.
    """
    if len(matches) != 8:
        return False

    venues = [match["venue"] for match in matches]

    if any(venue not in {"home", "away"} for venue in venues):
        return False

    for index in range(len(venues) - 2):
        sequence = venues[index:index + 3]

        if len(set(sequence)) == 1:
            return False

    first_two = venues[:2]
    last_two = venues[-2:]

    if first_two.count("home") != 1 or first_two.count("away") != 1:
        return False

    if last_two.count("home") != 1 or last_two.count("away") != 1:
        return False

    return True


def validate_complete_draw(clubs, draw):
    """
    UEFA Champions League Regulations 2026/27 — Articles 16.02,
    17.01 and 17.02.

    Performs the main structural validation of a complete
    league-phase draw.

    Parameters
    ----------
    clubs : pandas.DataFrame
        UCL clubs participating in the league phase.
    draw : dict
        Complete draw structure indexed by club ID.

    Returns
    -------
    bool
        True if the complete draw satisfies the implemented
        structural constraints, otherwise False.
    """
    if len(clubs) != 36:
        return False

    for club in clubs.to_dict("records"):
        club_id = club["club_id"]

        if club_id not in draw:
            return False

        opponents = draw[club_id]

        if not validate_eight_opponents(opponents):
            return False

        if not validate_home_away_balance(opponents):
            return False

        if not validate_no_duplicate_opponents(opponents):
            return False

        opponents_by_pot = {
            "pot_1": [],
            "pot_2": [],
            "pot_3": [],
            "pot_4": [],
        }

        for opponent in opponents:
            opponents_by_pot[opponent["pot"]].append(opponent)

        if not validate_pot_distribution(opponents_by_pot):
            return False

        if not validate_home_away_distribution(opponents_by_pot):
            return False

        opponent_dataframe = pd.DataFrame(opponents)

        if not can_play_against(
            pd.Series(club),
            opponent_dataframe.iloc[0]
        ):
            return False

        if not respects_association_limit(
            pd.Series(club),
            opponent_dataframe
        ):
            return False

        if not validate_matchday_home_away_sequence(opponents):
            return False

    return True
