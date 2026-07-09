#!/usr/bin/env python3
"""
Interleaved-RB style protocol comparing bare-H vs HI-augmented sequences,
under the paper's over-rotation noise model.

We construct random sequences of Cliffords built from {H, S, S^dagger, X, Z}.
For the "interleaved" gate we insert Hadamards; in the HI version we
alternate H and H^dagger (a compiler could always do this given a self-
inverse target). We fit an exponential decay to the survival probability
and extract the effective per-Clifford error rate.
"""
import numpy as np, json
from sim_hidden_inverses import (X_noisy, Y_noisy, H_standard, H_hidden,
                                  fidelity_states, Z_ideal)

RNG = np.random.default_rng(42)
I2 = np.eye(2, dtype=complex)

def S_ideal():
    return np.array([[1,0],[0,1j]], dtype=complex)

def X_ideal(theta):
    c, s = np.cos(theta/2), np.sin(theta/2)
    return np.array([[c, -1j*s],[-1j*s, c]], dtype=complex)

# a small Clifford set (single-qubit)
def sample_clifford_seq(length, hi=False):
    """
    Returns a list of (name, U_noisy) whose overall product should equal
    identity times some phase-tracked global rotation. The inverse is
    appended at the end so ideal sequence == I.
    """
    seq = []
    prod_ideal = np.eye(2, dtype=complex)
    for i in range(length):
        choice = RNG.integers(0, 4)
        if choice == 0:
            # H (with alternating HI convention if hi=True)
            if hi and (i % 2 == 1):
                U = H_hidden(eps_global)   # noisy alternative
                U_id = H_hidden(0)
            else:
                U = H_standard(eps_global)
                U_id = H_standard(0)
            seq.append(("H", U))
            prod_ideal = U_id @ prod_ideal
        elif choice == 1:
            # S -- no over-rotation for this ideal-Z rotation
            U = S_ideal()
            seq.append(("S", U))
            prod_ideal = U @ prod_ideal
        elif choice == 2:
            # X(pi/2)
            U = X_noisy(np.pi/2, eps_global)
            U_id = X_noisy(np.pi/2, 0)
            seq.append(("X90", U))
            prod_ideal = U_id @ prod_ideal
        else:
            # X(pi)
            U = X_noisy(np.pi, eps_global)
            U_id = X_noisy(np.pi, 0)
            seq.append(("X", U))
            prod_ideal = U_id @ prod_ideal
    # append ideal inverse (assumed perfect for simplicity — this focuses
    # the measured decay on the accumulated coherent error only)
    U_inv = prod_ideal.conj().T
    seq.append(("INV", U_inv))
    return seq

def run_sequence(seq, psi0=None):
    if psi0 is None:
        psi0 = np.array([1+0j, 0+0j])
    psi = psi0.copy()
    for _, U in seq:
        psi = U @ psi
    return psi

def survival_prob(psi):
    return float(np.abs(psi[0])**2)

def rb_curve(lengths, n_seqs=30, hi=False):
    means = []
    for L in lengths:
        surv = []
        for _ in range(n_seqs):
            s = sample_clifford_seq(L, hi=hi)
            psi = run_sequence(s)
            surv.append(survival_prob(psi))
        means.append(float(np.mean(surv)))
    return means

def fit_exp_decay(lengths, ys):
    """Fit ys = A * p^L + B  (with B=0.5 fixed for single qubit)."""
    from scipy.optimize import curve_fit
    def f(L, A, p):
        return A * p**L + 0.5
    p0 = [0.5, 0.99]
    try:
        popt, _ = curve_fit(f, lengths, ys, p0=p0,
                            bounds=([0,0.5],[1,1]), maxfev=5000)
        A, p = popt
        # per-Clifford error rate = (1-p)/2 for d=2
        r = (1.0 - p) / 2.0
        return float(A), float(p), float(r)
    except Exception as ex:
        return None, None, None

if __name__ == "__main__":
    eps_global = 0.05
    lengths = [1, 2, 4, 8, 16, 32]

    print(f"Running RB-style benchmark with over-rotation eps={eps_global} ...")
    means_bare = rb_curve(lengths, n_seqs=40, hi=False)
    means_hi   = rb_curve(lengths, n_seqs=40, hi=True)

    A_b, p_b, r_b = fit_exp_decay(np.array(lengths), np.array(means_bare))
    A_h, p_h, r_h = fit_exp_decay(np.array(lengths), np.array(means_hi))

    print(f"BARE : A={A_b:.3f}, p={p_b:.5f}, per-Clifford err r={r_b:.4e}")
    print(f"HI   : A={A_h:.3f}, p={p_h:.5f}, per-Clifford err r={r_h:.4e}")
    if r_h > 0 and r_b > 0:
        print(f"Error-rate reduction: {r_b/r_h:.2f}x")

    out = {
        "eps": eps_global,
        "lengths": list(lengths),
        "means_bare": means_bare,
        "means_hi":   means_hi,
        "fit_bare":   {"A": A_b, "p": p_b, "r": r_b},
        "fit_hi":     {"A": A_h, "p": p_h, "r": r_h},
        "reduction_x": float(r_b/r_h) if r_h and r_h>0 else None,
    }
    with open("results_rb.json", "w") as f:
        json.dump(out, f, indent=2)
