#!/usr/bin/env python3
"""Independently verify the 71 source-strain GCA assemblies exist on NCBI.

For each assembly, hit NCBI Datasets v2 assembly summary and record:
  - assembly_accession exists
  - organism.tax_id / organism_name
  - reported strain (if any)
  - total_sequence_length

Then verify a sample by cross-checking that the reported contig accession
(from Table S2) is actually contained in that assembly."""
import json, urllib.request, urllib.parse, time, sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

with open(DATA / "indep_s5_strains.json") as fh:
    strains = json.load(fh)

with open(DATA / "indep_s2_systems.json") as fh:
    systems = json.load(fh)

# 1. Verify each assembly exists
print(f"Verifying {len(strains)} assemblies via NCBI Datasets v2 REST...")
BASE = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-repro/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

results = []
for i, s in enumerate(strains):
    acc = s["assembly"]
    url = f"{BASE}/{acc}/dataset_report"
    try:
        raw = fetch(url)
        data = json.loads(raw)
        reports = data.get("reports", [])
        if not reports:
            results.append({"strain": s["name"], "assembly": acc, "status": "NOT_FOUND"})
        else:
            r = reports[0]
            org = r.get("organism", {})
            asm_info = r.get("assembly_info", {})
            asm_stats = r.get("assembly_stats", {})
            results.append({
                "strain": s["name"], "assembly": acc, "status": "OK",
                "org": org.get("organism_name"),
                "tax_id": org.get("tax_id"),
                "asm_name": asm_info.get("assembly_name"),
                "biosample": asm_info.get("biosample", {}).get("accession"),
                "total_len": asm_stats.get("total_sequence_length"),
                "contig_n50": asm_stats.get("contig_n50"),
                "n_contigs": asm_stats.get("number_of_contigs"),
            })
    except Exception as e:
        results.append({"strain": s["name"], "assembly": acc, "status": f"ERR: {str(e)[:100]}"})
    if (i+1) % 10 == 0: print(f"  {i+1}/{len(strains)}")
    time.sleep(0.34)

with open(DATA / "assembly_verification.json", "w") as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)

ok = sum(1 for r in results if r["status"] == "OK")
print(f"\nAssemblies present in NCBI: {ok}/{len(strains)}")

# 2. Cross-check: strain -> assembly names match source-strain names in S2?
name_to_asm = {}
for r in results:
    # extract strain (e.g. "Escherichia coli strain ECOR3" -> "ECOR3")
    nm = r.get("strain") or ""
    for tag in ["strain ", "isolate "]:
        if tag in nm:
            short = nm.split(tag,1)[1].strip()
            name_to_asm[short] = r["assembly"]
            break

# S2 sources are: UMB0934, ECOR65, ECOR68 etc.
s2_sources = sorted(set(s["source"] for s in systems))
print(f"\nS2 source strains ({len(s2_sources)}): {s2_sources}")
missing = [s for s in s2_sources if s not in name_to_asm]
print(f"S2 sources present in S5 strain list: {len(s2_sources)-len(missing)}/{len(s2_sources)}")
if missing:
    print(f"  missing: {missing}")

# 3. For those 18 S2 sources, spot-check that the S2 contig accession
#    actually belongs to the strain's declared assembly by using NCBI Datasets
#    contigs endpoint (or Nucleotide efetch as fallback).
print("\nContig-in-assembly spot-check via NCBI Nucleotide efetch (5 samples):")
import random
random.seed(42)
sample = random.sample(systems, min(5, len(systems)))
for s in sample:
    contig = s["contig"]
    src = s["source"]
    asm = name_to_asm.get(src)
    if not asm:
        print(f"  {s['pd']} {src}/{contig}: no assembly for source")
        continue
    # efetch summary from Nucleotide
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nuccore&id={contig}&retmode=json"
    try:
        raw = fetch(url)
        d = json.loads(raw)
        uids = d.get("result", {}).get("uids", [])
        info = d["result"].get(uids[0], {}) if uids else {}
        title = info.get("title", "")
        organism = info.get("organism", "")
        strain = info.get("strain", "")
        print(f"  {s['pd']} src={src} contig={contig} asm={asm}  ->  strain='{strain}' title='{title[:80]}'")
    except Exception as e:
        print(f"  {s['pd']} {contig}: ERR {e}")
    time.sleep(0.34)
