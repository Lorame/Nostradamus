
from pathlib import Path
import pandas as pd
import re


UCL_PATH = Path("data/raw/ucl_2026_2027_teams.csv")
UEFA_PATH = Path("data/raw/uefa_club_coefficients_full.csv")
OUTPUT_PATH = Path("data/processed/ucl_2026_2027_clubs_full.csv")


def extract_club_id(url):
    """
    Extract UEFA club ID from UEFA URL.
    Example:
    /uefachampionsleague/clubs/52280--arsenal/
    returns 52280
    """

    if pd.isna(url):
        return None

    match = re.search(r"/clubs/(\d+)", url)

    return int(match.group(1)) if match else None


ucl = pd.read_csv(UCL_PATH)
uefa = pd.read_csv(UEFA_PATH)

print(f"UCL clubs : {len(ucl)}")
print(f"UEFA coefficients : {len(uefa)}")


ucl["club_id"] = ucl["uefa_url"].apply(extract_club_id)

print("\nClub IDs extracted:")
print(ucl[["team", "club_id"]].head())


df = ucl.merge(
    uefa,
    on="club_id",
    how="left",
    suffixes=("_ucl", "_uefa")
)

print(f"\nFinal clubs : {len(df)}")


missing = df[df["points"].isna()]

if not missing.empty:
    print("\nClubs without UEFA coefficients:")
    print(missing[["team", "club_id"]])


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