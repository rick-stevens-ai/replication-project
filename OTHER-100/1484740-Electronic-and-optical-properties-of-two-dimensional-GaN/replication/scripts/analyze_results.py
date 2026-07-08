#!/usr/bin/env python3
"""
Analysis script for 2D GaN replication (OSTI 1484740)
Processes QE output files and generates figures/data for the report.
"""

import numpy as np
import os
import re
import json

BASEDIR = os.path.expanduser("~/replication/outputs")
FIGDIR = os.path.expanduser("~/replication/figures")
os.makedirs(FIGDIR, exist_ok=True)

def parse_scf_output(filename):
    """Extract key data from SCF output"""
    data = {}
    with open(filename) as f:
        text = f.read()
    
    # Total energy
    m = re.findall(r'!\s+Total energy\s+=\s+([-\d.]+)\s+Ry', text)
    if m:
        data['total_energy_Ry'] = float(m[-1])
        data['total_energy_eV'] = float(m[-1]) * 13.6057
    
    # Band gap
    m = re.search(r'highest occupied, lowest unoccupied level \(ev\):\s+([-\d.]+)\s+([-\d.]+)', text)
    if m:
        data['vbm'] = float(m.group(1))
        data['cbm'] = float(m.group(2))
        data['band_gap'] = data['cbm'] - data['vbm']
    else:
        m = re.search(r'highest occupied level \(ev\):\s+([-\d.]+)', text)
        if m:
            data['vbm'] = float(m.group(1))
    
    # Fermi energy
    m = re.search(r'the Fermi energy is\s+([-\d.]+)\s+ev', text)
    if m:
        data['fermi_energy'] = float(m.group(1))
    
    # Lattice parameter
    m = re.findall(r'CELL_PARAMETERS.*\n\s+([\d.]+)', text)
    if m:
        data['lattice_a'] = float(m[-1])
    
    # Number of electrons
    m = re.search(r'number of electrons\s+=\s+([\d.]+)', text)
    if m:
        data['n_electrons'] = float(m.group(1))
    
    return data

def parse_bands_dat(filename):
    """Parse bands.x output file"""
    bands = []
    kpoints = []
    current_band = []
    current_k = []
    
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 0:
                if current_band:
                    bands.append(current_band)
                    if not kpoints:
                        kpoints = current_k[:]
                    current_band = []
                    current_k = []
            elif len(parts) == 2:
                current_k.append(float(parts[0]))
                current_band.append(float(parts[1]))
    
    if current_band:
        bands.append(current_band)
    
    return np.array(kpoints), np.array(bands)

def parse_relax_output(filename):
    """Extract relaxed structure from vc-relax output"""
    data = {}
    with open(filename) as f:
        text = f.read()
    
    # Final cell
    m = re.findall(r'CELL_PARAMETERS.*?\n(.*?\n.*?\n.*?)\n', text)
    if m:
        cell_lines = m[-1].strip().split('\n')
        cell = []
        for line in cell_lines:
            cell.append([float(x) for x in line.split()])
        data['cell'] = cell
        data['lattice_a'] = cell[0][0]  # a parameter
    
    # Final positions
    m = re.findall(r'ATOMIC_POSITIONS.*?\n((?:.*?\n)+?)(?:End|$)', text)
    if m:
        pos_text = m[-1].strip()
        positions = []
        for line in pos_text.split('\n'):
            parts = line.split()
            if len(parts) >= 4:
                positions.append({
                    'species': parts[0],
                    'x': float(parts[1]),
                    'y': float(parts[2]),
                    'z': float(parts[3])
                })
        data['positions'] = positions
    
    # Total energy
    energies = re.findall(r'!\s+Total energy\s+=\s+([-\d.]+)\s+Ry', text)
    if energies:
        data['total_energy_Ry'] = float(energies[-1])
    
    # Forces
    forces = re.findall(r'Total force =\s+([\d.]+)', text)
    if forces:
        data['final_force'] = float(forces[-1])
    
    return data

def compute_buckling(positions, c_param=20.0):
    """Compute buckling height (Ga-N z-distance) in Angstroms"""
    ga_z = None
    n_z = None
    for p in positions:
        if p['species'] == 'Ga':
            ga_z = p['z'] * c_param
        elif p['species'] == 'N':
            n_z = p['z'] * c_param
    if ga_z is not None and n_z is not None:
        return abs(n_z - ga_z)
    return None

def compute_internal_field(positions, c_param=20.0):
    """Estimate internal electric field from Ga-N polarization"""
    # Simplified: field from dipole of Ga-N bond
    # In real calculation, need plane-averaged potential
    pass

def main():
    results = {}
    
    # Monolayer relaxation
    mono_relax_file = os.path.join(BASEDIR, "mono_relax.out")
    if os.path.exists(mono_relax_file):
        mono_relax = parse_relax_output(mono_relax_file)
        results['monolayer_relax'] = mono_relax
        print(f"Monolayer lattice a = {mono_relax.get('lattice_a', 'N/A')} Å")
        if 'positions' in mono_relax:
            buckling = compute_buckling(mono_relax['positions'])
            results['monolayer_buckling'] = buckling
            print(f"Monolayer buckling = {buckling:.4f} Å")
    
    # Monolayer SCF
    mono_scf_file = os.path.join(BASEDIR, "mono_scf.out")
    if os.path.exists(mono_scf_file):
        mono_scf = parse_scf_output(mono_scf_file)
        results['monolayer_scf'] = mono_scf
        print(f"Monolayer band gap (DFT-PBE) = {mono_scf.get('band_gap', 'N/A')} eV")
        print(f"Monolayer total energy = {mono_scf.get('total_energy_Ry', 'N/A')} Ry")
    
    # Monolayer bands
    mono_bands_file = os.path.join(BASEDIR, "mono_bands.dat")
    if os.path.exists(mono_bands_file):
        kpts, bands = parse_bands_dat(mono_bands_file)
        results['monolayer_bands'] = {
            'n_bands': len(bands),
            'n_kpoints': len(kpts),
            'k_range': [float(kpts.min()), float(kpts.max())]
        }
        print(f"Monolayer: {len(bands)} bands, {len(kpts)} k-points")
        
        # Save band data for plotting
        np.savez(os.path.join(FIGDIR, 'mono_bands.npz'), 
                 kpoints=kpts, bands=bands)
    
    # Bilayer relaxation
    bi_relax_file = os.path.join(BASEDIR, "bi_relax.out")
    if os.path.exists(bi_relax_file):
        bi_relax = parse_relax_output(bi_relax_file)
        results['bilayer_relax'] = bi_relax
        print(f"Bilayer lattice a = {bi_relax.get('lattice_a', 'N/A')} Å")
    
    # Bilayer SCF
    bi_scf_file = os.path.join(BASEDIR, "bi_scf.out")
    if os.path.exists(bi_scf_file):
        bi_scf = parse_scf_output(bi_scf_file)
        results['bilayer_scf'] = bi_scf
        print(f"Bilayer band gap (DFT-PBE) = {bi_scf.get('band_gap', 'N/A')} eV")
    
    # Bilayer bands
    bi_bands_file = os.path.join(BASEDIR, "bi_bands.dat")
    if os.path.exists(bi_bands_file):
        kpts, bands = parse_bands_dat(bi_bands_file)
        results['bilayer_bands'] = {
            'n_bands': len(bands),
            'n_kpoints': len(kpts),
        }
        np.savez(os.path.join(FIGDIR, 'bi_bands.npz'), 
                 kpoints=kpts, bands=bands)
    
    # Save all results
    # Convert numpy types for JSON serialization
    def convert(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"Object of type {type(o)} not serializable")
    
    with open(os.path.join(BASEDIR, 'results_summary.json'), 'w') as f:
        json.dump(results, f, indent=2, default=convert)
    
    print("\nResults saved to results_summary.json")
    return results

if __name__ == "__main__":
    main()
