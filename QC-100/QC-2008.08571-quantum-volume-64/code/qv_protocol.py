#!/usr/bin/env python3
"""
Independent replication of the Quantum Volume protocol from
Jurcevic et al., arXiv:2008.08571 ("Demonstration of quantum volume 64 on a
superconducting quantum computing system", IBM 2020).

Original QV protocol reference: Cross et al., PRA 100, 032328 (2019),
arXiv:1811.12926 (cited as [1] in the paper).

This script implements the QV protocol on a NOISELESS statevector simulator
and, optionally, under depolarizing noise. It cannot reproduce IBM's hardware
QV=64 result (that requires access to ibmq_montreal + all their pulse-level
improvements). What we DO reproduce here:

  1. The protocol itself: generate random square QV circuits of width n and
     depth d=n, compute the ideal heavy-output set from the statevector,
     then measure the circuit on a simulator and compute HOP.
  2. The QV pass criterion: mean HOP > 2/3 with 2sigma confidence,
     giving quantum volume QV = 2**n_pass.
  3. Under noiseless simulation, HOP tends to the asymptotic value
     (1 + ln 2)/2 ~ 0.847, well above 2/3 -> protocol passes at all widths.
  4. Under a small per-2q-gate depolarizing noise, HOP degrades with n,
     illustrating the same qualitative behavior IBM had to fight against.

Outputs are written as JSON to ../report/evidence/ .
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import quantum_volume as qv_func
from qiskit.quantum_info import Statevector

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent / "report" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------ #
# Core QV protocol pieces
# ------------------------------------------------------------------ #

def heavy_outputs(statevector: np.ndarray) -> tuple[set[int], float]:
    """
    Given the ideal statevector of a QV circuit, return
      (set of computational-basis bitstrings whose ideal probability
       exceeds the median probability, sum of their ideal probabilities).

    This is the standard QV heavy-output-set definition
    (Cross et al. 2019, Def. 1).
    """
    probs = np.abs(statevector) ** 2
    median = float(np.median(probs))
    heavy_mask = probs > median
    heavy = {int(i) for i, m in enumerate(heavy_mask) if m}
    return heavy, float(probs[heavy_mask].sum())


def sampled_hop(counts: dict[str, int], heavy: set[int], n_qubits: int) -> float:
    """
    Fraction of measured shots whose bitstring lies in the heavy-output set.
    Qiskit returns bitstrings in little-endian text; convert to int.
    """
    total = sum(counts.values())
    if total == 0:
        return 0.0
    hits = 0
    for bitstring, c in counts.items():
        # Qiskit bitstring is q_{n-1}...q_1 q_0, i.e. little-endian in the sense
        # that leftmost char is highest qubit index. int(bitstring, 2) matches
        # the statevector index convention Qiskit uses.
        idx = int(bitstring.replace(" ", ""), 2)
        if idx in heavy:
            hits += c
    return hits / total


def two_sigma_lower(mean_hop: float, n_circuits: int) -> float:
    """
    Standard QV 2-sigma lower bound on the mean HOP after n_circuits circuits
    (Cross et al. 2019, appendix A; also appendix C of the QV64 paper).

    A conservative binomial/Wilson-style bound:
        sigma = sqrt(mean * (1 - mean) / n_circuits)
        lower = mean - 2 * sigma
    """
    if n_circuits <= 0:
        return 0.0
    sigma = math.sqrt(max(mean_hop * (1.0 - mean_hop), 0.0) / n_circuits)
    return mean_hop - 2.0 * sigma


# ------------------------------------------------------------------ #
# Optional noise model (depolarizing on 1q and 2q gates)
# ------------------------------------------------------------------ #

def build_noise_model(p1: float, p2: float) -> NoiseModel:
    nm = NoiseModel()
    if p1 > 0:
        one_q_err = depolarizing_error(p1, 1)
        nm.add_all_qubit_quantum_error(one_q_err, ["u1", "u2", "u3", "u", "rx", "ry", "rz", "sx", "x", "h"])
    if p2 > 0:
        two_q_err = depolarizing_error(p2, 2)
        nm.add_all_qubit_quantum_error(two_q_err, ["cx", "cz", "ecr"])
    return nm


# ------------------------------------------------------------------ #
# One QV experiment at a given width n
# ------------------------------------------------------------------ #

@dataclass
class QVResult:
    width: int
    depth: int
    n_circuits: int
    n_shots: int
    mean_hop: float
    two_sigma_lower_hop: float
    ideal_mean_heavy_prob: float
    per_circuit_hop: list[float]
    passes_2_over_3: bool
    quantum_volume_if_pass: int
    noise: dict
    wall_time_sec: float


def run_qv_at_width(
    n: int,
    n_circuits: int,
    n_shots: int,
    seed: int,
    noise_p1: float = 0.0,
    noise_p2: float = 0.0,
) -> QVResult:
    """
    Run the QV protocol at width=depth=n for n_circuits random circuits,
    n_shots per circuit. Return aggregate stats.
    """
    t0 = time.time()
    rng = np.random.default_rng(seed)

    # Backend for measurement sampling
    if noise_p1 > 0 or noise_p2 > 0:
        noise = build_noise_model(noise_p1, noise_p2)
        sim = AerSimulator(noise_model=noise)
    else:
        sim = AerSimulator()

    per_hop: list[float] = []
    ideal_heavy_probs: list[float] = []

    for i in range(n_circuits):
        circ_seed = int(rng.integers(0, 2**31 - 1))
        # QuantumVolume model circuit (square: depth=width=n).
        # `quantum_volume(...)` (Qiskit >=2.2) returns a QuantumCircuit whose
        # layers are random SU(4) blocks on random qubit permutations.
        qv = qv_func(num_qubits=n, depth=n, seed=circ_seed)

        # Ideal statevector (no measurements)
        sv = Statevector.from_instruction(qv)
        heavy, ideal_hp = heavy_outputs(np.asarray(sv.data))
        ideal_heavy_probs.append(ideal_hp)

        # Now build a version with measurements for simulator sampling
        meas = QuantumCircuit(n, n)
        meas.compose(qv, qubits=range(n), inplace=True)
        meas.measure(range(n), range(n))
        tqc = transpile(meas, sim, optimization_level=1, seed_transpiler=circ_seed)
        result = sim.run(tqc, shots=n_shots).result()
        counts = result.get_counts()
        per_hop.append(sampled_hop(counts, heavy, n))

    mean_hop = float(np.mean(per_hop))
    lower = two_sigma_lower(mean_hop, n_circuits)
    passes = lower > (2.0 / 3.0)
    dt = time.time() - t0

    return QVResult(
        width=n,
        depth=n,
        n_circuits=n_circuits,
        n_shots=n_shots,
        mean_hop=mean_hop,
        two_sigma_lower_hop=lower,
        ideal_mean_heavy_prob=float(np.mean(ideal_heavy_probs)),
        per_circuit_hop=per_hop,
        passes_2_over_3=passes,
        quantum_volume_if_pass=(2 ** n if passes else 0),
        noise={"p1": noise_p1, "p2": noise_p2},
        wall_time_sec=dt,
    )


# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--widths", type=int, nargs="+", default=[2, 3, 4, 5],
                    help="QV widths to test (depth = width).")
    ap.add_argument("--circuits", type=int, default=100,
                    help="Number of random QV circuits per width.")
    ap.add_argument("--shots", type=int, default=1024,
                    help="Shots per circuit.")
    ap.add_argument("--seed", type=int, default=20260703)
    ap.add_argument("--noise-p1", type=float, default=0.0)
    ap.add_argument("--noise-p2", type=float, default=0.0)
    ap.add_argument("--tag", type=str, default="noiseless",
                    help="Tag for output filename.")
    args = ap.parse_args()

    print(f"[qv_protocol] widths={args.widths}  circuits={args.circuits}  "
          f"shots={args.shots}  noise=(p1={args.noise_p1}, p2={args.noise_p2})",
          flush=True)

    out = {
        "paper": "arXiv:2008.08571",
        "protocol_reference": "Cross et al., PRA 100, 032328 (2019); arXiv:1811.12926",
        "config": vars(args),
        "results": [],
    }

    for n in args.widths:
        res = run_qv_at_width(
            n=n,
            n_circuits=args.circuits,
            n_shots=args.shots,
            seed=args.seed + n,
            noise_p1=args.noise_p1,
            noise_p2=args.noise_p2,
        )
        d = asdict(res)
        # Trim per-circuit HOP if massive
        d["per_circuit_hop_summary"] = {
            "min": float(np.min(res.per_circuit_hop)),
            "max": float(np.max(res.per_circuit_hop)),
            "n": len(res.per_circuit_hop),
        }
        out["results"].append(d)
        print(
            f"  n={n:>2}  mean_HOP={res.mean_hop:.4f}  "
            f"2s_lower={res.two_sigma_lower_hop:.4f}  "
            f"ideal_heavy_prob={res.ideal_mean_heavy_prob:.4f}  "
            f"passes>2/3={res.passes_2_over_3}  "
            f"QV_if_pass={res.quantum_volume_if_pass}  "
            f"wall={res.wall_time_sec:.1f}s",
            flush=True,
        )

    out_path = EVIDENCE / f"qv_results_{args.tag}.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"[qv_protocol] wrote {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
