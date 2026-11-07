import pandas as pd

df = pd.read_csv("data/fitness_apps_initial.csv")

# Preserve Apple's genre and the complete list of matched searches.
df = df.rename(columns={
    "genre": "apple_genre",
    "search_terms": "matched_search_terms",
})

priority = [
    "weightlifting",
    "pilates",
    "yoga",
    "running",
    "cycling workout",
    "strength training",
    "home workout",
    "fitness tracker",
]

def choose_genre(matched_search_terms):
    terms = {term.strip() for term in matched_search_terms.split(",")}

    if len(terms) > 1:
        terms.discard("fitness tracker")

    return next(term for term in priority if term in terms)

df["genre"] = df["matched_search_terms"].apply(choose_genre)

for column in ["collected_at", "release_date", "latest_update"]:
    df[column] = pd.to_datetime(df[column], utc=True)

df["app_age_days"] = (df["collected_at"] - df["release_date"]).dt.days
df["days_since_update"] = (
    df["collected_at"] - df["latest_update"]
).dt.days
df["has_ratings"] = df["rating_count"] > 0

df.to_csv("data/fitness_apps_final.csv", index=False)

print("Final rows:", len(df))
print(df["genre"].value_counts())