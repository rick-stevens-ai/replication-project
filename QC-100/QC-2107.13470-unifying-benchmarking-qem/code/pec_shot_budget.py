"""PEC as a function of sample budget — quick check that PEC's poor showing
in the 300-sample setting is a shot-budget artefact (paper's explicit finding:
more powerful methods need larger budgets)."""

import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from replicate_qem import (
    build_circuit, exact_expval_Z0, executor_noisy, P2, EVID_DIR, RNG_SEED,
)
from mitiq import pec
from mitiq.pec.representations.depolarizing import (
    represent_operations_in_circuit_with_local_depolarizing_noise,
)
from mitiq.interface.conversions import convert_to_mitiq

qc = build_circuit(seed=2)
exact = exact_expval_Z0(qc)
mitiq_circ, _ = convert_to_mitiq(qc)
reps = represent_operations_in_circuit_with_local_depolarizing_noise(
    mitiq_circ, noise_level=P2)

raw = executor_noisy(qc)
print(f"[reference] exact={exact:+.4f} raw_err={abs(raw-exact):.4f}")

results = []
for n in [100, 300, 1000, 3000]:
    t0 = time.time()
    pv = pec.execute_with_pec(mitiq_circ, executor_noisy,
                               representations=reps,
                               num_samples=n, random_state=RNG_SEED)
    v = float(pv[0] if isinstance(pv, tuple) else pv)
    err = abs(v - exact)
    dt = time.time() - t0
    print(f"[PEC n={n:>4}] val={v:+.4f} |err|={err:.4f}  ({dt:.1f}s)")
    results.append({"num_samples": n, "value": v, "abs_error": err, "seconds": dt})

out = EVID_DIR / "pec_shot_budget.json"
out.write_text(json.dumps({
    "exact": exact, "raw": raw, "raw_abs_error": abs(raw-exact),
    "results": results,
}, indent=2))
print(f"[write] {out}")
