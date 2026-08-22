import re

import pandas as pd


UEFA_FILE = "data/raw/ucl_2026_2027_teams.csv"
KASSIESA_FILE = "data/raw/kassiesa_club_ranking_2026.csv"


def extract_uefa_id(url):
    match = re.search(r"/clubs/(\d+)", url)
    return match.group(1) if match else None


def normalize_country(country):
    return country.strip().lower()


uefa = pd.read_csv(UEFA_FILE)
kassiesa = pd.read_csv(KASSIESA_FILE)

uefa["uefa_id"] = uefa["uefa_url"].apply(extract_uefa_id)
uefa["country_normalized"] = uefa["country"].apply(normalize_country)
kassiesa["country_normalized"] = kassiesa["country"].apply(normalize_country)

merged = uefa.merge(
    kassiesa,
    left_on=["team", "country_normalized"],
    right_on=["team", "country_normalized"],
    how="left",
    suffixes=("_uefa", "_kassiesa"),
)

matches = merged[merged["coefficient"].notna()]
unmatched = merged[merged["coefficient"].isna()]

print(f"Équipes UEFA : {len(uefa)}")
print(f"Correspondances exactes : {len(matches)}")
print(f"Équipes non trouvées : {len(unmatched)}")

print("\nCorrespondances :")

for _, row in matches.iterrows():
    print(
        f"- {row['team']} | "
        f"{row['country_uefa']} | "
        f"UEFA ID : {row['uefa_id']} | "
        f"Coefficient : {row['coefficient']}"
    )

print("\nÉquipes non trouvées :")

for _, row in unmatched.iterrows():
    print(
        f"- {row['team']} | "
        f"{row['country_uefa']} | "
        f"UEFA ID : {row['uefa_id']}"
    )