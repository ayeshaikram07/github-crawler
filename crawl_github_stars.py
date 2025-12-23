import os
import time
import requests
import psycopg2
import pandas as pd
import json
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# -----------------------------
# GitHub GraphQL API setup
# -----------------------------
url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

TOTAL_REPOS = 1000  # Use 1000 for testing, change to 100_000
PER_PAGE = 50
fetched_repos = 0
after_cursor = None

while fetched_repos < TOTAL_REPOS:
    query = """
    query ($after: String) {
      search(query: "stars:>1", type: REPOSITORY, first: %d, after: $after) {
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          ... on Repository {
            name
            owner { login }
            stargazerCount
          }
        }
      }
    }
    """ % PER_PAGE

    variables = {"after": after_cursor}

    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            print("GitHub API error:", response.status_code, response.text)
            time.sleep(10)
            continue
    except Exception as e:
        print("Request failed:", e)
        time.sleep(10)
        continue

    nodes = data['data']['search']['nodes']
    page_info = data['data']['search']['pageInfo']

    for repo in nodes:
        cursor.execute(
            """
            INSERT INTO repos (repo_name, owner, stars)
            VALUES (%s, %s, %s)
            ON CONFLICT (repo_name, owner)
            DO UPDATE SET stars = EXCLUDED.stars, last_updated = CURRENT_TIMESTAMP
            """,
            (repo['name'], repo['owner']['login'], repo['stargazerCount'])
        )

    conn.commit()
    fetched_repos += len(nodes)
    print(f"Fetched {fetched_repos}/{TOTAL_REPOS} repos")

    if not page_info['hasNextPage']:
        break

    after_cursor = page_info['endCursor']
    time.sleep(1)

# -----------------------------
# Export data as JSON & CSV
# -----------------------------
cursor.execute("SELECT id, repo_name, owner, stars, last_updated FROM repos")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Convert to DataFrame
df = pd.DataFrame(rows, columns=columns)

# Save CSV
df.to_csv("repos_data.csv", index=False)
print("Saved repos_data.csv")

# Save JSON
df.to_json("repos_data.json", orient="records", indent=4)
print("Saved repos_data.json")

cursor.close()
conn.close()
print("Crawling complete!")
