#!/usr/bin/env python3
"""Independent computation of genome statistics for L. lactis LL16.

Rick's standard: no reuse of the pass-1 numbers — recompute from scratch
from the freshly downloaded assembly.
"""
import json
import sys
from pathlib import Path

FASTA = Path(sys.argv[1])

seqs = []
name = None
buf = []
for line in FASTA.read_text().splitlines():
    if line.startswith(">"):
        if name is not None:
            seqs.append((name, "".join(buf).upper()))
        name = line[1:].split()[0]
        buf = []
    else:
        buf.append(line.strip())
if name is not None:
    seqs.append((name, "".join(buf).upper()))

total = sum(len(s) for _, s in seqs)
gc = sum(s.count("G") + s.count("C") for _, s in seqs)
at = sum(s.count("A") + s.count("T") for _, s in seqs)
n  = sum(s.count("N") for _, s in seqs)

lens = sorted((len(s) for _, s in seqs), reverse=True)
cum = 0
n50 = None
for L in lens:
    cum += L
    if cum >= total / 2 and n50 is None:
        n50 = L
        break

out = {
    "input_fasta": str(FASTA),
    "n_contigs": len(seqs),
    "total_bp": total,
    "gc_pct": round(100.0 * gc / (gc + at), 4) if (gc + at) else None,
    "gc_pct_inc_n": round(100.0 * gc / total, 4) if total else None,
    "N_bases": n,
    "N50_bp": n50,
    "largest_contig_bp": lens[0],
    "smallest_contig_bp": lens[-1],
}
print(json.dumps(out, indent=2))
