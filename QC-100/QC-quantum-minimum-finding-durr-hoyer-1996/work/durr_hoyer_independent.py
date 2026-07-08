#!/usr/bin/env python3
"""
Independent statevector replication of Dürr & Høyer (1996)
"A quantum algorithm for finding the minimum" (arXiv:quant-ph/9607014).

This is a from-scratch implementation using pure NumPy statevector simulation
so it does not depend on a specific quantum SDK and can be re-derived from
first principles. It implements:

  * Grover iteration on n = log2(N) qubits with an oracle that marks all
    indices j with T[j] < T[y] (the current threshold).
  * The BBHT (Boyer–Brassard–Høyer–Tapp, 1998) exponential searching
    subroutine: without knowing the number of marked items t, one picks a
    random Grover rotation count r ∈ {0, 1, ..., ⌈m⌉ − 1} for a slowly
    growing m ← min(λ·m, √N), λ = 6/5, starting at m = 1.
  * The outer Dürr–Høyer loop: after each successful BBHT call, if the
    observed index has a strictly smaller value than the current threshold
    T[y], adopt it as the new threshold. The whole thing is interrupted
    when the total number of Grover iterations exceeds 22.5·√N + 1.4·lg²(N),
    the exact iteration budget stated in the paper.

We then run many independent trials to estimate:

  (E1) empirical success probability P[return true minimum]
       ≥ 1/2  (paper Theorem 1)
  (E2) empirical expected number of Grover oracle calls, compared to the
       paper's asymptotic 22.5·√N (plus lower-order term).

We compare against the classical O(N) linear scan (which is deterministic
and always correct).

Author: independent replicator, 2026-07-06.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Statevector Grover core (pure numpy, no external quantum SDK).
# ---------------------------------------------------------------------------

def uniform_superposition(n_qubits: int) -> np.ndarray:
    """|s> = 1/sqrt(N) sum_j |j>, N = 2**n_qubits."""
    N = 1 << n_qubits
    return np.full(N, 1.0 / math.sqrt(N), dtype=np.complex128)


def oracle_flip(state: np.ndarray, marked_mask: np.ndarray) -> np.ndarray:
    """Phase-flip the amplitudes of every marked basis index.

    marked_mask: 1D bool array of length N.
    """
    out = state.copy()
    out[marked_mask] *= -1.0
    return out


def diffusion(state: np.ndarray) -> np.ndarray:
    """Grover diffusion operator 2|s><s| - I in the computational basis.

    Equivalent to reflecting about the mean amplitude.
    """
    mean = state.mean()
    return 2.0 * mean - state


def grover_iterate(state: np.ndarray, marked_mask: np.ndarray, r: int) -> np.ndarray:
    """Apply r Grover iterations (oracle + diffusion) to state."""
    s = state
    for _ in range(r):
        s = oracle_flip(s, marked_mask)
        s = diffusion(s)
    return s


def measure(state: np.ndarray, rng: random.Random) -> int:
    """Standard-basis measurement: sample index j with probability |psi_j|^2."""
    probs = np.abs(state) ** 2
    # numerical hygiene
    probs = np.clip(probs.real, 0.0, None)
    probs /= probs.sum()
    u = rng.random()
    # inverse-CDF sample
    cdf = np.cumsum(probs)
    idx = int(np.searchsorted(cdf, u))
    if idx >= len(probs):
        idx = len(probs) - 1
    return idx


# ---------------------------------------------------------------------------
# BBHT exponential search (the subroutine Dürr–Høyer calls).
# Reference: Boyer, Brassard, Høyer, Tapp, "Tight bounds on quantum
# searching", Fortsch. Phys. 46 (1998) 493–505 — cited by Dürr–Høyer as [2].
# ---------------------------------------------------------------------------

BBHT_LAMBDA = 6.0 / 5.0


def bbht_search(
    n_qubits: int,
    marked_mask: np.ndarray,
    rng: random.Random,
    max_grover_calls: int,
) -> Tuple[Optional[int], int]:
    """Run BBHT until a marked index is observed, or the Grover-call budget
    is exhausted.

    Returns (observed_index_or_None, total_grover_iterations_used).
    """
    N = 1 << n_qubits
    m = 1.0
    total = 0
    any_marked = bool(marked_mask.any())
    if not any_marked:
        # Would loop forever; the outer algorithm avoids this after the first
        # improvement, but on the very first BBHT call the threshold may be
        # the true minimum. We conservatively still burn the whole budget.
        while total < max_grover_calls:
            r = rng.randrange(0, max(1, int(math.ceil(m))))
            total += r
            m = min(BBHT_LAMBDA * m, math.sqrt(N))
        return None, total

    while total < max_grover_calls:
        r = rng.randrange(0, max(1, int(math.ceil(m))))
        state = uniform_superposition(n_qubits)
        state = grover_iterate(state, marked_mask, r)
        idx = measure(state, rng)
        total += r  # count Grover-iteration budget in oracle calls
        if marked_mask[idx]:
            return idx, total
        m = min(BBHT_LAMBDA * m, math.sqrt(N))
    return None, total


# ---------------------------------------------------------------------------
# Dürr–Høyer outer loop.
# ---------------------------------------------------------------------------

@dataclass
class DHResult:
    N: int
    n_qubits: int
    table: List[float]
    true_min_index: int
    returned_index: int
    correct: bool
    grover_iterations_used: int          # to the point of budget exhaustion (paper convention)
    grover_iterations_to_first_hit: int  # iterations until y became the true min (-1 if never)
    outer_updates: int
    budget: int


def durr_hoyer(table: List[float], rng: random.Random) -> DHResult:
    N = len(table)
    assert N > 0 and (N & (N - 1)) == 0, "N must be a power of 2"
    n_qubits = int(round(math.log2(N)))

    # Paper's iteration budget: 22.5*sqrt(N) + 1.4*lg^2(N), plus the
    # "one iteration takes one time step" convention; we treat it as a hard
    # ceiling on the total Grover iterations across all BBHT calls.
    budget = int(math.ceil(22.5 * math.sqrt(N) + 1.4 * (math.log2(N) ** 2)))

    # Stage 1: pick threshold uniformly at random.
    y = rng.randrange(0, N)

    values = np.array(table)
    true_min_index = int(np.argmin(values))

    total_used = 0
    outer_updates = 0
    first_hit_iters = -1
    if y == true_min_index:
        first_hit_iters = 0

    while total_used < budget:
        # Build oracle mask: mark all j with T[j] < T[y].
        marked_mask = values < values[y]
        remaining = budget - total_used
        idx, used = bbht_search(n_qubits, marked_mask, rng, remaining)
        total_used += used
        if idx is not None and values[idx] < values[y]:
            y = idx
            outer_updates += 1
            if y == true_min_index and first_hit_iters < 0:
                first_hit_iters = total_used

    return DHResult(
        N=N,
        n_qubits=n_qubits,
        table=list(map(float, table)),
        true_min_index=int(true_min_index),
        returned_index=int(y),
        correct=bool(y == true_min_index),
        grover_iterations_used=int(total_used),
        grover_iterations_to_first_hit=int(first_hit_iters),
        outer_updates=int(outer_updates),
        budget=int(budget),
    )


# ---------------------------------------------------------------------------
# Classical baseline.
# ---------------------------------------------------------------------------

def classical_linear_scan(table: List[float]) -> Tuple[int, int]:
    """Return (argmin, number of probes)."""
    best_idx = 0
    best_val = table[0]
    probes = 1
    for j in range(1, len(table)):
        probes += 1
        if table[j] < best_val:
            best_val = table[j]
            best_idx = j
    return best_idx, probes


# ---------------------------------------------------------------------------
# Experiment driver.
# ---------------------------------------------------------------------------

@dataclass
class TrialSummary:
    N: int
    trials: int
    successes: int
    success_prob: float
    mean_grover_iters: float
    median_grover_iters: float
    std_grover_iters: float
    mean_iters_to_first_hit: float
    median_iters_to_first_hit: float
    paper_budget: int
    paper_leading_bound: float  # 22.5*sqrt(N)
    classical_probes_worst: int
    mean_outer_updates: float
    per_trial_iters: List[int] = field(default_factory=list)
    per_trial_iters_to_first_hit: List[int] = field(default_factory=list)
    per_trial_correct: List[bool] = field(default_factory=list)
    per_trial_outer_updates: List[int] = field(default_factory=list)


def run_experiment(N: int, trials: int, seed: int) -> TrialSummary:
    rng = random.Random(seed)
    n_qubits = int(round(math.log2(N)))
    assert (1 << n_qubits) == N, "N must be a power of 2"

    iters_used: List[int] = []
    iters_to_hit: List[int] = []
    corrects: List[bool] = []
    updates: List[int] = []

    for t in range(trials):
        # Fresh random table each trial: distinct values (permutation of range).
        perm = list(range(N))
        rng.shuffle(perm)
        table = [float(v) for v in perm]
        res = durr_hoyer(table, rng)
        iters_used.append(res.grover_iterations_used)
        iters_to_hit.append(res.grover_iterations_to_first_hit)
        corrects.append(res.correct)
        updates.append(res.outer_updates)

    hit_only = [x for x in iters_to_hit if x >= 0]
    successes = sum(corrects)
    return TrialSummary(
        N=N,
        trials=trials,
        successes=successes,
        success_prob=successes / trials,
        mean_grover_iters=float(np.mean(iters_used)),
        median_grover_iters=float(np.median(iters_used)),
        std_grover_iters=float(np.std(iters_used)),
        mean_iters_to_first_hit=float(np.mean(hit_only)) if hit_only else float("nan"),
        median_iters_to_first_hit=float(np.median(hit_only)) if hit_only else float("nan"),
        paper_budget=int(math.ceil(22.5 * math.sqrt(N) + 1.4 * math.log2(N) ** 2)),
        paper_leading_bound=22.5 * math.sqrt(N),
        classical_probes_worst=N,
        mean_outer_updates=float(np.mean(updates)),
        per_trial_iters=iters_used,
        per_trial_iters_to_first_hit=iters_to_hit,
        per_trial_correct=corrects,
        per_trial_outer_updates=updates,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--Ns", type=int, nargs="+", default=[8, 16, 32])
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260706)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    all_summaries = {}
    t0 = time.time()
    for N in args.Ns:
        print(f"[run] N={N} trials={args.trials}", file=sys.stderr)
        s = run_experiment(N=N, trials=args.trials, seed=args.seed + N)
        all_summaries[str(N)] = asdict(s)
        print(
            f"[run] N={N}: success_prob={s.success_prob:.3f} "
            f"mean_iters={s.mean_grover_iters:.2f} "
            f"paper_bound(22.5√N)={s.paper_leading_bound:.2f} "
            f"budget={s.paper_budget}",
            file=sys.stderr,
        )
    t1 = time.time()

    result = {
        "paper": "arXiv:quant-ph/9607014 (Dürr & Høyer, 1996)",
        "implementation": "independent NumPy statevector, no external quantum SDK",
        "wall_time_seconds": round(t1 - t0, 3),
        "seed": args.seed,
        "runs": all_summaries,
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[done] wrote {args.out} in {t1 - t0:.2f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
