import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("div", class_="card-content")

results = []

for job in jobs:
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()

    if title.lower().endswith("ist"):
        results.append((title, company, location))

# Save to file
with open("jobs.txt", "w") as f:
    for r in results:
        line = f"{r[0]} | {r[1]} | {r[2]}"
        print(line)
        f.write(line + "\n")

import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=csdata.cd4sevot432y.us-east-1.rds.amazonaws.com;"
    "DATABASE=IST311Projs;"
    "UID=IST311;"
    "PWD=i$t311spR26"
)

cursor = conn.cursor()

proj_id = 47

seq = 1

for r in results:
    cursor.execute("""
        INSERT INTO MidTerm.ProjectReport
        VALUES (?, ?, ?, ?, ?)
    """, proj_id, seq, r[0], r[1], r[2])

    seq += 1

conn.commit()
conn.close()