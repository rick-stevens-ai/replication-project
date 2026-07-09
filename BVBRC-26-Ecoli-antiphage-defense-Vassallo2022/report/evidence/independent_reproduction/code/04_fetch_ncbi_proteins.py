#!/usr/bin/env python3
"""Independently fetch every one of the 32 defence-system CDS proteins from NCBI
by protein accession, and record:
  - HTTP status (does the record exist / is it publicly available?)
  - Protein length + a checksum of the sequence
  - The source /coded_by contig accession (from the GenPept feature table)

This verifies the paper's Table S2 provenance from a totally independent source
(NCBI eutils efetch, no BV-BRC involvement)."""
import json, time, urllib.parse, urllib.request, hashlib, sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
DL = DATA / "ncbi_proteins"
DL.mkdir(parents=True, exist_ok=True)

with open(DATA / "indep_s2_systems.json") as fh:
    systems = json.load(fh)

# Collect (pd, contig, protein_accession)
tasks = []
for s in systems:
    for p in s["proteins"]:
        tasks.append({"pd": s["pd"], "contig": s["contig"], "source": s["source"], "acc": p})

print(f"Tasks: {len(tasks)} proteins across {len(systems)} systems")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-repro/1.0 rick@anl.gov"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def get_fasta(acc):
    url = f"{EUTILS}/efetch.fcgi?db=protein&id={acc}&rettype=fasta&retmode=text"
    return fetch(url)

def get_gpc_xml(acc):
    # gp = GenPept flat file (contains /coded_by feature)
    url = f"{EUTILS}/efetch.fcgi?db=protein&id={acc}&rettype=gp&retmode=text"
    return fetch(url)

results = []
for i, t in enumerate(tasks):
    acc = t["acc"]
    try:
        fa = get_fasta(acc)
        lines = fa.strip().split("\n")
        header = lines[0]
        seq = "".join(lines[1:])
        seq_len = len(seq)
        sha = hashlib.sha256(seq.encode()).hexdigest()[:16]
        (DL / f"{acc}.faa").write_text(fa)
        time.sleep(0.34)  # NCBI etiquette
        gp = get_gpc_xml(acc)
        # find coded_by= line
        coded_by = None
        for line in gp.splitlines():
            L = line.strip()
            if L.startswith("/coded_by="):
                coded_by = L.split("=",1)[1].strip('"')
                break
            if L.startswith("coded_by="):
                coded_by = L.split("=",1)[1].strip('"')
                break
        # also try to grab from within CDS feature block
        if coded_by is None:
            in_cds = False
            for line in gp.splitlines():
                if "  CDS  " in line or line.startswith("     CDS"):
                    in_cds = True
                if in_cds and "/coded_by=" in line:
                    coded_by = line.split("/coded_by=",1)[1].strip().strip('"')
                    break
        # capture DBSOURCE (accession of source)
        dbsource = None
        for line in gp.splitlines():
            if line.startswith("DBSOURCE"):
                dbsource = line[len("DBSOURCE"):].strip()
                break
        (DL / f"{acc}.gp").write_text(gp)
        r = {**t, "http": 200, "len": seq_len, "sha256": sha, "coded_by": coded_by, "dbsource": dbsource}
    except Exception as e:
        r = {**t, "http": "ERR", "error": str(e)[:200]}
    results.append(r)
    print(f"[{i+1}/{len(tasks)}] {t['pd']} {acc}: {r.get('len','ERR')}aa dbsource={str(r.get('dbsource',''))[:60]}")
    time.sleep(0.34)

with open(DATA / "ncbi_protein_fetch.json", "w") as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)

# summary
ok = sum(1 for r in results if r["http"] == 200)
print(f"\nSummary: {ok}/{len(results)} proteins fetched from NCBI")

# check coded_by mentions expected contig
contig_ok = 0
contig_check = []
for r in results:
    if r["http"] != 200: continue
    ec = r["contig"]
    cb = (r.get("coded_by") or "") + " " + (r.get("dbsource") or "")
    match = ec in cb
    contig_check.append({"pd": r["pd"], "acc": r["acc"], "expected_contig": ec, "coded_by_or_dbsource": cb[:200], "match": match})
    if match: contig_ok += 1
print(f"Contig match (expected contig appears in /coded_by or DBSOURCE): {contig_ok}/{ok}")

with open(DATA / "contig_check.json", "w") as fh:
    json.dump(contig_check, fh, indent=2, ensure_ascii=False)
