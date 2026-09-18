# Extraction Schema

Each processed/raw article should follow this JSON format:

```json
{
  "source_name": "Name of the source",
  "feed_url": "RSS Feed URL",
  "article_url": "URL of the specific article",
  "title": "Article Title",
  "published_date": "YYYY-MM-DD",
  "scraped_date": "YYYY-MM-DD",
  "extracted_text": "Full text of the article",
  "extraction_status": "success/partial/failed"
}
```
