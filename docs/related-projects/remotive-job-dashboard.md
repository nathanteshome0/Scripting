# Website Data Scraper Dashboard for Job Listings

This document summarizes a related IST 311 scripting project that explored a broader job-data workflow than the primary scraper in this repository. It is included as companion coursework because both projects focus on automating job-listing collection and turning raw job data into a more useful format.

> **Important:** This is a related project, not the same implementation as `src/job_scraper.py`. The primary project in this repository uses the Real Python fake-jobs page, BeautifulSoup, text output, and optional SQL Server storage. This companion project used the Remotive public API, CSV storage, and a Streamlit dashboard.

## Project Overview

The project, titled **Website Data Scraper Dashboard for Job Listings**, was created for **IST 311 – Scripting Languages** by:

- Kabir Singh
- Nathan Teshome
- Brett Cannon

The goal was to reduce the time spent manually browsing job boards by creating a Python-based system that automatically collects remote job-listing data and presents it through an interactive dashboard.

The overall workflow was:

```text
Remotive API -> scraper.py -> jobs.csv -> dashboard.py
```

The solution had two main components:

1. A data-collection script that retrieved job listings from the Remotive public API.
2. A Streamlit dashboard that loaded the resulting CSV file and displayed charts, summary statistics, a map, and a full job table.

## Technologies Used

- Python
- Requests
- Pandas
- Streamlit
- Plotly
- Remotive public API

## Data Collection

The scraper sent requests to the Remotive remote-jobs API and processed the returned JSON data. The report describes extracting fields such as:

- Job title
- Company
- Location
- Category
- Job type
- Salary
- Publication date
- Job link
- Source
- Scrape timestamp

The processed results were saved to `jobs.csv` for use by the dashboard.

One design decision was to use a public API rather than scraping sites such as LinkedIn or Indeed because those sites can restrict or block automated scraping.

## Dashboard

The dashboard was built with Streamlit and Pandas, with Plotly used for charts and map visualization.

The dashboard included:

- Total job count
- Unique company count
- World map of job locations
- Jobs-by-location bar chart
- Full job-listing table

The dashboard reloaded the CSV data when the underlying file changed.

## Results

In the documented demo, the system collected **21 job listings** across categories including software development, AI/ML, marketing, and customer service.

The report found that many of the remote listings were concentrated in the United States. The dashboard made it easier to identify patterns such as which locations had the most listings, which companies were hiring, and what types of jobs were available.

## Team Responsibilities

According to the project report:

- Kabir handled the scraper and dashboard coding.
- Nathan tested the script and made adjustments to the dashboard.
- Brett handled the presentation and report and also tested the code.

## Limitations and Future Improvements

The report identified several limitations:

- Location data was not always precise.
- The project depended on the availability and structure of the external API.

Potential future improvements included:

- Adding more dashboard filters
- Storing collected data in a database
- Automatically refreshing job data

## Relationship to This Repository

This companion project is relevant because it represents a natural extension of the same core scripting concepts demonstrated by the primary project:

- HTTP-based data collection
- Structured data extraction
- Data cleaning and transformation
- Persistent output
- Automation

The two projects also demonstrate different approaches to the same general problem. The primary repository project focuses on HTML parsing and SQL integration, while this project focused on API-based collection and interactive visualization.
