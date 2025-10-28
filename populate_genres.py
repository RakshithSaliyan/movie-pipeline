import sqlite3

conn = sqlite3.connect("movies.db")
c = conn.cursor()

# Create tables if they don't exist
c.execute("""
CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movieId),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
)
""")

# Fetch movie IDs and genres
c.execute("SELECT movieId, genre FROM movies WHERE genre IS NOT NULL AND genre != ''")
rows = c.fetchall()

for movie_id, genre_str in rows:
    genres = [g.strip() for g in genre_str.split(",") if g.strip()]
    for g in genres:
        # Insert unique genre
        c.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (g,))
        # Link movie to genre
        c.execute("""
            INSERT OR IGNORE INTO movie_genres (movie_id, genre_id)
            VALUES (?, (SELECT genre_id FROM genres WHERE name = ?))
        """, (movie_id, g))

conn.commit()
conn.close()

print("✅ Genres and movie_genres tables populated successfully!")
