#!/usr/bin/env python3
"""Parse NCBI BLAST XML results and extract E. coli hits."""
import xml.etree.ElementTree as ET
import os, csv, json, re

BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli")
RESULTS_DIR = os.path.join(BASEDIR, "analysis/blast_results")

# Map safe filenames back to system names
with open(os.path.join(BASEDIR, "data/blast_rids.json")) as f:
    rids = json.load(f)

safe_to_sys = {}
for sys_name in rids:
    safe = sys_name.replace("-", "_")
    safe_to_sys[safe] = sys_name

all_results = {}

for fname in sorted(os.listdir(RESULTS_DIR)):
    if not fname.endswith(".xml"):
        continue
    safe_name = fname.replace(".xml", "")
    sys_name = safe_to_sys.get(safe_name, safe_name)
    
    filepath = os.path.join(RESULTS_DIR, fname)
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError:
        print(f"WARNING: Could not parse {fname}")
        continue
    
    # Navigate BLAST XML structure
    iterations = root.findall(".//Iteration")
    hits = []
    
    for iteration in iterations:
        query_def = iteration.find("Iteration_query-def")
        query_len = iteration.find("Iteration_query-len")
        q_len = int(query_len.text) if query_len is not None else 0
        
        for hit in iteration.findall(".//Hit"):
            hit_def = hit.find("Hit_def").text if hit.find("Hit_def") is not None else ""
            hit_acc = hit.find("Hit_accession").text if hit.find("Hit_accession") is not None else ""
            hit_len = int(hit.find("Hit_len").text) if hit.find("Hit_len") is not None else 0
            
            for hsp in hit.findall(".//Hsp"):
                evalue = float(hsp.find("Hsp_evalue").text)
                identity = int(hsp.find("Hsp_identity").text)
                align_len = int(hsp.find("Hsp_align-len").text)
                q_from = int(hsp.find("Hsp_query-from").text)
                q_to = int(hsp.find("Hsp_query-to").text)
                bitscore = float(hsp.find("Hsp_bit-score").text)
                
                pident = (identity / align_len * 100) if align_len > 0 else 0
                qcov = ((q_to - q_from + 1) / q_len * 100) if q_len > 0 else 0
                
                # Apply filters: E<1e-10, >=30% identity, >=70% coverage
                is_ecoli = "escherichia" in hit_def.lower() or "e. coli" in hit_def.lower() or "ecoli" in hit_def.lower()
                passes_filter = (evalue < 1e-10 and pident >= 30 and qcov >= 70)
                
                hits.append({
                    "system": sys_name,
                    "hit_acc": hit_acc,
                    "hit_def": hit_def[:120],
                    "hit_len": hit_len,
                    "evalue": evalue,
                    "pident": round(pident, 1),
                    "qcov": round(qcov, 1),
                    "bitscore": round(bitscore, 1),
                    "is_ecoli": is_ecoli,
                    "passes_filter": passes_filter,
                    "align_len": align_len,
                })
    
    all_results[sys_name] = hits
    
    # Stats
    total = len(hits)
    ecoli_hits = [h for h in hits if h["is_ecoli"]]
    filtered = [h for h in ecoli_hits if h["passes_filter"]]
    
    # Count unique accessions passing filter
    unique_filtered = set(h["hit_acc"] for h in filtered)
    
    print(f"{sys_name}: {total} total hits, {len(ecoli_hits)} E. coli, {len(filtered)} passing filter ({len(unique_filtered)} unique accessions)")
    if filtered:
        # Show top 3
        for h in sorted(filtered, key=lambda x: x["evalue"])[:3]:
            print(f"  {h['hit_acc']}: {h['pident']}% id, {h['qcov']}% cov, E={h['evalue']:.1e} — {h['hit_def'][:80]}")

# Save all results as TSV
outpath = os.path.join(BASEDIR, "analysis/ncbi_blast_all_hits.tsv")
with open(outpath, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["system", "hit_acc", "hit_def", "evalue", "pident", "qcov", "bitscore", "is_ecoli", "passes_filter"], delimiter="\t")
    writer.writeheader()
    for sys_name in sorted(all_results.keys()):
        for h in all_results[sys_name]:
            writer.writerow({k: h[k] for k in writer.fieldnames})

print(f"\nSaved all hits to {outpath}")

# Save filtered E. coli hits
outpath2 = os.path.join(BASEDIR, "analysis/ncbi_blast_ecoli_filtered.tsv")
with open(outpath2, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["system", "hit_acc", "hit_def", "evalue", "pident", "qcov", "bitscore"], delimiter="\t")
    writer.writeheader()
    for sys_name in sorted(all_results.keys()):
        for h in all_results[sys_name]:
            if h["is_ecoli"] and h["passes_filter"]:
                writer.writerow({k: h[k] for k in writer.fieldnames})

print(f"Saved filtered E. coli hits to {outpath2}")

# Summary stats per system
summary = {}
for sys_name in sorted(all_results.keys()):
    hits = all_results[sys_name]
    ecoli = [h for h in hits if h["is_ecoli"]]
    filtered = [h for h in ecoli if h["passes_filter"]]
    any_organism_filtered = [h for h in hits if h["passes_filter"]]
    
    # Count unique organisms in all filtered hits (not just E. coli)
    organisms = set()
    for h in any_organism_filtered:
        # Extract organism from hit_def
        match = re.search(r'\[(.+?)\]', h["hit_def"])
        if match:
            organisms.add(match.group(1))
    
    summary[sys_name] = {
        "total_hits": len(hits),
        "ecoli_filtered": len(set(h["hit_acc"] for h in filtered)),
        "all_filtered": len(set(h["hit_acc"] for h in any_organism_filtered)),
        "organisms": len(organisms),
        "organism_list": sorted(organisms)[:10]
    }

print("\n=== Distribution summary (systems retrieved so far) ===")
print(f"{'System':<12} {'Total hits':<12} {'E.coli(filt)':<14} {'All(filt)':<12} {'Organisms':<10}")
for sys_name in sorted(summary.keys()):
    s = summary[sys_name]
    print(f"{sys_name:<12} {s['total_hits']:<12} {s['ecoli_filtered']:<14} {s['all_filtered']:<12} {s['organisms']:<10}")
    if s['organism_list']:
        for org in s['organism_list'][:5]:
            print(f"             {org}")

# Save summary
with open(os.path.join(BASEDIR, "analysis/blast_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
