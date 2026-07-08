#!/usr/bin/env python3
"""
Replication of Takita et al. 2016 (arXiv:1611.06946) — Fault-tolerant [[4,2,2]] error detection.

Implements the FT encoding circuit for |00>_L (Fig. 2a) plus the two stabilizer measurements
Sz = ZZZZ, Sx = XXXX (Fig. 2e,f) using Stim under a depolarizing noise model.

Key physics reproduced:
  - Logical La (fault-tolerant, X_a=X_1X_3) and gauge Lb (non-FT, X_b=X_1X_2) errors
    are extracted from postselected shots (Sx=+1, Sz=+1, and even data-qubit parity).
  - Under depolarizing noise p per 2-qubit gate + p/10 per 1-qubit gate + p/10 SPAM
    (matching paper qualitative regime: 2q dominates, 3-4% per CNOT), we expect:
      * Yield in the 60-80% range for p ~ 0.03 (matches paper 65-78%)
      * Error(La) << Error(Lb) — the "order of magnitude" FT gap
      * Error(La) scales quadratically (or better) with p — the "convex" FT scaling
      * Error(Lb) scales linearly with p — the non-FT scaling
      * Below some p, Error(La) < physical qubit error rate

Circuit for |00>_L encoding (Fig 2a of the paper, standard [[4,2,2]] FT prep):
  Qubits: data q0,q1,q2,q3, ancilla a=q4 (extra ancilla q5 used per stabilizer round)
  |00>_L is the +1 eigenstate of both Sx=XXXX and Sz=ZZZZ, with La=Lb=|0>.
  A standard FT prep is:
      1. Start all in |0>
      2. H on q0
      3. CNOT q0->q1, q0->q2, q0->q3  (this makes (|0000>+|1111>)/sqrt(2) = |00>_L)
     (7 CNOTs total after adding stabilizer measurement: 3 for encoding + 4 for a stabilizer)

  For Sz = ZZZZ measurement: ancilla H; CZ ancilla-q0..q3 (or equivalently H q_i; CNOT q_i->a; H q_i);
    simpler: ancilla in |0>, CNOT q_i -> a for i in 0..3, measure a in Z basis.  (Since we want Sz)
  For Sx = XXXX: ancilla |+>; CNOT a -> q_i for i in 0..3; measure a in X (H then Z).

Logical bit-flip/phase-flip decoding after postselection:
  La = X_a X_a-parity from data: La=|0> iff X_1 X_3 measurement yields even parity in Hadamard basis...
  Easier: since we prepared |00>_L and measured in Z basis at end (after all gates), we look at the
  4-bit outcome pattern. |00>_L populates {0000, 1111}. |01>_L populates {0011, 1100}. |10>_L populates
  {0101, 1010}. |11>_L populates {0110, 1001}. (Even parity = code space, odd = leaked out.)

  Assignment (matching the paper's convention with Xa = X⊗I⊗X⊗I, Xb = X⊗X⊗I⊗I, i.e. the codewords
  |La Lb>_L are labelled by (Za, Zb) = (Z_1 Z_2, Z_1 Z_3) computed from the data bits):
    Given even-parity data bits (d0,d1,d2,d3):
      Za_meas = d0 XOR d1     -> La state
      Zb_meas = d0 XOR d2     -> Lb state
    (Both are stabilizer-preserving parities in the codespace.)
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import stim


def build_circuit(p: float, meas_stab: str, noise: str = "depol2", encoding: str = "flag") -> stim.Circuit:
    """Build the [[4,2,2]] |00>_L encoding + one stabilizer measurement + terminal data measurement.

    p: depolarizing physical error rate applied per 2-qubit gate; single-qubit gates
       and SPAM get p/10 (approximating the paper's regime where 2q dominates).
    noise:
      "depol2" — full 2-qubit uniform depolarizing after each CNOT (worst-case model,
                  includes correlated XX/ZZ that can defeat FT for weight-2 errors).
      "single" — each qubit gets an independent DEPOLARIZE1 after every gate it touches;
                  this is the true "single-qubit-fault" model the paper's FT claim is
                  against, and should exhibit the p^2 La suppression clearly.
    meas_stab: "Sz" or "Sx".
    """
    p2 = p                      # 2-qubit gate error (depol2 mode)
    p1 = p / 10.0               # 1-qubit gate error (depol2 mode)
    psp = p / 10.0              # SPAM / init / meas error (before/after)

    c = stim.Circuit()

    data = [0, 1, 2, 3]
    flag = 4     # flag ancilla used ONLY in encoding="flag" (paper's Fig 2a is analogous)
    anc = 5      # syndrome ancilla for stabilizer

    def one_qubit_noise(q_list):
        """Apply a single-qubit depolarizing channel per qubit — SINGLE-fault model."""
        for q in q_list:
            if p_per_qubit > 0:
                c.append("DEPOLARIZE1", [q], p_per_qubit)

    def two_qubit_noise(qa, qb):
        """Apply noise after a CNOT depending on the noise model."""
        if noise == "depol2":
            if p2 > 0:
                c.append("DEPOLARIZE2", [qa, qb], p2)
        elif noise == "single":
            # "single-qubit fault" model: with probability p per gate, exactly ONE
            # of the two involved qubits gets a uniform Pauli (X, Y, or Z).
            # Implemented as independent DEPOLARIZE1 at rate p/2 on each (so total
            # single-fault mass ~= p, and probability of TWO simultaneous faults is p^2/4).
            if p2 > 0:
                c.append("DEPOLARIZE1", [qa], p2 / 2.0)
                c.append("DEPOLARIZE1", [qb], p2 / 2.0)
        else:
            raise ValueError(noise)

    def one_qubit_gate_noise(q):
        if noise == "depol2":
            if p1 > 0:
                c.append("DEPOLARIZE1", [q], p1)
        elif noise == "single":
            if p1 > 0:
                c.append("DEPOLARIZE1", [q], p1)

    def spam_noise(q):
        if noise == "depol2":
            if psp > 0:
                c.append("X_ERROR", [q], psp)
        elif noise == "single":
            if psp > 0:
                c.append("X_ERROR", [q], psp)

    # --- Reset all with SPAM ---
    qubits_used = data + [anc] + ([flag] if encoding == "flag" else [])
    for q in qubits_used:
        c.append("R", [q])
        spam_noise(q)

    # --- Encoding |00>_L ---
    c.append("H", [0])
    one_qubit_gate_noise(0)

    if encoding == "cat":
        # Naive cat-state prep. NOT strictly FT (single X_0 mid-encoding propagates to
        # X_0 X_j and causes undetectable La+Lb error).
        for tgt in (1, 2, 3):
            c.append("CNOT", [0, tgt])
            two_qubit_noise(0, tgt)
    elif encoding == "flag":
        # FT encoding with a flag qubit wrapping the data CNOTs.
        # A single X error on q0 anywhere between the two flag-CNOTs propagates onto
        # the flag and is caught by postselecting flag=0 at the flag measurement.
        c.append("CNOT", [0, flag]); two_qubit_noise(0, flag)   # flag on
        for tgt in (1, 2, 3):
            c.append("CNOT", [0, tgt]); two_qubit_noise(0, tgt)
        c.append("CNOT", [0, flag]); two_qubit_noise(0, flag)   # flag off
        spam_noise(flag)
        c.append("M", [flag])   # flag measurement is measurement record index 0
    else:
        raise ValueError(encoding)

    # --- Stabilizer measurement ---
    if meas_stab == "Sz":
        # ZZZZ via CNOT data->anc, anc starts in |0>
        for d in data:
            c.append("CNOT", [d, anc])
            two_qubit_noise(d, anc)
        # Measure ancilla in Z
        spam_noise(anc)
        c.append("M", [anc])   # record index 0 = ancilla
    elif meas_stab == "Sx":
        # XXXX: prepare anc in |+>, apply CNOT anc->data_i, measure anc in X
        c.append("H", [anc])
        one_qubit_gate_noise(anc)
        for d in data:
            c.append("CNOT", [anc, d])
            two_qubit_noise(anc, d)
        c.append("H", [anc])
        one_qubit_gate_noise(anc)
        spam_noise(anc)
        c.append("M", [anc])
    else:
        raise ValueError(meas_stab)

    # --- Terminal Z measurement of the 4 data qubits ---
    for d in data:
        spam_noise(d)
        c.append("M", [d])   # record indices 1..4

    return c


def analyze(shots: np.ndarray, encoding: str = "flag") -> dict:
    """For encoding="cat":  shots[:,0]=stab-anc, shots[:,1..4]=data
    For encoding="flag": shots[:,0]=flag, shots[:,1]=stab-anc, shots[:,2..5]=data.

    Returns:
      yield_frac: fraction of shots with ancilla=0 (stabilizer=+1) AND even data parity
      err_La: P(La != 0 | accepted)
      err_Lb: P(Lb != 0 | accepted)
      err_11: P((La,Lb)=(1,1) | accepted)
      n_accept, n_total, populations dict
    """
    n = shots.shape[0]
    if encoding == "cat":
        anc = shots[:, 0]
        data = shots[:, 1:5]
        flag_accept = np.ones(n, dtype=bool)
    elif encoding == "flag":
        flag = shots[:, 0]
        anc = shots[:, 1]
        data = shots[:, 2:6]
        flag_accept = (flag == 0)
    else:
        raise ValueError(encoding)

    even = (data.sum(axis=1) % 2) == 0
    accept = flag_accept & (anc == 0) & even
    n_accept = int(accept.sum())

    if n_accept == 0:
        return {
            "n_total": n,
            "n_accept": 0,
            "yield_frac": 0.0,
            "err_La": None,
            "err_Lb": None,
            "err_11": None,
            "populations": {},
        }

    d = data[accept]
    # Za_meas = d0 XOR d1  -> La
    # Zb_meas = d0 XOR d2  -> Lb
    La = (d[:, 0] ^ d[:, 1]).astype(int)
    Lb = (d[:, 0] ^ d[:, 2]).astype(int)

    err_La = float(La.mean())
    err_Lb = float(Lb.mean())
    err_11 = float(((La == 1) & (Lb == 1)).mean())

    pop = {}
    for La_v in (0, 1):
        for Lb_v in (0, 1):
            k = f"|{La_v}{Lb_v}>_L"
            pop[k] = float(((La == La_v) & (Lb == Lb_v)).mean())

    # Also compute "leakage" out of codespace (odd parity or ancilla=1)
    n_stab_trigger = int(((anc == 1) & even).sum())
    n_odd = int((~even).sum())

    return {
        "n_total": n,
        "n_accept": n_accept,
        "yield_frac": n_accept / n,
        "n_stab_trigger": n_stab_trigger,
        "n_odd_parity": n_odd,
        "err_La": err_La,
        "err_Lb": err_Lb,
        "err_11": err_11,
        "populations": pop,
    }


def bare_physical_error(p: float, shots: int = 200_000, seed: int = 0) -> float:
    """Reference: bare physical qubit prepared in |0>, measured — just one X_ERROR then M.

    We charge one SPAM (init) + one SPAM (readout) at rate p/10 each, same as circuit-level.
    Bare qubit error = 2*(p/10) - 2*(p/10)^2 ~ p/5 at small p.
    """
    psp = p / 10.0
    c = stim.Circuit()
    c.append("R", [0])
    c.append("X_ERROR", [0], psp)   # init error
    c.append("X_ERROR", [0], psp)   # readout error
    c.append("M", [0])
    s = c.compile_sampler(seed=seed)
    out = s.sample(shots).astype(int)[:, 0]
    return float(out.mean())


def run_scan(p_values, stab: str, shots: int, seed: int = 0, noise: str = "depol2", encoding: str = "flag") -> list:
    rows = []
    for p in p_values:
        c = build_circuit(p, stab, noise=noise, encoding=encoding)
        sampler = c.compile_sampler(seed=seed)
        out = sampler.sample(shots).astype(int)
        stats = analyze(out, encoding=encoding)
        stats["p"] = p
        stats["stab"] = stab
        stats["noise"] = noise
        stats["encoding"] = encoding
        stats["shots"] = shots
        stats["bare_p_err"] = bare_physical_error(p, shots=min(shots, 200_000), seed=seed + 1)
        rows.append(stats)
        seed += 100
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, default=200_000)
    ap.add_argument("--out", type=str, default="results.json")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--noise", choices=["depol2", "single", "both"], default="both",
                    help="Noise model: depol2 (uniform 2q depolarizing) or single (single-qubit-fault only) or both.")
    ap.add_argument("--encoding", choices=["cat", "flag", "both"], default="both",
                    help="Encoding: cat (naive, not FT vs XX) or flag (FT via flag qubit) or both.")
    args = ap.parse_args()

    p_values = [0.0, 0.001, 0.003, 0.01, 0.03, 0.05, 0.1, 0.2]
    noise_models = ["depol2", "single"] if args.noise == "both" else [args.noise]
    encodings = ["cat", "flag"] if args.encoding == "both" else [args.encoding]

    t0 = time.time()
    print(f"# stim version: {stim.__version__}")
    print(f"# shots per point: {args.shots}")
    print(f"# p values: {p_values}")
    print(f"# noise models: {noise_models}")

    all_results = {}
    for encoding in encodings:
        print(f"\n############### Encoding: {encoding} ###############")
        all_results[encoding] = {}
        for noise in noise_models:
            print(f"\n############## Encoding={encoding}  Noise={noise} ##############")
            results = {}
            for stab in ("Sz", "Sx"):
                print(f"\n=== enc={encoding} noise={noise} stab={stab} ===")
                rows = run_scan(p_values, stab, args.shots, seed=args.seed, noise=noise, encoding=encoding)
                results[stab] = rows
                print(f"{'p':>8} {'yield':>8} {'err_La':>11} {'err_Lb':>11} {'Lb/La':>8} {'bare_p':>10}")
                for r in rows:
                    ratio = (r["err_Lb"] / r["err_La"]) if (r["err_La"] and r["err_La"] > 1e-6) else float("inf")
                    print(f"{r['p']:>8.4f} {r['yield_frac']:>8.4f} "
                          f"{(r['err_La'] or 0):>11.6f} {(r['err_Lb'] or 0):>11.6f} "
                          f"{ratio:>8.2f} {r['bare_p_err']:>10.5f}")

            # Paper comparison @ p=0.03
            print(f"\n=== Paper comparison @ p=0.03 (enc={encoding} noise={noise}) ===")
            for stab in ("Sz", "Sx"):
                row = [r for r in results[stab] if abs(r["p"] - 0.03) < 1e-9][0]
                paper_Lb = "1.7" if stab == "Sz" else "2.4"
                paper_yld = "77.8" if stab == "Sz" else "65.2"
                paper_ratio = "6x" if stab == "Sz" else "8x"
                print(f"{stab}: yield={row['yield_frac']*100:.1f}% (paper: {paper_yld}%)  "
                      f"err_La={row['err_La']*100:.3f}% (paper: 0.3%)  "
                      f"err_Lb={row['err_Lb']*100:.3f}% (paper: {paper_Lb}%)  "
                      f"ratio Lb/La={row['err_Lb']/max(row['err_La'],1e-9):.1f}x (paper: {paper_ratio})")

            # FT-scaling test (fit log-log slope in the small-p regime, up to p=0.03)
            print(f"\n=== FT-scaling test (log-log slope, enc={encoding} noise={noise}) ===")
            for stab in ("Sz", "Sx"):
                pts = [r for r in results[stab] if 0.0009 < r["p"] < 0.031 and r["err_La"] and r["err_Lb"]]
                if len(pts) >= 3:
                    ps = np.array([r["p"] for r in pts])
                    La = np.array([r["err_La"] for r in pts])
                    Lb = np.array([r["err_Lb"] for r in pts])
                    slope_La, _ = np.polyfit(np.log(ps), np.log(La), 1)
                    slope_Lb, _ = np.polyfit(np.log(ps), np.log(Lb), 1)
                    print(f"{stab}: slope err_La ~ p^{slope_La:.2f} (FT expect >=2 for flag+single)   "
                          f"slope err_Lb ~ p^{slope_Lb:.2f} (NFT expect ~1)")

            all_results[encoding][noise] = results

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({
            "stim_version": stim.__version__,
            "shots_per_point": args.shots,
            "p_values": p_values,
            "noise_models": noise_models,
            "encodings": encodings,
            "results": all_results,
            "elapsed_sec": time.time() - t0,
        }, f, indent=2, default=str)
    print(f"\nWrote {out_path}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
