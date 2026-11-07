import pandas as pd

df = pd.read_csv("data/fitness_apps_initial.csv")

print("Total apps:", len(df))
print("Duplicate app IDs:", df["app_id"].duplicated().sum())

important_columns = [
    "rating",
    "rating_count",
    "upfront_price",
    "release_date",
    "latest_update",
]

print("\nMissing values:")
print(df[important_columns].isna().sum())

print("\nRating count summary:")
print(df["rating_count"].describe())

print("\nApps found by multiple searches:")
print(df["search_terms"].str.contains(",", na=False).sum())

print("\nRandom sample to review for relevance:")
print(
    df[["name", "search_terms"]]
    .sample(25, random_state=386)
    .to_string(index=False)
)