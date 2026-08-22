import pandas as pd
import unicodedata
import re
from rapidfuzz import fuzz, process


KASSIESA_PATH = "data/raw/kassiesa_club_ranking_2026.csv"
WIKIDATA_PATH = "data/raw/wikidata_uefa_clubs.csv"

OUTPUT_PATH = "data/processed/kassiesa_wikidata_matching.csv"


def normalize_name(name):
    """
    Normalisation des noms de clubs
    """

    name = str(name).lower()

    # Suppression des accents
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        c for c in name
        if not unicodedata.combining(c)
    )

    # Suppression caractères spéciaux
    name = re.sub(
        r"[^a-z0-9 ]",
        " ",
        name
    )

    # Suppression termes fréquents
    stop_words = [
        "fc",
        "cf",
        "afc",
        "kv",
        "club",
    ]

    for word in stop_words:
        name = re.sub(
            rf"\b{word}\b",
            "",
            name
        )

    # Nettoyage espaces
    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()


# Chargement des données

kassiesa = pd.read_csv(KASSIESA_PATH)
wikidata = pd.read_csv(WIKIDATA_PATH)


print("Clubs Kassiesa :", len(kassiesa))
print("Clubs Wikidata :", len(wikidata))


# Normalisation

kassiesa["normalized"] = kassiesa["team"].apply(normalize_name)
wikidata["normalized"] = wikidata["team"].apply(normalize_name)


results = []


for _, row in kassiesa.iterrows():

    # Pour l'instant on compare avec tous les clubs Wikidata
    candidates = wikidata


    matches = process.extract(
        row["normalized"],
        candidates["normalized"],
        scorer=fuzz.ratio,
        limit=2
    )


    best_name = None
    uefa_id = None
    best_score = 0
    second_score = None


    if matches:

        best_normalized = matches[0][0]
        best_score = matches[0][1]


        best_row = candidates[
            candidates["normalized"] == best_normalized
        ].iloc[0]


        best_name = best_row["team"]
        uefa_id = best_row["uefa_id"]


        if len(matches) > 1:
            second_score = matches[1][1]


    gap = (
        best_score - second_score
        if second_score is not None
        else best_score
    )


    # Règles de décision

    if best_score >= 90:
        status = "auto"

    elif best_score >= 70 and gap >= 15:
        status = "auto_gap"

    else:
        status = "manual"


    results.append(
        {
            "kassiesa_team": row["team"],
            "country": row["country"],
            "coefficient": row["coefficient"],
            "wikidata_team": best_name,
            "uefa_id": uefa_id,
            "similarity": best_score,
            "second_similarity": second_score,
            "gap": gap,
            "status": status,
        }
    )


# Création dataframe résultat

df = pd.DataFrame(results)


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nFichier créé :", OUTPUT_PATH)


print("\nRépartition des statuts :")
print(df["status"].value_counts())


print("\nExemples :")
print(
    df.head(20).to_string(index=False)
)