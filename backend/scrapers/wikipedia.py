"""
Wikipedia scraper for seed-company list articles.
Uses the public Wikipedia API (no scraping, no account needed).
"""
import requests
from database import get_db, upsert_company

WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "Varieties-Research/1.0 (research aggregator)"}


def _get_category_members(category: str, limit: int = 500):
    """Return a list of page titles in a given Wikipedia category."""
    members = []
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": min(limit, 500),
        "cmtype": "page",
        "format": "json",
    }
    cont = None
    while True:
        p = dict(params)
        if cont:
            p.update(cont)
        r = requests.get(WIKI_API, params=p, headers=HEADERS, timeout=20)
        r.raise_for_status()
        data = r.json()
        for m in data.get("query", {}).get("categorymembers", []):
            members.append(m["title"])
        if "continue" in data and len(members) < limit:
            cont = data["continue"]
        else:
            break
    return members


def _get_page_extract(title: str):
    """Return (extract, country_guess) for a Wikipedia page."""
    params = {
        "action": "query",
        "prop": "extracts|info",
        "exintro": 1,
        "explaintext": 1,
        "inprop": "url",
        "titles": title,
        "format": "json",
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    for _, page in pages.items():
        extract = page.get("extract", "")
        return extract[:500]
    return ""


def _guess_country(text: str) -> str:
    """Simple country extraction from intro text."""
    countries = [
        "United States", "China", "Netherlands", "Germany", "France",
        "Japan", "South Korea", "India", "Israel", "Italy", "Spain",
        "United Kingdom", "Canada", "Australia", "Brazil", "Mexico",
        "Thailand", "Turkey", "Poland", "Russia", "Ukraine", "Hungary",
        "Czech Republic", "Belgium", "Denmark", "Sweden", "Finland",
        "Switzerland", "Austria", "South Africa", "Kenya", "Egypt",
        "Taiwan", "Vietnam", "Indonesia", "Philippines", "Malaysia",
        "Argentina", "Chile", "New Zealand", "Portugal", "Romania",
    ]
    t = text[:600]
    for c in countries:
        if c in t:
            return c
    # common alternates
    if "American" in t[:400] and "Latin" not in t[:400]:
        return "United States"
    if "Dutch" in t[:400]:
        return "Netherlands"
    if "Japanese" in t[:400]:
        return "Japan"
    if "Chinese" in t[:400]:
        return "China"
    return ""


# Wikipedia categories most likely to contain seed companies.
CATEGORIES = [
    "Seed_companies",
    "Seed_producers",
    "Seed_companies_of_the_United_States",
    "Seed_companies_of_the_Netherlands",
    "Seed_companies_of_France",
    "Seed_companies_of_Germany",
    "Seed_companies_of_Japan",
    "Seed_companies_of_China",
    "Seed_companies_of_India",
    "Seed_companies_of_Israel",
    "Seed_companies_of_Italy",
    "Seed_companies_of_Spain",
    "Seed_companies_of_the_United_Kingdom",
    "Agricultural_companies",  # broad, we filter by keywords
    "Horticulture",
]

CROP_KEYWORDS = {
    "tomato": "tomato",
    "pepper": "pepper",
    "cucumber": "cucumber",
    "melon": "melon",
    "watermelon": "watermelon",
    "lettuce": "lettuce",
    "onion": "onion",
    "carrot": "carrot",
    "cabbage": "cabbage",
    "broccoli": "broccoli",
    "corn": "corn",
    "maize": "corn",
    "rice": "rice",
    "wheat": "wheat",
    "soybean": "soybean",
    "cotton": "cotton",
    "sunflower": "sunflower",
    "flower": "flowers",
    "ornamental": "flowers",
    "vegetable": "vegetables",
    "herb": "herbs",
    "fruit": "fruit",
}


def run():
    conn = get_db()
    added = 0
    skipped = 0

    for category in CATEGORIES:
        try:
            members = _get_category_members(category, limit=200)
        except Exception as e:
            print(f"  [skip category {category}] {e}")
            continue

        for title in members:
            # skip obvious non-company pages
            if any(x in title for x in ["Category:", "List of", "History of", "Template:"]):
                continue

            try:
                extract = _get_page_extract(title)
            except Exception:
                skipped += 1
                continue

            if not extract:
                skipped += 1
                continue

            # Must look like a company
            extract_lower = extract.lower()
            company_signals = ["company", "corporation", "firm", "ltd", "inc.",
                               "gmbh", "b.v.", "breeder", "seed producer"]
            if not any(s in extract_lower for s in company_signals):
                skipped += 1
                continue

            country = _guess_country(extract)
            crops = ",".join(sorted({
                v for k, v in CROP_KEYWORDS.items() if k in extract_lower
            }))

            was_added, _ = upsert_company(
                conn,
                name=title,
                country=country,
                website="",
                description=extract[:400],
                crops=crops,
                source="wikipedia",
                source_url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            )
            if was_added:
                added += 1

        conn.commit()

    conn.close()
    return {"added": added, "skipped": skipped}


if __name__ == "__main__":
    r = run()
    print(f"Added {r['added']} companies, skipped {r['skipped']}")
