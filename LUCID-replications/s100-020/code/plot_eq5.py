#!/usr/bin/env python3
"""Plot Eq. 5 against Table 1 column 1 (DSB clusters, outermost shell)."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = Path(__file__).resolve().parent.parent
tab = np.genfromtxt(here / "evidence" / "eq5_vs_table1.csv", delimiter=",", names=True)
fine = np.genfromtxt(here / "evidence" / "eq5_fine_curve.csv", delimiter=",", names=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

ax1.semilogx(fine['E_n_MeV'], fine['RBE_Eq5'], '-', color='C0', lw=1.5,
             label='Eq. 5 (replicated, published q-params)')
ax1.semilogx(tab['E_n_MeV'], tab['RBE_Table1_shell1'], 'o', color='C3', ms=6,
             label='Paper Table 1, shell #1 (DSB clusters)')
ax1.set_xlabel(r'Incident neutron energy $E_n$ (MeV)')
ax1.set_ylabel(r'RBE (DSB clusters), outermost shell #1')
ax1.set_title("Eq. 5 vs Table 1 (Mentana et al. 2025)")
ax1.grid(True, which='both', alpha=0.3)
ax1.legend(loc='upper left', fontsize=8)
ax1.set_xlim(1e-8, 1e5)
ax1.set_ylim(0, 18)

# residuals
ax2.semilogx(tab['E_n_MeV'], tab['abs_err'], 'o-', color='C2')
ax2.axhline(0, color='k', lw=0.5)
ax2.axhline( 0.5, ls='--', color='gray', lw=0.7, label='±0.5 (Table 1 rounding ~0.05)')
ax2.axhline(-0.5, ls='--', color='gray', lw=0.7)
ax2.axhline( 1.0, ls=':',  color='gray', lw=0.7, label='±1.0')
ax2.axhline(-1.0, ls=':',  color='gray', lw=0.7)
ax2.set_xlabel(r'$E_n$ (MeV)')
ax2.set_ylabel('Eq.5 − Table1  [RBE units]')
ax2.set_title('Replication residuals (RMSE = {:.2f})'.format(
    float(np.sqrt(np.mean(tab['abs_err']**2)))))
ax2.grid(True, which='both', alpha=0.3)
ax2.legend(fontsize=8)

fig.tight_layout()
out = here / "figures" / "eq5_replication.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
print(f"Wrote {out}")
