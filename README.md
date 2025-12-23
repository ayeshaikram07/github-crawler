# GitHub Repository Data Crawler (Python)

## Overview

This repository implements a **Python-based GitHub data crawling system** designed to collect repository metadata at scale using the **GitHub GraphQL API**, persist it in **PostgreSQL**, and export structured datasets for downstream usage.
The project focuses on **data ingestion architecture**, **repeatable execution**, and **scalability-first design**, intentionally keeping the scope limited to core system foundations.

## System Architecture

```
GitHub GraphQL API
        ↓
Python Crawling Engine
        ↓
PostgreSQL Database
        ↓
CSV / JSON Structured Outputs
```

Each layer is isolated, allowing independent scaling, replacement, or automation without redesigning the system.

## Technology Stack

* **Python 3.10**
* **GitHub GraphQL API**
* **PostgreSQL**
* **psycopg2** – database connectivity
* **pandas** – data transformation & export
* **python-dotenv** – environment configuration

## Project Structure

```
github-crawler/
│
├── crawl_github_stars.py      # Core crawling logic
├── .env                      # Environment variables (not committed)
├── requirements.txt          # Python dependencies
│
├── repos_data.csv             # Exported CSV output
├── repos_data.json            # Exported JSON output
│
├── README.md                  # Project documentation
```

---

## Database Schema

### `repos` Table

Stores the latest snapshot of repository metadata.

| Column       | Description           |
| ------------ | --------------------- |
| id           | Primary key           |
| repo_name    | Repository name       |
| owner        | Repository owner      |
| stars        | Stargazer count       |
| last_updated | Last update timestamp |

---

### `crawl_jobs` Table

Tracks crawl execution lifecycle for observability.

| Column      | Description             |
| ----------- | ----------------------- |
| id          | Crawl job ID            |
| started_at  | Crawl start time        |
| finished_at | Crawl end time          |
| status      | Success / Failed        |
| records     | Total records processed |

---

## Execution Flow

1. Environment variables are loaded securely
2. PostgreSQL connection is initialized
3. A crawl job is registered as **Running**
4. GitHub repositories are fetched using paginated GraphQL queries
5. Repository data is inserted or updated atomically
6. Crawl job status is finalized
7. Data is exported into CSV and JSON formats

This ensures **data consistency**, **fault tolerance**, and **repeatable execution**.

---

## GitHub API Strategy

* Uses **GraphQL** for efficient data retrieval
* Pagination handles large datasets safely
* Rate limiting is respected via controlled delays
* Queries are parameterized for flexibility

Current execution limit is **1,000 repositories**, configurable via constants.

---

## Sample Outputs

### PostgreSQL (`repos` table)

```
id | repo_name  | owner     | stars  | last_updated
----------------------------------------------------
1  | react      | facebook  | 220000 | 2025-01-10
2  | tensorflow | google    | 185000 | 2025-01-10
3  | next.js    | vercel    | 125000 | 2025-01-10
```

---

### JSON Output (excerpt)

```json
[
  {
    "repo_name": "react",
    "owner": "facebook",
    "stars": 220000
  },
  {
    "repo_name": "tensorflow",
    "owner": "google",
    "stars": 185000
  }
]
```

---

### CSV Output (excerpt)

```
repo_name,owner,stars
react,facebook,220000
tensorflow,google,185000
next.js,vercel,125000
```

---

## Scalability Design

Although executed with a controlled dataset, the system is designed to scale naturally:

* Pagination already supports millions of records
* PostgreSQL schema supports large datasets
* Crawl job tracking enables scheduling and retries
* Output formats integrate with analytics, BI, and ML pipelines

Scaling primarily involves increasing limits or introducing parallel workers—no architectural changes required.

---

## Automation & Extension Potential

This foundation supports:

* Scheduled crawlers
* Autonomous data collection agents
* Dataset generation pipelines
* Market intelligence systems
* AI/ML data ingestion workflows

The crawler is a **system component**, not a one-off script.

---

## Scope Clarification

✔ Data crawling
✔ Database persistence
✔ Structured exports
✔ Execution tracking
The emphasis is on **engineering fundamentals and system thinking**.
---

## Summary

This repository demonstrates:
* Clean data ingestion architecture
* Reliable persistence and observability
* Scalable system design
* Strong foundations for automation and analytics

---


