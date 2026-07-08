#!/usr/bin/env python3
"""
LUCID-100 OA-recovery pass (Ollie). Targets the 47 'oa-but-*' blocker rows that
are OA but my naive urllib fetch failed on (403 bot-block / landing page).
Strategy: Semantic Scholar API (WITH key) openAccessPdf field → direct PDF URL,
plus a browser-like User-Agent. Updates blocker TSV in place: removes recovered,
keeps the rest.
"""
import csv, os, re, time, json, sys, subprocess, urllib.request

TARGET_DIR = os.path.expanduser("~/Dropbox/XFER/LUCID-replication-targets")
BLOCKERS = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/priority-lists/LUCID100_access_blockers.tsv")
DELAY = 1.1

# S2 key from keychain (fallback to env)
def s2_key():
    try:
        k = subprocess.check_output(
            ["security","find-generic-password","-a","rick-stevens-ai","-s","semantic-scholar-api-key","-w"],
            text=True).strip()
        if k: return k
    except Exception: pass
    return os.environ.get("S2_API_KEY","")

S2KEY = s2_key()
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

def doi_key(d): return d.replace('/','_').replace('.','_').replace(':','_').lower()

def already_have(doi):
    k=doi_key(doi)
    for f in os.listdir(TARGET_DIR):
        if f.lower().startswith(k) and f.lower().endswith('.pdf'): return f
    return None

def s2_oa_pdf(doi):
    url=f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf,isOpenAccess"
    req=urllib.request.Request(url, headers={"x-api-key":S2KEY,"User-Agent":BROWSER_UA})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            d=json.load(r)
        oap=d.get("openAccessPdf") or {}
        return oap.get("url")
    except Exception as e:
        return None

def fetch(doi,url):
    try:
        req=urllib.request.Request(url,headers={"User-Agent":BROWSER_UA,"Accept":"application/pdf,*/*"})
        with urllib.request.urlopen(req,timeout=60) as r:
            data=r.read()
        if not data[:5].startswith(b"%PDF"): return False,"not-pdf"
        out=os.path.join(TARGET_DIR,doi_key(doi)+".pdf")
        with open(out,"wb") as f: f.write(data)
        return True,f"{len(data)//1024}KB"
    except Exception as e:
        return False,f"err:{type(e).__name__}"

def main():
    rows=list(csv.DictReader(open(BLOCKERS),delimiter='\t'))
    targets=[r for r in rows if r["blocker_status"].startswith("oa-but") or r["blocker_status"].startswith("unpaywall-err")]
    print(f"S2 key: {'YES' if S2KEY else 'NO'} | OA-recoverable targets: {len(targets)} / {len(rows)} blockers")
    recovered=set()
    for r in targets:
        doi=r["doi"].rstrip("/").replace("/full","")  # clean the fenvs /full suffix
        if already_have(doi):
            recovered.add(r["doi"]); print(f"  ✓ #{r['rank']} already on disk"); continue
        pdf=s2_oa_pdf(doi); time.sleep(DELAY)
        if pdf:
            ok,info=fetch(doi,pdf); time.sleep(DELAY)
            if ok:
                recovered.add(r["doi"]); print(f"  ✓ #{r['rank']:>3} {doi} RECOVERED via S2 [{info}]"); continue
            print(f"  ✗ #{r['rank']:>3} {doi} s2-pdf-but-{info}")
        else:
            print(f"  – #{r['rank']:>3} {doi} no S2 openAccessPdf")
    # rewrite blocker TSV minus recovered
    kept=[r for r in rows if r["doi"] not in recovered]
    with open(BLOCKERS,"w") as f:
        f.write("rank\tdoi\tblocker_status\n")
        for r in kept: f.write(f"{r['rank']}\t{r['doi']}\t{r['blocker_status']}\n")
    print(f"\nRECOVERED {len(recovered)} OA papers via S2. Blockers remaining: {len(kept)} (true paywall/unfetchable).")

if __name__=="__main__": main()
