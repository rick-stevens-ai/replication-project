#!/usr/bin/env python3
"""Download OSTI abstracts with subject categories via public API.

Strategy: paginate through search API. Each record keeps: osti_id, title,
abstract (description), primary_subject (leading numeric code from first
subject entry), all_subjects.
"""
import json, os, re, sys, time, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

API = "https://www.osti.gov/api/v1/records"
CODE_RE = re.compile(r"^\s*(\d{1,3})\s+(.*)")

def parse_primary_subject(subjects):
    if not subjects:
        return None, None
    first = subjects[0]
    m = CODE_RE.match(first)
    if not m:
        return None, first
    return int(m.group(1)), m.group(2).strip()

def fetch_page(page, rows, product_type=None, params_extra=None):
    params = {"rows": rows, "page": page, "format": "json"}
    if product_type:
        params["product_type"] = product_type
    if params_extra:
        params.update(params_extra)
    for attempt in range(4):
        try:
            r = requests.get(API, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
            time.sleep(2 + attempt*2)
        except Exception as e:
            time.sleep(2 + attempt*2)
    return []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--target", type=int, default=60000)
    ap.add_argument("--rows", type=int, default=100)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--start-page", type=int, default=0)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    seen = set()
    n_kept = 0
    out_f = open(args.out, "w")
    page = args.start_page
    t0 = time.time()
    while n_kept < args.target:
        # Fetch a batch of pages in parallel
        batch_pages = list(range(page, page + args.workers))
        page += args.workers
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(fetch_page, p, args.rows): p for p in batch_pages}
            for fut in as_completed(futures):
                recs = fut.result() or []
                if not recs:
                    continue
                for rec in recs:
                    oid = rec.get("osti_id")
                    if not oid or oid in seen:
                        continue
                    seen.add(oid)
                    desc = (rec.get("description") or "").strip()
                    title = (rec.get("title") or "").strip()
                    subjects = rec.get("subjects") or []
                    if not desc or len(desc) < 100:
                        continue
                    prim_code, prim_name = parse_primary_subject(subjects)
                    if prim_code is None:
                        continue
                    out_f.write(json.dumps({
                        "osti_id": oid,
                        "title": title,
                        "abstract": desc,
                        "primary_code": prim_code,
                        "primary_name": prim_name,
                        "subjects": subjects,
                    }) + "\n")
                    n_kept += 1
        if page % 50 < args.workers:
            elapsed = time.time() - t0
            print(f"page={page} kept={n_kept} elapsed={elapsed:.0f}s rate={n_kept/max(elapsed,1):.1f}/s", flush=True)
        if n_kept >= args.target:
            break
    out_f.close()
    print(f"DONE: kept={n_kept} pages_to={page}")

if __name__ == "__main__":
    main()
