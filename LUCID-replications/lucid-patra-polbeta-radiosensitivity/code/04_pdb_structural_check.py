#!/usr/bin/env python3
"""
04_pdb_structural_check.py

Independent structural verification of Patra et al. 2022 docking inputs.

What this does (real local computation, no fabricated numbers):
  1. Parses each cited PDB structure (1TV9 + 10 BER-partner PDBs).
  2. Reports each chain's protein-sequence length and identity (header CMPND/SOURCE).
  3. For 1TV9 (the SWISS-MODEL template for Polβ), extracts the protein chain
     and verifies the catalytic-triad and dNTP-binding residues the paper
     calls out (D190, D192, D256; the canonical Polβ palm/finger residues).
  4. For each docking partner, checks that the PDB protein name matches the
     functional identifier the paper attaches to it (e.g. 1DE8 = APE1,
     1TDH = NEIL1, 1EBM = OGG1, etc.).
  5. Writes a JSON + text audit to results/pdb_audit.{json,txt}.

This independently verifies (or refutes) the *input side* of the docking
pipeline without re-running the docking servers themselves. It cannot
reproduce ClusPro/HDOCK scores, but it can verify the structural primary
sources.
"""

import json, os, sys, re
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import is_aa
try:
    from Bio.PDB.Polypeptide import three_to_one  # older Biopython
except ImportError:
    from Bio.Data.PDBData import protein_letters_3to1_extended as _3to1
    def three_to_one(r):
        try:
            return _3to1[r]
        except KeyError:
            raise KeyError(r)

ROOT  = Path(__file__).resolve().parents[1]
PDBD  = ROOT / "data" / "pdb"
RES   = ROOT / "results"
RES.mkdir(exist_ok=True, parents=True)

# Authors' Suppl-Table-S2 protein panel + their functional labels in the paper
PANEL = [
    ("1TV9", "Polβ (template)",                          "DNA polymerase beta"),
    ("1DE8", "AP endonuclease 1 (APE1)",                 "AP endonuclease"),
    ("1EBM", "8-oxoguanine DNA glycosylase (OGG1)",      "8-oxoguanine"),
    ("1TDH", "Endonuclease VIII-like 1 (NEIL1)",         "endonuclease"),
    ("1WSR", "DNA ligase III",                           "ligase"),
    ("1XNA", "XRCC1 N-terminal domain",                  "XRCC1"),
    ("2BRF", "PNKP FHA domain",                          "polynucleotide kinase"),
    ("2FOZ", "ADP-ribosylhydrolase 3 (ARH3)",            "ADP-ribosylhydrolase"),
    ("2RCW", "PARP1",                                    "poly"),       # PARP
    ("3Q8K", "FEN1 (flap endonuclease)",                 "flap"),
    ("4ZZY", "PARP2",                                    "poly"),
]

# Catalytic / dNTP-binding residues for human Polβ as called out in BER literature
POLB_CATALYTIC = {
    190: "ASP",   # catalytic triad
    192: "ASP",
    256: "ASP",
    272: "PHE",   # template-base interaction (canonical)
    271: "TYR",
    279: "ASN",
    283: "ARG",
}

parser = PDBParser(QUIET=True)

def chain_seq(chain):
    """Return one-letter protein sequence of standard residues only."""
    s = []
    for r in chain:
        if is_aa(r, standard=True):
            try:
                s.append(three_to_one(r.get_resname()))
            except KeyError:
                s.append("X")
    return "".join(s)

def header_text(struct):
    """Extract COMPND + SOURCE descriptive text from header dict."""
    h = struct.header
    return {
        "name":        h.get("name", ""),
        "head":        h.get("head", ""),
        "compound":    h.get("compound", {}),
        "source":      h.get("source", {}),
        "resolution":  h.get("resolution", None),
        "deposition":  h.get("deposition_date", ""),
        "structure_method": h.get("structure_method", ""),
    }

def first_protein_chain(struct):
    """Return (chain_id, sequence) for the longest protein chain."""
    best = ("", "")
    for model in struct:
        for ch in model:
            s = chain_seq(ch)
            if len(s) > len(best[1]):
                best = (ch.id, s)
        break  # only first model
    return best

audit = []
for pid, label_paper, name_token in PANEL:
    fp = PDBD / f"{pid}.pdb"
    if not fp.exists():
        audit.append({"pdb": pid, "error": "missing file"})
        continue
    try:
        struct = parser.get_structure(pid, str(fp))
    except Exception as e:
        audit.append({"pdb": pid, "error": f"parse fail: {e}"})
        continue

    hdr   = header_text(struct)
    cid, seq = first_protein_chain(struct)
    # The 'name' header is often a concatenated compound description
    header_blob = " ".join([
        str(hdr.get("name", "")),
        str(hdr.get("head", "")),
        json.dumps(hdr.get("compound", {})),
    ]).lower()

    match = name_token.lower() in header_blob

    row = {
        "pdb": pid,
        "paper_label": label_paper,
        "header_match_token": name_token,
        "header_token_found": match,
        "longest_protein_chain": cid,
        "longest_protein_chain_len": len(seq),
        "resolution_A": hdr.get("resolution"),
        "structure_method": hdr.get("structure_method"),
        "header_name_snippet": (hdr.get("name") or "")[:160],
    }
    audit.append(row)

# Polβ catalytic-residue spot-check on 1TV9 chain A
polb_struct = parser.get_structure("1TV9", str(PDBD / "1TV9.pdb"))
polb_chain  = next(iter(next(iter(polb_struct))))  # first chain
# pick longest:
cid, seq = first_protein_chain(polb_struct)
chain = next(c for m in polb_struct for c in m if c.id == cid)

polb_check = {"chain_id": cid, "chain_len": len(seq), "residues": {}}
for resnum, expected in POLB_CATALYTIC.items():
    found = None
    for r in chain:
        if r.id[0] == " " and r.id[1] == resnum:
            found = r.get_resname()
            break
    polb_check["residues"][resnum] = {
        "expected": expected,
        "found":    found,
        "match":    (found == expected),
    }
polb_check["all_canonical_match"] = all(v["match"] for v in polb_check["residues"].values())

out = {"panel_audit": audit, "polb_catalytic_check": polb_check}
(RES / "pdb_audit.json").write_text(json.dumps(out, indent=2))

# human-readable
lines = []
lines.append("PDB structural audit — Patra et al. 2022 docking inputs")
lines.append("=" * 64)
lines.append("")
lines.append(f"{'PDB':6} {'Chain':5} {'Len':>5} {'Res(Å)':>7}  Label / header match")
lines.append("-" * 78)
for r in audit:
    if "error" in r:
        lines.append(f"{r['pdb']:6} ERROR {r['error']}")
        continue
    res = r.get("resolution_A")
    res_str = f"{res:.2f}" if isinstance(res, (int, float)) else "  NMR" if (r.get("structure_method","").lower().startswith("solution")) else "   -"
    flag = "✓" if r["header_token_found"] else "✗"
    lines.append(f"{r['pdb']:6} {r['longest_protein_chain']:>5} {r['longest_protein_chain_len']:>5} {res_str:>7}  {flag} {r['paper_label']}")
    lines.append(f"           header: {r['header_name_snippet']!r}")

lines.append("")
lines.append("Polβ catalytic-residue spot-check on 1TV9 chain " + polb_check["chain_id"])
lines.append("-" * 64)
for n, v in polb_check["residues"].items():
    mark = "✓" if v["match"] else "✗"
    lines.append(f"  residue {n:>3}: expected {v['expected']}  found {v['found']}  {mark}")
lines.append("")
lines.append("ALL canonical Polβ active-site residues match in 1TV9: "
             + ("YES" if polb_check["all_canonical_match"] else "NO"))

(RES / "pdb_audit.txt").write_text("\n".join(lines))
print("\n".join(lines))
print("\nWrote results/pdb_audit.json and results/pdb_audit.txt")
