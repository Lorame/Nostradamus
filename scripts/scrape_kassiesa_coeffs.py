import requests
from bs4 import BeautifulSoup
import csv

URL = "https://kassiesa.net/uefa/data/method5/trank2026.html"


response = requests.get(URL)
response.raise_for_status()
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.select("tr.clubline")

print(f"Clubs trouvés : {len(rows)}")

teams = []

for row in rows:
    cells = row.select("td, th")

    if len(cells) < 10:
        continue

    team = {
        "rank": cells[0].get_text(strip=True),
        "team": cells[2].get_text(strip=True),
        "country": cells[3].get_text(strip=True),
        "coefficient": cells[9].get_text(strip=True),
    }

    teams.append(team)

print(f"Clubs extraits : {len(teams)}")
print(teams[:3])

output_file = "data/raw/kassiesa_club_ranking_2026.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["rank", "team", "country", "coefficient"]
    )
    writer.writeheader()
    writer.writerows(teams)

print(f"Données enregistrées dans {output_file}")