"""
Reproduce dose-response aspects of Fig 4 (apoptotic fraction by dose) using
the deterministic mean-field interpretation of the Kracikova thresholds.

The paper says (Cell fate decision section):
  - First threshold: P21 elevated -> cell cycle arrest
  - Second threshold: P53pn AND Bax simultaneously elevated -> apoptosis
The exact threshold numerical values are described in Additional file 6
(see report -- they are inferred from Kracikova et al. and a thresholding
procedure). We don't get exact numeric thresholds, but the paper's qualitative
claims are testable: peak P53pn and Bax should both rise monotonically with IR
dose; apoptotic-fraction proxy (peak P53pn * peak BAX) should rise with dose.
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


def ir_pulse(dose_gy):
    if dose_gy <= 0:
        return lambda t: 0.0, 0.0
    pulse_len = dose_gy * 60.0
    rate = 1.0 / 60.0
    return (lambda t: rate if 0 <= t <= pulse_len else 0.0), pulse_len


def run(rnai, dose_gy, t_hours=48.0, tnf_func=None):
    siR = 1 if rnai == "Wip1" else 0
    y0 = model.initial_state(rnai)
    IR_func, _ = ir_pulse(dose_gy)
    if tnf_func is None:
        tnf_func = lambda t: 0.0
    sol = solve_ivp(
        lambda t, y: model.rhs(t, y, IR_func, tnf_func, siR=siR),
        (0.0, t_hours * 3600.0), y0,
        method="LSODA", rtol=1e-6, atol=1e-3, max_step=60.0,
        t_eval=np.linspace(0.0, t_hours * 3600.0, 481),
    )
    return sol


def pick(sol, key):
    return sol.y[model.IDX[key], :]


# ---------- Dose response 0, 2, 4, 6, 8, 10 Gy ----------
doses = [0, 2, 4, 6, 8, 10]
results = {"Ctr": {}, "Wip1": {}}

for rnai in ("Ctr", "Wip1"):
    for d in doses:
        sol = run(rnai, d, t_hours=48.0)
        t_h = sol.t / 3600.0
        p53 = pick(sol, "P53pn")
        bax = pick(sol, "BAX")
        p21 = pick(sol, "P21")
        dsb = pick(sol, "DSB")
        wip = pick(sol, "WIP1n")
        results[rnai][d] = {
            "peak_P53pn": float(p53.max()), "tpeak_P53pn_h": float(t_h[p53.argmax()]),
            "peak_BAX":   float(bax.max()), "tpeak_BAX_h":   float(t_h[bax.argmax()]),
            "peak_P21":   float(p21.max()), "tpeak_P21_h":   float(t_h[p21.argmax()]),
            "peak_DSB":   float(dsb.max()),
            "peak_WIP1n": float(wip.max()),
            "P53pn_24h":  float(p53[t_h >= 24][0]) if (t_h >= 24).any() else None,
            "BAX_24h":    float(bax[t_h >= 24][0]) if (t_h >= 24).any() else None,
            "BAX_48h":    float(bax[-1]),
            "P21_48h":    float(p21[-1]),
            "p53_x_bax_peak": float((p53 * bax).max()),  # apoptotic proxy
        }
        print(f"  {rnai:5s} {d:2d} Gy -> peak p53={p53.max():.0f}  bax_48h={bax[-1]:.0f}  peak_p21={p21.max():.0f}  peak_dsb={dsb.max():.2f}")

with open(os.path.join(EVI_DIR, "dose_response.json"), "w") as f:
    json.dump(results, f, indent=2)


# ---- Plot dose-response curves ----
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, key, ttl in zip(axes, ["peak_P53pn", "peak_P21", "BAX_48h"],
                              ["Peak active p53", "Peak p21", "Bax at 48 h"]):
    for rnai, c in (("Ctr", "C0"), ("Wip1", "C1")):
        vals = [results[rnai][d][key] for d in doses]
        ax.plot(doses, vals, "o-", color=c, label=rnai + "-RNAi")
    ax.set_xlabel("IR dose [Gy]"); ax.set_ylabel(key); ax.set_title(ttl)
    ax.grid(alpha=0.3); ax.legend()
fig.suptitle("Fig 4 reproduction (deterministic mean-field dose response)", y=1.02)
fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "fig4_dose_response.png"),
                                dpi=140, bbox_inches="tight")
plt.close(fig)

# ---------- TNFα experiment (3 conditions, Fig 4c) ----------
print("\n=== TNFα experiments ===")
# (1) TNF only, no IR: 10 ng/ml for 60 min
# (2) IR only (4 Gy), no TNF
# (3) TNF 10 ng/ml for 60 min, then 2 h gap, then 4 Gy IR
def tnf_pulse_then_gap(dose_ngml, dur_s, gap_s):
    """TNF on for `dur_s`, off for `gap_s`, then off forever; returns conc func + when IR starts."""
    def f(t):
        return dose_ngml if 0 <= t < dur_s else 0.0
    return f, dur_s + gap_s


# Case 1: TNF only
sol_tnf_only = run("Ctr", 0.0, t_hours=48.0,
                   tnf_func=tnf_pulse_then_gap(10.0, 3600, 0)[0])

# Case 2: 4 Gy IR only
sol_ir_only = run("Ctr", 4.0, t_hours=48.0)

# Case 3: TNF then IR (need a combined integrator with shifted IR start)
def combined_tnf_ir(dose_gy, tnf_dose, tnf_dur_s, gap_s, rnai="Ctr", t_hours=48.0):
    siR = 1 if rnai == "Wip1" else 0
    y0 = model.initial_state(rnai)
    pulse_len_ir = dose_gy * 60.0
    ir_start = tnf_dur_s + gap_s
    def IR(t):
        return (1.0/60.0) if ir_start <= t <= ir_start + pulse_len_ir else 0.0
    def TNF(t):
        return tnf_dose if 0 <= t < tnf_dur_s else 0.0
    sol = solve_ivp(
        lambda t, y: model.rhs(t, y, IR, TNF, siR=siR),
        (0.0, t_hours * 3600.0), y0,
        method="LSODA", rtol=1e-6, atol=1e-3, max_step=30.0,
        t_eval=np.linspace(0.0, t_hours * 3600.0, 481),
    )
    return sol


sol_combo = combined_tnf_ir(4.0, 10.0, 3600.0, 7200.0)

tnf_results = {
    "TNF_only":   {
        "peak_P53pn": float(pick(sol_tnf_only, "P53pn").max()),
        "peak_BAX":   float(pick(sol_tnf_only, "BAX").max()),
        "BAX_48h":    float(pick(sol_tnf_only, "BAX")[-1]),
        "NFKBn_peak": float(pick(sol_tnf_only, "NFKBn").max()),
    },
    "IR_only_4Gy": {
        "peak_P53pn": float(pick(sol_ir_only, "P53pn").max()),
        "peak_BAX":   float(pick(sol_ir_only, "BAX").max()),
        "BAX_48h":    float(pick(sol_ir_only, "BAX")[-1]),
        "NFKBn_peak": float(pick(sol_ir_only, "NFKBn").max()),
    },
    "TNF_then_IR_4Gy": {
        "peak_P53pn": float(pick(sol_combo, "P53pn").max()),
        "peak_BAX":   float(pick(sol_combo, "BAX").max()),
        "BAX_48h":    float(pick(sol_combo, "BAX")[-1]),
        "NFKBn_peak": float(pick(sol_combo, "NFKBn").max()),
    },
}
print(json.dumps(tnf_results, indent=2))
with open(os.path.join(EVI_DIR, "tnf_experiment.json"), "w") as f:
    json.dump(tnf_results, f, indent=2)

# ---- TNF plot ----
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
t_h = sol_combo.t / 3600.0
axes[0].plot(t_h, pick(sol_tnf_only, "NFKBn"), "C0", label="TNF only")
axes[0].plot(t_h, pick(sol_ir_only,  "NFKBn"), "C1", label="4 Gy IR only")
axes[0].plot(t_h, pick(sol_combo,    "NFKBn"), "C2", label="TNF then 4 Gy")
axes[0].set_title("Nuclear NF-κB"); axes[0].set_ylabel("NFKBn")
axes[1].plot(t_h, pick(sol_tnf_only, "P53pn"), "C0", label="TNF only")
axes[1].plot(t_h, pick(sol_ir_only,  "P53pn"), "C1", label="4 Gy IR only")
axes[1].plot(t_h, pick(sol_combo,    "P53pn"), "C2", label="TNF then 4 Gy")
axes[1].set_title("Active p53"); axes[1].set_ylabel("P53pn")
axes[2].plot(t_h, pick(sol_tnf_only, "BAX"), "C0", label="TNF only")
axes[2].plot(t_h, pick(sol_ir_only,  "BAX"), "C1", label="4 Gy IR only")
axes[2].plot(t_h, pick(sol_combo,    "BAX"), "C2", label="TNF then 4 Gy")
axes[2].set_title("Bax (apoptotic proxy)"); axes[2].set_ylabel("BAX")
for ax in axes:
    ax.set_xlabel("Time [h]"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
fig.suptitle("Fig 4c reproduction: radio-protective effect of TNFα pre-treatment",
             y=1.02)
fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "fig4c_tnf_ir.png"),
                                dpi=140, bbox_inches="tight")
plt.close(fig)
print("Done.")
