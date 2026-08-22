from pathlib import Path

import pandas as pd
import requests


QUERY = """
SELECT ?team ?teamLabel ?uefaId WHERE {
    ?team wdt:P31 wd:Q476028 .
    ?team wdt:P7361 ?uefaId .

    SERVICE wikibase:label {
        bd:serviceParam wikibase:language "fr,en" .
    }
}
"""

ENDPOINT = "https://query.wikidata.org/sparql"
OUTPUT_FILE = Path("data/raw/wikidata_uefa_clubs.csv")


def fetch_data():
    response = requests.get(
        ENDPOINT,
        params={"query": QUERY, "format": "json"},
        headers={"User-Agent": "Nostradamus/1.0"},
        timeout=60,
    )
    response.raise_for_status()

    return response.json()


def build_dataframe(data):
    rows = []

    for result in data["results"]["bindings"]:
        rows.append(
            {
                "wikidata_id": result["team"]["value"].split("/")[-1],
                "team": result["teamLabel"]["value"],
                "uefa_id": result["uefaId"]["value"],
            }
        )

    return pd.DataFrame(rows)


def main():
    data = fetch_data()
    df = build_dataframe(data)

    df = df.drop_duplicates(subset="uefa_id")
    df = df.sort_values("team").reset_index(drop=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Clubs récupérés : {len(df)}")
    print(f"Fichier créé : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()