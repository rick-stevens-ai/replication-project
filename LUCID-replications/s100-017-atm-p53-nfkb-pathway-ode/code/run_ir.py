"""
Reproduce Figs 2 & 3 of Jonak et al. 2016: 10 Gy IR dose for Ctr-RNAi and Wip1-RNAi.

Paper: IR is "1 Gy/min", so 10 Gy = 600 s pulse starting at t=0.
Trajectories saved over 24 h.
"""
import os, json
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import model

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG_DIR = os.path.join(ROOT, "figures")
EVI_DIR = os.path.join(ROOT, "evidence")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(EVI_DIR, exist_ok=True)


def ir_pulse(dose_gy: float, duration_s: float = 60.0):
    """1 Gy/min square pulse of `dose_gy` Gy over `dose_gy * duration_s` seconds."""
    pulse_len = dose_gy * duration_s   # at 1 Gy/min, length is dose*60 s
    rate = dose_gy / pulse_len         # = 1 Gy / 60 s = 1/60 Gy/s
    def f(t):
        return rate if 0 <= t <= pulse_len else 0.0
    return f, pulse_len


def run(rnai: str, dose_gy: float, t_hours: float = 24.0):
    siR = 1 if rnai == "Wip1" else 0
    y0 = model.initial_state(rnai)
    IR_func, pulse_len = ir_pulse(dose_gy)
    TNF_func = lambda t: 0.0
    t_final = t_hours * 3600.0
    sol = solve_ivp(
        fun=lambda t, y: model.rhs(t, y, IR_func, TNF_func, siR=siR),
        t_span=(0.0, t_final),
        y0=y0,
        method="LSODA",
        rtol=1e-6, atol=1e-3,
        max_step=30.0,
        t_eval=np.linspace(0.0, t_final, 481),  # 3-min resolution
    )
    print(f"[{rnai} {dose_gy} Gy] solver status {sol.status}, n={sol.t.size}")
    return sol


# ---------- Run 10 Gy for both lines ----------
sol_ctr  = run("Ctr",  10.0, t_hours=24.0)
sol_w1   = run("Wip1", 10.0, t_hours=24.0)


def pick(sol, name):
    return sol.y[model.IDX[name], :]


t_h = sol_ctr.t / 3600.0

# ---- Fig 2-style: Wip1 kinetics, 10 Gy, Ctr ----
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(t_h, pick(sol_ctr, "WIP1n"), label="Ctr-RNAi", lw=2)
ax.plot(t_h, pick(sol_w1,  "WIP1n"), label="Wip1-RNAi", lw=2, color="C1")
ax.set_xlabel("Time after IR [h]")
ax.set_ylabel("Nuclear Wip1 [molecules]")
ax.set_title("Fig 2 reproduction: Wip1 kinetics after 10 Gy IR")
ax.axvline(18, ls=":", color="grey", alpha=0.5)  # paper: peak ~18 h
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "fig2_wip1.png"), dpi=140)
plt.close(fig)

# ---- Fig 3-style: p53, Mdm2, Chk2 dynamics ----
fig, axes = plt.subplots(2, 2, figsize=(11, 7))
for ax, (key, ttl) in zip(axes.flat, [
    ("P53pn",  "Active nuclear p53"),
    ("MDM2pn", "Active nuclear Mdm2"),
    ("CHK2pn", "Active nuclear Chk2"),
    ("WIP1n",  "Nuclear Wip1"),
]):
    ax.plot(t_h, pick(sol_ctr, key), label="Ctr-RNAi", lw=2)
    ax.plot(t_h, pick(sol_w1,  key), label="Wip1-RNAi", lw=2, color="C1")
    ax.set_xlabel("Time after IR [h]")
    ax.set_ylabel(f"{key} [molecules]")
    ax.set_title(ttl); ax.grid(alpha=0.3); ax.legend()
fig.suptitle("Fig 3 reproduction: 10 Gy IR, Ctr vs Wip1-RNAi", y=1.02)
fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "fig3_p53_mdm2_chk2_wip1.png"),
                                dpi=140, bbox_inches="tight")
plt.close(fig)

# ---- Save full time-series evidence ----
np.savez_compressed(
    os.path.join(EVI_DIR, "trajectories_10Gy.npz"),
    t_s=sol_ctr.t,
    names=np.array(model.NAMES),
    y_ctr=sol_ctr.y,
    y_wip1=sol_w1.y,
)

# ---- Numerical claim checks ----
def stats(sol, key):
    y = pick(sol, key)
    return {
        "peak_value":   float(y.max()),
        "peak_time_h":  float(t_h[y.argmax()]),
        "min_value":    float(y.min()),
        "final_value":  float(y[-1]),
    }

claims = {
    "WIP1n_Ctr":   stats(sol_ctr, "WIP1n"),
    "WIP1n_Wip1":  stats(sol_w1,  "WIP1n"),
    "P53pn_Ctr":   stats(sol_ctr, "P53pn"),
    "P53pn_Wip1":  stats(sol_w1,  "P53pn"),
    "MDM2pn_Ctr":  stats(sol_ctr, "MDM2pn"),
    "MDM2pn_Wip1": stats(sol_w1,  "MDM2pn"),
    "CHK2pn_Ctr":  stats(sol_ctr, "CHK2pn"),
    "CHK2pn_Wip1": stats(sol_w1,  "CHK2pn"),
    "DSB_Ctr":     stats(sol_ctr, "DSB"),
    "BAX_Ctr":     stats(sol_ctr, "BAX"),
    "P21_Ctr":     stats(sol_ctr, "P21"),
    "ATMan_Ctr":   stats(sol_ctr, "ATMan"),
    # 4-fold Wip1 reduction check (paper Result section)
    "wip1_ratio_24h":
        float(pick(sol_w1, "WIP1n")[-1] / max(pick(sol_ctr, "WIP1n")[-1], 1.0)),
}
with open(os.path.join(EVI_DIR, "claims_10Gy.json"), "w") as f:
    json.dump(claims, f, indent=2)
print(json.dumps(claims, indent=2))

print("\nFigures + evidence written.")
