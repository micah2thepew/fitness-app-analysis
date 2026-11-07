from datetime import datetime, timezone
from pathlib import Path
import time

import pandas as pd
import requests


SEARCH_TERMS = [
    "running",
    "weightlifting",
    "strength training",
    "yoga",
    "pilates",
    "cycling workout",
    "home workout",
    "fitness tracker",
]

apps_by_id = {}
collected_at = datetime.now(timezone.utc).isoformat()


def fetch_results(term):
    response = requests.get(
        "https://itunes.apple.com/search",
        params={
            "term": term,
            "country": "us",
            "entity": "software",
            "limit": 50,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["results"]


def make_record(app, collected_at):
    return {
        "app_id": app["trackId"],
        "name": app.get("trackName"),
        "developer": app.get("artistName"),
        "genre": app.get("primaryGenreName"),
        "rating": app.get("averageUserRating"),
        "rating_count": app.get("userRatingCount"),
        "upfront_price": app.get("price"),
        "release_date": app.get("releaseDate"),
        "latest_update": app.get("currentVersionReleaseDate"),
        "collected_at": collected_at,
        "search_terms": set(),
    }


for term in SEARCH_TERMS:
    results = fetch_results(term)

    for app in results:
        # Keep apps in Apple's Health & Fitness genre.
        if app.get("primaryGenreName") != "Health & Fitness":
            continue

        app_id = app.get("trackId")
        if app_id is None:
            continue

        # An app can appear in more than one search.
        if app_id not in apps_by_id:
            apps_by_id[app_id] = make_record(app, collected_at)

        apps_by_id[app_id]["search_terms"].add(term)

    print(f"{term}: {len(results)} results")
    time.sleep(3)  # Space out requests.


# Convert the sets of search terms into text that fits in a CSV file.
rows = []
for app in apps_by_id.values():
    app["search_terms"] = ", ".join(sorted(app["search_terms"]))
    rows.append(app)

df = pd.DataFrame(rows)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/fitness_apps_initial.csv", index=False)

print(f"\nUnique Health & Fitness apps: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(df[["name", "rating", "rating_count", "search_terms"]].head())
