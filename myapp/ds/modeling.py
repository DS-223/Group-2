import requests
import pandas as pd

API_BASE = "http://api:8000"

# Fetch users
users = requests.get(f"{API_BASE}/users/").json()
df_users = pd.DataFrame(users)

# Fetch transactions
transactions = requests.get(f"{API_BASE}/transactions/").json()
df_transactions = pd.DataFrame(transactions)
# print('users', users, 'transactions', transactions)
# Ensure datetime

df_transactions["created_at"] = pd.to_datetime(df_transactions["created_at"])

# Join on mobile_id
df = df_transactions.merge(df_users, on="mobile_id", how="inner")

# RFM base calculation
rfm_base = (
    df.groupby("mobile_id")
    .agg(
        last_transaction_date=("created_at", "max"),
        frequency=("transaction_id", "nunique"),
        monetary=("total_amount", "sum")
    )
    .reset_index()
)

rfm_base["recency_days"] = (pd.Timestamp.now().normalize() - rfm_base["last_transaction_date"]).dt.days

rfm = rfm_base[["mobile_id", "recency_days", "frequency", "monetary"]].sort_values(
    by=["recency_days", "frequency", "monetary"], ascending=[True, False, False]
)

# ============================
# RFM Scoring & Segmentation
# ============================

def rfm_score_segment_fast(df):
    df['R_rank'] = df['recency_days'].rank(method='first', ascending=True)
    df['F_rank'] = df['frequency'].rank(method='first', ascending=False)
    df['M_rank'] = df['monetary'].rank(method='first', ascending=False)

    df['R_score'] = pd.qcut(df['R_rank'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    df['F_score'] = pd.qcut(df['F_rank'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    df['M_score'] = pd.qcut(df['M_rank'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

    df['RFM_score'] = df['R_score'].astype(str) + df['F_score'].astype(str) + df['M_score'].astype(str)

    conditions = [
        (df['R_score'] >= 4) & (df['F_score'] >= 4),
        (df['R_score'] >= 3) & (df['F_score'] >= 3),
        (df['R_score'] >= 4),
        (df['F_score'] >= 4)
    ]
    segments = ['Champions', 'Loyal Customers', 'Recent Customers', 'Frequent Buyers']
    df['Segment'] = pd.Series('Others', index=df.index)
    for cond, label in zip(conditions, segments):
        df.loc[cond, 'Segment'] = label

    return df.drop(columns=['R_rank', 'F_rank', 'M_rank'])

rfm_result = rfm_score_segment_fast(rfm)


print(rfm_result.head())