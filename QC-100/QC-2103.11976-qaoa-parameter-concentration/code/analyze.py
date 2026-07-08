"""Post-process the sweep: fold to canonical branch, compare to paper eqs. (9,10)
and fit the p=1 optimum shape beta = pi/(a1 * n + a2) as in eq. (19)."""
import json, math, os
import numpy as np
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVID = os.path.join(ROOT, "report", "evidence")

with open(os.path.join(EVID, "p1_sweep.json")) as f:
    rows = json.load(f)

# Fold to small-beta branch (paper's principal branch): if beta > pi/2, apply symmetry
folded = []
for r in rows:
    n = r["n"]; g = r["gamma_opt"]; b = r["beta_opt"]
    if b > math.pi / 2:
        b = math.pi - b
        g = (2 * math.pi - g) % (2 * math.pi)
    folded.append({"n": n, "gamma_folded": g, "beta_folded": b,
                   "beta_paper_approx": r["beta_paper_approx"],
                   "gamma_paper_approx": r["gamma_paper_approx"],
                   "beta_asymptotic": r["beta_asymptotic"],
                   "gamma_asymptotic": r["gamma_asymptotic"],
                   "overlap": r["overlap"]})

print("Folded p=1 optima vs paper prediction beta = pi/(n+2), gamma = pi*(n+2)/(n+4):")
print(f"{'n':>3} {'beta_opt':>10} {'beta_paper':>11} {'beta_diff':>10}  "
      f"{'gamma_opt':>10} {'gamma_paper':>12} {'gamma_diff':>11}")
for r in folded:
    n = r["n"]
    bd = r["beta_folded"] - r["beta_paper_approx"]
    gd = r["gamma_folded"] - r["gamma_paper_approx"]
    print(f"{n:>3d} {r['beta_folded']:>10.6f} {r['beta_paper_approx']:>11.6f} {bd:>10.3e}  "
          f"{r['gamma_folded']:>10.6f} {r['gamma_paper_approx']:>12.6f} {gd:>11.3e}")

# Fit beta_opt = pi / (a1 * n + a2)
n_arr = np.array([r["n"] for r in folded])
b_arr = np.array([r["beta_folded"] for r in folded])
g_arr = np.array([r["gamma_folded"] for r in folded])

def fit_beta(n, a1, a2):
    return math.pi / (a1 * n + a2)

popt_b, _ = curve_fit(fit_beta, n_arr, b_arr, p0=[1.0, 2.0])
print(f"\nFit beta = pi / ({popt_b[0]:.4f} * n + {popt_b[1]:.4f})   "
      f"(paper says a1=1.04, a2=0.92 for p=5-beta1, and beta=pi/(n+2) for p=1)")

def fit_gamma(n, b1, b2):
    # eq. (19): gamma = b1 * pi - b2 * beta  where beta = pi/(a1 n + a2)
    beta = math.pi / (popt_b[0] * n + popt_b[1])
    return b1 * math.pi - b2 * beta

popt_g, _ = curve_fit(fit_gamma, n_arr, g_arr, p0=[1.0, 2.0])
print(f"Fit gamma = {popt_g[0]:.4f} * pi - {popt_g[1]:.4f} * beta  "
      f"(paper analytical result: gamma = pi - 2 beta, i.e. b1=1, b2=2)")

# Save folded rows + fits
out = {
    "folded": folded,
    "fit_beta": {"form": "beta = pi/(a1*n + a2)", "a1": float(popt_b[0]), "a2": float(popt_b[1])},
    "fit_gamma": {"form": "gamma = b1*pi - b2*beta", "b1": float(popt_g[0]), "b2": float(popt_g[1])},
    "paper_prediction": {"p1_beta": "pi/(n+2)", "p1_gamma": "pi*(n+2)/(n+4) = pi - 2*beta"},
}
with open(os.path.join(EVID, "p1_analysis.json"), "w") as f:
    json.dump(out, f, indent=2)

# Concentration diagnostic re-done on folded values, and fit |Delta|^2 = C / n^l
delta_sq = []
for i in range(len(folded) - 1):
    n = folded[i]["n"]
    d2 = ((folded[i+1]["gamma_folded"] - folded[i]["gamma_folded"]) ** 2
          + (folded[i+1]["beta_folded"] - folded[i]["beta_folded"]) ** 2)
    delta_sq.append((n, d2))

print("\nRefined concentration (folded to canonical branch):")
print(f"{'n':>3} {'|Delta|^2':>12} {'1/n^4':>12} {'ratio':>10}")
for n, d2 in delta_sq:
    print(f"{n:>3d} {d2:>12.3e} {1.0 / n**4:>12.3e} {d2 / (1.0 / n**4):>10.3f}")

# Fit log|Delta|^2 = log C - l * log n
ns = np.array([x[0] for x in delta_sq])
ds = np.array([x[1] for x in delta_sq])
coeffs = np.polyfit(np.log(ns), np.log(ds), 1)
l_fit = -coeffs[0]
C_fit = math.exp(coeffs[1])
print(f"\nPower-law fit |Delta|^2 ~ C / n^l:  l = {l_fit:.3f}, C = {C_fit:.3f}")
print(f"  Paper claim: l = 4 (i.e. concentrations scale as O(1/n^4)).")

with open(os.path.join(EVID, "p1_concentration_fit.json"), "w") as f:
    json.dump({"delta_sq_folded": [{"n": int(n), "delta_sq": float(d)} for n, d in delta_sq],
               "power_law_exponent_l": float(l_fit),
               "power_law_prefactor_C": float(C_fit),
               "paper_claim_exponent": 4}, f, indent=2)

print("\nAll analysis saved.")
