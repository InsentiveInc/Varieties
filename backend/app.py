"""
Varieties - FastAPI application (v2).

News endpoint now supports:
- crop filter (multiple, comma-separated)
- region filter (multiple, comma-separated)
- source filter (multiple, comma-separated)
- date range (from/to, ISO dates)
- date grouping in the response (today / yesterday / this_week / this_month / older)
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
from pathlib import Path
from datetime import datetime, timezone

from database import get_db, init_db

app = FastAPI(title="Varieties", description="Seed Industry Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ============================================================
# Companies
# ============================================================
@app.get("/api/companies")
def list_companies(
    q: Optional[str] = None,
    country: Optional[str] = None,
    crop: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
):
    conn = get_db()
    cur = conn.cursor()

    where, params = [], []
    if q:
        where.append("(name LIKE ? OR country LIKE ? OR description LIKE ? OR crops LIKE ?)")
        like = f"%{q}%"
        params += [like, like, like, like]
    if country:
        where.append("country = ?")
        params.append(country)
    if crop:
        where.append("crops LIKE ?")
        params.append(f"%{crop.lower()}%")

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    total = cur.execute(f"SELECT COUNT(*) FROM companies {where_sql}", params).fetchone()[0]

    rows = cur.execute(
        f"""SELECT id, name, country, website, description, crops, source, updated_at
            FROM companies {where_sql}
            ORDER BY name COLLATE NOCASE LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()
    conn.close()
    return {"total": total, "limit": limit, "offset": offset,
            "items": [dict(r) for r in rows]}


@app.get("/api/companies/{company_id}")
def get_company(company_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"error": "not found"}


# ============================================================
# News
# ============================================================
def _csv_to_list(s: Optional[str]) -> List[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def _date_bucket(published_at: str) -> str:
    """Classify an article by recency for front-end grouping."""
    if not published_at:
        return "older"
    try:
        d = datetime.fromisoformat(published_at.replace("Z", ""))
    except Exception:
        return "older"
    now = datetime.utcnow()
    delta_days = (now.date() - d.date()).days
    if delta_days <= 0:
        return "today"
    if delta_days == 1:
        return "yesterday"
    if delta_days <= 7:
        return "this_week"
    if delta_days <= 30:
        return "this_month"
    return "older"


@app.get("/api/news")
def list_news(
    q: Optional[str] = None,
    crops: Optional[str] = Query(None, description="Comma-separated, e.g. tomato,pepper"),
    regions: Optional[str] = Query(None, description="Comma-separated, e.g. Netherlands,China"),
    sources: Optional[str] = Query(None, description="Comma-separated feed names"),
    date_from: Optional[str] = Query(None, description="ISO date, e.g. 2026-01-01"),
    date_to: Optional[str] = Query(None, description="ISO date, e.g. 2026-04-19"),
    limit: int = 40,
    offset: int = 0,
):
    conn = get_db()
    cur = conn.cursor()

    where, params = [], []
    if q:
        where.append("(title LIKE ? OR summary LIKE ? OR content LIKE ?)")
        like = f"%{q}%"
        params += [like, like, like]

    crop_list = _csv_to_list(crops)
    if crop_list:
        sub = " OR ".join(["crops LIKE ?" for _ in crop_list])
        where.append(f"({sub})")
        params += [f"%{c}%" for c in crop_list]

    region_list = _csv_to_list(regions)
    if region_list:
        sub = " OR ".join(["regions LIKE ?" for _ in region_list])
        where.append(f"({sub})")
        params += [f"%{r}%" for r in region_list]

    source_list = _csv_to_list(sources)
    if source_list:
        sub = ",".join(["?"] * len(source_list))
        where.append(f"source IN ({sub})")
        params += source_list

    if date_from:
        where.append("published_at >= ?")
        params.append(date_from)
    if date_to:
        # inclusive end-of-day
        where.append("published_at <= ?")
        params.append(date_to + "T23:59:59")

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    total = cur.execute(f"SELECT COUNT(*) FROM news {where_sql}", params).fetchone()[0]

    rows = cur.execute(
        f"""SELECT id, title, link, summary, source, published_at,
                   crops, regions, image_url
            FROM news {where_sql}
            ORDER BY published_at DESC, id DESC
            LIMIT ? OFFSET ?""",
        params + [limit, offset],
    ).fetchall()
    conn.close()

    items = []
    for r in rows:
        d = dict(r)
        d["bucket"] = _date_bucket(d["published_at"])
        items.append(d)

    return {"total": total, "limit": limit, "offset": offset, "items": items}


@app.get("/api/news/{news_id}")
def get_news(news_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM news WHERE id = ?", (news_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"error": "not found"}


@app.get("/api/news/meta/facets")
def news_facets():
    """Return available crops, regions, sources for building the filter UI."""
    conn = get_db()
    cur = conn.cursor()

    def split_tags(col):
        vals = set()
        for row in cur.execute(f"SELECT {col} FROM news WHERE {col} != ''"):
            for v in (row[0] or "").split(","):
                v = v.strip()
                if v:
                    vals.add(v)
        return sorted(vals)

    crops = split_tags("crops")
    regions = split_tags("regions")
    sources = [r[0] for r in cur.execute(
        "SELECT source FROM news WHERE source != '' GROUP BY source ORDER BY COUNT(*) DESC"
    )]

    conn.close()
    return {"crops": crops, "regions": regions, "sources": sources}


# ============================================================
# Stats
# ============================================================
@app.get("/api/stats")
def stats():
    conn = get_db()
    cur = conn.cursor()
    total_companies = cur.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_news = cur.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    countries = cur.execute(
        "SELECT COUNT(DISTINCT country) FROM companies WHERE country != ''"
    ).fetchone()[0]
    tomato = cur.execute(
        "SELECT COUNT(*) FROM companies WHERE crops LIKE '%tomato%'"
    ).fetchone()[0]
    conn.close()
    return {
        "companies": total_companies,
        "news": total_news,
        "countries": countries,
        "tomato_companies": tomato,
    }


# ============================================================
# Static frontend
# ============================================================
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
