#!/usr/bin/env python3
"""
Verify the central sequence claim of Patra et al. 2022 (doi:10.3857/roj.2021.00689):

  Claim 1: "PolβΔ has a deletion of 97 amino acids in its catalytic domains"
  Claim 2: deleted region = amino acid residues 208–304 (also stated 208–301
           and 211–339 in different places in the paper — internal inconsistency)
  Claim 3: PolβΔ co-expressed with WT in heterozygous condition is dominant-negative

We use Supplementary Table S1 nucleotide sequences verbatim. We also compare
against the canonical human POLB protein (UniProt P06746, 335 aa) — Beard &
Wilson (2006) confirm the mature human Polβ is 335 aa.

Outputs:
  results/sequence_check.json  — full quantitative comparison
  results/wt_protein.fasta, results/del_protein.fasta
  results/alignment.txt        — pairwise global alignment
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

from Bio.Seq import Seq
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RES  = ROOT / "results"; RES.mkdir(exist_ok=True)

# ----- Parse Supplementary Table S1 directly from suppl3.txt -----
suppl3 = (DATA / "suppl3.txt").read_text()

def extract(label: str) -> str:
    # Find the labeled block and pull every uppercase ACGT run after it.
    idx = suppl3.find(label)
    if idx < 0:
        raise RuntimeError(f"label not found: {label}")
    block = suppl3[idx:]
    # stop at next labeled block heading (any of the markers)
    end = len(block)
    for marker in ("Pol beta (Polβ", "Pol beta (Polβ,", "Table S", "https://doi"):
        j = block.find(marker, 5)  # skip our own header
        if 0 < j < end:
            end = j
    chunk = block[:end]
    seq = "".join(re.findall(r"[ACGT]+", chunk))
    return seq

wt_nt  = extract("Pol beta (Polβ wild type) nucleotide sequence:")
del_nt = extract("Pol beta (PolβΔ, deleted exon 11-13) nucleotide sequence:")

print(f"WT  nt length: {len(wt_nt)}")
print(f"DEL nt length: {len(del_nt)}")
print(f"Nucleotide difference: {len(wt_nt)-len(del_nt)} nt ; /3 = {(len(wt_nt)-len(del_nt))/3}")

# Translate
wt_prot  = str(Seq(wt_nt).translate())
del_prot = str(Seq(del_nt).translate())
# strip trailing stop
wt_prot_clean  = wt_prot.rstrip("*")
del_prot_clean = del_prot.rstrip("*")

print(f"WT  protein length: {len(wt_prot_clean)} aa  (stop codons in sequence: {wt_prot.count('*')})")
print(f"DEL protein length: {len(del_prot_clean)} aa  (stop codons in sequence: {del_prot.count('*')})")
print(f"Protein length difference: {len(wt_prot_clean)-len(del_prot_clean)} aa")

# Pairwise alignment (global, BLOSUM62-like simple scoring is fine here;
# we use globalms with simple match/mismatch/gap since these are nearly identical).
alns = pairwise2.align.globalms(
    wt_prot_clean, del_prot_clean,
    match=2, mismatch=-1, open=-10, extend=-0.5,
)
best = alns[0]
ali_str = format_alignment(*best)
(RES / "alignment.txt").write_text(ali_str)

# Identify the gap range in the alignment vs WT coordinates
top, bot, score, beg, end = best
# Map: find contiguous gap regions in 'bot' relative to WT coords (top has no gaps if del nested)
wt_pos = 0
gap_blocks = []  # list of (wt_start, wt_end, length)
in_gap = False
gap_start_wt = None
for tc, bc in zip(top, bot):
    if tc != "-":
        wt_pos += 1
    if bc == "-" and tc != "-":
        if not in_gap:
            in_gap = True
            gap_start_wt = wt_pos
    else:
        if in_gap:
            gap_blocks.append((gap_start_wt, wt_pos - 1, wt_pos - gap_start_wt))
            in_gap = False
if in_gap:
    gap_blocks.append((gap_start_wt, wt_pos, wt_pos - gap_start_wt + 1))

# Write FASTAs
(RES / "wt_protein.fasta").write_text(f">WT_Polbeta_translated len={len(wt_prot_clean)}\n{wt_prot_clean}\n")
(RES / "del_protein.fasta").write_text(f">PolBetaDelta_translated len={len(del_prot_clean)}\n{del_prot_clean}\n")
(RES / "wt_nt.fasta").write_text(f">WT_Polbeta_nt len={len(wt_nt)}\n{wt_nt}\n")
(RES / "del_nt.fasta").write_text(f">PolBetaDelta_nt len={len(del_nt)}\n{del_nt}\n")

# Canonical human Polβ length = 335 aa (UniProt P06746). The cDNA published in
# the supplement encodes 335 aa as the WT, confirming the canonical reading frame.
EXPECTED_WT_LEN = 335

claims = {
    "claim_97aa_deletion": (len(wt_prot_clean) - len(del_prot_clean) == 97),
    "claim_deletion_residues_208_304": False,  # filled below
    "wt_length_is_canonical_335": (len(wt_prot_clean) == EXPECTED_WT_LEN),
    "del_length": len(del_prot_clean),
    "wt_length":  len(wt_prot_clean),
    "single_contiguous_deletion": (len(gap_blocks) == 1),
    "gap_blocks": gap_blocks,
}

if len(gap_blocks) == 1:
    s, e, ln = gap_blocks[0]
    claims["deletion_start_wt"] = s
    claims["deletion_end_wt"]   = e
    claims["deletion_length"]   = ln
    claims["claim_deletion_residues_208_304"] = (s == 208 and e == 304)
    claims["matches_paper_211_339_text"] = (s == 211 and e == 339)
    claims["matches_paper_208_301"]      = (s == 208 and e == 301)

print("\n--- Reconciliation with paper's textual claims ---")
for k, v in claims.items():
    print(f"  {k}: {v}")

(RES / "sequence_check.json").write_text(json.dumps(claims, indent=2))
print(f"\nResults written under {RES}")
