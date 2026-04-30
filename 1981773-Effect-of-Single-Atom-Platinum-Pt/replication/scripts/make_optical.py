#!/usr/bin/env python3
"""Process Yambo eps data, compute alpha(omega), find absorption edges, plot."""
import numpy as np, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/1981773-Effect-of-Single-Atom-Platinum-Pt/replication')
OD = os.path.join(BASE, 'optical_data')
FIG = os.path.join(BASE, 'figures')

def load(path):
    rows = []
    with open(path) as f:
        for ln in f:
            if ln.startswith('#') or not ln.strip(): continue
            rows.append([float(x) for x in ln.split()])
    a = np.array(rows)
    # cols: E, Im(eps), Re(eps), Im(eps_o), Re(eps_o)
    return a[:,0], a[:,1], a[:,2]

# absorption coefficient alpha = (omega/c) * Im(refractive index n_imag) ; here we use Im(eps)
# Use Im(eps) directly (proportional to absorption); also compute alpha (cm^-1) via
# alpha = 2 omega/c * k where k = sqrt((|eps|-Re eps)/2)
HBAR_EV_S = 6.582119569e-16
C_CMS = 2.99792458e10

def alpha_from_eps(E, im, re):
    abs_eps = np.sqrt(re*re + im*im)
    k = np.sqrt(np.maximum((abs_eps - re)/2.0, 0.0))
    omega = E / HBAR_EV_S
    return 2.0 * omega * k / C_CMS  # cm^-1

systems = {
    'bulk':       'eps_bulk.dat',
    'slab_clean': 'eps_slab_clean.dat',
    'slab_Pt':    'eps_slab_Pt.dat',
}
data = {}
for k, f in systems.items():
    E, im, re = load(os.path.join(OD, f))
    al = alpha_from_eps(E, im, re)
    data[k] = dict(E=E, im=im, re=re, alpha=al)

# Onset = lowest E where Im(eps) > threshold. Use 0.2 (matches earlier convention)
THR = 0.2
def onset(E, im, thr=THR):
    idx = np.where(im > thr)[0]
    if len(idx) == 0: return float('nan')
    return float(E[idx[0]])

# also find "edge" as 1% of max alpha
def edge_alpha(E, alpha, frac=0.05):
    target = frac * alpha.max()
    idx = np.where(alpha > target)[0]
    if len(idx) == 0: return float('nan')
    return float(E[idx[0]])

# Visible band integrated absorption (1.7 - 3.1 eV)
def vis_avg(E, im, lo=1.7, hi=3.1):
    m = (E >= lo) & (E <= hi)
    return float(np.trapezoid(im[m], E[m]) / (hi - lo))

results = {}
for k, d in data.items():
    results[k] = dict(
        onset_im_eps_eV   = onset(d['E'], d['im']),
        edge_5pct_alpha_eV= edge_alpha(d['E'], d['alpha']),
        vis_avg_im_eps    = vis_avg(d['E'], d['im']),
        peak_im_eps       = float(d['im'].max()),
        E_at_peak_eV      = float(d['E'][d['im'].argmax()]),
    )

# Redshift (clean -> Pt) on slab
results['redshift_clean_to_Pt_eV'] = (
    results['slab_clean']['onset_im_eps_eV'] - results['slab_Pt']['onset_im_eps_eV']
)
results['vis_enhancement_Pt_over_clean'] = (
    results['slab_Pt']['vis_avg_im_eps'] / results['slab_clean']['vis_avg_im_eps']
)
results['paper'] = dict(
    redshift_eV = 2.2,
    bulk_gap_eV = 3.8,
    slab_001_clean_gap_eV = 3.2,
    slab_001_Pt_gap_eV = 1.0,
    qual_vis_enhancement = 'Pt activates visible-light absorption',
)
results['agreement'] = dict(
    redshift_pct_diff = abs(results['redshift_clean_to_Pt_eV'] - 2.2) / 2.2 * 100.0,
)

with open(os.path.join(BASE, 'results_optical.json'), 'w') as f:
    json.dump(results, f, indent=2, default=lambda x: float(x))
print(json.dumps(results, indent=2, default=lambda x: float(x)))

# Plot: absorption_edge.png — Im(eps) and alpha vs E for slab_clean / slab_Pt (and bulk faint)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
ax = axes[0]
colors = dict(bulk='#888', slab_clean='C0', slab_Pt='C3')
labels = dict(bulk='Bulk LTO', slab_clean='(001) clean slab', slab_Pt='(001) Pt-doped slab')
for k in ('bulk', 'slab_clean', 'slab_Pt'):
    d = data[k]
    ax.plot(d['E'], d['im'], color=colors[k], lw=1.6, label=labels[k],
            alpha=0.9 if k != 'bulk' else 0.6)
ax.axhline(THR, ls=':', color='k', alpha=0.3, label=f'onset thr Im(ε)={THR}')
ax.axvspan(1.7, 3.1, alpha=0.08, color='orange', label='visible (1.7–3.1 eV)')
ax.set_xlim(0, 6); ax.set_ylim(0, None)
ax.set_xlabel('Photon energy (eV)'); ax.set_ylabel('Im ε(ω)')
ax.set_title('Yambo PBE/RPA dielectric function')
ax.legend(fontsize=8, loc='upper right')

ax = axes[1]
for k in ('slab_clean', 'slab_Pt'):
    d = data[k]
    ax.semilogy(d['E'], np.maximum(d['alpha'], 1e2), color=colors[k], lw=1.6, label=labels[k])
ax.axvline(results['slab_clean']['onset_im_eps_eV'], color='C0', ls='--', alpha=0.5,
           label=f"clean onset {results['slab_clean']['onset_im_eps_eV']:.2f} eV")
ax.axvline(results['slab_Pt']['onset_im_eps_eV'], color='C3', ls='--', alpha=0.5,
           label=f"Pt onset {results['slab_Pt']['onset_im_eps_eV']:.2f} eV")
ax.axvspan(1.7, 3.1, alpha=0.08, color='orange')
ax.set_xlim(0, 6); ax.set_ylim(1e3, 1e7)
ax.set_xlabel('Photon energy (eV)'); ax.set_ylabel('α(ω)  (cm⁻¹)')
ax.set_title(f"Absorption edge — redshift {results['redshift_clean_to_Pt_eV']:.2f} eV "
             f"(paper 2.2 eV, {results['agreement']['redshift_pct_diff']:.0f}% diff)")
ax.legend(fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig(os.path.join(FIG, 'absorption_edge.png'), dpi=160)
plt.savefig(os.path.join(FIG, 'absorption_edge.pdf'))
print('Wrote', os.path.join(FIG, 'absorption_edge.png'))
