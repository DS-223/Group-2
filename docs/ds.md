# Data Science & Analytics – SmartCRM

This module contains the analytical logic behind SmartCRM's intelligence layer. It includes customer segmentation using RFM scoring and menu item recommendations based on order history and time-of-day behavior. These analytics enable targeted marketing, loyalty tracking, and dynamic personalization.

---

## 🎯 Goals

- Classify customers into behavioral segments using RFM (Recency, Frequency, Monetary)
- Recommend high-performing menu items per time window
- Lay the foundation for future machine learning–based personalization

---

## 📂 Code Structure

| File               | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| `modeling.py`      | RFM segmentation pipeline: scoring, labeling, export                 |
| `recomendation.py` | Popular item recommendation logic by daytime                         |
| `main.py`          | Entrypoint for running DS workflows and writing results to database  |

---

## 🧩 RFM Segmentation

RFM analysis is a marketing technique used to rank and segment customers based on:
- **Recency**: How long ago the customer last made a purchase
- **Frequency**: How often they make purchases
- **Monetary**: How much they spend in total

### Steps:
1. **Aggregate Data**:
   - Group transactions by `mobile_id` (customer)
   - Calculate `recency_days`, `frequency`, and `monetary`

2. **Score Customers**:
   - Use quantile-based binning (1 = low, 5 = high)
   - Combine scores to form composite segment IDs

3. **Label Segments**:
   - Mapping score combinations to labels like:
     - Champions
     - Loyal Customers
     - Need Attention
     - At Risk

### Output Columns:
- `mobile_id`
- `recency_days`
- `frequency`
- `monetary`
- `segment` (text label)

These are stored in the `rfm_segments` table and made available through the API.

---

## 🍽️ Menu Item Recommendation

SmartCRM recommends food and drink items to customers depending on the **time of day**. The system uses historical ordering behavior to suggest the most popular and relevant items.

### Time Segments (Dayparts):
| ID | Label                   | Time Window     |
|----|--------------------------|-----------------|
| 1  | Early Breakfast          | 04:00–06:29     |
| 4  | Lunch                    | 12:30–14:29     |
| 8  | Standard Dinner          | 19:30–21:29     |
... (and more defined in the system)

### Logic:

1. Load all historical transaction items
2. For each `daytime_id`, find the top `N` items by frequency
3. Store ranked list in `menu_recommendation` table

### Output Columns:
- `daytime_id`
- `menu_item_id`
- `rank` (1 = most recommended)
- `created_at`

This data is consumed in the frontend to show personalized menu items per time slot.

---

## 🔄 Data Flow Summary

Transactions → Grouped via pandas → RFM segments → API
→ Grouped by daytime  → Menu rankings → API

---

## 📈 Future Extensions

- Integrate user-level collaborative filtering for personalized menu recs
- Cluster customers using unsupervised models beyond RFM
- Add time-series trend analysis for menu and customer metrics
- Introduce model retraining pipelines for ongoing learning

---

## 🧠 Notes

- Data pipelines are built using pandas and SQLAlchemy
- Results are inserted into the database via ORM and served via API
- Designed to be reproducible and containerized for testing and deployment

---
