from __future__ import annotations

import random

import pandas as pd

from scripts.draw_rules import (
    can_play_against,
    respects_association_limit,
    validate_eight_opponents,
    validate_home_away_balance,
    validate_home_away_distribution,
    validate_no_duplicate_opponents,
    validate_pot_distribution,
)


def prepare_pots(
    clubs: pd.DataFrame,
    titleholder_id: int,
) -> dict[str, pd.DataFrame]:
    """Prepare the four draw pots from the UEFA club ranking."""

    required_columns = {
        "club_id",
        "rank",
        "country_code",
    }

    missing = required_columns - set(clubs.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    clubs = clubs.copy()

    clubs = clubs.sort_values("rank").reset_index(drop=True)

    titleholder = clubs.loc[
        clubs["club_id"] == titleholder_id
    ]

    if titleholder.empty:
        raise ValueError(
            f"Titleholder {titleholder_id} not found."
        )

    titleholder = titleholder.iloc[0]

    remaining = clubs[
        clubs["club_id"] != titleholder_id
    ].copy()

    remaining = remaining.sort_values("rank")

    pot_1 = pd.concat(
        [
            pd.DataFrame([titleholder]),
            remaining.iloc[:8],
        ],
        ignore_index=True,
    )

    remaining = remaining.iloc[8:]

    pots = {
        "pot_1": pot_1.reset_index(drop=True),
        "pot_2": remaining.iloc[:9].reset_index(drop=True),
        "pot_3": remaining.iloc[9:18].reset_index(drop=True),
        "pot_4": remaining.iloc[18:27].reset_index(drop=True),
    }

    validate_pot_sizes(pots)

    return pots


def validate_pot_sizes(
    pots: dict[str, pd.DataFrame],
) -> None:
    """Validate the four UEFA pots."""

    if set(pots) != {
        "pot_1",
        "pot_2",
        "pot_3",
        "pot_4",
    }:
        raise ValueError("Exactly four pots are required.")

    for pot_name, pot in pots.items():
        if len(pot) != 9:
            raise ValueError(
                f"{pot_name} contains {len(pot)} clubs instead of 9."
            )


def get_candidates(
    team: pd.Series,
    pot: pd.DataFrame,
    existing_opponents: list[dict],
) -> pd.DataFrame:
    """Return clubs that can legally face the selected team."""

    candidates = []

    existing_ids = {
        opponent["club_id"]
        for opponent in existing_opponents
    }

    for _, opponent in pot.iterrows():

        if opponent["club_id"] == team["club_id"]:
            continue

        if opponent["club_id"] in existing_ids:
            continue

        if not can_play_against(team, opponent):
            continue

        current_opponents = pd.DataFrame(existing_opponents)

        if not current_opponents.empty:
            if not respects_association_limit(
                team,
                current_opponents,
            ):
                continue

        candidates.append(opponent)

    if not candidates:
        return pd.DataFrame(columns=pot.columns)

    return pd.DataFrame(candidates)


def choose_venue(
    rng: random.Random,
    existing_opponents: list[dict],
) -> str:
    """Choose home or away while targeting a 4/4 balance."""

    home_count = sum(
        opponent["venue"] == "home"
        for opponent in existing_opponents
    )

    away_count = sum(
        opponent["venue"] == "away"
        for opponent in existing_opponents
    )

    if home_count >= 4:
        return "away"

    if away_count >= 4:
        return "home"

    return rng.choice(["home", "away"])


def add_opponent(
    draw: dict[int, list[dict]],
    team: pd.Series,
    opponent: pd.Series,
    pot_name: str,
    venue: str,
) -> None:
    """Add an opponent to the draw."""

    team_id = int(team["club_id"])

    draw.setdefault(team_id, [])

    draw[team_id].append(
        {
            "club_id": int(opponent["club_id"]),
            "country_code": opponent["country_code"],
            "pot": pot_name,
            "venue": venue,
        }
    )


def generate_team_draw(
    team: pd.Series,
    pots: dict[str, pd.DataFrame],
    rng: random.Random,
) -> list[dict]:
    """Generate eight opponents for one team."""
    opponents = []

    for pot_name, pot in pots.items():
        candidates = get_candidates(
            team,
            pot,
            opponents,
        )

        if len(candidates) < 2:
            raise RuntimeError(
                f"Not enough valid opponents found for "
                f"{team['club_id']} in {pot_name}."
            )

        candidate_indices = list(candidates.index)
        rng.shuffle(candidate_indices)

        selected_indices = candidate_indices[:2]

        venues = ["home", "away"]
        rng.shuffle(venues)

        for index, venue in zip(selected_indices, venues):
            selected = candidates.loc[index]

            opponents.append(
                {
                    "club_id": int(selected["club_id"]),
                    "country_code": selected["country_code"],
                    "pot": pot_name,
                    "venue": venue,
                }
            )

    return opponents


def validate_team_draw(
    opponents: list[dict],
) -> bool:
    """Validate a complete eight-opponent draw."""

    return all(
        [
            validate_eight_opponents(opponents),
            validate_home_away_balance(opponents),
            validate_no_duplicate_opponents(opponents),
            validate_pot_distribution(
                {
                    pot_name: [
                        opponent
                        for opponent in opponents
                        if opponent["pot"] == pot_name
                    ]
                    for pot_name in [
                        "pot_1",
                        "pot_2",
                        "pot_3",
                        "pot_4",
                    ]
                }
            ),
            validate_home_away_distribution(
                {
                    pot_name: [
                        opponent
                        for opponent in opponents
                        if opponent["pot"] == pot_name
                    ]
                    for pot_name in [
                        "pot_1",
                        "pot_2",
                        "pot_3",
                        "pot_4",
                    ]
                }
            ),
        ]
    )


def generate_draw(
    clubs: pd.DataFrame,
    titleholder_id: int,
    random_state: int = 42,
) -> dict[int, list[dict]]:
    """
    Generate a deterministic candidate draw.

    The same dataset and random_state produce
    the same result.
    """

    rng = random.Random(random_state)

    pots = prepare_pots(
        clubs,
        titleholder_id,
    )

    draw: dict[int, list[dict]] = {}

    teams = pd.concat(
        pots.values(),
        ignore_index=True,
    )

    teams = teams.sort_values(
        "rank"
    ).reset_index(drop=True)

    for _, team in teams.iterrows():

        team_id = int(team["club_id"])

        if team_id in draw:
            continue

        opponents = generate_team_draw(
            team,
            pots,
            rng,
        )

        if not validate_team_draw(opponents):
            raise RuntimeError(
                f"Generated draw is invalid for club {team_id}."
            )

        draw[team_id] = opponents

    return draw