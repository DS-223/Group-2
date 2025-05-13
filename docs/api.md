# API Service – SmartCRM

The API service is a FastAPI-based backend that serves as the central data gateway for SmartCRM. It communicates with the PostgreSQL database using SQLAlchemy ORM and provides structured endpoints for accessing transactions, menu data, RFM segments, NFC engagements, and more.

---

## 🚀 Purpose

This service powers the entire analytical dashboard and customer engagement logic by:
- Serving business data to the Streamlit frontend
- Performing aggregations and joins on the fly
- Managing entities like users, campaigns, and segments

---

## 🔌 Endpoints

| Endpoint                             | Method | Description                                      |
|--------------------------------------|--------|--------------------------------------------------|
| `/api/transactions/`                | GET    | Fetch all transaction records                   |
| `/api/fact_transaction_items/`      | GET    | Get item-level data for transactions            |
| `/api/rfm_segments/`                | GET    | Retrieve computed RFM segments                  |
| `/api/rfm_segments/`                | POST   | Create a new RFM segment entry                  |
| `/api/dashboard/overview`           | GET    | Summary metrics: sales, items sold, users       |
| `/api/dashboard/sales_trend`        | GET    | Daily trend of total sales                      |
| `/api/dashboard/nfc_engagement`     | GET    | Count of NFC engagements by tag type            |
| `/api/campaigns/`                   | GET    | Retrieve all campaigns                          |
| `/api/campaigns/`                   | POST   | Create a new campaign                           |
| `/api/recommendations/menu`         | GET    | Menu recommendations based on time of day       |
| `/api/dim_menu_items/`              | GET    | Get all menu items                              |
| `/api/dim_tables/`                  | GET    | Get all tables                                  |
| `/api/dim_time/`                    | GET    | Time dimension reference table                  |
| `/api/nfc_engagements/`             | GET    | Get raw NFC engagement logs                     |
| `/api/auth/login`                   | POST   | Dummy login with static credentials             |

---

## 🧱 Key Components

| File            | Description                                                |
|-----------------|------------------------------------------------------------|
| `main.py`       | Defines all FastAPI routes                                 |
| `crud.py`       | General-purpose database access functions                  |
| `models.py`     | SQLAlchemy ORM models for all database tables              |
| `schemas.py`    | Pydantic validation models used in requests/responses      |
| `database.py`   | DB connection and session setup using SQLAlchemy           |
| `Dockerfile`    | Container configuration for running the API service        |

---

## 🛠️ Example: Dashboard Summary

The `/api/dashboard/overview` endpoint uses SQLAlchemy queries to calculate:
- Total sales from `FactTransaction`
- Total item quantity from `FactTransactionItem`
- Total users from `DimUser`
- Timestamp for `last_updated`

It returns a response like:

```json
{
  "total_sales": 18567.20,
  "total_transactions": 302,
  "total_users": 48,
  "total_items_sold": 954,
  "last_updated": "2025-05-17T14:00:00Z"
}