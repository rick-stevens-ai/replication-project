#!/usr/bin/env python3
"""
Independent replication (small-instance, faithful) of the central claim of
Yoshioka et al., "Fermionic Quantum Approximate Optimization Algorithm"
arXiv:2301.10756 (2023).

Central claim tested: On a *constrained* (fixed-Hamming-weight) portfolio-like
QUBO, FQAOA (fermionic driver, particle-number-preserving initial state and
mixer) achieves *lower residual energy* Delta E := E_p - E_min at matched
depth p than X-QAOA (transverse-field mixer, |+>^N initial state) with an
Ising-style quadratic soft-penalty enforcing the constraint. Fixed-angle
schedule (Eq. 22 of the paper) is used for both (no variational optimization),
so the comparison is apples-to-apples and driven purely by the ansatz choice.

We use N=6 sites (single-leg lattice, D=1) with M=3 held (constraint sum x_l =
M=3). This is a 6-qubit, 2^6=64-dimensional state-vector problem, exactly
simulable on a laptop in seconds. Random reproducible portfolio: covariance
Sigma symmetric positive-definite from a Wishart-like construction, returns mu
Gaussian, risk-tolerance lambda=0.9, penalty A=0.003 (paper's values).

Everything is a real numerical simulation. No fabrication.
"""

import json
import math
import os
import time
from pathlib import Path

import numpy as np
from scipy.linalg import expm

# ------------------------------------------------------------
# Problem setup: cardinality-constrained QUBO portfolio (D=1)
# ------------------------------------------------------------

def build_portfolio(N=6, M=3, lam=0.9, seed=20260703):
    """Return Sigma (NxN, symmetric PSD), mu (N,), lam, M, N.
    Mirrors Eq. (26) of the paper (with D=1, unary encoding f_d=1)."""
    rng = np.random.default_rng(seed)
    # Wishart-like covariance
    A = rng.normal(size=(N, N))
    Sigma = (A @ A.T) / N + 0.1 * np.eye(N)
    Sigma = 0.5 * (Sigma + Sigma.T)
    mu = rng.normal(size=N) * 0.5
    return dict(N=N, M=M, lam=lam, Sigma=Sigma, mu=mu)


def energy_bitstring(x, prob):
    """Portfolio energy E(x) for binary vector x, per Eq. (30) with D=1.

    E(x) = (lam / M^2) sum_{l,l'} Sigma_{l,l'} x_l x_l'
          + ((1-lam) / M) sum_l mu_l (x_l - 1/2)  ... with sign convention
    We follow the paper: minimize risk minus return, so the return term is
    subtracted. Using paper's Eq. (26) form E(w) = (lam/M^2)*x^T Sigma x - ((1-lam)/M)*sum mu_l x_l.
    """
    M = prob["M"]
    lam = prob["lam"]
    Sigma = prob["Sigma"]
    mu = prob["mu"]
    x = np.asarray(x, dtype=float)
    risk = (lam / (M * M)) * (x @ Sigma @ x)
    ret = ((1.0 - lam) / M) * float(mu @ x)
    return risk - ret


def all_bitstrings(N):
    for k in range(1 << N):
        yield np.array([(k >> i) & 1 for i in range(N)], dtype=int)


def diagonal_hp(prob):
    """Return the 2^N-dim diagonal of the problem Hamiltonian H_p, whose
    computational-basis eigenvalues equal E(x). Bit ordering: index i encodes
    site 0 in bit 0, site 1 in bit 1, ... (little-endian)."""
    N = prob["N"]
    diag = np.zeros(1 << N)
    for k in range(1 << N):
        x = np.array([(k >> i) & 1 for i in range(N)], dtype=int)
        diag[k] = energy_bitstring(x, prob)
    return diag


def feasible_indices(prob):
    """Basis indices satisfying sum x_l = M."""
    N, M = prob["N"], prob["M"]
    idx = []
    for k in range(1 << N):
        c = bin(k).count("1")
        if c == M:
            idx.append(k)
    return np.array(idx, dtype=int)


# ------------------------------------------------------------
# Baseline energy references
# ------------------------------------------------------------

def brute_force(prob):
    """Return (E_min_feasible, E_max_feasible, W_scale, x_opt)."""
    diag = diagonal_hp(prob)
    feas = feasible_indices(prob)
    e_feas = diag[feas]
    e_min = float(e_feas.min())
    e_max = float(e_feas.max())
    W = e_max - e_min
    kstar = feas[int(np.argmin(e_feas))]
    x_opt = [(kstar >> i) & 1 for i in range(prob["N"])]
    return e_min, e_max, W, x_opt, diag


# ------------------------------------------------------------
# X-QAOA (baseline): H_d = -sum X_i, initial |+>^N, penalty added to H_p.
# ------------------------------------------------------------

def pauli_x_sum(N):
    """Return dense 2^N x 2^N matrix of -sum_i X_i (transverse field driver).
    Sign chosen so ground state is |+>^N with eigenvalue -N."""
    dim = 1 << N
    H = np.zeros((dim, dim), dtype=complex)
    for i in range(N):
        # -X_i
        for k in range(dim):
            k2 = k ^ (1 << i)
            H[k2, k] += -1.0
    return H


def h_penalty_diag(prob, A_pen):
    """Diagonal of A * (sum_l n_l - M)^2 penalty (Eq. 73 with D=1)."""
    N, M = prob["N"], prob["M"]
    diag = np.zeros(1 << N)
    for k in range(1 << N):
        c = bin(k).count("1")
        diag[k] = A_pen * (c - M) ** 2
    return diag


def xqaoa_run(prob, p, dt, A_pen=0.003):
    """Run fixed-angle X-QAOA with penalty. Returns (E_expect, |psi>).
    Uses fixed-angle schedule from paper Eq. (22):
        gamma_j = ((2j-1)/(2p)) * dt
        beta_j  = (1 - (2j-1)/(2p)) * dt
    Energy scale used inside U_p is that of H_p' = H_p + A*H_pen.
    """
    N = prob["N"]
    dim = 1 << N
    diag_hp = diagonal_hp(prob)
    diag_hp_prime = diag_hp + h_penalty_diag(prob, A_pen)
    Hx = pauli_x_sum(N)  # = -sum_i X_i (drives ground = |+>^N)

    # Initial state |+>^N
    psi = np.ones(dim, dtype=complex) / math.sqrt(dim)

    for j in range(1, p + 1):
        gamma_j = ((2 * j - 1) / (2 * p)) * dt
        beta_j = (1.0 - (2 * j - 1) / (2 * p)) * dt
        # exp(-i * gamma * H_p')  (diagonal)
        psi = np.exp(-1j * gamma_j * diag_hp_prime) * psi
        # exp(-i * beta * H_d) where H_d = -sum X_i --> the "mixer" step
        U_mix = expm(-1j * beta_j * Hx)
        psi = U_mix @ psi

    # Expectation of H_p (the *true* problem energy) — note: we score
    # w.r.t. H_p (not H_p') because that's the physical cost function.
    probs = np.abs(psi) ** 2
    e_expect = float(np.sum(probs * diag_hp))
    # Feasibility-projected energy: sum over feasible only, normalised
    feas = feasible_indices(prob)
    p_feas = float(np.sum(probs[feas]))
    if p_feas > 1e-12:
        e_expect_feas = float(np.sum(probs[feas] * diag_hp[feas]) / p_feas)
    else:
        e_expect_feas = float("nan")
    return dict(E_expect=e_expect, E_expect_feas=e_expect_feas,
                p_feasible=p_feas, psi=psi)


# ------------------------------------------------------------
# FQAOA (ring hopping driver): H_d = -t sum_l (c_l^dag c_{l+1} + h.c.)
# on periodic 1D chain (Eq. 36-37 with D=1). Jordan-Wigner: this becomes
#   H_d = -(t/2) sum_l (X_l X_{l+1} + Y_l Y_{l+1}) * (JW string on boundary)
# For open BC we drop the wrap-around. For periodic BC there's a fermion-
# parity phase on the wrap term. We build H_d directly in the full 2^N space
# by summing hopping in the *particle-number basis* (guaranteed to conserve N)
# via bilinear-form diagonalisation, then project the exponential.
# ------------------------------------------------------------

def hopping_matrix(N, t=1.0, periodic=True):
    """N x N one-body hopping matrix h with -t on nearest-neighbor bonds.
    Periodic wrap sign: for a particle-conserving TB model, the wrap term
    picks up a factor (-1)^{M'-1} in the many-body Hamiltonian under JW.
    Here we return the free-particle hopping matrix h; the many-body H_d
    is realised via the free-fermion single-particle basis (Eq. 37-40)."""
    h = np.zeros((N, N))
    for i in range(N):
        j = (i + 1) % N
        if not periodic and i == N - 1:
            continue
        h[i, j] += -t
        h[j, i] += -t
    return h


def fermion_basis(N, M):
    """Enumerate basis indices with popcount == M; return list of (basis_idx,
    tuple of occupied sites in ascending order)."""
    out = []
    for k in range(1 << N):
        occ = tuple(i for i in range(N) if (k >> i) & 1)
        if len(occ) == M:
            out.append((k, occ))
    return out


def slater_amplitude(occ_sites, orb_matrix):
    """<x|Slater> for occupation pattern `occ_sites` (tuple of site indices,
    ascending) and Slater determinant made of columns of orb_matrix
    (N x M complex).  Returns det of the M x M sub-matrix rows=occ_sites."""
    sub = orb_matrix[list(occ_sites), :]
    return np.linalg.det(sub)


def build_fqaoa_initial_state(N, M):
    """Return |phi_0> = ground state of H_d with particle number M, as a
    2^N-dim state vector.  H_d = hopping on periodic ring."""
    h = hopping_matrix(N, t=1.0, periodic=True)
    eps, phi = np.linalg.eigh(h)  # eps ascending
    # Pick M lowest single-particle levels
    C = phi[:, :M]  # N x M
    # Build |phi_0> in the many-body computational basis
    dim = 1 << N
    psi = np.zeros(dim, dtype=complex)
    for k, occ in fermion_basis(N, M):
        # amplitude = det of C[occ_sites, :] (unnormalised by 1/sqrt(M!) — but
        # we normalise at the end anyway)
        psi[k] = slater_amplitude(occ, C)
    nrm = np.linalg.norm(psi)
    assert nrm > 0
    psi /= nrm
    return psi, eps, phi


def build_hd_manybody(N, M):
    """Return the many-body H_d = sum_{k} eps_k n_k, but expressed in the
    computational basis, restricted to particle number M sector. We build it
    as a dense 2^N x 2^N matrix that is block-diagonal in particle-number
    sectors; only the M sector will be exercised because our initial state
    lives in that sector."""
    h = hopping_matrix(N, t=1.0, periodic=True)
    eps, phi = np.linalg.eigh(h)
    # For each many-body basis state |x>, H_d|x> = sum_l h_{l,l'} c_l^dag c_l' |x>
    dim = 1 << N
    H = np.zeros((dim, dim), dtype=complex)
    for k in range(dim):
        for l in range(N):
            for lp in range(N):
                if abs(h[l, lp]) < 1e-14:
                    continue
                # apply c_lp then c_l^dag to |k>
                # c_lp |k>: if bit lp not set, 0. Else remove and JW phase.
                if not ((k >> lp) & 1):
                    continue
                # JW sign: (-1)^{#occupied sites < lp}
                sign1 = 1
                for q in range(lp):
                    if (k >> q) & 1:
                        sign1 *= -1
                k_mid = k ^ (1 << lp)
                # c_l^dag |k_mid>: if bit l already set, 0.
                if (k_mid >> l) & 1:
                    continue
                sign2 = 1
                for q in range(l):
                    if (k_mid >> q) & 1:
                        sign2 *= -1
                k_new = k_mid ^ (1 << l)
                H[k_new, k] += h[l, lp] * sign1 * sign2
    # Hermitise (numerical)
    H = 0.5 * (H + H.conj().T)
    return H


def fqaoa_run(prob, p, dt):
    """Run fixed-angle FQAOA. Initial state = g.s. of H_d in M sector.
    Fixed-angle schedule (paper Eq. 22, adapted):
        gamma_j = ((2j-1)/(2p)) * dt
        beta_j  = (1 - (2j-1)/(2p)) * dt
    Since |phi_0> lives entirely in the M-particle sector and both H_p and
    H_d preserve particle number, the evolved state stays in that sector,
    trivially satisfying the constraint. No penalty needed.
    """
    N = prob["N"]
    M = prob["M"]
    diag_hp = diagonal_hp(prob)  # H_p is diagonal in computational basis
    Hd = build_hd_manybody(N, M)  # dense many-body hopping H_d (JW)
    psi, _, _ = build_fqaoa_initial_state(N, M)

    # Sanity: initial state must live entirely in particle-number-M sector
    feas = feasible_indices(prob)
    infeas_mass_init = 1.0 - float(np.sum(np.abs(psi[feas]) ** 2))
    assert infeas_mass_init < 1e-10, f"init leaked into wrong sector: {infeas_mass_init}"

    for j in range(1, p + 1):
        gamma_j = ((2 * j - 1) / (2 * p)) * dt
        beta_j = (1.0 - (2 * j - 1) / (2 * p)) * dt
        # exp(-i gamma H_p) — diagonal in computational basis
        psi = np.exp(-1j * gamma_j * diag_hp) * psi
        # exp(-i beta H_d) — dense many-body exponential
        U_mix = expm(-1j * beta_j * Hd)
        psi = U_mix @ psi

    probs = np.abs(psi) ** 2
    e_expect = float(np.sum(probs * diag_hp))
    p_feas = float(np.sum(probs[feas]))
    if p_feas > 1e-12:
        e_expect_feas = float(np.sum(probs[feas] * diag_hp[feas]) / p_feas)
    else:
        e_expect_feas = float("nan")
    return dict(E_expect=e_expect, E_expect_feas=e_expect_feas,
                p_feasible=p_feas, psi=psi)


# ------------------------------------------------------------
# Main experiment
# ------------------------------------------------------------

def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)

    N, M = 6, 3
    prob = build_portfolio(N=N, M=M, lam=0.9, seed=20260703)
    e_min, e_max, W, x_opt, _ = brute_force(prob)
    print(f"[problem] N={N}, M={M}, lam=0.9  (D=1, single-leg)")
    print(f"[problem] E_min (feasible) = {e_min:.6f}")
    print(f"[problem] E_max (feasible) = {e_max:.6f}")
    print(f"[problem] W = E_max - E_min = {W:.6f}")
    print(f"[problem] optimal bitstring = {x_opt}")

    A_pen = 0.003  # paper's value
    p_values = [1, 2, 3, 4, 5, 6, 8, 10]
    dt_values = [0.1, 5.0, 10.0]   # paper uses Wtilde*dt on x-axis (Fig. 5)

    results = {
        "problem": {
            "N": N, "M": M, "lam": 0.9, "A_pen": A_pen,
            "E_min": e_min, "E_max": e_max, "W": W,
            "x_opt": x_opt,
            "Sigma": prob["Sigma"].tolist(),
            "mu": prob["mu"].tolist(),
        },
        "fixed_angle_schedule": "paper Eq. (22): gamma_j=((2j-1)/(2p))*dt, beta_j=(1-(2j-1)/(2p))*dt",
        "runs": [],
    }

    print()
    print(f"{'method':<9} {'p':>3} {'dt':>6} {'E_expect':>12} {'E_expect_feas':>14} {'p_feas':>8} {'DeltaE':>12} {'DeltaE/W':>12}")

    t0 = time.time()
    for dt in dt_values:
        for p in p_values:
            r_x = xqaoa_run(prob, p=p, dt=dt, A_pen=A_pen)
            delta_x = r_x["E_expect"] - e_min
            row = dict(method="X-QAOA", p=p, dt=dt,
                       E_expect=r_x["E_expect"],
                       E_expect_feas=r_x["E_expect_feas"],
                       p_feasible=r_x["p_feasible"],
                       DeltaE=delta_x, DeltaE_over_W=delta_x / W)
            results["runs"].append(row)
            print(f"{'X-QAOA':<9} {p:>3} {dt:>6.2f} {r_x['E_expect']:>12.5f} "
                  f"{r_x['E_expect_feas']:>14.5f} {r_x['p_feasible']:>8.4f} "
                  f"{delta_x:>12.5f} {delta_x/W:>12.5f}")

            r_f = fqaoa_run(prob, p=p, dt=dt)
            delta_f = r_f["E_expect"] - e_min
            row = dict(method="FQAOA", p=p, dt=dt,
                       E_expect=r_f["E_expect"],
                       E_expect_feas=r_f["E_expect_feas"],
                       p_feasible=r_f["p_feasible"],
                       DeltaE=delta_f, DeltaE_over_W=delta_f / W)
            results["runs"].append(row)
            print(f"{'FQAOA':<9} {p:>3} {dt:>6.2f} {r_f['E_expect']:>12.5f} "
                  f"{r_f['E_expect_feas']:>14.5f} {r_f['p_feasible']:>8.4f} "
                  f"{delta_f:>12.5f} {delta_f/W:>12.5f}")

    elapsed = time.time() - t0
    print(f"\n[timing] full sweep in {elapsed:.2f} s")

    # ----- Verdict summary: at matched (p, dt), does FQAOA beat X-QAOA? -----
    wins_fqaoa = 0
    ties = 0
    losses = 0
    per_dt_summary = {}
    for dt in dt_values:
        pairs = []
        for p in p_values:
            dx = next(r for r in results["runs"]
                      if r["method"] == "X-QAOA" and r["p"] == p and r["dt"] == dt)
            df = next(r for r in results["runs"]
                      if r["method"] == "FQAOA" and r["p"] == p and r["dt"] == dt)
            fqaoa_better = df["DeltaE"] < dx["DeltaE"] - 1e-9
            xqaoa_better = dx["DeltaE"] < df["DeltaE"] - 1e-9
            if fqaoa_better:
                wins_fqaoa += 1; tag = "FQAOA<"
            elif xqaoa_better:
                losses += 1; tag = "X<FQAOA"
            else:
                ties += 1; tag = "tie"
            pairs.append(dict(p=p, dx=dx["DeltaE"], df=df["DeltaE"],
                              ratio=(dx["DeltaE"] / df["DeltaE"]) if df["DeltaE"] > 1e-12 else float("inf"),
                              tag=tag))
        per_dt_summary[str(dt)] = pairs

    results["summary"] = dict(
        wins_fqaoa=wins_fqaoa, ties=ties, losses=losses,
        per_dt=per_dt_summary,
    )

    print()
    print("=== FQAOA vs X-QAOA head-to-head (fixed-angle, matched p and dt) ===")
    for dt in dt_values:
        print(f"  dt={dt}:")
        for row in per_dt_summary[str(dt)]:
            ratio_str = f"{row['ratio']:.3f}x" if math.isfinite(row['ratio']) else "inf"
            print(f"    p={row['p']:>2}  DeltaE(X)={row['dx']:+.5f}  DeltaE(F)={row['df']:+.5f}  "
                  f"X/F={ratio_str}  --> {row['tag']}")
    print()
    print(f"Wins for FQAOA: {wins_fqaoa} / {wins_fqaoa+ties+losses}  (ties={ties}, X-QAOA wins={losses})")

    out_json = outdir / "fqaoa_vs_xqaoa_results.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print(f"[saved] {out_json}")

    # Also write a compact CSV
    csv_path = outdir / "fqaoa_vs_xqaoa_results.csv"
    with open(csv_path, "w") as f:
        f.write("method,p,dt,E_expect,E_expect_feas,p_feasible,DeltaE,DeltaE_over_W\n")
        for r in results["runs"]:
            f.write(f"{r['method']},{r['p']},{r['dt']},{r['E_expect']:.8f},"
                    f"{r['E_expect_feas']:.8f},{r['p_feasible']:.8f},"
                    f"{r['DeltaE']:.8f},{r['DeltaE_over_W']:.8f}\n")
    print(f"[saved] {csv_path}")


if __name__ == "__main__":
    main()
