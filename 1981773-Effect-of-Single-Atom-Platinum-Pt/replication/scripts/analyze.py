#!/usr/bin/env python3
"""Analyze QE outputs: extract energies, gaps, structures."""
import os, re, sys
from pathlib import Path
import numpy as np

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))

RY_EV = 13.605693

def parse_energy(path):
    e = None
    for line in open(path):
        m = re.match(r"!\s+total energy\s+=\s+(-?\d+\.\d+)", line)
        if m: e = float(m.group(1))
    return e

def parse_fermi(path):
    ef = None
    for line in open(path):
        m = re.search(r"Fermi energy is\s+(-?\d+\.\d+)", line)
        if m: ef = float(m.group(1))
        m = re.search(r"highest occupied, lowest unoccupied level .*:\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m: ef = (float(m.group(1)), float(m.group(2)))
    return ef

def parse_bandgap_nscf(path):
    """From nscf output: find highest occupied and lowest unoccupied over all k-points."""
    nelec = None
    kblocks = []
    current = []
    with open(path) as f:
        for line in f:
            m = re.search(r"number of electrons\s+=\s+(-?\d+\.\d+)", line)
            if m: nelec = float(m.group(1))
            if line.strip().startswith("k =") or re.match(r"\s+k =", line):
                if current: kblocks.append(current)
                current = []
                continue
            # match band energies (floats on a line)
            parts = line.split()
            if parts and all(re.match(r"-?\d+\.\d+", p) for p in parts):
                try:
                    current.extend(float(p) for p in parts)
                except: pass
        if current: kblocks.append(current)
    if nelec is None or not kblocks: return None
    nocc = int(round(nelec/2))
    homo = max(b[nocc-1] for b in kblocks if len(b) >= nocc)
    lumo = min(b[nocc] for b in kblocks if len(b) > nocc)
    return dict(homo=homo, lumo=lumo, gap=lumo-homo, nelec=nelec, nocc=nocc)

def summary():
    results = {}
    for name, relpath in [
        ("bulk_scf", "bulk/bulk_scf.out"),
        ("bulk_nscf", "bulk/bulk_nscf.out"),
        ("slab_001_relax", "slab_001/slab_relax.out"),
        ("slab_001_scf_final", "slab_001/lto_scf_final.out"),
        ("slab_001_nscf_final", "slab_001/lto_nscf_final.out"),
        ("slab_001_Pt_relax", "slab_001_Pt/slab_Pt_relax.out"),
        ("slab_001_Pt_scf_final", "slab_001_Pt/lto_scf_final.out"),
        ("slab_001_Pt_nscf_final", "slab_001_Pt/lto_nscf_final.out"),
        ("slab_010_relax", "slab_010/slab_relax.out"),
        ("slab_010_Pt_relax", "slab_010_Pt/slab_Pt_relax.out"),
    ]:
        p = ROOT / relpath
        if not p.exists(): continue
        r = {"energy_Ry": parse_energy(p), "fermi": parse_fermi(p)}
        if "nscf" in name or "scf" in name:
            g = parse_bandgap_nscf(p)
            if g: r.update(g)
        results[name] = r
    import json
    print(json.dumps(results, indent=2, default=str))
    # Substitution energy if both available
    return results

if __name__ == "__main__":
    summary()
