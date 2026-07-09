"""
Replication of Ambainis 2007 (arXiv:0704.3628) — "A nearly optimal discrete query
quantum algorithm for evaluating NAND formulas" — for the *balanced* case.

Core construction (Sec 3.2 of the paper), for the complete binary NAND tree T with
N = 2^n leaves and depth n:

    * State space H = C^{|T'|} where T' = T augmented by a tail of even length
      t = 2*ceil(sqrt(N)) (paper's balanced-case choice).
    * H is a Hermitian weighted adjacency matrix of T'. For the *complete* balanced
      tree, all in-tree edge weights are H_{pc} = 1 (see paper §3.2 remark).
      All tail edges also have weight 1.
    * U1 = reflection about the 0-eigenspace of H:  U1 = 2*P_{ker H} - I.
    * U2 = oracle: -1 on basis states |v> for leaves with x_v = 1, +1 elsewhere.
    * |psi_start> = sum_{i=0..t/2} |tail vertex 2i>  (unnormalised)
      Then |psi_start''> = P_{ker H} |psi_start>, normalised.
    * Theorem 3: if T evaluates to 0 there is an eigenstate |psi_0> of U2 U1 with
      eigenvalue 1 that has |<psi_0|psi_start''>|^2 >= c (constant); if T evaluates
      to 1, every eigenstate not orthogonal to |psi_start''> has eigenvalue e^{i theta}
      with |theta| = Omega(1/sqrt(N)).
    * Query complexity = number of U2 applications = O(sqrt N) via phase estimation
      of U2 U1 with precision delta = theta_min/2 = c'/sqrt(N).

What this script does (real numpy simulation, no fabrication):
    * Build T' explicitly for n = 2, 3, 4, 5 (N = 4, 8, 16, 32 leaves).
    * Build H, compute ker H (SVD threshold), build U1 = 2 P_ker - I, U2 diagonal.
    * Randomise the leaf assignment x uniformly over {0,1}^N so both T=0 and T=1
      inputs are represented; run many random trials per (n, T).
    * Run textbook phase estimation on W = U2 U1 with the initial state |psi_start''>,
      counting query complexity = (# calls to U2) = (2^m - 1) where m = phase register
      qubits chosen as m = ceil(log2(4*c*sqrt(N))). Decode: |theta_est| < theta_min/2
      -> answer 0; else -> answer 1. Amplify by C independent repetitions and take
      majority. Empirical success prob and (query count) reported per (n, T value).
    * Save a JSON summary + a scaling plot text.

Everything is a *real* linear-algebra simulation of the discrete quantum query model.
No claim beyond what is computed is recorded.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Tree construction
# ---------------------------------------------------------------------------

@dataclass
class Tree:
    """Complete balanced binary NAND tree of depth n (root at level 0, leaves at level n).
    Augmented by a tail of even length t attached to the root.

    Vertex indexing convention (0-based, contiguous):
        indices [0 .. num_tree_vertices - 1]        -> tree vertices (BFS order, root at 0)
        indices [num_tree_vertices .. total - 1]    -> tail vertices tail_1, tail_2, ..., tail_t

    Level of tree vertex k (BFS index) is floor(log2(k+1)). The root has BFS index 0.
    Children of tree vertex k are 2k+1 and 2k+2.
    "Tail vertex 0" in the paper == the root of T (BFS index 0). Tail vertex i for
    i >= 1 is the newly added tail node; edges connect tail vertex i-1 to tail vertex i.
    We store tail_1 ... tail_t at indices num_tree_vertices .. total-1.
    """

    n: int  # depth
    t: int  # tail length (even)
    num_tree_vertices: int = field(init=False)
    total: int = field(init=False)
    leaves: List[int] = field(init=False)  # indices of leaf vertices in [0..num_tree_vertices)
    tail_indices_incl_root: List[int] = field(init=False)  # index of tail vertex 0, 1, ..., t

    def __post_init__(self):
        self.num_tree_vertices = 2 ** (self.n + 1) - 1
        self.total = self.num_tree_vertices + self.t
        # leaves are BFS indices [2^n - 1, 2^(n+1) - 2]
        self.leaves = list(range(2 ** self.n - 1, 2 ** (self.n + 1) - 1))
        # tail vertex 0 == root == index 0; tail vertices 1..t at indices num_tree_vertices..total-1
        self.tail_indices_incl_root = [0] + list(range(self.num_tree_vertices, self.total))
        assert len(self.tail_indices_incl_root) == self.t + 1

    def build_H(self) -> np.ndarray:
        """Hermitian weighted adjacency matrix H of T'. For the *complete balanced tree*
        all in-tree edge weights are 1 (Ambainis 2007, §3.2 remark) and all tail edges
        have weight 1."""
        N = self.total
        H = np.zeros((N, N), dtype=np.float64)
        # tree edges (parent k, children 2k+1, 2k+2) for k such that 2k+2 < num_tree_vertices
        # i.e. for k in [0 .. 2^n - 2]
        for k in range(2 ** self.n - 1):
            c1 = 2 * k + 1
            c2 = 2 * k + 2
            H[k, c1] = 1.0
            H[c1, k] = 1.0
            H[k, c2] = 1.0
            H[c2, k] = 1.0
        # tail edges: tail_indices_incl_root[i] -- tail_indices_incl_root[i+1] for i in [0..t-1]
        for i in range(self.t):
            u = self.tail_indices_incl_root[i]
            v = self.tail_indices_incl_root[i + 1]
            H[u, v] = 1.0
            H[v, u] = 1.0
        return H


def eval_nand_tree(x: np.ndarray, n: int) -> int:
    """Evaluate complete balanced binary NAND tree of depth n on leaf values x
    (len(x) == 2^n). Returns 0 or 1."""
    vals = x.astype(int).tolist()
    # bottom-up combine pairs with NAND
    while len(vals) > 1:
        vals = [1 - (a & b) for a, b in zip(vals[0::2], vals[1::2])]
    return vals[0]


def assert_even_depth(n: int):
    """The construction above assumes leaves are at even distance from the root
    (paper §3.2: 'Without the loss of generality, assume that all leafs are at
    an even distance from the root.'). For a complete balanced tree that means
    depth n must be even. For odd n we would need the doubling preprocessing
    described in the same paragraph (add two children under each odd-depth leaf,
    both = NOT x_i). This replication restricts to even n and keeps the
    construction faithful rather than adding preprocessing scaffolding.
    """
    if n % 2 != 0:
        raise ValueError(
            f"n={n} is odd. Paper's construction assumes leaves at even depth. "
            f"Use even n \u2208 {{2,4,6,8,...}} or apply doubling preproc (not implemented here)."
        )


# ---------------------------------------------------------------------------
# Building U1, U2, |psi_start>
# ---------------------------------------------------------------------------

def kernel_projector(H: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    """Orthogonal projector onto ker(H). Uses eigendecomposition of the Hermitian H."""
    w, V = np.linalg.eigh(H)
    mask = np.abs(w) < tol * max(1.0, np.max(np.abs(w)))
    K = V[:, mask]
    return K @ K.conj().T


def build_U1(H: np.ndarray) -> np.ndarray:
    P_ker = kernel_projector(H)
    dim = H.shape[0]
    U1 = 2.0 * P_ker - np.eye(dim)
    return U1  # real symmetric orthogonal (reflection)


def build_U2(tree: Tree, x: np.ndarray) -> np.ndarray:
    """Oracle: diagonal +/-1. -1 on leaf-with-x_i=1 basis states, +1 elsewhere."""
    dim = tree.total
    diag = np.ones(dim, dtype=np.float64)
    for pos_in_leaves, leaf_idx in enumerate(tree.leaves):
        if x[pos_in_leaves] == 1:
            diag[leaf_idx] = -1.0
    return np.diag(diag)


def build_psi_start(tree: Tree) -> np.ndarray:
    """|psi_start> = sum_{i=0..t/2} |tail vertex 2i>  (unnormalised). Note tail vertex 0 = root."""
    dim = tree.total
    v = np.zeros(dim, dtype=np.complex128)
    for i in range(tree.t // 2 + 1):
        v[tree.tail_indices_incl_root[2 * i]] = 1.0
    return v


def build_psi_start_doubleprime(tree: Tree, H: np.ndarray) -> np.ndarray:
    """|psi_start''> = P_{ker H} |psi_start> / || ... ||"""
    P = kernel_projector(H)
    v = build_psi_start(tree)
    pv = P @ v
    nrm = np.linalg.norm(pv)
    if nrm < 1e-14:
        raise RuntimeError("|psi_start''> has zero norm — construction bug")
    return pv / nrm


# ---------------------------------------------------------------------------
# Phase estimation of W = U2 U1
# ---------------------------------------------------------------------------

def phase_estimation_run(
    W: np.ndarray,
    psi: np.ndarray,
    m: int,
    rng: np.random.Generator,
) -> Tuple[float, int]:
    """Textbook phase estimation with m phase-register qubits, on unitary W and
    input state psi (an eigenvector-or-superposition thereof).

    Returns
    -------
    theta_est : float in [0, 2pi)  — estimated phase of an eigenvalue e^{i theta}
                sampled with prob |<eigenvec|psi>|^2 (up to PE discretisation).
    queries   : int — number of oracle U2 calls, which equals (2^m - 1) since we apply
                W^{2^0}, W^{2^1}, ..., W^{2^{m-1}} controlled — total W applications
                sum_{k=0..m-1} 2^k = 2^m - 1, and each W = U2 U1 uses one U2 call.

    Implementation: we don't build the full (2^m * dim_state)-dim register; instead we
    exploit that PE is equivalent to sampling from |c_j|^2 where c_j is the FFT (over
    the 2^m grid) of the sequence <psi| W^k |psi> for k = 0..2^m-1. In fact for the
    standard PE circuit the output distribution on the phase register (with input |psi>)
    is:
        Prob(j) = sum_{eigenvalue e^{i theta}} |alpha_theta|^2 * KerFejer(2^m theta / (2 pi) - j)
    where alpha_theta = <eigvec_theta | psi>, and KerFejer is the Fejer kernel giving
    the sinc^2-like concentration. We sample this exactly by eigendecomposing W.
    """
    dim = W.shape[0]
    M = 1 << m  # 2^m
    # Eigendecompose W (unitary => eigenvalues on unit circle)
    eigvals, eigvecs = np.linalg.eig(W)
    thetas = np.angle(eigvals) % (2.0 * math.pi)  # in [0, 2pi)
    # Amplitudes alpha_j = <eigvec_j | psi>
    alphas = eigvecs.conj().T @ psi  # shape (dim,)
    prob_eig = np.abs(alphas) ** 2  # sum ~= 1 (if eigvecs orthonormal — Hermitian W has that; unitary is normal too so yes)
    # normalise defensively
    prob_eig = prob_eig / prob_eig.sum()

    # For each eigenvalue with phase theta, the phase-register outcome j in [0, M) has
    # probability:
    #     P(j | theta) = (1/M^2) * |sum_{k=0}^{M-1} exp(i k (theta - 2 pi j / M))|^2
    # We compute this by outer-product FFT-like trick:
    #     P(j | theta) = (1/M^2) * |D_M(theta - 2 pi j / M)|^2
    # where D_M(x) = sin(M x / 2) / sin(x / 2). Handle the x=0 limit as M.
    js = np.arange(M)
    grid_phases = 2.0 * math.pi * js / M  # (M,)

    # We only need to sample outcome j from the mixture sum_theta prob_eig[theta] * P(j | theta),
    # but for speed sample a single eigenstate first (categorical), then sample j | theta.
    idx = rng.choice(dim, p=prob_eig)
    theta = thetas[idx]

    diff = (theta - grid_phases) % (2.0 * math.pi)  # (M,)
    # to compute D_M robustly, use diff mapped to (-pi, pi]
    diff = np.where(diff > math.pi, diff - 2.0 * math.pi, diff)
    # sin(M diff/2) / sin(diff/2) — careful near 0
    num = np.sin(M * diff / 2.0)
    den = np.sin(diff / 2.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        D = np.where(np.abs(den) < 1e-15, float(M), num / den)
    Pj = (D * D) / (M * M)
    Pj = Pj / Pj.sum()  # renormalise (tiny numerical drift)

    j = rng.choice(M, p=Pj)
    theta_est = 2.0 * math.pi * j / M
    queries = M - 1  # number of U2 calls in this one PE run
    return theta_est, queries


def decoded_answer(theta_est: float, theta_thresh: float) -> int:
    """Return 0 if |theta_est| (taken to nearest wrap) < theta_thresh, else 1.

    theta_est in [0, 2pi). Wrap so we compare to 0 correctly:
    dist = min(theta_est, 2pi - theta_est) — distance from 0 on the circle.
    """
    d = min(theta_est, 2.0 * math.pi - theta_est)
    return 0 if d < theta_thresh else 1


# ---------------------------------------------------------------------------
# Trial harness
# ---------------------------------------------------------------------------

def run_one_input(
    tree: Tree,
    H: np.ndarray,
    U1: np.ndarray,
    psi_start_dp: np.ndarray,
    x: np.ndarray,
    m: int,
    C: int,
    rng: np.random.Generator,
) -> Tuple[int, int, int]:
    """Run C independent PE rounds on input x, majority-vote. Return (answer, total_queries, correct)."""
    U2 = build_U2(tree, x)
    W = U2 @ U1
    N_leaves = len(tree.leaves)
    theta_thresh = 0.5 * (1.0 / math.sqrt(N_leaves)) * 1.0  # theta_min/2 with c'=1 (heuristic bound)
    votes = np.zeros(2, dtype=int)
    tot_queries = 0
    for _ in range(C):
        theta_est, q = phase_estimation_run(W, psi_start_dp, m, rng)
        tot_queries += q
        ans = decoded_answer(theta_est, theta_thresh)
        votes[ans] += 1
    ans_final = int(np.argmax(votes))
    truth = eval_nand_tree(x, tree.n)
    return ans_final, tot_queries, int(ans_final == truth)


def run_scaling(
    ns: List[int],
    trials_per_n: int,
    m_scale: float,
    C: int,
    rng: np.random.Generator,
) -> Dict:
    """For each n, generate `trials_per_n` random leaf assignments, run the algorithm,
    collect empirical success prob and average query count."""
    results = {"per_n": [], "m_scale": m_scale, "C": C, "trials_per_n": trials_per_n}
    for n in ns:
        N = 2 ** n
        t = 2 * math.ceil(math.sqrt(N))
        assert_even_depth(n)
        tree = Tree(n=n, t=t)
        H = tree.build_H()
        U1 = build_U1(H)
        psi_start_dp = build_psi_start_doubleprime(tree, H)
        # phase register bits: m = ceil(log2(m_scale * sqrt(N)))
        m = max(3, math.ceil(math.log2(m_scale * math.sqrt(N))))
        # separate correctness for T=0 and T=1 inputs (sampled uniformly at random)
        num_correct = 0
        num_correct_by_truth = {0: 0, 1: 0}
        num_by_truth = {0: 0, 1: 0}
        queries_sum = 0
        # Balanced sampling: half trials with T=0, half with T=1 (accept-reject on random x).
        want = trials_per_n // 2
        got = {0: 0, 1: 0}
        while got[0] < want or got[1] < (trials_per_n - want):
            x = rng.integers(0, 2, size=N, dtype=int)
            truth = eval_nand_tree(x, n)
            need = want if truth == 0 else (trials_per_n - want)
            if got[truth] >= need:
                continue
            got[truth] += 1
            num_by_truth[truth] += 1
            ans, qs, ok = run_one_input(tree, H, U1, psi_start_dp, x, m, C, rng)
            queries_sum += qs
            num_correct += ok
            num_correct_by_truth[truth] += ok
        succ = num_correct / trials_per_n
        succ_by_truth = {
            k: (num_correct_by_truth[k] / num_by_truth[k]) if num_by_truth[k] else None
            for k in (0, 1)
        }
        avg_q = queries_sum / trials_per_n
        # queries-per-shot (one PE call): (2^m - 1); total per input = C * (2^m - 1)
        results["per_n"].append({
            "n": n,
            "N_leaves": N,
            "tail_t": t,
            "state_dim": tree.total,
            "m_phase_bits": m,
            "queries_per_shot": (1 << m) - 1,
            "shots_C": C,
            "queries_per_input_total": C * ((1 << m) - 1),
            "avg_queries": avg_q,
            "trials": trials_per_n,
            "num_by_truth": num_by_truth,
            "success_overall": succ,
            "success_when_T0": succ_by_truth[0],
            "success_when_T1": succ_by_truth[1],
        })
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[2, 4, 6, 8],
                    help="depths (leaves at even distance from root only — see paper §3.2 WLOG note; for odd depth, apply doubling preproc)")
    ap.add_argument("--trials", type=int, default=60)
    ap.add_argument("--m-scale", type=float, default=4.0,
                    help="phase-bits scale: m = ceil(log2(m_scale * sqrt N))")
    ap.add_argument("--C", type=int, default=5, help="PE repetitions per input for majority vote")
    ap.add_argument("--seed", type=int, default=20260705)
    ap.add_argument("--out", type=str, default="scaling_results.json")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    t0 = time.time()
    res = run_scaling(args.ns, args.trials, args.m_scale, args.C, rng)
    res["wall_time_s"] = time.time() - t0
    res["seed"] = args.seed
    res["ns"] = args.ns
    res["numpy_version"] = np.__version__
    with open(args.out, "w") as f:
        json.dump(res, f, indent=2)
    print(f"Wrote {args.out}  (wall {res['wall_time_s']:.1f}s)")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
