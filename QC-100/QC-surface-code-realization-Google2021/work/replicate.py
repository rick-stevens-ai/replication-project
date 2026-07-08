#!/usr/bin/env python3
"""
Independent replication of the REPRODUCIBLE CORE of:
  Google Quantum AI (2022/2023), "Suppressing quantum errors by scaling a
  surface code logical qubit", arXiv:2207.06431, Nature 615, 676 (2023).

NB on paper identity: the wave task cited arXiv:2112.13505, but that ID is the
Zhao et al. Zuchongzhi-2.1 *distance-3-only* surface code paper. The scientific
core specified by the task (d=3 vs d=5, error-suppression factor Lambda, the
"d=5 does NOT strongly beat d=3, Lambda~1" honest finding) is uniquely the
Google 2207.06431 paper (Lambda_3/5 = 1.10). We replicate that paper's core.
The device/hardware portion is OUT OF SCOPE (cannot rerun Sycamore); we
replicate the DECODING + LOGICAL-ERROR-SCALING core with Stim + PyMatching.

Claims replicated (simulator core):
  C1  logical error per cycle (LEC) for d=3 and d=5 rotated surface codes under
      circuit-level depolarizing noise.
  C2  error-suppression factor Lambda_3/5 = eps_3 / eps_5.
  C3  the crossover: Lambda depends on p; there is a physical error rate near
      which d=5 barely beats d=3 (Lambda ~ 1.1, the paper's central finding),
      d=5 clearly wins below it, d=5 loses above it (Lambda<1). => a threshold.
  C4  the surface-code circuit-level threshold sits ~0.5-1% (paper's crossover
      regime "s=1.2 to 1.0"), and identify the p where Lambda matches paper 1.10.

Method: stim.Circuit.generated("surface_code:rotated_memory_z", ...) with
circuit-level depolarizing noise on all four channels, detector_error_model
with decompose_errors, pymatching MWPM decoder, Monte-Carlo shots.
Logical error per cycle eps derived from per-shot logical error P over R rounds
via the standard fidelity relation  1 - 2P = (1 - 2eps)^R.
"""
import sys, json, time, math
import numpy as np
import stim
import pymatching

def make_circuit(distance, rounds, p):
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=rounds,
        distance=distance,
        after_clifford_depolarization=p,
        before_measure_flip_probability=p,
        after_reset_flip_probability=p,
        before_round_data_depolarization=p,
    )

def logical_error_prob(distance, rounds, p, shots, seed=None):
    """Return per-shot logical error probability P and its 1-sigma stderr."""
    circ = make_circuit(distance, rounds, p)
    dem = circ.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circ.compile_detector_sampler(seed=seed)
    det, obs = sampler.sample(shots, separate_observables=True)
    pred = matcher.decode_batch(det)
    # single logical observable for memory experiment
    errors = np.sum(np.any(pred != obs, axis=1))
    P = errors / shots
    # binomial stderr
    se = math.sqrt(max(P * (1 - P), 1e-12) / shots)
    return P, se, errors

def per_cycle(P, rounds):
    """Convert per-shot logical error P over `rounds` cycles to per-cycle eps
    using 1-2P = (1-2eps)^R  =>  eps = (1 - (1-2P)^(1/R))/2."""
    P = min(P, 0.4999999)
    return (1.0 - (1.0 - 2.0 * P) ** (1.0 / rounds)) / 2.0

def run_c1(shots=200000, rounds=25, seed=12345):
    """LEC for d=3 and d=5 at a fixed p (near-device regime).
    Paper device sits in a crossover where Lambda~1.1; pick p to bracket it in C3.
    Here we report at a representative low-noise point p=0.001 and p=0.005."""
    out = {}
    for p in [0.001, 0.002, 0.003, 0.005]:
        row = {}
        for d in [3, 5]:
            P, se, ne = logical_error_prob(d, rounds, p, shots, seed=seed + d)
            eps = per_cycle(P, rounds)
            row[f"d{d}"] = {"P_per_shot": P, "P_se": se, "n_err": int(ne),
                            "eps_per_cycle": eps, "rounds": rounds, "shots": shots}
        row["Lambda_3_5"] = row["d3"]["eps_per_cycle"] / row["d5"]["eps_per_cycle"]
        out[f"p={p}"] = row
        print(f"[C1] p={p}: eps3={row['d3']['eps_per_cycle']:.4e} "
              f"eps5={row['d5']['eps_per_cycle']:.4e}  Lambda={row['Lambda_3_5']:.3f}")
    return out

def run_c34(shots=100000, rounds=25, seed=999):
    """Sweep p to map Lambda_3/5(p): find crossover (Lambda=1) & the point where
    Lambda matches paper's 1.10. Also sweep d=3,5,7 for threshold."""
    ps = [0.0005, 0.0008, 0.001, 0.0015, 0.002, 0.003, 0.004, 0.005,
          0.006, 0.008, 0.01, 0.012, 0.015, 0.02]
    sweep = []
    for p in ps:
        rec = {"p": p}
        for d in [3, 5, 7]:
            P, se, ne = logical_error_prob(d, rounds, p, shots, seed=seed + d + int(p * 1e5))
            eps = per_cycle(P, rounds)
            rec[f"d{d}"] = {"P": P, "se": se, "eps": eps, "n_err": int(ne)}
        rec["Lambda_3_5"] = rec["d3"]["eps"] / rec["d5"]["eps"]
        rec["Lambda_5_7"] = rec["d5"]["eps"] / rec["d7"]["eps"]
        sweep.append(rec)
        print(f"[C34] p={p:.4f}  eps3={rec['d3']['eps']:.3e} eps5={rec['d5']['eps']:.3e} "
              f"eps7={rec['d7']['eps']:.3e}  L35={rec['Lambda_3_5']:.3f} L57={rec['Lambda_5_7']:.3f}")
    return {"sweep": sweep, "ps": ps, "rounds": rounds, "shots": shots}

def find_lambda_match(sweep, target=1.10):
    """Interpolate p where Lambda_3/5 == target (paper's value)."""
    pts = [(r["p"], r["Lambda_3_5"]) for r in sweep]
    # Lambda increases as p decreases; find bracket
    for i in range(len(pts) - 1):
        (p1, l1), (p2, l2) = pts[i], pts[i + 1]
        if (l1 - target) * (l2 - target) <= 0:
            # linear interp in log-p
            if l2 == l1:
                return p1
            frac = (target - l1) / (l2 - l1)
            lp = math.log(p1) + frac * (math.log(p2) - math.log(p1))
            return math.exp(lp)
    return None

def find_crossover(sweep):
    """Interpolate p where Lambda_3/5 == 1 (d5 stops beating d3)."""
    return find_lambda_match(sweep, target=1.0)

def counts(d, rounds=25, p=0.005):
    c = make_circuit(d, rounds, p)
    return {"num_qubits": c.num_qubits, "num_detectors": c.num_detectors,
            "num_observables": c.num_observables, "num_measurements": c.num_measurements}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    shots = int(sys.argv[2]) if len(sys.argv) > 2 else None
    t0 = time.time()
    res = {"paper": "arXiv:2207.06431 Google 2023 (task cited 2112.13505 = Zuchongzhi d3-only; corrected)",
           "stim": stim.__version__, "pymatching": pymatching.__version__}

    # circuit sanity: qubit counts
    res["circuit_counts"] = {"d3": counts(3), "d5": counts(5), "d7": counts(7)}
    print("[counts] d3:", res["circuit_counts"]["d3"])
    print("[counts] d5:", res["circuit_counts"]["d5"])

    if which in ("all", "c1"):
        res["C1"] = run_c1(shots=shots or 200000)
    if which in ("all", "c34"):
        sw = run_c34(shots=shots or 100000)
        res["C34"] = sw
        res["crossover_p"] = find_crossover(sw["sweep"])
        res["p_at_Lambda_1.10"] = find_lambda_match(sw["sweep"], 1.10)
        print(f"[crossover] Lambda_3/5=1 at p={res['crossover_p']}")
        print(f"[match]     Lambda_3/5=1.10 (paper) at p={res['p_at_Lambda_1.10']}")

    res["wall_s"] = time.time() - t0
    out = f"results_{which}.json"
    json.dump(res, open(out, "w"), indent=2)
    print(f"[done] wrote {out} in {res['wall_s']:.1f}s")
