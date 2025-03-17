from article_scrapper import *
import sqlite3
from datetime import datetime
from article_scrapper import fetch_articles

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()

# Create table if not already done
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        content TEXT,
        url TEXT UNIQUE,  -- Store the article link
        date TEXT
    )
""")

sites = ['indianexpress.com', 'bbc.com', 'timesofindia.indiatimes.com']
articles = fetch_articles(sites)

# Insert articles into the database
for source, data in articles.items():
    for url, content in data:  # Extract content & URL
        cursor.execute("""
            INSERT OR IGNORE INTO articles (source, content, url, date) 
            VALUES (?, ?, ?, ?)
        """, (source, content, url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

# Commit changes and close connection
conn.commit()
conn.close()
