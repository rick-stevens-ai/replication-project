#!/usr/bin/env python3
"""Compute surface energies, work functions, plot facet comparison.

Surface energy:
  sigma = (E_slab - n_fu * E_bulk_per_atom * N_slab_atoms_in_units_of_bulk) / (2*A)
  Practically: sigma = (E_slab - (N_slab/N_bulk) * E_bulk) / (2 A)

Work function:
  Phi = V_vac - E_F
  V_vac extracted from planar-averaged total potential in the vacuum region.
  E_F from QE scf.out 'the Fermi energy is'.
"""
import os, sys, json, re, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/1981773-Effect-of-Single-Atom-Platinum-Pt/replication')
FAC  = os.path.join(BASE, 'facets')
FIG  = os.path.join(BASE, 'figures')

# Bulk reference (from existing bulk SCF, 44 atoms)
E_BULK_RY = -5793.26164041
N_BULK    = 44
RY_TO_EV  = 13.605693122994
E_BULK_PER_ATOM_EV = E_BULK_RY * RY_TO_EV / N_BULK

# Pt-doped: subtracting (E_clean - E_Ti_atom) and adding E_Pt_atom is the
# standard treatment, but the paper uses E_Pt-LTO_surf - E_LTO_surf - E_Pt
# for adsorption energy. We'll just track the slab total E and skip true
# adsorption because Pt here REPLACES a surface Ti (not adsorbed).
# Surface energy of Pt-doped slab is reported as 'effective' value ignoring
# the 1-atom Ti->Pt swap chemical-potential correction.

def parse_scf_out(path):
    data = dict(path=path, ok=False)
    if not os.path.exists(path):
        return data
    txt = open(path).read()
    m = re.search(r'!\s+total energy\s*=\s*(-?\d+\.\d+)\s*Ry', txt)
    if m: data['total_energy_Ry'] = float(m.group(1))
    m = re.search(r'the Fermi energy is\s+(-?\d+\.\d+)\s*ev', txt)
    if m: data['fermi_eV'] = float(m.group(1))
    m = re.search(r'JOB DONE', txt)
    data['ok'] = bool(m)
    # Cell vectors and atoms
    m = re.search(r'lattice parameter \(alat\)\s*=\s*(\d+\.\d+)', txt)
    if m: data['alat_au'] = float(m.group(1))
    m = re.search(r'number of atoms/cell\s*=\s*(\d+)', txt)
    if m: data['nat'] = int(m.group(1))
    # Crystal axes (3 lines after "crystal axes:")
    m = re.search(r'crystal axes: \(cart\. coord\. in units of alat\)\s*\n\s*a\(1\)\s*=\s*\(([^\)]+)\)\s*\n\s*a\(2\)\s*=\s*\(([^\)]+)\)\s*\n\s*a\(3\)\s*=\s*\(([^\)]+)\)', txt)
    if m and 'alat_au' in data:
        a1 = [float(x) for x in m.group(1).split()]
        a2 = [float(x) for x in m.group(2).split()]
        a3 = [float(x) for x in m.group(3).split()]
        alat_A = data['alat_au'] * 0.529177210903
        cell = np.array([a1, a2, a3]) * alat_A
        # Surface area = |a1 x a2| (z-stacking convention)
        area = np.linalg.norm(np.cross(cell[0], cell[1]))
        data['cell_A'] = cell.tolist()
        data['surface_area_A2'] = float(area)
    return data

facets = ['100', '101', '110']
runs = {}
for f in facets:
    for tag in ('clean', 'Pt'):
        key = f'{f}_{tag}'
        p = os.path.join(FAC, f'run_{key}', 'scf.out')
        runs[key] = parse_scf_out(p)

# Compute surface energies
EV_PER_A2_TO_J_M2 = 16.0218  # eV/Å² -> J/m²
results = dict(bulk_ref_E_Ry=E_BULK_RY, bulk_ref_E_per_atom_eV=E_BULK_PER_ATOM_EV)
results['runs'] = {}
for key, r in runs.items():
    if 'total_energy_Ry' not in r:
        results['runs'][key] = dict(status='missing', detail=r)
        continue
    nat = r.get('nat', 88)
    E_slab_eV = r['total_energy_Ry'] * RY_TO_EV
    A = r['surface_area_A2']
    # Use atom-count ratio for surface energy estimate (clean: pure LTO; Pt-doped:
    # we approximate without chemical potential correction, then add caveat)
    if key.endswith('_clean'):
        E_ref = (nat / N_BULK) * E_BULK_RY * RY_TO_EV
        sigma_eV_A2 = (E_slab_eV - E_ref) / (2.0 * A)
    else:
        # For Pt slab, subtract 1 Ti atom's bulk E and approximate Pt atom E as 0
        # (rough); honest caveat in REPORT. Better would be Pt bulk E.
        E_ref = ((nat - 1) / N_BULK) * E_BULK_RY * RY_TO_EV  # approx
        sigma_eV_A2 = (E_slab_eV - E_ref) / (2.0 * A)
    sigma_J_m2 = sigma_eV_A2 * EV_PER_A2_TO_J_M2
    results['runs'][key] = dict(
        status='ok' if r.get('ok') else 'partial',
        nat=nat,
        E_slab_eV=E_slab_eV,
        E_ref_eV=E_ref,
        surface_area_A2=A,
        sigma_eV_per_A2=sigma_eV_A2,
        sigma_J_per_m2=sigma_J_m2,
        fermi_eV=r.get('fermi_eV'),
    )

# Try to compute work function from planar-averaged potential if .pot files exist
def parse_avg_dat(path):
    """Parse output of average.x: lines of (z, V_avg, V_macro)."""
    if not os.path.exists(path): return None
    arr = np.loadtxt(path, comments='#')
    return arr

for key in runs.keys():
    avg_path = os.path.join(FAC, f'run_{key}', 'avg.dat')
    arr = parse_avg_dat(avg_path)
    if arr is None: continue
    z = arr[:, 0]
    Vmacro = arr[:, 2] if arr.shape[1] >= 3 else arr[:, 1]
    Vmax = float(Vmacro.max())  # vacuum potential
    Vmax_eV = Vmax * RY_TO_EV
    Ef = results['runs'][key].get('fermi_eV')
    if Ef is not None:
        results['runs'][key]['V_vac_eV'] = Vmax_eV
        results['runs'][key]['work_function_eV'] = Vmax_eV - Ef

# Paper reference values
results['paper'] = {
    'sigma_J_m2': {'001': 0.87, '100': 1.20, '101': 1.67},
    'note': 'Paper Table values for clean surface energy (relaxed)',
    'pt_adsorption_eV': {'100': -2.13, '101': -2.62, '001': None},
}

with open(os.path.join(BASE, 'results_facets.json'), 'w') as f:
    json.dump(results, f, indent=2, default=lambda x: float(x))

print(json.dumps(results, indent=2, default=lambda x: float(x)))

# Plot facet comparison
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

ax = axes[0]
labels = ['(001)', '(100)', '(101)', '(110)']
paper = [0.87, 1.20, 1.67, None]
ours_clean = []
# (001) we don't have a fresh clean SCF in this run; use the existing one
# Try to parse existing slab_001 SCF from the previous tier:
prev = parse_scf_out(os.path.join(BASE, 'slab_001', 'lto_scf_final.out'))
if 'total_energy_Ry' in prev:
    nat = prev.get('nat', 44)
    A = prev.get('surface_area_A2', 1.0)
    E_slab_eV = prev['total_energy_Ry'] * RY_TO_EV
    E_ref = (nat / N_BULK) * E_BULK_RY * RY_TO_EV
    sigma = (E_slab_eV - E_ref) / (2.0 * A) * EV_PER_A2_TO_J_M2
    ours_clean.append(sigma)
    results['runs']['001_clean_existing'] = dict(
        sigma_J_per_m2=sigma, surface_area_A2=A, nat=nat,
        E_slab_eV=E_slab_eV, fermi_eV=prev.get('fermi_eV'),
    )
else:
    ours_clean.append(None)
for f in ('100', '101', '110'):
    r = results['runs'].get(f'{f}_clean', {})
    ours_clean.append(r.get('sigma_J_per_m2'))

xs = np.arange(len(labels))
w = 0.35
paper_vals = [v if v is not None else 0 for v in paper]
ours_vals  = [v if v is not None else 0 for v in ours_clean]
b1 = ax.bar(xs - w/2, paper_vals, w, label='Paper', color='#888', alpha=0.7)
b2 = ax.bar(xs + w/2, ours_vals,  w, label='This work', color='C2', alpha=0.85)
ax.set_xticks(xs); ax.set_xticklabels(labels)
ax.set_ylabel('Surface energy σ (J/m²)')
ax.set_title('Clean LTO surface energy by facet')
ax.legend(fontsize=9)
for x, v in zip(xs, ours_vals):
    if v: ax.text(x + w/2, v + 0.05, f'{v:.2f}', ha='center', fontsize=8)
for x, v in zip(xs, paper_vals):
    if v: ax.text(x - w/2, v + 0.05, f'{v:.2f}', ha='center', fontsize=8)

# Right: work function bars per facet (clean vs Pt) if we have them
ax = axes[1]
have_wf = []
for f in ('100', '101', '110'):
    wc = results['runs'].get(f'{f}_clean', {}).get('work_function_eV')
    wp = results['runs'].get(f'{f}_Pt',    {}).get('work_function_eV')
    have_wf.append((f, wc, wp))
xs = np.arange(len(have_wf))
clean = [v[1] if v[1] is not None else 0 for v in have_wf]
ptv   = [v[2] if v[2] is not None else 0 for v in have_wf]
ax.bar(xs - w/2, clean, w, label='Clean', color='C0', alpha=0.85)
ax.bar(xs + w/2, ptv,   w, label='Pt-doped', color='C3', alpha=0.85)
ax.set_xticks(xs); ax.set_xticklabels(['(' + v[0] + ')' for v in have_wf])
ax.set_ylabel('Work function Φ (eV)')
ax.set_title('Work function: clean vs. Pt-doped facet')
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'facet_comparison.png'), dpi=160)
plt.savefig(os.path.join(FIG, 'facet_comparison.pdf'))
print('Wrote', os.path.join(FIG, 'facet_comparison.png'))

# Re-write results with the existing-001 figures included
with open(os.path.join(BASE, 'results_facets.json'), 'w') as f:
    json.dump(results, f, indent=2, default=lambda x: float(x))
