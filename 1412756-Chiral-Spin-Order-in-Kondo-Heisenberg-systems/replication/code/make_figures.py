"""Generate replication figures for OSTI 1412756."""
import os, json
import numpy as np
import matplotlib.pyplot as plt
from mean_field import (KHParams, energy_density, optimal_alpha, J_c,
                        thermal_averages, T_c_estimate,
                        scalar_chirality_amplitude)

HERE  = os.path.dirname(__file__)
FIGS  = os.path.abspath(os.path.join(HERE, "..", "figures"))
DATA  = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(FIGS, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

BASE = dict(J_K=1.0, D=10.0, s=0.5, rho_F=0.05, jQ_over_JH=0.0, jG_over_JH=-4.0)

# ---------------------------------------------------------------------------
# Fig 1: Energy functional E0(alpha) for several J_H/J_c values
# ---------------------------------------------------------------------------
p0  = KHParams(J_H=0.0, **BASE)
Jc  = J_c(p0)
print(f"[reproduction] J_c = {Jc:.5e}  (units of bandwidth)")

alphas = np.linspace(1e-4, np.pi/2 - 1e-4, 800)
plt.figure(figsize=(6.4, 4.2))
for ratio, ls in [(0.6, '--'), (1.0, ':'), (1.2, '-'), (1.6, '-'), (2.5, '-')]:
    p = KHParams(J_H=ratio*Jc, **BASE)
    E = energy_density(alphas, p)
    plt.plot(alphas, E - E[0], ls, label=fr'$J_H/J_c = {ratio}$')
plt.axhline(0, color='k', lw=0.4)
plt.xlabel(r'$\alpha$ (rad)')
plt.ylabel(r'$[E_0(\alpha) - E_0(0)]/s^2$')
plt.title('Mean-field energy functional (paper eq. 16)')
plt.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig1_energy_functional.pdf"))
plt.savefig(os.path.join(FIGS, "fig1_energy_functional.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Fig 2: alpha*(J_H) order-parameter curve at T = 0
# ---------------------------------------------------------------------------
J_grid  = np.linspace(0.0, 5*Jc, 200)
alpha_v = np.array([optimal_alpha(KHParams(J_H=JH, **BASE)) for JH in J_grid])

plt.figure(figsize=(6.4, 4.2))
plt.plot(J_grid/Jc, np.sin(alpha_v), label=r'$\sin\alpha^*$')
plt.plot(J_grid/Jc, np.cos(alpha_v), label=r'$\cos\alpha^*$')
plt.axvline(1.0, color='gray', ls=':')
plt.xlabel(r'$J_H / J_c$')
plt.ylabel(r'order parameter components')
plt.title(r'Zero-$T$ optimum $\alpha^*$ vs $J_H$')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig2_alpha_vs_JH.pdf"))
plt.savefig(os.path.join(FIGS, "fig2_alpha_vs_JH.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Fig 3: <sin alpha> vs T for several J_H (Ising-like transition, Fig 3 inset)
# ---------------------------------------------------------------------------
Ts = np.linspace(1e-6, 0.3, 80)
plt.figure(figsize=(6.4, 4.2))
datasets = {}
for ratio in [1.2, 1.5, 2.0, 3.0]:
    p = KHParams(J_H=ratio*Jc, **BASE)
    sa = np.array([thermal_averages(p, T)['m'] for T in Ts])
    plt.plot(Ts, sa, label=fr'$J_H/J_c = {ratio}$')
    datasets[ratio] = sa.tolist()
plt.xlabel(r'$T$ (arb. units)')
plt.ylabel(r'Ising order parameter $m$')
plt.title(r'Ising order parameter (paper Fig. 3 inset)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig3_sinalpha_vs_T.pdf"))
plt.savefig(os.path.join(FIGS, "fig3_sinalpha_vs_T.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Fig 4: Phase diagram T vs J_H/J_c  (paper Fig. 3 main panel)
# ---------------------------------------------------------------------------
ratios = np.linspace(1.02, 3.5, 30)
Tc_list = []
for r in ratios:
    p = KHParams(J_H=r*Jc, **BASE)
    Tc = T_c_estimate(p, tol=5e-3, T_hi=0.5)
    Tc_list.append(Tc)
Tc_arr = np.array(Tc_list)

plt.figure(figsize=(6.4, 4.4))
plt.plot(ratios, Tc_arr, 'o-', label=r'$T_c(J_H)$')
plt.fill_between(ratios, 0, Tc_arr, alpha=0.25, label='AFM-CSL phase')
# Paper predicts T_c ~ (J_H-J_c)^2 / J_K   near the transition
JK = BASE['J_K']
fit_x = np.linspace(1.02, 2.0, 30)
# Fit amplitude by least squares on small (J_H-J_c) range
mask = ratios < 1.8
coef = np.polyfit((ratios[mask]-1.0)**2, Tc_arr[mask], 1)
plt.plot(fit_x, coef[0]*(fit_x-1.0)**2 + coef[1], 'k--',
         label=fr'$\propto (J_H-J_c)^2$ fit')
plt.xlabel(r'$J_H / J_c$')
plt.ylabel(r'$T$')
plt.title('Phase diagram: disordered / AFM-CSL (paper Fig. 3)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig4_phase_diagram.pdf"))
plt.savefig(os.path.join(FIGS, "fig4_phase_diagram.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Fig 5: Scalar chirality |O_c|(T) at J_H = 1.5 J_c
# ---------------------------------------------------------------------------
# Amplitude of scalar chirality = s^3 <sin alpha cos^2 alpha> (geometric
# prefactor absorbed; paper eq. 7).  SCO vanishes in both limits alpha->0
# and alpha->pi/2 and is maximal for intermediate canting, so we pick
# J_H slightly above J_c where alpha* is moderate.
from mean_field import thermal_averages as _ta
p = KHParams(J_H=1.1*Jc, **BASE)
Tc_this = T_c_estimate(p, tol=5e-3, T_hi=0.5)
# dense grid near Tc to resolve mean-field beta = 1/2 rounding
Ts2 = np.sort(np.concatenate([
    np.linspace(1e-6, 1.05*Tc_this, 80),
    np.linspace(1.05*Tc_this, 2.0*max(Tc_this,1e-3), 20),
]))
Oc = np.array([p.s**3 * _ta(p, T, N=8000)['sin_cos2'] for T in Ts2])

plt.figure(figsize=(6.4, 4.2))
plt.plot(Ts2, Oc, 'r-', lw=2)
if Tc_this > 0:
    plt.axvline(Tc_this, color='k', ls=':', label=fr'$T_c\approx{Tc_this:.4f}$')
plt.xlabel(r'$T$')
plt.ylabel(r'$|\mathcal{O}_c|$   (scalar chirality)')
plt.title(r'Scalar spin chirality vs $T$ at $J_H = 1.1\,J_c$')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig5_chirality_vs_T.pdf"))
plt.savefig(os.path.join(FIGS, "fig5_chirality_vs_T.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Save data
# ---------------------------------------------------------------------------
with open(os.path.join(DATA, "results.json"), "w") as f:
    json.dump({
        "params": BASE,
        "J_c": Jc,
        "J_grid_over_Jc": (J_grid/Jc).tolist(),
        "alpha_star": alpha_v.tolist(),
        "Ts": Ts.tolist(),
        "sin_alpha_vs_T": datasets,
        "phase_ratios": ratios.tolist(),
        "Tc": Tc_arr.tolist(),
        "Tc_fit_slope_intercept": coef.tolist(),
        "chirality_Ts": Ts2.tolist(),
        "chirality_Oc": Oc.tolist(),
        "Tc_at_1p5Jc": Tc_this,
    }, f, indent=2)

# ---------------------------------------------------------------------------
# Fig 6: CSL dome - zero-T scalar chirality amplitude vs J_H/J_c
# ---------------------------------------------------------------------------
ratios6 = np.linspace(1.0, 3.0, 80)
SCO = []
for r in ratios6:
    pr = KHParams(J_H=r*Jc, **BASE)
    a = optimal_alpha(pr)
    SCO.append(pr.s**3 * np.sin(a) * np.cos(a)**2)
SCO = np.array(SCO)
plt.figure(figsize=(6.4, 4.2))
plt.plot(ratios6, SCO, 'g-', lw=2)
plt.fill_between(ratios6, 0, SCO, color='green', alpha=0.25)
plt.xlabel(r'$J_H / J_c$')
plt.ylabel(r'$|\mathcal{O}_c|$  at $T = 0$')
plt.title('CSL dome: zero-$T$ chirality amplitude')
plt.tight_layout()
plt.savefig(os.path.join(FIGS, "fig6_csl_dome.pdf"))
plt.savefig(os.path.join(FIGS, "fig6_csl_dome.png"), dpi=150)
plt.close()

print("Figures and data written.")
print(f"  J_c                  = {Jc:.5e}")
print(f"  Tc(J_H=1.5 J_c)      = {Tc_this:.5e}")
print(f"  slope/intercept fit  = {coef}")
