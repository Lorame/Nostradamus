# scripts/fetch_kassiesa_uefa_urls.py

import pandas as pd
import time
import os
from ddgs import DDGS


INPUT_FILE = "data/raw/kassiesa_club_ranking_2026.csv"
OUTPUT_FILE = "data/raw/kassiesa_uefa_urls.csv"


def search_uefa_url(team):

    queries = [
        f'UEFA {team}',
        f'{team} UEFA Champions League',
        f'site:uefa.com/uefachampionsleague/clubs {team}'
    ]

    import re

    for query in queries:

        try:
            with DDGS() as ddgs:

                results = ddgs.text(
                    query,
                    max_results=10
                )

                for result in results:

                    url = result.get("href", "")

                    # Nettoyage éventuel Markdown
                    if url.startswith("["):
                        url = url.split("](")[1].replace(")", "")


                    # On cherche un vrai identifiant club UEFA
                    if re.search(
                        r"uefa\.com/.*/clubs/\d+",
                        url
                    ):
                        return url


        except Exception as e:
            print(
                f"Erreur DuckDuckGo pour {team}: {e}"
            )

    return None



def main():

    df = pd.read_csv(INPUT_FILE)

    print(f"Clubs Kassiesa : {len(df)}")


    results = []

    # Reprise si fichier déjà existant
    if os.path.exists(OUTPUT_FILE):

        old = pd.read_csv(OUTPUT_FILE)

        results = old.to_dict("records")

        done = set(old["kassiesa_team"])

        print(
            f"Reprise : {len(done)} clubs déjà traités"
        )

    else:
        done = set()



    for index, row in df.iterrows():

        team = row["team"]


        if team in done:
            continue


        print(
            f"{index+1}/{len(df)} : {team}"
        )


        url = search_uefa_url(team)


        results.append(
            {
                "kassiesa_team": team,
                "country": row["country"],
                "coefficient": row["coefficient"],
                "uefa_url": url,
                "status": (
                    "found"
                    if url
                    else "not_found"
                )
            }
        )


        # sauvegarde intermédiaire
        if len(results) % 20 == 0:

            pd.DataFrame(results).to_csv(
                OUTPUT_FILE,
                index=False
            )

            print("Sauvegarde intermédiaire")


        # éviter limitation
        time.sleep(2)



    final = pd.DataFrame(results)

    final.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("\nFichier créé :", OUTPUT_FILE)

    print("\nStatuts :")
    print(
        final["status"].value_counts()
    )



if __name__ == "__main__":
    main()