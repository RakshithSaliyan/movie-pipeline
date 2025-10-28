import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("movies.db")
c = conn.cursor()

# Display first 10 movies with director & genre info
c.execute("SELECT title, director, genre FROM movies LIMIT 10")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
