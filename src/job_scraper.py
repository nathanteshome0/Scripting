from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

import pyodbc
import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT = Path("data/jobs.txt")

JobRecord = tuple[str, str, str]


def scrape_jobs(url: str = SOURCE_URL, title_suffix: str = "ist") -> list[JobRecord]:
    """Scrape job listings and return records whose titles end with title_suffix."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[JobRecord] = []

    for card in soup.select("div.card-content"):
        title_element = card.select_one("h2.title")
        company_element = card.select_one("h3.company")
        location_element = card.select_one("p.location")

        if not all((title_element, company_element, location_element)):
            continue

        title = title_element.get_text(strip=True)
        company = company_element.get_text(strip=True)
        location = location_element.get_text(strip=True)

        if title.lower().endswith(title_suffix.lower()):
            results.append((title, company, location))

    return results


def write_results(records: Iterable[JobRecord], output_path: Path) -> None:
    """Write job records to a pipe-delimited text file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        for title, company, location in records:
            output_file.write(f"{title} | {company} | {location}\n")


def get_database_connection() -> pyodbc.Connection:
    """Create a SQL Server connection from environment variables."""
    required_variables = ("DB_SERVER", "DB_NAME", "DB_USER", "DB_PASSWORD")
    missing = [name for name in required_variables if not os.getenv(name)]

    if missing:
        raise RuntimeError(
            "Missing required database environment variables: " + ", ".join(missing)
        )

    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={os.environ['DB_SERVER']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USER']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)


def insert_results(records: Iterable[JobRecord], project_id: int) -> None:
    """Insert job records into MidTerm.ProjectReport using parameterized SQL."""
    insert_statement = """
        INSERT INTO MidTerm.ProjectReport
            (ProjID, SeqNo, JobTitle, Employer, Location)
        VALUES (?, ?, ?, ?, ?)
    """

    with get_database_connection() as connection:
        cursor = connection.cursor()

        for sequence, (title, company, location) in enumerate(records, start=1):
            cursor.execute(
                insert_statement,
                project_id,
                sequence,
                title,
                company,
                location,
            )

        connection.commit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape fake job listings, filter by title suffix, and optionally save to SQL Server."
    )
    parser.add_argument(
        "--url",
        default=SOURCE_URL,
        help="Source page containing job listings.",
    )
    parser.add_argument(
        "--suffix",
        default="ist",
        help="Keep job titles ending with this suffix (default: ist).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output text file (default: data/jobs.txt).",
    )
    parser.add_argument(
        "--save-to-db",
        action="store_true",
        help="Insert the filtered records into SQL Server.",
    )
    parser.add_argument(
        "--project-id",
        type=int,
        help="Project ID required when --save-to-db is used.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        records = scrape_jobs(args.url, args.suffix)
        write_results(records, args.output)

        for title, company, location in records:
            print(f"{title} | {company} | {location}")

        print(f"\nSaved {len(records)} records to {args.output}.")

        if args.save_to_db:
            if args.project_id is None:
                raise ValueError("--project-id is required when --save-to-db is used.")

            insert_results(records, args.project_id)
            print(f"Inserted {len(records)} records into SQL Server.")

    except (requests.RequestException, pyodbc.Error, RuntimeError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()
