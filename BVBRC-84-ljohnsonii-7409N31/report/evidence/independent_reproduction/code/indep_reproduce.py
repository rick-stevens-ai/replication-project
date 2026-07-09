#!/usr/bin/env python3
"""Independent reproduction: recompute all headline numbers from scratch."""
import json, gzip, os, subprocess, sys, re
from collections import Counter

BASE = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/BVBRC-84-ljohnsonii-7409N31/report/evidence/independent_reproduction")
FNA = f"{BASE}/downloads/ncbi_dataset/ncbi_dataset/data/GCF_022810665.1/GCF_022810665.1_ASM2281066v1_genomic.fna"
GFF = f"{BASE}/downloads/ncbi_dataset/ncbi_dataset/data/GCF_022810665.1/genomic.gff"
PROT = f"{BASE}/downloads/ncbi_dataset/ncbi_dataset/data/GCF_022810665.1/protein.faa"
GB   = f"{BASE}/downloads/CP084221_indep.gb"

out = {}

# ---- (1) Genome length + GC, computed byte-by-byte ----
print("=== (1) Genome length + GC from FASTA (independent) ===")
seq_parts = []
header = None
n_contigs = 0
with open(FNA) as f:
    for line in f:
        if line.startswith(">"):
            header = line.strip()
            n_contigs += 1
        else:
            seq_parts.append(line.strip().upper())
seq = "".join(seq_parts)
L = len(seq)
counts = Counter(seq)
gc = counts["G"] + counts["C"]
at = counts["A"] + counts["T"]
n  = counts["N"]
gc_pct = gc / L * 100.0
print(f"  header: {header}")
print(f"  n_contigs (FASTA records): {n_contigs}")
print(f"  length: {L}")
print(f"  A={counts['A']} T={counts['T']} G={counts['G']} C={counts['C']} N={n}")
print(f"  GC%: {gc_pct:.4f}")
print(f"  GC% rounded to 2dp: {round(gc_pct, 2)}")

out["genome_length_bp"] = L
out["gc_percent_raw"] = gc_pct
out["gc_percent_rounded_2dp"] = round(gc_pct, 2)
out["n_contigs_fasta"] = n_contigs
out["base_counts"] = dict(counts)

# ---- (2) Topology from GenBank LOCUS ----
print("\n=== (2) Topology from GenBank LOCUS line ===")
with open(GB) as f:
    locus = f.readline().strip()
print(f"  LOCUS: {locus}")
topology = "circular" if "circular" in locus.lower() else ("linear" if "linear" in locus.lower() else "unknown")
print(f"  topology: {topology}")
out["locus_line"] = locus
out["topology"] = topology

# ---- (3) Feature counts from RefSeq GFF (current, 2026 re-annotation) ----
print("\n=== (3) Feature counts from RefSeq GFF (current re-annotation) ===")
gff_feature_types = Counter()
gene_biotypes = Counter()
cds_count = 0
trna_count = 0
rrna_count = 0
ncrna_count = 0
tmrna_count = 0
pseudogene_count = 0

with open(GFF) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 9:
            continue
        ftype = cols[2]
        attrs = cols[8]
        gff_feature_types[ftype] += 1
        # Parse gene_biotype
        m = re.search(r"gene_biotype=([^;]+)", attrs)
        if m:
            gene_biotypes[m.group(1)] += 1
        # Pseudo flag
        if "pseudo=true" in attrs and ftype == "gene":
            pseudogene_count += 1

# tRNA/rRNA/ncRNA/tmRNA counts via feature type
trna_count  = gff_feature_types.get("tRNA", 0)
rrna_count  = gff_feature_types.get("rRNA", 0)
ncrna_count = gff_feature_types.get("ncRNA", 0)
tmrna_count = gff_feature_types.get("tmRNA", 0)
cds_count   = gff_feature_types.get("CDS", 0)

print(f"  All feature types: {dict(gff_feature_types)}")
print(f"  Gene biotypes: {dict(gene_biotypes)}")
print(f"  CDS: {cds_count}")
print(f"  tRNA: {trna_count}")
print(f"  rRNA: {rrna_count}")
print(f"  ncRNA: {ncrna_count}")
print(f"  tmRNA: {tmrna_count}")
print(f"  pseudogenes (gene w/ pseudo=true): {pseudogene_count}")

out["gff_feature_types"] = dict(gff_feature_types)
out["gff_gene_biotypes"] = dict(gene_biotypes)
out["refseq_cds"] = cds_count
out["refseq_trna"] = trna_count
out["refseq_rrna"] = rrna_count
out["refseq_ncrna"] = ncrna_count
out["refseq_tmrna"] = tmrna_count
out["refseq_pseudogenes"] = pseudogene_count

# ---- (4) Protein FASTA independent count ----
print("\n=== (4) Protein count from protein.faa ===")
n_prot = 0
with open(PROT) as f:
    for line in f:
        if line.startswith(">"):
            n_prot += 1
print(f"  n proteins: {n_prot}")
out["refseq_protein_count"] = n_prot

# ---- (5) Prodigal independent CDS prediction (ab initio, standalone) ----
print("\n=== (5) Independent CDS prediction via prodigal (single-genome mode) ===")
prod_gff = f"{BASE}/downloads/prodigal_predictions.gff"
prod_faa = f"{BASE}/downloads/prodigal_predictions.faa"
prod_log = f"{BASE}/downloads/prodigal.log"
r = subprocess.run(
    ["prodigal", "-i", FNA, "-f", "gff", "-o", prod_gff, "-a", prod_faa, "-c", "-p", "single", "-q"],
    capture_output=True, text=True
)
with open(prod_log, "w") as lf:
    lf.write("stdout:\n" + r.stdout + "\nstderr:\n" + r.stderr)
print(f"  prodigal rc={r.returncode}, stderr tail: {r.stderr.strip()[-200:]}")
prod_cds = 0
with open(prod_gff) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) >= 3 and cols[2] == "CDS":
            prod_cds += 1
print(f"  prodigal CDS count (ab initio, closed-ends, -c): {prod_cds}")
out["prodigal_cds"] = prod_cds

# also without -c (allow partial)
prod_gff2 = f"{BASE}/downloads/prodigal_predictions_open.gff"
r2 = subprocess.run(
    ["prodigal", "-i", FNA, "-f", "gff", "-o", prod_gff2, "-p", "single", "-q"],
    capture_output=True, text=True
)
prod_cds_open = 0
with open(prod_gff2) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) >= 3 and cols[2] == "CDS":
            prod_cds_open += 1
print(f"  prodigal CDS count (open ends, no -c): {prod_cds_open}")
out["prodigal_cds_open"] = prod_cds_open

# ---- (6) barrnap independent rRNA prediction ----
print("\n=== (6) Independent rRNA prediction via barrnap ===")
barr_gff = f"{BASE}/downloads/barrnap_bac.gff"
r = subprocess.run(
    ["barrnap", "--kingdom", "bac", "--quiet", FNA],
    capture_output=True, text=True
)
with open(barr_gff, "w") as f:
    f.write(r.stdout)
barr_types = Counter()
barr_lines = []
for line in r.stdout.splitlines():
    if line.startswith("#") or not line.strip():
        continue
    cols = line.split("\t")
    if len(cols) < 9:
        continue
    m = re.search(r"Name=([^;]+)", cols[8])
    label = m.group(1) if m else cols[2]
    barr_types[label] += 1
    barr_lines.append(line)
print(f"  barrnap rRNA hits by type: {dict(barr_types)}")
print(f"  total rRNA features: {sum(barr_types.values())}")
out["barrnap_rrna_by_type"] = dict(barr_types)
out["barrnap_rrna_total"] = sum(barr_types.values())

# ---- (7) abricate AMR/VF scan (for AMR/feature claims) ----
print("\n=== (7) abricate scan (CARD default DB) ===")
abr_out = f"{BASE}/downloads/abricate_card.tsv"
r = subprocess.run(
    ["abricate", "--db", "card", "--nopath", FNA],
    capture_output=True, text=True
)
with open(abr_out, "w") as f:
    f.write(r.stdout)
abr_hits = [l for l in r.stdout.splitlines() if l and not l.startswith("#")]
print(f"  abricate CARD hits: {len(abr_hits)}")
if abr_hits:
    for l in abr_hits[:10]:
        print(f"    {l}")
out["abricate_card_hits"] = len(abr_hits)

# Check available DBs
r = subprocess.run(["abricate", "--list"], capture_output=True, text=True)
print(f"  abricate DBs: {r.stdout}")

# ---- (8) Assembly method / platform / bioproject from data report ----
print("\n=== (8) Assembly metadata from NCBI Datasets JSONL ===")
dr = json.load(open(f"{BASE}/downloads/ncbi_dataset/ncbi_dataset/data/assembly_data_report.jsonl"))
ai = dr["assemblyInfo"]
seq_tech = ai.get("sequencingTech")
asm_method = ai.get("assemblyMethod")
bio = ai.get("bioprojectLineage",[{}])[0].get("bioprojects",[{}])[0].get("accession")
biosample = ai.get("biosample",{}).get("accession")
print(f"  sequencingTech: {seq_tech}")
print(f"  assemblyMethod: {asm_method}")
print(f"  bioproject: {bio}")
print(f"  biosample: {biosample}")

annot = dr.get("annotationInfo", {})
print(f"  annotation name: {annot.get('name')}")
print(f"  annotation provider: {annot.get('provider')}")
gc_stats = annot.get("stats",{}).get("geneCounts",{})
print(f"  RefSeq geneCounts: {gc_stats}")

out["sequencing_platform"] = seq_tech
out["assembly_method"] = asm_method
out["bioproject"] = bio
out["biosample"] = biosample
out["annotation_name"] = annot.get("name")
out["annotation_provider"] = annot.get("provider")
out["refseq_gene_counts_json"] = gc_stats

# ---- (9) SRA check (raw reads) ----
print("\n=== (9) SRA availability check for biosample ===")
import urllib.request
try:
    with urllib.request.urlopen(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=SAMN21619988&retmode=json", timeout=30) as r:
        js = json.load(r)
    ids = js.get("esearchresult",{}).get("idlist", [])
    count = js.get("esearchresult",{}).get("count", "?")
    print(f"  SRA count for SAMN21619988: {count}")
    print(f"  SRA ids: {ids}")
    out["sra_count"] = count
    out["sra_ids"] = ids
except Exception as e:
    print(f"  SRA check failed: {e}")
    out["sra_count"] = "error"

# ---- (10) BV-BRC PATRIC annotation counts (paper's actual annotation source) ----
print("\n=== (10) BV-BRC PATRIC feature counts (paper's actual annotation source) ===")
try:
    url = "https://www.bv-brc.org/api/genome/?eq(strain,7409N31)&select(genome_id,genome_name,genome_length,gc_content,cds,patric_cds,contigs,trna,rrna,sequencing_platform,assembly_method)&limit(5)"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        bv = json.load(r)
    print(json.dumps(bv, indent=2))
    out["bvbrc_genome"] = bv
except Exception as e:
    print(f"  BV-BRC fetch failed: {e}")
    out["bvbrc_genome"] = f"error: {e}"

# ---- Save ----
sumfile = f"{BASE}/indep_summary.json"
with open(sumfile, "w") as f:
    json.dump(out, f, indent=2, default=str)
print(f"\nSaved: {sumfile}")
