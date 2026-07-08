#!/usr/bin/env python3
"""
Character randomized benchmarking (character-RB) for a non-Clifford subgroup:
the single-qubit **Pauli group** P1 = {I, X, Y, Z} (as unsigned Weyl operators
in PU(2), size 4).

Motivation (Helsen et al. 2019, arXiv:1806.02048):

  Standard RB (eq. 1 of the paper) works ONLY when the benchmarking group is
  the full Clifford group; for other gatesets the survival probability decays
  as a sum of several exponentials (eq. 2), which is very hard to fit.

  The paper's fix is *character* RB: multiply survival probabilities by a
  character function chi_lambda(g_0) and average. This projects out ONE
  irreducible-representation channel, yielding a SINGLE clean exponential
  (eq. 3-5 of the paper) that can be fitted robustly with much less data.

Concrete test here:

  Benchmark group  G = <I, X, Y, Z> (single-qubit Pauli group), which is
  NOT the full Clifford group, so standard RB does NOT give a clean decay.

  We inject the same depolarizing noise as the standard RB experiment and:

  (A) run "naive Pauli RB" — sample random Pauli sequences, apply inverse,
      measure |0>, fit A + B f^m.  This will fit poorly or give a decay that
      does not track the injected error (multiple decay channels present).

  (B) run *character* Pauli RB following the paper's recipe:
        - pick an irrep index lambda (a non-identity Pauli w)
        - draw a random 'character-averaging' element g_0 uniformly from G
        - build sequence (g_0, g_1, ..., g_m, inv) as usual
        - measure in the Z basis
        - multiply the survival probability by chi_lambda(g_0)
        - average over many (sequence, g_0) draws
      Fit the resulting character-averaged data to a SINGLE exponential
      f_lambda^m and read off f_lambda.

Efficiency claim (from the paper): (B) uses fewer sequences and yields a
clean single-exponential fit; (A) either needs many more sequences to
disentangle the multi-exponential decay or gives an ambiguous number.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
from scipy.optimize import curve_fit

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import IGate, XGate, YGate, ZGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# --- single-qubit Pauli group as circuits ---------------------------------
PAULI_NAMES = ["I", "X", "Y", "Z"]

def pauli_gate(name: str):
    return {"I": IGate(), "X": XGate(), "Y": YGate(), "Z": ZGate()}[name]

def pauli_circuit(name: str) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.append(pauli_gate(name), [0])
    return qc

# multiplication table on unsigned Paulis (in PU(2)): ignores +/- 1, +/- i signs
PAULI_MUL = {
    ("I", "I"): "I", ("I", "X"): "X", ("I", "Y"): "Y", ("I", "Z"): "Z",
    ("X", "I"): "X", ("X", "X"): "I", ("X", "Y"): "Z", ("X", "Z"): "Y",
    ("Y", "I"): "Y", ("Y", "X"): "Z", ("Y", "Y"): "I", ("Y", "Z"): "X",
    ("Z", "I"): "Z", ("Z", "X"): "Y", ("Z", "Y"): "X", ("Z", "Z"): "I",
}

def product_of_paulis(seq: List[str]) -> str:
    acc = "I"
    for p in seq:
        acc = PAULI_MUL[(acc, p)]
    return acc

# characters chi_lambda(g) for the 4 1-D irreps of the abelian group
# G = Z_2 x Z_2 (unsigned Paulis).  Label irreps by w in {I, X, Y, Z}.
# chi_w(g) = +1 if g commutes with w in the symplectic sense, else -1.
# Equivalently, for the abelian Pauli group (unsigned) all irreps are 1-D
# and chi_w(g) = +/-1 encoding the pairing.
# Concretely (up to symplectic parity table):
#   chi_I  = +1 for all g
#   chi_X (g in {I,X}) = +1;  (g in {Y,Z}) = -1
#   chi_Y (g in {I,Y}) = +1;  (g in {X,Z}) = -1
#   chi_Z (g in {I,Z}) = +1;  (g in {X,Y}) = -1
CHAR_TABLE = {
    "I": {"I": +1, "X": +1, "Y": +1, "Z": +1},
    "X": {"I": +1, "X": +1, "Y": -1, "Z": -1},
    "Y": {"I": +1, "X": -1, "Y": +1, "Z": -1},
    "Z": {"I": +1, "X": -1, "Y": -1, "Z": +1},
}


def build_pauli_sequence(m: int, rng: np.random.Generator
                         ) -> Tuple[List[str], str]:
    """Return (list of m Pauli names, name of inverse Pauli)."""
    idx = rng.integers(0, 4, size=m)
    names = [PAULI_NAMES[i] for i in idx]
    prod = product_of_paulis(names)
    inv = prod  # Paulis are self-inverse (unsigned)
    return names, inv


def circuit_for_pauli_sequence(names: List[str], inv: str,
                               prepend: str | None = None
                               ) -> QuantumCircuit:
    """Build measurement circuit for state |0>, applying (optionally a
    prepend gate g_0) then the m Pauli gates then the inverse Pauli.
    Prepend g_0 is applied BEFORE the sequence (i.e. as the first gate
    acting on the state); mathematically equivalent to appending g_0 to the
    left of the sequence per Fig. 1 of the paper."""
    qc = QuantumCircuit(1, 1)
    if prepend is not None:
        qc.append(pauli_gate(prepend), [0])
    for n in names:
        qc.append(pauli_gate(n), [0])
    qc.append(pauli_gate(inv), [0])
    qc.measure(0, 0)
    return qc


def survival_prob_from_counts(counts: dict, shots: int) -> float:
    return counts.get("0", 0) / shots


# --- noise model ----------------------------------------------------------

def make_noise(p_gate_depol: float) -> NoiseModel:
    nm = NoiseModel()
    err = depolarizing_error(p_gate_depol, 1)
    for g in ["x", "y", "z", "id"]:
        nm.add_all_qubit_quantum_error(err, [g])
    return nm


# --- experiments ----------------------------------------------------------

@dataclass
class Params:
    p_gate_depol: float
    seq_lengths: List[int]
    seqs_per_length: int
    shots: int
    seed: int
    lambda_irrep: str = "Z"


def run_naive_pauli_rb(params: Params, sim: AerSimulator) -> dict:
    """(A) Naive Pauli RB: no character averaging."""
    rng = np.random.default_rng(params.seed + 1000)
    curve = []
    for m in params.seq_lengths:
        surv_list = []
        for _ in range(params.seqs_per_length):
            names, inv = build_pauli_sequence(m, rng)
            qc = circuit_for_pauli_sequence(names, inv, prepend=None)
            tqc = transpile(qc, sim,
                            basis_gates=["x", "y", "z", "id", "measure"],
                            optimization_level=0)
            res = sim.run(tqc, shots=params.shots).result()
            surv_list.append(survival_prob_from_counts(res.get_counts(),
                                                      params.shots))
        curve.append((m, float(np.mean(surv_list)),
                      float(np.std(surv_list) / np.sqrt(len(surv_list)))))
        print(f"  [A/naive]  m={m:>3d}  <p>={curve[-1][1]:.4f}")
    return {"curve": curve}


def run_character_pauli_rb(params: Params, sim: AerSimulator) -> dict:
    """(B) Character Pauli RB with irrep lambda = params.lambda_irrep."""
    rng = np.random.default_rng(params.seed + 2000)
    curve = []
    lam = params.lambda_irrep
    for m in params.seq_lengths:
        char_vals = []
        for _ in range(params.seqs_per_length):
            # draw g_0 uniformly from the group and multiply survival by chi(g_0)
            g0 = PAULI_NAMES[rng.integers(0, 4)]
            names, inv = build_pauli_sequence(m, rng)
            qc = circuit_for_pauli_sequence(names, inv, prepend=g0)
            tqc = transpile(qc, sim,
                            basis_gates=["x", "y", "z", "id", "measure"],
                            optimization_level=0)
            res = sim.run(tqc, shots=params.shots).result()
            surv = survival_prob_from_counts(res.get_counts(), params.shots)
            # character projects onto irrep 'lam'; also shift to Z-expectation
            # because the projector <Z> = 2 p_0 - 1 tracks the depolarizing decay
            z_exp = 2 * surv - 1
            char = CHAR_TABLE[lam][g0]
            char_vals.append(char * z_exp)
        mean_char = float(np.mean(char_vals))
        sem = float(np.std(char_vals) / np.sqrt(len(char_vals)))
        curve.append((m, mean_char, sem))
        print(f"  [B/char lambda={lam}]  m={m:>3d}  <chi*<Z>>={mean_char:.4f}")
    return {"curve": curve}


def fit_exponential(curve: List[Tuple[int, float, float]],
                    two_param: bool = False):
    ms = np.array([c[0] for c in curve], dtype=float)
    ys = np.array([c[1] for c in curve], dtype=float)
    sem = np.array([max(c[2], 1e-4) for c in curve], dtype=float)
    if two_param:
        # y = B * f^m  (character RB: no offset because <Z>_max = 0)
        def model(m, B, f):
            return B * (f ** m)
        p0 = [ys[0] if ys[0] > 0 else 1.0, 0.98]
        try:
            popt, pcov = curve_fit(model, ms, ys, sigma=sem, p0=p0,
                                   bounds=([-2, 0], [2, 1.0]),
                                   absolute_sigma=True, maxfev=20000)
            B, f = float(popt[0]), float(popt[1])
            perr = np.sqrt(np.diag(pcov))
            return {"A": 0.0, "B": B, "f": f,
                    "A_stderr": 0.0,
                    "B_stderr": float(perr[0]),
                    "f_stderr": float(perr[1]),
                    "form": "B*f^m"}
        except Exception as e:
            return {"error": str(e), "form": "B*f^m"}
    else:
        def model(m, A, B, f):
            return A + B * (f ** m)
        p0 = [0.5, 0.5, 0.98]
        try:
            popt, pcov = curve_fit(model, ms, ys, sigma=sem, p0=p0,
                                   bounds=([0, 0, 0], [1, 1, 1]),
                                   absolute_sigma=True, maxfev=20000)
            A, B, f = [float(x) for x in popt]
            perr = np.sqrt(np.diag(pcov))
            return {"A": A, "B": B, "f": f,
                    "A_stderr": float(perr[0]),
                    "B_stderr": float(perr[1]),
                    "f_stderr": float(perr[2]),
                    "form": "A+B*f^m"}
        except Exception as e:
            return {"error": str(e), "form": "A+B*f^m"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=float, default=0.01)
    ap.add_argument("--seqs", type=int, default=40)
    ap.add_argument("--shots", type=int, default=512)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--lengths", type=str,
                    default="1,2,4,8,16,32,64,96")
    ap.add_argument("--lam", type=str, default="Z",
                    help="irrep label for character RB")
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    lengths = [int(x) for x in args.lengths.split(",")]
    params = Params(
        p_gate_depol=args.p,
        seq_lengths=lengths,
        seqs_per_length=args.seqs,
        shots=args.shots,
        seed=args.seed,
        lambda_irrep=args.lam,
    )
    noise = make_noise(args.p)
    sim = AerSimulator(noise_model=noise)

    print(f"[naive Pauli RB]  p={args.p}  seqs={args.seqs}")
    t0 = time.time()
    res_A = run_naive_pauli_rb(params, sim)
    dt_A = time.time() - t0

    print(f"[character Pauli RB lambda={args.lam}]")
    t0 = time.time()
    res_B = run_character_pauli_rb(params, sim)
    dt_B = time.time() - t0

    fit_A = fit_exponential(res_A["curve"], two_param=False)
    fit_B = fit_exponential(res_B["curve"], two_param=True)

    print("\nFits:")
    print(f"  naive  : {fit_A}")
    print(f"  charRB : {fit_B}")

    # Expected f for a depolarizing 1q channel of param p_dep:
    # single-Pauli-gate application -> depolarizing channel with survival
    # f_pauli = 1 - (4/3) * p_dep   for the single-qubit case (chan on Bloch
    # vector shrinks by 1 - (4/3)p).  Each RB step applies effectively 1
    # basis gate (Pauli), so f ~ 1 - (4/3)*p.
    d = 2
    p_expected = args.p
    f_expected_single = 1.0 - (2 * d / (d - 1) / d) * p_expected  # = 1 - 2p for d=2
    # actually for 1q depolarizing with prob p:
    #   Bloch vector -> (1 - 4p/3) * r  (Nielsen-Chuang convention)
    # so per basis-Pauli gate the character f = 1 - 4p/3
    f_expected = 1.0 - (4.0 / 3.0) * p_expected

    out = {
        "params": {
            "p_gate_depol": args.p,
            "seq_lengths": lengths,
            "seqs_per_length": args.seqs,
            "shots": args.shots,
            "seed": args.seed,
            "lambda_irrep": args.lam,
        },
        "naive": {"curve": [{"m": int(m), "y": float(y), "sem": float(s)}
                            for m, y, s in res_A["curve"]],
                  "fit": fit_A,
                  "wall_sec": dt_A},
        "character": {"curve": [{"m": int(m), "y": float(y), "sem": float(s)}
                                for m, y, s in res_B["curve"]],
                      "fit": fit_B,
                      "wall_sec": dt_B},
        "expected_f_per_basis_gate": f_expected,
    }
    (out_dir / "rb_character_pauli_result.json").write_text(
        json.dumps(out, indent=2))
    print(f"\nExpected f (per basis gate) = {f_expected:.5f}")
    print(f"Character-RB fitted f       = {fit_B.get('f', 'nan')}")
    print(f"Naive-RB fitted f           = {fit_A.get('f', 'nan')}")


if __name__ == "__main__":
    main()
