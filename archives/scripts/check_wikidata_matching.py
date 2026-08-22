from pathlib import Path

import pandas as pd


UEFA_FILE = Path("data/raw/ucl_2026_2027_teams.csv")
WIKIDATA_FILE = Path("data/raw/wikidata_uefa_clubs.csv")


def main():
    uefa = pd.read_csv(UEFA_FILE)
    wikidata = pd.read_csv(WIKIDATA_FILE)

    merged = uefa.merge(
        wikidata,
        on="team",
        how="left",
        indicator=True,
    )

    matched = merged[merged["_merge"] == "both"]
    unmatched = merged[merged["_merge"] == "left_only"]

    print(f"Équipes UEFA : {len(uefa)}")
    print(f"Correspondances exactes : {len(matched)}")
    print(f"Équipes non trouvées : {len(unmatched)}")

    print("\nCorrespondances :")

    for _, row in matched.iterrows():
        print(
            f"- {row['team']} | "
            f"{row['country']} | "
            f"UEFA ID : {row['uefa_id']}"
        )

    print("\nÉquipes non trouvées :")

    for _, row in unmatched.iterrows():
        print(
            f"- {row['team']} | "
            f"{row['country']}"
        )


if __name__ == "__main__":
    main()
