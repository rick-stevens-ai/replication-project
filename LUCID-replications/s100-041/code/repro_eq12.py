"""
Numerical reproduction of Eqs (1)-(2) and Figs 6-7 of
Abolfath, Grosshans, Mohan, Med. Phys. 47 (2020), DOI 10.1002/mp.14548.

Coupled ROS / NROS rate equations:

    dN1/dt = G(t) - 2 Df N1^2 - Df N2 N1     (1)
    dN2/dt =                    Df N1^2       (2)

Pulse parameters as printed in §III A:
    FLASH-UHDR : G1 = 100 cm^-3 s^-1, pulse width 0.01 s   -> integral 1.0
    CDR        : G2 = 0.01 cm^-3 s^-1, pulse width 100 s   -> integral 1.0

Df is not given numerically by the authors; we use Df = 1 in the same
arbitrary units as G, since the figures are unitless log-log plots and
the only quantitative claim is the long-time RATIO N2(FLASH)/N2(CDR) ~ 2.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
FIGDIR = OUT / "figures"
EVDIR = OUT / "evidence"
FIGDIR.mkdir(exist_ok=True, parents=True)
EVDIR.mkdir(exist_ok=True, parents=True)

DF = 1.0  # arbitrary units, matches G units

def make_rhs(G_amp, pulse_width):
    """Return rhs(t, y) for a square pulse of amplitude G_amp over [0, pulse_width]."""
    def rhs(t, y):
        N1, N2 = y
        G = G_amp if (0.0 <= t <= pulse_width) else 0.0
        dN1 = G - 2.0 * DF * N1 * N1 - DF * N2 * N1
        dN2 =       DF * N1 * N1
        return [dN1, dN2]
    return rhs

# Time grids: log-spaced sampling from 1e-4 s to 100 s, matching figs 6-7 axes
t_eval = np.logspace(-4, 2, 600)

# FLASH UHDR pulse
flash_rhs = make_rhs(G_amp=100.0, pulse_width=0.01)
sol_flash = solve_ivp(
    flash_rhs, (0.0, 100.0), [0.0, 0.0],
    method="Radau", t_eval=t_eval, rtol=1e-9, atol=1e-14, max_step=1e-3,
)
assert sol_flash.success, sol_flash.message

# CDR pulse
cdr_rhs = make_rhs(G_amp=0.01, pulse_width=100.0)
sol_cdr = solve_ivp(
    cdr_rhs, (0.0, 100.0), [0.0, 0.0],
    method="Radau", t_eval=t_eval, rtol=1e-9, atol=1e-14, max_step=1e-1,
)
assert sol_cdr.success, sol_cdr.message

t = sol_flash.t
N1_f, N2_f = sol_flash.y
N1_c, N2_c = sol_cdr.y

# ---------- Fig 6 reproduction: N1 vs t ----------
fig, ax = plt.subplots(figsize=(6, 4))
ax.loglog(t, np.maximum(N1_f, 1e-30), label="FLASH UHDR (G=100, width=0.01 s)")
ax.loglog(t, np.maximum(N1_c, 1e-30), label="CDR        (G=0.01, width=100 s)")
ax.set_xlabel("time (s)")
ax.set_ylabel("N1 (ROS, arb. units)")
ax.set_title("Repro of Fig 6 — N1 vs t, FLASH vs CDR\n(Abolfath/Grosshans/Mohan 2020, Eqs 1-2)")
ax.set_xlim(1e-3, 1e2)
ax.set_ylim(1e-3, 2.0)
ax.legend(loc="best")
ax.grid(True, which="both", ls=":", alpha=0.5)
fig.tight_layout()
fig.savefig(FIGDIR / "fig6_repro_N1.png", dpi=140)
plt.close(fig)

# ---------- Fig 7 reproduction: N2 vs t ----------
fig, ax = plt.subplots(figsize=(6, 4))
ax.loglog(t, np.maximum(N2_f, 1e-30), label="FLASH UHDR (G=100, width=0.01 s)")
ax.loglog(t, np.maximum(N2_c, 1e-30), label="CDR        (G=0.01, width=100 s)")
ax.set_xlabel("time (s)")
ax.set_ylabel("N2 (NROS, arb. units)")
ax.set_title("Repro of Fig 7 — N2 vs t, FLASH vs CDR\n(Abolfath/Grosshans/Mohan 2020, Eqs 1-2)")
ax.set_xlim(1e-3, 1e2)
ax.set_ylim(1e-6, 1e1)
ax.legend(loc="best")
ax.grid(True, which="both", ls=":", alpha=0.5)
fig.tight_layout()
fig.savefig(FIGDIR / "fig7_repro_N2.png", dpi=140)
plt.close(fig)

# ---------- Quantitative checks ----------
# Long-time ratio N2(FLASH) / N2(CDR) at t = 100 s  (paper caption: "approximately twice")
N2_flash_final = N2_f[-1]
N2_cdr_final = N2_c[-1]
ratio_late = N2_flash_final / N2_cdr_final

# Peak N1
N1_flash_peak = float(np.max(N1_f))
N1_cdr_peak = float(np.max(N1_c))
t_flash_peak = float(t[np.argmax(N1_f)])
t_cdr_peak = float(t[np.argmax(N1_c)])

# Conservation check: integrate dN2/dt and 2*N2 + N1 + 2*N1*N2 integration
# Actually let's verify total ROS budget: integral of G over time == 1.0 for both
# by construction; verify final mass-balance:
#   N1 + 2*N2  + 2*integral(Df*N1*N1*dt) consumed-by-coalescence + integral(Df*N2*N1*dt) consumed-by-capture
# is conservation-like but not strictly conserved because G2N2N1 captures one N1 onto an N2 without making
# a new N2 (the third term in Eq 1 is just N1 loss, not N2 gain). The paper's model is non-conservative.

with open(EVDIR / "repro_results.txt", "w") as f:
    f.write("=== Abolfath 2020 Med Phys (DOI 10.1002/mp.14548) — Eq 1-2 numerical reproduction ===\n\n")
    f.write(f"Df = {DF} (arb. units, paper does not specify; same units as G)\n\n")
    f.write("FLASH UHDR pulse: G=100 cm^-3 s^-1, width=0.01 s, integral=1.0\n")
    f.write(f"  N1 peak = {N1_flash_peak:.4e} at t = {t_flash_peak:.4e} s\n")
    f.write(f"  N1(t=100s) = {N1_f[-1]:.4e}\n")
    f.write(f"  N2(t=100s) = {N2_flash_final:.4e}\n\n")
    f.write("CDR pulse: G=0.01 cm^-3 s^-1, width=100 s, integral=1.0\n")
    f.write(f"  N1 peak = {N1_cdr_peak:.4e} at t = {t_cdr_peak:.4e} s\n")
    f.write(f"  N1(t=100s) = {N1_c[-1]:.4e}\n")
    f.write(f"  N2(t=100s) = {N2_cdr_final:.4e}\n\n")
    f.write(f"Long-time ratio N2(FLASH) / N2(CDR) at t = 100 s : {ratio_late:.3f}\n")
    f.write("Paper Fig 7 caption claims this ratio is 'approximately twice'.\n")
    f.write(f"Reproduction:  {'PASS' if 1.3 < ratio_late < 3.0 else 'FAIL'} "
            f"(target ~2.0, obtained {ratio_late:.3f})\n\n")
    f.write("N1 ordering at long times: CDR N1 > FLASH N1?  "
            f"{'YES (matches Fig 6)' if N1_c[-1] > N1_f[-1] else 'NO'}\n")
    f.write(f"  N1(FLASH, 100 s) = {N1_f[-1]:.4e}\n")
    f.write(f"  N1(CDR,   100 s) = {N1_c[-1]:.4e}\n")

print("DONE — see evidence/repro_results.txt and figures/")
print(f"Long-time N2(FLASH)/N2(CDR) ratio = {ratio_late:.3f}  (paper claim: ~2)")
