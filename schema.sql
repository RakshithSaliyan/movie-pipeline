-- schema.sql
-- Database schema for MovieLens ETL project

-- Movies table (base + OMDb data)
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT,
    year INTEGER,
    imdb_id TEXT,
    director TEXT,
    plot TEXT,
    box_office TEXT
);

-- Genres (unique list)
CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

-- Link table: many-to-many relationship between movies and genres
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

-- Ratings table
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER,
    PRIMARY KEY (user_id, movie_id, timestamp),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
