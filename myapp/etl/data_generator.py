from faker import Faker
import pandas as pd
import random
from datetime import datetime
from loguru import logger

fake = Faker()
logger.add(lambda msg: print(msg), level="INFO")


def generate_dim_user(mobile_id: str) -> dict:
    return {"mobile_id": mobile_id, "notes": ""}



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
    # Realistic menu catalog by category
    menu_catalog = {
        "Coffee": ["Espresso", "Americano", "Cappuccino", "Latte", "Mocha", "Flat White"],
        "Tea": ["Black Tea", "Green Tea", "Herbal Tea", "Oolong Tea", "Chamomile"],
        "Pastry": ["Croissant", "Blueberry Muffin", "Chocolate Donut", "Baklava", "Cherry Tart"],
        "Sandwich": ["Club Sandwich", "Panini", "BLT", "Turkey Wrap", "Grilled Cheese"],
        "Smoothie": ["Strawberry Banana Smoothie", "Green Detox Smoothie", "Mango Lassi"],
        "Juice": ["Orange Juice", "Apple Juice", "Carrot Ginger Juice", "Beetroot Juice"],
        "Salad": ["Caesar Salad", "Greek Salad", "Quinoa Salad", "Caprese Salad"],
        "Soup": ["Tomato Basil Soup", "Chicken Noodle Soup", "Mushroom Soup", "Lentil Soup"],
        "Breakfast": ["Pancakes", "French Toast", "Omelette", "Avocado Toast"],
        "Snack": ["Fruit Bowl", "Yogurt Parfait", "Granola Bar", "Nachos"],
        "Alcohol": ["Red Wine", "White Wine", "Local Beer", "Mojito", "Whiskey Sour"],
        "Non‑Alcoholic": ["Sparkling Water", "Lemonade", "Iced Tea", "Soft Drink"],
        "Specialty": ["Affogato", "Turkish Coffee", "Matcha Latte", "Chai Latte"]
    }

    # Select category and item name
    category = random.choice(list(menu_catalog.keys()))
    item_name = random.choice(menu_catalog[category])

    # Define base price ranges by category
    price_ranges = {
        "Coffee": (2.5, 5.0),
        "Tea": (1.5, 4.0),
        "Pastry": (1.0, 3.5),
        "Sandwich": (4.0, 8.0),
        "Smoothie": (3.5, 6.5),
        "Juice": (2.5, 5.0),
        "Salad": (3.5, 7.0),
        "Soup": (3.0, 6.0),
        "Breakfast": (5.0, 10.0),
        "Snack": (1.0, 4.0),
        "Alcohol": (4.0, 12.0),
        "Non‑Alcoholic": (1.0, 3.0),
        "Specialty": (3.0, 7.0)
    }
    low, high = price_ranges.get(category, (2.0, 6.0))
    price = round(random.uniform(low, high), 2)

    return {
        "item_id": item_id,
        "item_name": item_name,
        "price": price,
        "category": category
    }


def generate_nfc_engagement(engagement_id: int, mobile_pool: list[str]) -> dict:
    return {
        "engagement_id": engagement_id,
        "table_id": random.randint(1, 10),
        "tag_type": random.choice(["WiFi", "Menu", "Review"]),
        "mobile_id": random.choice(mobile_pool),
        "engagement_time": fake.date_time_between(start_date="-3M", end_date="now")
    }


def generate_fact_transaction(transaction_id: int, mobile_pool: list[str]) -> dict:
    return {
        "transaction_id": transaction_id,
        "mobile_id": random.choice(mobile_pool),
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

    campaign_names = [
        "Double Points Week", "Smoothie Sunday", "Happy Hour Promo", "Loyalty Launch",
        "Review & Reward", "VIP Tasting Event", "Menu Discovery Week"
    ]

    descriptions = [
        "Get 2x points on all coffee orders", "Free dessert with lunch combos",
        "Special discounts for new members", "Win-back offer for past visitors",
        "Try our new seasonal menu and earn points"
    ]

    return {
        "campaign_id": campaign_id,
        "name": random.choice(campaign_names),
        "start_time_id": start,
        "end_time_id": end,
        "target_segment": random.choice(segments),
        "description": random.choice(descriptions)
    }



def simulate_all(
        n_tables: int = 10,
        n_days: int = 365,
        n_menu_items: int = 50,
        n_users: int = 100,          # ← new
        n_nfc: int = 100,
        n_tx: int = 300,
        n_campaigns: int = 5
) -> dict[str, pd.DataFrame]:
    # 1) build a shared pool of mobile_ids
    mobile_pool = [fake.uuid4() for _ in range(n_users)]
    dim_users   = [generate_dim_user(m) for m in mobile_pool]

    # 2) generate existing dims
    dim_tables = [generate_dim_table(i) for i in range(1, n_tables + 1)]
    dim_time   = [generate_dim_time(i)  for i in range(1, n_days   + 1)]
    dim_menu   = [generate_dim_menu_item(i) for i in range(1, n_menu_items + 1)]

    # 3) engagements & txs now draw from the same pool
    nfc_events   = [generate_nfc_engagement(i, mobile_pool) for i in range(1, n_nfc + 1)]
    transactions = [generate_fact_transaction(i, mobile_pool)     for i in range(1, n_tx  + 1)]

    # 4) bridge table
    txn_items = []
    for tx in transactions:
        chosen_items = random.sample(range(1, n_menu_items + 1), random.randint(1, 3))
        for item_id in chosen_items:
            txn_items.append(generate_fact_transaction_item(tx["transaction_id"], item_id))

    # 5) campaigns
    campaigns = [generate_marketing_campaign(i, max_time_id=n_days) for i in range(1, n_campaigns + 1)]

    # 6) pack into DataFrames
    dfs = {
        "dim_users":              pd.DataFrame(dim_users),            # ← new
        "dim_tables":             pd.DataFrame(dim_tables),
        "dim_time":               pd.DataFrame(dim_time),
        "dim_menu_items":         pd.DataFrame(dim_menu),
        "nfc_engagements":        pd.DataFrame(nfc_events),
        "fact_transactions":      pd.DataFrame(transactions),
        "fact_transaction_items": pd.DataFrame(txn_items),
        "marketing_campaigns":    pd.DataFrame(campaigns),
    }

    # Log counts
    for name, df in dfs.items():
        logger.info(f"→ {name}: {len(df)} rows")

    return dfs