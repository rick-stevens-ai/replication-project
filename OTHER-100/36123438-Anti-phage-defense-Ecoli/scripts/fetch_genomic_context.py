#!/usr/bin/env python3
"""Fetch ±20kb genomic context around each PD system from NCBI."""
import os, json, time, requests
from Bio import Entrez, SeqIO
from io import StringIO

Entrez.email = "rick.stevens@mac.com"
BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli")
CONTEXT_DIR = os.path.join(BASEDIR, "analysis/genomic_context")
os.makedirs(CONTEXT_DIR, exist_ok=True)

# System locations from Table S2
systems = [
    ("PD-T4-1", "RRWJ01000003", 226997, 228199),
    ("PD-T4-2", "QOYX01000002", 338334, 339873),
    ("PD-T4-3", "QOZA01000068", 1828, 2601),
    ("PD-T4-4", "QOYR01000017", 106928, 108900),
    ("PD-T4-5", "QOXT01000046", 4695, 5639),
    ("PD-T4-6", "RRWI01000019", 62620, 63930),
    ("PD-T4-7", "RRWT01000001", 337619, 338677),
    ("PD-T4-8", "QOXQ01000011", 97619, 98845),
    ("PD-T4-9", "QOXH01000008", 116077, 117290),
    ("PD-T4-10", "QOYX01000006", 196254, 197857),
    ("PD-L-1", "QOXL01000020", 49060, 50562),
    ("PD-L-2", "QOYB01000002", 229385, 232009),
    ("PD-L-3", "QOXN01000003", 22616, 25374),
    ("PD-L-4", "QOXP01000002", 381149, 385792),
    ("PD-L-5", "QOWS01000001", 264599, 267059),
    ("PD-L-6", "RRUL01000001", 426209, 426605),
    ("PD-T7-1", "QOYF01000088", 2183, 3533),
    ("PD-T7-2", "RRWG01000006", 138207, 140968),
    ("PD-T7-3", "QOXP01000001", 286951, 288318),
    ("PD-T7-4", "RRVG01000013", 34, 694),
    ("PD-T7-5", "RRWJ01000050", 27110, 28283),
]

FLANK = 20000  # ±20kb

results = {}
for sys_name, contig, start, end in systems:
    outfile = os.path.join(CONTEXT_DIR, f"{sys_name.replace('-','_')}_context.gb")
    if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
        print(f"{sys_name}: Already fetched")
        continue
    
    # Calculate fetch region
    fetch_start = max(1, start - FLANK)
    fetch_end = end + FLANK
    
    try:
        # Fetch GenBank record for the region
        handle = Entrez.efetch(
            db="nucleotide",
            id=contig,
            rettype="gb",
            retmode="text",
            seq_start=fetch_start,
            seq_stop=fetch_end
        )
        data = handle.read()
        handle.close()
        
        with open(outfile, "w") as f:
            f.write(data)
        
        # Parse and count features
        record = SeqIO.read(StringIO(data), "genbank")
        cds_count = sum(1 for f in record.features if f.type == "CDS")
        region_len = len(record.seq)
        
        # Check for phage-related annotations
        phage_keywords = ["phage", "prophage", "integrase", "recombinase", "terminase", 
                         "capsid", "tail", "baseplate", "portal", "lysozyme", "holin",
                         "lysogeny", "repressor", "cI", "cro", "attL", "attR"]
        phage_cds = []
        for f in record.features:
            if f.type == "CDS":
                product = f.qualifiers.get("product", [""])[0].lower()
                note = f.qualifiers.get("note", [""])[0].lower()
                for kw in phage_keywords:
                    if kw in product or kw in note:
                        phage_cds.append(f.qualifiers.get("product", ["?"])[0])
                        break
        
        results[sys_name] = {
            "contig": contig,
            "region": f"{fetch_start}-{fetch_end}",
            "region_len": region_len,
            "cds_count": cds_count,
            "phage_cds_count": len(phage_cds),
            "phage_annotations": phage_cds[:10],
        }
        
        print(f"{sys_name}: {region_len}bp, {cds_count} CDS, {len(phage_cds)} phage-related")
        if phage_cds:
            for p in phage_cds[:5]:
                print(f"  → {p}")
        
    except Exception as e:
        print(f"{sys_name}: ERROR - {e}")
        results[sys_name] = {"error": str(e)}
    
    time.sleep(1)

# Save results
with open(os.path.join(CONTEXT_DIR, "context_summary.json"), "w") as f:
    json.dump(results, f, indent=2)

print(f"\nFetched {len([r for r in results.values() if 'error' not in r])} contexts")
