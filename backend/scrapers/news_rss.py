"""
News scraper v3 - expanded feed list.

Covers: seed industry, vegetable/produce, greenhouse/horticulture, general ag,
biotech/breeding research, regional ag (EU, Asia, LatAm, Africa), ag business.

Feeds may go dead over time. The scraper logs failures and skips them without
breaking the run. Prune or replace feeds from /api/news/meta/facets if you
see them show up empty over multiple runs.
"""
import feedparser
import re
import html as html_module
from datetime import datetime
from database import get_db, upsert_news

# ---------------------------------------------------------------------------
# Feed list - grouped by category for readability
# ---------------------------------------------------------------------------
FEEDS = [
    # ===== Seed industry =====
    ("Seed World",                      "https://www.seedworld.com/feed/"),
    ("Seed World Europe",               "https://www.seedworldeurope.com/feed/"),
    ("Seed World LATAM",                "https://www.seedworldlatam.com/feed/"),
    ("Seed Today",                      "https://www.seedtoday.com/rss/news.rss"),
    ("European Seed",                   "https://european-seed.com/feed/"),
    ("Asian Seed (APSA)",               "https://apsaseed.org/feed/"),
    ("ISF News",                        "https://worldseed.org/feed/"),
    ("Seed Quest",                      "https://www.seedquest.com/rss/news.xml"),
    ("AgriBusiness Global",             "https://www.agribusinessglobal.com/feed/"),

    # ===== Produce / fresh / vegetable =====
    ("HortiDaily",                      "https://www.hortidaily.com/rss/"),
    ("Fresh Plaza",                     "https://www.freshplaza.com/rss/"),
    ("Vegetable Growers News",          "https://vegetablegrowersnews.com/feed/"),
    ("Produce Grower",                  "https://www.producegrower.com/rss"),
    ("Growing Produce",                 "https://www.growingproduce.com/feed/"),
    ("The Packer",                      "https://www.thepacker.com/rss.xml"),
    ("The Packer — News",               "https://www.thepacker.com/news/feed"),
    ("Produce Blue Book",               "https://www.producebluebook.com/feed/"),
    ("Produce Processing",              "https://www.produceprocessing.net/feed/"),
    ("Fruit Growers News",              "https://fruitgrowersnews.com/feed/"),
    ("Fresh Fruit Portal",              "https://www.freshfruitportal.com/feed/"),
    ("Produce Business",                "https://www.producebusiness.com/feed/"),
    ("Produce Market Guide",            "https://www.producemarketguide.com/rss.xml"),
    ("Potato News Today",               "https://www.potatonewstoday.com/feed/"),
    ("AndNowUKnow",                     "https://www.andnowuknow.com/rss.xml"),

    # ===== Greenhouse / horticulture / indoor ag =====
    ("Greenhouse Grower",               "https://www.greenhousegrower.com/feed/"),
    ("Greenhouse Management",           "https://www.greenhousemag.com/rss"),
    ("Greenhouse Canada",               "https://www.greenhousecanada.com/feed/"),
    ("Greenhouse Product News",         "https://gpnmag.com/feed/"),
    ("Urban Ag News",                   "https://urbanagnews.com/feed/"),
    ("Nursery Management",              "https://www.nurserymag.com/rss"),
    ("Floral Daily",                    "https://www.floraldaily.com/rss/"),
    ("FloraCulture International",      "https://www.floracultureinternational.com/feed/"),

    # ===== General agriculture & ag-tech =====
    ("AgFunder News",                   "https://agfundernews.com/feed"),
    ("AgWeb",                           "https://www.agweb.com/rss.xml"),
    ("Successful Farming",              "https://www.agriculture.com/feed"),
    ("Farm Progress",                   "https://www.farmprogress.com/rss.xml"),
    ("AgDaily",                         "https://www.agdaily.com/feed/"),
    ("Farm Journal",                    "https://www.agweb.com/farm-journal/rss.xml"),
    ("Modern Farmer",                   "https://modernfarmer.com/feed/"),
    ("Food Navigator",                  "https://www.foodnavigator.com/rss"),
    ("Food Navigator USA",              "https://www.foodnavigator-usa.com/rss"),
    ("AgriNews",                        "https://www.agrinews-pubs.com/feed/"),
    ("Feedstuffs",                      "https://www.feedstuffs.com/rss.xml"),
    ("Civil Eats",                      "https://civileats.com/feed/"),
    ("Ag Alert",                        "https://www.agalert.com/rss.xml"),
    ("Western Farm Press",              "https://www.farmprogress.com/western-farm-press/rss.xml"),
    ("Drovers",                         "https://www.drovers.com/rss.xml"),

    # ===== Biotech / breeding / research =====
    ("Crop Biotech Update (ISAAA)",     "https://www.isaaa.org/kc/cropbiotechupdate/rss/default.asp"),
    ("Genetic Literacy Project",        "https://geneticliteracyproject.org/feed/"),
    ("AgroPages",                       "http://news.agropages.com/rss/news/"),
    ("Phys.org Agriculture",            "https://phys.org/rss-feed/biology-news/agriculture/"),
    ("Phys.org Plants & Animals",       "https://phys.org/rss-feed/biology-news/plants-animals/"),
    ("Science Daily Agriculture",       "https://www.sciencedaily.com/rss/plants_animals/agriculture_and_food.xml"),
    ("Science Daily Plant Biology",     "https://www.sciencedaily.com/rss/plants_animals/botany.xml"),
    ("Nature Plants",                   "https://www.nature.com/nplants.rss"),
    ("Plant Cell (AAAS)",               "https://academic.oup.com/rss/site_5127/3090.xml"),

    # ===== Public research institutions =====
    ("USDA ARS News",                   "https://www.ars.usda.gov/news-events/news/rss/"),
    ("Wageningen University",           "https://www.wur.nl/en/rss.htm"),
    ("CGIAR News",                      "https://www.cgiar.org/news/feed/"),
    ("World Vegetable Center",          "https://avrdc.org/feed/"),
    ("EUCARPIA",                        "https://eucarpia.org/feed/"),

    # ===== Regional: Europe =====
    ("Agriland (Ireland)",              "https://www.agriland.ie/feed/"),
    ("Farmers Weekly (UK)",             "https://www.fwi.co.uk/feed"),
    ("Farmers Guardian",                "https://www.fginsight.com/rss"),
    ("Sud-Ouest Agricole",              "https://www.lafranceagricole.fr/rss"),
    ("AgriFood World",                  "https://www.euractiv.com/sections/agriculture-food/feed/"),

    # ===== Regional: Asia & Oceania =====
    ("ABC Rural (Australia)",           "https://www.abc.net.au/news/feed/7866/rss.xml"),
    ("Farm Weekly (Australia)",         "https://www.farmweekly.com.au/rss.xml"),
    ("Rural News Group (NZ)",           "https://www.ruralnewsgroup.co.nz/rural-news/feed.rss"),
    ("Krishi Jagran (India)",           "https://krishijagran.com/rss/agriculture-world.xml"),
    ("The Hindu BusinessLine Agri",     "https://www.thehindubusinessline.com/economy/agri-business/feeds/rss/"),
    ("China Daily Agriculture",         "https://www.chinadaily.com.cn/rss/bizchina_rss.xml"),

    # ===== Regional: Americas =====
    ("Agro Brasil",                     "https://www.agrolink.com.br/rss.aspx"),
    ("Successful Farming LA",           "https://www.laprensalatina.com/feed/?cat=agriculture"),
    ("Portal do Agronegocio",           "https://www.portaldoagronegocio.com.br/rss/noticias"),

    # ===== Regional: Africa =====
    ("African Farming",                 "https://www.africanfarming.com/feed/"),
    ("Farmers Review Africa",           "https://farmersreviewafrica.com/feed/"),
    ("Food for Mzansi",                 "https://www.foodformzansi.co.za/feed/"),

    # ===== Ag business / trade =====
    ("Progressive Farmer (DTN)",        "https://www.dtnpf.com/agriculture/web/ag/news/rss-feed.xml"),
    ("Reuters Agriculture",             "https://www.reutersagency.com/feed/?best-sectors=agriculture&post_type=best"),

    # ===== Organic / sustainable =====
    ("Rodale Institute",                "https://rodaleinstitute.org/feed/"),
    ("Organic Grower",                  "https://organicgrower.info/feed/"),
    ("Sustainable Food Trust",          "https://sustainablefoodtrust.org/feed/"),
]

# Deduplicate by URL (in case entries got duplicated by accident)
_seen = set()
FEEDS = [(n, u) for (n, u) in FEEDS if not (u in _seen or _seen.add(u))]


# ---------------------------------------------------------------------------
# Relevance and tagging
# ---------------------------------------------------------------------------
# We keep the keyword list broad because general-ag feeds carry lots of items,
# and we want to filter for things growers and breeders actually care about.
SEED_KEYWORDS = [
    # Core seed / breeding
    "seed", "breed", "variety", "varieties", "cultivar", "hybrid",
    "genetics", "germplasm", "genome", "phenotype", "rootstock",
    "traits", "trait ", "gene edit", "crispr", "gmo", "biotech",
    # Crops
    "tomato", "pepper", "cucumber", "melon", "watermelon", "lettuce",
    "onion", "broccoli", "carrot", "cabbage", "spinach", "eggplant",
    "aubergine", "bean", "pea ", "corn", "maize", "squash", "pumpkin",
    "potato", "strawberry", "berries", "brassica", "cucurbit",
    "capsicum", "chili", "leafy", "vegetable", "horticulture",
    # Context
    "greenhouse", "indoor farm", "vertical farm", "protected cultivation",
    "plant breed", "open field", "glasshouse", "fresh produce",
    # Diseases / pathology
    "tobrfv", "tospovirus", "powdery mildew", "downy mildew", "nematode",
    "virus resistan", "disease resistan", "tyl", "tswv",
]

CROP_TAGS = {
    "tomato":     ["tomato", "tomatoes"],
    "pepper":     ["pepper", "peppers", "capsicum", "bell pepper", "chili", "chilli"],
    "cucumber":   ["cucumber", "cucumbers", "cucurbit"],
    "melon":      ["melon", "cantaloupe", "muskmelon", "honeydew"],
    "watermelon": ["watermelon"],
    "lettuce":    ["lettuce"],
    "onion":      ["onion", "shallot"],
    "carrot":     ["carrot"],
    "cabbage":    ["cabbage", "brassica"],
    "broccoli":   ["broccoli"],
    "cauliflower":["cauliflower"],
    "eggplant":   ["eggplant", "aubergine", "brinjal"],
    "spinach":    ["spinach"],
    "bean":       ["bean", "snap bean", "green bean"],
    "pea":        ["pea ", "peas"],
    "corn":       ["corn", "maize", "sweet corn"],
    "strawberry": ["strawberry", "strawberries"],
    "blueberry":  ["blueberry", "blueberries"],
    "potato":     ["potato", "potatoes"],
    "squash":     ["squash", "zucchini", "pumpkin", "courgette"],
    "herbs":      ["basil", "cilantro", "parsley", " mint ", "oregano"],
    "flowers":    ["flower ", "flowers", "ornamental", "petunia", "geranium", "rose "],
    "cotton":     ["cotton"],
    "soybean":    ["soybean", "soya"],
    "rice":       ["rice "],
    "wheat":      ["wheat"],
    "apple":      ["apple", "apples"],
    "grape":      ["grape", "grapes", "vineyard"],
    "citrus":     ["citrus", "orange", "lemon", "lime", "grapefruit", "mandarin"],
    "banana":     ["banana"],
    "avocado":    ["avocado"],
    "mushroom":   ["mushroom"],
}

REGION_TAGS = {
    "United States":  ["united states", "u.s.", " us ", "usa", "american", "california",
                       "florida", "texas", "washington state", "michigan", "oregon",
                       "idaho", "iowa", "georgia", "north carolina", "pennsylvania"],
    "Canada":         ["canada", "canadian", "ontario", "quebec", "british columbia",
                       "alberta", "saskatchewan"],
    "Mexico":         ["mexico", "mexican", "sinaloa", "baja california"],
    "Netherlands":    ["netherlands", "dutch", "holland", "wageningen", "enkhuizen",
                       "de lier", "westland"],
    "Germany":        ["germany", "german "],
    "France":         ["france", "french ", "provence"],
    "Spain":          ["spain", "spanish", "almeria", "murcia", "valencia"],
    "Italy":          ["italy", "italian "],
    "United Kingdom": ["united kingdom", " uk ", " u.k.", "britain", "british", "england",
                       "scotland", "wales"],
    "Ireland":        ["ireland", "irish"],
    "Belgium":        ["belgium", "belgian"],
    "Poland":         ["poland", "polish"],
    "Turkey":         ["turkey", "turkish", "antalya"],
    "Greece":         ["greece", "greek "],
    "Israel":         ["israel", "israeli"],
    "Egypt":          ["egypt", "egyptian"],
    "Morocco":        ["morocco", "moroccan"],
    "Russia":         ["russia", "russian"],
    "Ukraine":        ["ukraine", "ukrainian"],
    "China":          ["china", "chinese", "shandong", "beijing", "shanghai"],
    "Japan":          ["japan", "japanese"],
    "South Korea":    ["south korea", "korean", "seoul"],
    "India":          ["india ", "indian ", "bengaluru", "hyderabad", "punjab"],
    "Pakistan":       ["pakistan"],
    "Thailand":       ["thailand", "thai "],
    "Vietnam":        ["vietnam"],
    "Indonesia":      ["indonesia"],
    "Philippines":    ["philippines", "filipino"],
    "Taiwan":         ["taiwan", "taiwanese"],
    "Malaysia":       ["malaysia"],
    "Australia":      ["australia", "australian", "queensland", "victoria"],
    "New Zealand":    ["new zealand"],
    "Brazil":         ["brazil", "brazilian", "sao paulo"],
    "Argentina":      ["argentina", "argentine"],
    "Chile":          ["chile ", "chilean"],
    "Peru":           ["peru ", "peruvian"],
    "Colombia":       ["colombia", "colombian"],
    "South Africa":   ["south africa", "south african"],
    "Kenya":          ["kenya", "kenyan"],
    "Ethiopia":       ["ethiopia", "ethiopian"],
    "Nigeria":        ["nigeria", "nigerian"],
}

# ---------------------------------------------------------------------------
# Cleaning and extraction (unchanged from v2)
# ---------------------------------------------------------------------------
BOILERPLATE_PATTERNS = [
    re.compile(r"The post .*? appeared first on .*?\.?\s*$", re.I | re.S),
    re.compile(r"Continue reading .*?$", re.I),
    re.compile(r"Read more.*?$", re.I),
    re.compile(r"\[&#?8230;?\]"),
    re.compile(r"\[\s*\.\.\.\s*\]"),
    re.compile(r"Click here to read.*?$", re.I),
    re.compile(r"This article.*?appeared.*?$", re.I),
    re.compile(r"^\s*Related:.*?$", re.I | re.M),
    re.compile(r"^\s*Share this article.*?$", re.I | re.M),
    re.compile(r"Source:\s*\S+\s*$", re.I),
    re.compile(r"Photo(?:s)?\s+courtesy\s+of.*?$", re.I),
    re.compile(r"Image\s*:?\s*\S.*?$", re.I),
]


def _strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_module.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _strip_boilerplate(s: str) -> str:
    for pat in BOILERPLATE_PATTERNS:
        s = pat.sub("", s)
    return s.strip()


def _pick_best_body(entry) -> str:
    content_list = entry.get("content") or []
    for c in content_list:
        val = c.get("value") or ""
        if val and len(val) > 100:
            return val
    if entry.get("summary_detail", {}).get("value"):
        return entry["summary_detail"]["value"]
    return entry.get("summary") or entry.get("description") or ""


def _smart_summary(text: str, max_chars: int = 360) -> str:
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    out = ""
    for s in sentences:
        if len(out) + len(s) + 1 > max_chars and out:
            break
        out = (out + " " + s).strip()
    if not out:
        cut = text[:max_chars].rsplit(" ", 1)[0]
        return cut + "…"
    return out


def _extract_image(entry) -> str:
    for key in ("media_content", "media_thumbnail"):
        items = entry.get(key) or []
        for item in items:
            url = item.get("url") or ""
            if url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                return url
            if url:
                return url
    for enc in entry.get("enclosures") or []:
        url = enc.get("href") or enc.get("url") or ""
        typ = enc.get("type") or ""
        if typ.startswith("image/") and url:
            return url
    for c in (entry.get("content") or []):
        m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', c.get("value") or "", re.I)
        if m:
            return m.group(1)
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', entry.get("summary") or "", re.I)
    if m:
        return m.group(1)
    return ""


def _tag_crops(text: str) -> str:
    tl = text.lower()
    hits = []
    for crop, keywords in CROP_TAGS.items():
        for kw in keywords:
            if kw in tl:
                hits.append(crop)
                break
    return ",".join(sorted(set(hits)))


def _tag_regions(text: str) -> str:
    tl = " " + text.lower() + " "
    hits = []
    for region, keywords in REGION_TAGS.items():
        for kw in keywords:
            if kw in tl:
                hits.append(region)
                break
    return ",".join(sorted(set(hits)))


def _is_relevant(title: str, body_text: str) -> bool:
    text = (title + " " + body_text).lower()
    return any(k in text for k in SEED_KEYWORDS)


def _parse_date(entry) -> str:
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            try:
                return datetime(*t[:6]).isoformat()
            except Exception:
                pass
    return datetime.utcnow().isoformat()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run():
    conn = get_db()
    added = 0
    updated = 0
    failed_feeds = []
    empty_feeds = []

    total = len(FEEDS)
    print(f"      Pulling from {total} feeds...")

    for i, (source, url) in enumerate(FEEDS, 1):
        try:
            parsed = feedparser.parse(url, request_headers={
                "User-Agent": "Mozilla/5.0 (compatible; Varieties/1.0; +https://varieties.nicojones.ca)"
            })
            if parsed.bozo and not parsed.entries:
                failed_feeds.append((source, str(parsed.bozo_exception)[:120]))
                continue

            if not parsed.entries:
                empty_feeds.append(source)
                continue

            feed_added = 0
            for entry in parsed.entries[:60]:
                title = _strip_html(entry.get("title", "")).strip()
                link = entry.get("link", "").strip()
                if not title or not link:
                    continue

                raw_body = _pick_best_body(entry)
                body_text = _strip_boilerplate(_strip_html(raw_body))

                if not _is_relevant(title, body_text):
                    continue

                summary = _smart_summary(body_text, max_chars=340)
                image_url = _extract_image(entry)
                published = _parse_date(entry)

                tag_source_text = title + " " + body_text
                crops = _tag_crops(tag_source_text)
                regions = _tag_regions(tag_source_text)

                was_added = upsert_news(
                    conn,
                    title=title,
                    link=link,
                    summary=summary,
                    content=body_text[:4000],
                    source=source,
                    published_at=published,
                    crops=crops,
                    regions=regions,
                    image_url=image_url,
                )
                if was_added:
                    added += 1
                    feed_added += 1
                else:
                    updated += 1

            # commit after each feed so a late crash doesn't lose earlier work
            conn.commit()

        except Exception as e:
            failed_feeds.append((source, str(e)[:120]))

    conn.close()
    return {
        "added": added,
        "updated": updated,
        "failed_feeds": failed_feeds,
        "empty_feeds": empty_feeds,
        "total_feeds": total,
    }


if __name__ == "__main__":
    result = run()
    print(f"Added {result['added']} new, updated tags on {result['updated']} existing")
    print(f"Feeds: {result['total_feeds']} total, "
          f"{len(result['failed_feeds'])} failed, "
          f"{len(result['empty_feeds'])} empty")
    if result["failed_feeds"]:
        print("\nFailed feeds:")
        for src, err in result["failed_feeds"]:
            print(f"  {src}: {err}")
    if result["empty_feeds"]:
        print("\nEmpty feeds (no entries returned):")
        for src in result["empty_feeds"]:
            print(f"  {src}")
