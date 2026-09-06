"""
Generates a sample CSV of YouTube video data for testing the dashboard.

Run:
    python sample_data_generator.py

Output:
    sample_video_data.csv
"""

import csv
import random
from datetime import date, timedelta

random.seed(7)

CATEGORIES = ["Tutorial", "Vlog", "Review", "Shorts", "Q&A"]
TAG_POOL = ["python", "coding", "tech", "review", "howto", "tips", "2026", "beginner"]

NUM_VIDEOS = 35
START_DATE = date(2025, 6, 1)

rows = []
for i in range(NUM_VIDEOS):
    category = random.choice(CATEGORIES)
    title = f"{category} Video {i + 1}"
    published_date = START_DATE + timedelta(days=random.randint(0, 300))

    views = random.choice([800, 3000, 12000, 40000, 90000]) + random.randint(-500, 2000)
    views = max(views, 50)
    likes = int(views * random.uniform(0.02, 0.09))
    comments = int(views * random.uniform(0.002, 0.015))
    tags = ";".join(random.sample(TAG_POOL, k=random.randint(2, 4)))

    rows.append([title, category, published_date.isoformat(), views, likes, comments, tags])

header = ["video_title", "category", "published_date", "view_count", "like_count", "comment_count", "tags"]

with open("sample_video_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Generated {len(rows)} sample video rows -> sample_video_data.csv")
