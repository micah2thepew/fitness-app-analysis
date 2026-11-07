import requests

url = "https://itunes.apple.com/search"
parameters = {
    "term": "running",
    "country": "us",
    "entity": "software",
    "limit": 5,
}

response = requests.get(url, params=parameters, timeout=20)
response.raise_for_status()
data = response.json()

print("Apps returned:", data["resultCount"])

for app in data["results"]:
    print({
        "name": app.get("trackName"),
        "developer": app.get("artistName"),
        "genre": app.get("primaryGenreName"),
        "rating": app.get("averageUserRating"),
        "rating_count": app.get("userRatingCount"),
        "upfront_price": app.get("price"),
        "release_date": app.get("releaseDate"),
        "latest_update": app.get("currentVersionReleaseDate"),
    })