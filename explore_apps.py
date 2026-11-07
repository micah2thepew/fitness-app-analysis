from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


apps = pd.read_csv("data/fitness_apps_final.csv")
apps["release_year"] = pd.to_datetime(apps["release_date"], utc=True).dt.year
rated = apps.loc[apps["rating_count"] > 0].copy()

genre_summary = rated.groupby("genre").agg(
    rated_apps=("app_id", "size"),
    average_rating=("rating", "mean"),
    average_days_since_update=("days_since_update", "mean"),
)

print("Total apps:", len(apps))
print("Apps with ratings:", len(rated))
print("\nGenre summary:\n", genre_summary.round(2).to_string())
print(
    "\nCorrelation, all rated apps:",
    round(rated["days_since_update"].corr(rated["rating"]), 2),
)
well_rated = rated.loc[rated["rating_count"] >= 100]
print(
    "Correlation, apps with at least 100 ratings:",
    round(well_rated["days_since_update"].corr(well_rated["rating"]), 2),
)
print("Apps with at least 100 ratings:", len(well_rated))

figures = Path("figures")
figures.mkdir(exist_ok=True)

# Every bar starts at zero; value labels make the small differences legible.
rating_order = genre_summary.sort_values("average_rating")
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(rating_order.index, rating_order["average_rating"], color="#2171b5")
ax.bar_label(bars, fmt="%.2f", padding=4)
ax.set_xlim(0, 5.35)
ax.set_xlabel("Mean user rating (0–5 stars)")
ax.set_title("Average rating among rated apps, by assigned genre")
fig.tight_layout()
fig.savefig(figures / "average_rating_by_genre.png", dpi=200)
plt.close(fig)

# Each point summarizes one assigned genre, not an individual app.
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(
    genre_summary["average_days_since_update"],
    genre_summary["average_rating"],
    s=90,
    color="#d95f0e",
)
for genre, row in genre_summary.iterrows():
    ax.annotate(
        genre,
        (row["average_days_since_update"], row["average_rating"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8,
    )
ax.set_xlim(0, genre_summary["average_days_since_update"].max() + 75)
ax.set_ylim(
    genre_summary["average_rating"].min() - 0.03,
    genre_summary["average_rating"].max() + 0.03,
)
ax.set_xlabel("Mean days since latest update")
ax.set_ylabel("Mean user rating (0–5 stars)")
ax.set_title("Genre averages: update recency and rating")
fig.tight_layout()
fig.savefig(figures / "update_recency_vs_rating.png", dpi=200)
plt.close(fig)

# This counts original release years for apps in today's sample.
release_counts = (
    apps.groupby(["release_year", "genre"]).size().unstack(fill_value=0)
)
years = range(release_counts.index.min(), release_counts.index.max() + 1)
release_counts = release_counts.reindex(years, fill_value=0)
fig, axes = plt.subplots(4, 2, figsize=(10, 10), sharex=True, sharey=True)
for ax, genre in zip(axes.flat, release_counts.columns):
    ax.plot(release_counts.index, release_counts[genre], marker="o", markersize=3)
    ax.set_title(genre.title())
    ax.grid(axis="y", alpha=0.2)
    ax.set_xlim(release_counts.index.min(), release_counts.index.max())
    ax.set_xticks(range(2008, 2027, 4))
for ax in axes[-1, :]:
    ax.set_xlabel("Original release year")
for ax in axes[:, 0]:
    ax.set_ylabel("Apps in sample")
fig.tight_layout()
fig.savefig(figures / "release_year_by_genre.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 5))
release_counts.plot.bar(stacked=True, ax=ax, width=0.85)
ax.set_xlabel("Original release year")
ax.set_ylabel("Apps in sample")
ax.set_xticklabels(release_counts.index, rotation=45, ha="right")
ax.legend(title="Assigned genre", bbox_to_anchor=(1.02, 1), loc="upper left")
fig.tight_layout()
fig.savefig(figures / "release_year_by_genre_stacked.png", dpi=200)
plt.close(fig)
