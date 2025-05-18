# Frontend – Streamlit App (SmartCRM)

The frontend of SmartCRM is built with Streamlit and serves as the main user interface for interacting with the CRM data. It allows restaurant and cafe managers to explore sales, customer behavior, NFC usage, and campaign performance—all in a visual, interactive format.

---

## 🎯 Purpose

- Provide visual analytics and KPIs to decision-makers
- Interact with the FastAPI backend to fetch real-time business data
- Serve as the MVP interface for campaign management and menu recommendations

---

## 🚀 Features

| Section                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Dashboard**          | Sales overview, top items, sales trends, NFC engagement, table usage       |
| **Customer Segments**  | RFM segmentation analysis, loyalty & recency visualizations                 |
| **Campaign Management**| View and track campaigns by target segment and duration                     |
| **Menu Recommendation**| Recommend food items based on time of day using backend-generated logic     |

---

## 🛠️ Architecture

- Communicates with the FastAPI backend through `requests.get()` to `/api/...`
- Merges and preprocesses the data client-side using `pandas`
- Visualized using `altair` charts and interactive Streamlit components
- Session-state driven page routing via Streamlit sidebar

---

## 📂 Files

| File        | Purpose                                      |
|-------------|----------------------------------------------|
| `app.py`    | Main Streamlit app; handles UI logic         |
| `Dockerfile`| Container for deploying the Streamlit UI     |
| `requirements.txt` | Dependencies for running the app     |

---

## 🧪 How It Works

1. On launch, the app fetches data from these endpoints:
   - `/api/dim_menu_items/`
   - `/api/transactions/`
   - `/api/dashboard/overview`
   - `/api/rfm_segments/`
   - etc.

2. Merges data in memory using `pandas`

3. Renders:
   - `st.metric()` for KPIs
   - `alt.Chart()` for line and bar charts
   - `st.dataframe()` for detailed views

4. Navigation handled by `st.sidebar.button()` → tracks `st.session_state["section"]`

---

## 📦 Deployment (Docker)

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

--

docker build -t smartcrm-frontend .
docker run -p 8501:8501 smartcrm-frontend
