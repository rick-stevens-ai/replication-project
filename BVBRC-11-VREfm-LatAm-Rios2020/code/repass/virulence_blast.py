#!/usr/bin/env python3
"""
Targeted virulence-gene BLASTX against the 55 LATAM assemblies.

The pass-1 VFDB scan only had 4 E. faecium virulence genes (acm, ecbA/fss3, scm,
sgrA). The paper's claim about Clade I lacking fms22, swpC, hylEfm cannot be
tested from that. So here we use a small curated set of reference *amino acid*
sequences for E. faecium virulence proteins and run tblastn against each
assembly.

Reference proteins (RefSeq IDs):
  esp     - WP_002309878.1   enterococcal surface protein, E. faecium
  hylEfm  - WP_002281063.1   hyaluronidase (Hyl), E. faecium
  acm     - WP_002282472.1   collagen adhesin Acm
  scm     - WP_002311049.1   secondary collagen adhesin
  sgrA    - WP_002296629.1   serine-glycine repeats A
  fms6    - WP_002312073.1   pilin Fms6
  fms22   - WP_010785036.1   pilin Fms22 (PilA-like)
  swpC    - WP_002297395.1   surface protein SwpC (LPxTG)
  ptsD    - WP_002311946.1   PTS system D

The script fetches the proteins from NCBI (one-time, cached), then tblastn
each protein against every assembly, applying the same thresholds the paper
used (BLASTX hits with ≥95% identity and ≥80% coverage of target).

OUTPUT: results/repass/virulome_calls.tsv (strain × gene presence/absence)
"""

import os, csv, json, subprocess, sys, time
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020")
GENOMES = ROOT / "data" / "genomes"
OUT = ROOT / "results" / "repass"
OUT.mkdir(parents=True, exist_ok=True)

REFS = {
    "esp":    "WP_002309878.1",
    "hylEfm": "WP_002281063.1",
    "acm":    "WP_002282472.1",
    "scm":    "WP_002311049.1",
    "sgrA":   "WP_002296629.1",
    "fms6":   "WP_002312073.1",
    "fms22":  "WP_010785036.1",
    "swpC":   "WP_002297395.1",
    "ptsD":   "WP_002311946.1",
}

REF_FA = OUT / "virulence_refs.faa"

# -------- Step 1: download reference proteins (efetch via NCBI) --------
if not REF_FA.exists() or REF_FA.stat().st_size < 100:
    print("Fetching reference protein sequences from NCBI...")
    seqs = []
    for gene, acc in REFS.items():
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={acc}&rettype=fasta&retmode=text"
        print(f"  {gene} = {acc}")
        try:
            r = subprocess.run(["curl", "-s", "--max-time", "20", url],
                               capture_output=True, text=True, check=True)
            fa = r.stdout.strip()
            if fa.startswith(">"):
                # rewrite header to gene name
                lines = fa.splitlines()
                lines[0] = f">{gene} {acc}"
                seqs.append("\n".join(lines))
            else:
                print(f"    FAIL: {acc} returned no FASTA")
        except Exception as e:
            print(f"    error: {e}")
        time.sleep(0.4)  # NCBI politeness

    with open(REF_FA, "w") as f:
        f.write("\n".join(seqs) + "\n")
    print(f"Wrote {len(seqs)} sequences to {REF_FA}")
else:
    print(f"Using cached {REF_FA}")

# Check what genes we actually have
have_genes = []
with open(REF_FA) as f:
    for line in f:
        if line.startswith(">"):
            g = line[1:].split()[0]
            have_genes.append(g)
print(f"Reference genes available: {have_genes}")

# -------- Step 2: run tblastn for each assembly --------
ASSEMBLIES = sorted(GENOMES.glob("*.fna"))
print(f"\nScanning {len(ASSEMBLIES)} assemblies...")

# tblastn against each genome. Output columns:
# qseqid sseqid pident length qlen slen evalue bitscore qcovs
FMT = "6 qseqid sseqid pident length qlen slen evalue bitscore qcovs"

all_hits = []  # list of dicts
for i, asm in enumerate(ASSEMBLIES, 1):
    strain = asm.stem
    cmd = ["tblastn",
           "-query", str(REF_FA),
           "-subject", str(asm),
           "-outfmt", FMT,
           "-evalue", "1e-20",
           "-max_target_seqs", "5"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"  [{i}/{len(ASSEMBLIES)}] {strain}: TIMEOUT")
        continue
    except Exception as e:
        print(f"  [{i}/{len(ASSEMBLIES)}] {strain}: ERROR {e}")
        continue

    for line in r.stdout.strip().splitlines():
        if not line: continue
        parts = line.split("\t")
        if len(parts) < 9: continue
        all_hits.append({
            "strain": strain,
            "gene":   parts[0],
            "contig": parts[1],
            "pident": float(parts[2]),
            "length": int(parts[3]),
            "qlen":   int(parts[4]),
            "slen":   int(parts[5]),
            "evalue": float(parts[6]),
            "bitscore": float(parts[7]),
            "qcovs":  float(parts[8]),
        })
    if i % 10 == 0:
        print(f"  [{i}/{len(ASSEMBLIES)}] processed")

# -------- Step 3: aggregate, apply thresholds, save --------
# Paper thresholds: BLASTX hits with %identity ≥ 95 and qcov ≥ 80
# But for protein search of long surface proteins via tblastn from one ref,
# we use ≥80% identity and ≥80% query coverage (these are still very stringent
# for protein hits — the paper used a custom alignment which may have
# accommodated variants).
STRICT = lambda h: h["pident"] >= 80.0 and h["qcovs"] >= 80.0
# Also report a more relaxed bucket
RELAX  = lambda h: h["pident"] >= 60.0 and h["qcovs"] >= 60.0

strain_set = set(a.stem for a in ASSEMBLIES)
genes      = list(REFS.keys())

# Build presence matrices
presence_strict = {s: {g: 0 for g in genes} for s in strain_set}
presence_relax  = {s: {g: 0 for g in genes} for s in strain_set}
best_hit        = defaultdict(dict)

for h in all_hits:
    s, g = h["strain"], h["gene"]
    if g not in genes: continue
    # keep best by bitscore
    if g not in best_hit[s] or h["bitscore"] > best_hit[s][g]["bitscore"]:
        best_hit[s][g] = h
    if STRICT(h):
        presence_strict[s][g] = 1
    if RELAX(h):
        presence_relax[s][g] = 1

# Write hit table
with open(OUT/"virulome_calls.tsv", "w") as f:
    f.write("strain\t" + "\t".join(genes+[g+"_pident" for g in genes]+[g+"_qcov" for g in genes]) + "\n")
    for s in sorted(strain_set):
        row = [s] + [str(presence_strict[s][g]) for g in genes]
        row += [f"{best_hit[s].get(g,{}).get('pident','-')}" for g in genes]
        row += [f"{best_hit[s].get(g,{}).get('qcovs','-')}" for g in genes]
        f.write("\t".join(row) + "\n")

# Summary
print("\nPer-gene presence summary (strict: pident>=80 & qcov>=80):")
for g in genes:
    n = sum(presence_strict[s][g] for s in strain_set)
    nr = sum(presence_relax[s][g] for s in strain_set)
    print(f"  {g}: strict={n}/{len(strain_set)} ({100*n/len(strain_set):.1f}%), relaxed={nr}/{len(strain_set)} ({100*nr/len(strain_set):.1f}%)")

# Save summary JSON
summary = {
    g: {
        "strict_count": sum(presence_strict[s][g] for s in strain_set),
        "relax_count":  sum(presence_relax[s][g] for s in strain_set),
        "total": len(strain_set),
    } for g in genes
}
with open(OUT/"virulome_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nWrote virulome_calls.tsv and virulome_summary.json to {OUT}")
