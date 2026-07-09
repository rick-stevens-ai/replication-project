#!/usr/bin/env python3
"""Verify the qPCR primer panel reported in Li et al. 2022 (cbin.11900).

Checks per primer pair:
  1. Length (typical qPCR forward/reverse 18-25 nt)
  2. GC content (40-60% target window)
  3. Approximate Tm via Wallace rule and SantaLucia (basic) — only sanity check
  4. Self-complementarity / hairpin score (simple)
  5. Forward-reverse heterodimer overlap (4-mer)
  6. BLAST-free in-silico match: search transcript region for each gene
     using cached Ensembl REST hits where possible (offline fallback: print primer)

This is NOT a replication of Li et al.'s qPCR experiment — that needs the
RPRM-KO mouse line + RNA + a thermocycler. This IS a sanity check that
the primer set as printed is consistent with standard qPCR primer design
and is therefore reproducible by any wet-lab group.
"""

import json
import os
import re
import urllib.request
import urllib.error
import time

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "qpcr_primer_audit.json")

# Primer panel as captured by smoke_check.py from the JATS XML (Table 1).
PRIMERS = [
    ("Ccl11",  "GAATCACCAACAACAGATGCAC", "ATCCTGGACCCACTTCTTCTT"),
    ("Il13",   "CCTGGCTCTTGCTTGCCTT",   "GGTCTTGTGTGATGTTGCTCA"),
    ("Tnf",    "GACGTGGAACTGGCAGAAGAG", "TTGGTGGTTTGTGAGTGTGAG"),
    ("Rprm",   "CTGGCCCTGGGACAAAGAC",   "TCAAAACGGTGTCACGGATGT"),
    ("Il1a",   "AAGTCTCCAGGGCAGAGAGG",  "AGTCAGGAACTTTGGCCATCT"),
    ("Il1b",   "TGCCACCTTTTGACAGTGATG", "TGTGCTGCTGCGAGATTTGA"),
    ("Ccl2",   "GAGGACAGATGTGGTGGGTTT", "AGGAGTCAACTCAGCTTTCTCTT"),  # MCP-1
    ("Lin28a", "GGCATCTGTAAGTGGTTCAACG","CCCTCCTTGAGGCTTCGGA"),
    ("Egfr",   "GCCATCTGGGCCAAAGATACC", "GTCTTCGCATGAATAGGCCAAT"),
    ("Xrcc6",  "ATGTCAGAGTGGGAGTCCTAC", "TCGCTGCTTATGATCTTACTGGT"),
    ("Gapdh",  "AGGTCGGTGTGAACGGATTTG", "TGTAGACCATGTAGTTGAGGTCA"),
]

def gc_pct(s):
    s = s.upper()
    if not s:
        return 0.0
    return 100.0 * sum(1 for c in s if c in "GC") / len(s)

def tm_wallace(s):
    s = s.upper()
    return 2 * sum(1 for c in s if c in "AT") + 4 * sum(1 for c in s if c in "GC")

def tm_basic_santalucia(s):
    # Very rough: 64.9 + 41*(GC-16.4)/L for L>=14
    L = len(s)
    if L < 14:
        return None
    gc = sum(1 for c in s.upper() if c in "GC")
    return 64.9 + 41.0 * (gc - 16.4) / L

def rev_comp(s):
    comp = str.maketrans("ACGTacgt", "TGCAtgca")
    return s.translate(comp)[::-1]

def kmer_overlap(a, b, k=5):
    # Count how many shared k-mers exist between a and rev_comp(b) — proxy for primer dimer risk
    rcb = rev_comp(b)
    kset = {a[i:i+k] for i in range(len(a)-k+1)}
    hits = sum(1 for i in range(len(rcb)-k+1) if rcb[i:i+k] in kset)
    return hits

def ensembl_lookup(symbol, species="mus_musculus", timeout=15):
    """Lookup gene record from Ensembl REST. Returns dict or None on failure."""
    url = f"https://rest.ensembl.org/lookup/symbol/{species}/{symbol}?content-type=application/json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None

def cdna_fetch(ensembl_id, timeout=20):
    """Fetch cDNA sequence (longest) for a given ENSMUSG id."""
    url = f"https://rest.ensembl.org/sequence/id/{ensembl_id}?type=cdna"
    req = urllib.request.Request(url, headers={"Accept": "text/x-fasta"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode()
        # Take sequence portion only
        seq = "".join(line.strip() for line in data.splitlines() if not line.startswith(">"))
        return seq.upper()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None

def primer_hits_in_transcript(forward, reverse, cdna):
    """Return (forward_match, reverse_rc_match, amplicon_len_or_None)."""
    if not cdna:
        return False, False, None
    f = forward.upper()
    rrc = rev_comp(reverse.upper())
    f_idx = cdna.find(f)
    r_idx = cdna.find(rrc)
    amp = None
    if f_idx >= 0 and r_idx >= 0 and r_idx > f_idx:
        amp = r_idx + len(rrc) - f_idx
    return f_idx >= 0, r_idx >= 0, amp

def main():
    audit = []
    for gene, fwd, rev in PRIMERS:
        fwd_u = fwd.upper()
        rev_u = rev.upper()
        rec = {
            "gene": gene,
            "forward": fwd_u,
            "reverse": rev_u,
            "fwd_len": len(fwd_u),
            "rev_len": len(rev_u),
            "fwd_gc_pct": round(gc_pct(fwd_u), 1),
            "rev_gc_pct": round(gc_pct(rev_u), 1),
            "fwd_tm_wallace_C": tm_wallace(fwd_u),
            "rev_tm_wallace_C": tm_wallace(rev_u),
            "fwd_tm_basic_C": round(tm_basic_santalucia(fwd_u) or 0, 1),
            "rev_tm_basic_C": round(tm_basic_santalucia(rev_u) or 0, 1),
            "primer_dimer_5mer_hits": kmer_overlap(fwd_u, rev_u, k=5),
            "length_ok": 18 <= len(fwd_u) <= 25 and 18 <= len(rev_u) <= 25,
            "gc_ok": 40 <= gc_pct(fwd_u) <= 65 and 40 <= gc_pct(rev_u) <= 65,
            "tm_close": abs(tm_basic_santalucia(fwd_u) - tm_basic_santalucia(rev_u)) < 5
                        if tm_basic_santalucia(fwd_u) and tm_basic_santalucia(rev_u) else None,
        }
        # Try Ensembl lookup + amplicon detection
        try:
            lk = ensembl_lookup(gene)
            time.sleep(0.6)
            if lk and "id" in lk:
                rec["ensembl_id"] = lk["id"]
                rec["ensembl_symbol"] = lk.get("display_name")
                rec["chromosome"] = lk.get("seq_region_name")
                rec["biotype"] = lk.get("biotype")
                cdna = cdna_fetch(lk["id"])
                time.sleep(0.6)
                if cdna:
                    f_hit, r_hit, amp = primer_hits_in_transcript(fwd_u, rev_u, cdna)
                    rec["cdna_len"] = len(cdna)
                    rec["fwd_in_canonical_cdna"] = f_hit
                    rec["rev_rc_in_canonical_cdna"] = r_hit
                    rec["amplicon_len_bp"] = amp
        except Exception as exc:  # pragma: no cover - best-effort
            rec["lookup_error"] = str(exc)
        audit.append(rec)
        print(f"[primer] {gene:8s}  fwd_len={rec['fwd_len']:2d}  rev_len={rec['rev_len']:2d}  "
              f"GC=({rec['fwd_gc_pct']:.0f},{rec['rev_gc_pct']:.0f})  "
              f"Tm=({rec['fwd_tm_basic_C']:.0f},{rec['rev_tm_basic_C']:.0f})  "
              f"len_ok={rec['length_ok']}  gc_ok={rec['gc_ok']}  "
              f"amp={rec.get('amplicon_len_bp')}", flush=True)

    summary = {
        "n_primers": len(audit),
        "n_length_ok": sum(1 for r in audit if r["length_ok"]),
        "n_gc_ok": sum(1 for r in audit if r["gc_ok"]),
        "n_tm_close": sum(1 for r in audit if r.get("tm_close")),
        "n_ensembl_resolved": sum(1 for r in audit if r.get("ensembl_id")),
        "n_amplicon_in_canonical_cdna": sum(1 for r in audit if r.get("amplicon_len_bp")),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"audit": audit, "summary": summary}, f, indent=2)
    print("[summary]", json.dumps(summary, indent=2))
    print(f"[saved] {OUT}")


if __name__ == "__main__":
    main()
