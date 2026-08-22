import pandas as pd
import re
import unicodedata
from rapidfuzz import fuzz, process


# =========================
# CONFIG
# =========================

KASSIESA_FILE = "data/raw/kassiesa_club_ranking_2026.csv"
WIKIDATA_FILE = "data/raw/wikidata_uefa_clubs.csv"

OUTPUT_FILE = "data/processed/kassiesa_wikidata_mapping.csv"


# =========================
# NORMALISATION
# =========================

def normalize_name(name):
    """
    Normalisation des noms de clubs
    """

    if pd.isna(name):
        return ""

    name = str(name).lower()

    # accents
    name = unicodedata.normalize(
        "NFD",
        name
    )

    name = "".join(
        c for c in name
        if unicodedata.category(c) != "Mn"
    )

    # caractères spéciaux
    name = re.sub(
        r"[^a-z0-9\s]",
        " ",
        name
    )

    # mots peu utiles
    remove_words = [
        "fc",
        "cf",
        "afc",
        "club",
        "football",
        "soccer",
        "sv",
        "fk",
        "kv",
        "sk",
        "ac",
        "as",
        "calcio"
    ]

    tokens = name.split()

    tokens = [
        t for t in tokens
        if t not in remove_words
    ]

    return " ".join(tokens)



# =========================
# CHARGEMENT
# =========================

kassiesa = pd.read_csv(KASSIESA_FILE)

wikidata = pd.read_csv(WIKIDATA_FILE)


print(f"Clubs Kassiesa : {len(kassiesa)}")
print(f"Clubs Wikidata : {len(wikidata)}")


# normalisation

kassiesa["name_norm"] = (
    kassiesa["team"]
    .apply(normalize_name)
)


wikidata["name_norm"] = (
    wikidata["team"]
    .apply(normalize_name)
)


# liste de recherche

wikidata_choices = (
    wikidata["name_norm"]
    .tolist()
)



# =========================
# MATCHING
# =========================

results = []


for i, row in kassiesa.iterrows():

    team = row["team"]
    name = row["name_norm"]

    matches = process.extract(
        name,
        wikidata_choices,
        scorer=fuzz.token_set_ratio,
        limit=2
    )


    best_name, score, index = matches[0]


    if len(matches) > 1:
        second_score = matches[1][1]
    else:
        second_score = 0


    gap = score - second_score


    matched_row = wikidata.iloc[index]


    if score >= 90:

        status = "auto"

    elif score >= 80 and gap >= 15:

        status = "auto_gap"

    else:

        status = "manual"



    results.append({

        "kassiesa_team": team,
        "country": row["country"],
        "coefficient": row["coefficient"],

        "wikidata_team": matched_row["team"],
        "wikidata_id": matched_row["wikidata_id"],
        "uefa_id": matched_row["uefa_id"],

        "similarity": score,
        "second_similarity": second_score,
        "gap": gap,

        "status": status

    })


    if (i+1) % 50 == 0:
        print(f"{i+1}/{len(kassiesa)} traités")



# =========================
# EXPORT
# =========================

df = pd.DataFrame(results)


df.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("Fichier créé :", OUTPUT_FILE)

print()
print("Statuts :")
print(df["status"].value_counts())


print()
print("Exemples :")
print(
    df.head(20).to_string(index=False)
)