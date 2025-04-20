

import os
import glob
import sys
import pandas as pd
from loguru import logger
import sqlalchemy as sql
sys.path.append(os.path.dirname(__file__))
from data_generator import simulate_all
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = sql.create_engine(DATABASE_URL, echo=True)



N_TABLES       = 10
N_DAYS         = 365
N_MENU_ITEMS   = 50
N_NFC          = 100
N_TRANSACTIONS = 300
N_CAMPAIGNS    = 5

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

logger.info("Starting data generation…")
dfs = simulate_all(
    n_tables=N_TABLES,
    n_days=N_DAYS,
    n_menu_items=N_MENU_ITEMS,
    n_nfc=N_NFC,
    n_tx=N_TRANSACTIONS,
    n_campaigns=N_CAMPAIGNS
)

logger.info("Saving the data to csv files")
for table_name, df in dfs.items():
    csv_path = os.path.join(DATA_DIR, f"{table_name}.csv")
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} rows to {csv_path}")


logger.info("Load the csv files into the tables")
def load_csv_to_table(table_name: str, csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Loaded {len(df)} rows into table '{table_name}'")


logger.info("Beginning data ingestion into database…")
csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
for file_path in csv_files:
    table = os.path.splitext(os.path.basename(file_path))[0]
    try:
        load_csv_to_table(table, file_path)
    except Exception as e:
        logger.error(f"Failed to load {table} from {file_path}: {e}")

logger.info("ETL process complete. All tables populated.")