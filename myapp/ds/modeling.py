import pandas as pd

def rfm_score_segment_fast(df):
    """
    Fast version of RFM scoring & segmentation.
    Assumes df has columns: recency_days, frequency, monetary
    """

    # Use rank directly and bin using quantiles without apply
    df['R_rank'] = df['recency_days'].rank(method='first', ascending=True)
    df['F_rank'] = df['frequency'].rank(method='first', ascending=False)
    df['M_rank'] = df['monetary'].rank(method='first', ascending=False)

    df['R_score'] = pd.qcut(df['R_rank'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    df['F_score'] = pd.qcut(df['F_rank'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    df['M_score'] = pd.qcut(df['M_rank'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

    df['RFM_score'] = df['R_score'].astype(str) + df['F_score'].astype(str) + df['M_score'].astype(str)

    # Faster vectorized segmentation
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

rfm_df = pd.read_csv("rfm.csv")


rfm_result = rfm_score_segment_fast(rfm_df)

# Preview
print(rfm_result.head())