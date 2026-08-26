import json
from pathlib import Path

import pandas as pd

from scripts.draw_engine import generate_draw, prepare_pots


POOL_PATH = Path("data/processed/ucl_2026_2027_qualification_pool.csv")
SCENARIOS_PATH = Path(
    "data/processed/ucl_2026_2027_playoff_scenarios.json"
)


def load_qualification_pool(path):
    """Load the UCL qualification pool."""
    return pd.read_csv(path)


def load_playoff_scenarios(path):
    """Load the predefined playoff qualification scenarios."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_scenario_dataset(pool, scenario):
    """Build the 36-club dataset for one playoff qualification scenario."""

    league_phase = pool[
        pool["qualification_status"] == "league_phase"
    ].copy()

    qualified_ids = scenario["qualified_clubs"]

    playoff_qualified = pool[
        pool["club_id"].isin(qualified_ids)
    ].copy()

    scenario_df = pd.concat(
        [league_phase, playoff_qualified],
        ignore_index=True,
    )

    return scenario_df


def validate_scenario_dataset(df):
    """Validate that a scenario contains exactly 36 unique clubs."""

    if len(df) != 36:
        raise ValueError(
            f"Expected 36 clubs, found {len(df)}."
        )

    if df["club_id"].nunique() != 36:
        raise ValueError(
            "The scenario contains duplicate club IDs."
        )

    return True


def prepare_scenario_pots(scenario_df):
    """Prepare the four UEFA draw pots for one scenario."""

    titleholder_id = 52747

    return prepare_pots(
        scenario_df,
        titleholder_id,
    )


def run_scenario(scenario_id, pool, scenarios):
    """Build and run one complete UCL league-phase scenario."""
    scenario = scenarios[str(scenario_id)]

    scenario_df = build_scenario_dataset(
        pool,
        scenario,
    )

    validate_scenario_dataset(scenario_df)

    pots = prepare_scenario_pots(scenario_df)

    draw = generate_draw(
        scenario_df,
        titleholder_id=52747,
        random_state=42,
    )

    return scenario_df, pots, draw


if __name__ == "__main__":
    pool = load_qualification_pool(POOL_PATH)
    scenarios = load_playoff_scenarios(SCENARIOS_PATH)

    scenario_df, pots, draw = run_scenario(
        scenario_id=1,
        pool=pool,
        scenarios=scenarios,
    )

    print("Scenario 1")
    print(f"Clubs: {len(scenario_df)}")

    for pot_number, pot in pots.items():
        print(f"Pot {pot_number}: {len(pot)} clubs")
        print(pot[["team", "club_id", "points"]].to_string(index=False))
        print()
    print("Nostradamus draw")
    print()

    for club_id, opponents in draw.items():
        team_name = scenario_df.loc[
        scenario_df["club_id"] == club_id,
        "team",
        ].iloc[0]

        print(f"{team_name} ({club_id})")

        for opponent in opponents:
            opponent_name = scenario_df.loc[
            scenario_df["club_id"] == opponent["club_id"],
            "team",
            ].iloc[0]

        print(
            f"  - {opponent_name} "
            f"(pot {opponent['pot']}, {opponent['venue']})"
        )

    print()