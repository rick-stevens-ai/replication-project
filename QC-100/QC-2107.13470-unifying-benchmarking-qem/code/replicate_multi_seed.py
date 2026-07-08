"""
Robustness pass: run the same replication over multiple random-circuit seeds
so we can report mean absolute error across an ensemble, matching the paper's
methodology (they average over 30 RQC instances; we use fewer since our
instances are much smaller and this is a laptop replication).
"""

import json, time, sys, random
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))

from replicate_qem import (
    build_circuit, exact_expval_Z0, executor_noisy, executor_ideal,
    NQ, DEPTH, P1, P2, SHOTS, RNG_SEED, EVID_DIR,
)
from mitiq import zne, cdr, pec, Executor
from mitiq.zne.scaling.folding import fold_gates_at_random
from mitiq.zne.inference import RichardsonFactory
from mitiq.pec.representations.depolarizing import (
    represent_operations_in_circuit_with_local_depolarizing_noise,
)
from mitiq.interface.conversions import convert_to_mitiq

SEEDS = [1, 2, 3, 5, 7]  # 5 different RQC instances (skip 0 which has ~0 exact)
per_seed = []

t0 = time.time()
exec_noisy = Executor(executor_noisy, max_batch_size=1)

for seed in SEEDS:
    qc = build_circuit(seed=seed)
    exact = exact_expval_Z0(qc)
    if abs(exact) < 0.05:
        print(f"[skip seed={seed}] |exact|={abs(exact):.3f} too small (near null case)")
        continue

    raw = executor_noisy(qc)

    # ZNE
    fac = RichardsonFactory(scale_factors=[1.0, 2.0, 3.0])
    zne_val = float(zne.execute_with_zne(qc, exec_noisy, factory=fac,
                                          scale_noise=fold_gates_at_random))

    # PEC
    mitiq_circ, _ = convert_to_mitiq(qc)
    reps = represent_operations_in_circuit_with_local_depolarizing_noise(
        mitiq_circ, noise_level=P2)
    pv = pec.execute_with_pec(mitiq_circ, executor_noisy,
                              representations=reps,
                              num_samples=300, random_state=RNG_SEED + seed)
    pec_val = float(pv[0] if isinstance(pv, tuple) else pv)

    # CDR
    cdr_val = float(cdr.execute_with_cdr(
        qc, exec_noisy, simulator=executor_ideal,
        num_training_circuits=10, fraction_non_clifford=0.3,
        random_state=RNG_SEED + seed))

    row = {
        "seed": seed,
        "exact": exact,
        "raw": raw,
        "zne": zne_val,
        "pec": pec_val,
        "cdr": cdr_val,
        "err_raw": abs(raw - exact),
        "err_zne": abs(zne_val - exact),
        "err_pec": abs(pec_val - exact),
        "err_cdr": abs(cdr_val - exact),
    }
    per_seed.append(row)
    print(f"[seed={seed}] exact={exact:+.4f} raw|err|={row['err_raw']:.4f} "
          f"zne|err|={row['err_zne']:.4f} pec|err|={row['err_pec']:.4f} "
          f"cdr|err|={row['err_cdr']:.4f}")

# Aggregate
errs = {k: [r[f"err_{k}"] for r in per_seed] for k in ("raw","zne","pec","cdr")}
mean_err = {k: float(np.mean(v)) for k, v in errs.items()}
max_err  = {k: float(np.max(v))  for k, v in errs.items()}

print("\n=== ENSEMBLE MEAN |error| across", len(per_seed), "instances ===")
for k in ("raw","zne","pec","cdr"):
    tag = "" if k == "raw" else (" (beats raw)" if mean_err[k] < mean_err["raw"] else " (worse than raw)")
    print(f"  {k:>3}: mean={mean_err[k]:.4f}  max={max_err[k]:.4f}{tag}")

n_beats = sum(1 for k in ("zne","pec","cdr") if mean_err[k] < mean_err["raw"])
print(f"\n[VERDICT] {n_beats}/3 methods have mean-error better than raw noisy")

out = {
    "paper": "arXiv:2107.13470",
    "n_instances": len(per_seed),
    "seeds_used": [r["seed"] for r in per_seed],
    "shots_per_execution": SHOTS,
    "noise_model": {"p1": P1, "p2": P2},
    "per_instance": per_seed,
    "mean_error": mean_err,
    "max_error": max_err,
    "methods_beating_raw_on_mean": {
        k: mean_err[k] < mean_err["raw"] for k in ("zne","pec","cdr")
    },
    "n_methods_beating_raw_on_mean": n_beats,
    "elapsed_seconds": time.time() - t0,
}
outfile = EVID_DIR / "replication_results_multi_seed.json"
outfile.write_text(json.dumps(out, indent=2))
print(f"[write] {outfile}")
