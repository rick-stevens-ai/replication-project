"""Generate convergence figures for Lightning-Laplace replication report."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).parent

# --- Fig 1: L-shape convergence (tol sweep) ----------------------------------
d1 = pd.read_csv(HERE/'exp1_Lshape_convergence.csv')
d1 = d1[d1['maxerr'] < 1].copy()
d1['sqrtN'] = np.sqrt(d1['N_dofs'])

# Drop trailing saturated rows (last two show 3.3e-9 plateau)
d1_ok = d1[d1['maxerr'] < 3e-10].copy()
# Fit log(err) = a - b*sqrt(N)  (root-exp convergence)
x = d1_ok['sqrtN'].to_numpy()
y = np.log(d1_ok['maxerr'].to_numpy())
A = np.vstack([np.ones_like(x), x]).T
coef, *_ = np.linalg.lstsq(A, y, rcond=None)
a_fit, b_fit = coef
fit_line = np.exp(a_fit + b_fit*np.sqrt(d1['N_dofs']))
print(f"Fit: err = {np.exp(a_fit):.2e} * exp({b_fit:.3f}*sqrt(N))")

fig, ax = plt.subplots(figsize=(7,5))
ax.semilogy(d1['sqrtN'], d1['maxerr'], 'o-', label='Lightning (maxerr, adaptive)')
ax.semilogy(d1['sqrtN'], d1['err_probe'], 's--', label='|u(0.99+0.99i) - 1.0267919261073|')
ax.semilogy(d1['sqrtN'], fit_line, ':', color='k',
            label=f'fit: exp({b_fit:.2f}·√N)')
ax.set_xlabel(r'$\sqrt{N}$ (N = total DoFs)')
ax.set_ylabel('error')
ax.set_title('Lightning Laplace solver on L-shape:\nroot-exponential convergence')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(HERE.parent/'report'/'fig1_Lshape_convergence.png', dpi=150)

# --- Fig 2: Lightning vs polynomial-only on L-shape ---------------------------
dL = pd.read_csv(HERE/'exp3_lightning.csv')
dP = pd.read_csv(HERE/'exp3_polynomial.csv')

fig, ax = plt.subplots(figsize=(7,5))
ax.semilogy(np.sqrt(dL['N']),  dL['maxerr'], 'o-', label='Lightning (poles + polynomial)')
ax.semilogy(np.sqrt(dP['N']),  dP['maxerr'], 's-', label='Polynomial only (Arnoldi-stabilised)')
# Reference lines for algebraic convergence rate of polynomials on r^{2/3}
Ns = np.array(dP['N'])
ax.semilogy(np.sqrt(Ns), 0.6*Ns**(-2./3), ':', color='gray', label=r'$\sim N^{-2/3}$')
ax.set_xlabel(r'$\sqrt{N}$')
ax.set_ylabel('boundary max error')
ax.set_title('L-shape: clustered poles turn algebraic → root-exp convergence')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(HERE.parent/'report'/'fig2_poles_vs_polynomial.png', dpi=150)

# --- Fig 3: multi-domain summary ---------------------------------------------
d2 = pd.read_csv(HERE/'exp2_domains.csv')
fig, ax = plt.subplots(figsize=(8,4.5))
y_pos = np.arange(len(d2))
ax.barh(y_pos, d2['walltime_s'], color='tab:blue')
for i, (n, e, t) in enumerate(zip(d2['N_dofs'], d2['maxerr'], d2['walltime_s'])):
    ax.text(t+0.1, i, f'N={n}, err={e:.1e}', va='center', fontsize=8)
ax.set_yticks(y_pos); ax.set_yticklabels(d2['domain'], fontsize=8)
ax.set_xlabel('wall time (s) to tol=1e-8')
ax.set_title('Lightning Laplace: wall time by domain (target tol=1e-8)')
ax.grid(True, axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(HERE.parent/'report'/'fig3_domains.png', dpi=150)

print('plots written to report/')
