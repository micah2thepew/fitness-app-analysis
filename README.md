# Fitness apps in the U.S. App Store

This repository contains the Python code for a STAT 386 data-acquisition project. It uses [Apple's Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/) to collect public metadata for apps returned by eight fitness-related searches, deduplicates results by App Store ID, assigns one analysis genre per app, and makes summary figures.

The November 6, 2026 run found **304 unique Health & Fitness apps**. This is a sample of search results, not a census of all fitness apps. The [blog post](https://micah2thepew.github.io/micahkp.github.io/fitness-apps.html) explains the question, collection choices, ethics, and findings.

## Files

| File | Purpose |
|---|---|
| `collect_apps.py` | Request up to 50 U.S. apps for each of eight search phrases, pause three seconds between requests, and save the deduplicated initial CSV. |
| `prepare_apps.py` | Assign one analysis genre, calculate age and update-recency features, and save the final CSV. |
| `explore_apps.py` | Print summaries and create the four charts in `figures/`. |
| `inspect_apps.py`, `explore_api.py` | Small inspection scripts used during development. |
| `figures/` | Figures from the November 6, 2026 collection. |

## Reproduce the workflow

From this directory, create a Python environment and install the packages in `requirements.txt`. Then run:

```bash
python collect_apps.py
python prepare_apps.py
python explore_apps.py
```

The scripts write CSVs into `data/`. Search results, ratings, and update dates can change, so a new run may produce different counts and figures. Python 3.13 was used for the original run.

## Data and reuse

The raw and cleaned CSVs are not included while reuse rights for a compiled Apple metadata dataset are being reviewed. The scripts make the collection and transformations reproducible without an API key. The published charts contain only aggregate summaries. Do not interpret search-result counts as market size, downloads, or evidence that updates cause higher ratings.
