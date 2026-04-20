"""
Database layer. SQLite for simplicity, upgradeable to Postgres later.

v2 changes:
- news table gets: content, crops, regions, image_url fields
- a small migration runs on init_db for existing databases
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "varieties.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _migrate(cur):
    """Add any new columns to existing tables. Safe to run multiple times."""
    existing = {row[1] for row in cur.execute("PRAGMA table_info(news)")}
    for col, decl in [
        ("content", "TEXT DEFAULT ''"),
        ("crops", "TEXT DEFAULT ''"),
        ("regions", "TEXT DEFAULT ''"),
        ("image_url", "TEXT DEFAULT ''"),
    ]:
        if col not in existing:
            cur.execute(f"ALTER TABLE news ADD COLUMN {col} {decl}")


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_normalized TEXT NOT NULL,
            country TEXT DEFAULT '',
            website TEXT DEFAULT '',
            description TEXT DEFAULT '',
            crops TEXT DEFAULT '',
            source TEXT DEFAULT '',
            source_url TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name_normalized, country)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_companies_country ON companies(country)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_companies_crops ON companies(crops)")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            summary TEXT DEFAULT '',
            content TEXT DEFAULT '',
            source TEXT DEFAULT '',
            published_at TEXT DEFAULT '',
            crops TEXT DEFAULT '',
            regions TEXT DEFAULT '',
            image_url TEXT DEFAULT '',
            fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_at DESC)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_news_source ON news(source)")

    _migrate(cur)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS run_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scraper TEXT NOT NULL,
            ran_at TEXT DEFAULT CURRENT_TIMESTAMP,
            items_added INTEGER DEFAULT 0,
            items_updated INTEGER DEFAULT 0,
            status TEXT DEFAULT '',
            error TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def normalize_name(name: str) -> str:
    import re
    if not name:
        return ""
    s = name.lower().strip()
    for suffix in [" co., ltd.", " co., ltd", " co.,ltd", " co ltd", " ltd.", " ltd",
                   " inc.", " inc", " llc", " gmbh", " s.a.", " sa", " ag", " bv",
                   " b.v.", " corporation", " corp.", " corp", " limited"]:
        if s.endswith(suffix):
            s = s[: -len(suffix)]
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def upsert_company(conn, *, name, country="", website="", description="",
                    crops="", source="", source_url=""):
    cur = conn.cursor()
    norm = normalize_name(name)
    if not norm:
        return False, None

    existing = cur.execute(
        "SELECT id, website, description, crops FROM companies WHERE name_normalized = ? AND country = ?",
        (norm, country),
    ).fetchone()

    if existing:
        new_website = existing["website"] or website
        new_description = existing["description"] or description
        existing_crops = set(c.strip() for c in (existing["crops"] or "").split(",") if c.strip())
        new_crops = set(c.strip() for c in (crops or "").split(",") if c.strip())
        merged_crops = ",".join(sorted(existing_crops | new_crops))
        cur.execute(
            """UPDATE companies
               SET website=?, description=?, crops=?, updated_at=CURRENT_TIMESTAMP
               WHERE id=?""",
            (new_website, new_description, merged_crops, existing["id"]),
        )
        return False, existing["id"]
    else:
        cur.execute(
            """INSERT INTO companies
               (name, name_normalized, country, website, description, crops, source, source_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, norm, country, website, description, crops, source, source_url),
        )
        return True, cur.lastrowid


def upsert_news(conn, *, title, link, summary="", content="", source="",
                published_at="", crops="", regions="", image_url=""):
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO news (title, link, summary, content, source,
                                  published_at, crops, regions, image_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, link, summary, content, source, published_at,
             crops, regions, image_url),
        )
        return True
    except sqlite3.IntegrityError:
        # already exists - update crops/regions in case our tagging improved
        cur.execute(
            """UPDATE news SET crops=?, regions=?, image_url=COALESCE(NULLIF(?, ''), image_url)
               WHERE link=?""",
            (crops, regions, image_url, link),
        )
        return False
