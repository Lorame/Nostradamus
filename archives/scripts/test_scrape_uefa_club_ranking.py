from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import html


URL = "https://www.uefa.com/nationalassociations/uefarankings/club/?year=2026"


OUTPUT = Path("data/raw/test_uefa_club_ranking_urls.csv")
DEBUG_HTML = Path("data/raw/uefa_debug.html")


def slugify(text):
    """
    Transforme un nom de club en slug UEFA probable
    """
    text = text.lower()

    replacements = {
        "ä": "a",
        "ö": "o",
        "ü": "u",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "á": "a",
        "à": "a",
        "ñ": "n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def scrape_uefa():

    print("Chargement UEFA...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        # attendre le tableau React
        page.wait_for_timeout(5000)

        html_content = page.content()

        DEBUG_HTML.write_text(
            html_content,
            encoding="utf-8"
        )

        browser.close()


    soup = BeautifulSoup(
        html_content,
        "html.parser"
    )


    clubs = []


    rows = soup.select(
        "div[role='row']"
    )


    for row in rows:

        club_cell = row.select_one(
            "pk-identifier"
        )

        if not club_cell:
            continue


        name = club_cell.get(
            "title"
        )


        if not name:

            span = club_cell.select_one(
                "span"
            )

            if span:
                name = span.text.strip()


        if not name:
            continue


        row_id = row.get(
            "row-id"
        )


        country = None

        secondary = club_cell.select_one(
            "[slot='secondary']"
        )

        if secondary:
            country = secondary.text.strip()


        if row_id:

            club_url = (
                "https://www.uefa.com/"
                "uefachampionsleague/clubs/"
                f"{row_id}--{slugify(name)}/"
            )

        else:
            club_url = None


        clubs.append(
            {
                "club": name,
                "country": country,
                "club_id": row_id,
                "uefa_url": club_url
            }
        )


    return pd.DataFrame(clubs)



if __name__ == "__main__":

    df = scrape_uefa()

    print()
    print(
        f"Clubs trouvés : {len(df)}"
    )

    print()

    print(
        df.head(10)
    )


    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    df.to_csv(
        OUTPUT,
        index=False,
        encoding="utf-8"
    )


    print()
    print(
        f"Fichier créé : {OUTPUT}"
    )