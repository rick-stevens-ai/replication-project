#!/usr/bin/env python3
"""
Independent replication of core claims from Gilchrist et al. (Ralph et al. group),
"Schrödinger cats and their power for quantum information processing",
arXiv:quant-ph/0312194 (2003).

Central claims tested numerically in Fock-truncated bosonic Fock space (dim=40 by default):

C1  Cat-state construction & normalization:
    |cat_+>_α = N_+ (|α> + |-α>)   even cat
    |cat_->_α = N_- (|α> - |-α>)   odd cat
    Check ⟨cat_±|cat_±⟩ = 1 and ⟨cat_+|cat_-⟩ = 0.

C2  Near-orthogonality of the two coherent-state "computational basis" |±α> as α grows.
    Overlap |⟨α|-α⟩|² = exp(-4|α|²) — the exponentially small overlap that motivates
    the whole cat-qubit encoding (Section 2 of the paper).

C3  Bell state on two cat modes:
    |ψ_Bell⟩ ∝ (|α,α> + |-α,-α>)
    Compute concurrence in the effective 2-qubit basis {|α>,|-α>} and verify it
    approaches 1 (maximally entangled) as α grows.

C4  Single-qubit Z gate on the cat basis via free evolution U = exp(-iπ n̂),
    which is a linear phase-shift that maps |α> -> |-α> (and vice-versa) up to
    global phase. In the cat basis:
        |cat_+> -> |cat_+>          (eigenvalue +1)
        |cat_-> -> -|cat_->         (eigenvalue -1)
    → i.e. a Z gate.

Output: JSON with all measured quantities and PASS/FAIL flags per claim.
"""

import json
import math
import os
import sys
import numpy as np
import qutip as qt

# ------------ configuration ------------
DIM = 40                        # Fock truncation
ALPHAS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]  # sweep for α
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

def make_cats(alpha, N):
    """Return (|α>, |-α>, |cat_+>, |cat_->) in Fock dim N."""
    a_pos = qt.coherent(N, alpha)
    a_neg = qt.coherent(N, -alpha)
    plus  = a_pos + a_neg
    minus = a_pos - a_neg
    plus  = plus.unit()
    minus = minus.unit()
    return a_pos, a_neg, plus, minus

def concurrence_2q(rho):
    """Wootters concurrence for a 2-qubit density matrix rho (4x4, ordered as basis
    of the cat effective qubits)."""
    # rho must be a Qobj with dims [[2,2],[2,2]]
    sy = qt.sigmay()
    Y  = qt.tensor(sy, sy)
    rho_tilde = Y * rho.conj() * Y
    R = rho * rho_tilde
    # eigenvalues of R (should be nonnegative real up to num error)
    evs = np.array(sorted(np.real(R.eigenenergies()), reverse=True))
    evs = np.clip(evs, 0.0, None)
    sqrt_ev = np.sqrt(evs)
    C = max(0.0, sqrt_ev[0] - sqrt_ev[1] - sqrt_ev[2] - sqrt_ev[3])
    return float(C)

results = {
    "meta": {
        "paper": "arXiv:quant-ph/0312194",
        "title": "Schrödinger cats and their power for quantum information processing",
        "authors": ["A. Gilchrist", "K. Nemoto", "W. J. Munro", "T. C. Ralph",
                    "S. Glancy", "S. L. Braunstein", "G. J. Milburn"],
        "year": 2003,
        "fock_dim": DIM,
        "qutip_version": qt.__version__,
        "numpy_version": np.__version__,
    },
    "C1_cat_normalization": [],
    "C2_pm_alpha_overlap":  [],
    "C3_bell_concurrence":  [],
    "C4_Z_gate":            [],
}

# ---------- C1 & C2: cat basis & ±α overlap ----------
for alpha in ALPHAS:
    a_pos, a_neg, plus, minus = make_cats(alpha, DIM)

    # normalizations (QuTiP 5 returns scalar for bra*ket)
    n_pp = float(np.abs(complex(plus.dag()  * plus )))
    n_mm = float(np.abs(complex(minus.dag() * minus)))
    o_pm = complex(plus.dag() * minus)

    # bare ±α overlap
    ov_alpha  = complex(a_pos.dag() * a_neg)
    theory_ov = math.exp(-2.0 * alpha**2)  # ⟨α|-α⟩ = exp(-2|α|²) for real α

    results["C1_cat_normalization"].append({
        "alpha": alpha,
        "cat_plus_norm":  n_pp,
        "cat_minus_norm": n_mm,
        "cat_plus_minus_overlap_abs": float(abs(o_pm)),
        "pass": (abs(n_pp-1) < 1e-6 and abs(n_mm-1) < 1e-6 and abs(o_pm) < 1e-6),
    })

    results["C2_pm_alpha_overlap"].append({
        "alpha": alpha,
        "numerical_overlap":       float(ov_alpha.real),
        "theory_exp_neg_2_alpha2": theory_ov,
        "abs_error":               float(abs(ov_alpha.real - theory_ov)),
        "pass": abs(ov_alpha.real - theory_ov) < 1e-5,
    })

# ---------- C3: two-mode cat Bell state concurrence ----------
# |ψ_Bell> = N (|α,α> + |-α,-α>).  Compute density matrix in effective qubit basis
# formed by orthonormalized {|α>,|-α>} per mode via Gram-Schmidt.
for alpha in ALPHAS:
    a_pos, a_neg, _, _ = make_cats(alpha, DIM)

    # Gram-Schmidt to build orthonormal 2D subspace per mode
    e0 = a_pos.unit()
    proj = complex(e0.dag() * a_neg)
    r1 = a_neg - proj * e0
    e1 = r1.unit()

    # two-mode Bell-like state
    psi = qt.tensor(a_pos, a_pos) + qt.tensor(a_neg, a_neg)
    psi = psi.unit()

    # project onto qubit×qubit subspace (basis e0,e1 per mode)
    basis = [qt.tensor(e0, e0), qt.tensor(e0, e1),
             qt.tensor(e1, e0), qt.tensor(e1, e1)]
    coeffs = np.array([complex(b.dag() * psi) for b in basis])
    subspace_norm = float(np.sum(np.abs(coeffs)**2))  # probability inside 2q subspace

    # renormalized 2-qubit pure state
    v = coeffs / np.sqrt(subspace_norm)
    rho2q = qt.Qobj(np.outer(v, v.conj()), dims=[[2,2],[2,2]])

    C = concurrence_2q(rho2q)

    results["C3_bell_concurrence"].append({
        "alpha": alpha,
        "subspace_projection_prob": subspace_norm,
        "concurrence_in_cat_qubit_basis": C,
        "pass": (alpha >= 2.0 and C > 0.99) or (alpha < 2.0),
    })

# ---------- C4: Z gate via linear phase shift exp(-iπ n̂) ----------
# Note: exp(-iπ n̂) |α> = |α e^{-iπ}> = |-α>.  This swaps |α> and |-α>, which
# maps |cat_+> -> |cat_+> and |cat_-> -> -|cat_->  (up to a global phase).
for alpha in ALPHAS:
    a_pos, a_neg, plus, minus = make_cats(alpha, DIM)
    n_op = qt.num(DIM)
    U = (-1j * math.pi * n_op).expm()

    plus_out  = U * plus
    minus_out = U * minus

    # fidelities to targets
    amp_plus  = complex(plus.dag()  * plus_out )
    amp_minus = complex(minus.dag() * minus_out)
    F_plus  = float(np.abs(amp_plus )**2)
    F_minus_pos = float(np.abs(amp_minus)**2)

    results["C4_Z_gate"].append({
        "alpha": alpha,
        "amp_cat_plus_to_cat_plus":   {"re": amp_plus.real,  "im": amp_plus.imag},
        "amp_cat_minus_to_cat_minus": {"re": amp_minus.real, "im": amp_minus.imag},
        "fidelity_plus_to_plus":      F_plus,
        "fidelity_minus_to_minus":    F_minus_pos,
        "sign_check_minus_is_negative": bool(amp_minus.real < -0.999 and abs(amp_minus.imag) < 1e-6),
        "pass": (F_plus > 0.999 and F_minus_pos > 0.999
                 and amp_plus.real >  0.999
                 and amp_minus.real < -0.999),
    })

# ---------- summary ----------
def all_pass(lst): return all(x["pass"] for x in lst)
results["summary"] = {
    "C1_pass_all_alphas": all_pass(results["C1_cat_normalization"]),
    "C2_pass_all_alphas": all_pass(results["C2_pm_alpha_overlap"]),
    "C3_pass_alpha_ge_2": all(x["pass"] for x in results["C3_bell_concurrence"] if x["alpha"] >= 2.0),
    "C4_pass_all_alphas": all_pass(results["C4_Z_gate"]),
}
results["summary"]["overall_pass"] = all(results["summary"].values())

with open(OUT, "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results["summary"], indent=2))
print("Wrote:", OUT)
