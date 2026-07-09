#!/usr/bin/env python3
"""Pass-2 claim test: full VF panel — plo, nanH, nanP, cbpA(=cna in Prokka), and 4 fimbrial subunits.
Pass-1 only ran plo + nanH. Pass-2 covers all 8 candidate VFs the paper enumerates.

References:
  ref_plo.fasta  (1606 nt) - confirmed
  ref_nanH.fasta (2548 nt) - confirmed
  ref_nanP.fasta (1138 nt) - confirmed
  ref_cna.fasta extracted now from TP6375 Prokka CAOFJOCJ_01776 (3456 nt, "Collagen adhesin" = cbpA-like)
  ref_fim1_spaH_642.fasta  (1408 nt) -> fimA-like
  ref_fim2_spaH_1394.fasta (1753 nt) -> fimC-like
  ref_fim3_spaH_1750.fasta (1804 nt) -> fimE-like
  ref_fim4_spaH_1892.fasta (1138 nt) -> fimJ-like

Per-paper qc/pid stringency: query coverage >=30%, percent identity >=60% (Section 2.9).
"""
import subprocess, csv, json, os, re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-05-Trueperella-pyogenes-Thakur2022")
GENOMES = ROOT / "data" / "genomes"
VF = ROOT / "analysis" / "virulence"
OUT = ROOT / "results" / "repass"
OUT.mkdir(parents=True, exist_ok=True)

strains = sorted([p.stem for p in GENOMES.glob("*.fna") if "_" not in p.stem])

# Extract cna (cbpA candidate) from TP6375 Prokka
ffn = ROOT / "analysis" / "prokka" / "TP6375" / "TP6375.ffn"
cna_path = VF / "ref_cna.fasta"
if not cna_path.exists() or cna_path.stat().st_size < 1000:
    with open(ffn) as f, open(cna_path, "w") as out:
        capture = False
        for line in f:
            if line.startswith(">"):
                if "CAOFJOCJ_01776" in line:
                    capture = True
                    out.write(line)
                else:
                    capture = False
            elif capture:
                out.write(line)

# VF references with paper-mapped names
refs = {
    "plo":  VF / "ref_plo.fasta",
    "nanH": VF / "ref_nanH.fasta",
    "nanP": VF / "ref_nanP.fasta",
    "cbpA": VF / "ref_cna.fasta",       # Collagen adhesin = cbpA-like
    "fimA": VF / "ref_fim1_spaH_642.fasta",
    "fimC": VF / "ref_fim2_spaH_1394.fasta",
    "fimE": VF / "ref_fim3_spaH_1750.fasta",
    "fimJ": VF / "ref_fim4_spaH_1892.fasta",
}

# Reference lengths
ref_len = {}
for vf, p in refs.items():
    seq = "".join(l.strip() for l in open(p) if not l.startswith(">"))
    ref_len[vf] = len(seq)
    if len(seq) == 0:
        print(f"WARN: {vf} reference empty ({p})")

# BLAST against each genome (build db if needed)
blastdir = OUT / "vf_blast"
blastdir.mkdir(exist_ok=True)

# Use cumulative hits: sum query coverage of hits with pid>=60 that don't overlap on query
# Simpler: best hit per genome with pid>=60; then sum hit lengths against ref length
# Per Section 2.9 stringency: query coverage >=30% AND pid >=60%

results = defaultdict(dict)  # vf -> strain -> dict
fields = "qseqid sseqid pident length qstart qend sstart send evalue bitscore qlen slen qcovhsp qcovs"
for vf, ref in refs.items():
    if ref_len[vf] == 0:
        continue
    for s in strains:
        gdb = GENOMES / s
        out_blast = blastdir / f"{vf}__{s}.tsv"
        cmd = ["blastn", "-query", str(ref), "-subject", str(GENOMES / f"{s}.fna"),
               "-outfmt", f"6 {fields}", "-evalue", "1e-10",
               "-max_target_seqs", "5", "-out", str(out_blast)]
        subprocess.run(cmd, check=True)
        best = None
        any_pass = False
        cum_cov = 0.0
        for line in open(out_blast):
            t = line.rstrip().split("\t")
            if len(t) < 14: continue
            pid = float(t[2]); length = int(t[3]); qlen = int(t[10])
            qcov_hit = 100.0*length/qlen if qlen else 0.0
            qcovs = float(t[13])
            if pid >= 60.0 and qcovs >= 30.0:
                any_pass = True
            if best is None or float(t[9]) > best["bitscore"]:
                best = dict(pident=pid, length=length, qlen=qlen, qcov_hit=qcov_hit, qcovs=qcovs, bitscore=float(t[9]))
        results[vf][s] = dict(
            present=any_pass,
            best_pid=best["pident"] if best else None,
            best_qcovs=best["qcovs"] if best else None,
            ref_len=ref_len[vf],
        )

# Per-VF counts
per_vf_counts = {vf: sum(1 for s in strains if results[vf][s]["present"]) for vf in results}
print("VF presence (paper threshold: qcov>=30%, pid>=60%):")
print(f"  Strains: {len(strains)}")
for vf in ["plo","nanH","nanP","cbpA","fimA","fimC","fimE","fimJ"]:
    if vf in results:
        c = per_vf_counts[vf]
        print(f"  {vf:6s}: present in {c}/{len(strains)} strains")

# Per-strain detail TSV
out_tsv = OUT / "vf_full_panel.tsv"
with open(out_tsv, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    header = ["strain"]
    vf_order = ["plo","nanH","nanP","cbpA","fimA","fimC","fimE","fimJ"]
    for vf in vf_order:
        header += [f"{vf}_present", f"{vf}_pid", f"{vf}_qcov"]
    w.writerow(header)
    for s in strains:
        row = [s]
        for vf in vf_order:
            r = results.get(vf, {}).get(s, {})
            row += [r.get("present"), r.get("best_pid"), r.get("best_qcovs")]
        w.writerow(row)

# Paper claims to compare
paper_claims = {
    "plo":  {"in_all_19": True,  "n_present": 19, "note": "all 19, pid 80.8 (Bu5) to 100 (UFV1)"},
    "nanH": {"in_all_19": True,  "n_present": 19, "note": "all 19, pid ~87.59-87.62%"},
    "nanP": {"in_all_19": False, "n_present": 12, "note": "12 of 19"},
    "cbpA": {"in_all_19": True,  "n_present": 19, "note": "all 19; truncated in TP2/MS249/UFV1/SH01"},
    "fimA": {"in_all_19": True,  "n_present": 19, "note": "all 19 with truncation in 2012CQ-ZSH/DSM/NCTC/UFV1"},
    "fimC": {"in_all_19": True,  "n_present": 19, "note": "all 19, conserved"},
    "fimE": {"in_all_19": True,  "n_present": 19, "note": "all 19"},
    "fimJ": {"in_all_19": False, "n_present": 17, "note": "all 19 except Bu5 and UFV1 -> 17"},
}

print("\nPaper-vs-ours comparison:")
print(f"{'VF':6s} {'paper':>7s} {'ours':>6s} {'agree?':>8s}  note")
agreements = []
for vf, claim in paper_claims.items():
    ours = per_vf_counts.get(vf, 0)
    agree = (ours == claim["n_present"])
    agreements.append((vf, ours, claim["n_present"], agree))
    print(f"{vf:6s} {claim['n_present']:>7d} {ours:>6d} {str(agree):>8s}  {claim['note']}")

n_agree = sum(1 for *_, a in agreements if a)
print(f"\nVF claims exact-count agreement: {n_agree}/{len(agreements)}")

with open(OUT / "vf_full_summary.json", "w") as f:
    json.dump({
        "vf_counts_ours": per_vf_counts,
        "paper_claims": paper_claims,
        "agreement": [{"vf":v,"ours":o,"paper":p,"agree":a} for v,o,p,a in agreements],
    }, f, indent=2)
