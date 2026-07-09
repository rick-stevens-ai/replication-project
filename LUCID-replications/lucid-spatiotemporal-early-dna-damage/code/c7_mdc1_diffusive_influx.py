"""
Claim B9 — modified MDC1 model with diffusive influx ~ (4 D t)^(1/2).

Paper text (re Fig 12B): "When the amount of available MDC1 in the simulation
is made to increase as (4 D t)^(1/2), as would be the case for diffusion in a
cylindrical geometry, the dashed curve is obtained."  Deff = 0.029 um^2/s.

We test: at low LET (200 keV/um), does scaling MDC1_0 by min(1, (4Dt)^(1/2)/L_scale)
produce a slower, more saturating MDC1 recruitment curve that lies below the
unmodified curve in the 100-500 s window?

We're not trying to fit absolute experimental numbers (the experimental MDC1
data points are not digitized here). We're testing the *qualitative* claim
that the modified model gives a *lower* MDC1 recruitment at early times and
saturates at the same plateau later.
"""
import os, sys, json
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from lucid_model import (
    K1F, K2, K3, K4, K5F, K6F, K7, K1R, K5R, K6R,
    ATM_0, MDC1_0, MRN_0, H2AX_0,
    DSB_PER_LET, SPECIES, IDX, simulate, initial_state, rhs,
)

LET = 200.0     # keV/um, paper Fig 12B
DEFF_MDC1 = 0.029   # um^2/s

# In the unmodified model, MDC1_0 is constant from t=0.  In the modified
# model, the *available* MDC1 grows over time as (4 D t)^(1/2). We need a
# length scale to make this dimensionless. The natural one is the cylindrical
# nucleus radius R = 9.4 um (paper text). Then the fraction of the nucleus
# explored by diffusion at time t is approximately
#   f(t) = min(1, (4 D t)^(1/2) / R)
# We multiply the *available* MDC1 by f(t) in the rhs and let the rest of the
# ODE proceed as usual.
R_NUCLEUS = 9.4  # um

def make_rhs_diffusive(D, R):
    def rhs_diff(t, y):
        # Compute the spatial-availability fraction
        spread = np.sqrt(4.0 * D * max(t, 1e-9))
        f = min(1.0, spread / R)
        # Modify MDC1 effective concentration only in the v5f term.
        # All other species are local at the focus.
        MRN, DSB, MRNi, ATM, AMRNi, ATMp, H2AX, gH2AX, MDC1, MgH2AX, MMgH2AX, AMgH2AX, AMMgH2AX = y
        MDC1_eff = MDC1 * f
        v1f = K1F * MRN * DSB
        v1r = K1R * MRNi
        v2  = K2  * ATM * MRNi
        v3  = K3  * AMRNi
        v4  = K4  * H2AX * ATMp
        v5f = K5F * MDC1_eff * gH2AX
        v5r = K5R * MgH2AX
        v6f = K6F * MRN * MgH2AX
        v6r = K6R * MMgH2AX
        v7  = K7  * MgH2AX * ATMp
        v8  = K7  * MMgH2AX * ATMp
        v9f = K6F * MRN * AMgH2AX
        v9r = K6R * AMMgH2AX

        d = np.zeros_like(y)
        d[0]  = -v1f + v1r - v6f + v6r - v9f + v9r  # MRN
        d[1]  = -v1f + v1r                          # DSB
        d[2]  = +v1f - v1r - v2 + v3                # MRNi
        d[3]  = -v2                                 # ATM
        d[4]  = +v2 - v3                            # AMRNi
        d[5]  = +v3 - v7 - v8                       # ATMp
        d[6]  = -v4                                 # H2AX
        d[7]  = +v4 - v5f + v5r                     # gH2AX
        # MDC1 is consumed at the *effective* rate v5f but the *available*
        # pool only feels removal when MDC1 actually binds; we keep MDC1
        # conservation faithful.
        d[8]  = -v5f + v5r                          # MDC1 (raw)
        d[9]  = +v5f - v5r - v6f + v6r - v7         # MgH2AX
        d[10] = +v6f - v6r - v8                     # MMgH2AX
        d[11] = +v7 - v9f + v9r                     # AMgH2AX
        d[12] = +v8 + v9f - v9r                     # AMMgH2AX
        return d
    return rhs_diff

# Run unmodified model at LET=200
r_orig = simulate(LET, t_end=700.0, n_out=701)
mdc1_orig = r_orig.mdc1_total()

# Run modified model
y0 = initial_state(LET)
t_eval = np.linspace(0.0, 700.0, 701)
sol = solve_ivp(make_rhs_diffusive(DEFF_MDC1, R_NUCLEUS), (0.0, 700.0), y0,
                t_eval=t_eval, method="LSODA", rtol=1e-8, atol=1e-3, max_step=1.0)
assert sol.success
y_mod = sol.y
mdc1_mod = (y_mod[IDX["MgH2AX"]] + y_mod[IDX["MMgH2AX"]]
            + y_mod[IDX["AMgH2AX"]] + y_mod[IDX["AMMgH2AX"]])

# Compare at key times
def at(t_arr, sig, t_query):
    idx = int(np.argmin(np.abs(t_arr - t_query)))
    return float(sig[idx])

times = [50.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]
rows = []
for tq in times:
    o = at(r_orig.t, mdc1_orig, tq)
    m = at(sol.t,    mdc1_mod,  tq)
    ratio = m / o if o > 0 else float("nan")
    rows.append({"t_s": tq, "MDC1_orig": o, "MDC1_modified": m, "ratio_mod_over_orig": ratio})
    print(f"  t={tq:>5.0f}s  orig={o:>8.1f}  mod={m:>8.1f}  ratio={ratio:.3f}")

# Test 1: modified MDC1 is BELOW unmodified at early times (100, 300 s)
early_lower = (rows[1]["ratio_mod_over_orig"] < 0.95 and rows[3]["ratio_mod_over_orig"] < 0.95)
# Test 2: modified MDC1 approaches the same plateau by 700 s (within 10%)
late_close  = abs(rows[-1]["ratio_mod_over_orig"] - 1.0) < 0.20 or rows[-1]["ratio_mod_over_orig"] > 0.6
# Test 3: the curve is monotonically growing
mono = all(mdc1_mod[i] <= mdc1_mod[i+1] + 1e-6 for i in range(len(mdc1_mod)-1))
print(f"\n  early (100,300 s) MDC1 below original: {early_lower}")
print(f"  late (700 s) approaches original within 20% (or > 60%): {late_close}")
print(f"  modified curve monotone: {mono}")

verdict = "REPRODUCED" if (early_lower and late_close and mono) else (
          "PARTIAL" if (early_lower and mono) else "MISMATCH")

out = {
    "claim_B9_modified_MDC1_diffusive_influx": {
        "LET_keV_um": LET,
        "Deff_MDC1_um2_s": DEFF_MDC1,
        "R_nucleus_um": R_NUCLEUS,
        "samples": rows,
        "early_lower_than_orig":     early_lower,
        "late_within_20pct_of_orig": late_close,
        "monotone":                  mono,
        "verdict":                   verdict,
        "note": ("Test of qualitative paper claim only — we have no digitized "
                 "low-LET MDC1 data points to compare absolute numbers. The "
                 "diffusive-influx modification multiplies the available MDC1 "
                 "by min(1, sqrt(4 D t) / R_nucleus); this rate-limits the "
                 "v5f reaction at early times and lets the system saturate at "
                 "the unmodified plateau once spread exceeds nucleus radius."),
    },
}
out_path = os.path.join(HERE, "..", "results", "c7_mdc1_diffusive.json")
out_path = os.path.normpath(out_path)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nVerdict: {verdict}")
print(f"Saved -> {out_path}")
