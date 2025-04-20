from faker import Faker
import pandas as pd
import random
from datetime import datetime
from loguru import logger

# Initialize Faker and Logger
fake = Faker()
logger.add(lambda msg: print(msg), level="INFO")


# --- Data Model Generators ---

def generate_dim_table(table_id: int) -> dict:
    return {
        "table_id": table_id,
        "nfc_wifi_tag": fake.uuid4(),
        "nfc_menu_tag": fake.uuid4(),
        "nfc_review_tag": fake.uuid4()
    }


def generate_dim_time(time_id: int,
                      start_date: datetime = datetime(2024, 1, 1),
                      end_date: datetime = datetime(2024, 12, 31)) -> dict:
    # pick a random day in the year
    rand_day = fake.date_between(start_date=start_date, end_date=end_date)
    return {
        "time_id": time_id,
        "date": rand_day,
        "day_of_week": rand_day.strftime("%A"),
        "month": rand_day.month,
        "year": rand_day.year,
        "is_weekend": rand_day.weekday() >= 5
    }


def generate_dim_menu_item(item_id: int) -> dict:
    categories = [
        "Coffee", "Tea", "Espresso", "Cold Brew", "Juice", "Smoothie",
        "Pastry", "Cake", "Sandwich", "Salad", "Soup", "Breakfast",
        "Snack", "Alcohol", "Non‑Alcoholic", "Specialty"
    ]
    return {
        "item_id": item_id,
        "item_name": fake.word().capitalize(),
        "price": round(random.uniform(1.5, 15.0), 2),
        "category": random.choice(categories)
    }


def generate_nfc_engagement(engagement_id: int) -> dict:
    return {
        "engagement_id": engagement_id,
        "table_id": random.randint(1, 10),
        "tag_type": random.choice(["WiFi", "Menu", "Review"]),
        "mobile_id": fake.uuid4(),
        "engagement_time": fake.date_time_between(start_date="-3M", end_date="now")
    }


def generate_fact_transaction(transaction_id: int) -> dict:
    return {
        "transaction_id": transaction_id,
        "table_id": random.randint(1, 10),
        "time_id": random.randint(1, 365),
        "total_amount": round(random.uniform(5.0, 200.0), 2),
        "created_at": fake.date_time_between(start_date="-3M", end_date="now")
    }


def generate_fact_transaction_item(transaction_id: int, item_id: int) -> dict:
    return {
        "transaction_id": transaction_id,
        "item_id": item_id,
        "quantity": random.randint(1, 4),
        "price": round(random.uniform(1.5, 15.0), 2)
    }


def generate_marketing_campaign(campaign_id: int, max_time_id: int = 365) -> dict:
    start = random.randint(1, max_time_id - 1)
    end = random.randint(start, max_time_id)
    segments = ["High Value", "At Risk", "New", "Promising"]
    return {
        "campaign_id": campaign_id,
        "name": fake.bs().title(),
        "start_time_id": start,
        "end_time_id": end,
        "target_segment": random.choice(segments),
        "description": fake.sentence(nb_words=8)
    }


# --- Orchestrator ---

def simulate_all(
        n_tables: int = 10,
        n_days: int = 365,
        n_menu_items: int = 50,
        n_nfc: int = 100,
        n_tx: int = 300,
        n_campaigns: int = 5
) -> dict[str, pd.DataFrame]:
    # Generate each table
    dim_tables = [generate_dim_table(i) for i in range(1, n_tables + 1)]
    dim_time = [generate_dim_time(i) for i in range(1, n_days + 1)]
    dim_menu = [generate_dim_menu_item(i) for i in range(1, n_menu_items + 1)]
    nfc_events = [generate_nfc_engagement(i) for i in range(1, n_nfc + 1)]
    transactions = [generate_fact_transaction(i) for i in range(1, n_tx + 1)]

    # Transaction ↔ Item bridge
    txn_items = []
    for txn in transactions:
        chosen_items = random.sample(range(1, n_menu_items + 1), random.randint(1, 3))
        for item_id in chosen_items:
            txn_items.append(generate_fact_transaction_item(txn["transaction_id"], item_id))

    campaigns = [generate_marketing_campaign(i, max_time_id=n_days) for i in range(1, n_campaigns + 1)]

    # Convert to DataFrames
    dfs = {
        "dim_tables": pd.DataFrame(dim_tables),
        "dim_time": pd.DataFrame(dim_time),
        "dim_menu_items": pd.DataFrame(dim_menu),
        "nfc_engagements": pd.DataFrame(nfc_events),
        "fact_transactions": pd.DataFrame(transactions),
        "fact_transaction_items": pd.DataFrame(txn_items),
        "marketing_campaigns": pd.DataFrame(campaigns),
    }

    # Log counts
    for name, df in dfs.items():
        logger.info(f"→ {name}: {len(df)} rows")

    return dfs
