#!/usr/bin/env python3
"""Expanded LUCID harvester: reads expanded_targets.tsv (tag,doi,open_pdf_url,title),
reuses the multi-resolver chain from harvest.py, saves PDFs to pdfs_expanded/, logs to
harvest_expanded_log.tsv. Skips DOIs already present. Polite, diagnose-before-scrape."""
import csv, os, time, json, urllib.parse, urllib.request, subprocess, importlib.util, sys

HERE=os.path.dirname(os.path.abspath(__file__))
# import resolver functions from harvest.py
spec=importlib.util.spec_from_file_location("h", os.path.join(HERE,"harvest.py"))
h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

TSV=os.path.join(HERE,"expanded_targets.tsv")
PDFDIR=os.path.join(HERE,"pdfs_expanded"); os.makedirs(PDFDIR,exist_ok=True)
LOG=os.path.join(HERE,"harvest_expanded_log.tsv")

def main():
    rows=list(csv.DictReader(open(TSV),delimiter='\t'))
    logf=open(LOG,"w"); logf.write("tag\tdoi\tstatus\tmethod\thttp\tbytes\ttitle\n")
    ok=fail=0
    for r in rows:
        tag=r.get("tag","?"); doi=(r.get("doi") or "").strip()
        title=(r.get("title") or "")[:80].replace("\t"," ")
        if not doi: 
            logf.write(f"{tag}\t\tSKIP_NODOI\t\t\t\t{title}\n"); continue
        dest=os.path.join(PDFDIR, f"{h.slug(doi)}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest)>2000:
            logf.write(f"{tag}\t{doi}\tALREADY\t\t\t{os.path.getsize(dest)}\t{title}\n"); ok+=1; continue
        # if listed URL is a local path, copy
        listed=(r.get("open_pdf_url") or "").strip()
        got=False
        if listed.startswith("/") and listed.lower().endswith(".pdf") and os.path.exists(listed):
            import shutil; shutil.copy(listed,dest)
            logf.write(f"{tag}\t{doi}\tOK\tlocal\t\t{os.path.getsize(dest)}\t{title}\n"); logf.flush()
            print(f"[OK  ] {tag} local-copy {doi}"); ok+=1; continue
        for method,url in [("listed", listed if listed.startswith("http") else ""),
                           ("unpaywall",None),("europepmc",None),("s2",None)]:
            if method=="unpaywall": url=h.unpaywall_pdf(doi)
            elif method=="europepmc": url=h.europepmc_pdf(doi)
            elif method=="s2": url=h.s2_pdf(doi)
            if not url: continue
            okp,code,ctype,size=h.curl_pdf(url,dest)
            if okp:
                logf.write(f"{tag}\t{doi}\tOK\t{method}\t{code}\t{size}\t{title}\n"); logf.flush()
                print(f"[OK  ] {tag} via {method} ({size}B) {doi}"); ok+=1; got=True; break
            time.sleep(0.3)
        if not got:
            logf.write(f"{tag}\t{doi}\tFAIL\tall\t\t\t{title}\n"); logf.flush()
            print(f"[FAIL] {tag} {doi}"); fail+=1
        time.sleep(0.5)
    logf.close()
    print(f"\nDONE ok={ok} fail={fail} -> {PDFDIR}")

if __name__=="__main__":
    main()
