import plotly.express as px
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="Insights AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================
# Custom Theme
# ==========================

st.markdown("""
<style>

/* Main background */
.stApp{
    background-color:#F7F9FC;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#1E293B;
    color:white;
}

/* Headers */
h1,h2,h3{
    color:#1E3A8A;
}

/* Buttons */
.stButton>button{
    background:#2563EB;
    color:white;
    border-radius:10px;
}
/* KPI Metric Cards */
div[data-testid="stMetric"]{
    background-color:white;
    border:1px solid #E5E7EB;
    padding:15px;
    border-radius:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==========================
# Title
# ==========================

# ==========================
# Dashboard Banner
# ==========================

st.markdown("""
<div style="
background: linear-gradient(90deg,#2563EB,#1D4ED8);
padding:25px;
border-radius:15px;
color:white;
text-align:center;
margin-bottom:20px;
">

<h1>📊 Insights AI Dashboard</h1>

<h4>Interactive Business Intelligence Dashboard</h4>

<p>
Analyze Sales • Profit • Business Performance using Python, Streamlit & Plotly
</p>

</div>
""", unsafe_allow_html=True)

# ==========================
# Load Dataset
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "Data" / "SampleSuperstore.csv"

df = pd.read_csv(DATA_FILE)

# ==========================
# Sidebar Info
# ==========================

st.sidebar.title("📊 Insights AI")

st.sidebar.markdown("""
### Data Analytics Dashboard

Analyze Superstore Sales & Profit using interactive visualizations.

👨‍💻 Developed with:
- Python
- Pandas
- Streamlit
- Plotly
""")

st.sidebar.divider()
# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

# ==========================
# Apply Filters
# ==========================

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# ==========================
# Current Selection
# ==========================

st.sidebar.divider()

st.sidebar.subheader("📋 Current Selection")

st.sidebar.write(f"**Region:** {selected_region}")
st.sidebar.write(f"**Category:** {selected_category}")
st.sidebar.write(f"**Records Found:** {len(filtered_df)}")

st.sidebar.divider()

st.sidebar.subheader("📊 Quick Stats")

st.sidebar.metric(
    "💰 Total Sales",
    f"${filtered_df['Sales'].sum():,.0f}"
)

st.sidebar.metric(
    "📈 Total Profit",
    f"${filtered_df['Profit'].sum():,.0f}"
)

st.sidebar.metric(
    "📦 Orders",
    len(filtered_df)
)

# ==========================
# Dataset Preview
# ==========================

with st.expander("📋 View Dataset Preview"):
    st.dataframe(filtered_df.head())

# ==========================
# KPI Metrics
# ==========================

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_sales = filtered_df["Sales"].mean()
avg_profit = filtered_df["Profit"].mean()

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Orders", total_orders)
col4.metric("📊 Avg Sales", f"${avg_sales:,.2f}")
col5.metric("💵 Avg Profit", f"${avg_profit:,.2f}")

st.divider()

# ==========================
# Charts Section
# ==========================

col1, col2 = st.columns(2)

# --------------------------
# Sales by Category
# --------------------------

# --------------------------
# Sales by Category (Interactive)
# --------------------------

with col1:

    st.subheader("📊 Sales by Category")

    sales_by_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Interactive Pie Chart
# --------------------------

with col2:

    st.subheader("🥧 Sales Share by Category")

    sales_share = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sales_share,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.4
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Top Cities
# ==========================

col3, col4 = st.columns(2)

# --------------------------
# Top Sales Cities
# --------------------------

with col3:

    st.subheader("🏙️ Top 10 Cities by Sales")

    top_sales = (
        filtered_df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_sales,
        x="Sales",
        y="City",
        orientation="h",
        color="Sales",
        title="Top 10 Cities by Sales"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Top Profit Cities
# --------------------------

with col4:

    st.subheader("💰 Top 10 Cities by Profit")

    top_profit = (
        filtered_df.groupby("City")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_profit,
        x="Profit",
        y="City",
        orientation="h",
        color="Profit",
        title="Top 10 Cities by Profit"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# ==========================
# Download CSV
# ==========================

st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.caption("Download the filtered dataset for further analysis.")
st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ==========================
# Sales by State (Interactive Map)
# ==========================

st.subheader("🌍 Sales by State")

state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .reset_index()
)

fig = px.choropleth(
    state_sales,
    locations="State",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    color_continuous_scale="Blues",
    hover_name="State",
    title="State-wise Sales Distribution"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================
# AI Business Insights
# ==========================

st.subheader("🤖 AI Business Insights")

highest_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

highest_city = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .idxmax()
)

highest_state = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .idxmax()
)

best_segment = (
    filtered_df.groupby("Segment")["Profit"]
    .sum()
    .idxmax()
)

avg_discount = filtered_df["Discount"].mean()

st.success(f"🏆 Highest Sales Category: **{highest_category}**")

st.success(f"🌍 Top Sales City: **{highest_city}**")

st.success(f"📍 Best Performing State: **{highest_state}**")

st.success(f"👥 Most Profitable Segment: **{best_segment}**")

st.warning(f"🎯 Average Discount Offered: **{avg_discount:.2%}**")

st.info("""
### 📈 AI Recommendations

✅ Increase stock in top-performing states.

✅ Focus marketing on profitable customer segments.

✅ Review discount strategy to maximize profit.

✅ Expand high-performing categories across more regions.
""")
# ==========================
# Footer
# ==========================

st.divider()

st.markdown(
    """
    <div style='text-align:center; color:gray; padding:10px;'>
        ❤️ Developed by <b>Prem</b><br>
        Python • Pandas • Streamlit • Plotly
    </div>
    """,
    unsafe_allow_html=True
)
