#!/usr/bin/env python3
"""Phase sweep: does the bounded-sample alpha_zz track the k-space Chern-Simons
alpha across phi? That mutual agreement IS the paper's headline claim."""
import json, time, numpy as np
import malashevich2010_omp as M

t0 = time.time()
phis = [0.0, 0.4, 0.8, 1.2, 1.6] # * pi
rows = []
for f in phis:
    phi = f * np.pi
    _, ab = M.alpha_zz_bounded(phi, Ls=(4, 5))
    th = M.theta_CS(phi, N=8)
    aiso = th / (2*np.pi*2*np.pi)
    rows.append({"phi_over_pi": f, "alpha_zz_bounded": ab,
                 "theta_CS": th, "alpha_iso_CS": aiso})
    print(f"phi={f:.1f}pi  alpha_zz(bounded)={ab:+.5f}  theta_CS={th:+.5f}  alpha_iso^CS={aiso:+.6f}")

ab = np.array([r["alpha_zz_bounded"] for r in rows])
ac = np.array([r["alpha_iso_CS"] for r in rows])
# correlation of the two methods across the sweep
if np.std(ab) > 1e-9 and np.std(ac) > 1e-9:
    corr = float(np.corrcoef(ab, ac)[0, 1])
else:
    corr = None
out = {"sweep": rows, "method_correlation": corr,
       "alpha_bounded_range": [float(ab.min()), float(ab.max())],
       "alpha_CS_range": [float(ac.min()), float(ac.max())],
       "runtime_sec": round(time.time()-t0, 1)}
with open("malashevich2010_sweep.json", "w") as fh:
    json.dump(out, fh, indent=2)
print("corr(bounded,CS) =", corr, " runtime", out["runtime_sec"], "s")
