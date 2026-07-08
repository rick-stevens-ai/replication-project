"""
gsvd_reference.py
=================

Reference implementations of the GSVD (Alter-Brown-Botstein / Van Loan
formulation) and the HO-GSVD (Ponnapalli et al., PLoS ONE 2011), suitable
for replicating Alter et al. 2026 "Quantum mechanics-based multitensor
AI/ML" (APL Quantum 3, 026116) on TARGET-NBL WGS/RNA data.

Conventions
-----------
We follow the Alter-Brown-Botstein (PNAS 2003) / Van Loan (SIAM 1976)
form of the GSVD of two real matrices D1 (m1 x n) and D2 (m2 x n) with
the same column dimension (typically: rows = features, columns = patients,
so n = #patients shared across the two data types). The decomposition is:

    D1 = U1 . diag(S1) . V^T
    D2 = U2 . diag(S2) . V^T

with U1 (m1 x n), U2 (m2 x n) column-orthonormal, V (n x n) invertible
(NOT required to be orthonormal in the general GSVD; the "right basis"
is shared between the two decompositions), and the generalized singular
values are the pairs (S1[k], S2[k]) >= 0 with S1[k]^2 + S2[k]^2 = 1.

The shared right basis V is the key object: each column V[:, k] is a
shared "arraylet" / patient mode. The ratio S1[k] / S2[k] orders the
columns from "exclusive to D1" (ratio -> infinity) through "common"
(ratio ~ 1) to "exclusive to D2" (ratio -> 0). In the Alter et al. 2026
NBL analysis, V[:, k] is a 101-patient vector; the antisymmetric
patterns u1,1 (k=1, exclusive to D1=tumor) and u1,101 (k=101, exclusive
to D2=blood) become the two predictors. See Eqs. 3 and 13 of the paper.

Algorithm (stacked-QR + CS decomposition route)
-----------------------------------------------
The numerically stable construction (Paige & Saunders 1981; Bai & Demmel)
is:

  1. Stack    A = [[D1], [D2]]  (shape (m1+m2) x n).
  2. Thin QR  A = Q R,           Q (m1+m2) x n, R (n x n) upper-tri.
  3. Partition Q row-wise into Q1 (m1 x n) and Q2 (m2 x n).
  4. CS-decompose  Q1 = U1 C W^T,  Q2 = U2 S W^T, with C^2 + S^2 = I,
     C, S diagonal nonneg (this is scipy.linalg.cossin).
  5. Then  D1 = U1 (C W^T R) = U1 . diag(C) . (W^T R),
          D2 = U2 (S W^T R) = U2 . diag(S) . (W^T R).
     So V^T = W^T R, equivalently V = R^T W.

This yields D1 = U1 . diag(c) . V^T, D2 = U2 . diag(s) . V^T with
c = diag(C), s = diag(S), c^2 + s^2 = 1, V invertible (= R^T W).

`gsvd` below implements this. We verify (i) reconstruction error,
(ii) c^2 + s^2 = 1, (iii) U1, U2 column-orthonormal. The columns are
returned sorted by ratio c/s ascending (i.e. exclusive-to-D2 first,
common in the middle, exclusive-to-D1 last) so that "first" and "last"
columns correspond to the antisymmetric patterns the paper uses.

HO-GSVD (Ponnapalli et al. 2011)
--------------------------------
For N matrices D_i (m_i x n), i = 1..N, with shared column dimension n,
form the n x n matrices A_i = D_i^T D_i (assume full column rank). The
HO-GSVD common right basis V is defined as the eigenbasis of the
balanced "arithmetic vs harmonic" average

    S = (1 / (N (N-1))) * sum_{i < j} ( A_i A_j^{-1} + A_j A_i^{-1} )

Ponnapalli et al. prove (Theorem 2) that S has real nonnegative
eigenvalues all >= 1, that an eigenvalue equals exactly 1 iff the
corresponding right basis vector is in the "common HO-GSVD subspace"
(shared identically across all N matrices), and that in the N=2 case
this reduces to the classical GSVD. The eigenvectors of S form the
columns of V; then for each i we recover  B_i = D_i V (unnormalized
"left/expression" coordinates), Sigma_i = || B_i columns ||, and
U_i = B_i / Sigma_i (column-normalized). So

    D_i = U_i . diag(Sigma_i) . V^{-1}   (note V^{-1}, not V^T, for HO-GSVD).

`ho_gsvd` below implements this. It works for N >= 2 (and matches the
classical GSVD up to column scaling / ordering for N = 2).

References
----------
* Alter O, Brown PO, Botstein D. PNAS 2003;100(6):3351-6 (GSVD comparison
  of two genome-scale datasets).
* Van Loan CF. SIAM J. Numer. Anal. 13(1):76-83 (1976).
* Paige CC, Saunders MA. SIAM J. Numer. Anal. 18(3):398-405 (1981).
* Ponnapalli SP, Saunders MA, Van Loan CF, Alter O. PLoS ONE 2011;
  6(12):e28072 (HO-GSVD).
* Alter O, Newman E, Ponnapalli SP, Tsai JW. APL Quantum 3(2):026116
  (2026) (the paper being replicated).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from scipy.linalg import qr, svd


# ---------------------------------------------------------------------------
# Two-matrix GSVD
# ---------------------------------------------------------------------------

@dataclass
class GSVDResult:
    """Result of the Alter-Brown-Botstein / Van Loan GSVD.

    D1 = U1 . diag(c) . V.T
    D2 = U2 . diag(s) . V.T
    with c**2 + s**2 = 1, U1, U2 column-orthonormal, V invertible
    (n x n). Columns are sorted by ratio c/s ascending: column 0 is
    "exclusive to D2" (c ~ 0, s ~ 1), column n-1 is "exclusive to D1"
    (c ~ 1, s ~ 0). This matches the (u1,1, u1,101) "antisymmetric"
    convention of Alter et al. 2026.
    """

    U1: np.ndarray  # (m1, n)
    U2: np.ndarray  # (m2, n)
    c: np.ndarray   # (n,) generalized singular values of D1
    s: np.ndarray   # (n,) generalized singular values of D2
    V: np.ndarray   # (n, n) shared right basis (rows are right vectors via V.T)

    @property
    def ratio(self) -> np.ndarray:
        """Generalized singular-value ratio c/s (handles s=0 -> inf)."""
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(self.s > 0, self.c / np.maximum(self.s, 1e-300), np.inf)
        return r


def gsvd(D1: np.ndarray, D2: np.ndarray) -> GSVDResult:
    """Compute the GSVD of (D1, D2) sharing column dimension n.

    Parameters
    ----------
    D1 : (m1, n) array
    D2 : (m2, n) array

    Returns
    -------
    GSVDResult
        With  D1 = U1 . diag(c) . V.T  and  D2 = U2 . diag(s) . V.T.

    Notes
    -----
    Requires m1 + m2 >= n and that the stacked matrix has full column rank
    (the standard regularity condition for the GSVD).
    """
    D1 = np.asarray(D1, dtype=float)
    D2 = np.asarray(D2, dtype=float)
    m1, n = D1.shape
    m2, n2 = D2.shape
    if n != n2:
        raise ValueError(f"D1 and D2 must share column dimension; got {n} vs {n2}")
    if m1 + m2 < n:
        raise ValueError(
            f"Stacked matrix has fewer rows ({m1 + m2}) than columns ({n}); "
            "GSVD is rank-deficient in the standard form."
        )

    # 1. Stack and thin-QR.
    A = np.vstack([D1, D2])
    Q, R = qr(A, mode="economic")     # Q: (m1+m2, n), R: (n, n)
    Q1 = Q[:m1, :]                    # (m1, n)
    Q2 = Q[m1:, :]                    # (m2, n)

    # 2. Thin CS decomposition of the column-orthonormal stack [Q1; Q2],
    #    done elementarily (no dependence on scipy.linalg.cossin, which
    #    only accepts square inputs):
    #
    #      Q1 = U1_thin . diag(c) . W^T            (thin SVD of Q1)
    #      Q2 W = U2_thin . diag(s)                (orthonormalize)
    #
    #    Because [Q1; Q2] has orthonormal columns, c**2 + s**2 = 1
    #    elementwise (up to floating point). When some c_k or s_k equals 0
    #    we extend the corresponding U column by an orthonormal completion.
    Uq1, c_raw, Wt = svd(Q1, full_matrices=False)   # Uq1 (m1, n), c_raw (n,), Wt (n, n)
    W = Wt.T                                         # (n, n) orthonormal
    # Numerical safety: clip tiny negatives + values > 1 caused by float noise.
    c = np.clip(c_raw, 0.0, 1.0)
    s2 = np.clip(1.0 - c ** 2, 0.0, 1.0)
    s = np.sqrt(s2)
    U1 = Uq1                                          # (m1, n) col-orthonormal

    # Build U2 from Q2 W, normalizing each column to magnitude s_k. For
    # columns with s_k = 0 (i.e. c_k = 1), Q2 W[:, k] is the zero vector; we
    # patch in any unit vector from an orthonormal completion so U2 stays
    # column-orthonormal (it doesn't affect the decomposition since the
    # corresponding diagonal entry is 0).
    Q2W = Q2 @ W                                      # (m2, n)
    U2 = np.zeros_like(Q2W)
    eps_s = 1e-12 * max(1.0, float(np.max(np.abs(Q2W))))
    nonzero = s > eps_s
    if np.any(nonzero):
        U2[:, nonzero] = Q2W[:, nonzero] / s[nonzero]
    if np.any(~nonzero):
        # Re-orthonormalize the zero-norm columns against the nonzero ones.
        if np.any(nonzero):
            U2_nz = U2[:, nonzero]
            for k in np.where(~nonzero)[0]:
                v = np.zeros(m2)
                # Pick a basis direction not already covered.
                idx_candidates = list(range(m2))
                for j in idx_candidates:
                    cand = np.zeros(m2)
                    cand[j] = 1.0
                    proj = U2_nz @ (U2_nz.T @ cand)
                    cand = cand - proj
                    nrm = np.linalg.norm(cand)
                    if nrm > 1e-8:
                        v = cand / nrm
                        break
                U2[:, k] = v
                U2_nz = np.column_stack([U2_nz, v])
        else:
            # All s_k are zero (degenerate); just give U2 any orthonormal
            # basis of size n in R^{m2}.
            U2, _ = np.linalg.qr(np.eye(m2, n))

    # 3. Recover the shared right basis V from V^T = W^T R, i.e. V = R^T W.
    V = R.T @ W                                       # (n, n) invertible

    # 4. Sort by ratio c/s ascending so that column 0 = "exclusive to D2",
    #    column n-1 = "exclusive to D1".
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(s > 1e-15, c / np.maximum(s, 1e-300), np.inf)
    order = np.argsort(ratio, kind="stable")
    c = c[order]
    s = s[order]
    U1 = U1[:, order]
    U2 = U2[:, order]
    V = V[:, order]

    return GSVDResult(U1=U1, U2=U2, c=c, s=s, V=V)


# ---------------------------------------------------------------------------
# Higher-Order GSVD (Ponnapalli 2011)
# ---------------------------------------------------------------------------

@dataclass
class HOGSVDResult:
    """Result of the HO-GSVD on N matrices D_i (m_i x n).

    For each i:
        D_i = U_i . diag(Sigma_i) . V^{-1}
    with V (n x n) invertible (eigenbasis of the balanced average S),
    U_i (m_i x n) column-normalized.
    """

    U: List[np.ndarray]
    Sigma: List[np.ndarray]
    V: np.ndarray
    Vinv: np.ndarray
    eigenvalues: np.ndarray  # eigenvalues of the balanced average S


def ho_gsvd(matrices: List[np.ndarray]) -> HOGSVDResult:
    """Higher-order GSVD of N >= 2 matrices sharing column dimension n.

    Implementation follows Ponnapalli, Saunders, Van Loan, Alter
    (PLoS ONE 2011) Eq. 3 / Theorem 2: form

        S = 1 / (N (N-1)) * sum_{i<j} ( A_i A_j^{-1} + A_j A_i^{-1} ),
        A_i = D_i^T D_i,

    eigendecompose S to get the shared right basis V, then
    U_i = D_i V / column_norm,  Sigma_i = column_norm.

    Parameters
    ----------
    matrices : list of (m_i, n) arrays. Must all share the same n. Each
        D_i should have full column rank n (m_i >= n typically). The
        method is well-defined whenever every A_i is invertible.

    Returns
    -------
    HOGSVDResult
    """
    if len(matrices) < 2:
        raise ValueError("HO-GSVD needs N >= 2 matrices.")
    Ds = [np.asarray(D, dtype=float) for D in matrices]
    n = Ds[0].shape[1]
    for k, D in enumerate(Ds):
        if D.shape[1] != n:
            raise ValueError(f"matrix {k} has column dim {D.shape[1]}, expected {n}.")

    N = len(Ds)
    As = [D.T @ D for D in Ds]
    # Invert each A_i (use solve for stability).
    Ainvs = []
    for k, A in enumerate(As):
        try:
            Ainvs.append(np.linalg.solve(A, np.eye(n)))
        except np.linalg.LinAlgError as e:
            raise np.linalg.LinAlgError(
                f"HO-GSVD: A_{k} = D_{k}^T D_{k} is singular; matrix {k} "
                "does not have full column rank."
            ) from e

    S = np.zeros((n, n))
    for i in range(N):
        for j in range(i + 1, N):
            S = S + As[i] @ Ainvs[j] + As[j] @ Ainvs[i]
    S = S / (N * (N - 1))

    # Eigendecompose S. By Ponnapalli Thm 2, eigenvalues are real >= 1
    # for full-rank input; in finite precision they can be slightly
    # complex / slightly below 1. Strategy:
    #   - If S is numerically symmetric (within tolerance), use eigh on
    #     (S + S^T) / 2 to get a real orthonormal eigenbasis. This is the
    #     case in particular when all D_i share the same Gram matrix, in
    #     which case S = I and any orthonormal basis is valid.
    #   - Else use np.linalg.eig and project to real at the noise floor.
    sym_err = float(np.max(np.abs(S - S.T))) / max(1.0, float(np.max(np.abs(S))))
    if sym_err < 1e-8:
        S_sym = 0.5 * (S + S.T)
        eigvals, V = np.linalg.eigh(S_sym)   # eigenvalues ascending, V orthonormal
    else:
        eigvals, V = np.linalg.eig(S)
        if np.max(np.abs(eigvals.imag)) < 1e-6 * (np.max(np.abs(eigvals.real)) + 1e-12):
            eigvals = eigvals.real
            V = V.real
        order = np.argsort(eigvals.real if np.iscomplexobj(eigvals) else eigvals,
                           kind="stable")
        eigvals = eigvals[order]
        V = V[:, order]

    # Recover U_i, Sigma_i from D_i V.
    try:
        Vinv = np.linalg.inv(V)
    except np.linalg.LinAlgError as e:
        raise np.linalg.LinAlgError(
            "HO-GSVD: shared right basis V is singular (degenerate eigenspace)."
        ) from e

    Us = []
    Sigmas = []
    for D in Ds:
        B = D @ V                                # (m_i, n)
        norms = np.linalg.norm(B, axis=0)
        norms_safe = np.where(norms > 0, norms, 1.0)
        U = B / norms_safe
        Us.append(U)
        Sigmas.append(norms)

    return HOGSVDResult(U=Us, Sigma=Sigmas, V=V, Vinv=Vinv, eigenvalues=eigvals)


# ---------------------------------------------------------------------------
# Antisymmetric / symmetric pattern selection (Alter et al. 2026, NBL)
# ---------------------------------------------------------------------------

def antisymmetric_patterns(result: GSVDResult) -> Tuple[int, int]:
    """Return (k_first, k_last) indices into the GSVD result that are the
    "antisymmetric" patterns the paper uses as predictors.

    In the GSVDResult returned by `gsvd`, columns are sorted by ratio
    c/s ascending. The "first" predictor (u1,1 in the paper, paired with
    D1 = tumor genome) corresponds to the column most exclusive to D1
    (ratio -> infinity), i.e. the LAST column n-1. The "last" predictor
    (u1,101 in the paper, paired with D2 = blood genome) corresponds to
    the column most exclusive to D2, i.e. the FIRST column 0.

    NOTE on naming: the paper's "u1,1" and "u1,101" are the first and
    last *left* arraylets of the GSVD using the paper's own ordering
    convention (most-exclusive-to-D1 first, most-exclusive-to-D2 last).
    We invert that ordering inside `gsvd` so that our column 0 is "least
    D1, most D2" and column n-1 is "most D1, least D2". Hence:

        u1,1   (paper, exclusive-to-tumor)   -> our column n - 1 -> k_first
        u1,101 (paper, exclusive-to-blood)   -> our column 0     -> k_last

    Returns
    -------
    (k_first, k_last) : Tuple[int, int]
        Indices into result.U1, result.U2, result.V, result.c, result.s.
    """
    n = result.V.shape[1]
    k_first = n - 1   # most exclusive to D1
    k_last = 0        # most exclusive to D2
    return k_first, k_last


def classify_patients(arraylet: np.ndarray) -> np.ndarray:
    """Two-class (low vs high) patient classification by sign of the
    right-basis arraylet, matching the paper's "antisymmetric pattern"
    predictor scoring.

    Parameters
    ----------
    arraylet : (n_patients,) array
        A single column of the shared right basis V (i.e. V[:, k]) or,
        equivalently, the patient-mode coordinate vector for a chosen
        GSVD column.

    Returns
    -------
    labels : (n_patients,) int array of 0 / 1
        0 for patients with arraylet[i] <= 0, 1 for arraylet[i] > 0.
        This binary classification is what is fed into Kaplan-Meier /
        log-rank / Cox in `survival_stats`.
    """
    arraylet = np.asarray(arraylet, dtype=float)
    return (arraylet > 0).astype(int)


def combine_predictors(arraylet_first: np.ndarray,
                       arraylet_last: np.ndarray) -> np.ndarray:
    """Combine the "first" and "last" antisymmetric patterns into a single
    3-class predictor, following the paper's "Tumor DNA 1+101" combined
    classifier.

    The paper splits patients into three groups by joint sign of the two
    arraylets:
        - low  : both arraylets negative
        - mid  : signs disagree
        - high : both arraylets positive
    We return integer labels 0 / 1 / 2 to be passed to log-rank /
    multi-arm Cox.

    Parameters
    ----------
    arraylet_first : (n_patients,) array
    arraylet_last  : (n_patients,) array

    Returns
    -------
    labels : (n_patients,) int array in {0, 1, 2}.
    """
    a = np.asarray(arraylet_first, dtype=float)
    b = np.asarray(arraylet_last, dtype=float)
    if a.shape != b.shape:
        raise ValueError("arraylet shapes must match")
    pos_a = a > 0
    pos_b = b > 0
    labels = np.zeros_like(a, dtype=int)
    labels[(~pos_a) & (~pos_b)] = 0
    labels[pos_a ^ pos_b] = 1
    labels[pos_a & pos_b] = 2
    return labels
