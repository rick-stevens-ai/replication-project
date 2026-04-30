#!/usr/bin/env python3
"""Build (100), (101), and (110) slabs of LTO for facet comparison.
Outputs QE pw.x scf inputs for each clean facet, and a Pt-doped variant
for each (one surface Ti -> Pt swap).
"""
import os, sys, numpy as np
from ase import Atoms
from ase.io import read, write
from ase.build import surface, sort

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/1981773-Effect-of-Single-Atom-Platinum-Pt/replication')
OUT  = os.path.join(BASE, 'facets')
os.makedirs(OUT, exist_ok=True)

# Build bulk Atoms from QE input
def parse_qe_in(p):
    txt = open(p).read().splitlines()
    cell = []
    pos = []
    sym = []
    mode = None
    for ln in txt:
        s = ln.strip()
        if s.startswith('CELL_PARAMETERS'):
            mode = 'cell'; continue
        if s.startswith('ATOMIC_POSITIONS'):
            mode = 'pos'; continue
        if s.startswith('K_POINTS'):
            mode = None; continue
        if mode == 'cell':
            parts = s.split()
            if len(parts) == 3:
                cell.append([float(x) for x in parts])
            if len(cell) == 3:
                mode = None
        elif mode == 'pos':
            parts = s.split()
            if len(parts) >= 4:
                sym.append(parts[0])
                pos.append([float(parts[1]), float(parts[2]), float(parts[3])])
    cell = np.array(cell)
    pos = np.array(pos)
    # crystal -> cartesian
    cart = pos @ cell
    return Atoms(symbols=sym, positions=cart, cell=cell, pbc=True)

bulk = parse_qe_in(os.path.join(BASE, 'bulk', 'bulk_scf.in'))
print(f"Bulk: {len(bulk)} atoms, cell:\n{bulk.cell.array}")

# Surface energy reference: bulk energy per atom from final scf -5793.26164041 Ry / 44 atoms
E_BULK_RY = -5793.26164041
RY_TO_EV = 13.605693122994
E_BULK_PER_ATOM_EV = E_BULK_RY * RY_TO_EV / 44

# Build slabs with ase.build.surface(bulk, (h,k,l), layers, vacuum)
# For 88-atom slabs (paper's (100) facet, which is what slab_010 already is)
# we want similar atom counts.
# 2 layers x 44-atom bulk = 88 atoms (matches paper's (100) atom count).
specs = [
    # (label, miller, layers, vacuum_A)
    ('100', (1, 0, 0), 2, 10.0),
    ('101', (1, 0, 1), 2, 10.0),
    ('110', (1, 1, 0), 2, 10.0),
]

def build_facet(label, miller, layers, vacuum):
    s = surface(bulk, miller, layers, vacuum=vacuum)
    s = sort(s)
    s.center(vacuum=vacuum, axis=2)
    return s

for label, miller, layers, vac in specs:
    s = build_facet(label, miller, layers, vac)
    print(f"({label}) slab: {len(s)} atoms, cell c={s.cell[2,2]:.2f} A")
    write(os.path.join(OUT, f'slab_{label}.cif'), s)
    write(os.path.join(OUT, f'slab_{label}.xyz'), s)

# Pt-doped variant: replace highest-z Ti with Pt (single-atom doping on surface)
def make_pt(s):
    s2 = s.copy()
    sy = np.array(s2.get_chemical_symbols())
    z = s2.positions[:, 2]
    ti_idx = np.where(sy == 'Ti')[0]
    surf_ti = ti_idx[np.argmax(z[ti_idx])]
    sy[surf_ti] = 'Pt'
    s2.set_chemical_symbols(sy.tolist())
    return s2

for label, miller, layers, vac in specs:
    s = build_facet(label, miller, layers, vac)
    spt = make_pt(s)
    write(os.path.join(OUT, f'slab_{label}_Pt.cif'), spt)
    write(os.path.join(OUT, f'slab_{label}_Pt.xyz'), spt)

print("Built clean and Pt-doped slabs at:", OUT)

# Generate QE pw.x SCF inputs (no relaxation, single-shot)
HEADER = """&CONTROL
  calculation = 'scf'
  restart_mode = 'from_scratch'
  prefix = 'lto'
  outdir = './tmp'
  pseudo_dir = '/home/stevens/projects/replicate-1981773/pseudo'
  verbosity = 'default'
  tprnfor = .true.
  tstress = .true.
  disk_io = 'low'
/
&SYSTEM
  ibrav = 0
  nat = {nat}
  ntyp = {ntyp}
  ecutwfc = 60.0
  ecutrho = 480.0
  occupations = 'smearing'
  smearing = 'gaussian'
  degauss = 0.01
  nosym = .true.
  noinv = .true.
{extra_sys}/
&ELECTRONS
  conv_thr = 1.0d-5
  mixing_beta = 0.3
  electron_maxstep = 150
  diagonalization = 'david'
/
ATOMIC_SPECIES
{species}
CELL_PARAMETERS angstrom
{cell}
ATOMIC_POSITIONS angstrom
{positions}
K_POINTS automatic
  {kx} {ky} 1  0 0 0
"""

PSEUDO = {
    'La': 'La.upf',
    'O' : 'O.upf',
    'Ti': 'Ti.upf',
    'Pt': 'Pt.upf',
}
MASS = {'La':138.9055, 'O':15.999, 'Ti':47.867, 'Pt':195.084}

def write_scf_in(s, out_in, has_pt=False):
    a = s.cell.lengths()[0]; b = s.cell.lengths()[1]
    kx = max(2, int(np.round(20.0 / a)))
    ky = max(2, int(np.round(20.0 / b)))
    species = sorted(set(s.get_chemical_symbols()))
    species_block = '\n'.join(f"  {sp}  {MASS[sp]}  {PSEUDO[sp]}" for sp in species)
    cell_block = '\n'.join('  ' + '  '.join(f"{x:.10f}" for x in row) for row in s.cell.array)
    pos_block = '\n'.join(f"  {sp}  {p[0]:.10f}  {p[1]:.10f}  {p[2]:.10f}"
                          for sp, p in zip(s.get_chemical_symbols(), s.positions))
    extra = ''
    txt = HEADER.format(
        nat=len(s), ntyp=len(species), species=species_block,
        cell=cell_block, positions=pos_block, kx=kx, ky=ky,
        extra_sys=extra,
    )
    with open(out_in, 'w') as f: f.write(txt)
    print('Wrote', out_in, f"nat={len(s)} kx={kx} ky={ky}")

for label, miller, layers, vac in specs:
    for tag, mk in (('clean', lambda x: x), ('Pt', make_pt)):
        s = build_facet(label, miller, layers, vac)
        if tag == 'Pt':
            s = make_pt(s)
        write_scf_in(s, os.path.join(OUT, f'slab_{label}_{tag}_scf.in'),
                     has_pt=(tag == 'Pt'))

# Save bulk reference info
import json
ref = dict(
    E_bulk_total_Ry = E_BULK_RY,
    E_bulk_per_atom_eV = E_BULK_PER_ATOM_EV,
    n_atoms_bulk = 44,
)
with open(os.path.join(OUT, 'bulk_ref.json'), 'w') as f:
    json.dump(ref, f, indent=2)
print('Bulk ref:', ref)
