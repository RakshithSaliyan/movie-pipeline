import os
import csv
import sqlite3
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ---------------------------
# CONFIGURATION
# ---------------------------
MOVIES_CSV = "movies.csv"
CACHE_FILE = "tmdb_cache.json"
TMDB_API_KEY = "a2b9da0add8ca508651e514568bc46c2"  # your TMDb key
TMDB_URL = "https://api.themoviedb.org/3/search/movie"
DETAIL_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
MAX_WORKERS = 10
BATCH_SIZE = 100

# ---------------------------
# THREAD-SAFE CACHE
# ---------------------------
cache_lock = threading.Lock()
tmdb_cache = {}

# ---------------------------
# LOAD MOVIES CSV
# ---------------------------
movies = []
with open(MOVIES_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title_year = row["title"]
        if "(" in title_year and ")" in title_year:
            title = title_year.rsplit("(", 1)[0].strip()
            year = title_year.rsplit("(", 1)[1].replace(")", "").strip()
        else:
            title, year = title_year, ""
        movies.append({
            "movieId": row["movieId"],
            "title": title,
            "year": year
        })

print(f"🎬 Movies CSV loaded: {len(movies)} rows")

# ---------------------------
# LOAD CACHE
# ---------------------------
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            tmdb_cache = json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("⚠️ Cache file corrupted. Starting new.")
        tmdb_cache = {}

# ---------------------------
# FETCH MOVIE DATA
# ---------------------------
def fetch_movie_data(movie):
    title = movie["title"]
    year = movie["year"]
    key = f"{title} ({year})"

    with cache_lock:
        if key in tmdb_cache:
            data = tmdb_cache[key]
            movie["director"] = data.get("director", "")
            movie["genre"] = data.get("genre", "")
            movie["plot"] = data.get("plot", "")
            return movie

    try:
        # Search for movie
        params = {"api_key": TMDB_API_KEY, "query": title, "year": year}
        response = requests.get(TMDB_URL, params=params, timeout=10)
        search_data = response.json()

        if search_data.get("results"):
            movie_id = search_data["results"][0]["id"]
            # Get movie details
            details = requests.get(DETAIL_URL.format(movie_id=movie_id),
                                   params={"api_key": TMDB_API_KEY, "append_to_response": "credits"},
                                   timeout=10).json()

            directors = [crew["name"] for crew in details.get("credits", {}).get("crew", [])
                         if crew.get("job") == "Director"]
            genres = [g["name"] for g in details.get("genres", [])]

            data = {
                "director": ", ".join(directors) if directors else "",
                "genre": ", ".join(genres),
                "plot": details.get("overview", "")
            }
        else:
            print(f"❌ Not found: {title} ({year})")
            data = {"director": "", "genre": "", "plot": ""}

    except Exception as e:
        print(f"⚠️ Error fetching {title}: {e}")
        data = {"director": "", "genre": "", "plot": ""}

    with cache_lock:
        tmdb_cache[key] = data
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(tmdb_cache, f, indent=4)

    movie["director"] = data["director"]
    movie["genre"] = data["genre"]
    movie["plot"] = data["plot"]

    time.sleep(0.1)
    return movie


# ---------------------------
# PARALLEL FETCHING
# ---------------------------
to_fetch = [m for m in movies if f"{m['title']} ({m['year']})" not in tmdb_cache][:100]
total = len(to_fetch)
print(f"🚀 Fetching TMDb data for {total} movies...\n")

for start in range(0, total, BATCH_SIZE):
    end = min(start + BATCH_SIZE, total)
    batch = to_fetch[start:end]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_movie_data, m): m for m in batch}
        for i, future in enumerate(as_completed(futures), start=start + 1):
            movie = future.result()
            print(f"[{i}/{total}] ✅ {movie['title']} → {movie['director']}")

print("✅ Data fetching complete!")

# ---------------------------
# SAVE TO SQLITE
# ---------------------------
conn = sqlite3.connect("movies.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS movies")
c.execute("""
CREATE TABLE movies (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    year TEXT,
    director TEXT,
    genre TEXT,
    plot TEXT
)
""")

for movie in movies:
    # Use defaults if keys are missing
    director = movie.get("director", "")
    genre = movie.get("genre", "")
    plot = movie.get("plot", "")

    c.execute("""
    INSERT OR REPLACE INTO movies (movieId, title, year, director, genre, plot)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (movie["movieId"], movie["title"], movie["year"], director, genre, plot))


conn.commit()
conn.close()
print("🎉 SQLite database updated with TMDb data successfully!")
