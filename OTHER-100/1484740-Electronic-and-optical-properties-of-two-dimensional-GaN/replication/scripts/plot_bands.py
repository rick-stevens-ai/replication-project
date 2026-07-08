#!/usr/bin/env python3
"""
Plot band structure and strain results for 2D GaN replication.
Generates data files for PGFplots in the LaTeX report.
"""
import numpy as np
import re
import os
import sys

BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/1484740-Electronic-and-optical-properties-of-two-dimensional-GaN/replication")
OUTDIR = os.path.join(BASEDIR, "outputs")
REPDIR = os.path.join(BASEDIR, "report")
os.makedirs(REPDIR, exist_ok=True)

def parse_bands_qe(filename):
    """Parse QE bands.dat file"""
    with open(filename) as f:
        header = f.readline()
        # Parse nbnd and nks
        m = re.search(r'nbnd=\s*(\d+),\s*nks=\s*(\d+)', header)
        nbnd = int(m.group(1))
        nks = int(m.group(2))
        
        kpoints = []
        bands = [[] for _ in range(nbnd)]
        
        for ik in range(nks):
            kline = f.readline().split()
            kx, ky, kz = float(kline[0]), float(kline[1]), float(kline[2])
            kpoints.append((kx, ky, kz))
            
            # Read eigenvalues (may span multiple lines)
            eigs = []
            while len(eigs) < nbnd:
                line = f.readline()
                eigs.extend([float(x) for x in line.split()])
            
            for ib in range(nbnd):
                bands[ib].append(eigs[ib])
    
    return np.array(kpoints), np.array(bands)

def kpath_distance(kpoints):
    """Compute cumulative k-path distance"""
    dist = [0.0]
    for i in range(1, len(kpoints)):
        dk = kpoints[i] - kpoints[i-1]
        dist.append(dist[-1] + np.linalg.norm(dk))
    return np.array(dist)

def write_band_data(filename, kdist, bands, efermi=0.0):
    """Write band data for PGFplots"""
    with open(filename, 'w') as f:
        f.write("% k-distance  Energy(eV)\n")
        for ib in range(len(bands)):
            for ik in range(len(kdist)):
                f.write(f"{kdist[ik]:.6f}  {bands[ib][ik] - efermi:.6f}\n")
            f.write("\n")  # Separator between bands

# Parse monolayer bands
mono_bands_file = os.path.join(OUTDIR, "mono_bands.dat")
if os.path.exists(mono_bands_file):
    kpts, bands = parse_bands_qe(mono_bands_file)
    kdist = kpath_distance(kpts)
    
    # VBM from NSCF
    vbm = -5.7937
    cbm = -2.8005
    efermi = (vbm + cbm) / 2  # Mid-gap reference
    
    # Write data for PGFplots
    write_band_data(os.path.join(REPDIR, "mono_bands_data.dat"), kdist, bands, efermi)
    
    # High-symmetry point positions (Gamma=0, M=40, K=80, Gamma=120)
    # Find indices
    gamma1 = 0
    m_idx = 40
    k_idx = 80
    gamma2 = 120
    
    hspts = {
        'Gamma1': kdist[gamma1],
        'M': kdist[m_idx],
        'K': kdist[k_idx],
        'Gamma2': kdist[gamma2],
    }
    
    with open(os.path.join(REPDIR, "mono_hspts.dat"), 'w') as f:
        for name, pos in hspts.items():
            f.write(f"{name}  {pos:.6f}\n")
    
    print(f"Monolayer band structure: {len(bands)} bands, {len(kpts)} k-points")
    print(f"  VBM = {vbm:.4f} eV, CBM = {cbm:.4f} eV, Gap = {cbm-vbm:.4f} eV")
    print(f"  High-sym points: {hspts}")

# Strain data
strain_data = []
for s in [-5, -3, -1, 0, 1, 3, 5]:
    fname = os.path.join(OUTDIR, f"mono_strain_{s}.out")
    if os.path.exists(fname):
        with open(fname) as f:
            text = f.read()
        m = re.search(r'highest occupied, lowest unoccupied level \(ev\):\s+([-\d.]+)\s+([-\d.]+)', text)
        if m:
            vbm = float(m.group(1))
            cbm = float(m.group(2))
            gap = cbm - vbm
            strain_data.append((s, gap))
            
            # Also get total energy
            en = re.findall(r'!\s+Total energy\s+=\s+([-\d.]+)\s+Ry', text)
            if en:
                strain_data[-1] = (s, gap, float(en[-1]) * 13.6057)

if strain_data:
    with open(os.path.join(REPDIR, "strain_gap_data.dat"), 'w') as f:
        f.write("% Strain(%)  BandGap(eV)  TotalEnergy(eV)\n")
        for entry in strain_data:
            if len(entry) == 3:
                f.write(f"{entry[0]}  {entry[1]:.4f}  {entry[2]:.6f}\n")
            else:
                f.write(f"{entry[0]}  {entry[1]:.4f}\n")
    
    print("\nStrain vs Band Gap:")
    for entry in strain_data:
        print(f"  {entry[0]:+d}%: {entry[1]:.4f} eV")

print("\nData files written to:", REPDIR)
