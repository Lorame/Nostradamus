import pandas as pd

from scripts.draw_rules import (
    build_draw_pots,
    assign_titleholder_seed,
    can_play_against,
    respects_association_limit,
    validate_pot_distribution,
    validate_home_away_distribution,
    validate_eight_opponents,
    validate_home_away_balance,
    validate_no_duplicate_opponents,
    validate_matchday_home_away_sequence,
)


def make_team(club_id, country_code):
    return pd.Series(
        {
            "club_id": club_id,
            "country_code": country_code,
        }
    )


def make_opponent(club_id, country_code, pot, venue):
    return {
        "club_id": club_id,
        "country_code": country_code,
        "pot": pot,
        "venue": venue,
    }


def test_build_draw_pots():
    clubs = pd.DataFrame(
        {
            "club_id": range(1, 37),
            "rank": range(1, 37),
        }
    )

    pots = build_draw_pots(clubs)

    assert len(pots) == 4
    assert all(len(pot) == 9 for pot in pots.values())

    assert pots["pot_1"].iloc[0]["rank"] == 1
    assert pots["pot_4"].iloc[-1]["rank"] == 36


def test_titleholder_is_top_seed():
    clubs = pd.DataFrame(
        {
            "club_id": [1, 2, 3],
            "rank": [1, 2, 3],
        }
    )

    pots = {
        "pot_1": clubs.copy(),
        "pot_2": pd.DataFrame(),
        "pot_3": pd.DataFrame(),
        "pot_4": pd.DataFrame(),
    }

    pots = assign_titleholder_seed(pots, 3)

    assert pots["pot_1"].iloc[0]["club_id"] == 3


def test_same_association_is_not_allowed():
    team_a = make_team(1, "FRA")
    team_b = make_team(2, "FRA")

    assert can_play_against(team_a, team_b) is False


def test_different_association_is_allowed():
    team_a = make_team(1, "FRA")
    team_b = make_team(2, "ENG")

    assert can_play_against(team_a, team_b) is True


def test_association_limit():
    team = make_team(1, "FRA")

    opponents = pd.DataFrame(
        [
            {"club_id": 2, "country_code": "ENG"},
            {"club_id": 3, "country_code": "ENG"},
        ]
    )

    assert respects_association_limit(team, opponents) is True

    opponents.loc[len(opponents)] = [4, "ENG"]

    assert respects_association_limit(team, opponents) is False


def test_two_opponents_per_pot():
    opponents_by_pot = {
        "pot_1": [1, 2],
        "pot_2": [3, 4],
        "pot_3": [5, 6],
        "pot_4": [7, 8],
    }

    assert validate_pot_distribution(opponents_by_pot) is True


def test_invalid_pot_distribution():
    opponents_by_pot = {
        "pot_1": [1],
        "pot_2": [3, 4],
        "pot_3": [5, 6],
        "pot_4": [7, 8],
    }

    assert validate_pot_distribution(opponents_by_pot) is False


def test_one_home_one_away_per_pot():
    opponents_by_pot = {
        "pot_1": [
            {"venue": "home"},
            {"venue": "away"},
        ],
        "pot_2": [
            {"venue": "home"},
            {"venue": "away"},
        ],
        "pot_3": [
            {"venue": "home"},
            {"venue": "away"},
        ],
        "pot_4": [
            {"venue": "home"},
            {"venue": "away"},
        ],
    }

    assert validate_home_away_distribution(opponents_by_pot) is True


def test_invalid_home_away_distribution():
    opponents_by_pot = {
        "pot_1": [
            {"venue": "home"},
            {"venue": "home"},
        ],
        "pot_2": [
            {"venue": "home"},
            {"venue": "away"},
        ],
        "pot_3": [
            {"venue": "home"},
            {"venue": "away"},
        ],
        "pot_4": [
            {"venue": "home"},
            {"venue": "away"},
        ],
    }

    assert validate_home_away_distribution(opponents_by_pot) is False


def test_eight_unique_opponents():
    opponents = [
        make_opponent(i, "ENG", "pot_1", "home")
        for i in range(1, 9)
    ]

    assert validate_eight_opponents(opponents) is True


def test_not_eight_opponents():
    opponents = [
        make_opponent(i, "ENG", "pot_1", "home")
        for i in range(1, 8)
    ]

    assert validate_eight_opponents(opponents) is False


def test_home_away_balance():
    opponents = [
        make_opponent(1, "ENG", "pot_1", "home"),
        make_opponent(2, "ESP", "pot_1", "away"),
        make_opponent(3, "GER", "pot_2", "home"),
        make_opponent(4, "ITA", "pot_2", "away"),
        make_opponent(5, "POR", "pot_3", "home"),
        make_opponent(6, "NED", "pot_3", "away"),
        make_opponent(7, "BEL", "pot_4", "home"),
        make_opponent(8, "FRA", "pot_4", "away"),
    ]

    assert validate_home_away_balance(opponents) is True


def test_invalid_home_away_balance():
    opponents = [
        make_opponent(1, "ENG", "pot_1", "home"),
        make_opponent(2, "ESP", "pot_1", "home"),
        make_opponent(3, "GER", "pot_2", "home"),
        make_opponent(4, "ITA", "pot_2", "home"),
        make_opponent(5, "POR", "pot_3", "home"),
        make_opponent(6, "NED", "pot_3", "away"),
        make_opponent(7, "BEL", "pot_4", "away"),
        make_opponent(8, "FRA", "pot_4", "away"),
    ]

    assert validate_home_away_balance(opponents) is False


def test_no_duplicate_opponents():
    opponents = [
        make_opponent(i, "ENG", "pot_1", "home")
        for i in range(1, 9)
    ]

    assert validate_no_duplicate_opponents(opponents) is True


def test_duplicate_opponent():
    opponents = [
        make_opponent(i, "ENG", "pot_1", "home")
        for i in range(1, 8)
    ]

    opponents.append(
        make_opponent(1, "ENG", "pot_4", "away")
    )

    assert validate_no_duplicate_opponents(opponents) is False


def test_valid_matchday_sequence():
    matches = [
        {"venue": "home"},
        {"venue": "away"},
        {"venue": "home"},
        {"venue": "home"},
        {"venue": "away"},
        {"venue": "away"},
        {"venue": "home"},
        {"venue": "away"},
    ]

    assert validate_matchday_home_away_sequence(matches) is True


def test_invalid_matchday_sequence():
    matches = [
        {"venue": "home"},
        {"venue": "home"},
        {"venue": "home"},
        {"venue": "away"},
        {"venue": "away"},
        {"venue": "home"},
        {"venue": "away"},
        {"venue": "home"},
    ]

    assert validate_matchday_home_away_sequence(matches) is False