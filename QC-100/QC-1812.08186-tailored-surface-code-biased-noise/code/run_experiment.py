#!/usr/bin/env python3
"""
Independent replication of Tuckett, Bartlett, Flammia et al.,
"Tailoring surface codes for highly biased noise" (arXiv:1812.08186).

Central claim tested:
  Under Z-biased noise (Z errors much more likely than X/Y), the surface code
  achieves better error suppression than under symmetric depolarizing noise.
  With MWPM decoding (suboptimal vs. paper's tensor-network decoder), we expect:
    - Standard depolarizing threshold ~10.9% (paper cites for MWPM regime)
    - Improved threshold / lower logical error rate under Z-biased noise

We use Stim's built-in rotated surface code memory experiment with a custom
biased Pauli noise channel injected as per-qubit error operators, and PyMatching
for decoding. We compare logical error rate (per shot) vs physical error rate p
for distances d=3, 5, 7 under bias eta in {0.5 (depolarizing), 10, 100, 1000}.

The crossing point of curves for different d is the empirical threshold.

Design notes:
- We use rotated surface code memory experiment (Z basis) with r rounds = d.
- For biased noise, we replace uniform depolarizing errors on data qubits with
  a Pauli channel where P(X)=P(Y)=p/(2*(eta+1)), P(Z)=p*eta/(eta+1).
  (Consistent with paper's Z-biased definition; the paper uses Y-biased equivalent
   via a code modification. Because standard PyMatching decodes X and Z separately,
   this cleanly demonstrates the bias-advantage claim.)
- Measurement / reset errors set to same p for simplicity.
"""

import argparse, json, math, os, sys, time
from pathlib import Path

import numpy as np
import stim
import pymatching


def build_biased_surface_code_circuit(d: int, rounds: int, p: float, eta: float, basis: str = "Z"):
    """
    Build a rotated surface code memory experiment with biased single-qubit
    Pauli noise on data qubits after each round.

    Uses Stim's canonical rotated_memory_z / rotated_memory_x generator, then
    rebuilds error model with biased Pauli channel.

    We construct via stim.Circuit.generated then overwrite noise using
    NOISY_CIRCUIT_TRANSFORMATIONS is not straightforward; instead we build a
    clean circuit and then insert PAULI_CHANNEL_1 errors on data qubits.
    """
    # Simplest: generate the circuit with p=0 (noise-free), then insert biased
    # PAULI_CHANNEL_1 operations manually before each stabilizer round.
    #
    # Even simpler and rigorous: use Stim's generator with after_reset_flip_probability=p,
    # before_measure_flip_probability=p (these are X flips) plus a
    # before_round_data_depolarization=p converted post-hoc? No — Stim only supports
    # symmetric depolarizing there.
    #
    # We'll build the circuit ourselves programmatically at low level:
    # generate the noiseless template, then walk through and replace/insert noise.
    template = stim.Circuit.generated(
        f"surface_code:rotated_memory_{basis.lower()}",
        distance=d,
        rounds=rounds,
        after_clifford_depolarization=0.0,
        after_reset_flip_probability=0.0,
        before_measure_flip_probability=0.0,
        before_round_data_depolarization=0.0,
    )

    # Identify data qubits by parsing the template's TICK structure.
    # In Stim's rotated surface code circuit, data qubits are those measured at the
    # very end via M/MR on the whole set; but simplest: find all qubit indices
    # that appear in the initial R (reset) block and are used as targets in the
    # final measurement layer M without any intervening MR (ancilla) pattern.
    #
    # Robust shortcut: for rotated surface code distance d, number of data qubits = d*d
    # and they are the first d*d qubit indices in Stim's convention. Ancilla qubits
    # are the remaining d*d - 1 qubits. We'll verify by checking the final M targets.
    #
    # Simpler still: iterate all qubit indices used in the circuit and identify data
    # qubits as those NOT used in mid-circuit MR (measure-reset) operations.
    all_qubits = set()
    mr_qubits = set()  # ancilla (measure-reset)
    for inst in template.flattened():
        if inst.name in ("R", "RX", "M", "MX", "MR", "MRX"):
            for t in inst.targets_copy():
                q = t.value
                all_qubits.add(q)
                if inst.name in ("MR", "MRX"):
                    mr_qubits.add(q)
        elif inst.name in ("H", "CX", "CZ", "X", "Y", "Z"):
            for t in inst.targets_copy():
                if t.is_qubit_target:
                    all_qubits.add(t.value)
    data_qubits = sorted(all_qubits - mr_qubits)
    # Sanity: for rotated surface code we expect d*d data qubits
    assert len(data_qubits) == d * d, (
        f"Expected {d*d} data qubits, got {len(data_qubits)}: {data_qubits}"
    )

    # Biased Pauli channel probabilities per data qubit per round.
    # Convention: bias eta = P(Z) / (P(X) + P(Y))
    # Total physical error prob = p, so P(X) + P(Y) + P(Z) = p
    # Symmetric X and Y: P(X) = P(Y) = p / (2 * (eta + 1)) * (2*eta+... )
    # Let a = P(X) = P(Y), b = P(Z). Then 2a + b = p, and b/(2a) = eta -> b = 2*a*eta
    # -> 2a + 2*a*eta = p -> a = p / (2*(1+eta))
    # -> b = p*eta / (1+eta)
    # For eta = 0.5 (depolarizing): a = p/3, b = p/3. Symmetric. Correct.
    a = p / (2.0 * (1.0 + eta))
    b = p * eta / (1.0 + eta)
    px, py, pz = a, a, b

    # Build final circuit: same as template, but before every stabilizer round
    # (identified by looking at the repeated block), inject biased noise on data qubits.
    #
    # Stim's generated rotated_memory circuits have the structure:
    #   [init prep] TICK ... TICK [round block] REPEAT rounds-1 { round block } [final measure]
    # The round block starts after the initial reset+H layer.
    #
    # Simplest robust approach: use stim.Circuit's decompose_repeats -> walk instructions
    # and after every "TICK" that immediately follows an "MR" layer of ancilla, we insert
    # a biased PAULI_CHANNEL_1 on all data qubits. But cleaner: insert biased noise on
    # data qubits AT THE START of every syndrome extraction round.
    #
    # We'll rebuild the circuit by walking the template and adding a
    # PAULI_CHANNEL_1(px,py,pz) targeting all data qubits right after every
    # "R" or "MR" operation that involves ancilla qubits (i.e., start of a round).

    new_circuit = stim.Circuit()

    def emit_biased_noise(circ):
        circ.append("PAULI_CHANNEL_1", data_qubits, [px, py, pz])

    # We need to handle REPEAT blocks: expand them so we can insert noise inside.
    # But expansion blows up. Instead we recursively handle blocks.

    def walk(circ_in, circ_out):
        for inst in circ_in:
            if isinstance(inst, stim.CircuitRepeatBlock):
                sub_out = stim.Circuit()
                walk(inst.body_copy(), sub_out)
                circ_out.append(stim.CircuitRepeatBlock(inst.repeat_count, sub_out))
            else:
                circ_out.append(inst)
                # After the ancilla measure-reset (MR/MRX) that ends a syndrome round,
                # inject biased noise on data qubits for the next round.
                if inst.name in ("MR", "MRX"):
                    emit_biased_noise(circ_out)
                # Also after the initial R (data qubit reset) at start of circuit,
                # inject a first round of noise so round 1 sees noise too.
                # (Actually Stim's generated circuit already has an "R data; H data" prep;
                #  we insert noise once after the very first R block. Simplest: insert
                #  noise right after the first R by tracking a flag.)

        return circ_out

    # First pass: inject biased noise after every MR (end of syndrome round)
    walk(template, new_circuit)

    # Additionally add measurement flip errors: before every M/MR on ancilla and
    # final M on data, add X error with probability p_meas = p (simplification;
    # paper uses code capacity model where measurements are perfect. For a
    # phenomenological / circuit noise model, adding measurement error is standard.
    # We'll produce two variants: (i) code-capacity model (perfect measurements,
    # noise only on data), (ii) phenomenological (noisy measurements too). We use
    # code capacity for the threshold study to match the paper's setting more closely.
    # -> so we DON'T add measurement noise.

    return new_circuit, data_qubits


def sample_logical_error_rate(circuit: stim.Circuit, num_shots: int, seed: int = None):
    """Sample shots, decode with PyMatching, return (num_errors, num_shots, elapsed)."""
    t0 = time.time()
    sampler = circuit.compile_detector_sampler(seed=seed)
    detection_events, observable_flips = sampler.sample(
        num_shots, separate_observables=True
    )
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    predicted = matcher.decode_batch(detection_events)
    # A shot is a logical error if predicted observable != actual observable
    num_errors = int(np.any(predicted != observable_flips, axis=1).sum())
    return num_errors, num_shots, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distances", nargs="+", type=int, default=[3, 5, 7])
    ap.add_argument(
        "--etas",
        nargs="+",
        type=float,
        default=[0.5, 10.0, 100.0, 1000.0],
        help="Bias values (P(Z)/(P(X)+P(Y))). 0.5 = depolarizing",
    )
    ap.add_argument(
        "--ps",
        nargs="+",
        type=float,
        default=[0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.25, 0.30, 0.35, 0.40, 0.45],
    )
    ap.add_argument("--shots", type=int, default=20000)
    ap.add_argument("--rounds", type=int, default=None,
                    help="Syndrome rounds. Default = distance.")
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--seed", type=int, default=1234)
    args = ap.parse_args()

    results = []
    total_start = time.time()
    for eta in args.etas:
        for d in args.distances:
            rounds = args.rounds if args.rounds else d
            for p in args.ps:
                # Skip very high p that don't matter for threshold determination
                # for low bias
                circuit, data_qubits = build_biased_surface_code_circuit(
                    d=d, rounds=rounds, p=p, eta=eta, basis="Z"
                )
                num_errors, num_shots, elapsed = sample_logical_error_rate(
                    circuit, args.shots, seed=args.seed
                )
                ler = num_errors / num_shots
                # binomial 1-sigma error
                ler_err = math.sqrt(max(num_errors, 1) * (num_shots - num_errors) / num_shots) / num_shots
                rec = {
                    "distance": d,
                    "rounds": rounds,
                    "eta": eta,
                    "p": p,
                    "shots": num_shots,
                    "num_errors": num_errors,
                    "logical_error_rate": ler,
                    "ler_err": ler_err,
                    "n_data_qubits": len(data_qubits),
                    "elapsed_sec": elapsed,
                }
                results.append(rec)
                print(
                    f"eta={eta:>6.1f} d={d} rnd={rounds} p={p:.3f} "
                    f"shots={num_shots} err={num_errors:>6d} LER={ler:.4f}±{ler_err:.4f} "
                    f"[{elapsed:.1f}s]",
                    flush=True,
                )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "args": vars(args),
            "stim_version": stim.__version__,
            "pymatching_version": pymatching.__version__,
            "numpy_version": np.__version__,
            "total_elapsed_sec": time.time() - total_start,
            "results": results,
        }, f, indent=2)
    print(f"\nWrote {out_path}  ({len(results)} rows, {time.time()-total_start:.1f}s total)")


if __name__ == "__main__":
    main()
