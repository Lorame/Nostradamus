import pandas as pd

from scripts.draw_engine import (
    prepare_pots,
    get_candidates,
    choose_venue,
    validate_team_draw,
)


def make_clubs():
    return pd.DataFrame(
        {
            "club_id": range(1, 37),
            "draw_coefficient": range(36, 0, -1),
            "rank": range(1, 37),
            "country_code": [
                "FRA",
                "ENG",
                "ESP",
                "GER",
                "ITA",
                "POR",
                "NED",
                "BEL",
                "SCO",
                "FRA",
                "ENG",
                "ESP",
                "GER",
                "ITA",
                "POR",
                "NED",
                "BEL",
                "SCO",
                "FRA",
                "ENG",
                "ESP",
                "GER",
                "ITA",
                "POR",
                "NED",
                "BEL",
                "SCO",
                "FRA",
                "ENG",
                "ESP",
                "GER",
                "ITA",
                "POR",
                "NED",
                "BEL",
                "SCO",
            ],
        }
    )


def test_prepare_pots():
    clubs = make_clubs()

    pots = prepare_pots(
        clubs,
        titleholder_id=1,
    )

    assert len(pots) == 4

    assert all(
        len(pot) == 9
        for pot in pots.values()
    )

    assert pots["pot_1"].iloc[0]["club_id"] == 1


def test_titleholder_is_in_pot_one():
    clubs = make_clubs()

    pots = prepare_pots(
        clubs,
        titleholder_id=1,
    )

    pot_one_ids = set(
        pots["pot_1"]["club_id"]
    )

    assert 1 in pot_one_ids


def test_all_clubs_are_in_exactly_one_pot():
    clubs = make_clubs()

    pots = prepare_pots(
        clubs,
        titleholder_id=1,
    )

    all_ids = []

    for pot in pots.values():
        all_ids.extend(
            pot["club_id"].tolist()
        )

    assert len(all_ids) == 36
    assert len(set(all_ids)) == 36


def test_same_association_is_not_candidate():
    clubs = make_clubs()

    pots = prepare_pots(
        clubs,
        titleholder_id=1,
    )

    team = clubs.iloc[0]

    opponents = []

    candidates = get_candidates(
        team,
        pots["pot_2"],
        opponents,
    )

    candidate_countries = set(
        candidates["country_code"]
    )

    assert "FRA" not in candidate_countries


def test_existing_opponent_is_removed():
    clubs = make_clubs()

    pots = prepare_pots(
        clubs,
        titleholder_id=1,
    )

    team = clubs.iloc[0]

    existing_opponents = [
        {
            "club_id": 11,
            "country_code": "ENG",
            "pot": "pot_2",
            "venue": "home",
        }
    ]

    candidates = get_candidates(
        team,
        pots["pot_2"],
        existing_opponents,
    )

    assert 11 not in set(
        candidates["club_id"]
    )


def test_choose_venue_keeps_four_four_balance():
    existing = [
        {
            "club_id": i,
            "country_code": "ENG",
            "pot": "pot_1",
            "venue": "home",
        }
        for i in range(1, 5)
    ]

    from random import Random

    venue = choose_venue(
        Random(42),
        existing,
    )

    assert venue == "away"


def test_valid_team_draw():
    opponents = [
        {
            "club_id": 2,
            "country_code": "ENG",
            "pot": "pot_1",
            "venue": "home",
        },
        {
            "club_id": 3,
            "country_code": "ESP",
            "pot": "pot_1",
            "venue": "away",
        },
        {
            "club_id": 4,
            "country_code": "GER",
            "pot": "pot_2",
            "venue": "home",
        },
        {
            "club_id": 5,
            "country_code": "ITA",
            "pot": "pot_2",
            "venue": "away",
        },
        {
            "club_id": 6,
            "country_code": "POR",
            "pot": "pot_3",
            "venue": "home",
        },
        {
            "club_id": 7,
            "country_code": "NED",
            "pot": "pot_3",
            "venue": "away",
        },
        {
            "club_id": 8,
            "country_code": "BEL",
            "pot": "pot_4",
            "venue": "home",
        },
        {
            "club_id": 9,
            "country_code": "SCO",
            "pot": "pot_4",
            "venue": "away",
        },
    ]

    assert validate_team_draw(opponents) is True
