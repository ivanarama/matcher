import requests
import json

legacy_example = {
    "pagetitle": "Corallia Beach and Coral Beach olympic swimming pool",
    "City": "Coral Bay",
    "Country": "Cyprus",
    "Page in Google maps": "https://www.google.com/maps/place/Corallia+Beach+Hotel+Apartments/@34.8590644,32.3569649,17z",
    "Full address": "Coral Bay Ave 70, Peyia 8575, Cyprus",
    "Olympic sports": "Diving (FINA),Swimming (FINA),Synchronized swimming (FINA),Water Polo (FINA)",
    "Sports infrastructure": "Olympic size pool, Diving tower, Water polo field"
}

resp = requests.post("http://api:8000/api/match/", json=legacy_example)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))