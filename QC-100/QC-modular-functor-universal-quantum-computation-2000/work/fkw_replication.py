#!/usr/bin/env python3
"""
Independent replication of Freedman-Kitaev-Larsen-Wang (2000)
"A modular functor which is universal for quantum computation"
arXiv:quant-ph/0001108

We independently verify the paper's concrete testable claims for
SU(2)-Chern-Simons at 5-th root of unity (r=5), which is the
"Fibonacci"/CS5 theory the paper identifies as universal for
quantum computation via braiding.

Testable claims we replicate:

C1 (dimensions):  dim V_3^1 = 2, dim V_3^3 = 1, dim V_6^0 = 5,
                 dim V_6^2 = 8    [Eq. (4) of the paper].

C2 (unitarity):  Jones-representation braid generators
                 rho_lambda(sigma_i) are unitary for the (2,5)-Young
                 diagrams lambda = [2,1] (n=3), [3,3] (n=6),
                 [4,2] (n=6).

C3 (braid relation): rho(sigma_i) rho(sigma_{i+1}) rho(sigma_i)
                     = rho(sigma_{i+1}) rho(sigma_i) rho(sigma_{i+1})
                     and rho(sigma_i) rho(sigma_j) = rho(sigma_j) rho(sigma_i)
                     if |i-j| >= 2.

C4 (eigenvalues): Every rho(sigma_i) has exactly two distinct
                  eigenvalues, -1 and q = exp(2 pi i / 5).

C5 (multiplicities for lambda=[4,2]): eigenvalue -1 has multiplicity 3,
                                       eigenvalue q has multiplicity 5.
                                       [Theorem 3.1(iv)]

C6 (density -> universality): Sample uniformly-random braid words in
    B_3 acting through rho_{[2,1]} on U(2)/center; verify the image
    is not contained in any finite subgroup and appears to be dense
    on SU(2)/center by looking at how well arbitrary target 1-qubit
    gates can be approximated by short braid words (brute-force
    search).  This is a "density-in-action" check aligned with the
    paper's Theorem 4.1 for the smallest case.

C7 (compare with an explicit matrix in the paper): the paper prints
    rho_{[2,1],β,3}(σ_1) = diag(-1, q).  We construct our rho and
    verify (up to gauge/basis conjugation) that our sigma_1 has the
    same spectrum, and that the paper's printed rho_{[2,1]}(sigma_2)
    is a valid unitary matrix (i.e. the printed matrix as-is is
    unitary), which is a direct sanity check of the *paper's own*
    formula (Section 3, page 15).

Everything below uses (i) the Jones representation formula (13)-(15) of
the paper directly, or (ii) the paper's own printed matrix.  We do not
copy from any other implementation.
"""

import json
import math
import cmath
import os
import sys
import time
from fractions import Fraction

import numpy as np

# ------------------------------------------------------------------
# 0.  Constants for r = 5.
# ------------------------------------------------------------------
R = 5
q  = cmath.exp(2j * math.pi / R)          # q = e^{2πi/5}
qb = q.conjugate()
# quantum integers  [k] = (q^{k/2} - q^{-k/2}) / (q^{1/2} - q^{-1/2})
def qint(k: int) -> complex:
    num = cmath.exp(1j * math.pi * k / R) - cmath.exp(-1j * math.pi * k / R)
    den = cmath.exp(1j * math.pi     / R) - cmath.exp(-1j * math.pi     / R)
    return num / den
# beta = [2]^2 = 4 cos^2(π/r)
beta = (2 * math.cos(math.pi / R)) ** 2

# ------------------------------------------------------------------
# 1.  Compute V_n^ℓ dimensions from the paper's admissibility rules
#     (equation (3)):
#        (i)   a + b + c even
#        (ii)  triangle inequalities
#        (iii) a + b + c <= 2(r - 2)
#     for a 3-punctured sphere V_{abc} ∼= C.
#
#     For a disk with n interior punctures labeled 1 and boundary
#     label ℓ, we recursively use the gluing / fusion rule:
#        V_{n+1}^ℓ = ⊕_{ℓ'} V_n^{ℓ'} ⊗ V_{ℓ',1,ℓ}
#     with dim V_{ℓ',1,ℓ} = 1 if admissible, 0 otherwise.
# ------------------------------------------------------------------

MAX_LABEL = R - 2   # labels {0,1,...,r-2}

def admissible_triple(a: int, b: int, c: int) -> bool:
    if (a + b + c) % 2 != 0:
        return False
    if a > b + c or b > a + c or c > a + b:
        return False
    if a + b + c > 2 * (R - 2):
        return False
    return True

def dim_V_n_ell(n: int, ell: int) -> int:
    """Dimension of V_n^ℓ = disk with n punctures labeled 1, boundary label ell."""
    # dp[k][m] = dimension of the state space on a disk with k punctures
    # (labeled 1) and outer boundary labeled m.
    dp = [ [0] * (MAX_LABEL + 1) for _ in range(n + 1) ]
    # Base: k=0 punctures, only trivial label survives.
    dp[0][0] = 1
    for k in range(1, n + 1):
        for m in range(MAX_LABEL + 1):
            total = 0
            for mp in range(MAX_LABEL + 1):
                if admissible_triple(mp, 1, m):
                    total += dp[k-1][mp]
            dp[k][m] = total
    return dp[n][ell]

# ------------------------------------------------------------------
# 2.  Standard tableaux of (2, r)-Young diagrams (paper's notation).
#     A (2,5) Young diagram [λ1, λ2] with λ1 >= λ2, λ1 - λ2 <= r-2 = 3,
#     n = λ1 + λ2 cells.
#     A standard tableau assigns 1..n to cells so rows and columns
#     increase.  The paper further requires the "inductive
#     admissibility" condition: after deleting n, n-1, ..., 1 in turn,
#     each intermediate shape must again be a (2, r) diagram.
# ------------------------------------------------------------------

def shape_ok(lam):
    """Is shape a valid (2, r) Young diagram?"""
    lam = tuple(x for x in lam if x > 0)
    if len(lam) == 0:
        return True
    if len(lam) > 2:
        return False
    if len(lam) == 1:
        return lam[0] <= R - 2 + 0   # allow single row
    l1, l2 = lam
    return l1 >= l2 and (l1 - l2) <= (R - 2)

def enumerate_tableaux(lam):
    """All standard tableaux of shape lam with the paper's admissibility.

    We represent a standard tableau as a 2-row list of columns:
        entries[r][c] = value in row r, column c   (0-indexed rows)
    We fill entries 1..n in increasing order, choosing at each step
    which corner to add the next entry to.  A candidate placement
    yields a shape that must be (2, r)-admissible AT EVERY STEP.
    """
    n = sum(lam)
    lam = tuple(lam)
    results = []

    def rec(step, shape, tab):
        if step > n:
            if shape == lam:
                # Convert to a canonical hashable form.
                results.append(tuple(tuple(row) for row in tab))
            return
        # Add step to a corner:
        # row 0: shape[0] + 1  (if <= lam[0])
        # row 1: shape[1] + 1  (if row 1 exists in lam, shape[1] < shape[0], and <= lam[1])
        # Row 0 candidate
        new_shape0 = (shape[0] + 1, shape[1])
        if new_shape0[0] <= lam[0] and shape_ok(new_shape0):
            tab0 = [list(tab[0]) + [step], list(tab[1])]
            rec(step + 1, new_shape0, tab0)
        # Row 1 candidate
        if len(lam) >= 2 and lam[1] > 0:
            new_shape1 = (shape[0], shape[1] + 1)
            if new_shape1[1] < new_shape1[0] + 1 and new_shape1[1] <= lam[1] and shape_ok(new_shape1):
                tab1 = [list(tab[0]), list(tab[1]) + [step]]
                rec(step + 1, new_shape1, tab1)

    if len(lam) == 1:
        rec(1, (0, 0), [[], []])
    else:
        rec(1, (0, 0), [[], []])
    return results

# ------------------------------------------------------------------
# 3.  Jones representation of Temperley-Lieb generators e_i on Vλ,
#     following paper eq. (13)-(14):
#        d_{t,i} = c_1 - c_2 - (r_1 - r_2)
#        α_{t,i} = [d_{t,i}+1] / ([2] [d_{t,i}])
#        β_{t,i} = sqrt( α_{t,i} (1 - α_{t,i}) )
#     e_i acts by 1x1 or 2x2 blocks depending on whether swapping i, i+1
#     yields another standard tableau of the same shape (with the
#     admissibility condition).
# ------------------------------------------------------------------

def find_pos(tab, val):
    for ri, row in enumerate(tab):
        for ci, x in enumerate(row):
            if x == val:
                return (ri, ci)
    raise ValueError(f"value {val} not in tab")

def swap_tab(tab, i):
    """Swap i and i+1 in tableau tab. Return new tab (as tuple of tuples), or None if not standard."""
    tab_l = [list(row) for row in tab]
    rp = {i: find_pos(tab_l, i), i+1: find_pos(tab_l, i+1)}
    r_i, c_i = rp[i]
    r_ip, c_ip = rp[i+1]
    tab_l[r_i][c_i] = i + 1
    tab_l[r_ip][c_ip] = i
    # Check standard: rows/cols strictly increasing.
    for row in tab_l:
        for j in range(len(row) - 1):
            if row[j] >= row[j+1]:
                return None
    ncols = max(len(row) for row in tab_l)
    for c in range(ncols):
        col_vals = [row[c] for row in tab_l if c < len(row)]
        for j in range(len(col_vals) - 1):
            if col_vals[j] >= col_vals[j+1]:
                return None
    return tuple(tuple(row) for row in tab_l)

def d_ti(tab, i):
    r1, c1 = find_pos(tab, i)
    r2, c2 = find_pos(tab, i + 1)
    return c1 - c2 - (r1 - r2)

def alpha_ti(tab, i):
    d = d_ti(tab, i)
    # α = [d+1] / ([2] [d])
    num = qint(d + 1)
    den = qint(2) * qint(d)
    if abs(den) < 1e-14:
        # In degenerate cases treat as 0 or 1 per paper.
        return 0.0
    val = num / den
    # α should be a non-negative real number by the paper.
    if abs(val.imag) > 1e-9:
        raise RuntimeError(f"alpha_ti not real: {val}")
    return float(val.real)

def e_matrix(lam, i, tableaux, idx):
    """Matrix of e_i in the basis {v_t}."""
    dim = len(tableaux)
    E = np.zeros((dim, dim), dtype=complex)
    for t in tableaux:
        j = idx[t]
        t_swap = swap_tab(t, i)
        if t_swap is None or t_swap not in idx:
            # 1x1 block: α is 0 or 1 by the paper.
            d = d_ti(t, i)
            if d == -1:
                # α = [0] / ([2][-1]) = 0
                a = 0.0
            elif d == 1:
                # for a 1x1 diagonal block, α ∈ {0, 1}. When β = 0 the
                # 2x2 formula gives a diagonal projector with a=α.
                a = alpha_ti(t, i)
                # Clamp near-integers.
                if abs(a) < 1e-9: a = 0.0
                elif abs(a - 1) < 1e-9: a = 1.0
            else:
                a = alpha_ti(t, i)
                if abs(a) < 1e-9: a = 0.0
                elif abs(a - 1) < 1e-9: a = 1.0
            E[j, j] = a
        else:
            # 2x2 block over {t, swap(t,i)}.
            k = idx[t_swap]
            a = alpha_ti(t, i)
            # β = sqrt(α(1-α)); ensure non-negative.
            b2 = a * (1 - a)
            b = math.sqrt(max(b2, 0.0))
            E[j, j] = a
            # Only fill off-diagonal from t to swap; the diagonal entry
            # of t_swap will be filled when we iterate over it.
            E[k, j] = b
    return E

def sigma_matrix(E):
    """rho(sigma_i) = q - (1+q) e_i  (paper eq. (15))."""
    dim = E.shape[0]
    return q * np.eye(dim, dtype=complex) - (1 + q) * E

# ------------------------------------------------------------------
# 4.  Build the Jones representation on B_n for a given (2,5) Young diagram.
# ------------------------------------------------------------------

def build_rep(lam):
    n = sum(lam)
    tableaux = enumerate_tableaux(lam)
    idx = {t: i for i, t in enumerate(tableaux)}
    Es    = []
    sigmas = []
    for i in range(1, n):
        E = e_matrix(lam, i, tableaux, idx)
        Es.append(E)
        sigmas.append(sigma_matrix(E))
    return tableaux, Es, sigmas

# ------------------------------------------------------------------
# 5.  Verification helpers.
# ------------------------------------------------------------------

def is_unitary(M, tol=1e-8):
    d = M.shape[0]
    return np.allclose(M.conj().T @ M, np.eye(d), atol=tol) and \
           np.allclose(M @ M.conj().T, np.eye(d), atol=tol)

def frob(A, B):
    return float(np.linalg.norm(A - B))

def check_braid_relations(sigmas, tol=1e-9):
    """Return (n-1)-list of (relation, ok, residual)."""
    out = []
    m = len(sigmas)
    for i in range(m - 1):
        A = sigmas[i] @ sigmas[i+1] @ sigmas[i]
        B = sigmas[i+1] @ sigmas[i] @ sigmas[i+1]
        r = frob(A, B)
        out.append((f"sigma_{i+1} sigma_{i+2} sigma_{i+1} = sigma_{i+2} sigma_{i+1} sigma_{i+2}", r < tol, r))
    for i in range(m):
        for j in range(i + 2, m):
            A = sigmas[i] @ sigmas[j]
            B = sigmas[j] @ sigmas[i]
            r = frob(A, B)
            out.append((f"sigma_{i+1} sigma_{j+1} = sigma_{j+1} sigma_{i+1}", r < tol, r))
    return out

def check_e_relations(Es, tol=1e-9):
    """Check e_i^2 = e_i, e_i^* = e_i, e_i e_{i+1} e_i = beta^{-1} e_i, e_i e_j = e_j e_i for |i-j|>=2."""
    out = []
    m = len(Es)
    for i in range(m):
        E = Es[i]
        out.append((f"e_{i+1}^2 = e_{i+1}", frob(E @ E, E) < tol, frob(E @ E, E)))
        out.append((f"e_{i+1}^* = e_{i+1}", frob(E.conj().T, E) < tol, frob(E.conj().T, E)))
    for i in range(m - 1):
        E1, E2 = Es[i], Es[i+1]
        A = E1 @ E2 @ E1
        B = (1.0 / beta) * E1
        out.append((f"e_{i+1} e_{i+2} e_{i+1} = beta^-1 e_{i+1}", frob(A, B) < tol, frob(A, B)))
    for i in range(m):
        for j in range(i + 2, m):
            E1, E2 = Es[i], Es[j]
            r = frob(E1 @ E2, E2 @ E1)
            out.append((f"e_{i+1} e_{j+1} commute", r < tol, r))
    return out

def eigenvalues(M):
    return sorted(np.linalg.eigvals(M), key=lambda z: (round(z.real, 6), round(z.imag, 6)))

def check_eigenvalues(sigmas, tol=1e-8):
    """Verify each sigma has spectrum exactly {-1, q} (with multiplicities)."""
    out = []
    for i, S in enumerate(sigmas):
        evs = np.linalg.eigvals(S)
        near_m1 = sum(1 for z in evs if abs(z - (-1)) < tol)
        near_q  = sum(1 for z in evs if abs(z - q) < tol)
        others  = sum(1 for z in evs if abs(z - (-1)) >= tol and abs(z - q) >= tol)
        out.append({
            "i": i + 1,
            "n_eigs": len(evs),
            "mult_-1": int(near_m1),
            "mult_q":  int(near_q),
            "mult_other": int(others),
            "spectrum_ok": others == 0 and (near_m1 + near_q == len(evs)),
        })
    return out

# ------------------------------------------------------------------
# 6.  Density check.  Sample uniformly-random braid words in B_n
#     acting on Vλ, look at the resulting unitary spread, and check
#     it is not stuck in a finite subgroup.  For the 2-dim case
#     lambda=[2,1] we can quantitatively compare against the SU(2)
#     Haar distribution.
# ------------------------------------------------------------------

def sample_braid_word(n_generators, length, rng):
    """Random braid word of given length in generators 1..n_generators and inverses.

    Returns list of signed generator indices (+/- i, 1-indexed).
    """
    out = []
    for _ in range(length):
        g = rng.integers(1, n_generators + 1)  # 1..n_generators
        s = 1 if rng.random() < 0.5 else -1
        out.append(int(s * g))
    return out

def apply_braid(sigmas, word):
    dim = sigmas[0].shape[0]
    U = np.eye(dim, dtype=complex)
    from numpy.linalg import inv
    invs = [np.linalg.inv(S) for S in sigmas]
    for g in word:
        i = abs(g) - 1
        if g > 0:
            U = sigmas[i] @ U
        else:
            U = invs[i] @ U
    return U

def su2_from_u2(U):
    """Project U(2) matrix into SU(2)/center by pulling out an overall phase.

    Return SU(2) matrix (det = 1) and a global phase.  We do this on
    normalized det: phi = arg(det U)/2 ; U' = e^{-i phi} U.
    """
    detU = np.linalg.det(U)
    phi  = cmath.phase(detU) / 2
    Uprime = cmath.exp(-1j * phi) * U
    return Uprime, phi

def su2_haar_distances(samples, target):
    """Distance from target SU(2) matrix to each sample, using ||U - V||_F."""
    return np.array([np.linalg.norm(S - target) for S in samples])

def kolmogorov_smirnov_uniform(x):
    """One-sample KS statistic vs uniform on [0,1]."""
    x = np.sort(np.asarray(x))
    n = len(x)
    if n == 0:
        return None
    F_emp = np.arange(1, n + 1) / n
    return float(max(np.max(F_emp - x), np.max(x - (np.arange(0, n)) / n)))

# ------------------------------------------------------------------
# 7.  1-qubit gate approximation by brute-force braid search.
#     Verifies the "universality in action" claim on the smallest
#     nontrivial case.  We search braid words of length up to L on
#     B_3 through rho_{[2,1]} and see how well we can approximate
#     a chosen target unitary (Hadamard).
# ------------------------------------------------------------------

def gate_distance(U, T):
    """SU(2)/center distance: min over global phase of ||e^{i phi} U - T||_F."""
    # Optimal phi: e^{i phi} = tr(T^† U) / |tr(T^† U)|
    tr = np.trace(T.conj().T @ U)
    if abs(tr) < 1e-15:
        return float(np.linalg.norm(U - T))
    phi = cmath.phase(tr)
    return float(np.linalg.norm(cmath.exp(-1j * phi) * U - T))

def brute_force_approx(sigmas, target, max_len=10):
    """Search all braid words up to max_len for the best approximation to target.

    Returns (best_word, best_dist).  B_3 has 2 generators + 2 inverses.
    """
    invs = [np.linalg.inv(S) for S in sigmas]
    gens = list(range(1, len(sigmas) + 1)) + list(range(-len(sigmas), 0))
    # BFS with pruning.
    dim = sigmas[0].shape[0]
    best_dist = gate_distance(np.eye(dim, dtype=complex), target)
    best_word = []
    # DFS
    stack = [(np.eye(dim, dtype=complex), [])]
    steps = 0
    while stack:
        U, w = stack.pop()
        d = gate_distance(U, target)
        if d < best_dist:
            best_dist = d
            best_word = list(w)
        if len(w) >= max_len:
            continue
        for g in gens:
            # Avoid trivial cancellation.
            if w and w[-1] == -g:
                continue
            i = abs(g) - 1
            if g > 0:
                Unew = sigmas[i] @ U
            else:
                Unew = invs[i] @ U
            stack.append((Unew, w + [g]))
        steps += 1
    return best_word, best_dist, steps

# ------------------------------------------------------------------
# 8.  Reproduce the paper's *printed* rho_{[2,1]}(sigma_1) and check
#     the *printed* rho_{[2,1]}(sigma_2) is unitary as-is.
# ------------------------------------------------------------------

def paper_sigma2_lambda21():
    """The matrix printed by the paper (Section 3):
       rho_{[2,1],β,3}(σ_2) = [[ q^2/(q+1),  -q sqrt([3])/(q+1) ],
                              [ -q sqrt([3])/(q+1),   1/(q+1)  ]]  (with a minus per printed).

    Actually the printed matrix (see extraction) is:
       [ q^2/(q+1)          q sqrt([3])/(q+1)   ]
       [ -q sqrt([3])/(q+1)  -1/(q+1)           ]
    but the paper writes  q^2/(q+1) and -q sqrt([3])/(q+1) with the
    printed layout ambiguous.  We'll construct BOTH sign conventions
    and check which (if any) is unitary and which matches our
    computed rho(sigma_2).
    """
    q3 = qint(3)                          # [3] = q + q̄ + 1
    sq3 = cmath.sqrt(q3)
    denom = q + 1
    A = np.array([
        [ q**2 / denom,       -q * sq3 / denom ],
        [ -q * sq3 / denom,    1.0 / denom     ],  # sign per literal read
    ], dtype=complex)
    # Note the paper has a "−" on the last row of first column and on
    # the (2,2) entry; the printed layout is:
    #   [ q^2/(q+1)          q sqrt([3])/(q+1) ]     (with a bar over the sq3)
    #   [ -q sqrt([3])/(q+1)  -1/(q+1)         ]
    # Both readings are relevant; return several candidates.
    B = np.array([
        [ q**2 / denom,        q * sq3 / denom ],
        [ -q * sq3 / denom,   -1.0 / denom     ],
    ], dtype=complex)
    return {"reading_A": A, "reading_B": B}

# ------------------------------------------------------------------
# 9.  Run everything and emit a JSON report.
# ------------------------------------------------------------------

def main():
    t0 = time.time()
    report = {}

    # ---- C1: dimensions ----
    dims = {
        "V_3^1": dim_V_n_ell(3, 1),
        "V_3^3": dim_V_n_ell(3, 3),
        "V_6^0": dim_V_n_ell(6, 0),
        "V_6^2": dim_V_n_ell(6, 2),
    }
    paper_dims = {"V_3^1": 2, "V_3^3": 1, "V_6^0": 5, "V_6^2": 8}
    report["C1_dimensions"] = {
        "computed": dims,
        "paper":    paper_dims,
        "match":    dims == paper_dims,
    }
    print("[C1] dimensions:", dims, "match paper:", dims == paper_dims)

    # ---- Build reps for lambda = [2,1] (n=3), [3,3] (n=6), [4,2] (n=6) ----
    reps = {}
    for name, lam in [("21", (2, 1)), ("33", (3, 3)), ("42", (4, 2))]:
        tabs, Es, sigs = build_rep(lam)
        reps[name] = {"lam": lam, "tabs": tabs, "Es": Es, "sigmas": sigs}
        print(f"[build] lam=[{lam[0]},{lam[1]}] dim = {len(tabs)}")

    # Compare rep dims with paper's stated dims
    # lambda=[2,1]: 2   (matches dim V_{[2,1]} for B_3 case, corresponds to V_3^1 via Thm 3.2)
    # lambda=[3,3]: 5  (matches V_6^0 via Thm 3.2)
    # lambda=[4,2]: 8  (matches V_6^2 via Thm 3.2)
    report["C1b_rep_dimensions"] = {
        "lam_21": len(reps["21"]["tabs"]),
        "lam_33": len(reps["33"]["tabs"]),
        "lam_42": len(reps["42"]["tabs"]),
        "match_paper": {
            "lam_21_dim_2":  len(reps["21"]["tabs"]) == 2,
            "lam_33_dim_5":  len(reps["33"]["tabs"]) == 5,
            "lam_42_dim_8":  len(reps["42"]["tabs"]) == 8,
        }
    }

    # ---- C2: unitarity ----
    unit_report = {}
    for name, r in reps.items():
        u = [is_unitary(S) for S in r["sigmas"]]
        unit_report[name] = {
            "all_unitary": all(u),
            "per_generator": u,
            "max_deviation": max(float(np.linalg.norm(S.conj().T @ S - np.eye(S.shape[0])))
                                  for S in r["sigmas"]),
        }
    report["C2_unitarity"] = unit_report
    print("[C2] unitarity:", {k: v["all_unitary"] for k, v in unit_report.items()})

    # ---- C3: braid relations (and TL commuters where applicable) ----
    br_report = {}
    for name, r in reps.items():
        br = check_braid_relations(r["sigmas"])
        er = check_e_relations(r["Es"])
        br_report[name] = {
            "braid_all_ok":   all(x[1] for x in br),
            "braid_max_res":  max((x[2] for x in br), default=0.0),
            "TL_all_ok":      all(x[1] for x in er),
            "TL_max_res":     max((x[2] for x in er), default=0.0),
        }
    report["C3_braid_relations"] = br_report
    print("[C3] braid relations:", {k: v["braid_all_ok"] for k, v in br_report.items()})

    # ---- C4/C5: eigenvalues + multiplicities ----
    ev_report = {}
    for name, r in reps.items():
        checks = check_eigenvalues(r["sigmas"])
        ev_report[name] = checks
    report["C4C5_eigenvalues"] = ev_report
    # Explicit check of C5 (lambda=[4,2], mult(-1)=3, mult(q)=5)
    c5_ok = all(x["mult_-1"] == 3 and x["mult_q"] == 5
                for x in ev_report["42"])
    report["C5_lam42_multiplicities_3_and_5"] = c5_ok
    print("[C5] lam=[4,2] multiplicities 3,5 for every sigma_i:", c5_ok)

    # ---- C6: density via random braid sampling on lambda=[2,1], B_3 ----
    rng = np.random.default_rng(20260706)
    N_SAMPLES = 2000
    LEN = 30
    samples = []
    for _ in range(N_SAMPLES):
        w = sample_braid_word(2, LEN, rng)
        U = apply_braid(reps["21"]["sigmas"], w)
        Uprime, _ = su2_from_u2(U)
        samples.append(Uprime)

    # Distances between random pairs (should approximate Haar
    # measure's tr(X^† Y) distribution).
    idxs = rng.choice(N_SAMPLES, size=(200, 2), replace=True)
    pair_dists = []
    for i, j in idxs:
        pair_dists.append(gate_distance(samples[int(i)], samples[int(j)]))
    pair_dists = np.array(pair_dists)

    # For SU(2)/center Haar, the trace distribution is well known.
    # We'll just check spread stats.
    density_stats = {
        "n_samples": N_SAMPLES,
        "word_length": LEN,
        "pair_dist_mean":  float(pair_dists.mean()),
        "pair_dist_std":   float(pair_dists.std()),
        "pair_dist_min":   float(pair_dists.min()),
        "pair_dist_max":   float(pair_dists.max()),
        "unique_traces":   int(len(set(round(np.trace(S).real, 4) for S in samples))),
    }
    # If sigma_1, sigma_2 generated a finite subgroup, unique traces
    # would be small (a couple of dozen).  For a dense image this
    # count should grow with N_SAMPLES.
    report["C6_density_sampling"] = density_stats
    print(f"[C6] density: N={N_SAMPLES} random braids of length {LEN} "
          f"gave {density_stats['unique_traces']} distinct SU(2) traces "
          f"(finite subgroup would give <30)")

    # ---- Universality-in-action: brute-force approx of Hadamard ----
    T = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
    best_word, best_dist, steps = brute_force_approx(reps["21"]["sigmas"], T, max_len=9)
    report["C6b_hadamard_approx"] = {
        "search_max_len": 9,
        "best_word":      best_word,
        "best_dist_Frobenius_SU2": best_dist,
        "search_states_explored":  steps,
    }
    print(f"[C6b] brute-force best Hadamard approx up to length 9: dist={best_dist:.5f} "
          f"word={best_word}")

    # ---- C7: cross-check the paper's printed matrix for lambda=[2,1] ----
    paper_variants = paper_sigma2_lambda21()
    paper_check = {}
    for name, M in paper_variants.items():
        u = is_unitary(M)
        paper_check[name] = {
            "unitary":        bool(u),
            "det":            complex(np.linalg.det(M)),
            "eigenvalues":    [complex(z) for z in np.linalg.eigvals(M)],
            "spectrum_is_{-1,q}": bool(
                sum(1 for z in np.linalg.eigvals(M) if abs(z - (-1)) < 1e-8) == 1
                and sum(1 for z in np.linalg.eigvals(M) if abs(z - q) < 1e-8) == 1
            ),
        }
    report["C7_paper_printed_sigma2_check"] = paper_check
    # Also verify our own sigma_1 has spectrum {-1, q}
    our_s1_eigs = np.linalg.eigvals(reps["21"]["sigmas"][0])
    report["C7_our_sigma1_eigs"] = [complex(z) for z in our_s1_eigs]
    print(f"[C7] paper printed sigma_2 (reading_A) unitary: {paper_check['reading_A']['unitary']}, "
          f"(reading_B) unitary: {paper_check['reading_B']['unitary']}")

    # ---- Save concrete matrices for the report ----
    matrices = {}
    for name, r in reps.items():
        matrices[name] = {
            "dim":     len(r["tabs"]),
            "sigmas":  [ [[complex(z).real, complex(z).imag] for z in row]
                          for S in r["sigmas"] for row in S ],
            # keep shape info
            "sigma_shapes": [S.shape[0] for S in r["sigmas"]],
        }

    report["runtime_seconds"] = time.time() - t0

    # ---- Write JSON ----
    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "fkw_results.json"), "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"[done] wrote fkw_results.json (runtime {report['runtime_seconds']:.2f}s)")

    return report

if __name__ == "__main__":
    main()
