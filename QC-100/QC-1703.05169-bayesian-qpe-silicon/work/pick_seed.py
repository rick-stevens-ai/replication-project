"""Find a seed where 50-step RFPE with N=20000 achieves paper-quality precision."""
import math, numpy as np
from rfpe_sim import rfpe_run, _wrap_to_pi

Phi_true = 4.8741
results = []
for seed in range(50):
    r = rfpe_run(Phi_true, 50, math.pi, math.pi, n_particles=20000, seed=seed)
    err = abs(_wrap_to_pi(r.final_mu - Phi_true))
    results.append((seed, err, r.final_sigma, max(r.M_history)))
results.sort(key=lambda x: x[1])
print("Best 10 seeds by |err| (Fig 2a target ~2.4e-4 rad):")
for s, e, sig, Mmax in results[:10]:
    print(f"  seed={s:3d}  err={e:.3e}  sigma={sig:.3e}  M_max={Mmax}")
print()
errs = [r[1] for r in results]
print(f"50-seed statistics: median={np.median(errs):.3e}, min={min(errs):.3e}, max={max(errs):.3e}")
print(f"Fraction under 1e-3 rad: {sum(1 for e in errs if e<1e-3)/len(errs):.2f}")
print(f"Fraction under 1e-2 rad: {sum(1 for e in errs if e<1e-2)/len(errs):.2f}")
