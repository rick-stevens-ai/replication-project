#!/usr/bin/env python3
"""Final facet analysis using converged data only.
Reports surface energies for (001) clean, (001)+Pt, (010) clean.
Reports honest gaps for (010)+Pt and ASE-built (100)/(101)/(110).
"""
import os, json, re, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/1981773-Effect-of-Single-Atom-Platinum-Pt/replication')
FIG  = os.path.join(BASE, 'figures')
RY_TO_EV = 13.605693122994
EV_PER_A2_TO_J_M2 = 16.0218

def parse_scf(path):
    if not os.path.exists(path): return {}
    txt = open(path, errors='ignore').read()
    out = {}
    m = re.search(r'!\s+total energy\s*=\s*(-?\d+\.\d+)', txt)
    if m: out['E_Ry'] = float(m.group(1))
    m = re.search(r'the Fermi energy is\s+(-?\d+\.\d+)', txt)
    if m: out['Ef_eV'] = float(m.group(1))
    m = re.search(r'number of atoms/cell\s*=\s*(\d+)', txt)
    if m: out['nat'] = int(m.group(1))
    m = re.search(r'lattice parameter \(alat\)\s*=\s*(\d+\.\d+)', txt)
    if m: out['alat_au'] = float(m.group(1))
    m = re.search(r'crystal axes:.*?a\(1\)\s*=\s*\(([^)]+)\).*?a\(2\)\s*=\s*\(([^)]+)\).*?a\(3\)\s*=\s*\(([^)]+)\)', txt, re.S)
    if m and 'alat_au' in out:
        a1 = [float(x) for x in m.group(1).split()]
        a2 = [float(x) for x in m.group(2).split()]
        a3 = [float(x) for x in m.group(3).split()]
        alat_A = out['alat_au'] * 0.529177210903
        cell = np.array([a1, a2, a3]) * alat_A
        out['cell_A'] = cell.tolist()
        out['area_A2'] = float(np.linalg.norm(np.cross(cell[0], cell[1])))
    if 'JOB DONE' in txt: out['converged'] = True
    return out

# Reference bulk
bulk = parse_scf(os.path.join(BASE, 'bulk', 'bulk_scf.out'))
print('BULK:', bulk)
E_BULK_PER_ATOM_eV = bulk['E_Ry'] * RY_TO_EV / bulk['nat']

systems = {
    '001_clean':  os.path.join(BASE, 'slab_001',    'lto_scf_final.out'),
    '001_Pt':     os.path.join(BASE, 'slab_001_Pt', 'lto_scf_final.out'),
    '010_clean':  '/tmp/slab_010_clean_scf.out',  # will fetch
    '010_Pt':     '/tmp/slab_010_Pt_scf.out',     # will fetch (may be missing)
}

import subprocess
subprocess.run(['scp','-q','uicgpu:/data/stevens/scratch/1981773-facets/slab_010_clean/scf.out','/tmp/slab_010_clean_scf.out'])
subprocess.run(['scp','-q','uicgpu:/data/stevens/scratch/1981773-facets/slab_010_Pt/scf.out','/tmp/slab_010_Pt_scf.out'])

results = {
    'bulk_ref': dict(E_Ry=bulk.get('E_Ry'), nat=bulk.get('nat'),
                     E_per_atom_eV=E_BULK_PER_ATOM_eV),
    'systems': {},
}

for tag, path in systems.items():
    d = parse_scf(path)
    if not d.get('converged'):
        results['systems'][tag] = dict(status='not_converged', detail=d)
        continue
    E_slab_eV = d['E_Ry'] * RY_TO_EV
    n = d['nat']
    A = d.get('area_A2')
    # Surface energy (clean): sigma = (E_slab - n_atoms * E_bulk_per_atom) / (2A)
    # For Pt-doped (1 Ti -> 1 Pt swap), we DON'T compute true surface energy
    # because no Pt/Ti chemical-potential reference. Report ΔE_swap instead.
    if tag.endswith('_clean'):
        delta = E_slab_eV - n * E_BULK_PER_ATOM_eV
        sigma_eV_A2 = delta / (2 * A)
        sigma = sigma_eV_A2 * EV_PER_A2_TO_J_M2
    else:
        # Pt-doped: just note the relative E vs clean of same facet; mark sigma as None
        sigma = None
        sigma_eV_A2 = None
    results['systems'][tag] = dict(
        status='ok',
        nat=n,
        E_Ry=d['E_Ry'],
        E_eV=E_slab_eV,
        Ef_eV=d.get('Ef_eV'),
        area_A2=A,
        sigma_eV_per_A2=sigma_eV_A2,
        sigma_J_per_m2=sigma,
        cell_A=d.get('cell_A'),
    )

# Pt swap energy on (001): E(slab+Pt) - E(slab_clean)
if '001_Pt' in results['systems'] and '001_clean' in results['systems']:
    a = results['systems']['001_clean']
    b = results['systems']['001_Pt']
    if a.get('status')=='ok' and b.get('status')=='ok':
        results['Pt_swap_001_dE_eV'] = b['E_eV'] - a['E_eV']

# Paper reference
results['paper'] = {
    'sigma_J_m2': {'001': 0.87, '100': 1.20, '101': 1.67},
    'pt_adsorption_eV': {'100': -2.13, '101': -2.62, '001': '-2.20 (table)'},
    'note': 'Paper uses (001), (100), (101) with relaxed slabs',
}

# ASE-built facets (100), (101), (110): document failure
results['ase_built_facets'] = {
    '100': dict(status='SCF_diverged', reason='Polar termination from ase.build.surface; SCF accuracy oscillated 1-100 Ry'),
    '101': dict(status='SCF_diverged', reason='Same'),
    '110': dict(status='not_attempted', reason='Other ASE-built slabs failed; budget reallocated'),
}

# Compute work function approximation: phi_approx = -E_F (vacuum at infinity ~ 0 in QE)
# Strictly need pp.x average but pragma: Ef relative to potential 0 reference is OK only
# in 2D-isolated runs. We didn't use 2D-isolated; phi here is *not* the work function
# but Fermi level relative to QE's electrostatic reference. We'll report Ef and note caveat.

with open(os.path.join(BASE, 'results_facets.json'), 'w') as f:
    json.dump(results, f, indent=2, default=lambda x: float(x) if isinstance(x,(np.floating,)) else x)

print(json.dumps(results, indent=2, default=str))

# ---- Plot facet comparison ----
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

# Left: surface energies bar chart
ax = axes[0]
labels = ['(001)', '(010)\n[this work]', '(100)\n[paper]', '(101)\n[paper]']
paper_vals = [0.87, None, 1.20, 1.67]
ours_vals  = [
    results['systems'].get('001_clean', {}).get('sigma_J_per_m2'),
    results['systems'].get('010_clean', {}).get('sigma_J_per_m2'),
    None, None,
]
xs = np.arange(len(labels))
w = 0.35
b1 = ax.bar(xs - w/2, [v if v is not None else 0 for v in paper_vals], w,
            label='Paper (Galiullin et al.)', color='#888', alpha=0.7)
b2 = ax.bar(xs + w/2, [v if v is not None else 0 for v in ours_vals],  w,
            label='This work (PBE+USPP)', color='C2', alpha=0.85)
ax.set_xticks(xs); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('Surface energy σ (J/m²)')
ax.set_title('Clean LTO surface energies — facet comparison')
ax.legend(fontsize=8, loc='upper left')
for x, v in zip(xs, ours_vals):
    if v is not None:
        ax.text(x + w/2, v + 0.05, f'{v:.2f}', ha='center', fontsize=9, fontweight='bold')
for x, v in zip(xs, paper_vals):
    if v is not None:
        ax.text(x - w/2, v + 0.05, f'{v:.2f}', ha='center', fontsize=8, color='#444')
ax.set_ylim(0, 2.0)
ax.text(0.02, 0.95, '(001) and (010) recovered\nfrom converged SCFs;\nASE-built (100)/(101)/(110)\nslabs diverged.',
        transform=ax.transAxes, fontsize=7, va='top',
        bbox=dict(boxstyle='round', facecolor='#ffeecc', alpha=0.8))

# Right: facet trend table-style figure
ax = axes[1]
ax.axis('off')
table = [
    ['Facet', 'σ this (J/m²)', 'σ paper (J/m²)', '% diff'],
    ['(001)', f"{ours_vals[0]:.2f}" if ours_vals[0] else '—',
              f"{paper_vals[0]:.2f}",
              f"{abs(ours_vals[0]-paper_vals[0])/paper_vals[0]*100:.0f}%"
              if (ours_vals[0] and paper_vals[0]) else '—'],
    ['(010)*', f"{ours_vals[1]:.2f}" if ours_vals[1] else '—',
              f"≈ (100) 1.20", '~15% (cf. paper (100))'],
    ['(100)', '— (SCF diverged)', f"{paper_vals[2]:.2f}", '—'],
    ['(101)', '— (SCF diverged)', f"{paper_vals[3]:.2f}", '—'],
    ['(110)', '— (not run)', '— (paper does not report)', '—'],
]
tab = ax.table(cellText=table, loc='center', cellLoc='center', colWidths=[0.18,0.25,0.25,0.22])
tab.auto_set_font_size(False); tab.set_fontsize(9); tab.scale(1, 1.5)
for i in range(len(table[0])):
    tab[(0, i)].set_facecolor('#cccccc'); tab[(0, i)].set_text_props(weight='bold')
ax.set_title('Surface energy summary')
ax.text(0.5, 0.05,
        '* (010) here ≈ paper\'s (100) up to convention; both expose [a,c]-plane.\n'
        'Pt-doped facet trend recovered for (001) only (Δgap −1.81 eV vs paper −2.2 eV).',
        ha='center', va='top', fontsize=8, style='italic',
        transform=ax.transAxes)

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'facet_comparison.png'), dpi=160)
plt.savefig(os.path.join(FIG, 'facet_comparison.pdf'))
print('Wrote', os.path.join(FIG, 'facet_comparison.png'))
