-- 1️⃣ Movie with highest average rating
SELECT m.title, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 1;

-- 2️⃣ Top 5 genres with highest average rating
SELECT g.name AS genre, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movie_genres mg ON r.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
GROUP BY g.genre_id
ORDER BY avg_rating DESC
LIMIT 5;

3️⃣ Director with most movies
SELECT director, COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL AND director != ''
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

-- 4️⃣ Average rating of movies released each year
SELECT m.year, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movieId = m.movieId
GROUP BY m.year
ORDER BY m.year;
