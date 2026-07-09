#!/usr/bin/env python3
"""
Independent replication of the HBAC (Heat-Bath Algorithmic Cooling) core numerical
claims from Park et al. 2015, arXiv:1501.00082 (QINP paper on hyperfine spin qubits
in irradiated malonic acid).

Reproduces:
  C1: 3-qubit PPA first-round polarization = 1.5*eps_b - 0.5*eps_b^3
  C2: 3-qubit PPA asymptotic polarization  -> 2*eps_b   (weak-eps limit)
  C3: General PPA asymptote for n system qubits used in compression:
        eps_th = eps_b * 2^(n-2)   for eps_b << 2^-n
        eps_th -> ~1                for eps_b >> 2^-n
  C4: Closed-system (Shannon / reversible) upper bound on the target polarization
      is bounded and is _exceeded_ once bath resets are permitted.

Method: pure numpy density-matrix simulation. No hardware, no Lindblad/T1-T2
imperfections (the paper's Sec. 5 splits "theory" (ideal) from "with relaxation"
plots; we reproduce the theory curves, since the replication brief calls for the
analytical / ideal-PPA numbers, not the GRAPE-pulse-limited experimental
projections).

Density-matrix convention:
  - Each spin is a qubit with Hamiltonian H = -1/2 * eps * Z  (up more populated).
  - Thermal state at bath polarization eps:  rho = (I - eps*Z)/2 ... this puts
    <Z> = -eps but conventional "polarization" here = P(|0>) - P(|1>) = eps.
    We use rho = (I + eps*Z)/2 so that <Z> = +eps and |0>(up) is the majority state.
  - Target polarization after each round = <Z>_target = Tr(rho_target * Z).
  - PPA compression = permutation of the diagonal entries of the full density matrix
    into non-increasing order (paper Sec. 5, ref [18,42]).
"""

import json
import os
import sys
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# -------------------- Single-qubit thermal state --------------------

def thermal_1q(eps):
    """Diagonal thermal state at polarization eps: p(|0>)=(1+eps)/2, p(|1>)=(1-eps)/2."""
    return np.array([(1 + eps) / 2.0, (1 - eps) / 2.0])


def kron_diag(*diagonals):
    """Kronecker product of diagonal vectors (returns 1-D of length prod)."""
    out = np.array([1.0])
    for d in diagonals:
        out = np.kron(out, d)
    return out


# -------------------- Polarization measurement --------------------

def polarization_of_qubit(diag, n_qubits, target_idx):
    """
    Given full diagonal (length 2^n_qubits, ordering |q0 q1 ... q_{n-1}>),
    return <Z_target> = P(target=|0>) - P(target=|1>).
    """
    d = 2 ** n_qubits
    z_diag = np.empty(d)
    for i in range(d):
        # bit for target_idx: MSB = qubit index 0 (matches np.kron ordering)
        bit = (i >> (n_qubits - 1 - target_idx)) & 1
        z_diag[i] = 1.0 if bit == 0 else -1.0
    return float(np.sum(diag * z_diag))


# -------------------- PPA compression: diagonal sort --------------------

def ppa_compression(diag):
    """
    PPA compression = permutation that rearranges the diagonal of the density matrix
    in non-increasing order (paper text + Refs [18,42]: Boykin/Mor/Roychowdhury,
    Schulman-Vazirani, Fernandez-Mor-Weinstein).
    """
    return np.sort(diag)[::-1]


# -------------------- Bath reset --------------------

def reset_qubit_to_bath(diag, n_qubits, reset_idx, eps_b):
    """
    Replace the reduced state of `reset_idx` with the thermal bath state at
    polarization eps_b, assuming no correlations with the rest (product-state
    reset: valid for the PPA idealization).

    Because ideal PPA assumes the reset is a full thermalization and the paper
    treats the compressed diagonal as separable in the PPA idealization (all
    off-diagonals are zero by construction, and the compression itself is a
    permutation that keeps the state classical), we trace out the reset qubit,
    then tensor a fresh thermal reset qubit in the same slot.
    """
    d = 2 ** n_qubits
    n_others = n_qubits - 1

    # Compute reduced diagonal of the other qubits by marginalizing over reset bit.
    reduced = np.zeros(2 ** n_others)
    for i in range(d):
        bits = [(i >> (n_qubits - 1 - k)) & 1 for k in range(n_qubits)]
        other_bits = [b for k, b in enumerate(bits) if k != reset_idx]
        j = 0
        for b in other_bits:
            j = (j << 1) | b
        reduced[j] += diag[i]

    # Fresh thermal reset qubit.
    p_up = (1 + eps_b) / 2.0
    p_dn = (1 - eps_b) / 2.0

    # Re-embed as product with reset in slot `reset_idx`.
    new = np.zeros(d)
    for i in range(d):
        bits = [(i >> (n_qubits - 1 - k)) & 1 for k in range(n_qubits)]
        reset_bit = bits[reset_idx]
        other_bits = [b for k, b in enumerate(bits) if k != reset_idx]
        j = 0
        for b in other_bits:
            j = (j << 1) | b
        new[i] = reduced[j] * (p_up if reset_bit == 0 else p_dn)
    return new


# -------------------- HBAC / PPA simulation --------------------

def run_ppa(n_qubits, eps_b, n_rounds, target_idx=0, reset_idx=None,
            initial="thermal"):
    """
    Run n_rounds of the Partner-Pairing Algorithm on n_qubits with a single
    bath-thermalizing reset qubit. The compression uses all n_qubits (i.e.
    system size in the paper's sense of "n system qubits used in the compression
    step" -> for the 3-qubit case n = 3).

    Returns list of length n_rounds+1 with target polarization at each round
    (index 0 = initial polarization).
    """
    if reset_idx is None:
        reset_idx = n_qubits - 1  # last qubit is the reset

    # Initial state: all qubits at thermal eps_b (paper Sec 5 assumes nuclei
    # first swapped up to the electron bath polarization).
    if initial == "thermal":
        diag = kron_diag(*[thermal_1q(eps_b) for _ in range(n_qubits)])
    elif initial == "mixed":
        diag = np.ones(2 ** n_qubits) / (2 ** n_qubits)
    else:
        raise ValueError(initial)

    hist = [polarization_of_qubit(diag, n_qubits, target_idx)]

    for _r in range(n_rounds):
        # Compression: sort diagonal in non-increasing order.
        diag = ppa_compression(diag)
        # Reset: re-thermalize the reset qubit to the bath at eps_b.
        diag = reset_qubit_to_bath(diag, n_qubits, reset_idx, eps_b)
        hist.append(polarization_of_qubit(diag, n_qubits, target_idx))

    return hist


# -------------------- Closed-system Shannon bound --------------------

def shannon_bound_target_polarization(n_qubits, eps_b):
    """
    Closed-system (unitary) bound: max target polarization achievable with a
    single unitary compression on n_qubits all initially at eps_b, i.e. sort
    the initial thermal diagonal into non-increasing order (PPA compression
    once, WITHOUT any subsequent bath reset).

    This is the exact maximum <Z_target> reachable by any unitary on the
    starting product-thermal state (proof: any unitary permutes eigenvalues +
    unitary rotation on eigenbasis; for a computational-basis target measurement
    the optimum is the sorting permutation).
    """
    diag = kron_diag(*[thermal_1q(eps_b) for _ in range(n_qubits)])
    diag = ppa_compression(diag)
    return polarization_of_qubit(diag, n_qubits, target_idx=0)


# -------------------- Experiments --------------------

def experiment_first_round_3q(eps_b_list):
    """C1: first-round polarization vs paper formula 1.5*eps - 0.5*eps^3."""
    rows = []
    for eps_b in eps_b_list:
        hist = run_ppa(n_qubits=3, eps_b=eps_b, n_rounds=1)
        sim = hist[1]
        paper = 1.5 * eps_b - 0.5 * eps_b ** 3
        rel = abs(sim - paper) / abs(paper) if paper != 0 else 0.0
        rows.append({"eps_b": eps_b, "sim_first_round": sim,
                     "paper_formula_1p5e_minus_0p5e3": paper,
                     "rel_err": rel})
    return rows


def experiment_asymptote_3q(eps_b_list, n_rounds=40):
    """C2: 3-qubit asymptote -> 2*eps_b for weak eps."""
    rows = []
    for eps_b in eps_b_list:
        hist = run_ppa(n_qubits=3, eps_b=eps_b, n_rounds=n_rounds)
        asym = hist[-1]
        paper = 2.0 * eps_b
        rel = abs(asym - paper) / abs(paper) if paper != 0 else 0.0
        rows.append({"eps_b": eps_b, "sim_asymptote": asym,
                     "paper_asymptote_2eps": paper,
                     "rel_err": rel, "n_rounds": n_rounds})
    return rows


def experiment_scaling_n(n_list, eps_b, n_rounds=60):
    """
    C3: asymptote scales as eps_b * 2^(n-2) for weak eps_b (paper text just
    before Sec 5.1). Compression uses all n qubits.
    """
    rows = []
    for n in n_list:
        hist = run_ppa(n_qubits=n, eps_b=eps_b, n_rounds=n_rounds)
        asym = hist[-1]
        paper = eps_b * 2 ** (n - 2)
        # Predicted only valid while paper's regime eps_b << 2^-n holds AND
        # asym < 1. We report both regimes.
        weak_regime = eps_b < 2.0 ** (-n)
        rel = abs(asym - paper) / abs(paper) if paper != 0 else 0.0
        rows.append({"n_qubits": n, "eps_b": eps_b, "sim_asymptote": asym,
                     "paper_weak_asymptote_eps_2n2": paper,
                     "weak_regime": weak_regime, "rel_err_weak_formula": rel})
    return rows


def experiment_shannon_violation(n_qubits, eps_b, n_rounds=40):
    """
    C4: Shannon (closed-system) bound is exceeded by open-bath HBAC.
    """
    shannon = shannon_bound_target_polarization(n_qubits, eps_b)
    hist = run_ppa(n_qubits=n_qubits, eps_b=eps_b, n_rounds=n_rounds)
    ppa_asym = hist[-1]
    return {"n_qubits": n_qubits, "eps_b": eps_b,
            "shannon_closed_bound": shannon,
            "ppa_open_bath_asymptote": ppa_asym,
            "ratio_open_over_closed": ppa_asym / shannon if shannon > 0 else None,
            "shannon_violated": ppa_asym > shannon + 1e-12}


def experiment_full_curve_3q(eps_b, n_rounds=10):
    """Full per-round curve, matching Fig. 7's x-axis (rounds 1..9 of paper)."""
    hist = run_ppa(n_qubits=3, eps_b=eps_b, n_rounds=n_rounds)
    return {"eps_b": eps_b, "polarization_per_round": hist,
            "ratio_pol_over_eps_b_per_round": [h / eps_b for h in hist]}


# -------------------- Main --------------------

def main():
    eps_b_paper = 8e-4   # paper Sec 5.1: room-temp electron polarization
    results = {
        "paper": "arXiv:1501.00082 (Park et al. 2015)",
        "eps_b_used_from_paper": eps_b_paper,
        "note": "Idealized PPA density-matrix simulation. Reproduces analytical "
                "HBAC claims of paper Sec 5 (no T1/T2 relaxation modeled; "
                "those are the paper's 'theory' curves in Fig 7,10,11).",
    }

    # C1: first-round 3-qubit vs 1.5 eps - 0.5 eps^3
    results["C1_first_round_3q"] = experiment_first_round_3q(
        [1e-4, 8e-4, 1e-3, 1e-2, 1e-1])

    # C2: 3-qubit asymptote -> 2 eps
    results["C2_asymptote_3q"] = experiment_asymptote_3q(
        [1e-4, 8e-4, 1e-3, 1e-2, 1e-1], n_rounds=60)

    # C3: scaling with n system qubits
    results["C3_scaling_n_qubits"] = experiment_scaling_n(
        n_list=[3, 4, 5, 6, 7], eps_b=eps_b_paper, n_rounds=200)

    # C4: Shannon-bound violation (3-, 5-qubit).
    results["C4_shannon_violation"] = [
        experiment_shannon_violation(3, eps_b_paper, n_rounds=60),
        experiment_shannon_violation(5, eps_b_paper, n_rounds=200),
    ]

    # Full curve for 3-qubit matching Fig 7 (paper eps_b).
    results["fig7_like_curve_3q"] = experiment_full_curve_3q(
        eps_b_paper, n_rounds=15)

    # Also do curves at a range of eps_b for a plot.
    curves = {}
    for eps_b in [1e-3, 1e-2, 1e-1]:
        curves[f"eps_b={eps_b}"] = experiment_full_curve_3q(eps_b, n_rounds=15)
    results["curves_3q_various_eps"] = curves

    out_json = os.path.join(OUT_DIR, "hbac_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[ok] wrote {out_json}")

    # Console summary.
    print("\n=== C1: 3-qubit first-round vs paper 1.5*eps - 0.5*eps^3 ===")
    for r in results["C1_first_round_3q"]:
        print(f"  eps_b={r['eps_b']:.1e}  sim={r['sim_first_round']:.6e}  "
              f"paper={r['paper_formula_1p5e_minus_0p5e3']:.6e}  "
              f"rel_err={r['rel_err']:.2e}")

    print("\n=== C2: 3-qubit asymptote -> 2*eps_b ===")
    for r in results["C2_asymptote_3q"]:
        print(f"  eps_b={r['eps_b']:.1e}  sim_asym={r['sim_asymptote']:.6e}  "
              f"paper_2eps={r['paper_asymptote_2eps']:.6e}  "
              f"rel_err={r['rel_err']:.2e}")

    print("\n=== C3: scaling eps_b*2^(n-2) at eps_b=8e-4 ===")
    for r in results["C3_scaling_n_qubits"]:
        print(f"  n={r['n_qubits']}  sim_asym={r['sim_asymptote']:.6e}  "
              f"weak_pred={r['paper_weak_asymptote_eps_2n2']:.6e}  "
              f"weak_regime={r['weak_regime']}  "
              f"rel_err={r['rel_err_weak_formula']:.2e}")

    print("\n=== C4: Shannon bound violation ===")
    for r in results["C4_shannon_violation"]:
        print(f"  n={r['n_qubits']}  Shannon={r['shannon_closed_bound']:.4e}  "
              f"PPA_open={r['ppa_open_bath_asymptote']:.4e}  "
              f"ratio={r['ratio_open_over_closed']:.3f}  "
              f"violated={r['shannon_violated']}")

    print("\n=== Fig 7 like curve (eps_b=8e-4) ratio eps_c/eps_b per round ===")
    ratios = results["fig7_like_curve_3q"]["ratio_pol_over_eps_b_per_round"]
    for r_idx, ratio in enumerate(ratios):
        print(f"  round {r_idx}: eps_c/eps_b = {ratio:.4f}")


if __name__ == "__main__":
    main()
