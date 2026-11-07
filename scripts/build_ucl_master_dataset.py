from pathlib import Path
import pandas as pd
import re
import numpy as np


UCL_PATH = Path("data/raw/ucl_2026_2027_teams.csv")
UEFA_PATH = Path("data/raw/uefa_club_coefficients_full.csv")
OUTPUT_PATH = Path("data/processed/ucl_2026_2027_qualification_pool.csv")


def extract_club_id(url):
    """
    Extract UEFA club ID from UEFA URL.

    Example:
    /uefachampionsleague/clubs/52280--arsenal/

    returns:
    52280
    """

    if pd.isna(url):
        return None

    match = re.search(r"/clubs/(\d+)", url)

    return int(match.group(1)) if match else None


def define_qualification_status(stage):
    """
    Convert UEFA stage information into a Nostradamus qualification status.
    """

    if stage == "Phase de ligue":
        return "league_phase"

    return "playoff"


ucl = pd.read_csv(UCL_PATH)
uefa = pd.read_csv(UEFA_PATH)

print(f"UCL clubs : {len(ucl)}")
print(f"UEFA coefficients : {len(uefa)}")


ucl["club_id"] = ucl["uefa_url"].apply(extract_club_id)

ucl["qualification_status"] = (
    ucl["stage"]
    .apply(define_qualification_status)
)


print("\nClub IDs extracted:")
print(
    ucl[
        [
            "team",
            "club_id",
            "qualification_status"
        ]
    ].head()
)


ucl = ucl.drop(
    columns=[
        "stage",
        "uefa_url"
    ]
)


df = ucl.merge(
    uefa,
    on="club_id",
    how="left",
    suffixes=("_ucl", "_uefa")
)

# Build national association coefficient mapping
association_coefficients = (
    uefa[["country_code", "national_association_points"]]
    .dropna()
    .drop_duplicates()
)

if association_coefficients["country_code"].duplicated().any():
    raise ValueError(
        "Multiple national association coefficients found for a country."
    )

association_map = association_coefficients.set_index(
    "country_code"
)["national_association_points"]

# Validate association coverage
missing_associations = (
    set(df["country_ucl"].dropna())
    - set(association_map.index)
)

if missing_associations:
    raise ValueError(
        f"Missing national association coefficients: "
        f"{sorted(missing_associations)}"
    )

# Complete missing national association coefficients
df["national_association_points"] = (
    df["national_association_points"].fillna(
        df["country_ucl"].map(association_map)
    )
)

# Calculate the 20% national association floor
df["association_floor"] = (
    np.floor(
        df["national_association_points"] * 0.20 * 1000
    ) / 1000
)

# Calculate the coefficient applicable to the draw
df["draw_coefficient"] = (
    df[["points", "association_floor"]].max(axis=1)
)

print(f"\nFinal clubs : {len(df)}")


missing = df[df["points"].isna()]

if not missing.empty:
    print("\nClubs without UEFA coefficients:")
    print(
        missing[
            [
                "team",
                "club_id"
            ]
        ]
    )


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8"
)


print(f"\nDataset created : {OUTPUT_PATH}")