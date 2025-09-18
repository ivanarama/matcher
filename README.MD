🏊 Legacy Sports Facilities Matcher

This project provides an API + client for matching legacy sports facility records against live business data using RapidAPI Local Business Data, with fuzzy scoring and geographic validation.

It is containerized with Docker for easy deployment.

✨ Features

Django REST API endpoint /api/match/

Matches a legacy record (e.g. Olympic sports facilities) to real business data

Uses:

Fuzzy title and address similarity (rapidfuzz)

Geographical distance (geopy)

Olympic sports and infrastructure type matching

Configurable weights for scoring (title, address, geo, olympic, infra)

Status classification:

✅ matched

⚠️ weak_match

❓ ambiguous

❌ unmatched

Client app to test API with sample legacy data

Ready-to-run via Docker Compose

## 📂 Project Structure

```bash
matcher/                     # Project root
├── api/                     # App with matching logic
│   ├── matcher.py           # Matching pipeline
│   └── views.py             # Django REST views
├── matcher/                 # Django project
│   ├── settings.py
│   └── urls.py
├── client.py                # Client sending sample request to API
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env                     # Environment variables

⚙ Configuration

Create a .env file with your credentials:

RAPIDAPI_KEY=your_real_key_here
DJANGO_SECRET_KEY=changeme123

🚀 Running with Docker

Build and start services:

docker-compose up --build


API will run at: http://localhost:8000/api/match/

Client will automatically send a test legacy record and print results in logs

📡 API Usage
Endpoint
POST /api/match/

Example Request Body
{
  "pagetitle": "Corallia Beach and Coral Beach olympic swimming pool",
  "City": "Coral Bay",
  "Country": "Cyprus",
  "Page in Google maps": "https://www.google.com/maps/place/Corallia+Beach+Hotel+Apartments/@34.8590644,32.3569649,17z",
  "Full address": "Coral Bay Ave 70, Peyia 8575, Cyprus",
  "Olympic sports": "Diving (FINA),Swimming (FINA),Synchronized swimming (FINA),Water Polo (FINA)",
  "Sports infrastructure": "Olympic size pool, Diving tower, Water polo field"
}

Example Response
{
  "status": "matched",
  "best": {
    "candidate": {
      "title": "Corallia Beach Hotel & Swimming Pool",
      "address": "Coral Bay Ave 70, Peyia, Cyprus",
      "coords": [34.85906, 32.35954],
      "type": "Swimming pool"
    },
    "scores": {
      "title_score": 0.95,
      "address_score": 0.92,
      "geo_score": 0.99,
      "olympic_score": 1.0,
      "infra_score": 0.8,
      "final_score": 0.94
    }
  },
  "alternatives": [...]
}

🛠 Development

If you prefer running without Docker:

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Then test with:

python client.py

📜 License

MIT License.

⚖️ Custom Weights

The scoring function supports configurable weights for each component:

title – facility name similarity

address – address similarity

geo – geographic distance match

olympic – overlap with Olympic sports list

infra – overlap with sports infrastructure list

Default Weights
weights = {
  "title": 0.4,
  "address": 0.25,
  "geo": 0.2,
  "olympic": 0.1,
  "infra": 0.05
}

Example: Geo-dominant Matching

If you want to rely more heavily on geolocation (e.g., when addresses are noisy):

custom_weights = {
  "title": 0.3,
  "address": 0.2,
  "geo": 0.4,
  "olympic": 0.05,
  "infra": 0.05
}

How to Use

Pass weights into the API request:

{
  "pagetitle": "Corallia Beach and Coral Beach olympic swimming pool",
  "City": "Coral Bay",
  "Country": "Cyprus",
  "Full address": "Coral Bay Ave 70, Peyia 8575, Cyprus",
  "Olympic sports": "Swimming (FINA), Water Polo (FINA)",
  "Sports infrastructure": "Olympic size pool, Diving tower",
  "weights": {
    "title": 0.3,
    "address": 0.2,
    "geo": 0.4,
    "olympic": 0.05,
    "infra": 0.05
  }
}


The API will then compute the final score using these weights instead of defaults.