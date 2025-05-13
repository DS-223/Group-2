# ETL Service – SmartCRM

The ETL service in SmartCRM is designed to generate synthetic transactional and dimensional data for restaurants and cafes. It prepares all necessary datasets to populate the PostgreSQL database, enabling realistic dashboarding, segmentation, and recommendations.

---

## 🎯 Purpose

- Simulate restaurant operations: orders, users, tables, menu items
- Preload structured data for development, testing, and demo environments
- Ensure consistency between entity relationships (e.g., transactions ↔ items)

---

## 📂 Files

| File                | Description                                                       |
|---------------------|-------------------------------------------------------------------|
| `etl_process.py`    | Main entry point to generate and insert data into PostgreSQL      |
| `data_generator.py` | Contains Faker-powered functions to simulate each entity          |
| `models.py`         | Defines the SQLAlchemy ORM structure for all database tables      |
| `database.py`       | Manages DB session and engine creation                            |
| `Dockerfile`        | Dockerized entry to run the ETL in an isolated environment        |
| `requirements.txt`  | Declares dependencies like `pandas`, `faker`, and `sqlalchemy`    |

---

## 🔄 Pipeline Overview

### 1. Data Simulation (via `data_generator.py`)
- **Menu Items** – Random dish names, prices, categories
- **Tables** – Unique identifiers for physical table slots
- **Users** – Random user IDs and metadata
- **Time** – Full date/time dimension with day/month/year/hour
- **Transactions** – Each with assigned user, table, and timestamp
- **Transaction Items** – Line items per transaction
- **NFC Engagements** – Simulated scans with tag types and timestamps
- **Campaigns** – Mocked marketing campaigns for testing targeting logic

### 2. Insertion Logic (via `etl_process.py`)
- Calls generators from `data_generator.py`
- Inserts records using SQLAlchemy session transactions
- Ensures primary/foreign key relationships are respected
- Creates tables via `Base.metadata.create_all(bind=engine)` if not present

---

## 🧪 How to Run

```bash
python etl_process.py