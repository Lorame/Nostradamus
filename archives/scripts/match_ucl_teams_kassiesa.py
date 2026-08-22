import pandas as pd
import unicodedata
import re
from rapidfuzz import fuzz, process


UEFA_PATH = "data/raw/ucl_2026_2027_teams.csv"
KASSIESA_PATH = "data/raw/kassiesa_club_ranking_2026.csv"

OUTPUT_PATH = "data/processed/ucl_2026_2027_teams_coefficients.csv"


def normalize_name(name):
    """
    Normalisation des noms de clubs
    """

    name = str(name).lower()

    # enlever accents
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        c for c in name
        if not unicodedata.combining(c)
    )

    # caractères spéciaux
    name = re.sub(
        r"[^a-z0-9 ]",
        " ",
        name
    )

    # mots peu utiles
    stop_words = [
        "fc",
        "cf",
        "afc",
        "kv",
        "club"
    ]

    for word in stop_words:
        name = re.sub(
            rf"\b{word}\b",
            "",
            name
        )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()



uefa = pd.read_csv(UEFA_PATH)
kassiesa = pd.read_csv(KASSIESA_PATH)


print("Equipes UEFA :", len(uefa))
print("Clubs Kassiesa :", len(kassiesa))


uefa["normalized"] = uefa["team"].apply(normalize_name)
kassiesa["normalized"] = kassiesa["team"].apply(normalize_name)


results = []


for _, row in uefa.iterrows():

    matches = process.extract(
        row["normalized"],
        kassiesa["normalized"],
        scorer=fuzz.ratio,
        limit=2
    )


    best_team = None
    coefficient = None
    score = 0
    second_score = None


    if matches:

        best_normalized = matches[0][0]
        score = matches[0][1]


        best_row = kassiesa[
            kassiesa["normalized"] == best_normalized
        ].iloc[0]


        best_team = best_row["team"]
        coefficient = best_row["coefficient"]


        if len(matches) > 1:
            second_score = matches[1][1]


    gap = (
        score - second_score
        if second_score is not None
        else score
    )


    if score >= 90:
        status = "auto"

    elif score >= 70 and gap >= 15:
        status = "auto_gap"

    else:
        status = "manual"


    results.append(
        {
            "uefa_team": row["team"],
            "country": row["country"],
            "stage": row["stage"],
            "uefa_url": row["uefa_url"],
            "kassiesa_team": best_team,
            "coefficient": coefficient,
            "similarity": score,
            "second_similarity": second_score,
            "gap": gap,
            "status": status
        }
    )


df = pd.DataFrame(results)


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nFichier créé :", OUTPUT_PATH)

print("\nStatuts :")
print(df["status"].value_counts())


print("\nRésultats :")
print(
    df.to_string(index=False)
)