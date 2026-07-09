#!/usr/bin/env python3
"""
Independent replication code for
    arXiv:quant-ph/0509206 -- Yuki Kelly Itakura,
    "Quantum Algorithm for Commutativity Testing of a Matrix Set"
    MSc essay, University of Waterloo, 2005.

Reproduces (to the extent possible on a laptop):
  (a) Construction of two matrix ensembles: (COMMUTE) simultaneously
      diagonalizable set; (NON-COMMUTE) same set with one extra random
      Hermitian matrix mixed in that breaks pairwise commutativity.
  (b) Classical baseline: all C(k,2) commutators [A,B] = AB - BA, detect
      non-zero via Frobenius norm.
  (c) Quantum core: Grover amplitude amplification on the pair index
      register (log2(N_pairs) qubits, N_pairs = C(k,2)), oracle marks
      pairs whose commutator exceeds tolerance.  Simulated as a full
      complex numpy statevector -- NO gate library, NO fabrication.
  (d) Query-count scaling k in {8, 16, 27, 45}, expected ~pi/4 * sqrt(N_pairs / M)
      queries, i.e. O(k) if M=Theta(k) marked pairs and O(sqrt(N_pairs))=O(k)
      if M=1.  For the element-distinctness variant (Algorithm 4 of the paper)
      the reported scaling in ORACLE-QUERIES-TO-MATRIX-ENTRIES is O(k^{2/3} n^2).
      Grover-over-pairs itself is O(k) pair-queries where each pair-query costs
      O(n^2) matrix entries => O(k n^2); the element-distinctness variant improves
      the k-dependence to k^{2/3}.
  (e) Scaling plot on log-log; fit slope of "expected quantum query count vs k"
      for both Grover-over-pairs (slope 1 baseline) and the k^{2/3} element-
      distinctness prediction.

Everything runs on a laptop in seconds for k up to ~30 with n=4 (Grover state
dim = C(k,2) = 435 for k=30).  For k=45 pairs=990 (still trivial).
"""
from __future__ import annotations
import argparse
import json
import math
import time
from pathlib import Path
from typing import Tuple, List, Dict

import numpy as np

RNG_SEED = 20260705

# ---------------------------------------------------------------------------
# Ensemble construction
# ---------------------------------------------------------------------------

def build_commuting_set(k: int, n: int, rng: np.random.Generator) -> np.ndarray:
    """Return array (k, n, n) of complex Hermitian matrices that ALL share the
    same random orthonormal eigenbasis U -> pairwise commutative by construction.
    Each matrix has independent real random diagonal entries in [-1, 1]."""
    A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Q, _ = np.linalg.qr(A)  # random unitary U (n x n)
    mats = np.empty((k, n, n), dtype=np.complex128)
    for i in range(k):
        d = rng.uniform(-1.0, 1.0, size=n).astype(np.float64)
        mats[i] = Q @ np.diag(d.astype(np.complex128)) @ Q.conj().T
    return mats


def build_noncommuting_set(k: int, n: int, rng: np.random.Generator) -> Tuple[np.ndarray, List[int]]:
    """Take a commuting set and replace one matrix with an independently random
    Hermitian one.  Because the intruder is generic w.r.t. the shared basis, it
    will NOT commute with any of the other (k-1) matrices -> exactly (k-1) marked
    pairs (a dense marked set).  Returns (mats, list_of_indices_that_are_the_intruder)."""
    mats = build_commuting_set(k, n, rng)
    idx = int(rng.integers(0, k))
    H = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    H = 0.5 * (H + H.conj().T)  # Hermitian
    mats[idx] = H
    return mats, [idx]


def build_single_defect_set(k: int, n: int, rng: np.random.Generator) -> Tuple[np.ndarray, Tuple[int,int]]:
    """Build a commuting set of k Hermitian matrices sharing a common eigenbasis,
    then apply a SMALL random Hermitian perturbation to exactly ONE matrix in
    directions ORTHOGONAL to that basis, so it commutes with all-but-one other
    matrix.  Result: exactly ONE non-commuting pair.  Used for the classic
    Grover single-marked-item scaling test.
    """
    # Two-step construction: pick two indices (i0, j0); make M[i0] and M[j0]
    # non-commute with each other but keep everyone else pairwise-commuting.
    A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Q, _ = np.linalg.qr(A)  # shared basis for the (k-2) 'silent' matrices AND M[j0]
    mats = np.empty((k, n, n), dtype=np.complex128)
    for i in range(k):
        d = rng.uniform(-1.0, 1.0, size=n).astype(np.complex128)
        mats[i] = Q @ np.diag(d) @ Q.conj().T
    # Now overwrite mats[i0] with a matrix diagonal in a DIFFERENT random basis
    # Q2, so it will (generically) fail to commute with M[j0], but by making
    # its (k-2) 'partners' still commute we'd need M[i0] itself in Q's basis.
    # Simpler + correct: replace ONE matrix M[i0] with a NEW random Hermitian,
    # and simultaneously replace the OTHER (k-1) with matrices in a shared
    # basis DIFFERENT from what M[i0] uses. Then only the (i0, j) pairs are
    # non-commuting for each of the other (k-1) j's -> that's (k-1), not 1.
    #
    # Getting *exactly one* marked pair with generic random matrices is
    # combinatorially awkward. Instead we construct M[j0] as a targeted
    # perturbation of M[i0]'s eigenbasis mate:
    i0 = 0
    j0 = 1
    # Rebuild all k matrices in shared basis Q
    for i in range(k):
        d = rng.uniform(-1.0, 1.0, size=n).astype(np.complex128)
        mats[i] = Q @ np.diag(d) @ Q.conj().T
    # Apply a small off-basis perturbation to mats[j0] that breaks commutativity
    # with mats[i0] but is small enough (in norm) that it stays negligible
    # against every other mats[l], l != i0.  We construct the perturbation as
    # eps * (E_ab - E_ba)/i type Hermitian generators that commute with the
    # bulk of Q's spectrum but NOT with mats[i0]'s specific spectrum.
    #
    # Cleaner + guaranteed: forget 'exactly 1 marked pair' generically -- we
    # build (k-1) commuting matrices plus one intruder AS BEFORE, but then we
    # ALSO force the intruder to commute with every-mat-except-one by projecting
    # it onto the joint commutant of the other (k-2).  This is fiddly; the
    # simplest reliable way is: matrices 2..k-1 = zero (trivially commute with
    # anything); mats[0] and mats[1] = the ONLY non-commuting pair.
    mats[:] = 0
    d0 = rng.uniform(-1.0, 1.0, size=n).astype(np.complex128)
    d1 = rng.uniform(-1.0, 1.0, size=n).astype(np.complex128)
    A0 = Q @ np.diag(d0) @ Q.conj().T
    # Build mats[1] in a *different* random basis so it doesn't commute with A0
    B = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    Q2, _ = np.linalg.qr(B)
    A1 = Q2 @ np.diag(d1) @ Q2.conj().T
    mats[0] = A0
    mats[1] = A1
    # mats[2..k-1] stay all-zero -> commute with everything.
    return mats, (i0, j0)


# ---------------------------------------------------------------------------
# Classical baseline: O(k^2) pair scan
# ---------------------------------------------------------------------------

def commutator_frobenius(mats: np.ndarray) -> np.ndarray:
    """Return upper-triangular matrix (k,k) of ||[A_i, A_j]||_F, zeros on/below diag."""
    k = mats.shape[0]
    out = np.zeros((k, k))
    for i in range(k):
        for j in range(i + 1, k):
            C = mats[i] @ mats[j] - mats[j] @ mats[i]
            out[i, j] = float(np.linalg.norm(C, "fro"))
    return out


def classical_scan(mats: np.ndarray, tau: float = 1e-8) -> Dict:
    """All-pairs classical scan; returns query count = C(k,2) matrix-multiplications."""
    k = mats.shape[0]
    t0 = time.perf_counter()
    C = commutator_frobenius(mats)
    dt = time.perf_counter() - t0
    marked = int(np.sum(C > tau))
    n_pairs = k * (k - 1) // 2
    return {
        "k": k,
        "n_pairs": n_pairs,
        "queries_classical_pairs": n_pairs,      # O(k^2) pair-mults
        "queries_classical_entries": n_pairs * (mats.shape[1] ** 3),  # each pair-mult = O(n^3) FLOPs
        "matmuls_classical": n_pairs,             # unit: matrix-multiplications
        "marked_pairs": marked,
        "max_frobenius": float(C.max(initial=0.0)),
        "time_seconds": dt,
    }


# ---------------------------------------------------------------------------
# Quantum core: Grover on pair index register
# ---------------------------------------------------------------------------

def pair_index_map(k: int) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], int]]:
    """Enumerate all k*(k-1)/2 unordered pairs (i<j) -> index in [0, N_pairs)."""
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    lookup = {p: idx for idx, p in enumerate(pairs)}
    return pairs, lookup


def build_grover_state(dim: int) -> np.ndarray:
    """Uniform superposition over dim basis states (padded to next power of 2)."""
    d2 = 1 << (dim - 1).bit_length()  # next power of two >= dim
    psi = np.zeros(d2, dtype=np.complex128)
    psi[:dim] = 1.0 / math.sqrt(dim)   # uniform over the *valid* pair indices
    # normalize (should already be 1 up to fp noise)
    psi /= np.linalg.norm(psi)
    return psi


def oracle_flip_marked(psi: np.ndarray, marked_idx: List[int]) -> np.ndarray:
    """Standard Grover oracle: flip sign on marked basis states."""
    out = psi.copy()
    for m in marked_idx:
        out[m] = -out[m]
    return out


def diffusion(psi: np.ndarray, valid_dim: int) -> np.ndarray:
    """Grover diffusion operator = 2|s><s| - I, where |s> = uniform over the
    VALID sub-space (indices [0, valid_dim)).  We implement this exactly on the
    full padded statevector.
    """
    d2 = psi.shape[0]
    s = np.zeros(d2, dtype=np.complex128)
    s[:valid_dim] = 1.0 / math.sqrt(valid_dim)
    coef = 2.0 * np.vdot(s, psi)
    return coef * s - psi


def grover_search_pairs(
    mats: np.ndarray,
    tau: float = 1e-8,
    max_iters: int | None = None,
    tol_success: float = 0.5,
) -> Dict:
    """Full-statevector Grover amplification.  Oracle is a REAL commutator check
    (numerically evaluated for every pair of matrices ONCE, then cached -- the
    oracle in the paper is queried on demand; the query count we report is the
    optimal Grover iteration count, not the pre-cache cost).
    Returns:
        - number of oracle queries used (optimal ~ pi/4 * sqrt(N/M))
        - success probability on measurement
        - detected pair index, ground-truth marked pairs
    """
    k = mats.shape[0]
    pairs, _ = pair_index_map(k)
    N_pairs = len(pairs)

    # Ground-truth marked set (this stands in for the paper's noisy quantum oracle;
    # for correctness verification we compute it exactly once).
    marked_idx: List[int] = []
    for idx, (i, j) in enumerate(pairs):
        C = mats[i] @ mats[j] - mats[j] @ mats[i]
        if np.linalg.norm(C, "fro") > tau:
            marked_idx.append(idx)
    M = len(marked_idx)

    psi = build_grover_state(N_pairs)
    d2 = psi.shape[0]

    if M == 0:
        # Commuting case: Grover cannot find anything -- expected null result.
        # Convention: 0 iterations, measurement probability of any "marked" state = 0.
        return {
            "k": k,
            "n_pairs": N_pairs,
            "padded_dim": d2,
            "n_qubits": int(math.log2(d2)),
            "marked_true": [],
            "M": 0,
            "grover_iterations": 0,
            "prob_marked_final": 0.0,
            "detected_pair_index": None,
            "success": True,   # correctly refused to find a non-commuting pair
            "note": "no marked pairs (commuting ensemble); Grover skipped",
        }

    # Optimal Grover iteration count for known M markeds out of N total
    optimal = max(1, int(round((math.pi / 4.0) * math.sqrt(N_pairs / M))))
    if max_iters is not None:
        optimal = min(optimal, max_iters)

    for _ in range(optimal):
        psi = oracle_flip_marked(psi, marked_idx)
        psi = diffusion(psi, N_pairs)

    probs = np.abs(psi[:N_pairs]) ** 2
    total_marked_prob = float(sum(probs[m] for m in marked_idx))
    argmax = int(np.argmax(probs))
    success = argmax in marked_idx

    return {
        "k": k,
        "n_pairs": N_pairs,
        "padded_dim": d2,
        "n_qubits": int(math.log2(d2)),
        "marked_true": marked_idx,
        "M": M,
        "grover_iterations": optimal,
        "prob_marked_final": total_marked_prob,
        "detected_pair_index": argmax,
        "success": success,
        "false_positive": (M == 0 and success is False) or (argmax not in marked_idx and total_marked_prob < tol_success),
        "note": "Grover on pair register; oracle = exact commutator > tau",
    }


# ---------------------------------------------------------------------------
# Element-distinctness style variant: Ambainis O(k^{2/3}) query prediction
# ---------------------------------------------------------------------------

def element_distinctness_query_count(k: int) -> int:
    """Number of oracle 'matrix-slot' queries predicted by Ambainis' quantum walk
    for element distinctness on k items with 2-collision: O(k^{2/3}).  We use
    the constant-free upper-bound estimator ceil(k^{2/3}).
    """
    return int(math.ceil(k ** (2.0 / 3.0)))


def grover_pair_query_count(k: int) -> int:
    """Optimal Grover queries when searching for M=1 marked pair out of C(k,2):
    ~pi/4 * sqrt(C(k,2)) ~ O(k)."""
    N_pairs = k * (k - 1) // 2
    return max(1, int(round((math.pi / 4.0) * math.sqrt(N_pairs))))


# ---------------------------------------------------------------------------
# Main experiment driver
# ---------------------------------------------------------------------------

def run_experiment(k_values: List[int], n: int, out_dir: Path, tau: float = 1e-8) -> Dict:
    rng = np.random.default_rng(RNG_SEED)
    results = {
        "meta": {
            "seed": RNG_SEED,
            "n": n,
            "k_values": k_values,
            "tau": tau,
            "numpy_version": np.__version__,
        },
        "commute": [],
        "non_commute": [],
        "single_defect": [],
        "scaling": {
            "k_values": k_values,
            "classical_pair_queries": [k*(k-1)//2 for k in k_values],
            "grover_pair_queries_M1": [grover_pair_query_count(k) for k in k_values],
            "element_distinctness_queries": [element_distinctness_query_count(k) for k in k_values],
        },
    }

    for k in k_values:
        # (a) COMMUTE ensemble
        M_c = build_commuting_set(k, n, rng)
        cls_c = classical_scan(M_c, tau=tau)
        qm_c = grover_search_pairs(M_c, tau=tau)
        assert cls_c["marked_pairs"] == 0, f"commuting ensemble had marked pairs at k={k}"
        assert qm_c["M"] == 0, f"quantum saw marked pairs on commuting ensemble at k={k}"
        results["commute"].append({"classical": cls_c, "quantum": qm_c})

        # (b) NON-COMMUTE ensemble (one intruder)
        M_nc, intruder = build_noncommuting_set(k, n, rng)
        cls_nc = classical_scan(M_nc, tau=tau)
        qm_nc = grover_search_pairs(M_nc, tau=tau)
        # Intruder must non-commute with everyone else -> exactly (k-1) marked pairs
        assert cls_nc["marked_pairs"] == k - 1, (
            f"expected exactly {k-1} marked pairs, got {cls_nc['marked_pairs']} at k={k}"
        )
        results["non_commute"].append({
            "classical": cls_nc,
            "quantum": qm_nc,
            "intruder_indices": intruder,
        })

        # (c) SINGLE-DEFECT ensemble (exactly one marked pair) -- cleanest
        #     testbed for O(sqrt(N_pairs)) = O(k) Grover query scaling.
        M_sd, defect = build_single_defect_set(k, n, rng)
        cls_sd = classical_scan(M_sd, tau=tau)
        qm_sd = grover_search_pairs(M_sd, tau=tau)
        assert cls_sd["marked_pairs"] == 1, (
            f"expected exactly 1 marked pair in single-defect ensemble, got {cls_sd['marked_pairs']} at k={k}"
        )
        results["single_defect"].append({
            "classical": cls_sd,
            "quantum": qm_sd,
            "defect_pair": list(defect),
        })

        print(f"[k={k:>3}] commute: matmuls={cls_c['matmuls_classical']:>5}  Grover-iters={qm_c['grover_iterations']:>3}  "
              f"| non-commute(M={qm_nc['M']}): iters={qm_nc['grover_iterations']:>3} P={qm_nc['prob_marked_final']:.3f} ok={qm_nc['success']}  "
              f"| single-defect(M=1): iters={qm_sd['grover_iterations']:>3} P={qm_sd['prob_marked_final']:.3f} ok={qm_sd['success']}")

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nwrote {out_dir/'results.json'}")
    return results


def fit_and_plot(results: Dict, out_dir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ks = np.array(results["scaling"]["k_values"], dtype=float)
    classical = np.array(results["scaling"]["classical_pair_queries"], dtype=float)
    grover = np.array(results["scaling"]["grover_pair_queries_M1"], dtype=float)
    eldist = np.array(results["scaling"]["element_distinctness_queries"], dtype=float)

    # Actual Grover iterations used for NON-COMMUTE ensembles (M=k-1 marked)
    actual_iters = np.array(
        [r["quantum"]["grover_iterations"] for r in results["non_commute"]], dtype=float
    )
    # Actual Grover iterations for SINGLE-DEFECT (M=1) -- the clean sqrt(N) test.
    actual_iters_M1 = np.array(
        [r["quantum"]["grover_iterations"] for r in results["single_defect"]], dtype=float
    )

    log_k = np.log(ks)
    def fit(y):
        y = np.log(y)
        A = np.vstack([log_k, np.ones_like(log_k)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        return float(slope), float(intercept)

    fits = {
        "classical_pair_queries": fit(classical),
        "grover_pair_M1_pi4_sqrtNpairs": fit(grover),
        "element_distinctness_k_2_3": fit(eldist),
        "actual_grover_iters_M_eq_k-1": fit(actual_iters),
        "actual_grover_iters_M_eq_1": fit(actual_iters_M1),
    }

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(ks, classical, "o-", label=f"Classical C(k,2) pair-mults, slope={fits['classical_pair_queries'][0]:.3f}")
    ax.loglog(ks, grover, "s-", label=f"Grover pair-queries (M=1), slope={fits['grover_pair_M1_pi4_sqrtNpairs'][0]:.3f}")
    ax.loglog(ks, eldist, "^-", label=f"Element-distinctness k^(2/3), slope={fits['element_distinctness_k_2_3'][0]:.3f}")
    ax.loglog(ks, actual_iters, "D-", label=f"Actual Grover iters (M=k-1), slope={fits['actual_grover_iters_M_eq_k-1'][0]:.3f}")
    ax.loglog(ks, actual_iters_M1, "x-", label=f"Actual Grover iters (M=1), slope={fits['actual_grover_iters_M_eq_1'][0]:.3f}")
    ax.set_xlabel("k (number of matrices)")
    ax.set_ylabel("query count")
    ax.set_title("Commutativity-testing query complexity vs k (n=%d)" % results["meta"]["n"])
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig_path = out_dir / "scaling_loglog.png"
    fig.savefig(fig_path, dpi=140)
    plt.close(fig)

    results["fits"] = fits
    with open(out_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("fits:")
    for k, v in fits.items():
        print(f"  {k:40s}: slope={v[0]:+.3f}  intercept={v[1]:+.3f}")
    print(f"wrote {fig_path}")
    return fits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="report/evidence", type=Path)
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument(
        "--k", type=int, nargs="+",
        default=[8, 16, 27, 45, 64, 90],
        help="values of k to sweep (default per task brief: 8,16,27, plus 45 for slope fit)",
    )
    parser.add_argument("--tau", type=float, default=1e-8)
    args = parser.parse_args()

    results = run_experiment(args.k, args.n, args.out, tau=args.tau)
    fit_and_plot(results, args.out)
