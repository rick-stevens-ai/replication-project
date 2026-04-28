#!/usr/bin/env python3
"""Extract time-series diagnostics from PeleC run.log files."""
import re, os, json, sys
from pathlib import Path

RUNS = Path.home() / "Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec/runs"
OUT  = Path.home() / "Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec/analysis"
OUT.mkdir(exist_ok=True)

# Pattern: "TIME = 1.234e-06 Temp        MAX = 1234.56"
# We want to collect per-time records: temp_min, temp_max, mass, fuel_prod, pressure_max
FIELDS = {
    'temp': r'Temp\s+MIN = ([\d\.eE\+\-]+)\s+MAX = ([\d\.eE\+\-]+)',
    'pres': r'pressure\s+MIN = ([\d\.eE\+\-]+)\s+MAX = ([\d\.eE\+\-]+)',
    'dens': r'density\s+MIN = ([\d\.eE\+\-]+)\s+MAX = ([\d\.eE\+\-]+)',
    'massfrac': r'massfrac\s+MIN = ([\d\.eE\+\-]+)\s+MAX = ([\d\.eE\+\-]+)',
}
scalar_fields = {
    'mass': r'MASS\s+=\s+([\d\.eE\+\-]+)',
    'fuel': r'FUEL PROD\s+=\s+([\d\.eE\+\-]+)',
    'rhoe': r'RHO\*e\s+=\s+([\d\.eE\+\-]+)',
}

results = {}
for phi_dir in sorted(RUNS.glob("phi_*")):
    logpath = phi_dir / "run.log"
    if not logpath.exists():
        continue
    phi = phi_dir.name.replace("phi_", "")
    records = {}  # time -> dict of fields
    text = logpath.read_text()
    # Split into sum_interval blocks. Each block has TIME = <t> repeated with different vars.
    for m in re.finditer(r'TIME = ([\d\.eE\+\-]+)\s+(\S.*?)(?=TIME =|\Z)', text, re.S):
        t = float(m.group(1))
        block = m.group(0)
        if t not in records:
            records[t] = {'time': t}
        for fname, pat in FIELDS.items():
            mm = re.search(pat, block)
            if mm:
                records[t][f'{fname}_min'] = float(mm.group(1))
                records[t][f'{fname}_max'] = float(mm.group(2))
        for fname, pat in scalar_fields.items():
            mm = re.search(pat, block)
            if mm:
                records[t][fname] = float(mm.group(1))
    # Sort by time, keep only records with temp (real sum-interval rows)
    sorted_recs = sorted([r for r in records.values() if 'temp_max' in r], key=lambda r: r['time'])
    results[phi] = sorted_recs
    print(f"phi={phi}: {len(sorted_recs)} time points, t_final={sorted_recs[-1]['time']:.6f}s, T_max at final={sorted_recs[-1]['temp_max']:.1f}K")

with open(OUT / 'timeseries.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {OUT / 'timeseries.json'}")
