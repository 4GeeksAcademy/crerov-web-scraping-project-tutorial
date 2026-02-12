import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

pip install pandas requests lxml

url = "https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScienceProject/1.0; +https://example.com)"
}

response = requests.get(url, headers=headers)

response.raise_for_status()

print("Status:", response.status_code)

html = io.StringIO(response.text) #esto ha salido del solucionario, no se que es pero funciona.

tables = pd.read_html(html)
print(f"{len(tables)} tables were found.")

df = tables[0]  # Extract the first table from the 27 found
df.head()  # Display the first 5 rows

df = df.drop(100)

df["Release date"] = pd.to_datetime(df["Release date"], errors="coerce")
df["Streams (billions)"] = df["Streams (billions)"].astype(float)

conn = sqlite3.connect("spotify_top_songs.db")

df.to_sql("most_streamed", conn, if_exists="replace", index=False)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM most_streamed")
print("Rows inserted:", cursor.fetchone()[0])

conn.commit()
conn.close()

SELECT *
FROM df
ORDER BY "Streams (billions)" DESC
LIMIT 10;