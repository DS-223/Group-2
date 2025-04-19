

import os
import sys
from loguru import logger

sys.path.append(os.path.dirname(__file__))


from data_generator import simulate_all

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

for table_name, df in dfs.items():
    csv_path = os.path.join(DATA_DIR, f"{table_name}.csv")
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved {len(df)} rows to {csv_path}")

