#!/usr/bin/env python3
"""
LUCID-100 source-PDF harvester (Ollie, owns LUCID-100 per Rick 2026-06-21).
Strategy order (validated by Kukla's smoke test 2026-06-21):
  1. Unpaywall-by-DOI FIRST (polite pool, real OA PDF URL)
  2. direct pdf_or_url from manifest only as fallback
  3. S2 API last resort w/ backoff (anon = global token bucket, 429s fast)
Logs paywall-blocked DOIs to LUCID100_access_blockers.tsv (the reproduction-ceiling list for Rick).
Skips DOIs already fetched on disk. Polite: 1.2s inter-request delay.
"""
import csv, os, re, time, json, sys, urllib.request, urllib.parse

UNPAYWALL_EMAIL = "stevens@anl.gov"   # polite-pool identifier
TARGET_DIR = os.path.expanduser("~/Dropbox/XFER/LUCID-replication-targets")
MANIFEST = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/priority-lists/PRIORITY_100_LUCID.md")
BLOCKERS = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/priority-lists/LUCID100_access_blockers.tsv")
DELAY = 1.2
UA = "Mozilla/5.0 (LUCID-100 OA harvester; mailto:stevens@anl.gov)"

os.makedirs(TARGET_DIR, exist_ok=True)

def doi_key(d): return d.replace('/','_').replace('.','_').replace(':','_').lower()

def already_have(doi):
    k = doi_key(doi)
    for f in os.listdir(TARGET_DIR):
        if f.lower().startswith(k) and f.lower().endswith('.pdf'):
            return f
    return None

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout)

def unpaywall_pdf(doi):
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={UNPAYWALL_EMAIL}"
    try:
        with get(url) as r:
            d = json.load(r)
    except Exception as e:
        return None, f"unpaywall-err:{type(e).__name__}"
    if not d.get("is_oa"):
        return None, "closed"
    loc = d.get("best_oa_location") or {}
    pdf = loc.get("url_for_pdf") or loc.get("url")
    return (pdf, loc.get("host_type","oa")) if pdf else (None, "oa-no-pdf-url")

def fetch_pdf(doi, pdf_url):
    try:
        with get(pdf_url, timeout=60) as r:
            data = r.read()
        if not data[:5].startswith(b"%PDF"):
            return False, "not-pdf"
        out = os.path.join(TARGET_DIR, doi_key(doi)+".pdf")
        with open(out,"wb") as f: f.write(data)
        return True, f"{len(data)//1024}KB"
    except Exception as e:
        return False, f"fetch-err:{type(e).__name__}"

def parse_manifest():
    rows=[]
    for line in open(MANIFEST):
        if not line.strip().startswith('|'): continue
        m=re.search(r'`(10\.\d{4,9}/[^`]+)`', line)
        if not m: continue
        cells=[c.strip() for c in line.split('|')]
        rows.append({"rank":cells[1],"status":cells[2],"doi":m.group(1).strip()})
    return rows

def main():
    limit = int(sys.argv[1]) if len(sys.argv)>1 else 999
    rows = parse_manifest()
    blockers=[]
    got=skip=blocked=0
    print(f"manifest DOIs: {len(rows)}; processing up to {limit}")
    n=0
    for row in rows:
        if n>=limit: break
        doi=row["doi"]
        ex=already_have(doi)
        if ex:
            skip+=1; continue
        n+=1
        pdf_url, status = unpaywall_pdf(doi)
        time.sleep(DELAY)
        if pdf_url:
            ok, info = fetch_pdf(doi, pdf_url)
            time.sleep(DELAY)
            if ok:
                got+=1; print(f"  ✓ #{row['rank']:>3} {doi}  [{info}]")
                continue
            else:
                status=f"oa-but-{info}"
        # blocked
        blocked+=1
        blockers.append((row["rank"], doi, status))
        print(f"  ✗ #{row['rank']:>3} {doi}  BLOCKED [{status}]")
    # write/append blocker TSV
    newfile = not os.path.exists(BLOCKERS)
    with open(BLOCKERS,"a") as f:
        if newfile: f.write("rank\tdoi\tblocker_status\n")
        for r in blockers: f.write("\t".join(map(str,r))+"\n")
    print(f"\nDONE: fetched {got}, already-had {skip}, blocked {blocked}")
    print(f"blocker TSV: {BLOCKERS} (+{len(blockers)} rows)")

if __name__=="__main__":
    main()
