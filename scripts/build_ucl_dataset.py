from pathlib import Path
import pandas as pd
import re


# Paths
ucl_path = Path("data/raw/ucl_2026_2027_teams.csv")
coef_path = Path("data/raw/uefa_club_coefficients_full.csv")

output_path = Path("data/processed/ucl_2026_2027_clubs_full.csv")


# Load data
ucl = pd.read_csv(ucl_path)
coef = pd.read_csv(coef_path)


# Extract UEFA club ID from URL
ucl["club_id"] = (
    ucl["uefa_url"]
    .astype(str)
    .apply(lambda x: re.findall(r"\d+", x)[0] if re.findall(r"\d+", x) else None)
)

# Convert type for merge
ucl["club_id"] = ucl["club_id"].astype(str)
coef["club_id"] = coef["club_id"].astype(str)


print("UCL clubs :", len(ucl))
print("UEFA coefficients :", len(coef))


# Merge
df = ucl.merge(
    coef,
    on="club_id",
    how="left",
    suffixes=("_ucl", "_uefa")
)


# Check missing coefficients
missing = df[df["points"].isna()]

print("\nClubs without UEFA coefficients:")
print(missing[["team", "club_id"]])


# Save
output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)


print("\nDataset final créé :", output_path)
print("Nombre de clubs :", len(df))
print(df.head())

print("\nDataset validation:")
print(df.groupby("stage").size())
print("\nColonnes:")
print(df.columns.tolist())