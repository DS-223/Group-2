import requests
import pandas as pd
from datetime import datetime

API_BASE = "http://api:8000"
RFMS_ENDPOINT = f"{API_BASE}/rfm_segments/"

users = requests.get(f"{API_BASE}/users/").json()
txns  = requests.get(f"{API_BASE}/transactions/").json()

df_users        = pd.DataFrame(users)
df_transactions = pd.DataFrame(txns)
df_transactions["created_at"] = pd.to_datetime(df_transactions["created_at"])

df = df_transactions.merge(df_users, on="mobile_id", how="inner")

rfm_base = (
    df.groupby("mobile_id")
      .agg(
          last_transaction_date=("created_at", "max"),
          frequency=("transaction_id", "nunique"),
          monetary   =("total_amount",     "sum")
      )
      .reset_index()
)
rfm_base["recency_days"] = (
    pd.Timestamp.now().normalize() - rfm_base["last_transaction_date"]
).dt.days

rfm = rfm_base[["mobile_id","recency_days","frequency","monetary"]]

def rfm_score_segment_fast(df):
    df = df.copy()
    df['R_rank'] = df['recency_days'].rank(method='first', ascending=True)
    df['F_rank'] = df['frequency'].rank(method='first', ascending=False)
    df['M_rank'] = df['monetary'].rank(method='first', ascending=False)

    df['R_score'] = pd.qcut(df['R_rank'], 5, labels=[5,4,3,2,1]).astype(int)
    df['F_score'] = pd.qcut(df['F_rank'], 5, labels=[1,2,3,4,5]).astype(int)
    df['M_score'] = pd.qcut(df['M_rank'], 5, labels=[1,2,3,4,5]).astype(int)

    df['RFM_score'] = (
        df['R_score'].astype(str)
      + df['F_score'].astype(str)
      + df['M_score'].astype(str)
    )

    conditions = [
      (df['R_score']>=4)&(df['F_score']>=4),
      (df['R_score']>=3)&(df['F_score']>=3),
      (df['R_score']>=4),
      (df['F_score']>=4)
    ]
    labels = ['Champions','Loyal Customers','Recent Customers','Frequent Buyers']
    df['segment'] = 'Others'
    for cond, lbl in zip(conditions, labels):
        df.loc[cond, 'segment'] = lbl

    return df.drop(columns=['R_rank','F_rank','M_rank'])

rfm_result = rfm_score_segment_fast(rfm)

# 4) Stamp with creation time
now_ts = datetime.utcnow().isoformat()
rfm_result['date_created'] = now_ts

# 5) Push into your rfm_segments API
failures = []
for rec in rfm_result.to_dict(orient="records"):
    resp = requests.post(RFMS_ENDPOINT, json=rec)
    if not resp.ok:
        failures.append((rec['mobile_id'], resp.status_code, resp.text))

print(f"Uploaded {len(rfm_result) - len(failures)} records.")
if failures:
    print("Failures:")
    for fail in failures:
        print(" ", fail)

print('Done')