"""
YouTube Channel Analytics Dashboard
------------------------------------
A Streamlit dashboard that analyzes YouTube video performance data
uploaded as a CSV. Built as a personal portfolio project.

Expected CSV columns:
    video_title, category, published_date, view_count,
    like_count, comment_count, tags

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(page_title="YouTube Channel Analytics", layout="wide")
st.title("📊 YouTube Channel Analytics Dashboard")
st.caption("Upload your channel's video data (CSV) to explore performance trends.")


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
REQUIRED_COLUMNS = ["video_title", "published_date", "view_count", "like_count", "comment_count"]


def load_data(file) -> pd.DataFrame:
    """Read the uploaded CSV and parse the date column."""
    data = pd.read_csv(file)
    if "published_date" in data.columns:
        data["published_date"] = pd.to_datetime(data["published_date"], errors="coerce")
    return data


def validate_columns(data: pd.DataFrame) -> list:
    """Return a list of required columns that are missing from the data."""
    return [col for col in REQUIRED_COLUMNS if col not in data.columns]


def compute_engagement_rate(data: pd.DataFrame) -> pd.DataFrame:
    """Add an engagement rate column: (likes + comments) / views."""
    data = data.copy()
    data["engagement_rate"] = (
        (data["like_count"] + data["comment_count"]) / data["view_count"].replace(0, pd.NA)
    ).fillna(0)
    return data


# ---------------------------------------------------------
# Main app
# ---------------------------------------------------------
uploaded_file = st.file_uploader("Upload your video data CSV", type=["csv"])

if uploaded_file is None:
    st.info("👆 Upload a CSV to get started. Don't have one? Use sample_data_generator.py to create one.")
    st.stop()

df = load_data(uploaded_file)

missing_cols = validate_columns(df)
if missing_cols:
    st.error(f"Your CSV is missing these required columns: {missing_cols}")
    st.stop()

df = compute_engagement_rate(df)

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

if "category" in df.columns:
    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    if selected_category != "All":
        df = df[df["category"] == selected_category]

if df["published_date"].notna().any():
    min_date = df["published_date"].min()
    max_date = df["published_date"].max()
    date_range = st.sidebar.date_input("Date range", [min_date, max_date])
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["published_date"] >= start) & (df["published_date"] <= end)]

# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------
st.subheader("Channel Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Views", f"{df['view_count'].sum():,.0f}")
col2.metric("Total Likes", f"{df['like_count'].sum():,.0f}")
col3.metric("Total Comments", f"{df['comment_count'].sum():,.0f}")
col4.metric("Avg. Engagement Rate", f"{df['engagement_rate'].mean() * 100:.2f}%")

# ---------------------------------------------------------
# Views over time
# ---------------------------------------------------------
st.subheader("📈 Views Over Time")

daily_views = df.groupby(df["published_date"].dt.date)["view_count"].sum().reset_index()
daily_views.columns = ["date", "views"]

fig_trend = px.line(daily_views, x="date", y="views", markers=True, title="Views by Publish Date")
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------
# Top videos
# ---------------------------------------------------------
st.subheader("🔥 Top 10 Videos by Views")

top_videos = df.sort_values("view_count", ascending=False).head(10)
fig_top = px.bar(
    top_videos, x="view_count", y="video_title", orientation="h",
    title="Top Performing Videos"
)
fig_top.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_top, use_container_width=True)

# ---------------------------------------------------------
# Category breakdown
# ---------------------------------------------------------
if "category" in df.columns:
    st.subheader("📂 Views by Category")
    category_views = df.groupby("category")["view_count"].sum().reset_index()
    fig_cat = px.bar(category_views, x="category", y="view_count", title="Total Views by Category")
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------
# Engagement rate distribution
# ---------------------------------------------------------
st.subheader("💬 Engagement Rate by Video")

fig_engagement = px.scatter(
    df, x="view_count", y="engagement_rate", hover_name="video_title",
    title="Engagement Rate vs. Views", labels={"engagement_rate": "Engagement Rate"}
)
st.plotly_chart(fig_engagement, use_container_width=True)

# ---------------------------------------------------------
# Raw data + download
# ---------------------------------------------------------
with st.expander("View filtered data"):
    st.dataframe(df)
    st.download_button(
        "Download filtered data as CSV",
        df.to_csv(index=False).encode("utf-8"),
        "filtered_youtube_data.csv",
        "text/csv"
    )
