import json
from pathlib import Path
import pandas as pd


INPUT = Path("data/raw/uefa_network/all_json.json")
OUTPUT = Path("data/raw/uefa_club_coefficients_full.csv")


print("Chargement JSON UEFA...")


with open(INPUT, encoding="utf-8") as f:
    responses = json.load(f)


clubs = []


for response in responses:

    url = response.get("url", "")

    if "coefficients" not in url:
        continue

    print("Analyse :", url)

    try:
        members = response["data"]["data"]["members"]

    except KeyError:
        continue


    for item in members:

        member = item["member"]
        overall = item["overallRanking"]


        row = {

            "club_id": member.get("id"),

            "club": member.get("displayName"),

            "official_name": member.get("displayOfficialName"),

            "country": member.get("countryName"),

            "country_code": member.get("countryCode"),

            "team_code": member.get("teamCode"),

            "uefa_logo": member.get("logoUrl"),

            "rank": overall.get("position"),

            "points": overall.get("totalPoints"),

            "national_association_points": overall.get(
                "nationalAssociationPoints"
            )
        }


        # Historique 5 saisons
        seasons = item.get("seasonRankings", [])


        for season in seasons:

            year = season.get("seasonYear")

            if year:

                row[
                    f"season_{year}"
                ] = season.get("totalPoints")


        clubs.append(row)



print()
print("Clubs trouvés :", len(clubs))


df = pd.DataFrame(clubs)


if not df.empty:

    df = df.drop_duplicates(
        subset=["club_id"]
    )


    df = df.sort_values(
        "points",
        ascending=False
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


    print("CSV créé :", OUTPUT)

    print(df.head(20))


else:

    print("Aucun club trouvé")