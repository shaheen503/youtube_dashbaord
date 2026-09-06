# YouTube Channel Analytics Dashboard

Done by Shaheen
A Streamlit dashboard that analyzes YouTube video performance data from a CSV file —
built as a personal data analytics portfolio project.

## Features
- Upload any CSV of video-level data (title, category, date, views, likes, comments, tags)
- KPI overview: total views, likes, comments, and average engagement rate
- Views-over-time trend chart
- Top 10 videos by views
- Views broken down by content category
- Engagement rate vs. views scatter plot (spot high-engagement videos even with fewer views)
- Filter by category and date range
- Download the filtered dataset back out as CSV

## Tech Stack
- Python
- Streamlit (UI)
- Pandas (data processing)
- Plotly (interactive charts)

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. (Optional) Generate sample data to try it out:
   ```
   python sample_data_generator.py
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

4. Upload `sample_video_data.csv` (or your own export) when prompted.

## CSV Format
Your CSV needs these columns at minimum:

| Column | Description |
|---|---|
| video_title | Name of the video |
| published_date | Upload date (YYYY-MM-DD) |
| view_count | Total views |
| like_count | Total likes |
| comment_count | Total comments |
| category | (Optional) content category, enables category filter/chart |
| tags | (Optional) semicolon-separated tags |

## What I Learned Building This
- Structuring a multi-page-feel Streamlit app with sidebar filters
- Computing derived metrics (engagement rate) safely, handling divide-by-zero
- Aggregating time-series data for cleaner trend charts
- Making chart data validation defensive (missing-column checks) instead of failing silently

## Possible Next Steps
- Connect directly to the YouTube Data API v3 instead of manual CSV upload
- Add sentiment analysis on video titles/descriptions
- Deploy on Streamlit Community Cloud for a live demo link
- 
