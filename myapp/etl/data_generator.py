from faker import Faker
import pandas as pd
import random
from datetime import datetime, time
from loguru import logger

fake = Faker()
logger.add(lambda msg: print(msg), level="INFO")


def generate_dim_user(mobile_id: str) -> dict:
    """
    Generate a user record for the dimension table.
    Args:
        mobile_id (str): Unique mobile ID.
    Returns:
        dict: Dictionary with user data.
    """
    return {"mobile_id": mobile_id, "notes": ""}



def generate_dim_table(table_id: int) -> dict:
    """
    Generate a table record with NFC tags.
    Args:
        table_id (int): Unique table ID.
    Returns:
        dict: Dictionary with table data including NFC tags.
    """
    return {
        "table_id": table_id,
        "nfc_wifi_tag": fake.uuid4(),
        "nfc_menu_tag": fake.uuid4(),
        "nfc_review_tag": fake.uuid4()
    }


def generate_dim_time(time_id: int,
                      start_date: datetime = datetime(2024, 1, 1),
                      end_date: datetime = datetime(2024, 12, 31)) -> dict:
    """
    Generate a time dimension record with random date attributes.
    Args:
        time_id (int): Unique time ID.
        start_date (datetime, optional): Start of date range. Defaults to 2024-01-01.
        end_date (datetime, optional): End of date range. Defaults to 2024-12-31.
    Returns:
        dict: Dictionary with time attributes (date, day, month, year, weekend flag).
    """
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
    """
    Generate a menu item record with category, name, and price.
    Args:
        item_id (int): Unique menu item ID.
    Returns:
        dict: Dictionary with menu item details.
    """
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
    category = random.choice(list(menu_catalog.keys()))
    item_name = random.choice(menu_catalog[category])
    price_ranges = {
        "Coffee": (2.5, 5.0), "Tea": (1.5, 4.0), "Pastry": (1.0, 3.5),
        "Sandwich": (4.0, 8.0), "Smoothie": (3.5, 6.5), "Juice": (2.5, 5.0),
        "Salad": (3.5, 7.0), "Soup": (3.0, 6.0), "Breakfast": (5.0, 10.0),
        "Snack": (1.0, 4.0), "Alcohol": (4.0, 12.0), "Non-Alcoholic": (1.0, 3.0),
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
    """
    Generate a random NFC engagement record.
    Args:
        engagement_id (int): Unique engagement ID.
        mobile_pool (list[str]): List of available mobile IDs.
    Returns:
        dict: Dictionary with NFC engagement data.
    """
    return {
        "engagement_id": engagement_id,
        "table_id": random.randint(1, 10),
        "tag_type": random.choice(["WiFi", "Menu", "Review"]),
        "mobile_id": random.choice(mobile_pool),
        "engagement_time": fake.date_time_between(start_date="-3M", end_date="now")
    }


def generate_fact_transaction(transaction_id: int, mobile_pool: list[str]) -> dict:
    """
    Generate a transaction record for the fact table.
    Args:
        transaction_id (int): Unique transaction ID.
        mobile_pool (list[str]): List of available mobile IDs.
    Returns:
        dict: Dictionary with transaction data.
    """
    return {
        "transaction_id": transaction_id,
        "mobile_id": random.choice(mobile_pool),
        "table_id": random.randint(1, 10),
        "time_id": random.randint(1, 365),
        "total_amount": round(random.uniform(5.0, 200.0), 2),
        "created_at": fake.date_time_between(start_date="-3M", end_date="now")
    }


def generate_fact_transaction_item(transaction_id: int, item_id: int) -> dict:
    """
    Generate a transaction item record linking a transaction to menu items.
    Args:
        transaction_id (int): ID of the related transaction.
        item_id (int): ID of the purchased item.
    Returns:
        dict: Dictionary with transaction item data.
    """
    return {
        "transaction_id": transaction_id,
        "item_id": item_id,
        "quantity": random.randint(1, 4),
        "price": round(random.uniform(1.5, 15.0), 2)
    }


def generate_marketing_campaign(campaign_id: int, max_time_id: int = 365) -> dict:
    """
    Generate a marketing campaign record.
    Args:
        campaign_id (int): Unique campaign ID.
        max_time_id (int, optional): Maximum time ID available. Defaults to 365.
    Returns:
        dict: Dictionary with marketing campaign data.
    """
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


def generate_dim_menu_daytimes() -> list[dict]:
    """
    Hard-coded daytime definitions (dim_menu_daytimes).
    """
    return [
        {"daytime_id":  1, "daytime_label": "Early Breakfast",         "start_time": time(4,  0), "end_time": time(6, 29)},
        {"daytime_id":  2, "daytime_label": "Standard Breakfast",      "start_time": time(6, 30), "end_time": time(10,29)},
        {"daytime_id":  3, "daytime_label": "Late Breakfast / Brunch", "start_time": time(10,30),"end_time": time(12,29)},
        {"daytime_id":  4, "daytime_label": "Lunch",                   "start_time": time(12,30),"end_time": time(14,29)},
        {"daytime_id":  5, "daytime_label": "Late Lunch",              "start_time": time(14,30),"end_time": time(16,29)},
        {"daytime_id":  6, "daytime_label": "Afternoon Tea / Snack",   "start_time": time(16,30),"end_time": time(17,59)},
        {"daytime_id":  7, "daytime_label": "Early Dinner",            "start_time": time(18, 0), "end_time": time(19,29)},
        {"daytime_id":  8, "daytime_label": "Standard Dinner",         "start_time": time(19,30),"end_time": time(21,29)},
        {"daytime_id":  9, "daytime_label": "Late Dinner / Supper",    "start_time": time(21,30),"end_time": time(23,59)},
        {"daytime_id": 10, "daytime_label": "Midnight Snack",          "start_time": time(0,  0), "end_time": time(1, 59)},
        {"daytime_id": 11, "daytime_label": "Closed / No Service",     "start_time": time(2,  0), "end_time": time(3, 59)},
    ]


def simulate_all(
        n_tables: int = 10,
        n_days: int = 365,
        n_menu_items: int = 50,
        n_users: int = 100,
        n_nfc: int = 100,
        n_tx: int = 300,
        n_campaigns: int = 5
) -> dict[str, pd.DataFrame]:
    """
    Simulate the entire database with generated data.
    Args:
        n_tables (int, optional): Number of tables to generate. Defaults to 10.
        n_days (int, optional): Number of days for the time dimension. Defaults to 365.
        n_menu_items (int, optional): Number of menu items to generate. Defaults to 50.
        n_users (int, optional): Number of mobile users to generate. Defaults to 100.
        n_nfc (int, optional): Number of NFC engagement events. Defaults to 100.
        n_tx (int, optional): Number of transactions to generate. Defaults to 300.
        n_campaigns (int, optional): Number of marketing campaigns to generate. Defaults to 5.
    Returns:
        dict[str, pd.DataFrame]: Dictionary of DataFrames for each table.
    """
    # 1) build a shared pool of mobile_ids
    mobile_pool = [fake.uuid4() for _ in range(n_users)]
    dim_users   = [generate_dim_user(m) for m in mobile_pool]

    # 2) dims
    dim_tables  = [generate_dim_table(i) for i in range(1, n_tables + 1)]
    dim_time    = [generate_dim_time(i)  for i in range(1, n_days   + 1)]
    dim_menu    = [generate_dim_menu_item(i) for i in range(1, n_menu_items + 1)]
    dim_daytimes = generate_dim_menu_daytimes()

    # 3) interactions & transactions
    nfc_events   = [generate_nfc_engagement(i, mobile_pool) for i in range(1, n_nfc + 1)]
    transactions = [generate_fact_transaction(i, mobile_pool)     for i in range(1, n_tx  + 1)]

    # 4) bridge table
    txn_items = []
    for tx in transactions:
        for item_id in random.sample(range(1, n_menu_items + 1), random.randint(1, 3)):
            txn_items.append(generate_fact_transaction_item(tx["transaction_id"], item_id))

    # 5) campaigns
    campaigns = [generate_marketing_campaign(i, max_time_id=n_days) for i in range(1, n_campaigns + 1)]

    # 6) pack into DataFrames
    dfs = {
        "dim_users":              pd.DataFrame(dim_users),
        "dim_tables":             pd.DataFrame(dim_tables),
        "dim_time":               pd.DataFrame(dim_time),
        "dim_menu_items":         pd.DataFrame(dim_menu),
        "dim_menu_daytimes":      pd.DataFrame(dim_daytimes),
        "nfc_engagements":        pd.DataFrame(nfc_events),
        "fact_transactions":      pd.DataFrame(transactions),
        "fact_transaction_items": pd.DataFrame(txn_items),
        "marketing_campaigns":    pd.DataFrame(campaigns),
    }

    # Log counts
    for name, df in dfs.items():
        logger.info(f"→ {name}: {len(df)} rows")

    return dfs
