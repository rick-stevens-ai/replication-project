#!/usr/bin/env python3
"""
Replication of Montanaro 2015 "Quantum walk speedup of backtracking algorithms"
(arXiv:1509.02374). QC-200 wave.

Goal: verify empirically that a Belovs-style quantum walk on the backtracking
search tree of a classical DPLL-like algorithm finds a marked (solution) node
with O(sqrt(T)) applications of the walk-step operator, versus O(T) node visits
classically. We follow the paper's Theorems 1-2 which give ~ sqrt(T * n) tests
(here n is the number of variables; we track the sqrt(T) scaling as the main
signature since n is held constant per instance and the log factors are
sub-leading for small T).

Method (faithful, small):
  (a) Classical DPLL-lite backtracking on random 3-SAT instances (n=10) at the
      critical density ratio m/n ~ 4.267. Count nodes T explored to find first
      satisfying assignment (or exhaust tree). Solvable instances only for the
      quantum comparison.
  (b) Materialize the exact search tree that DPLL walks (nodes = partial
      assignments visited; edges = parent/child in DPLL recursion). T = |V|.
  (c) Build the RA, RB reflection operators of Algorithm 2 of the paper on the
      T-node tree as (T+1)x(T+1) real matrices (root + tree). RA reflects
      about the |phi_x> super-position on even-depth vertices, RB about the
      odd-depth ones; solution vertices are unmarked (excluded from their
      star-state -- this is the marking mechanism in Belovs/Montanaro).
      Simulate the walk on the exact statevector -- no qubit encoding tricks,
      just the ~T-dim Hilbert space the paper's walk lives on.
  (d) Run W = RB * RA. Prepare the initial state |r> (uniform in root's star)
      and iterate. Measure the eigenphase-0 amplitude of |r> under W using
      exact phase estimation via eigen-decomposition of W. Compare
      #applications-of-W to reach constant success probability against
      classical T.
  (e) Repeat for several instances of increasing T; fit log(#iters) vs log(T)
      and check the exponent is close to 0.5 (i.e. sqrt(T) scaling).

We are NOT decomposing the walk into elementary gates or encoding on log(T)
qubits -- the paper itself treats the walk abstractly on the tree Hilbert
space (span of vertices + root). Simulating in that basis IS a faithful
simulation of the walk; the qubit-level circuit synthesis is orthogonal to the
sqrt(T) query-complexity claim we are checking.
"""

from __future__ import annotations
import json, math, random, sys, time
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np

# -----------------------------
# 1. Classical DPLL backtracking
# -----------------------------

@dataclass
class Node:
    """One vertex of the backtracking tree = one partial assignment DPLL visited."""
    idx: int
    parent: int | None
    depth: int
    assignment: tuple  # length n; entries in {-1,0,+1}   0 = unassigned
    children: list = field(default_factory=list)
    status: str = "internal"  # 'internal','sat','unsat','leaf-unsat'

def gen_3sat(n: int, m: int, rng: random.Random):
    """Generate a random 3-SAT instance: m clauses of 3 distinct literals over n vars."""
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(1, n+1), 3)
        lits = tuple(v if rng.random() < 0.5 else -v for v in vs)
        clauses.append(lits)
    return clauses

def eval_partial(clauses, assign):
    """Return 'sat','unsat','unknown' given partial assign (list of -1/0/+1)."""
    all_sat = True
    for cl in clauses:
        cl_val = 0  # 0 unknown, +1 sat, -1 unsat-so-far
        satisfied = False
        all_defined = True
        for lit in cl:
            v = abs(lit)
            a = assign[v-1]
            if a == 0:
                all_defined = False
            else:
                # literal true if sign matches
                if (lit > 0 and a == +1) or (lit < 0 and a == -1):
                    satisfied = True
                    break
        if satisfied:
            continue
        if all_defined:
            # clause fully assigned and unsatisfied -> conflict
            return "unsat"
        all_sat = False
    return "sat" if all_sat else "unknown"

def dpll_build_tree(clauses, n: int, node_cap: int = 20000):
    """Run DPLL with fixed variable order (branch on first unassigned) and
    record the whole visited tree. Return list of Node, and (solution_idx or None)."""
    nodes: list[Node] = []
    root = Node(idx=0, parent=None, depth=0, assignment=tuple([0]*n))
    nodes.append(root)
    solution_idx = None

    def visit(node_idx):
        nonlocal solution_idx
        if solution_idx is not None:
            return
        if len(nodes) > node_cap:
            return
        node = nodes[node_idx]
        st = eval_partial(clauses, list(node.assignment))
        if st == "sat":
            node.status = "sat"
            solution_idx = node_idx
            return
        if st == "unsat":
            node.status = "unsat"
            return
        # pick first unassigned var
        j = None
        for i, a in enumerate(node.assignment):
            if a == 0:
                j = i; break
        if j is None:
            # complete, and not sat -> mark unsat
            node.status = "unsat"
            return
        # branch: try +1 then -1 (i.e., True then False for var j+1)
        for val in (+1, -1):
            child_assign = list(node.assignment)
            child_assign[j] = val
            child = Node(idx=len(nodes), parent=node_idx,
                         depth=node.depth+1, assignment=tuple(child_assign))
            nodes.append(child)
            node.children.append(child.idx)
            visit(child.idx)
            if solution_idx is not None:
                return
    sys.setrecursionlimit(max(1000, node_cap*2 + 100))
    visit(0)
    return nodes, solution_idx


# -----------------------------
# 2. Belovs / Montanaro walk on the tree
# -----------------------------
#
# On a tree with vertex set V and root r, Belovs' walk lives on the Hilbert
# space spanned by { |v> : v in V } U { |r*> }  (we take dim = |V| since the
# root is already in V and no self-loop is needed for our detection variant).
# Split V = A U B where A = even-depth vertices (incl. root), B = odd-depth.
# For each v in A that is NOT marked, define
#     |phi_v> = |v> + sum_{c child of v} |c>      (unnormalized here; will
#                                                   normalize numerically)
# and RA = 2 * Pi_A - I where Pi_A = sum_{v in A, unmarked} |phi_v><phi_v|/<..|..>
#                                    + sum_{v in A, marked} |v><v|
# Similarly for RB over B (children rooted at odd-depth vertices).
#
# Actually to match Algorithm 2 (Montanaro sec 2) more literally, we take:
#   RA = reflection about span{ |psi_x> : x in A_unmarked } fixing marked |x>
#   RB = reflection about span{ |psi_x> : x in B_unmarked, x != root } fixing marked |x>
# where |psi_x> ∝ |x> + sum_{y in child(x)} |y>.
# W = RB * RA.  Starting state |r>. Detecting = amplitude of eigenphase 0 of W
# in |r> is >= constant iff a marked vertex is reachable. Query complexity:
# phase estimation with precision O(1/sqrt(Tn)) -> O(sqrt(T n)) uses of W.
#
# We check the sqrt(T) scaling by measuring, for each instance, the minimum
# integer k such that the marked-subspace overlap grows to >= 1/2 under the
# eigenspectrum -- equivalently, the smallest 1/theta where theta is the
# spectral gap of W around eigenvalue 1. By Belovs, theta ~ 1/sqrt(T n).
# So k_meas ~ sqrt(T*n) is our observable.

def build_walk_operator(nodes: list[Node], solution_idx: int) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Build RA, RB as (T,T) real orthogonal matrices in the vertex basis.
    Marked = {solution_idx}.
    Return (RA, RB, T).
    """
    T = len(nodes)
    A_indices = [i for i, nd in enumerate(nodes) if nd.depth % 2 == 0]
    B_indices = [i for i, nd in enumerate(nodes) if nd.depth % 2 == 1]

    def build_reflection(vertex_indices):
        """Reflection about span of {|psi_x> : x in vertex_indices, x unmarked}
        while fixing marked basis vectors. All vectors in R^T."""
        vecs = []
        # marked-fix vectors: identity on marked basis states in this set
        # (i.e. they contribute +1 eigenvalue to Pi)
        # We'll build Pi = sum |psi><psi|/<psi|psi> over unmarked-star-states
        #                + sum |x><x| over marked x in vertex_indices
        # R = 2*Pi - I
        Pi = np.zeros((T, T), dtype=np.float64)
        for x in vertex_indices:
            if x == solution_idx:
                # marked -> project onto basis vector |x>
                e = np.zeros(T); e[x] = 1.0
                Pi += np.outer(e, e)
            else:
                # star state: |x> + sum children
                v = np.zeros(T)
                v[x] = 1.0
                for c in nodes[x].children:
                    v[c] = 1.0
                norm2 = float(v @ v)
                if norm2 > 0:
                    Pi += np.outer(v, v) / norm2
        R = 2.0 * Pi - np.eye(T)
        return R

    RA = build_reflection(A_indices)
    RB = build_reflection(B_indices)
    return RA, RB, T


def walk_spectral_analysis(RA: np.ndarray, RB: np.ndarray, root_idx: int) -> dict:
    """
    Diagonalize W = RB @ RA. Return the phase gap around eigenvalue 1 (from
    the point of view of the |root> state) and the number of iterations that
    achieves >= 1/2 detection probability.

    Detection probability using phase estimation with s bits is ~1 iff
    s >~ 1/theta_min, where theta_min is the smallest non-zero eigenphase of
    W in the support of |root>. That #iterations ~ 1/theta_min is our
    empirical sqrt(T) observable.
    """
    T = RA.shape[0]
    W = RB @ RA
    # eigen-decompose (W is orthogonal -> eigvals on unit circle)
    eigvals, eigvecs = np.linalg.eig(W)
    phases = np.angle(eigvals)   # in (-pi, pi]

    # amplitudes of |root> in each eigenvector
    r = np.zeros(T); r[root_idx] = 1.0
    amps = np.abs(eigvecs.conj().T @ r) ** 2  # weight per eigenvector
    amps = amps / amps.sum()

    # phases sorted by |phase|; look for smallest |phase| > 1e-8 with real weight
    idx = np.argsort(np.abs(phases))
    smallest_nonzero_phase = None
    weight_at_zero = 0.0
    tol = 1e-6
    for k in idx:
        if abs(phases[k]) < tol:
            weight_at_zero += amps[k]
        else:
            if amps[k] > 1e-4 and smallest_nonzero_phase is None:
                smallest_nonzero_phase = abs(phases[k])
    if smallest_nonzero_phase is None or smallest_nonzero_phase == 0:
        smallest_nonzero_phase = float('nan')

    # #walk iterations to resolve = ~ pi / smallest_nonzero_phase
    n_iters_needed = float(math.pi / smallest_nonzero_phase) if smallest_nonzero_phase == smallest_nonzero_phase else float('inf')
    return dict(T=T, weight_at_zero_phase=float(weight_at_zero),
                smallest_nonzero_phase=float(smallest_nonzero_phase),
                n_walk_iters_for_detection=float(n_iters_needed),
                spectral_gap_over_pi=float(smallest_nonzero_phase/math.pi))


# -----------------------------
# 3. Verify Grover-like amplification on the tree by explicit simulation
# -----------------------------
def grover_style_simulation(RA: np.ndarray, RB: np.ndarray, root_idx: int, solution_idx: int, k_max: int) -> list:
    """
    Explicit iteration: start in |root>, apply (RB RA)^k for k=0..k_max, and
    record overlap-squared with |solution>. This isn't literally phase
    estimation, but it lets us see the amplitude-amplification-like oscillation
    that peaks at ~ pi/(2 theta) steps -- Grover's rule -- confirming the
    sqrt(T) scaling.
    """
    T = RA.shape[0]
    state = np.zeros(T); state[root_idx] = 1.0
    W = RB @ RA
    overlaps = []
    for k in range(k_max + 1):
        overlaps.append(float(abs(state[solution_idx])**2))
        state = W @ state
    return overlaps


# -----------------------------
# 4. Main experiment
# -----------------------------
def main():
    out = {}
    rng = random.Random(20260705)
    n = 10  # 10 boolean variables

    # generate several solvable 3-SAT instances of varying difficulty
    # aim for T in a spread from ~30 to ~800
    target_T_bins = [(20, 80), (80, 250), (250, 900)]
    instances = []
    attempts = 0
    while len(instances) < 3 and attempts < 200:
        attempts += 1
        # vary clause density around threshold
        m = rng.randint(20, 50)
        clauses = gen_3sat(n, m, rng)
        nodes, sol = dpll_build_tree(clauses, n, node_cap=1500)
        if sol is None:
            continue
        T = len(nodes)
        # place into first empty bin whose range this T fits
        for i, (lo, hi) in enumerate(target_T_bins):
            if any(inst['bin'] == i for inst in instances):
                continue
            if lo <= T <= hi:
                instances.append(dict(bin=i, m=m, n=n, T=T, clauses=clauses,
                                      nodes=nodes, sol=sol, seed=attempts))
                break
        if len(instances) == 3:
            break

    if len(instances) < 3:
        # fallback: just take the first 3 solvable we find
        pass

    # if we still have fewer, top up with any solvable ones we get
    while len(instances) < 3 and attempts < 500:
        attempts += 1
        m = rng.randint(25, 45)
        clauses = gen_3sat(n, m, rng)
        nodes, sol = dpll_build_tree(clauses, n, node_cap=1500)
        if sol is None:
            continue
        T = len(nodes)
        instances.append(dict(bin=len(instances), m=m, n=n, T=T, clauses=clauses,
                              nodes=nodes, sol=sol, seed=attempts))

    results = []
    for inst in instances:
        t0 = time.time()
        RA, RB, T = build_walk_operator(inst['nodes'], inst['sol'])
        root = 0
        # spectral analysis
        spec = walk_spectral_analysis(RA, RB, root)
        # short explicit simulation up to ~ 4*sqrt(T) steps
        k_max = min(int(6 * math.sqrt(T)) + 4, 300)
        overlaps = grover_style_simulation(RA, RB, root, inst['sol'], k_max)
        k_star = int(np.argmax(overlaps))
        peak_overlap = float(np.max(overlaps))
        dt = time.time() - t0
        rec = dict(bin=inst['bin'], seed=inst['seed'], n=inst['n'], m=inst['m'],
                   T=T, k_max=k_max,
                   walk_iters_needed_spec=spec['n_walk_iters_for_detection'],
                   spectral_gap_over_pi=spec['spectral_gap_over_pi'],
                   weight_at_zero_phase=spec['weight_at_zero_phase'],
                   k_first_peak=k_star, peak_overlap_root_to_solution=peak_overlap,
                   sim_seconds=dt,
                   solution_assignment=list(inst['nodes'][inst['sol']].assignment),
                   sample_clauses_head=inst['clauses'][:5])
        results.append(rec)
        print(f"[inst bin={inst['bin']}] n={inst['n']} m={inst['m']} T={T} "
              f"k_iters_spec~{spec['n_walk_iters_for_detection']:.2f} "
              f"k_peak_explicit={k_star} peak_overlap={peak_overlap:.4f} "
              f"({dt:.2f}s)")

    # fit sqrt(T) scaling for both metrics
    def fit_loglog(xs, ys):
        xs = np.log(np.array(xs, dtype=float))
        ys = np.log(np.array(ys, dtype=float))
        if len(xs) < 2:
            return dict(slope=None, intercept=None)
        A = np.vstack([xs, np.ones_like(xs)]).T
        m, b = np.linalg.lstsq(A, ys, rcond=None)[0]
        return dict(slope=float(m), intercept=float(b))

    Ts = [r['T'] for r in results]
    ks_spec = [r['walk_iters_needed_spec'] for r in results]
    ks_peak = [r['k_first_peak'] for r in results if r['k_first_peak'] > 0]
    Ts_peak = [results[i]['T'] for i in range(len(results)) if results[i]['k_first_peak'] > 0]
    scaling_spec = fit_loglog(Ts, ks_spec) if all(math.isfinite(k) for k in ks_spec) else dict(slope=None)
    scaling_peak = fit_loglog(Ts_peak, ks_peak) if len(ks_peak) >= 2 else dict(slope=None)

    out = dict(paper="arXiv:1509.02374", author="A. Montanaro",
               title="Quantum walk speedup of backtracking algorithms",
               n_variables=n, instances=results,
               scaling_fit_spectral_iters_vs_T=scaling_spec,
               scaling_fit_explicit_peak_vs_T=scaling_peak,
               expected_slope_for_sqrtT=0.5)
    print("\n== SCALING FITS ==")
    print(f"  slope (spectral iters ~ T^slope): {scaling_spec.get('slope')}")
    print(f"  slope (explicit peak k ~ T^slope): {scaling_peak.get('slope')}")
    print("  expected for sqrt(T) speedup: 0.5")

    Path(__file__).parent.joinpath("results.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote results.json")

if __name__ == "__main__":
    main()
