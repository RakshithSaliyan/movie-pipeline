# 🎬 Movie Data Pipeline (ETL + Analytics)

## 🧠 Overview
This project implements an **ETL (Extract, Transform, Load)** pipeline that enriches movie data from the **MovieLens dataset** using the **TMDb (The Movie Database) API**.  
The enriched data — including **directors, genres, and plots** — is then loaded into an **SQLite database (`movies.db`)** for analytics.

Originally, the assignment required OMDb API, but this implementation uses **TMDb** because it provides more accurate and detailed data.

---

## 📁 Project Structure

movie-pipeline/
│
├── movies.csv                # Source movie data (from MovieLens)
├── ratings.csv               # MovieLens ratings data
├── tmdb_cache.json           # Cached TMDb responses (for faster re-runs)
├── movies.db                 # SQLite database with enriched data
│
├── etl.py                    # Main ETL pipeline using TMDb API
├── check_movies.py           # Script to verify data from database
│
├── schema.sql                # Database schema definitions
├── queries.sql               # SQL queries for analytics
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation



---

## ⚙️ Features

✅ Extracts raw data from `movies.csv`  
✅ Fetches **director**, **genre**, and **plot** from **TMDb API**  
✅ Uses **thread-safe caching** with `tmdb_cache.json` to avoid duplicate requests  
✅ Loads enriched movie data into **SQLite database (`movies.db`)**  
✅ Includes **analytics queries** to get insights from the data  
✅ Handles **multi-threaded API requests** for better performance  

---

## 🧰 Technologies Used

- **Python 3.11+**
- **SQLite**
- **TMDb API**
- **Requests**
- **ThreadPoolExecutor**
- **JSON / CSV**
- **DB Browser for SQLite**

---

## 🔑 TMDb API Setup

### 1️⃣ Get a TMDb API Key
1. Visit [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
2. Sign up for a free account
3. Apply for a **Developer API key**
4. Copy your API key

### 2️⃣ Create a `.env` file in your project root folder
TMDB_API_KEY=your_api_key_here

> Alternatively, you can directly paste the key inside `etl_tmdb.py` for local testing.

---

## ▶️ Steps to Run the Project

Step 1: Clone the Repository
git clone <your-repo-link>
cd movie-pipeline

Step 2: Create and Activate Virtual Environment
python -m venv venv
.\venv\Scripts\activate   # For Windows

Step 3: Install Required Packages
pip install -r requirements.txt

Step 4: Run the ETL Script
This will:
Read movies.csv
Fetch details from TMDb API
Cache results in tmdb_cache.json
Populate SQLite database movies.db


python etl.py

Example Output:
🎬 Movies CSV loaded: 9742 rows
🚀 Fetching TMDb data for 100 movies...
[1/100] ✅ Toy Story → John Lasseter
[2/100] ✅ Jumanji → Joe Johnston
...
🎉 SQLite database updated with TMDb data successfully!

Step 5: Verify Database Content
python check_movies.py

Expected Output:

('Toy Story', 'John Lasseter', 'Family, Comedy, Animation, Adventure')
('Jumanji', 'Joe Johnston', 'Adventure, Fantasy, Family')
('Heat', 'Michael Mann', 'Crime, Drama, Action')

Step 6: Open Database (Optional GUI)
Install DB Browser for SQLite
Open movies.db
Go to Execute SQL tab
Copy and paste queries from queries.sql

📊 SQL Queries for Analysis
1️⃣ Movie with the Highest Average Rating

SELECT m.title, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 1;

2️⃣ Top 5 Genres with Highest Average Rating

SELECT g.name AS genre, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movie_genres mg ON r.movie_id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
GROUP BY g.genre_id
ORDER BY avg_rating DESC
LIMIT 5;

3️⃣ Director with the Most Movies

SELECT director, COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL AND director != ''
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

4️⃣ Average Rating by Year

SELECT m.year, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movieId
GROUP BY m.year
ORDER BY m.year;

🧩 Database Schema (schema.sql)
Table Name	         Description
movies	             Stores movie title, year, director, genre, plot
genres	             Stores unique genre list
movie_genres	     Links movies to genres (many-to-many)
ratings              Contains user ratings for each movie

🧾 Example Output
Title	    Director	        Genre
Toy Story	John Lasseter	    Animation, Adventure, Comedy
Jumanji	    Joe Johnston	    Adventure, Fantasy, Family
Heat	    Michael Mann	    Action, Crime, Drama
GoldenEye	Martin Campbell	    Action, Adventure, Thriller

⚡ Performance and Optimization
Used ThreadPoolExecutor for parallel API calls
Implemented local JSON cache to store TMDb responses
API throttling handled with short delay (time.sleep(0.1))
Data fetching is resumable (skips already cached movies)

✅ Deliverables Checklist
Requirement	                    Description	                                    Status
ETL pipeline implemented	    Extraction from CSV + TMDb enrichment       	✅
SQLite database created	        movies.db generated with enriched data	        ✅
Multi-threaded API fetching	    Using ThreadPoolExecutor	                    ✅
Cache mechanism	                Implemented via tmdb_cache.json	                ✅
SQL queries written	            queries.sql completed	                        ✅
README documentation	        Clear setup and run instructions	            ✅
Ratings analytics	            Included in queries.sql	                        ✅
Schema definition	            Defined in schema.sql	                        ✅

🚀 Optional Enhancements
Add a Flask dashboard for data visualization
Automate ETL runs using Apache Airflow or Cron
Integrate IMDb or OMDb APIs for extra metadata

👨‍💻 Author
Rakshith Saliyan N
📧 rakshithsaliyan539@gmail.com
