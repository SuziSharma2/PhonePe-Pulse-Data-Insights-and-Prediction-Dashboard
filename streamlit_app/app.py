# streamlit_app/app.py

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page configuration
st.set_page_config(page_title="PhonePe Data Insights", layout="wide")

# Load data using cache
@st.cache_data

def load_data():
    with sqlite3.connect("db/phonepe_data.db", check_same_thread=False) as conn:
        df_insurance = pd.read_sql_query("SELECT * FROM aggregated_insurance", conn)
        df_transactions = pd.read_sql_query("SELECT * FROM aggregated_transactions", conn)
        df_users = pd.read_sql_query("SELECT * FROM aggregated_user", conn)
        df_map = pd.read_sql_query("SELECT * FROM map_user", conn)
    return df_insurance, df_transactions, df_users, df_map

# Load all datasets
df_insurance, df_transactions, df_users, df_map = load_data()

# Title
st.title("\U0001F4CA PhonePe Data Insights Dashboard")
st.markdown("An interactive dashboard to explore PhonePe usage trends across India.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Insurance", "Transactions", "Device Usage", "Map Users"])

# ---------------- Insurance Tab ----------------
with tab1:
    st.header("\U0001F4D1 Insurance Insights by State & Year")

    state = st.selectbox("Select State", sorted(df_insurance['state'].unique()), key="ins_state")
    year = st.selectbox("Select Year", sorted(df_insurance['year'].unique()), key="ins_year")

    df_filtered = df_insurance[(df_insurance['state'] == state) & (df_insurance['year'] == year)]

    # KPIs
    total_amount = df_filtered['amount'].sum()
    total_policies = df_filtered['count'].sum()
    avg_amount = total_amount / (df_filtered['quarter'].nunique() or 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("\U0001F4B8 Total Insurance Amount", f"{total_amount/1e7:,.2f} Cr")
    col2.metric("\U0001F4CB Total Policies", f"{total_policies:,}")
    col3.metric("\U0001F4C8 Avg Amount per Quarter", f"{avg_amount:,.2f}")

    if df_filtered.empty:
        st.warning("No data available for this selection.")
    else:
        fig = px.bar(
            df_filtered,
            x="quarter",
            y="amount",
            color="type",
            barmode="group",
            title=f"Insurance Amount by Quarter - {state} ({year})"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- Transactions Tab ----------------
with tab2:
    st.header("\U0001F4B8 Transaction Trends")

    # KPIs
    total_amount = df_transactions["transaction_amount"].sum()
    total_count = df_transactions["transaction_count"].sum()
    top_state = df_transactions.groupby("state")["transaction_amount"].sum().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("\U0001F4B5 Total Transaction Volume", f"{total_amount/1e7:,.2f} Cr")
    col2.metric("\U0001F501 Total Transactions", f"{total_count:,}")
    col3.metric("\U0001F3C6 Top State by Volume", top_state)

    st.subheader("Top 10 States by Transaction Amount")
    top_states = df_transactions.groupby("state")["transaction_amount"].sum().nlargest(10).reset_index()
    fig = px.bar(top_states, x="state", y="transaction_amount", title="Top 10 States by Transaction Amount")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Quarterly Transaction Trends")
    state_trx = st.selectbox("Select State", sorted(df_transactions['state'].unique()), key="trx_state")
    df_state_trend = df_transactions[df_transactions['state'] == state_trx]
    fig = px.line(
        df_state_trend,
        x="quarter",
        y="transaction_amount",
        color="year",
        markers=True,
        title=f"Quarterly Transaction Trend - {state_trx}"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Device Usage Tab ----------------
with tab3:
    st.header("\U0001F4F1 Device Engagement Insights")

    year_dev = st.selectbox("Select Year", sorted(df_users['year'].unique()), key="year_dev")
    quarter_dev = st.selectbox("Select Quarter", sorted(df_users['quarter'].unique()), key="quarter_dev")

    df_filtered_user = df_users[(df_users['year'] == year_dev) & (df_users['quarter'] == quarter_dev)]

    total_devices = df_users["count"].sum()
    top_brand = df_users.groupby("brand")["count"].sum().idxmax()
    top_brand_count = df_users.groupby("brand")["count"].sum().max()

    col1, col2, col3 = st.columns(3)
    col1.metric("\U0001F4F2 Total Devices", f"{total_devices:,}")
    col2.metric("\U0001F4AA Top Brand", top_brand)
    col3.metric("\U0001F4C9 Users in Top Brand", f"{top_brand_count:,}")

    if df_filtered_user.empty:
        st.warning("No device data found.")
    else:
        fig = px.pie(
            df_filtered_user,
            names="brand",
            values="count",
            title=f"Device Brand Share in Q{quarter_dev} {year_dev}"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- Map User Tab ----------------
with tab4:
    st.header("\U0001F5FA District-level Usage Insights")

    state_map = st.selectbox("Select State", sorted(df_map["state"].unique()), key="map_state")
    df_map_filtered = df_map[df_map["state"] == state_map]

    total_users = df_map["registered_users"].sum()
    total_opens = df_map["app_opens"].sum()
    avg_opens_per_user = total_opens / (total_users + 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("\U0001F465 Total Registered Users", f"{total_users:,}")
    col2.metric("\U0001F4F1 Total App Opens", f"{total_opens:,}")
    col3.metric("\U0001F4C8 Avg Opens/User", f"{avg_opens_per_user:.2f}")

    st.subheader("Top Districts by App Opens")
    top_districts = df_map_filtered.sort_values("app_opens", ascending=False).head(10)
    fig = px.bar(top_districts, x="district", y="app_opens", title=f"Top 10 Districts by App Opens - {state_map}")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Low Conversion Districts")
    df_map_filtered["conversion_ratio"] = df_map_filtered["app_opens"] / (df_map_filtered["registered_users"] + 1)
    low_conversion = df_map_filtered.sort_values("conversion_ratio").head(10)
    fig = px.bar(low_conversion, x="district", y="conversion_ratio", title=f"Low Conversion Districts - {state_map}")
    st.plotly_chart(fig, use_container_width=True)
