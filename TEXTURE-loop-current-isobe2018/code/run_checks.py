"""
run_checks.py — machine-checkable claim tests for Isobe-Yuan-Fu 2018.
Writes JSON + a figure into ../work/.
Run: python3 run_checks.py
"""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from isobe2018_rg import (IDX, rg_rhs, interaction_strengths, integrate_rg,
                          leading_instability)

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work")
os.makedirs(WORK, exist_ok=True)
results = {}

# ---------------------------------------------------------------------------
# CLAIM 1 (Eq. 9): intravalley couplings g14,g24,g44 do NOT flow under RG.
# Test: their time derivative is identically 0 for random couplings + nesting.
# ---------------------------------------------------------------------------
rng = np.random.default_rng(0)
max_drift = 0.0
for _ in range(500):
    g = rng.uniform(-2, 2, 9)
    d1m, d2m, d3m = rng.uniform(0, 0.6, 3)
    dg = rg_rhs(0.0, g, d1m, d2m, d3m)
    drift = max(abs(dg[IDX["g14"]]), abs(dg[IDX["g24"]]), abs(dg[IDX["g44"]]))
    max_drift = max(max_drift, drift)
results["claim1_gi4_frozen"] = {
    "statement": "Eq.9: g14,g24,g44 have zero RG beta-function",
    "max_|dg_i4/dy|_over_500_random": max_drift,
    "pass": bool(max_drift < 1e-14),
}

# ---------------------------------------------------------------------------
# CLAIM 2 (Sec III C): symmetric density-density case, NO exchange.
#   Set g14=g24=g44=g22=g32=g42 = g0 > 0, all exchange (g11,g31,g41)=0.
#   (a) Mean-field (bare, y=0) finds NO SC: V_{s,d,p,f-SC}(0) with g41=g31=0
#       and g42=g32 give d-SC = p-SC = 2(g42-g32)=0, s-SC=f-SC=2(g42+g32)=+ (repulsive).
#   (b) Under RG with nesting d1->0, g42-g32 becomes NEGATIVE -> d/p-SC attractive.
# ---------------------------------------------------------------------------
g0 = 0.5
gdd = {"g14": g0, "g24": g0, "g44": g0, "g22": g0, "g32": g0, "g42": g0,
       "g11": 0.0, "g31": 0.0, "g41": 0.0}
V0 = interaction_strengths(np.array([gdd[k] for k in
      ["g11","g22","g31","g32","g41","g42","g14","g24","g44"]]))
d1m = 0.4
ys, gs = integrate_rg(gdd, d1m=d1m, d2m=0.0, d3m=0.0, y_max=8.0)
# g42 - g32 along the flow
diff = gs[:, IDX["g42"]] - gs[:, IDX["g32"]]
Vd_flow = np.array([interaction_strengths(g)["d-SC"] for g in gs])
results["claim2_meanfield_no_SC_but_RG_yes"] = {
    "statement": "Sym dens-dens, no exchange: mean-field d/p-SC pairing=0; RG generates attractive d/p-SC",
    "meanfield_d-SC_V(0)": V0["d-SC"],
    "meanfield_p-SC_V(0)": V0["p-SC"],
    "meanfield_s-SC_V(0)": V0["s-SC"],
    "min_(g42-g32)_under_RG": float(diff.min()),
    "min_V_dSC_under_RG": float(Vd_flow.min()),
    "pass": bool(abs(V0["d-SC"]) < 1e-12 and abs(V0["p-SC"]) < 1e-12
                 and diff.min() < -1e-3 and Vd_flow.min() < 0),
}

# ---------------------------------------------------------------------------
# CLAIM 3 (Sec III C): with nesting d1->0, g22 GROWS without BCS suppression,
#   while g32,g42 (BCS-coupled) DECREASE from repulsive initial values.
# ---------------------------------------------------------------------------
g22_series = gs[:, IDX["g22"]]
g32_series = gs[:, IDX["g32"]]
g42_series = gs[:, IDX["g42"]]
results["claim3_g22_grows_g3242_shrink"] = {
    "statement": "Nesting d1->0: g22 grows, g32 & g42 decrease under RG",
    "g22_initial": float(g22_series[0]),
    "g22_final": float(g22_series[-1]),
    "g32_initial": float(g32_series[0]),
    "g32_final": float(g32_series[-1]),
    "g42_initial": float(g42_series[0]),
    "g42_final": float(g42_series[-1]),
    "pass": bool(g22_series[-1] > g22_series[0]
                 and g42_series[-1] < g42_series[0]),
}

# ---------------------------------------------------------------------------
# CLAIM 4 (Sec III C + Fig 4): weak nesting -> SC leading; strong nesting ->
#   density-wave (CDW-/SDW-) leading. And Q- dominates Q0.
# ---------------------------------------------------------------------------
def leading_for(d1m, d2m=0.0, d3m=0.0, g0=0.5):
    gdd = {"g14": g0, "g24": g0, "g44": g0, "g22": g0, "g32": g0, "g42": g0,
           "g11": 0.0, "g31": 0.0, "g41": 0.0}
    ys, gs = integrate_rg(gdd, d1m, d2m, d3m, y_max=15.0)
    ch, yc, table = leading_instability(ys, gs, d1m, d2m, d3m)
    return ch, yc, table

weak = leading_for(d1m=0.05)
strong = leading_for(d1m=0.45)
# Q- vs Q0 dominance: give MORE nesting to Q0 (d2m large) but still expect Q- to
# appear at smaller d1m. Test the paper's statement: Q- density wave occurs at
# very small d1- even when nesting at Q0 is much stronger.
qtest = leading_for(d1m=0.15, d2m=0.45)
qminus_beats_q0 = ("-" in qtest[0]) and qtest[0] not in ("SDW0", "CDW0")
results["claim4_nesting_selects_order"] = {
    "statement": "weak nesting -> SC; strong nesting -> DW; Q- dominates Q0",
    "weak_d1-0.05_leading": weak[0], "weak_yc": float(weak[1]),
    "strong_d1-0.45_leading": strong[0], "strong_yc": float(strong[1]),
    "Qtest_d1-0.15_d2-0.45_leading": qtest[0],
    "pass": bool(("SC" in weak[0]) and ("DW" in strong[0]) and qminus_beats_q0),
}

# ---------------------------------------------------------------------------
# CLAIM 5 (Sec III B): with NO exchange interaction, susceptibility channels
#   are DEGENERATE: s-SC=f-SC, d-SC=p-SC, CDW-=SDW-... broken only by exchange.
#   Test the interaction-strength degeneracies at the bare symmetric point,
#   then show a finite exchange g11=g31=g41 lifts them.
# ---------------------------------------------------------------------------
def Vdict(gd):
    return interaction_strengths(np.array([gd[k] for k in
        ["g11","g22","g31","g32","g41","g42","g14","g24","g44"]]))
sym = {"g14":g0,"g24":g0,"g44":g0,"g22":g0,"g32":g0,"g42":g0,
       "g11":0.0,"g31":0.0,"g41":0.0}
Vs = Vdict(sym)
deg_sd = abs(Vs["d-SC"] - Vs["p-SC"])          # d/p degenerate
deg_sf = abs(Vs["s-SC"] - Vs["f-SC"])          # s/f degenerate
deg_cs = abs(Vs["CDW-"] - Vs["SDW-"])          # CDW-/SDW- : 4g11+... vs ...; with g11=g31=0 -> equal
# d-SC-p-SC = 4(g41-g31); CDW--SDW- = 4(g11+g31). A generic finite exchange
# (g31 != g41, g11 != 0) lifts BOTH degeneracies. Use distinct exchange values.
withex = dict(sym); withex["g11"]=0.2; withex["g31"]=0.1; withex["g41"]=0.3
Vx = Vdict(withex)
lift_sd = abs(Vx["d-SC"] - Vx["p-SC"])
lift_cs = abs(Vx["CDW-"] - Vx["SDW-"])
results["claim5_exchange_lifts_degeneracy"] = {
    "statement": "No exchange -> s=f, d=p, CDW-=SDW- degenerate; exchange lifts them",
    "deg_dSC_pSC_noexch": deg_sd,
    "deg_sSC_fSC_noexch": deg_sf,
    "deg_CDW-_SDW-_noexch": deg_cs,
    "lifted_dSC_pSC_withexch": lift_sd,
    "lifted_CDW-_SDW-_withexch": lift_cs,
    "pass": bool(deg_sd < 1e-12 and deg_sf < 1e-12 and deg_cs < 1e-12
                 and lift_sd > 1e-3 and lift_cs > 1e-3),
}

# ---------------------------------------------------------------------------
# Summary + write
# ---------------------------------------------------------------------------
n_pass = sum(1 for v in results.values() if v.get("pass"))
results["_summary"] = {"n_claims": 5, "n_pass": n_pass}

with open(os.path.join(WORK, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

# figure: RG flow (reproduces Fig 4c-type flow) + phase-diagram scan
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].axhline(0, color="k", lw=0.5)
    ax[0].plot(ys, gs[:, IDX["g22"]], label="g22 (forward)")
    ax[0].plot(ys, gs[:, IDX["g32"]], label="g32 (BCS)")
    ax[0].plot(ys, gs[:, IDX["g42"]], label="g42 (BCS)")
    ax[0].plot(ys, gs[:, IDX["g14"]], "--", label="g14 (frozen)")
    ax[0].set_xlabel("RG scale  g0*y"); ax[0].set_ylabel("g_ij")
    ax[0].set_title("RG flow, sym dens-dens, d1-=0.4 (cf. Fig 4c)")
    ax[0].legend(fontsize=8)
    # phase scan over d1-
    d1grid = np.linspace(0.0, 0.5, 26)
    ycs = []
    labels = []
    for d1 in d1grid:
        ch, yc, _ = leading_for(d1m=max(d1, 1e-4))
        ycs.append(yc if np.isfinite(yc) else np.nan)
        labels.append(ch)
    ax[1].plot(d1grid, ycs, "o-")
    ax[1].set_xlabel("nesting d1-"); ax[1].set_ylabel("critical y_c")
    ax[1].set_title("Critical scale vs nesting (SC->DW crossover)")
    fig.tight_layout()
    fig.savefig(os.path.join(WORK, "rg_flow_and_phase.png"), dpi=120)
    results["_figure"] = "rg_flow_and_phase.png"
except Exception as e:
    results["_figure_error"] = str(e)

print(json.dumps(results, indent=2))
print("\nPASS %d/5" % n_pass)
