import os
import json
import glob
import hashlib
import feedparser
import trafilatura
from datetime import datetime

print("Starting Phase 2: Normalizing to _SCHEMA.md format...")
os.makedirs("processed/articles", exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

for feed_file in glob.glob("raw/*/*/feed.xml"):
    # Read bytes to avoid urllib SSL issues in feedparser
    with open(feed_file, "rb") as f:
        feed_bytes = f.read()
    
    parsed = feedparser.parse(feed_bytes)
    
    # Extract source name from folder path: raw/slug/date/feed.xml
    parts = feed_file.split("/")
    source_slug = parts[1]
    
    os.makedirs(f"processed/articles/{source_slug}", exist_ok=True)
    
    for entry in parsed.entries:
        link = entry.get("link", "")
        if not link: continue
            
        url_hash = hashlib.sha1(link.encode("utf-8")).hexdigest()
        out_file = f"processed/articles/{source_slug}/{url_hash}.json"
        
        if os.path.exists(out_file):
            continue
            
        # Get content (Patrika puts full HTML in content:encoded)
        html_content = ""
        if "content" in entry:
            html_content = entry.content[0].value
        elif "summary" in entry:
            html_content = entry.summary
            
        # Extract plain text
        extracted_text = trafilatura.extract(html_content) if html_content else ""
        
        status = "failed"
        if extracted_text:
            status = "success" if len(extracted_text) > 400 else "partial"
            
        article_data = {
            "source_name": source_slug,
            "feed_url": feed_file, # We don't have the original feed_url easily here, keeping logic simple
            "article_url": link,
            "title": entry.get("title", ""),
            "published_date": entry.get("published", ""),
            "scraped_date": today,
            "extracted_text": extracted_text,
            "extraction_status": status
        }
        
        with open(out_file, "w", encoding="utf-8") as out:
            json.dump(article_data, out, indent=2, ensure_ascii=False)

print("Phase 2 Complete.")
