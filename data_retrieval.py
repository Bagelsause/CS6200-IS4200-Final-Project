#STANDALONE SCRIPT FOR DATA RETRIEVAL (already located in the jupyter notebook, but just in case)

import requests
import json
import time

API_KEY = ""

SEARCH_QUERIES = [
    "slow-motion motorcycle crash",
    "happy celebration dance",
    "sad farewell waving",
    "cat falling off table",
    "sports goal celebration",
    "funny reaction face",
    "rainy day window view",
    "mic drop moment",
    "shocked expression wide eyes",
    "explosive sneeze"
]
LIMIT = 20

def fetch_gifs(query, api_key, limit=20):
    url = f"https://tenor.googleapis.com/v2/search"
    params = {
        "q": query,
        "key": api_key,
        "limit": limit,
        "media_filter": "gif" #just filtering with "gifs", no mp4's tinygifs's etc
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for query: {query}, {response.text}")
        return None

collected_data = []

for query in SEARCH_QUERIES:
    print(f"Performing retrieval on \"{query}\"")
    data = fetch_gifs(query, API_KEY, LIMIT)
    if data:
        #process each result as needed; here we simply collect a list of URLs and basic metadata
        results = []
        for item in data.get("results", []):
            gif_information = item["media_formats"]["gif"] if "media_formats" in item else None
            results.append({
                #link according to actual format
                "link": gif_information["url"],
                "duration": gif_information["duration"],
                "dimensions": gif_information["dims"],
                "size": gif_information["size"],
                "created-at": item["created"],
                "description": item["content_description"],
                "tags": item["tags"],
                "visual clarity": 0,  #placeholder for manual eval
                "action matching": 0,  #placeholder for manual eval
                "relevance": 0  #placeholder for manual eval
            })
        collected_data.append({
            "query": query,
            "narrative": f"Auto-generated narrative for {query}.",
            "possible-results": results
        })
    #avoid rate limiting rq
    time.sleep(1)

#save all data into json
with open("sample_data_extended.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4)

print("Data collection complete!")