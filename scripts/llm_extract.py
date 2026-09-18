import os
import json
import glob
import requests

print("Starting Phase 3: Semantic LLM Extraction via Ollama GPU...")
os.makedirs("processed/activity", exist_ok=True)

# Schema requirement
schema = '''{
  "activity_type": ["rally","statement","government_scheme","inauguration","protest","appointment","election_event","other"],
  "electoral_relevance": "high|medium|low|none",
  "actors": [{"name":"","party":"","designation":"","role":""}],
  "parties": [], "constituencies": [], "locations": [],
  "event_date": "YYYY-MM-DD|null",
  "key_claims": [], "summary_hi": ""
}'''

prompt_template = f"""You are a political intelligence analyst extracting structured data from Hindi news articles.
Extract the data into this EXACT JSON format, outputting NOTHING else:
{schema}

Article Text:
{{text}}
"""

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b" # Colab GPU can handle 7B easily!

article_files = glob.glob("processed/articles/*/*.json")
print(f"Found {len(article_files)} articles to process.")

count = 0
for filepath in article_files:
    parts = filepath.split("/")
    source_slug = parts[2]
    filename = parts[3]
    
    out_dir = f"processed/activity/{source_slug}"
    os.makedirs(out_dir, exist_ok=True)
    out_file = f"{out_dir}/{filename}"
    
    if os.path.exists(out_file):
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        article = json.load(f)
        
    text = article.get("extracted_text", "")
    if len(text) < 100:
        continue # Skip failed extractions
        
    print(f"Extracting {filename}...")
    prompt = prompt_template.format(text=text[:4000]) # constrain context length to prevent OOM
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0}
    }
    
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if resp.status_code == 200:
            result = resp.json().get("response", "{}")
            try:
                parsed_json = json.loads(result)
                parsed_json["model"] = MODEL_NAME
                parsed_json["extraction_status"] = "success"
                
                with open(out_file, "w", encoding="utf-8") as out:
                    json.dump(parsed_json, out, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for {filename}")
    except Exception as e:
        print(f"LLM request failed: {e}")
        
    count += 1
    if count >= 100: # Limit to 100 articles per run for the pilot to save Colab timeout
        print("Reached pilot batch limit (100). Stopping.")
        break

print("Phase 3 Complete.")
