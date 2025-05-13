"""
ETL Process: Generate synthetic data and load directly into database using SQLAlchemy models.
"""

import os
import sys
from loguru import logger
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Set up paths and imports
sys.path.append(os.path.dirname(__file__)) ####### DONT FORGET __file__ IN CASE of COPY  PASTE
from data_generator import simulate_all

# 👇 Import your models & DB session
from database import SessionLocal
import models

# 🔑 Load DB connection string
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

# === Parameters ===
N_TABLES       = 10
N_DAYS         = 365
N_MENU_ITEMS   = 50
N_USERS        = 100
N_NFC          = 100
N_TRANSACTIONS = 300
N_CAMPAIGNS    = 5

# === Start Data Generation ===
logger.info("Starting data generation…")
dfs = simulate_all(
    n_tables=N_TABLES,
    n_days=N_DAYS,
    n_menu_items=N_MENU_ITEMS,
    n_nfc=N_NFC,
    n_tx=N_TRANSACTIONS,
    n_campaigns=N_CAMPAIGNS
)
# === ORM-based data loader ===
def load_data():
    """
    Loads synthetic data into the database using SQLAlchemy ORM models.

    This function:
    - Converts pandas DataFrames into SQLAlchemy model objects
    - Performs bulk inserts for each table
    - Commits the session or rolls back on failure
    """
    logger.info("Starting data loading using SQLAlchemy models…")
    db: Session = SessionLocal()

    try:
        # --- Load dim_users ---
        users = [models.DimUser(**row) for row in dfs["dim_users"].to_dict(orient="records")]
        db.bulk_save_objects(users)
        logger.info(f"Inserted {len(users)} rows into dim_users")

        # --- Load dim_tables ---
        tables = [models.DimTable(**row) for row in dfs["dim_tables"].to_dict(orient="records")]
        db.bulk_save_objects(tables)
        logger.info(f"Inserted {len(tables)} rows into dim_tables")

        # --- Load dim_time ---
        times = [models.DimTime(**row) for row in dfs["dim_time"].to_dict(orient="records")]
        db.bulk_save_objects(times)
        logger.info(f"Inserted {len(times)} rows into dim_time")

        # --- Load dim_menu_items ---
        menu_items = [models.DimMenuItem(**row) for row in dfs["dim_menu_items"].to_dict(orient="records")]
        db.bulk_save_objects(menu_items)
        logger.info(f"Inserted {len(menu_items)} rows into dim_menu_items")

        # --- Load dim_menu_daytimes ---
        daytimes = [models.DimMenuDaytime(**row) for row in dfs["dim_menu_daytimes"].to_dict(orient="records")]
        db.bulk_save_objects(daytimes)
        logger.info(f"Inserted {len(daytimes)} rows into dim_menu_daytimes")

        # --- Load nfc_engagements ---
        engagements = [models.NfcEngagement(**row) for row in dfs["nfc_engagements"].to_dict(orient="records")]
        db.bulk_save_objects(engagements)
        logger.info(f"Inserted {len(engagements)} rows into nfc_engagements")

        # --- Load fact_transactions ---
        transactions = [models.FactTransaction(**row) for row in dfs["fact_transactions"].to_dict(orient="records")]
        db.bulk_save_objects(transactions)
        logger.info(f"Inserted {len(transactions)} rows into fact_transactions")

        # --- Load fact_transaction_items ---
        txn_items = [models.FactTransactionItem(**row) for row in dfs["fact_transaction_items"].to_dict(orient="records")]
        db.bulk_save_objects(txn_items)
        logger.info(f"Inserted {len(txn_items)} rows into fact_transaction_items")

        # --- Load marketing_campaigns ---
        campaigns = [models.MarketingCampaign(**row) for row in dfs["marketing_campaigns"].to_dict(orient="records")]
        db.bulk_save_objects(campaigns)
        logger.info(f"Inserted {len(campaigns)} rows into marketing_campaigns")

        # ✅ COMMIT all
        db.commit()
        logger.info("✅ All data successfully committed to the database.")

    except Exception as e:
        logger.error(f"❌ Error during data loading: {e}")
        db.rollback()
    finally:
        db.close()
        logger.info("Database session closed.")

# === Run loader ===
if __name__ == "__main__":
    load_data()
