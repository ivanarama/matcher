import re
import requests
from rapidfuzz import fuzz
from geopy.distance import geodesic

# --- normalize ---
def normalize(text: str) -> str:
    return text.lower().strip() if text else ""

def parse_list_field(value: str):
    if not value:
        return []
    return [normalize(x) for x in value.split(",") if x.strip()]

def geo_score(coords1, coords2, max_km=10):
    if not coords1 or not coords2:
        return 0.0
    try:
        dist = geodesic(coords1, coords2).km
    except:
        return 0.0
    if dist >= max_km:
        return 0.0
    return 1 - (dist / max_km)

def score_match(legacy, candidate, weights=None):
    if weights is None:
        weights = {"title": 0.4, "address": 0.25, "geo": 0.2, "olympic": 0.1, "infra": 0.05}

    title_legacy = normalize(legacy.get("pagetitle"))
    title_cand = normalize(candidate.get("title"))
    addr_legacy = normalize(legacy.get("Full address") or f"{legacy.get('City')}, {legacy.get('Country')}")
    addr_cand = normalize(candidate.get("address"))
    cand_type = normalize(candidate.get("type"))

    title_score = fuzz.token_sort_ratio(title_legacy, title_cand) / 100.0
    address_score = fuzz.token_sort_ratio(addr_legacy, addr_cand) / 100.0
    geo = geo_score(legacy.get("coords"), candidate.get("coords"))

    olympic_score, infra_score = 0.0, 0.0
    olympic_list = parse_list_field(legacy.get("Olympic sports", ""))
    if olympic_list and cand_type:
        olympic_score = max([fuzz.token_sort_ratio(s, cand_type) / 100.0 for s in olympic_list])
    infra_list = parse_list_field(legacy.get("Sports infrastructure", ""))
    if infra_list and cand_type:
        infra_score = max([fuzz.token_sort_ratio(i, cand_type) / 100.0 for i in infra_list])

    final_score = (
        weights["title"] * title_score +
        weights["address"] * address_score +
        weights["geo"] * geo +
        weights["olympic"] * olympic_score +
        weights["infra"] * infra_score
    )

    return {
        "title_score": round(title_score, 3),
        "address_score": round(address_score, 3),
        "geo_score": round(geo, 3),
        "olympic_score": round(olympic_score, 3),
        "infra_score": round(infra_score, 3),
        "final_score": round(final_score, 3)
    }

def extract_coords_from_gmap(url: str):
    match = re.search(r'@([0-9.\-]+),([0-9.\-]+)', url)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None

def search_candidates(query, location=None, api_key=None):
    url = "https://local-business-data.p.rapidapi.com/search"
    params = {"query": query, "limit": 5}
    if location:
        params["region"] = location
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "local-business-data.p.rapidapi.com"
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for item in data.get("data", []):
        results.append({
            "title": item.get("name"),
            "address": item.get("address"),
            "coords": (item.get("latitude"), item.get("longitude")) if item.get("latitude") and item.get("longitude") else None,
            "type": item.get("type")
        })
    return results

def match_legacy_record(legacy, api_key, threshold=0.75, gap=0.1, weights=None):
    if not legacy.get("coords") and legacy.get("Page in Google maps"):
        legacy["coords"] = extract_coords_from_gmap(legacy["Page in Google maps"])

    if legacy.get("Full address"):
        query = f"{legacy['Full address']} {legacy['pagetitle']}"
    else:
        query = legacy.get("pagetitle")

    location = f"{legacy.get('City')}, {legacy.get('Country')}" if legacy.get("City") and legacy.get("Country") else None
    candidates = search_candidates(query, location, api_key)

    if not candidates:
        return {"status": "unmatched", "best": None, "alternatives": []}

    scored = [(cand, score_match(legacy, cand, weights=weights)) for cand in candidates]
    scored.sort(key=lambda x: x[1]["final_score"], reverse=True)

    best, best_scores = scored[0]
    alts = scored[1:]

    if best_scores["geo_score"] >= 0.99:
        status = "matched"
    else:
        if best_scores["final_score"] >= threshold:
            if alts and (best_scores["final_score"] - alts[0][1]["final_score"] < gap):
                status = "ambiguous"
            else:
                status = "matched"
        elif best_scores["final_score"] >= 0.5:
            status = "weak_match"
        else:
            status = "unmatched"

    return {
        "status": status,
        "best": {"candidate": best, "scores": best_scores},
        "alternatives": [{"candidate": c, "scores": s} for c, s in alts]
    }