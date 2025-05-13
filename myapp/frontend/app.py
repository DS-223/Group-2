import streamlit as st
import pandas as pd
import altair as alt
import requests

API_BASE = "http://api:8000/api"

st.set_page_config(page_title="SmartCRM", layout="wide")
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>
        <span style="color:#888888;">Smart</span><span style="color:#EA4335;">C</span><span style="color:#FBBC05;">R</span><span style="color:#4285F4;">M</span>
        </h1>
        <h3 style="color:#555555;">Analytical Platform for Restaurants and Cafes</h3>
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    }
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #2C2C2C;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #EAF1FB;
        padding: 1em;
        border-radius: 10px;
        color: #1a3b6d;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    menu = pd.DataFrame(requests.get(f"{API_BASE}/dim_menu_items/").json())
    tables = pd.DataFrame(requests.get(f"{API_BASE}/dim_tables/").json())
    time_df = pd.DataFrame(requests.get(f"{API_BASE}/dim_time/").json())
    trans_items = pd.DataFrame(requests.get(f"{API_BASE}/fact_transaction_items/").json())
    trans = pd.DataFrame(requests.get(f"{API_BASE}/transactions/").json())
    campaigns = pd.DataFrame(requests.get(f"{API_BASE}/campaigns/").json())
    nfc = pd.DataFrame(requests.get(f"{API_BASE}/nfc_engagements/").json())

    rfm_segments = pd.DataFrame(requests.get(f"{API_BASE}/rfm_segments/").json())
    menu_recs = pd.DataFrame(requests.get(f"{API_BASE}/menu_recommendations/").json())

    return menu, tables, time_df, trans_items, trans, campaigns, nfc, rfm_segments, menu_recs


menu, tables, time_df, trans_items, trans, campaigns, nfc, rfm_segments, menu_recs = load_data()




trans = trans.merge(time_df, on="time_id", how="left")
trans["month"] = pd.to_numeric(trans["month"], errors="coerce")

st.sidebar.markdown("## Navigation")

if st.sidebar.button("Dashboard"):
    st.session_state.section = "Dashboard"
if st.sidebar.button("Customer Segments"):
    st.session_state.section = "Customer Segments"
if st.sidebar.button("Campaign Management"):
    st.session_state.section = "Campaign Management"
if st.sidebar.button("Menu Recommendation"):
    st.session_state.section = "Menu Recommendation"

if "section" not in st.session_state:
    st.session_state.section = "Dashboard"

section = st.session_state.section

# ============================= DASHBOARD =======================================
if section == "Dashboard":
    st.markdown("<h2 style='font-family: Georgia, serif;'>Reporting and Analysis</h2>", unsafe_allow_html=True)

    month_map = {i: name for i, name in enumerate([
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ], start=1)}

    available_months = sorted(trans["month"].dropna().unique().astype(int))
    month_names = [month_map[m] for m in available_months]

    selected_name = st.selectbox("Select Month", month_names)
    selected_month = next((k for k, v in month_map.items() if v == selected_name), None)
    month_data = trans[trans["month"] == selected_month]

    st.markdown(f"<h3 style='font-family: Georgia, serif;'>Overview – {selected_name}</h3>", unsafe_allow_html=True)

    total_sales = month_data["total_amount"].sum()
    num_transactions = month_data["transaction_id"].nunique()
    avg_check = month_data["total_amount"].mean()

    top_items = trans_items.merge(menu[["item_id", "menu_item_name"]], on="item_id", how="left")
    top_items = top_items.merge(trans[["transaction_id", "month"]], on="transaction_id")
    top_items = top_items[top_items["month"] == selected_month]
    top_items_grouped = top_items.groupby("menu_item_name")["quantity"].sum().sort_values(ascending=False).head(3)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.0f}")
    with col2:
        st.metric("Transactions", f"{num_transactions:,}")
    with col3:
        st.metric("Avg Check", f"${avg_check:,.2f}")
    with col4:
        st.markdown("**Top Menu Items:**")
        for item in top_items_grouped.index:
            st.markdown(f"- {item}")

    st.markdown(f"<h3 style='font-family: Georgia, serif;'>Sales Trend & Engagement – {selected_name}</h3>",
                unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        daily_sales = month_data.groupby("date")["total_amount"].sum().reset_index()
        if not daily_sales.empty:
            chart = alt.Chart(daily_sales).mark_line().encode(
                x='date:T', y='total_amount:Q'
            ).properties(title=f"{selected_name} – Sales Trend")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f"No sales data for {selected_name}.")

    with col6:
        nfc_filtered = nfc.copy()
        nfc_filtered["engagement_date"] = pd.to_datetime(nfc_filtered["engagement_time"], errors="coerce")
        nfc_filtered = nfc_filtered[nfc_filtered["engagement_date"].dt.month == selected_month]
        nfc_filtered["engagement_hour"] = nfc_filtered["engagement_date"].dt.hour
        engagement_by_hour = nfc_filtered["engagement_hour"].value_counts().sort_index().reset_index()
        engagement_by_hour.columns = ["hour", "count"]
        if not engagement_by_hour.empty:
            chart = alt.Chart(engagement_by_hour).mark_line().encode(
                x='hour:O', y='count:Q'
            ).properties(title="Hourly NFC Engagement")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No NFC engagement data for selected month.")

    st.markdown("<h3 style='font-family: Georgia, serif;'>Menu Performance & Monthly Sales</h3>",
                unsafe_allow_html=True)
    perf = trans_items.merge(menu[["item_id", "menu_item_name"]], on="item_id", how="left")
    perf = perf.merge(trans[["transaction_id", "month"]], on="transaction_id", how="left")
    perf = perf[perf["month"] == selected_month]
    perf["total_price"] = perf["price"] * perf["quantity"]
    menu_summary = perf.groupby("menu_item_name").agg(
        Total_Sales=pd.NamedAgg(column="total_price", aggfunc="sum"),
        Avg_Price=pd.NamedAgg(column="price", aggfunc="mean")
    ).sort_values("Total_Sales", ascending=False).reset_index()

    monthly_sales = trans.groupby("month")["total_amount"].sum().reset_index()

    col7, col8 = st.columns([1.5, 1])
    with col7:
        st.dataframe(menu_summary.style.format({"Total_Sales": "${:,.0f}", "Avg_Price": "${:,.2f}"}))
    with col8:
        chart = alt.Chart(monthly_sales).mark_bar().encode(
            x=alt.X('month:O', title="Month"),
            y=alt.Y('total_amount:Q', title="Total Sales")
        ).properties(title="Monthly Sales")
        st.altair_chart(chart, use_container_width=True)

    st.markdown("<h3 style='font-family: Georgia, serif;'>Campaign Analytics & Table Utilization</h3>",
                unsafe_allow_html=True)
    col9, col10 = st.columns(2)
    with col9:
        if not daily_sales.empty:
            chart = alt.Chart(daily_sales).mark_line().encode(
                x='date:T', y='total_amount:Q'
            ).properties(title=f"{selected_name} – Campaign Trend")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f"No campaign data for {selected_name}.")

    with col10:
        table_usage = month_data["table_id"].value_counts().reset_index()
        table_usage.columns = ["table_id", "count"]
        if not table_usage.empty:
            chart = alt.Chart(table_usage).mark_bar().encode(
                x='table_id:N', y='count:Q'
            ).properties(title="Table Utilization")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No table usage data.")

    st.markdown("<h3 style='font-family: Georgia, serif;'>NFC Engagement Breakdown</h3>", unsafe_allow_html=True)
    if not nfc.empty:
        tag_counts = nfc["tag_type"].value_counts().reset_index()
        tag_counts.columns = ["tag_type", "count"]
        chart = alt.Chart(tag_counts).mark_bar().encode(
            x='tag_type:N', y='count:Q'
        ).properties(title="NFC Tag Engagement")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No NFC tag engagement data.")

# ============================ CUSTOMER SEGMENTS ================================
elif section == "Customer Segments":
    st.markdown("<h2 style='font-family: Georgia, serif;'>Customer Segmentation (RFM)</h2>", unsafe_allow_html=True)
    if not rfm_segments.empty:
        st.dataframe(rfm_segments)
    else:
        st.warning("No RFM segmentation data available.")

    with st.expander("📈 Frequency vs Monetary Value"):
        st.markdown("This scatter plot shows customer loyalty (frequency) vs. spending behavior (monetary value).")
        chart = alt.Chart(rfm_segments).mark_circle(
            size=80,
            color="#EA4335",
            opacity=0.6
        ).encode(
            x=alt.X("frequency:Q", title="Transaction Count"),
            y=alt.Y("monetary:Q", title="Total Spend ($)"),
            tooltip=["mobile_id", "frequency", "monetary", "segment"]
        ).properties(
            width=700,
            height=400,
            title="Customer Loyalty vs Revenue"
        )
        st.altair_chart(chart, use_container_width=True)

    with st.expander("🕓 Recency Distribution"):
        st.markdown("Shows how many days have passed since each customer’s last transaction.")
        chart = alt.Chart(rfm_segments).mark_bar(
            color="#4285F4"
        ).encode(
            x=alt.X("recency_days:Q", bin=alt.Bin(maxbins=20), title="Recency (Days Ago)"),
            y=alt.Y("count()", title="Number of Customers"),
            tooltip=["recency_days"]
        ).properties(
            width=700,
            height=300,
            title="How Recently Do Customers Return?"
        )
        st.altair_chart(chart, use_container_width=True)



# ============================= CAMPAIGNS ========================================
elif section == "Campaign Management":
    st.markdown("<h2 style='font-family: Georgia, serif;'>Campaign Management </h2>", unsafe_allow_html=True)

    if not campaigns.empty:
        st.dataframe(campaigns)

        st.markdown("### Campaigns by Target Segment")
        seg_chart = alt.Chart(campaigns).mark_bar(color="#4285F4").encode(
            x=alt.X("target_segment:N", title="Target Segment", axis=alt.Axis(labelAngle=45)),
            y=alt.Y("count():Q", title="Number of Campaigns"),
            tooltip=["target_segment", "count()"]
        ).properties(
            width=600,
            height=300
        )
        st.altair_chart(seg_chart, use_container_width=True)

        st.markdown("### Campaign Duration")
        campaigns["duration"] = campaigns["end_time_id"] - campaigns["start_time_id"]
        duration_chart = alt.Chart(campaigns).mark_bar(color="#EA4335").encode(
            x=alt.X("name:N", sort="-y", title="Campaign Name",axis=alt.Axis(labelAngle=45)),
            y=alt.Y("duration:Q", title="Duration (Time Units)"),
            tooltip=["name", "duration"]
        ).properties(
            width=700,
            height=300
        )
        st.altair_chart(duration_chart, use_container_width=True)


    else:
        st.warning("No campaigns data available.")

# ======================== MENU ITEM RECOMMENDATION =============================
elif section == "Menu Recommendation":
    st.markdown("<h2 style='font-family: Georgia, serif;'>🍽️ Menu Item Recommendation</h2>", unsafe_allow_html=True)

    if menu_recs.empty or menu.empty:
        st.warning("No menu recommendations available.")
    else:
        # Daytime display names
        daytime_map = {
            1: "🌅 Early Breakfast (04:00–06:29)",
            2: "🍳 Standard Breakfast (06:30–10:29)",
            3: "🥞 Late Breakfast / Brunch (10:30–12:29)",
            4: "🥪 Lunch (12:30–14:29)",
            5: "🫖 Late Lunch (14:30–16:29)",
            6: "🍰 Afternoon Tea / Snack (16:30–17:59)",
            7: "🍝 Early Dinner (18:00–19:29)",
            8: "🥩 Standard Dinner (19:30–21:29)",
            9: "🍣 Late Dinner / Supper (21:30–23:59)",
            10: "🌙 Midnight Snack (00:00–01:59)",
            11: "⛔ Closed / No Service (02:00–03:59)",
        }
        reverse_daytime_map = {v: k for k, v in daytime_map.items()}

        # Let user pick a time slot (but default is nothing shown)
        selected_slot = st.selectbox("Select Time Period", [""] + list(daytime_map.values()))

        if selected_slot:
            selected_id = reverse_daytime_map[selected_slot]
            filtered_recs = (
                menu_recs[menu_recs["daytime_id"] == selected_id]
                .merge(menu[["item_id", "menu_item_name"]], left_on="menu_item_id", right_on="item_id", how="left")
                .drop_duplicates(subset=["menu_item_id", "rank"])
                .sort_values("rank")
            )

            if not filtered_recs.empty:
                st.markdown(f"<h4 style='margin-top: 1em;'>Top Menu Items for {selected_slot}</h4>", unsafe_allow_html=True)
                for _, row in filtered_recs.iterrows():
                    st.markdown(
                        f"""
                        <div style="background-color:#f5f8ff; padding:10px; margin-bottom:10px; border-radius:8px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
                            <strong>#{row['rank']}</strong> — {row['menu_item_name']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No recommendations found for this time slot.")
        else:
            st.markdown("<div style='color: #999;'>Please select a time slot to view recommendations.</div>", unsafe_allow_html=True)
    with st.expander("Top 10 Most-Recommended Items"):
        top_items = (
            menu_recs
            .merge(menu[["item_id", "menu_item_name"]], left_on="menu_item_id", right_on="item_id")
            .groupby("menu_item_name")["rank"]
            .count()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
            .rename(columns={"rank": "Times Recommended"})
        )

        chart = alt.Chart(top_items).mark_bar(color="#FBBC05").encode(
            x=alt.X("menu_item_name:N", sort="-y", title="Menu Item", axis=alt.Axis(labelAngle=45)),

            y=alt.Y("Times Recommended:Q"),
            tooltip=["menu_item_name", "Times Recommended"]
        ).properties(
            width=700,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)