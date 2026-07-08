"""L=10 sanity: does dt_adapt / dt_bound grow with L, trending toward paper's ~10 at L=18?"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trotter24 import build_H, init_state_minus_y, pick_adaptive_dt, dt_bound

L = 10
print(f"L={L}")
t0 = time.time()
A, B, H = build_H(L)
psi = init_state_minus_y(L)
print(f"  build H done in {time.time()-t0:.1f}s")

epss = [1e-3, 10**(-1.5), 1e-2]
rows = []
for eps in epss:
    t1 = time.time()
    dt_star, eta_est, eta_true, hist = pick_adaptive_dt(A, B, H, psi, eps, dt0=0.4, C=0.95)
    dt_b, denom = dt_bound(A, B, eps)
    ratio = dt_star / dt_b
    row = {"L": L, "eps": float(eps), "dt_adapt": float(dt_star),
           "dt_bound": float(dt_b), "ratio": float(ratio),
           "eta_true_at_dt_adapt": float(eta_true),
           "meets_tolerance": bool(eta_true <= eps),
           "seconds": time.time()-t1}
    rows.append(row)
    print(f"  eps={eps:.3e}  dt_adapt={dt_star:.4f}  dt_bound={dt_b:.4f}  "
          f"ratio={ratio:.2f}  eta_true={eta_true:.3e}  meets={row['meets_tolerance']}  "
          f"({row['seconds']:.1f}s)")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trotter24_L10.json"), "w") as f:
    json.dump(rows, f, indent=2)
print("saved trotter24_L10.json")
