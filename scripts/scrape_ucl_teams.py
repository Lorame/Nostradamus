from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


URL = "https://fr.uefa.com/uefachampionsleague/clubs/"

target_labels = {"Phase de ligue", "Barrages"}

teams_data = []


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    print(page.title())

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    groups = soup.select("div.teams-overview_group")

    print(f"Groupes trouvés : {len(groups)}")

    for group in groups:
        label = group.select_one("h2.teams-overview__label")

        if not label:
            continue

        group_name = label.get_text(strip=True)

        if group_name not in target_labels:
            continue

        teams = group.select("div.team")

        print(f"\n{group_name} : {len(teams)} équipes")

        for team in teams:
            name = team.select_one("span[slot='primary']")
            country = team.select_one("span[slot='secondary']")
            link = team.select_one("a.team-wrap")

            if name and country:
                team_name = name.get_text(strip=True)
                country_name = country.get_text(strip=True).replace("(", "").replace(")", "")

                print(f"- {team_name} ({country_name})")

                teams_data.append(
                    {
                        "team": team_name,
                        "country": country_name,
                        "stage": group_name,
                        "uefa_url": link["href"] if link else None
                    }
                )

    browser.close()


output_path = Path("data/raw/ucl_2026_2027_teams.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(teams_data)

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)

print(f"\nCSV créé : {output_path}")
print(f"Nombre d'équipes enregistrées : {len(df)}")