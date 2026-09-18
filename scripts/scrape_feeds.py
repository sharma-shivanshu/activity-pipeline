import os
import csv
import time
import requests
from datetime import datetime

os.makedirs("raw", exist_ok=True)
os.makedirs("processed", exist_ok=True)

print("Starting Phase 1: Scraping Feeds...")
today = datetime.now().strftime("%Y-%m-%d")

with open("sources/source-registry.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["permission_status"] == "OK":
            feed_url = row["feed_url"]
            source_slug = row["source_name"].lower().replace(" ", "_")
            
            # Create raw directory
            out_dir = f"raw/{source_slug}/{today}"
            os.makedirs(out_dir, exist_ok=True)
            out_file = f"{out_dir}/feed.xml"
            
            # Skip if already fetched today
            if os.path.exists(out_file):
                print(f"Skipping {source_slug} - already fetched today.")
                continue
                
            print(f"Fetching {feed_url}...")
            try:
                # Use requests to bypass SSL strictly verified by feedparser
                resp = requests.get(feed_url, headers={'User-Agent': 'PoliticalChakra-Pipeline/1.0'}, timeout=15)
                if resp.status_code == 200:
                    with open(out_file, "wb") as out:
                        out.write(resp.content)
                
                # JMD News crawl delay
                if "jmdnewsflash" in feed_url:
                    time.sleep(60)
                else:
                    time.sleep(2)
            except Exception as e:
                print(f"Failed to fetch {feed_url}: {e}")

print("Phase 1 Complete.")
