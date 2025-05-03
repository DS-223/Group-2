# menu_recommendations_pipeline.py

from typing import Optional
import requests
import pandas as pd
from datetime import datetime, time

API_BASE             = "http://api:8000/api"
TXNS_ENDPOINT        = f"{API_BASE}/transactions/"
TXN_ITEMS_ENDPOINT   = f"{API_BASE}/fact_transaction_items/"
DAYTIMES_ENDPOINT    = f"{API_BASE}/dim_menu_daytimes/"
MENU_RECS_ENDPOINT   = f"{API_BASE}/menu_recommendations/"

def run_menu_recommendations():
    # 1) Fetch data from your APIs
    txns      = requests.get(TXNS_ENDPOINT).json()
    items     = requests.get(TXN_ITEMS_ENDPOINT).json()
    daytimes  = requests.get(DAYTIMES_ENDPOINT).json()

    df_txns     = pd.DataFrame(txns)
    df_items    = pd.DataFrame(items)
    df_daytimes = pd.DataFrame(daytimes)

    # 2) Parse timestamps and times
    df_txns["created_at"]     = pd.to_datetime(df_txns["created_at"])
    df_daytimes["start_time"] = pd.to_datetime(df_daytimes["start_time"], format="%H:%M:%S").dt.time
    df_daytimes["end_time"] = pd.to_datetime(df_daytimes["end_time"], format="%H:%M:%S").dt.time

    # 3) Join transactions ⇆ items
    df = (
        df_items
          .merge(
             df_txns[["transaction_id", "created_at"]],
             on="transaction_id",
             how="inner"
          )
    )
    df["order_time"] = df["created_at"].dt.time

    # 4) Assign each sale to a daytime slot
    def assign_daytime_slot(t: time) -> Optional[int]:
        """
        Return the daytime_id whose start_time ≤ t ≤ end_time,
        or None if no slot matches.
        """
        for _, row in df_daytimes.iterrows():
            if row["start_time"] <= t <= row["end_time"]:
                return row["daytime_id"]
        return None

    df["daytime_id"] = df["order_time"].apply(assign_daytime_slot)
    df = df.dropna(subset=["daytime_id"])  # drop sales outside defined slots

    # 5) Aggregate popularity per slot + item
    popularity = (
        df.groupby(["daytime_id", "item_id"])
          .agg(total_sold=("quantity", "sum"))
          .reset_index()
    )

    # 6) For each slot, pick & rank top 5 items and POST to your API
    failures = []
    for dt in popularity["daytime_id"].unique():
        top5 = (
            popularity[popularity["daytime_id"] == dt]
              .sort_values("total_sold", ascending=False)
              .head(5)
              .reset_index(drop=True)
        )
        for rank, row in top5.iterrows():
            payload = {
                "menu_item_id": int(row["item_id"]),
                "daytime_id":   int(dt),
                "rank":         int(rank + 1)
            }
            resp = requests.post(MENU_RECS_ENDPOINT, json=payload)
            if not resp.ok:
                failures.append((dt, row["item_id"], resp.status_code, resp.text))

    print(f"✅ Uploaded {len(popularity['daytime_id'].unique())*5 - len(failures)} recommendations.")
    if failures:
        print("❌ Failures:")
        for f in failures:
            print("  slot:", f[0], "item:", f[1], "→", f[2], f[3])

    print("Done.")

# ✅ Allow direct script execution too
if __name__ == "__main__":
    run_menu_recommendations()
