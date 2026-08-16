import plotly.express as px
import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

/* Main Background */
.stApp{
    background-color:#F7F9FC;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#1E293B;
}

/* Sidebar General Text */
section[data-testid="stSidebar"]{
    background:#1E293B;
    color:white;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div{
    color:white !important;
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

/* KPI Cards */
div[data-testid="stMetric"]{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:15px;
    padding:15px;
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

# ==========================
# Sidebar Navigation
# ==========================

page = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Dashboard",
        "📊 Sales Analysis",
        "💰 Profit Analysis",
        "🌍 Geography",
        "🤖 AI Insights",
        "ℹ️ About"
    ]
)

st.sidebar.divider()

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


# ==========================
# Dataset Preview
# ==========================

with st.expander("📋 View Dataset Preview"):
    st.dataframe(filtered_df.head())

# ==========================
# Profit Analysis Page
# ==========================

if page == "💰 Profit Analysis":

    st.header("💰 Profit Analysis")

    # Profit by Category
    st.subheader("💰 Profit by Category")

    profit_by_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit_by_category,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Top Sub-Categories by Profit
    st.subheader("📈 Top 10 Sub-Categories by Profit")

    profit_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        profit_by_subcategory,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Sub-Category",
        title="Top 10 Sub-Categories by Profit"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Loss-Making Sub-Categories
    st.subheader("🔴 Loss-Making Sub-Categories")

    loss_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .reset_index()
    )

    loss_by_subcategory = (
        loss_by_subcategory[
            loss_by_subcategory["Profit"] < 0
        ]
        .sort_values("Profit")
    )

    if loss_by_subcategory.empty:

        st.success(
            "🎉 No loss-making sub-categories found for the current filters."
        )

    else:

        fig = px.bar(
            loss_by_subcategory,
            x="Profit",
            y="Sub-Category",
            orientation="h",
            color="Profit",
            title="Loss-Making Sub-Categories"
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

    # Top Cities by Profit
    st.subheader("🏙️ Top 10 Cities by Profit")

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
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    st.stop()

# ==========================
# Sales Analysis Page
# ==========================

if page == "📊 Sales Analysis":

    st.header("📊 Sales Analysis")

    # Sales by Category
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
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sales Share
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
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Top Sub-Categories by Sales
    st.subheader("🏆 Top 10 Sub-Categories by Sales")

    sales_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        sales_by_subcategory,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color="Sub-Category",
        title="Top 10 Sub-Categories by Sales"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    # Top Cities by Sales
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
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    st.stop()

# ==========================
# Geography Page
# ==========================

if page == "🌍 Geography":

    st.header("🌍 Geography Analysis")

    # Regional Performance
    st.subheader("🌍 Regional Performance")

    col1, col2 = st.columns(2)

    with col1:

        st.write("💰 **Sales by Region**")

        sales_by_region = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            sales_by_region,
            x="Region",
            y="Sales",
            color="Region",
            title="Sales by Region"
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.write("📈 **Profit by Region**")

        profit_by_region = (
            filtered_df.groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            profit_by_region,
            x="Region",
            y="Profit",
            color="Region",
            title="Profit by Region"
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

    # Sales by State
    st.subheader("🗺️ Sales by State")

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

    # Profit vs Discount
    st.subheader("💹 Profit vs Discount Analysis")

    fig = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit",
        color="Category",
        size="Sales",
        hover_data=["Sub-Category", "Region"],
        title="Profit vs Discount"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    st.stop()


# ==========================
# Page Content Control
# ==========================

if page != "🏠 Dashboard":
    st.info("🚧 This section is being organized into its dedicated navigation page.")
    st.stop()

# ==========================
# KPI Metrics
# ==========================

st.subheader("📈 Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_discount = filtered_df["Discount"].mean()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "🎯 Avg Discount",
    f"{avg_discount:.2%}"
)

col5.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

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
# Regional Performance
# ==========================

st.divider()

st.subheader("🌍 Regional Performance")

col1, col2 = st.columns(2)

# --------------------------
# Sales by Region
# --------------------------

with col1:

    st.write("💰 **Sales by Region**")

    sales_by_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        sales_by_region,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Profit by Region
# --------------------------

with col2:

    st.write("📈 **Profit by Region**")

    profit_by_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        profit_by_region,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# Top Performing Sub-Categories
# ==========================

st.divider()

st.subheader("🏆 Top Performing Sub-Categories")

col1, col2 = st.columns(2)

# --------------------------
# Top Sub-Categories by Sales
# --------------------------

with col1:

    st.write("💰 **Top Sub-Categories by Sales**")

    sales_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        sales_by_subcategory,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color="Sub-Category",
        title="Top 10 Sub-Categories by Sales"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------
# Top Sub-Categories by Profit
# --------------------------

with col2:

    st.write("📈 **Top Sub-Categories by Profit**")

    profit_by_subcategory = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        profit_by_subcategory,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Sub-Category",
        title="Top 10 Sub-Categories by Profit"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================
# Loss Analysis
# ==========================

st.divider()

st.subheader("🔴 Loss-Making Sub-Categories")

loss_by_subcategory = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
)

loss_by_subcategory = (
    loss_by_subcategory[
        loss_by_subcategory["Profit"] < 0
    ]
    .sort_values("Profit")
)

if loss_by_subcategory.empty:

    st.success(
        "🎉 No loss-making sub-categories found for the current filters."
    )

else:

    fig = px.bar(
        loss_by_subcategory,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        title="Loss-Making Sub-Categories"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

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

st.subheader("💹 Profit vs Discount Analysis")

fig = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=["Sub-Category", "Region"],
    title="Profit vs Discount"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Discount",
    yaxis_title="Profit"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("🏆 Top 10 Sub-Categories by Profit")

top_profit_subcategory = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_profit_subcategory,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    color="Profit",
    title="Top 10 Most Profitable Sub-Categories"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Profit",
    yaxis_title="Sub-Category"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📋 Business Summary")

summary_df = (
    filtered_df
    .groupby("Category")
    .agg({
        "Sales":"sum",
        "Profit":"sum",
        "Quantity":"sum",
        "Discount":"mean"
    })
    .reset_index()
)

summary_df["Sales"] = summary_df["Sales"].round(2)
summary_df["Profit"] = summary_df["Profit"].round(2)
summary_df["Discount"] = (summary_df["Discount"]*100).round(2)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)
st.divider()

st.subheader("🎯 Business Performance Score")

sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
discount = filtered_df["Discount"].mean()
quantity = filtered_df["Quantity"].sum()

score = 0

# Sales Score (30 Marks)
if sales >= 800000:
    score += 30
elif sales >= 500000:
    score += 22
elif sales >= 300000:
    score += 15
else:
    score += 8

# Profit Score (30 Marks)
if profit >= 100000:
    score += 30
elif profit >= 50000:
    score += 22
elif profit >= 20000:
    score += 15
else:
    score += 8

# Discount Score (20 Marks)
if discount <= 0.10:
    score += 20
elif discount <= 0.20:
    score += 15
elif discount <= 0.30:
    score += 10
else:
    score += 5

# Quantity Score (20 Marks)
if quantity >= 9000:
    score += 20
elif quantity >= 6000:
    score += 15
elif quantity >= 3000:
    score += 10
else:
    score += 5

st.progress(score / 100)

if score >= 85:
    st.success(f"🏆 Overall Business Score: {score}/100 (Excellent)")
elif score >= 70:
    st.success(f"✅ Overall Business Score: {score}/100 (Good)")
elif score >= 50:
    st.warning(f"⚠️ Overall Business Score: {score}/100 (Average)")
else:
    st.error(f"❌ Overall Business Score: {score}/100 (Needs Improvement)")

st.caption(
    "Score is calculated based on Sales, Profit, Discount and Quantity performance."
)


# ==========================
# AI Business Insights
# ==========================

st.subheader("🤖 AI Business Insights")

# --------------------------------
# Key Business Insights
# --------------------------------

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


# --------------------------------
# Insight Cards
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"🏆 **Highest Sales Category**\n\n"
        f"### {highest_category}"
    )

with col2:
    st.success(
        f"🌍 **Top Sales City**\n\n"
        f"### {highest_city}"
    )

with col3:
    st.success(
        f"📍 **Best Performing State**\n\n"
        f"### {highest_state}"
    )


col4, col5 = st.columns(2)

with col4:
    st.success(
        f"👥 **Most Profitable Segment**\n\n"
        f"### {best_segment}"
    )

with col5:
    st.warning(
        f"🎯 **Average Discount Offered**\n\n"
        f"### {avg_discount:.2%}"
    )


st.divider()


# --------------------------------
# AI Recommendations
# --------------------------------

st.subheader("📈 AI Recommendations")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:

    st.info(
        "📦 **Inventory Strategy**\n\n"
        "Increase stock availability in top-performing states "
        "to support stronger sales."
    )

    st.info(
        "🎯 **Marketing Strategy**\n\n"
        "Focus marketing efforts on profitable customer segments."
    )

with rec_col2:

    st.info(
        "💰 **Discount Strategy**\n\n"
        "Review discount levels to balance sales growth with profit."
    )

    st.info(
        "🚀 **Growth Strategy**\n\n"
        "Expand high-performing categories into other promising regions."
    )


st.divider()


# ==========================
# Ask AI
# ==========================

st.subheader("🤖 Ask AI About Your Business")

question = st.text_input(
    "💬 Ask your business question",
    placeholder="Example: Which category is most profitable?"
)

st.caption(
    "💡 Try questions about sales, profit, cities, states, regions, "
    "categories, sub-categories, discounts, or quantity."
)
def normalize_business_question(question):
    q = question.lower().strip()

    # Profit-related words
    profit_words = [
        "profit",
        "profitable",
        "profitability",
        "earn",
        "earns", 
        "earning",
        "earnings",
        "money",
        "income",
        "gain"
    ]

    # Sales-related words
    sales_words = [
        "sales",
        "revenue",
        "sold",
        "selling",
        "turnover"
    ]

    # Loss-related words
    loss_words = [
        "loss",
        "losing",
        "negative profit",
        "money losing",
        "loss making"
    ]

    # Dimension detection
    dimensions = {
        "category": ["category", "categories"],
        "sub_category": ["sub-category", "subcategory", "sub category"],
        "region": ["region", "market", "area"],
        "state": ["state", "states"],
        "city": ["city", "cities"],
        "segment": ["segment", "customer group", "customer segment"],
        "product": ["product", "products"]
    }

    if any(word in q for word in loss_words):
        metric = "loss"

    elif any(word in q for word in profit_words):
        metric = "profit"

    elif any(word in q for word in sales_words):
        metric = "sales"

    elif "discount" in q:
        metric = "discount"

    elif "quantity" in q or "units" in q:
        metric = "quantity"

    else:
        metric = None

    dimension = None

    for name, keywords in dimensions.items():
        if any(word in q for word in keywords):
            dimension = name
            break

    return {
        "question": q,
        "metric": metric,
        "dimension": dimension
    }

if st.button("🚀 Ask AI"):

    analysis = normalize_business_question(question)

    q = analysis["question"].strip().lower()
    metric = analysis["metric"]
    dimension = analysis["dimension"]

    # --------------------------------
    # Empty Question
    # --------------------------------

    if not q:

        st.warning("Please enter a question first.")

       # --------------------------------
    # Business Summary
    # --------------------------------

    elif "summary" in q or "business performance" in q:

        total_sales = filtered_df["Sales"].sum()
        total_profit = filtered_df["Profit"].sum()
        avg_discount = filtered_df["Discount"].mean()
        total_quantity = filtered_df["Quantity"].sum()

        st.subheader("📊 Business Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Total Sales",
                f"${total_sales:,.2f}"
            )

        with col2:
            st.metric(
                "📈 Total Profit",
                f"${total_profit:,.2f}"
            )

        with col3:
            st.metric(
                "🎯 Avg Discount",
                f"{avg_discount:.2%}"
            )

        with col4:
            st.metric(
                "📦 Quantity Sold",
                f"{total_quantity:,.0f}"
            )

        
        # --------------------------------
    # Advanced Business Analysis
    # --------------------------------

    elif (
        ("high sales" in q or "highest sales" in q)
        and ("low profit" in q or "lowest profit" in q)
    ):

        if dimension == "category":
            group_col = "Category"

        elif dimension == "sub_category":
            group_col = "Sub-Category"

        elif dimension == "region":
            group_col = "Region"

        elif dimension == "state":
            group_col = "State"

        elif dimension == "city":
            group_col = "City"

        elif dimension == "segment":
            group_col = "Segment"

        else:
            group_col = "Category"

        comparison = (
            filtered_df.groupby(group_col)[["Sales", "Profit"]]
            .sum()
            .reset_index()
        )

        if comparison.empty:

            st.warning("No data available for the current filters.")

        else:

            comparison["Profit Margin"] = (
                comparison["Profit"] / comparison["Sales"] * 100
            ).where(comparison["Sales"] != 0, 0)

            high_sales_low_profit = (
                comparison
                .sort_values(
                    ["Sales", "Profit"],
                    ascending=[False, True]
                )
                .head(5)
            )

            st.subheader("🧠 High Sales but Low Profit Analysis")

            st.write(
                f"These {group_col.lower()}s generate strong sales "
                "but comparatively weaker profit."
            )

            st.dataframe(
                high_sales_low_profit[
                    [group_col, "Sales", "Profit", "Profit Margin"]
                ],
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------
    # Discount Risk Analysis
    # --------------------------------

    elif (
        ("high discount" in q or "highest discount" in q)
        and ("low profit" in q or "lowest profit" in q)
    ):

        if dimension == "category":
            group_col = "Category"

        elif dimension == "sub_category":
            group_col = "Sub-Category"

        elif dimension == "region":
            group_col = "Region"

        elif dimension == "state":
            group_col = "State"

        elif dimension == "city":
            group_col = "City"

        elif dimension == "segment":
            group_col = "Segment"

        else:
            group_col = "Category"

        comparison = (
            filtered_df.groupby(group_col)[
                ["Sales", "Profit", "Discount"]
            ]
            .mean()
            .reset_index()
        )

        if comparison.empty:

            st.warning("No data available for the current filters.")

        else:

            comparison = comparison.sort_values(
                ["Discount", "Profit"],
                ascending=[False, True]
            ).head(5)

            st.subheader("🎯 Discount Risk Analysis")

            st.write(
                f"These {group_col.lower()}s have relatively high "
                "discounts and weaker profitability."
            )

            st.dataframe(
                comparison[
                    [group_col, "Sales", "Profit", "Discount"]
                ],
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------
    # Business Opportunity Analysis
    # --------------------------------

    elif (
        ("best opportunity" in q or
         "business opportunity" in q or
         "best business" in q)
        and (
            "category" in q or
            "sub-category" in q or
            "subcategory" in q or
            "region" in q or
            "state" in q or
            "city" in q or
            "segment" in q
        )
    ):

        if dimension == "category":
            group_col = "Category"

        elif dimension == "sub_category":
            group_col = "Sub-Category"

        elif dimension == "region":
            group_col = "Region"

        elif dimension == "state":
            group_col = "State"

        elif dimension == "city":
            group_col = "City"

        elif dimension == "segment":
            group_col = "Segment"

        else:
            group_col = "Category"

        opportunity = (
            filtered_df.groupby(group_col)[
                ["Sales", "Profit"]
            ]
            .sum()
            .reset_index()
        )

        if opportunity.empty:

            st.warning(
                "No data available for the current filters."
            )

        else:

            opportunity["Profit Margin"] = (
                opportunity["Profit"] /
                opportunity["Sales"] * 100
            ).where(
                opportunity["Sales"] != 0,
                0
            )

            opportunity["Opportunity Score"] = (
                opportunity["Profit Margin"] * 0.5
                + (
                    opportunity["Sales"] /
                    opportunity["Sales"].max()
                ) * 50
            )

            opportunity = (
                opportunity
                .sort_values(
                    "Opportunity Score",
                    ascending=False
                )
                .head(5)
            )

            st.subheader(
                "💎 Business Opportunity Analysis"
            )

            st.write(
                f"These {group_col.lower()}s show the strongest "
                "combination of sales performance and profitability."
            )

            st.dataframe(
                opportunity[
                    [
                        group_col,
                        "Sales",
                        "Profit",
                        "Profit Margin",
                        "Opportunity Score"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------
    # Loss / Negative Profit
    # --------------------------------

    elif "loss" in q or "negative profit" in q:

        result = (
            filtered_df.groupby("Sub-Category")["Profit"]
            .sum()
            .sort_values()
        )

        result = result[result < 0].head(10)

        if len(result) > 0:

            loss_table = result.reset_index()

            total_loss = result.sum()

            st.write("⚠️ **Loss-Making Sub-Categories**")

            st.metric(
                "⚠️ Total Loss",
                f"${abs(total_loss):,.2f}"
            )

            st.bar_chart(
                loss_table.set_index("Sub-Category")["Profit"]
            )

            st.dataframe(
                loss_table,
                use_container_width=True
            )

        else:

            st.success(
                "✅ No loss-making sub-categories found."
            )

        # --------------------------------
    # Top 5 Ranking
    # --------------------------------

    elif "top 5" in q or "top five" in q:

                # Top 5 Cities by Profit
        if ("city" in q or "cities" in q) and "profit" in q:

            result = (
                filtered_df.groupby("City")["Profit"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("🏆 **Top 5 Cities by Profit**")

            st.bar_chart(
                result.set_index("City")["Profit"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 Cities by Sales
        elif ("city" in q or "cities" in q) and "sales" in q:

            result = (
                filtered_df.groupby("City")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("💰 **Top 5 Cities by Sales**")

            st.bar_chart(
                result.set_index("City")["Sales"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 States by Profit
        elif ("state" in q or "states" in q) and "profit" in q:

            result = (
                filtered_df.groupby("State")["Profit"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("🏆 **Top 5 States by Profit**")

            st.bar_chart(
                result.set_index("State")["Profit"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 States by Sales
        elif ("state" in q or "states" in q) and "sales" in q:

            result = (
                filtered_df.groupby("State")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("💰 **Top 5 States by Sales**")

            st.bar_chart(
                result.set_index("State")["Sales"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 Categories by Profit
        elif ("category" in q or "categories" in q) and "profit" in q:

            result = (
                filtered_df.groupby("Category")["Profit"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("🏆 **Top 5 Categories by Profit**")

            st.bar_chart(
                result.set_index("Category")["Profit"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

               # Top 5 Categories by Sales
        elif ("category" in q or "categories" in q) and "sales" in q:

            result = (
                filtered_df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("💰 **Top 5 Categories by Sales**")

            st.bar_chart(
                result.set_index("Category")["Sales"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 Sub-Categories by Profit
        elif (
            (
                "product" in q
                or "products" in q
                or "sub-category" in q
                or "subcategory" in q
                or "sub category" in q
            )
            and "profit" in q
        ):

            result = (
                filtered_df.groupby("Sub-Category")["Profit"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("🏆 **Top 5 Sub-Categories by Profit**")

            st.bar_chart(
                result.set_index("Sub-Category")["Profit"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

                # Top 5 Sub-Categories by Sales
        elif (
            (
                "product" in q
                or "products" in q
                or "sub-category" in q
                or "subcategory" in q
                or "sub category" in q
            )
            and "sales" in q
        ):

            result = (
                filtered_df.groupby("Sub-Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            st.write("💰 **Top 5 Sub-Categories by Sales**")

            st.bar_chart(
                result.set_index("Sub-Category")["Sales"]
            )

            st.dataframe(
                result,
                use_container_width=True
            )

        else:

            st.info(
                "🤖 Try asking:\n\n"
                "• Top 5 states by sales\n"
                "• Top 5 states by profit\n"
                "• Top 5 cities by sales\n"
                "• Top 5 cities by profit\n"
                "• Top 5 categories by sales\n"
                "• Top 5 categories by profit\n"
                "• Top 5 sub-categories by sales\n"
                "• Top 5 sub-categories by profit"
            )

    # --------------------------------
    # Total / Average Metrics
    # --------------------------------

    elif "total sales" in q or "sales total" in q:

        value = filtered_df["Sales"].sum()

        st.success(
            f"💰 Total Sales: **${value:,.2f}**"
        )

    elif "total profit" in q or "profit total" in q:

        value = filtered_df["Profit"].sum()

        st.success(
            f"📈 Total Profit: **${value:,.2f}**"
        )

    elif "average sales" in q or "avg sales" in q:

        value = filtered_df["Sales"].mean()

        st.success(
            f"💰 Average Sales: **${value:,.2f}**"
        )

    elif "average profit" in q or "avg profit" in q:

        value = filtered_df["Profit"].mean()

        st.success(
            f"📈 Average Profit: **${value:,.2f}**"
        )

    elif "average discount" in q or "avg discount" in q:

        value = filtered_df["Discount"].mean()

        st.success(
            f"🎯 Average Discount: **{value:.2%}**"
        )

    elif "total quantity" in q or "quantity sold" in q:

        value = filtered_df["Quantity"].sum()

        st.success(
            f"📦 Total Quantity Sold: **{value:,.0f}**"
        )

    # --------------------------------
    # Category Analysis
    # --------------------------------

    elif dimension == "category" and metric == "profit":

        result = (
            filtered_df.groupby("Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()
        value = result.max()

        st.success(
            f"🏆 Most Profitable Category: **{best}** "
            f"(${value:,.2f} profit)"
        )

    elif dimension == "category" and metric == "sales":

        result = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()
        value = result.max()

        st.success(
            f"💰 Highest Sales Category: **{best}** "
            f"(${value:,.2f} sales)"
        )

        # --------------------------------
    # Region Analysis
    # --------------------------------

    elif "region" in q and "profit" in q:

        result = (
            filtered_df.groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()
        value = result.max()

        st.success(
            f"📍 Most Profitable Region: **{best}** "
            f"(${value:,.2f} profit)"
        )

    elif "region" in q and "sales" in q:

        result = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()
        value = result.max()

        st.success(
            f"🌎 Highest Sales Region: **{best}** "
            f"(${value:,.2f} sales)"
        )

    # --------------------------------
    # City Analysis
    # --------------------------------

    elif dimension == "city" and metric == "profit":

        result = (
            filtered_df.groupby("City")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"🏙️ Most Profitable City: **{best}** "
            f"(${result.max():,.2f} profit)"
        )

    elif dimension == "city" and metric == "sales":

        result = (
            filtered_df.groupby("City")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"🏙️ Highest Sales City: **{best}** "
            f"(${result.max():,.2f} sales)"
        )

    # --------------------------------
    # State Analysis
    # --------------------------------

    elif dimension == "state" and metric == "profit":

        result = (
            filtered_df.groupby("State")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"📍 Most Profitable State: **{best}** "
            f"(${result.max():,.2f} profit)"
        )

    elif dimension == "state" and metric == "sales":

        result = (
            filtered_df.groupby("State")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"📍 Highest Sales State: **{best}** "
            f"(${result.max():,.2f} sales)"
        )

    # --------------------------------
    # Segment Analysis
    # --------------------------------

    elif dimension == "segment" and metric == "profit":

        result = (
            filtered_df.groupby("Segment")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"👥 Most Profitable Segment: **{best}** "
            f"(${result.max():,.2f} profit)"
        )

    elif dimension == "segment" and metric == "sales":

        result = (
            filtered_df.groupby("Segment")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"👥 Highest Sales Segment: **{best}** "
            f"(${result.max():,.2f} sales)"
        )

    # --------------------------------
    # Sub-Category Analysis
    # --------------------------------

    elif dimension == "sub_category" and metric == "profit":

        result = (
            filtered_df.groupby("Sub-Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"🏆 Most Profitable Sub-Category: **{best}** "
            f"(${result.max():,.2f} profit)"
        )

    elif dimension == "sub_category" and metric == "sales":

        result = (
            filtered_df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        best = result.idxmax()

        st.success(
            f"💰 Highest Sales Sub-Category: **{best}** "
            f"(${result.max():,.2f} sales)"
        )


    # --------------------------------
    # Fallback
    # --------------------------------

    else:

        st.info(
            """
🤖 I couldn't identify the exact analysis yet.

Try asking about:

**Sales • Profit • Discount • Category • Region • State • City • Segment • Products • Business Performance**
"""
        )


def generate_pdf_report():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Insights AI Dashboard Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"Total Sales: ${total_sales:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Total Profit: ${total_profit:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Total Orders: {total_orders}", styles["BodyText"]))
    avg_sales = filtered_df["Sales"].mean()
    avg_profit = filtered_df["Profit"].mean()
    story.append(Paragraph(f"Average Sales: ${avg_sales:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Average Profit: ${avg_profit:,.2f}", styles["BodyText"]))
    story.append(Paragraph(f"Business Score: {score}/100", styles["BodyText"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "Generated using Insights AI Dashboard",
            styles["Italic"]
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# ==========================
# PDF Report Download
# ==========================

st.divider()

st.subheader("📄 Business Report")

pdf_file = generate_pdf_report()

st.download_button(
    label="📥 Download Business Report",
    data=pdf_file,
    file_name="Insights_AI_Business_Report.pdf",
    mime="application/pdf"
)

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

