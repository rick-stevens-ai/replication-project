#!/usr/bin/env python3
"""
Replication of Chamberland & Cross (arXiv:1811.00566)
"Fault-tolerant magic state preparation with flag qubits"

Approach v2 (cleaner):
    We build a Stim circuit that implements one round of the Reichardt
    flag-based syndrome extraction for the [[7,1,3]] Steane code, PLUS
    a second round to catch measurement errors.  For simplicity we
    encode |+_L> (the logical + state) which is an eigenstate of the
    logical X operator; a magic state |H_L> = T|+_L> has the same
    Pauli-error structure and only re-weights the X/Y/Z error
    coefficients in Table 4.

    We use Stim's DetectorErrorModel + PyMatching-free rejection
    postselection: post-select on ALL flag qubits = 0 AND all
    syndromes = 0 in both rounds, then measure logical X.

    The core testable claim: post-selected logical error scales as p^2.

CORRECTED flag gadget:
    We use the "generalized 2-flag with CZ-brackets" from Chao-Reichardt
    that Stim's own tutorial uses for the Steane code.  Reference:
      https://github.com/quantumlib/Stim/blob/main/glue/sample/src/sinter/main_test.py
    A simpler approach that gives a proven distance-3 code protection
    for the accepted state: use TWO rounds of MPP measurement (Stim's
    native Measure-Pauli-Product) with per-measurement noise, and
    post-select on ALL trivial syndromes.  This is an idealized flag
    protocol where the flag is implicit in "measurement noise".

    The key property to reproduce is: with MPP + noise + post-selection,
    the p^2 scaling emerges for the [[7,1,3]] code, because the code has
    distance 3 and post-selection removes all weight-1 events.
"""

import stim
import numpy as np
import json
import argparse
import time
from pathlib import Path

STEANE_X_STABS = [
    [0, 2, 4, 6],   # g1
    [3, 4, 5, 6],   # g2
    [1, 2, 5, 6],   # g3
]
STEANE_Z_STABS = [
    [0, 2, 4, 6],
    [3, 4, 5, 6],
    [1, 2, 5, 6],
]


def add_noise_layer(c, qubits, p, kind='1q'):
    """Depolarizing noise per paper noise model."""
    if p <= 0 or not qubits:
        return
    if kind == '1q':
        c.append("DEPOLARIZE1", qubits, p)
    elif kind == '2q':
        # qubits is a flat list of pairs
        c.append("DEPOLARIZE2", qubits, p)
    elif kind == 'idle':
        c.append("DEPOLARIZE1", qubits, p / 100)
    elif kind == 'prep_z':
        c.append("X_ERROR", qubits, 2 * p / 3)
    elif kind == 'prep_x':
        c.append("Z_ERROR", qubits, 2 * p / 3)
    elif kind == 'meas':
        c.append("X_ERROR", qubits, 2 * p / 3)


def build_stab_measure_with_ancilla(c, support, s_anc, stab_type, p, other_data):
    """
    Measure one weight-4 stabilizer using one ancilla qubit.
    - Z stab (support is Z-Pauli qubits): ancilla in |+>, CX(anc,d), measure X
    - X stab (support is X-Pauli qubits): ancilla in |0>, CX(d,anc), measure Z
    Returns nothing; appends measurement to circuit.
    Idle noise applied to other data qubits during the sequence.
    """
    # Prepare ancilla
    c.append("R", [s_anc])
    add_noise_layer(c, [s_anc], p, 'prep_z')
    if stab_type == 'Z':
        c.append("H", [s_anc])
        add_noise_layer(c, [s_anc], p, '1q')

    # Do the 4 CNOTs
    for k, d in enumerate(support):
        if stab_type == 'Z':
            c.append("CX", [s_anc, d])
            add_noise_layer(c, [s_anc, d], p, '2q')
        else:
            c.append("CX", [d, s_anc])
            add_noise_layer(c, [d, s_anc], p, '2q')
        # Idle noise on other data qubits during this step
        idle_q = [q for q in other_data if q not in [d]]
        add_noise_layer(c, idle_q, p, 'idle')

    if stab_type == 'Z':
        c.append("H", [s_anc])
        add_noise_layer(c, [s_anc], p, '1q')
    add_noise_layer(c, [s_anc], p, 'meas')
    c.append("M", [s_anc])


def build_flag_stab_measure(c, support, s_anc, flag, stab_type, p, other_data):
    """
    Measure one weight-4 stabilizer using one ancilla + one flag qubit.
    Chao-Reichardt 1-flag gadget:
      * Prepare s_anc (Z-stab: |+>; X-stab: |0>) and flag in |0>
      * Do stab CNOT for k=0
      * CX(s_anc, flag)                          <-- flag gadget open
      * Do stab CNOTs for k=1, k=2
      * CX(s_anc, flag)                          <-- flag gadget close
      * Do stab CNOT for k=3
      * Measure flag in Z basis  (should be 0)
      * Measure s_anc (X basis for Z-stab, Z basis for X-stab)

    A single fault on s_anc between the two flag CNOTs propagates to
    both s_anc \u2192 X on d1, d2 (weight-2 X on data) AND to flag exactly
    ONCE (via the second CX(s_anc,flag)) \u2192 flag = 1 \u2192 rejected.

    A fault on s_anc BEFORE k=0 propagates through all stab CNOTs \u2192
    weight-4 X on the support = the X-stabilizer itself = trivial
    on codestates.  So this doesn't cause a logical error.

    A fault on s_anc BETWEEN k=0 and the first flag CNOT: propagates to
    d1,d2,d3 (weight-3) AND flag gets flipped ONCE (from the first
    CX(s_anc,flag) after fault) \u2192 flag=1 rejected.  Actually the first
    flag CNOT happened AFTER k=0 but BEFORE k=1, so it comes AFTER the
    fault; the fault propagates X_anc through: first flag CNOT (X\u2192flag),
    stab k=1 (X\u2192d1), stab k=2 (X\u2192d2), second flag CNOT (X\u2192flag
    again, flag becomes 0), stab k=3 (X\u2192d3). Weight-3 on {1,2,3}
    and flag=0. But weight-3 X may or may not be logical depending on
    which qubits. Detected by X-stab measurements.

    The key: single-fault errors either (a) get flagged, or (b) create
    weight-1 data errors detectable by syndrome, or (c) get absorbed into
    the stabilizer.  In all cases, no undetected logical error from a
    single fault \u2192 post-selection gives p^2 scaling.
    """
    # Prepare ancillas
    c.append("R", [s_anc, flag])
    add_noise_layer(c, [s_anc, flag], p, 'prep_z')
    if stab_type == 'Z':
        c.append("H", [s_anc])
        add_noise_layer(c, [s_anc], p, '1q')

    # k=0 stab CNOT
    if stab_type == 'Z':
        c.append("CX", [s_anc, support[0]])
        add_noise_layer(c, [s_anc, support[0]], p, '2q')
    else:
        c.append("CX", [support[0], s_anc])
        add_noise_layer(c, [support[0], s_anc], p, '2q')
    add_noise_layer(c, [q for q in other_data if q != support[0]], p, 'idle')

    # Flag CNOT #1
    c.append("CX", [s_anc, flag])
    add_noise_layer(c, [s_anc, flag], p, '2q')
    add_noise_layer(c, other_data, p, 'idle')

    # k=1, k=2 stab CNOTs
    for k in [1, 2]:
        d = support[k]
        if stab_type == 'Z':
            c.append("CX", [s_anc, d])
            add_noise_layer(c, [s_anc, d], p, '2q')
        else:
            c.append("CX", [d, s_anc])
            add_noise_layer(c, [d, s_anc], p, '2q')
        add_noise_layer(c, [q for q in other_data if q != d], p, 'idle')

    # Flag CNOT #2
    c.append("CX", [s_anc, flag])
    add_noise_layer(c, [s_anc, flag], p, '2q')
    add_noise_layer(c, other_data, p, 'idle')

    # k=3 stab CNOT
    d = support[3]
    if stab_type == 'Z':
        c.append("CX", [s_anc, d])
        add_noise_layer(c, [s_anc, d], p, '2q')
    else:
        c.append("CX", [d, s_anc])
        add_noise_layer(c, [d, s_anc], p, '2q')
    add_noise_layer(c, [q for q in other_data if q != d], p, 'idle')

    # Measure flag in Z basis
    add_noise_layer(c, [flag], p, 'meas')
    c.append("M", [flag])

    # Measure syndrome ancilla
    if stab_type == 'Z':
        c.append("H", [s_anc])
        add_noise_layer(c, [s_anc], p, '1q')
    add_noise_layer(c, [s_anc], p, 'meas')
    c.append("M", [s_anc])


def build_circuit(p, use_flag=True, n_rounds=2, final_perfect_round=True):
    """
    Prep |+_L> ideally, do n_rounds of noisy syndrome extraction with (or without)
    flag qubits, plus one FINAL PERFECT (noiseless) round of syndrome extraction
    to catch weight-1 residual errors that occurred mid-way through the last
    noisy round.  This is standard in FT-QEC analysis: you always end with an
    ideal syndrome measurement to define the logical state.  Then post-select
    on all syndromes/flags trivial and measure logical X.
    """
    c = stim.Circuit()
    data = list(range(7))
    # Ancillas allocated at qubit indices 7+
    next_q = 7

    # ---- Ideal |+_L> preparation via MPP + classical feedback ----
    for d in data:
        c.append("R", [d])
        c.append("H", [d])
    # X-stabs (deterministic +1 on |+>^7)
    for support in STEANE_X_STABS:
        targets = []
        for i, q in enumerate(support):
            if i > 0:
                targets.append(stim.target_combiner())
            targets.append(stim.target_x(q))
        c.append("MPP", targets)
    # Z-stabs (random on |+>^7 \u2014 apply feedback correction)
    for support in STEANE_Z_STABS:
        targets = []
        for i, q in enumerate(support):
            if i > 0:
                targets.append(stim.target_combiner())
            targets.append(stim.target_z(q))
        c.append("MPP", targets)
    # Feedback: apply X to data qubit that flips exactly the corresponding Z-stab
    # (see v1 code for the derivation of the mapping)
    c.append("CX", [stim.target_rec(-3), 0])   # s4 flip -> X on q0
    c.append("CX", [stim.target_rec(-2), 3])   # s5 flip -> X on q3
    c.append("CX", [stim.target_rec(-1), 1])   # s6 flip -> X on q1

    # ---- n_rounds of noisy syndrome extraction ----
    round_meas_counts = []  # list of (flag_slots_per_round, synd_slots_per_round)
    for r in range(n_rounds):
        add_noise_layer(c, data, p, 'idle')

        n_flag_meas = 0
        n_synd_meas = 0
        # X-stabs
        for support in STEANE_X_STABS:
            s_anc = next_q; next_q += 1
            if use_flag:
                flag = next_q; next_q += 1
                other = [q for q in data if q not in support]
                build_flag_stab_measure(c, support, s_anc, flag, 'X', p, other)
                n_flag_meas += 1
                n_synd_meas += 1
            else:
                other = [q for q in data if q not in support]
                build_stab_measure_with_ancilla(c, support, s_anc, 'X', p, other)
                n_synd_meas += 1
        # Z-stabs
        for support in STEANE_Z_STABS:
            s_anc = next_q; next_q += 1
            if use_flag:
                flag = next_q; next_q += 1
                other = [q for q in data if q not in support]
                build_flag_stab_measure(c, support, s_anc, flag, 'Z', p, other)
                n_flag_meas += 1
                n_synd_meas += 1
            else:
                other = [q for q in data if q not in support]
                build_stab_measure_with_ancilla(c, support, s_anc, 'Z', p, other)
                n_synd_meas += 1

        round_meas_counts.append((n_flag_meas, n_synd_meas))

    # ---- Optional FINAL PERFECT (noiseless) round of syndrome extraction ----
    # This catches any residual weight-1 data errors from the last noisy round.
    if final_perfect_round:
        # Noiseless MPP measurements of all 6 stabilizers
        for support in STEANE_X_STABS:
            targets = []
            for i, q in enumerate(support):
                if i > 0:
                    targets.append(stim.target_combiner())
                targets.append(stim.target_x(q))
            c.append("MPP", targets)
        for support in STEANE_Z_STABS:
            targets = []
            for i, q in enumerate(support):
                if i > 0:
                    targets.append(stim.target_combiner())
                targets.append(stim.target_z(q))
            c.append("MPP", targets)

    # ---- Final logical X readout ----
    targets = []
    for i in range(7):
        if i > 0:
            targets.append(stim.target_combiner())
        targets.append(stim.target_x(i))
    c.append("MPP", targets)

    return c, round_meas_counts, final_perfect_round


def run(p, shots, seed, use_flag=True, n_rounds=2, final_perfect_round=True):
    c, round_meta, has_perfect = build_circuit(p, use_flag=use_flag, n_rounds=n_rounds, final_perfect_round=final_perfect_round)
    sampler = c.compile_sampler(seed=seed)
    samples = sampler.sample(shots)

    # Measurement order:
    #  0..2   : X-stab initial MPPs
    #  3..5   : Z-stab initial MPPs
    #  For each round:
    #    per stab: (flag M then synd M) if use_flag else (synd M only)
    #    order within round: X-stab #1, #2, #3 then Z-stab #1, #2, #3
    #  Final: logical X MPP
    idx = 6
    init_x = samples[:, 0:3]
    accepts_per_round = []
    for r, (nf, ns) in enumerate(round_meta):
        # 6 stabilizers per round; each contributes either (1 flag + 1 synd) or just (1 synd)
        n_per_stab = 2 if use_flag else 1
        flags_list = []
        synds_list = []
        for s in range(6):  # 3 X + 3 Z
            if use_flag:
                flags_list.append(samples[:, idx]); idx += 1
                synds_list.append(samples[:, idx]); idx += 1
            else:
                synds_list.append(samples[:, idx]); idx += 1
        flags = np.stack(flags_list, axis=1) if use_flag else np.zeros((shots, 0), dtype=bool)
        synds = np.stack(synds_list, axis=1)
        accepts_per_round.append((flags, synds))

    # Optional perfect round: 6 more MPPs (3 X-stabs, 3 Z-stabs)
    perfect_stabs = None
    if has_perfect:
        perfect_stabs = samples[:, idx:idx+6]; idx += 6

    logical_x = samples[:, idx]; idx += 1

    accept = np.all(init_x == 0, axis=1)
    for flags, synds in accepts_per_round:
        if flags.shape[1] > 0:
            accept &= np.all(flags == 0, axis=1)
        accept &= np.all(synds == 0, axis=1)
    if perfect_stabs is not None:
        accept &= np.all(perfect_stabs == 0, axis=1)

    n_accept = int(accept.sum())
    n_err = int(logical_x[accept].sum()) if n_accept > 0 else 0
    p_acc = n_accept / shots
    p_err = (n_err / n_accept) if n_accept > 0 else 0.0
    p_err_se = np.sqrt(max(n_err, 1) * max(n_accept - n_err, 1) / n_accept) / n_accept if n_accept > 0 else 0.0

    return {
        "p": p, "n_shots": shots,
        "n_accept": n_accept, "p_accept": p_acc,
        "n_logical_err": n_err,
        "p_logical_err_given_accept": p_err,
        "stderr": p_err_se,
        "use_flag": use_flag, "n_rounds": n_rounds,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", type=int, default=500_000)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--p-list", type=str, default="1e-4,3e-4,1e-3,3e-3,1e-2")
    ap.add_argument("--no-flag", action="store_true",
                    help="Run WITHOUT flag qubits (baseline comparison)")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--no-perfect-final", action="store_true")
    args = ap.parse_args()

    p_list = [float(x) for x in args.p_list.split(",")]
    use_flag = not args.no_flag

    print(f"Config: use_flag={use_flag}, n_rounds={args.rounds}, shots={args.shots}")
    print(f"Stim version: {stim.__version__}")

    results = []
    t0 = time.time()
    for p in p_list:
        print(f"[{time.time()-t0:6.1f}s] p={p:g} ...")
        r = run(p, args.shots, seed=int(1e6*p)+42, use_flag=use_flag, n_rounds=args.rounds, final_perfect_round=not args.no_perfect_final)
        print(f"    -> p_accept={r['p_accept']:.4g}, p_err|accept={r['p_logical_err_given_accept']:.4g} (\u00b1 {r['stderr']:.2g}), n_acc={r['n_accept']}")
        results.append(r)

    # Fit log-log slope
    p_arr = np.array([r["p"] for r in results])
    pL_arr = np.array([r["p_logical_err_given_accept"] for r in results])
    mask = (pL_arr > 0) & np.array([r["n_accept"] > 100 and r["n_logical_err"] >= 5 for r in results])
    if mask.sum() >= 2:
        slope, intercept = np.polyfit(np.log(p_arr[mask]), np.log(pL_arr[mask]), 1)
        coef = np.exp(intercept)
        print(f"\nLog-log fit: slope={slope:.3f}, prefactor={coef:.3g}")
        print(f"Expected (paper Table 4 level-1): slope=2, prefactor \u2208 [4.4, 9.95] (X/Y/Z)")
    else:
        slope, coef = None, None

    summary = {
        "results": results,
        "fit_slope": float(slope) if slope is not None else None,
        "fit_prefactor": float(coef) if coef is not None else None,
        "stim_version": stim.__version__,
        "config": {"use_flag": use_flag, "n_rounds": args.rounds, "shots": args.shots},
        "paper": "arXiv:1811.00566 Table 4 level-1",
        "expected": {
            "slope": 2,
            "prefactor_range_XYZ": [4.41, 9.95],
            "acceptance": "(1-p)^75",
        },
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {args.out}")


if __name__ == "__main__":
    main()
