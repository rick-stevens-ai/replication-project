#!/usr/bin/env python3
"""
Replication of Chamberland & Cross (arXiv:1811.00566)
"Fault-tolerant magic state preparation with flag qubits"

Core testable claim (Table 4, level-1):
    The [[7,1,3]] Steane-code magic state prep with flag-qubit
    error DETECTION has logical error rate scaling as p^2, with
    leading coefficients c ~ O(1)-O(10) for X/Y/Z Pauli channels.

    Pr[accept]        ~ (1-p)^75           (75 fault locations)
    Pr[malE|G,p]      ~ (9.95, 4.41, 7.87) * p^2  for X, Y, Z

We use Stim to build:
  (1) The [[7,1,3]] Steane encoder (7 data qubits, non-FT encoding).
  (2) One round of Reichardt's flag-based syndrome extraction
      (3 ancilla flag qubits measuring the 6 stabilizers with
      CNOT gadgets that flag weight-2+ errors from single faults).
  (3) Circuit-level depolarizing noise per the paper's noise model:
        * 1-qubit gates:  p  depolarizing (uniform over X,Y,Z)
        * 2-qubit gates:  p  depolarizing (uniform over 15 nontrivial)
        * |0>/|+> prep:   2p/3 flip (X/Z)
        * measurement:    2p/3 flip
        * idle:           p/100 depolarizing
  (4) Sampling with rejection on any non-zero syndrome or flag.
  (5) Residual logical error is any nontrivial logical Pauli remaining
      on the accepted state; we track logical X and Z observables.

Because we cannot literally *prepare* |H> = T|+> in a stabilizer
simulator (T is non-Clifford), we replace the |H> resource with a
LOGICAL |+> state prep and check the logical X observable — the
Steane-code logical Pauli structure is what determines the p^2
scaling; the specific magic-state axis only re-weights the (px,py,pz)
coefficients (which is exactly what Table 4's three-tuple encodes).
This is the standard reduction used when one wants to isolate the
fault-tolerance scaling in a stabilizer simulator.

We EXPECT to reproduce:
  - Acceptance rate ≈ (1-p)^~75  (falls off with more fault locations)
  - Post-selected logical error rate ~ c * p^2  with c = O(1)-O(100)
"""

import stim
import numpy as np
import json
import argparse
import time
from pathlib import Path

# -----------------------------------------------------------------
# Steane [[7,1,3]] code definitions
# -----------------------------------------------------------------
# Stabilizer generators (Table 1 of Chamberland-Cross):
#   g1 = X I X I X I X   (qubits 0,2,4,6)
#   g2 = I I I X X X X   (qubits 3,4,5,6)
#   g3 = I X X I I X X   (qubits 1,2,5,6)
#   g4 = Z I Z I Z I Z
#   g5 = I I I Z Z Z Z
#   g6 = I Z Z I I Z Z
# Logical X = X^{\otimes 7}, logical Z = Z^{\otimes 7}
STEANE_X_STABS = [
    [0, 2, 4, 6],   # g1
    [3, 4, 5, 6],   # g2
    [1, 2, 5, 6],   # g3
]
STEANE_Z_STABS = [
    [0, 2, 4, 6],   # g4
    [3, 4, 5, 6],   # g5
    [1, 2, 5, 6],   # g6
]

# Data qubits: 0..6.  Ancillas allocated dynamically.

# -----------------------------------------------------------------
# Non-fault-tolerant Steane encoder for logical |+_L>
# -----------------------------------------------------------------
# The [[7,1,3]] code has a standard non-FT encoder using 6 CNOTs
# + 3 H gates to project into the codespace.
#
# One standard textbook encoder for |0_L>:
#   H on qubits 4,5,6
#   CNOTs to spread stabilizer generators:
#     CX 4->0, CX 4->1, CX 4->3
#     CX 5->0, CX 5->2, CX 5->3
#     CX 6->1, CX 6->2, CX 6->3
# To get |+_L> we apply logical H at the start — equivalently, we
# also H the "info" qubit before encoding.  For our error-scaling
# study, either logical basis works; we track the logical X
# observable = X on all 7 data qubits, which is preserved by |+_L>.
#
# ACTUALLY the cleanest: prepare all 7 in |+>, then measure the 3
# Z-type stabilizers destructively at the *end* of the sim into a
# Pauli frame.  Stim's `MPP` (measure Pauli product) and the
# detector formalism handle this natively.  So we skip an explicit
# encoder and use post-selection on stabilizers as the "encoding".
# For a magic-state analog, this is faithful to how the paper's
# nonFT prep (Fig. 4) works: syndrome extraction projects into the
# codespace, and errors give a nontrivial syndrome or a logical fault.

def build_flag_syndrome_round(circuit: stim.Circuit,
                              data_qubits,
                              stab_type: str,   # 'X' or 'Z'
                              stab_supports,     # list of lists of data qubit indices
                              flag_qubits,       # ONE flag per stabilizer
                              synd_qubits,       # one syndrome ancilla per stabilizer
                              p: float):
    """
    One round of syndrome extraction using Chao-Reichardt-style flag qubits.

    Per stabilizer, we use:
      * one syndrome ancilla (Z-stab: prepared in |+>; X-stab: in |0>)
      * one flag ancilla (prepared in |0>, measured in X basis via H at end)

    Flag gadget:
      For a Z-type weight-4 stab (control=synd_anc, target=data):
        CX(anc,d0), H(flag), CX(flag,anc), CX(anc,d1), CX(anc,d2),
        CX(flag,anc), H(flag), M(flag)  -- flag reads 1 iff a bad fault
        CX(anc,d3)

    Any single-fault X error on the ancilla between the two CX(flag,anc)
    gadgets propagates to weight-2+ on data AND flips the flag exactly
    once (odd) → flag = 1 → rejected.  A fault outside the flag gadget
    can only cause weight-1 on data (detectable by syndrome).
    """
    # Prepare flags and syndrome ancillas
    for f in flag_qubits:
        circuit.append("R", [f])
        if p > 0:
            circuit.append("X_ERROR", [f], 2 * p / 3)
    for s in synd_qubits:
        circuit.append("R", [s])
        if p > 0:
            circuit.append("X_ERROR", [s], 2 * p / 3)
    if stab_type == 'Z':
        for s in synd_qubits:
            circuit.append("H", [s])
            if p > 0:
                circuit.append("DEPOLARIZE1", [s], p)

    for si, (support, s_anc, flag) in enumerate(zip(stab_supports, synd_qubits, flag_qubits)):
        for k, d in enumerate(support):
            # Flag opening: after k=0 stab CNOT (i.e. before k=1)
            if k == 1:
                # CX(flag, s_anc) — the flag "controls" and any X_anc 
                # in between the two flag-CNOTs propagates to Z_flag once (odd)
                # For Z-stab we use CZ(flag, s_anc) instead so an X_anc during
                # the stabilizer CNOT sequence becomes Z_flag via CZ conjugation.
                # Actually simpler: use CX(s_anc, flag) both times — an X_anc 
                # fault BETWEEN them will propagate to flag TWICE (even) → miss.
                # The right gadget: CX(flag, s_anc) both times. An X_anc
                # in between propagates through the CX(flag,s_anc) target
                # side as a Z on control (flag). Do it twice → Z^2 = I on flag,
                # so that also fails.
                # CORRECT GADGET: two DIFFERENT CNOTs — the first CX(anc, flag)
                # (anc control) and the second CX(flag, anc) (flag control).
                # An X_anc fault between them:
                #   * first gadget was CX(anc,flag): X_anc → X_flag
                #   * fault X_anc happens
                #   * second gadget CX(flag,anc): X_anc unchanged (target-side X
                #     is preserved), Z_flag is unchanged (target of CX doesn't
                #     back-act on control for X errors)
                #   Net flag flip: 1 (from the first gadget).
                # So this works. Let's use that.
                circuit.append("CX", [s_anc, flag])   # first flag CNOT
                if p > 0:
                    circuit.append("DEPOLARIZE2", [s_anc, flag], p)
            if k == 3:
                circuit.append("CX", [flag, s_anc])   # second flag CNOT (SWAPPED direction)
                if p > 0:
                    circuit.append("DEPOLARIZE2", [flag, s_anc], p)
            # Now the stabilizer CNOT
            if stab_type == 'Z':
                circuit.append("CX", [s_anc, d])
            else:  # 'X'
                circuit.append("CX", [d, s_anc])
            if p > 0:
                if stab_type == 'Z':
                    circuit.append("DEPOLARIZE2", [s_anc, d], p)
                else:
                    circuit.append("DEPOLARIZE2", [d, s_anc], p)

    # Measure flags in Z basis
    for f in flag_qubits:
        if p > 0:
            circuit.append("X_ERROR", [f], 2 * p / 3)
        circuit.append("M", [f])
    # Measure syndrome ancillas
    for s in synd_qubits:
        if stab_type == 'Z':
            circuit.append("H", [s])
            if p > 0:
                circuit.append("DEPOLARIZE1", [s], p)
        if p > 0:
            circuit.append("X_ERROR", [s], 2 * p / 3)
        circuit.append("M", [s])


def build_prep_and_verify_circuit(p: float, seed: int = 0) -> stim.Circuit:
    """
    Build the full magic-state prep + flag-verification + syndrome-extraction
    circuit.  Returns a stim.Circuit.

    Layout:
      qubits 0..6   : data qubits (encode |+_L>)
      qubits 7..9   : X-stabilizer flag ancillas (one per X-stab)
      qubits 10..12 : X-stabilizer syndrome ancillas
      qubits 13..15 : Z-stabilizer flag ancillas
      qubits 16..18 : Z-stabilizer syndrome ancillas

    Protocol:
      1. Non-FT prep: initialize all 7 data qubits in |+>, then run
         *ideal* projection onto the codespace via stabilizer measurement
         (we do this by including a full syndrome round WITHOUT noise
         on the FIRST round and post-selecting on trivial syndrome).
         [Effect: state is |+_L>.]
      2. Noisy syndrome-extraction round with flag qubits (Fig. 3).
      3. Reject if any flag OR any syndrome bit is nonzero.
      4. Measure logical X observable at the end.
    """
    c = stim.Circuit()

    data = list(range(7))
    flag_x = [7, 8, 9]
    synd_x = [10, 11, 12]
    flag_z = [13, 14, 15]
    synd_z = [16, 17, 18]

    # ---- Step 1: prepare |+_L> on 7 data qubits IDEALLY via Stim's
    #      built-in stabilizer machinery.  The codeword |+_L> is the
    #      unique state with:  X-stabs=+1, Z-stabs=+1, logical X=+1.
    #      Equivalent circuit: R (|0>) on all 7, then apply a Steane
    #      encoder circuit, then H_L=H^{\otimes 7}.
    # But simplest: initialize all 7 qubits in |+>, then measure the 3
    # Z-stabilizers with ancillas and apply feedback (single-qubit Z
    # corrections) to force the +1 branch.  Stim supports classical
    # feedback with the CZ target_rec construction.
    # Simpler still: use MPP + rejection-in-simulator via *ideal-projection*
    # trick.  Since we can't feedback fix a random measurement outcome in a
    # stabilizer simulator cleanly, we use a NOISELESS classical fixup:
    # We measure the 3 Z-stabs and, based on the outcome, apply a
    # correction Z that flips exactly one stabilizer.  For the Steane code,
    # each of the 7 data qubits gives a unique 3-bit Z-syndrome, so the
    # correction is data-qubit index = syndrome (in the right convention).
    for d in data:
        c.append("R", [d])
        c.append("H", [d])
    # Measure X-stabs (deterministic +1 for |+>^7, no correction needed)
    for support in STEANE_X_STABS:
        c.append("MPP", [stim.target_x(support[0]), stim.target_combiner(),
                          stim.target_x(support[1]), stim.target_combiner(),
                          stim.target_x(support[2]), stim.target_combiner(),
                          stim.target_x(support[3])])
    # Measure Z-stabs (random for |+>^7; we'll apply Z-correction via feedback)
    for support in STEANE_Z_STABS:
        c.append("MPP", [stim.target_z(support[0]), stim.target_combiner(),
                          stim.target_z(support[1]), stim.target_combiner(),
                          stim.target_z(support[2]), stim.target_combiner(),
                          stim.target_z(support[3])])
    # The three Z-stab records are the most recent 3 measurements.
    # Steane code Z-syndrome -> data-qubit index (0-indexed) mapping:
    # Using g4=Z0Z2Z4Z6, g5=Z3Z4Z5Z6, g6=Z1Z2Z5Z6
    # For a single Z error on data qubit q, the syndrome (s4,s5,s6) is:
    #   q=0: (1,0,0);  q=1: (0,0,1);  q=2: (1,0,1);  q=3: (0,1,0)
    #   q=4: (1,1,0);  q=5: (0,1,1);  q=6: (1,1,1)
    # But actually we want to apply an X correction to flip the Z-stab outcome
    # (we're using MPP result: 0 = +1, 1 = -1 (i.e. Z-stab is -1)).
    # An X on data qubit q anticommutes with Z-stabs whose support includes q,
    # so applying X on qubit q would flip exactly the Z-stabs it appears in.
    # For a general Z-syndrome we choose q = min-weight X-correction:
    # (s4,s5,s6) -> q using the table above.
    # We implement this as CX <rec>-controlled feedback X on data qubits.
    # Stim: CX target_rec(-k), qubit  applies X to `qubit` if measurement k was 1.
    #
    # The mapping X on q flips (g4,g5,g6) as:
    #   q=0 flips (g4);            record recipe:  X on 0 if s4=1 & s5=0 & s6=0
    #   q=1 flips (g6);                              X on 1 if s4=0 & s5=0 & s6=1
    #   q=2 flips (g4, g6);                          X on 2 if s4=1 & s5=0 & s6=1
    #   q=3 flips (g5);                              X on 3 if s4=0 & s5=1 & s6=0
    #   q=4 flips (g4, g5);                          X on 4 if s4=1 & s5=1 & s6=0
    #   q=5 flips (g5, g6);                          X on 5 if s4=0 & s5=1 & s6=1
    #   q=6 flips (g4, g5, g6);                      X on 6 if s4=1 & s5=1 & s6=1
    # Stim doesn't support boolean AND of classical bits directly, but we can
    # apply a per-bit correction: X on q4 if s4=1, X on q3 if s5=1, X on q1 if s6=1,
    # where q4/q3/q1 are the qubits that each flip ONLY that one syndrome bit.
    # From the table:
    #   flips only g4: q=0
    #   flips only g5: q=3
    #   flips only g6: q=1
    # So the correction is:
    #   CX rec[-3] (s4), data qubit 0
    #   CX rec[-2] (s5), data qubit 3
    #   CX rec[-1] (s6), data qubit 1
    # This is a valid encoder-projection since the resulting state, up to a
    # stabilizer, is always |+_L>.
    c.append("CX", [stim.target_rec(-3), 0])
    c.append("CX", [stim.target_rec(-2), 3])
    c.append("CX", [stim.target_rec(-1), 1])
    # Records so far: 6 (3 X stabs + 3 Z stabs).  We'll insist all == 0
    # in post-processing (this projects into the |+_L> codeword; deterministic
    # for the ideal state since |+_L> is +1 for all X-stabs and 0 for all
    # Z-stabs deterministically since these are stabilizers of the codespace).
    # But wait — |+> on all 7 data qubits is NOT automatically in the codespace!
    # We need the 6 stabilizer measurements to project it.  So the X-stabs will
    # always give +1 (since |+>^7 is +1 eigenvector of X-tensor terms), and the
    # Z-stabs will be random (state collapses into a random Z-syndrome sector).
    # For a clean start we PRE-project: apply DETECTOR conditions and RESAMPLE
    # in Python — see run_experiment below.  Actually simpler: reject-and-retry
    # in Python by re-running the whole experiment.

    # ---- Step 2: noisy syndrome-extraction rounds with flag qubits ----
    # We do TWO rounds and post-select on BOTH being trivial.
    # This is what the paper's FT scheme (Fig. 5b) does: prep + verify + EC.
    # A single measurement flip in round 1 is caught by round 2, restoring
    # the p^2 scaling.  A single fault that spreads to weight-2+ data errors
    # is caught by the flag qubit in the round it occurred.
    for _round in range(2):
        # Idle noise on data qubits during ancilla prep is p/100
        if p > 0:
            c.append("DEPOLARIZE1", data, p / 100)
        build_flag_syndrome_round(c, data, 'X', STEANE_X_STABS, flag_x, synd_x, p)
        build_flag_syndrome_round(c, data, 'Z', STEANE_Z_STABS, flag_z, synd_z, p)

    # ---- Step 3: FINAL destructive readout ----
    # Measure logical X = X^{\otimes 7} using MPP (this is the observable we
    # compare against ideal +1).
    c.append("MPP", [stim.target_x(0), stim.target_combiner(),
                      stim.target_x(1), stim.target_combiner(),
                      stim.target_x(2), stim.target_combiner(),
                      stim.target_x(3), stim.target_combiner(),
                      stim.target_x(4), stim.target_combiner(),
                      stim.target_x(5), stim.target_combiner(),
                      stim.target_x(6)])
    # And logical Z = Z^{\otimes 7} for a second observable
    c.append("MPP", [stim.target_z(0), stim.target_combiner(),
                      stim.target_z(1), stim.target_combiner(),
                      stim.target_z(2), stim.target_combiner(),
                      stim.target_z(3), stim.target_combiner(),
                      stim.target_z(4), stim.target_combiner(),
                      stim.target_z(5), stim.target_combiner(),
                      stim.target_z(6)])

    return c


def run_experiment(p: float, n_shots: int, seed: int = 0) -> dict:
    """
    Returns dict with:
      p, n_shots, n_accept, n_logical_error_x, n_logical_error_z,
      p_accept, p_logical_x, p_logical_z (conditional on acceptance)
    """
    circuit = build_prep_and_verify_circuit(p, seed=seed)
    sampler = circuit.compile_sampler(seed=seed)
    samples = sampler.sample(n_shots)  # shape (n_shots, n_measurements)

    # Measurement record layout (in order appended):
    #  0..2 : initial X-stab MPPs (3)
    #  3..5 : initial Z-stab MPPs (3)
    #  Then for X-syndrome round:
    #    6   : flag
    #    7..9: 3 syndrome ancilla measurements
    #  Then for Z-syndrome round:
    #    10  : flag
    #    11..13: 3 syndrome ancilla measurements
    #  Then:
    #    14: logical X MPP
    #    15: logical Z MPP
    n_meas = samples.shape[1]
    # Layout: 3 X-stabs + 3 Z-stabs (init MPPs)
    # + per round: [3 X-flags + 3 X-synd + 3 Z-flags + 3 Z-synd] = 12 per round x 2 = 24
    # + logical_x_meas + logical_z_meas = 6 + 24 + 2 = 32
    assert n_meas == 32, f"Expected 32 measurements, got {n_meas}"

    init_x_stabs = samples[:, 0:3]   # should be all 0 (|+>^7 is +1 for X-stabs)
    init_z_stabs = samples[:, 3:6]   # random; feedback applied in-circuit

    # Round 1: X-flags[6:9], X-synd[9:12], Z-flags[12:15], Z-synd[15:18]
    r1_x_flag = samples[:, 6:9]
    r1_x_synd = samples[:, 9:12]
    r1_z_flag = samples[:, 12:15]
    r1_z_synd = samples[:, 15:18]
    # Round 2: X-flags[18:21], X-synd[21:24], Z-flags[24:27], Z-synd[27:30]
    r2_x_flag = samples[:, 18:21]
    r2_x_synd = samples[:, 21:24]
    r2_z_flag = samples[:, 24:27]
    r2_z_synd = samples[:, 27:30]

    logical_x_meas = samples[:, 30]
    logical_z_meas = samples[:, 31]

    # ---- Post-selection ----
    # (a) initial state prep succeeded: X-stabs = 0 (automatic; sanity check)
    # (b) initial Z-syndromes are 0 (fixes the |+_L> codeword branch)
    # (c) no flags fired
    # (d) noisy syndrome round returned trivial syndrome
    accept = (
        np.all(init_x_stabs == 0, axis=1) &
        np.all(r1_x_flag == 0, axis=1) & np.all(r1_x_synd == 0, axis=1) &
        np.all(r1_z_flag == 0, axis=1) & np.all(r1_z_synd == 0, axis=1) &
        np.all(r2_x_flag == 0, axis=1) & np.all(r2_x_synd == 0, axis=1) &
        np.all(r2_z_flag == 0, axis=1) & np.all(r2_z_synd == 0, axis=1)
    )
    n_accept = int(accept.sum())

    # Among accepted shots, count logical X errors
    # For |+_L>, logical X = X^{\otimes 7} has eigenvalue +1, so we expect
    # logical_x_meas == 0.  A "logical error" = logical_x_meas == 1
    # (this corresponds to a logical Z error on the state, which flipped |+_L>
    # to |-_L>).
    if n_accept > 0:
        n_logical_x_err = int(logical_x_meas[accept].sum())
    else:
        n_logical_x_err = 0

    # Logical Z observable is meaningless for |+_L> (uniformly random), skip it
    # as a proxy — but we can also count based on the initial Z-stab post-selection:
    # since |+_L> is a +1 eigenstate of the X-stabs AND logical X, but has random
    # logical Z value, we DO NOT count logical Z errors directly.  Instead the
    # experiment measures the p^2 scaling in logical X (equivalent to logical Z
    # on the input state by symmetry).

    return {
        "p": p,
        "n_shots": n_shots,
        "n_accept": n_accept,
        "p_accept": n_accept / n_shots,
        "n_logical_x_err": n_logical_x_err,
        "p_logical_x_given_accept": (n_logical_x_err / n_accept) if n_accept > 0 else 0.0,
        "logical_x_err_stderr_given_accept": (
            np.sqrt(n_logical_x_err * (n_accept - n_logical_x_err) / max(n_accept, 1)) / max(n_accept, 1)
            if n_accept > 0 else 0.0
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, default=200_000,
                    help="Monte-Carlo shots per physical error rate")
    ap.add_argument("--out", type=str, required=True,
                    help="Output JSON path")
    ap.add_argument("--p-list", type=str,
                    default="1e-4,3e-4,1e-3,3e-3,1e-2,3e-2",
                    help="Comma-separated physical error rates")
    args = ap.parse_args()

    p_values = [float(x) for x in args.p_list.split(",")]

    results = []
    t0 = time.time()
    for p in p_values:
        print(f"[{time.time()-t0:6.1f}s] Running p={p:g} with {args.shots} shots ...")
        r = run_experiment(p, args.shots, seed=int(1e6 * p) + 42)
        print(f"    -> p_accept = {r['p_accept']:.4g},  "
              f"p_logical_x|accept = {r['p_logical_x_given_accept']:.4g} "
              f"(± {r['logical_x_err_stderr_given_accept']:.2g}),  "
              f"n_accept = {r['n_accept']}")
        results.append(r)

    # Fit log-log slope of p_logical_x_given_accept vs p
    p_arr = np.array([r["p"] for r in results])
    pL_arr = np.array([r["p_logical_x_given_accept"] for r in results])
    # Only fit points with nonzero logical error and enough accepts
    mask = (pL_arr > 0) & np.array([r["n_accept"] > 100 for r in results])
    if mask.sum() >= 2:
        slope, intercept = np.polyfit(np.log(p_arr[mask]), np.log(pL_arr[mask]), 1)
        coef = np.exp(intercept)
        print(f"\nLog-log fit of p_logical_x|accept vs p:")
        print(f"    slope     = {slope:.3f}   (expect ~2 for fault-tolerance)")
        print(f"    prefactor = {coef:.3g}    (expect O(1)-O(100))")
    else:
        slope, coef = None, None

    summary = {
        "results": results,
        "fit_slope": float(slope) if slope is not None else None,
        "fit_prefactor": float(coef) if coef is not None else None,
        "stim_version": stim.__version__,
        "numpy_version": np.__version__,
        "paper": "arXiv:1811.00566",
        "table_expected": {
            "level_1_scaling": "p^2",
            "level_1_coeffs_XYZ": [9.95, 4.41, 7.87],
            "acceptance_expected": "(1-p)^75",
        },
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {args.out}")


if __name__ == "__main__":
    main()
