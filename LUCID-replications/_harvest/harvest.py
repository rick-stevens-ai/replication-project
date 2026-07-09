#!/usr/bin/env python3
"""LUCID Second-100 computational corpus harvester.
Multi-resolver chain per DOI:
  1. listed open_pdf_url (if it returns application/pdf)
  2. Unpaywall best_oa_location url_for_pdf
  3. EuropePMC PMC fulltextPDF
  4. Semantic Scholar openAccessPdf (uses S2 API key)
Saves PDFs to ./pdfs/<rank>__<doi-slug>.pdf, writes harvest_log.tsv.
Diagnose-before-scrape: host-bucketed, polite delays, records exact failure per DOI.
"""
import csv, os, re, sys, time, json, subprocess, urllib.parse, urllib.request

HERE=os.path.dirname(os.path.abspath(__file__))
TSV=os.path.join(HERE,"second100.tsv")
PDFDIR=os.path.join(HERE,"pdfs"); os.makedirs(PDFDIR,exist_ok=True)
LOG=os.path.join(HERE,"harvest_log.tsv")
EMAIL="rick.stevens.ai@gmail.com"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def s2key():
    try:
        return subprocess.check_output(["security","find-generic-password","-a","rick-stevens-ai","-s","semantic-scholar-api-key","-w"],text=True).strip()
    except Exception:
        return os.environ.get("S2_API_KEY","")
S2=s2key()

def slug(doi):
    return re.sub(r'[^a-zA-Z0-9]+','-',doi).strip('-')[:80]

def curl_pdf(url, dest, extra_headers=None):
    """Download url to dest if it is a PDF. Returns (ok, http_code, ctype, bytes)."""
    if not url: return (False,"","nourl",0)
    hdr=["-H",f"User-Agent: {UA}","-H","Accept: application/pdf,*/*"]
    if extra_headers:
        for k,v in extra_headers.items(): hdr+=["-H",f"{k}: {v}"]
    tmp=dest+".tmp"
    try:
        out=subprocess.run(["curl","-sL","--max-time","60",*hdr,"-o",tmp,"-w","%{http_code}\t%{content_type}\t%{size_download}",url],
                           capture_output=True,text=True,timeout=90).stdout.strip()
        code,ctype,size=(out.split("\t")+["","",""])[:3]
    except Exception as e:
        if os.path.exists(tmp): os.remove(tmp)
        return (False,"","err:"+str(e)[:40],0)
    # verify magic bytes
    ispdf=False
    if os.path.exists(tmp) and os.path.getsize(tmp)>2000:
        with open(tmp,"rb") as fh: head=fh.read(5)
        ispdf = head.startswith(b"%PDF")
    if ispdf:
        os.replace(tmp,dest); return (True,code,ctype,os.path.getsize(dest))
    if os.path.exists(tmp): os.remove(tmp)
    return (False,code,ctype,int(size) if size.isdigit() else 0)

def unpaywall_pdf(doi):
    try:
        u=f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
        req=urllib.request.Request(u,headers={"User-Agent":UA})
        d=json.load(urllib.request.urlopen(req,timeout=25))
        for loc in ([d.get("best_oa_location")] + (d.get("oa_locations") or [])):
            if loc and loc.get("url_for_pdf"): return loc["url_for_pdf"]
    except Exception: pass
    return ""

def europepmc_pdf(doi):
    try:
        q=f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22{urllib.parse.quote(doi)}%22&format=json&resultType=core'
        d=json.load(urllib.request.urlopen(urllib.request.Request(q,headers={"User-Agent":UA}),timeout=25))
        res=(d.get("resultList") or {}).get("result") or []
        for r in res:
            pmcid=r.get("pmcid")
            if pmcid:
                return f"https://www.ebi.ac.uk/europepmc/webservices/rest/{r.get('source','PMC')}/{pmcid}/fullTextPDF"
    except Exception: pass
    return ""

def s2_pdf(doi):
    if not S2: return ""
    try:
        u=f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?fields=openAccessPdf"
        req=urllib.request.Request(u,headers={"x-api-key":S2,"User-Agent":UA})
        d=json.load(urllib.request.urlopen(req,timeout=25))
        oa=d.get("openAccessPdf") or {}
        return oa.get("url","")
    except Exception: pass
    return ""

def main():
    rows=list(csv.DictReader(open(TSV),delimiter='\t'))
    logf=open(LOG,"w"); logf.write("rank\tdoi\tstatus\tmethod\thttp\tbytes\ttitle\n")
    ok=fail=skip=0
    for r in rows:
        rank=r.get("second100_rank","?"); doi=(r.get("doi") or "").strip()
        title=(r.get("title") or "")[:80].replace("\t"," ")
        if not doi:
            logf.write(f"{rank}\t\tSKIP_NODOI\t\t\t\t{title}\n"); skip+=1; continue
        dest=os.path.join(PDFDIR,f"{int(rank):03d}__{slug(doi)}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest)>2000:
            logf.write(f"{rank}\t{doi}\tALREADY\t\t\t{os.path.getsize(dest)}\t{title}\n"); ok+=1; continue
        got=False
        for method,url in [("listed",(r.get("open_pdf_url") or "").strip()),
                           ("unpaywall",None),("europepmc",None),("s2",None)]:
            if method=="unpaywall": url=unpaywall_pdf(doi)
            elif method=="europepmc": url=europepmc_pdf(doi)
            elif method=="s2": url=s2_pdf(doi)
            if not url: continue
            okp,code,ctype,size=curl_pdf(url,dest)
            if okp:
                logf.write(f"{rank}\t{doi}\tOK\t{method}\t{code}\t{size}\t{title}\n"); logf.flush()
                print(f"[OK  ] #{rank} via {method} ({size}B) {doi}"); ok+=1; got=True; break
            time.sleep(0.4)
        if not got:
            logf.write(f"{rank}\t{doi}\tFAIL\tall\t\t\t{title}\n"); logf.flush()
            print(f"[FAIL] #{rank} {doi}"); fail+=1
        time.sleep(0.6)
    logf.close()
    print(f"\nDONE  ok={ok} fail={fail} skip={skip}  -> {PDFDIR}")
    print(f"log: {LOG}")

if __name__=="__main__":
    main()
