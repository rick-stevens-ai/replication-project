#!/usr/bin/env python3
"""
LUCID-100 OA-recovery pass 2 (Ollie) — citation_pdf_url meta-tag hop.
Kukla's insight 2026-06-21: Unpaywall/landing pages return HTML; most publishers
embed <meta name="citation_pdf_url" content="...real.pdf"> (Google Scholar standard).
Strategy per blocker row: Unpaywall best_oa_location url → if HTML, parse
citation_pdf_url (+ a few fallbacks) → fetch the real PDF. Browser-like UA.
Updates LUCID100_access_blockers.tsv in place (removes recovered).
"""
import csv, os, re, time, json, urllib.request

TARGET_DIR=os.path.expanduser("~/Dropbox/XFER/LUCID-replication-targets")
BLOCKERS=os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/priority-lists/LUCID100_access_blockers.tsv")
EMAIL="stevens@anl.gov"
DELAY=1.0
UA=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

def dk(d): return d.replace('/','_').replace('.','_').replace(':','_').lower()
def have(doi):
    k=dk(doi)
    return any(f.lower().startswith(k) and f.lower().endswith('.pdf') for f in os.listdir(TARGET_DIR))

def opener(url, accept="*/*", timeout=40):
    req=urllib.request.Request(url, headers={"User-Agent":UA,"Accept":accept})
    return urllib.request.urlopen(req, timeout=timeout)

def unpaywall_loc(doi):
    try:
        with opener(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}") as r:
            d=json.load(r)
        loc=d.get("best_oa_location") or {}
        return loc.get("url_for_pdf") or loc.get("url") or loc.get("url_for_landing_page")
    except Exception: return None

import urllib.parse
META_RES=[
    re.compile(rb'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', re.I),
    re.compile(rb'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']', re.I),
]
def extract_pdf_url(html, base):
    for rx in META_RES:
        m=rx.search(html)
        if m:
            return urllib.parse.urljoin(base, m.group(1).decode('utf-8','ignore'))
    return None

def try_fetch(doi, url, depth=0):
    if not url or depth>2: return False,"no-url"
    try:
        with opener(url, accept="application/pdf,text/html") as r:
            ctype=r.headers.get("Content-Type","")
            data=r.read()
            final=r.geturl()
    except Exception as e:
        return False,f"err:{type(e).__name__}"
    if data[:5].startswith(b"%PDF"):
        out=os.path.join(TARGET_DIR,dk(doi)+".pdf")
        open(out,"wb").write(data)
        return True,f"{len(data)//1024}KB"
    # HTML → meta-tag hop
    if b"<html" in data[:2000].lower() or "html" in ctype.lower():
        pdfu=extract_pdf_url(data, final)
        if pdfu and pdfu!=url:
            time.sleep(DELAY)
            return try_fetch(doi, pdfu, depth+1)
        return False,"html-no-citation_pdf_url"
    return False,"not-pdf"

def main():
    rows=list(csv.DictReader(open(BLOCKERS),delimiter='\t'))
    targets=[r for r in rows if r["blocker_status"].startswith("oa-but") or "unpaywall-err" in r["blocker_status"]]
    print(f"meta-tag recovery targets: {len(targets)}/{len(rows)}")
    rec=set()
    for r in targets:
        doi=r["doi"].rstrip("/").replace("/full","")
        if have(doi): rec.add(r["doi"]); print(f"  ✓ #{r['rank']} on disk"); continue
        loc=unpaywall_loc(doi); time.sleep(DELAY)
        ok,info=try_fetch(doi,loc); time.sleep(DELAY)
        if ok: rec.add(r["doi"]); print(f"  ✓ #{r['rank']:>3} {doi} RECOVERED [{info}]")
        else: print(f"  ✗ #{r['rank']:>3} {doi} [{info}]")
    kept=[r for r in rows if r["doi"] not in rec]
    with open(BLOCKERS,"w") as f:
        f.write("rank\tdoi\tblocker_status\n")
        for r in kept: f.write(f"{r['rank']}\t{r['doi']}\t{r['blocker_status']}\n")
    print(f"\nRECOVERED {len(rec)} via citation_pdf_url hop. Blockers remaining: {len(kept)}")

if __name__=="__main__": main()
