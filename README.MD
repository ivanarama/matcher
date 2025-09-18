# 🏟️ Legacy Sports Facility Matcher

This project provides an API to **match legacy sports facility records** against live business/location data using **RapidAPI**.  
It combines **text similarity**, **address matching**, **geolocation**, and **domain-specific fields** (Olympic sports, infrastructure) to determine the best match.

---

## 🚀 Features

- Django-based REST API  
- Candidate search via [Local Business Data API (RapidAPI)](https://rapidapi.com/letscrape-6bRBa3QguO5/api/local-business-data)  
- Scoring based on:
  - Facility title  
  - Address  
  - Geographic coordinates  
  - Olympic sports  
  - Sports infrastructure  
- Match status:
  - ✅ `match` – confident match  
  - ⚠️ `weak_match` – possible but uncertain  
  - ❓ `ambiguous` – multiple similar candidates  
  - ❌ `unmatched` – no candidate found  
- Configurable weights for scoring  
- Dockerized for easy deployment  

---

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
```

---

## ⚖️ Custom Weights

The scoring function supports configurable weights for each component:

- **title** – facility name similarity  
- **address** – address similarity  
- **geo** – geographic distance match  
- **olympic** – overlap with Olympic sports list  
- **infra** – overlap with sports infrastructure list  

### Default Weights

```python
weights = {
  "title": 0.4,
  "address": 0.25,
  "geo": 0.2,
  "olympic": 0.1,
  "infra": 0.05
}
```

### Example: Geo-dominant Matching

```python
custom_weights = {
  "title": 0.3,
  "address": 0.2,
  "geo": 0.4,
  "olympic": 0.05,
  "infra": 0.05
}
```

### How to Use

```json
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
```

The API will then compute the final score using these weights instead of defaults.  

---

## 🐳 Running with Docker

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/legacy-sports-matcher.git
   cd legacy-sports-matcher
   ```

2. Create `.env` file:
   ```env
   RAPIDAPI_KEY=your_rapidapi_key
   SECRET_KEY=your_django_secret
   ```

3. Build and run:
   ```bash
   docker-compose up --build
   ```

4. API will be available at:
   ```bash
   http://localhost:8000/api/match/
   ```

---

## 📡 API Usage

### Endpoint
```http
POST /api/match/
```

### Request
```json
{
  "pagetitle": "Corallia Beach Swimming Pool",
  "City": "Coral Bay",
  "Country": "Cyprus",
  "Full address": "Coral Bay Ave 70, Peyia 8575, Cyprus",
  "Olympic sports": "Swimming (FINA), Synchronized swimming (FINA)",
  "Sports infrastructure": "Olympic size pool, Diving tower"
}
```

### Response
```json
{
  "status": "match",
  "best": {
    "candidate": {
      "title": "Corallia Beach Olympic Pool",
      "address": "Coral Bay Ave 70, Peyia",
      "coords": [34.85906, 32.35954]
    },
    "scores": {
      "title_score": 0.95,
      "address_score": 0.92,
      "geo_score": 0.98,
      "olympic_score": 1.0,
      "infra_score": 0.8,
      "final_score": 0.95
    }
  },
  "alternatives": [
    {
      "candidate": {
        "title": "Coral Beach Arena",
        "address": "Paphos, Cyprus"
      },
      "scores": {
        "final_score": 0.62
      }
    }
  ]
}
```

---

## 🛠️ Development

Run locally (without Docker):

```bash
pip install -r requirements.txt
python manage.py runserver
```

---

## 📜 License

MIT
