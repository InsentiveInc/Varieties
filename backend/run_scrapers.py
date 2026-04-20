"""
Orchestrator - runs all scrapers and loads the curated seed list.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import get_db, init_db, upsert_company
from scrapers.seed_list import SEED_COMPANIES
from scrapers import news_rss, wikipedia


def load_curated():
    conn = get_db()
    added = 0
    for c in SEED_COMPANIES:
        was_added, _ = upsert_company(conn, **c)
        if was_added:
            added += 1
    conn.commit()
    conn.close()
    return added


def run_all(skip_wiki=False):
    init_db()
    print("=" * 60)
    print("VARIETIES - data refresh")
    print("=" * 60)

    print("\n[1/3] Loading curated seed company list...")
    n = load_curated()
    print(f"      Added {n} new curated companies "
          f"(total curated: {len(SEED_COMPANIES)})")

    if not skip_wiki:
        print("\n[2/3] Scraping Wikipedia seed-company categories...")
        t0 = time.time()
        try:
            r = wikipedia.run()
            print(f"      Added {r['added']} companies from Wikipedia "
                  f"(skipped {r['skipped']}) in {time.time()-t0:.1f}s")
        except Exception as e:
            print(f"      FAILED: {e}")
    else:
        print("\n[2/3] Skipping Wikipedia.")

    print("\n[3/3] Fetching industry news feeds...")
    t0 = time.time()
    try:
        r = news_rss.run()
        print(f"      Added {r['added']} new, updated {r['updated']} existing "
              f"in {time.time()-t0:.1f}s")
        if r["failed_feeds"]:
            print(f"      {len(r['failed_feeds'])} feed(s) failed:")
            for src, err in r["failed_feeds"][:5]:
                print(f"        - {src}: {err}")
    except Exception as e:
        print(f"      FAILED: {e}")

    conn = get_db()
    total_c = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_n = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    conn.close()
    print("\n" + "=" * 60)
    print(f"Done. Directory: {total_c} companies | News: {total_n} items")
    print("=" * 60)


if __name__ == "__main__":
    skip = "--skip-wiki" in sys.argv
    run_all(skip_wiki=skip)
