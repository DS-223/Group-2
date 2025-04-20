import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="SmartCRM", layout="wide")
st.title("🍽️ SmartCRM for Restaurants & Cafes in Armenia")

@st.cache_data
def load_data():
    path = "../../data/"
    menu = pd.read_csv(path + "dim_menu_items.csv")
    tables = pd.read_csv(path + "dim_tables.csv")
    time = pd.read_csv(path + "dim_time.csv")
    trans_items = pd.read_csv(path + "fact_transaction_items.csv")
    trans = pd.read_csv(path + "fact_transactions.csv")
    campaigns = pd.read_csv(path + "marketing_campaigns.csv")
    nfc = pd.read_csv(path + "nfc_engagements.csv")
    return menu, tables, time, trans_items, trans, campaigns, nfc

menu, tables, time_df, trans_items, trans, campaigns, nfc = load_data()

trans = trans.merge(time_df, on="time_id", how="left")
trans["month"] = pd.to_numeric(trans["month"], errors="coerce")

section = st.sidebar.radio("Go to", ["Dashboard", "Customer Segments", "Campaigns", "Menu Recommender"])

if section == "Dashboard":
    st.subheader("📊 Reporting and Analysis")

    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    available_months = sorted(trans["month"].dropna().unique().astype(int))
    month_names = [month_map[m] for m in available_months]

    selected_name = st.selectbox("📅 Select Month", month_names)
    selected_month = [k for k, v in month_map.items() if v == selected_name][0]
    month_data = trans[trans["month"] == selected_month]

    st.markdown(f"### Overview – {selected_name}")

    total_sales = month_data["total_amount"].sum()
    num_transactions = month_data["transaction_id"].nunique()
    avg_check = month_data["total_amount"].mean()

    top_items = trans_items.merge(menu[["item_id", "item_name"]], on="item_id", how="left")
    top_items = top_items.merge(trans[["transaction_id", "month"]], on="transaction_id")
    top_items = top_items[top_items["month"] == selected_month]
    top_items_grouped = top_items.groupby("item_name")["quantity"].sum().sort_values(ascending=False).head(3)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.0f}")
    with col2:
        st.metric("Transactions", f"{num_transactions:,}")
    with col3:
        st.metric("Avg Check", f"${avg_check:,.2f}")
    with col4:
        st.markdown("**Top Menu Items**")
        for item in top_items_grouped.index:
            st.markdown(f"- {item}")

    st.markdown(f"### Sales Trend & Engagement – {selected_name}")
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

    st.markdown("### Menu Performance & Monthly Sales")
    perf = trans_items.merge(menu[["item_id", "item_name"]], on="item_id", how="left")
    perf = perf.merge(trans[["transaction_id", "month"]], on="transaction_id", how="left")
    perf = perf[perf["month"] == selected_month]
    perf["total_price"] = perf["price"] * perf["quantity"]
    menu_summary = perf.groupby("item_name").agg(
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

    st.markdown("### Campaign Analytics & Table Utilization")
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

    st.markdown("### NFC Engagement Breakdown")
    if not nfc.empty:
        tag_counts = nfc["tag_type"].value_counts().reset_index()
        tag_counts.columns = ["tag_type", "count"]
        chart = alt.Chart(tag_counts).mark_bar().encode(
            x='tag_type:N', y='count:Q'
        ).properties(title="NFC Tag Engagement")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No NFC tag engagement data.")

elif section == "Customer Segments":
    st.subheader("📦 Customer Segmentation (RFM)")
    st.info("Coming soon: RFM segments using Recency, Frequency, Monetary logic.")

elif section == "Campaigns":
    st.subheader("🎯 Campaign Management")
    if not campaigns.empty:
        st.dataframe(campaigns)
    else:
        st.warning("No campaigns data available.")

elif section == "Menu Recommender":
    st.subheader("📋 Menu Recommendation Engine")
    cust_id = st.text_input("Enter Customer ID")
    if cust_id:
        st.success(f"Recommended for customer {cust_id}: 🍕 Pizza, 🍣 Sushi, 🍷 Wine")
