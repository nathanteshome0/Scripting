# Job Data Pipeline Project

This is a Python project that scrapes job listings from the Real Python fake-jobs site, filters listings by job-title suffix, writes the results to a text file, and can optionally load the filtered records into Microsoft SQL Server.

This repository began as a scripting project for my scripting class and has been cleaned and revamped to demonstrate safer configuration, reusable Python functions, command-line options, error handling, and clearer project organization.

## Features

- Scrapes structured job data with `requests` and `BeautifulSoup`
- Extracts job title, company, and location
- Filters job titles by a configurable suffix
- Writes results to a pipe-delimited text file
- Optionally inserts records into SQL Server with parameterized queries
- Reads database credentials from environment variables instead of source code
- Handles HTTP, database, and configuration errors
- Provides a command-line interface for common options

## Project Structure

```text
Scripting/
├── data/
│   └── jobs.txt
├── docs/
│   ├── project-report.pdf
│   └── screenshots/
├── src/
│   └── job_scraper.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10+
- Microsoft ODBC Driver for SQL Server if using database output
- Access to a compatible SQL Server instance if using database output

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the scraper with the default settings:

```bash
python src/job_scraper.py
```

By default, the script filters for job titles ending in `ist` and writes the results to `data/jobs.txt`.

Use a different suffix or output file:

```bash
python src/job_scraper.py --suffix engineer --output data/engineer_jobs.txt
```

### Save Results to SQL Server

Copy `.env.example` values into environment variables for your system. Do not commit real credentials.

Required variables:

```text
DB_SERVER
DB_NAME
DB_USER
DB_PASSWORD
```

Optional variable:

```text
DB_DRIVER
```

Then run:

```bash
python src/job_scraper.py --save-to-db --project-id 47
```

The script inserts records into `MidTerm.ProjectReport` using the following fields:

- `ProjID`
- `SeqNo`
- `JobTitle`
- `Employer`
- `Location`

If your database schema differs, update the SQL statement in `insert_results()`.

## Example Output

```text
Physiological scientist | Kramer-Klein | South Christopher, AE
Meteorologist | Bush PLC | Kelseystad, AA
Data scientist | Thomas Group | Port Robertfurt, AA
Sports therapist | Spencer and Sons | Hullview, AA
Medical physicist | Parker, Goodwin and Zavala | Bellberg, AP
```

## Implementation Notes

The project separates scraping, file output, and database insertion into dedicated functions. The HTTP request uses a timeout and checks for failed responses before parsing. Database inserts use placeholders rather than constructing SQL from scraped values.

The SQL Server portion is optional, so the web-scraping and file-output portions can run without database access.

## Documentation

The `docs/` directory contains the original project report and renamed verification screenshots showing the scraper output and SQL Server results.

## Skills Demonstrated

- Python scripting
- Web scraping and HTML parsing
- HTTP request handling
- File I/O
- Data filtering and transformation
- Microsoft SQL Server integration
- Parameterized SQL queries
- Environment-based configuration
- Command-line interfaces
- Basic ETL workflow design

## Security

Database passwords and other secrets should never be committed to a repository. This project uses environment variables for database configuration and includes `.env` in `.gitignore`.

If a credential has ever been committed to Git history, removing it from the latest version does not invalidate the exposed credential. Rotate the credential and, when appropriate, remove the secret from repository history.

## Author

Nathan Teshome
