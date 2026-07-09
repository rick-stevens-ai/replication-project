#!/usr/bin/env python3
"""Re-parse all repass logs and rebuild the result CSVs (pass-1 parser bug fix).

The previous run_repass.sh extracted with `awk '{print $NF}'`, which captured
the unit "kJ/mol" instead of the numerical value (the value is at $(NF-1)).
This script re-reads the existing stdout logs (no re-run needed for the
already-completed pka-lig, protein-rna, ion-pmf, sub-solver probes) and
rebuilds clean CSV tables. The Born grid-refinement uses a different solver
configuration and is re-run by run_born_refinement.sh.
"""
import math
import os
import re
import sys
from pathlib import Path

ROOT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/apbs-pb")
LOG  = ROOT / "logs" / "repass"
RES  = ROOT / "results" / "repass"
RES.mkdir(parents=True, exist_ok=True)

RX_NET = re.compile(r"Global net ELEC energy\s*=\s*([-+0-9.eE]+)\s*kJ/mol")

def extract_all_net(path: Path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(errors="ignore").splitlines():
        m = RX_NET.search(line)
        if m:
            try:
                out.append(float(m.group(1)))
            except ValueError:
                pass
    return out

# ----------------------------- 1) pka-lig ---------------------------------
PKA_REF = {
    "apbs-mol-vdw.in":   8.08352,
    "apbs-smol-vdw.in":  20.9630,
    "apbs-mol-surf.in":  119.2610,
    "apbs-smol-surf.in": 108.8770,
}
rows = ["input\treference_v1.5_kJmol\trun_kJmol\tdelta\tstatus"]
for inp, ref in PKA_REF.items():
    log = LOG / f"pka-lig__{inp[:-3]}.stdout.log"
    vals = extract_all_net(log)
    if not vals:
        rows.append(f"{inp}\t{ref}\tNO_LOG\t-\trun-failed")
        continue
    val = vals[-1]   # final "print energy" line
    delta = abs(val - ref)
    status = "MATCH" if delta < 0.01 else "DIFF"
    rows.append(f"{inp}\t{ref}\t{val:.7g}\t{delta:.4g}\t{status}")
(RES / "pka-lig.tsv").write_text("\n".join(rows) + "\n")

# ----------------------------- 2) protein-rna ------------------------------
PRNA_REF = {
    "0.025": 86.74116429351,
    "0.050": 96.06836713867,
    "0.075": 101.1537214883,
    "0.100": 104.6142116108,
    "0.150": 109.3084123761,
    "0.200": 112.5199716537,
    "0.300": 116.8804254687,
    "0.500": 122.0607673699,
}
rows = ["ionstr\treference_kJmol\trun_kJmol\tdelta\trel_pct\tstatus"]
for ionstr, ref in PRNA_REF.items():
    log = LOG / f"protein-rna__{ionstr}.stdout.log"
    vals = extract_all_net(log)
    if len(vals) < 1:
        rows.append(f"{ionstr}\t{ref}\tNO_LOG\t-\t-\trun-failed")
        continue
    val = vals[0]   # complex's energy (README reference is the first elec block)
    delta = abs(val - ref)
    rel = delta / abs(ref) * 100.0
    status = "MATCH" if rel < 0.1 else "DIFF"
    rows.append(f"{ionstr}\t{ref}\t{val:.7g}\t{delta:.4g}\t{rel:.4f}\t{status}")
(RES / "protein-rna.tsv").write_text("\n".join(rows) + "\n")

print("Wrote", RES / "pka-lig.tsv")
print((RES / "pka-lig.tsv").read_text())
print("Wrote", RES / "protein-rna.tsv")
print((RES / "protein-rna.tsv").read_text())
