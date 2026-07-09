"""
Spot-check reproduction of the central mechanism in
Erdem et al., "Surrogate-driven design optimization with uncertainty constraints
in Monte Carlo simulations," Energy and AI 22 (2025) 100655.

The paper trains FNN surrogates on grid-searched MCNP tally outputs at five
different tally-uncertainty levels, then runs NSGA-III on each surrogate and
computes normalized hypervolume of the recovered Pareto front vs the lowest-
uncertainty (ground-truth) dataset. Central finding:

  - Neutron moderator: normalized hypervolume drops MONOTONICALLY from 0.886
    at 1.0% uncertainty to 0.748 at 10% uncertainty (~15.6% relative loss).
  - Ion-to-neutron converter: normalized hypervolume stays ~0.50 across all
    uncertainty levels (essentially noise-insensitive; ~1-5% loss).

Full MCNP + FNN + real geometries is out of scope for a fast spot-check, but
the *mechanism* the paper is really claiming is generic: surrogate-based MOO
degrades when training data has additive noise, at a problem-dependent rate.

This spot-check reproduces that mechanism on a **controlled synthetic analog**
built from two well-known multi-objective test problems:

  Problem A (mimics the moderator): a modified ZDT1-like 2D->2D bi-objective
  test with SHARP curvature -- expected to be noise-SENSITIVE.
  Problem B (mimics the converter): a smoother, degenerate-shape bi-objective
  test with weak curvature -- expected to be noise-INSENSITIVE.

For each problem and each of 5 noise levels sigma in {0.005, 0.02, 0.05, 0.075, 0.10}
(matching the paper's 1%, 3%, 5%, 7.5%, 10% moderator levels), we:
  1. Sample a grid, evaluate the true objectives, add Gaussian noise.
  2. Train an sklearn MLPRegressor as the FNN surrogate.
  3. Run NSGA-III on the surrogate.
  4. Evaluate the surrogate's Pareto candidates on the TRUE objectives.
  5. Compute normalized hypervolume vs the lowest-noise ground-truth Pareto.

If the paper's mechanism is real and general, we expect Problem A's normalized
hypervolume to drop monotonically with noise while Problem B's stays roughly flat.
"""

import json
import time
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.indicators.hv import HV

RNG = np.random.default_rng(20260703)

# ---------------- True test problems ----------------
# Problem A: ZDT1-like, sharp Pareto (mimics moderator: sensitive to noise)
# f1 = x1;  f2 = g * (1 - sqrt(x1/g));  g = 1 + 9 * x2   with x1,x2 in [0,1]
# Both to be MINIMIZED.
def true_A(X):
    x1 = X[..., 0]; x2 = X[..., 1]
    g = 1.0 + 9.0 * x2
    f1 = x1
    f2 = g * (1.0 - np.sqrt(np.clip(x1 / g, 0, None)))
    return np.stack([f1, f2], axis=-1)

# Problem B: smoother, weakly-curved bi-objective (mimics converter: less sensitive)
# f1 = 0.5*(x1 + x2);  f2 = 0.5*((1-x1) + x2)  -- essentially linear-ish, both min
def true_B(X):
    x1 = X[..., 0]; x2 = X[..., 1]
    f1 = 0.5 * (x1 + x2)
    f2 = 0.5 * ((1.0 - x1) + x2)
    return np.stack([f1, f2], axis=-1)

# ---------------- Grid dataset ----------------
# Small-ish grid on purpose: the paper's moderator dataset is 30x25 = 750
# points per uncertainty level (Table 1).  We use 20x20 = 400.
def grid_data(problem_fn, n_per_dim=20):
    xs = np.linspace(0, 1, n_per_dim)
    X = np.array([[a, b] for a in xs for b in xs])
    Y = problem_fn(X)
    return X, Y

# ---------------- Add Gaussian noise scaled to per-objective RANGE ----------------
# The paper's "1%..10% tally uncertainty" is per-simulation relative sigma on
# the raw tally value.  We approximate that here as multiplicative noise on
# each objective (Y * (1 + eps), eps ~ N(0, sigma_frac)) with an additive floor
# tied to the objective range so near-zero values still get noise.
def add_noise(Y, sigma_frac, rng):
    ranges = (Y.max(axis=0, keepdims=True) - Y.min(axis=0, keepdims=True))
    mult = 1.0 + rng.normal(0.0, sigma_frac, size=Y.shape)
    add = rng.normal(0.0, 0.25 * sigma_frac * ranges, size=Y.shape)
    return Y * mult + add

# ---------------- Train surrogate ----------------
def train_surrogate(X, Y_noisy):
    xs = StandardScaler().fit(X)
    ys = StandardScaler().fit(Y_noisy)
    Xn = xs.transform(X)
    Yn = ys.transform(Y_noisy)
    m = MLPRegressor(
        hidden_layer_sizes=(64, 64),
        activation="relu",
        solver="adam",
        learning_rate_init=1e-3,
        max_iter=2000,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=20,
        random_state=42,
    )
    m.fit(Xn, Yn)
    def predict(Xnew):
        return ys.inverse_transform(m.predict(xs.transform(Xnew)))
    return predict, m

# ---------------- Pymoo problem wrapping surrogate ----------------
class SurrProblem(ElementwiseProblem):
    def __init__(self, predict_fn):
        super().__init__(n_var=2, n_obj=2, xl=np.zeros(2), xu=np.ones(2))
        self.predict_fn = predict_fn
    def _evaluate(self, x, out, *args, **kwargs):
        y = self.predict_fn(x.reshape(1, -1))[0]
        out["F"] = y

def run_nsga3(predict_fn, seed=0):
    prob = SurrProblem(predict_fn)
    ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=12)
    algo = NSGA3(pop_size=60, ref_dirs=ref_dirs)
    res = minimize(prob, algo, ("n_gen", 40), seed=seed, verbose=False)
    return res.X, res.F

# ---------------- Evaluate candidates on TRUE fn, compute HV ----------------
def normalized_hv(true_F_candidates, ref):
    # Keep non-dominated set among the true-evaluated candidates
    F = true_F_candidates
    n = F.shape[0]
    dominated = np.zeros(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            if np.all(F[j] <= F[i]) and np.any(F[j] < F[i]):
                dominated[i] = True; break
    nd = F[~dominated]
    hv_ind = HV(ref_point=ref)
    return hv_ind(nd), nd

# ---------------- Experiment ----------------
NOISE_LEVELS = [0.010, 0.030, 0.050, 0.075, 0.100]  # paper's moderator set

def run_experiment(name, true_fn):
    print(f"\n=== Problem {name} ===")
    X_grid, Y_true = grid_data(true_fn, n_per_dim=20)
    # Reference point (nadir + margin) computed on the TRUE objective values,
    # matching the paper's protocol (worst observed value in the dataset).
    ref = Y_true.max(axis=0) + 0.1 * (Y_true.max(axis=0) - Y_true.min(axis=0))
    # Ground-truth Pareto (analytic): dense sample on true fn, take nd set,
    # compute HV to serve as the DENOMINATOR for normalized HV.
    Xd = np.array([[a, b] for a in np.linspace(0, 1, 60) for b in np.linspace(0, 1, 60)])
    Yd = true_fn(Xd)
    hv_ind = HV(ref_point=ref)
    # non-dominated set of true fn
    n = Yd.shape[0]; dom = np.zeros(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            if np.all(Yd[j] <= Yd[i]) and np.any(Yd[j] < Yd[i]):
                dom[i] = True; break
    Yd_nd = Yd[~dom]
    hv_gt = hv_ind(Yd_nd)
    print(f"  ground-truth HV = {hv_gt:.4f}, |true-nd|={len(Yd_nd)}, ref={ref}")
    results = []
    for sig in NOISE_LEVELS:
        t0 = time.time()
        Y_noisy = add_noise(Y_true, sig, RNG)
        predict, model = train_surrogate(X_grid, Y_noisy)
        Xc, Fs = run_nsga3(predict, seed=int(sig * 10000))
        # Score in the SURROGATE's predicted objective space (what the paper
        # reports as the surrogate-recovered Pareto front, Fig. 15 / Table 6-7).
        hv_pred, nd_pred = normalized_hv(Fs, ref)
        norm_hv_pred = hv_pred / hv_gt if hv_gt > 0 else float("nan")
        # Also score on TRUE fn evaluated at surrogate's chosen X (validation).
        Ft = true_fn(Xc)
        hv_true, nd_true = normalized_hv(Ft, ref)
        norm_hv_true = hv_true / hv_gt if hv_gt > 0 else float("nan")
        # R2 of surrogate on the noisy training data
        Yp = predict(X_grid)
        ss_res = ((Y_noisy - Yp) ** 2).sum()
        ss_tot = ((Y_noisy - Y_noisy.mean(axis=0)) ** 2).sum()
        r2 = 1 - ss_res / ss_tot
        # R2 of surrogate vs the TRUE (noise-free) function on the grid
        ss_res_t = ((Y_true - Yp) ** 2).sum()
        ss_tot_t = ((Y_true - Y_true.mean(axis=0)) ** 2).sum()
        r2_true = 1 - ss_res_t / ss_tot_t
        dt = time.time() - t0
        print(f"  sigma={sig*100:5.2f}%  hv_pred={hv_pred:.4f} (norm={norm_hv_pred:.4f})  hv_true={hv_true:.4f} (norm={norm_hv_true:.4f})  R2_noisy={r2:.4f}  R2_true={r2_true:.4f}  ({dt:.1f}s)")
        results.append({
            "sigma_pct": sig * 100,
            "hv_predicted_space": float(hv_pred),
            "hv_predicted_normalized": float(norm_hv_pred),
            "hv_true_validation": float(hv_true),
            "hv_true_normalized": float(norm_hv_true),
            "r2_vs_noisy_train": float(r2),
            "r2_vs_true_fn": float(r2_true),
            "n_nondominated_pred": int(len(nd_pred)),
            "n_nondominated_true": int(len(nd_true)),
            "n_iter_mlp": int(model.n_iter_),
        })
    # Relative loss vs cleanest (lowest-sigma) case, in the PREDICTED space
    hv0 = results[0]["hv_predicted_normalized"]
    for r in results:
        r["relative_hv_loss_pct"] = float(100.0 * (hv0 - r["hv_predicted_normalized"]) / hv0)
    return {"problem": name, "hv_ground_truth": float(hv_gt),
            "ref_point": ref.tolist(), "results": results}

if __name__ == "__main__":
    out = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed": 20260703,
        "noise_levels_pct": [x * 100 for x in NOISE_LEVELS],
        "problems": [
            run_experiment("A_sharp_moderator_analog", true_A),
            run_experiment("B_smooth_converter_analog", true_B),
        ],
    }
    with open("results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nWROTE results.json")
