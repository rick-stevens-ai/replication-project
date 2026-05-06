#!/usr/bin/env python3
"""Check genomic context for defense island signatures:
1. BLAST context proteins vs SorekandZhang.faa (known defense)
2. hmmscan context proteins vs DefenseDomains.hmm  
3. Check CDS products for defense island keywords
"""
import os, json, subprocess, tempfile, csv
from Bio import SeqIO

BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli")
CONTEXT_DIR = os.path.join(BASEDIR, "analysis/genomic_context")

# Parse all context GenBank files and extract CDS proteins
all_context_proteins = {}
all_system_neighbors = {}

for fname in sorted(os.listdir(CONTEXT_DIR)):
    if not fname.endswith("_context.gb"):
        continue
    sys_name = fname.replace("_context.gb", "").replace("_", "-")
    
    filepath = os.path.join(CONTEXT_DIR, fname)
    try:
        record = SeqIO.read(filepath, "genbank")
    except:
        continue
    
    proteins = []
    neighbor_info = []
    for f in record.features:
        if f.type != "CDS":
            continue
        protein_id = f.qualifiers.get("protein_id", [""])[0]
        product = f.qualifiers.get("product", ["hypothetical protein"])[0]
        translation = f.qualifiers.get("translation", [""])[0]
        locus = f.qualifiers.get("locus_tag", [""])[0]
        
        if translation and protein_id:
            proteins.append((protein_id, product, translation))
            neighbor_info.append({
                "protein_id": protein_id,
                "product": product,
                "start": int(f.location.start),
                "end": int(f.location.end),
                "strand": f.location.strand,
            })
    
    all_context_proteins[sys_name] = proteins
    all_system_neighbors[sys_name] = neighbor_info

# Write all context proteins to a single FASTA for BLAST
context_fasta = os.path.join(BASEDIR, "analysis/all_context_proteins.faa")
with open(context_fasta, "w") as f:
    for sys_name in sorted(all_context_proteins.keys()):
        for pid, product, seq in all_context_proteins[sys_name]:
            f.write(f">{pid} | {sys_name} | {product}\n{seq}\n")

total_proteins = sum(len(v) for v in all_context_proteins.values())
print(f"Extracted {total_proteins} context proteins from {len(all_context_proteins)} systems")

# BLAST context proteins vs SorekandZhang
print("\n=== BLASTP: Context proteins vs Known Defense Proteins ===")
blast_cmd = [
    "blastp", "-query", context_fasta,
    "-db", os.path.join(BASEDIR, "analysis/sorekzhang_db"),
    "-evalue", "1e-5",
    "-outfmt", "6 qseqid sseqid pident length evalue bitscore",
    "-out", os.path.join(BASEDIR, "analysis/context_vs_SorekZhang.blastp"),
    "-num_threads", "4",
]
subprocess.run(blast_cmd, capture_output=True, text=True)

# Parse BLAST results
defense_neighbors = {}
with open(os.path.join(BASEDIR, "analysis/context_vs_SorekZhang.blastp")) as f:
    for line in f:
        parts = line.strip().split("\t")
        qid = parts[0]
        sid = parts[1]
        pident = float(parts[2])
        evalue = float(parts[4])
        # Extract system name from qid header (stored in FASTA as: protein_id | system | product)
        # But BLAST only shows the first word, so we need to map back
        defense_neighbors.setdefault(qid, []).append({
            "target": sid,
            "pident": pident,
            "evalue": evalue
        })

# Map context proteins back to systems
for sys_name in sorted(all_context_proteins.keys()):
    hits = []
    for pid, product, seq in all_context_proteins[sys_name]:
        if pid in defense_neighbors:
            for h in defense_neighbors[pid]:
                hits.append(f"{pid} ({product[:40]}) → {h['target']} ({h['pident']:.0f}%id, E={h['evalue']:.1e})")
    
    if hits:
        print(f"\n{sys_name}: {len(hits)} defense protein neighbor(s)")
        for h in hits:
            print(f"  {h}")
    else:
        print(f"{sys_name}: No defense protein neighbors")

# hmmscan context proteins against DefenseDomains
print("\n\n=== hmmscan: Context proteins vs DefenseDomains.hmm ===")
hmmscan_out = os.path.join(BASEDIR, "analysis/context_vs_DefenseDomains.tbl")
hmmscan_cmd = [
    "hmmscan", "--tblout", hmmscan_out,
    "-E", "1e-5",
    os.path.join(BASEDIR, "data/phagedefense/DefenseDomains.hmm"),
    context_fasta
]
result = subprocess.run(hmmscan_cmd, capture_output=True, text=True)

# Parse hmmscan results
hmm_hits = {}
with open(hmmscan_out) as f:
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 18:
            continue
        target = parts[0]
        target_acc = parts[1]
        query = parts[2]
        evalue = float(parts[4])
        score = float(parts[5])
        hmm_hits.setdefault(query, []).append({
            "domain": target,
            "pfam": target_acc,
            "evalue": evalue,
            "score": score
        })

# Read DISign
disign = {}
with open(os.path.join(BASEDIR, "data/phagedefense/DISign.txt")) as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            disign[parts[0]] = parts[1]

# Summarize defense-related neighbors by system
print(f"\n{'System':<12} {'Defense neighbors (BLAST)':<8} {'DefenseDomain neighbors (HMM)':<8} {'DISign+ neighbors':<8}")
print("-" * 50)

system_defense_summary = {}
for sys_name in sorted(all_context_proteins.keys()):
    blast_count = 0
    hmm_count = 0
    disign_count = 0
    
    for pid, product, seq in all_context_proteins[sys_name]:
        if pid in defense_neighbors:
            blast_count += 1
        if pid in hmm_hits:
            hmm_count += 1
            for h in hmm_hits[pid]:
                pfam = h["pfam"].split(".")[0] if h["pfam"] != "-" else None
                if pfam and pfam in disign and disign[pfam] == "positive":
                    disign_count += 1
                    break
    
    print(f"{sys_name:<12} {blast_count:<28} {hmm_count:<30} {disign_count}")
    system_defense_summary[sys_name] = {
        "blast_defense_neighbors": blast_count,
        "hmm_defense_neighbors": hmm_count,
        "disign_positive_neighbors": disign_count,
        "total_context_cds": len(all_context_proteins[sys_name])
    }

with open(os.path.join(BASEDIR, "analysis/defense_island_summary.json"), "w") as f:
    json.dump(system_defense_summary, f, indent=2)

print(f"\nSaved defense island summary")
