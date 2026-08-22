import pandas as pd
import requests
import re


URL = "https://www.uefa.com/nationalassociations/uefarankings/club/?year=2026"

OUTPUT = "data/raw/uefa_club_ranking_2026.csv"


def extract_uefa_id(url):
    """
    Extrait l'identifiant UEFA depuis une URL club.
    Exemple:
    /clubs/50037--bayern-munchen/
    retourne 50037
    """

    match = re.search(r"/clubs/(\d+)--", url)

    if match:
        return int(match.group(1))

    return None


def fetch_page():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        )
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text



def extract_clubs(html):

    clubs = []

    # Recherche des URLs clubs UEFA
    urls = re.findall(
        r'https?://[^"]*?/uefachampionsleague/clubs/\d+--[^"]+',
        html
    )


    for url in urls:

        clean_url = url.replace("\\", "")

        uefa_id = extract_uefa_id(clean_url)

        clubs.append(
            {
                "uefa_url": clean_url,
                "uefa_id": uefa_id
            }
        )


    return clubs



def main():

    print("Téléchargement UEFA...")

    html = fetch_page()

    print(
        f"Taille HTML : {len(html)} caractères"
    )


    clubs = extract_clubs(html)


    df = pd.DataFrame(clubs)


    if df.empty:
        print(
            "Aucun club trouvé."
        )
        return


    df = df.drop_duplicates(
        subset=["uefa_id"]
    )


    print(
        f"Clubs trouvés : {len(df)}"
    )


    df.to_csv(
        OUTPUT,
        index=False
    )


    print(
        f"Fichier créé : {OUTPUT}"
    )


    print(
        df.head(10).to_string()
    )


if __name__ == "__main__":
    main()