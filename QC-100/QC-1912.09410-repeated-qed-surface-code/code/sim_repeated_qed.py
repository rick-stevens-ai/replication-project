#!/usr/bin/env python3
"""
Independent replication of arXiv:1912.09410
"Repeated Quantum Error Detection in a Surface Code" (Andersen et al., ETH Zurich, 2019)

Reproducible core (classical simulation, no hardware required):
- d=2 rotated surface code = 4 data qubits + 3 ancilla qubits (paper Fig 1)
- Stabilizers (paper Eq 1):
    X_D1 X_D2 X_D3 X_D4  (weight-4 X, ancilla A2)
    Z_D1 Z_D3             (weight-2 Z, ancilla A1)
    Z_D2 Z_D4             (weight-2 Z, ancilla A3)
- Repeated syndrome extraction under depolarizing noise
- Two observables the paper reports we can independently reproduce:
   (1) Success probability p_s(N) = Pr(no detector fires in ANY of N cycles)
       Paper Fig 5(c): p_s(10) ~ few * 10^-4  (they report ~10^-4 "around a factor of 6
       smaller than simulations", so their sim value is ~6e-4)
   (2) Detector-event rate per round (should be ~constant with round for a well-behaved
       error-detection experiment; this is the "central claim" that repeated detection works)
   (3) Logical-error rate (post-selected on no detections + code-space check) vs rounds
       Paper Fig 5(a): logical Z_L error accumulated ~2.6% over ~10 cycles
       Paper Fig 5(b): logical X_L error accumulated ~3.1% over ~10 cycles

We build the Stim circuit ourselves (not use the built-in surface_code helper) because
the paper's d=2 rotated code is not one of Stim's canned generators, and we want the
stabilizers to exactly match Eq 1.

Noise model: single-parameter depolarizing p on each gate + measurement flip probability p.
We sweep p and compute observables. This is standard for surface-code sim.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import stim
import pymatching


def build_circuit(rounds: int, p: float, basis: str = "Z") -> stim.Circuit:
    """
    Build repeated-syndrome-extraction circuit for the d=2 rotated surface code.

    Qubit layout (indices):
        D1=0, D2=1, D3=2, D4=3       (data)
        A1=4, A2=5, A3=6             (ancillas)

    Stabilizers:
        A1 measures Z_D1 Z_D3
        A2 measures X_D1 X_D2 X_D3 X_D4
        A3 measures Z_D2 Z_D4

    Basis="Z": prepare |0>_L (all data in |0>), measure Z_L = Z_D1 Z_D2 at the end
    Basis="X": prepare |+>_L (all data in |+>),  measure X_L = X_D1 X_D3

    We inject a single depolarizing channel `p` on all gate operations and use
    `p` as measurement flip prob. This is a minimal-but-honest noise model
    used ubiquitously in Stim surface-code studies.

    Detectors: we compare each round's ancilla measurement to the previous round's
    (or to the deterministic initialization value in the first round).
    """
    D1, D2, D3, D4, A1, A2, A3 = 0, 1, 2, 3, 4, 5, 6
    data = [D1, D2, D3, D4]
    anc  = [A1, A2, A3]

    circ = stim.Circuit()

    # --- Initialization ---
    circ.append("R", data + anc)
    if basis == "X":
        circ.append("H", data)  # prep |+>_L via all-plus (stabilizer of |+>_L up to code)

    # A useful helper for one round of syndrome extraction
    def one_round(circ: stim.Circuit, first_round: bool, prev_rec_offsets):
        # Reset ancillas at start of round
        circ.append("R", anc)
        circ.append("X_ERROR", anc, p)  # reset error

        # Hadamard the X-stab ancilla so its CNOTs act like CZs from data POV
        circ.append("H", [A2])
        circ.append("DEPOLARIZE1", [A2], p)

        # Idle noise on data qubits (rough model)
        circ.append("DEPOLARIZE1", data, p)

        # Stabilizer entangling gates.  We do them in 4 time steps.
        # Step 1: A1<-D1 (Z-stab CNOT), A3<-D2 (Z-stab CNOT), A2->D1 (X-stab CNOT ctrl=A2)
        pairs1 = [(D1, A1), (D2, A3), (A2, D1)]
        for c, t in pairs1:
            circ.append("CX", [c, t])
            circ.append("DEPOLARIZE2", [c, t], p)

        # Step 2: A1<-D3, A3<-D4, A2->D2
        pairs2 = [(D3, A1), (D4, A3), (A2, D2)]
        for c, t in pairs2:
            circ.append("CX", [c, t])
            circ.append("DEPOLARIZE2", [c, t], p)

        # Step 3: A2->D3
        pairs3 = [(A2, D3)]
        for c, t in pairs3:
            circ.append("CX", [c, t])
            circ.append("DEPOLARIZE2", [c, t], p)

        # Step 4: A2->D4
        pairs4 = [(A2, D4)]
        for c, t in pairs4:
            circ.append("CX", [c, t])
            circ.append("DEPOLARIZE2", [c, t], p)

        # Undo Hadamard on A2
        circ.append("H", [A2])
        circ.append("DEPOLARIZE1", [A2], p)

        # Measurement of ancillas
        circ.append("X_ERROR", anc, p)  # measurement flip
        circ.append("M", anc)  # measures A1, A2, A3 -> record indices new_rec-3..new_rec-1

        # Detectors: compare each ancilla to previous-round or to init value
        if first_round:
            # First round: for |0>_L init, Z-stabilizer outcomes should be 0
            # (deterministic).  X-stab is NOT deterministic on |0>_L => no detector.
            # For |+>_L init, X-stab outcome is 0 (deterministic); Z-stabs are random.
            if basis == "Z":
                circ.append("DETECTOR", [stim.target_rec(-3)])  # A1 (Z_D1 Z_D3) -> 0
                circ.append("DETECTOR", [stim.target_rec(-1)])  # A3 (Z_D2 Z_D4) -> 0
            else:
                circ.append("DETECTOR", [stim.target_rec(-2)])  # A2 (X_D1..X_D4) -> 0
        else:
            # Compare each ancilla to itself one round back (3 records back)
            circ.append("DETECTOR", [stim.target_rec(-3), stim.target_rec(-6)])  # A1
            circ.append("DETECTOR", [stim.target_rec(-2), stim.target_rec(-5)])  # A2
            circ.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-4)])  # A3
        return

    # First round
    one_round(circ, first_round=True, prev_rec_offsets=None)
    # Remaining rounds
    for _ in range(rounds - 1):
        one_round(circ, first_round=False, prev_rec_offsets=None)

    # --- Final data-qubit measurement in the initialization basis ---
    if basis == "X":
        circ.append("H", data)
        circ.append("DEPOLARIZE1", data, p)
    circ.append("X_ERROR", data, p)
    circ.append("M", data)  # D1, D2, D3, D4

    # A final "detector" reconstructing the stabilizers from the destructive measurement,
    # comparing against the last round's ancilla outcomes.  This is what closes the space-time
    # matching graph so pymatching can decode.
    # After the final measurement, records are (in reverse): -1=D4, -2=D3, -3=D2, -4=D1,
    # and the last ancilla round is -5=A3, -6=A2, -7=A1.
    if basis == "Z":
        # Stab A1 = Z_D1 Z_D3 -> parity(D1, D3) XOR previous A1
        circ.append("DETECTOR", [stim.target_rec(-4), stim.target_rec(-2), stim.target_rec(-7)])
        # Stab A3 = Z_D2 Z_D4 -> parity(D2, D4) XOR previous A3
        circ.append("DETECTOR", [stim.target_rec(-3), stim.target_rec(-1), stim.target_rec(-5)])
        # Logical Z_L = Z_D1 Z_D2 (paper's choice)
        circ.append("OBSERVABLE_INCLUDE", [stim.target_rec(-4), stim.target_rec(-3)], 0)
    else:
        # After H+meas we're effectively measuring X on data qubits.
        # Stab A2 = X_D1 X_D2 X_D3 X_D4 -> parity of all four XOR previous A2
        circ.append("DETECTOR",
                    [stim.target_rec(-4), stim.target_rec(-3), stim.target_rec(-2), stim.target_rec(-1),
                     stim.target_rec(-6)])
        # Logical X_L = X_D1 X_D3
        circ.append("OBSERVABLE_INCLUDE", [stim.target_rec(-4), stim.target_rec(-2)], 0)

    return circ


def run_experiment(rounds_list, p_list, shots=20000, basis="Z", seed=1):
    """Simulate and compute observables for each (rounds, p) pair."""
    results = []
    rng = np.random.default_rng(seed)
    for p in p_list:
        for R in rounds_list:
            circ = build_circuit(R, p, basis=basis)
            sampler = circ.compile_detector_sampler(seed=int(rng.integers(1 << 31)))
            det, obs = sampler.sample(shots=shots, separate_observables=True)
            # det shape: (shots, num_detectors); obs shape: (shots, 1)
            n_det = det.shape[1]

            # (a) success probability: no detector fired in ANY of the rounds
            #     (i.e. all detectors == 0).
            success_mask = ~det.any(axis=1)
            p_success = success_mask.mean()

            # (b) mean detector rate per round: fraction of detectors that fired,
            #     ignoring the special "boundary" detectors.  For our detector count:
            #       first round: 2 detectors (basis=Z) or 1 (basis=X)
            #       subsequent rounds: 3 detectors each
            #       final: 2 (Z) or 1 (X)
            #     We approximate "per-round detector rate" as total fires / total detectors.
            det_rate = det.mean()

            # (c) logical error rate WITHOUT postselection, decoded with pymatching
            dem = circ.detector_error_model(decompose_errors=False)
            try:
                matcher = pymatching.Matching.from_detector_error_model(dem)
                predictions = matcher.decode_batch(det)
                logical_err_decoded = (predictions.reshape(-1) != obs.reshape(-1)).mean()
            except Exception as e:
                logical_err_decoded = float("nan")

            # (d) logical error rate WITH postselection (paper's mode): only keep shots
            #     that had zero detectors AND whose observable is well-defined; the
            #     "logical error" is the fraction of these post-selected shots that have
            #     obs=1 (i.e. the encoded state came out with wrong parity even though
            #     no error was flagged).
            ps_shots = success_mask.sum()
            if ps_shots > 0:
                logical_err_postsel = obs[success_mask].mean()
            else:
                logical_err_postsel = float("nan")

            results.append(dict(
                basis=basis,
                p=p,
                rounds=R,
                shots=shots,
                num_detectors=n_det,
                p_success=float(p_success),
                mean_detector_rate=float(det_rate),
                logical_err_decoded=float(logical_err_decoded),
                logical_err_postsel=float(logical_err_postsel),
                postsel_shots=int(ps_shots),
            ))
            print(f"  basis={basis} p={p:.4f} R={R:2d}  "
                  f"p_success={p_success:.4g}  det_rate={det_rate:.4g}  "
                  f"logical_dec={logical_err_decoded:.4g}  "
                  f"logical_postsel={logical_err_postsel:.4g}  (ps_shots={ps_shots})",
                  flush=True)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="report/evidence/results.json")
    ap.add_argument("--shots", type=int, default=20000)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # Scan of physical error rates (log-spaced, similar to standard Stim demos)
    p_list = [0.0005, 0.001, 0.002, 0.005, 0.01]
    # Rounds up to 10 to match paper's Fig 5(c) N=10
    rounds_list = [1, 2, 4, 6, 8, 10]

    t0 = time.time()
    all_results = []
    print(f"# Stim {stim.__version__}  PyMatching {pymatching.__version__}  NumPy {np.__version__}")
    print(f"# Shots per point: {args.shots}")
    print(f"# p_list: {p_list}")
    print(f"# rounds_list: {rounds_list}")
    for basis in ("Z", "X"):
        print(f"\n=== basis = {basis} (prep |{'0' if basis=='Z' else '+'}>_L, measure {basis}_L) ===")
        rs = run_experiment(rounds_list, p_list, shots=args.shots, basis=basis, seed=42)
        all_results.extend(rs)

    elapsed = time.time() - t0
    print(f"\n# elapsed: {elapsed:.1f} s")

    with open(args.out, "w") as f:
        json.dump(dict(
            stim_version=stim.__version__,
            pymatching_version=pymatching.__version__,
            numpy_version=np.__version__,
            shots=args.shots,
            p_list=p_list,
            rounds_list=rounds_list,
            elapsed_seconds=elapsed,
            results=all_results,
        ), f, indent=2)
    print(f"# wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
