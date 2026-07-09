"""
Independent open replication of the stochastic DNA fragment rejoining model from:

    Li Y, Qian H, Wang Y, Cucinotta FA (2012)
    "A Stochastic Model of DNA Fragments Rejoining"
    PLoS ONE 7(9): e44293, doi:10.1371/journal.pone.0044293

This is an independent reimplementation. No author code was found or used.

Model (Gillespie direct method):
  Species:
    - E (Ku protein), assumed abundant -> treat as constant pool
    - Fragments: each fragment has (length n, bound_count b ∈ {0,1,2},
      residue tag t ∈ {clean, r, R, rr}), where:
        * clean : no protein residue (can recruit on free ends)
        * r     : one pair of residues blocks ONE end -> that end cannot bind
        * R     : one pair of residues blocks BOTH ends -> neither end can bind
        * rr    : two pairs of residues, one blocking each end
      Number of *available* free ends for binding = (number of ends not blocked
      and not currently occupied by E).

  Reactions:
    R1 Recruitment of Ku on a free end:
       fragment with one or more available free ends (and length >= Lm) gains a
       bound Ku at rate k1 * E * (#available free ends), but we cap total bound
       count at:
         - 1 if Lm <= n <= L*  (can only host one Ku reliably)
         - 2 if n > L*         (can host two, one at each end)
       (We treat the per-end propensity as k1 * E, summed across all available
       ends — equivalent to mass-action for end-binding.)

    R2 Joining of two fragments each with at least one bound Ku:
       For every ordered pair of fragments (i,j), i != j, both with bound>=1:
       propensity = k2 / V (mass-action volume scaling).
       Resulting fragment has length n_i + n_j; its residue tag depends on
       lengths (see paper Fig 1):
         - both short (n_i, n_j <= L*) -> residue R (blocks both ends)
         - one short, one long (short <= L* < long) -> residue r (blocks short end)
         - both long (n_i, n_j > L*) -> residue ignorable (clean)
       Joined fragment is released with bound_count reset to 0 (Ku detaches
       in the residue/joining step in this lumped description; see model text).
       Note: a fragment with residue tag rr can occur if a fragment with one
       residue (r) joins another short fragment producing a second residue.
       For simplicity we treat the second residue identically and label rr,
       meaning both ends are blocked until two release events occur.

    R3 Residue release (irreversible):
       For each residue present on a fragment:
         propensity = k3
       releasing one residue clears one blocked end; rr -> r -> clean, R -> clean
       (we model R as two simultaneously-blocked ends but a single release event
       per the paper's description: "the residue resulting from the joining of
       two short fragments...the residues must be removed" — paper treats it
       as a single release per joining step. We use a single k3 event for R.)

Rejoining is complete when only ONE fragment remains.

This file: pure NumPy/Python, CPU only. No external data.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional


# ---------- Default model constants (from paper) ----------
LM_DEFAULT = 15     # minimum length (bp) to recruit one Ku
LSTAR_DEFAULT = 45  # critical length (bp) above which TWO Ku can bind


@dataclass
class Fragment:
    length: int
    bound: int = 0          # number of Ku currently bound (0..max_bound)
    # residue blocks: number of ends blocked by protein residue
    # 0 = none, 1 = one end blocked, 2 = both ends blocked
    blocked_ends: int = 0

    def max_bound(self, Lm: int, Lstar: int) -> int:
        if self.length < Lm:
            return 0
        if self.length <= Lstar:
            return 1
        return 2

    def free_ends(self, Lm: int, Lstar: int) -> int:
        """Number of ends currently available for new Ku binding.

        A fragment has 2 physical ends. blocked_ends are unavailable. Bound Ku
        also occupy ends. Capacity:
          - n < Lm  : 0 (cannot bind)
          - Lm <= n <= Lstar : at most 1 total (one binding site overall)
          - n > Lstar : at most 2 (one per end)
        """
        if self.length < Lm:
            return 0
        cap = self.max_bound(Lm, Lstar)
        # Ends blocked or occupied
        unavailable = self.blocked_ends + self.bound
        free = cap - unavailable
        return max(0, free)


@dataclass
class SimParams:
    Lm: int = LM_DEFAULT
    Lstar: int = LSTAR_DEFAULT
    k1: float = 1.0         # protein recruitment rate (per E per end per unit time per unit volume)
    k2: float = 1.0         # fragment joining rate per pair (volume-scaled)
    k3: float = 1.0         # residue release rate (per residue, per unit time)
    E: float = 100.0        # Ku pool (treated abundant/constant per paper)
    V: float = 1.0          # nuclear volume (arbitrary units; scales 2nd-order)
    t_max: float = 1e6      # safety cutoff
    rng_seed: Optional[int] = None


@dataclass
class TrajectoryPoint:
    t: float
    n_fragments: int
    n_bound: int            # total Ku bound across all fragments
    n_residues: int         # total blocked ends across all fragments


def _propensities(fragments: List[Fragment], P: SimParams):
    """Compute total propensities for each channel and return enough info to fire.

    Channels:
      A: recruitment (sum over fragments of k1 * E * free_ends_i)
      B: joining (sum over ordered pairs (i<j) of k2/V * bound_i * bound_j_factor)
         Simplification: we require BOTH fragments have bound >= 1, propensity
         per unordered pair = k2 / V. Total = k2/V * C(M_bound, 2)
         where M_bound = number of fragments with bound >= 1.
         This matches the paper's reaction X^E + X^E -> ... with mass action
         per pair (no enzyme stoichiometry beyond "Ku is bound on each").
      C: residue release (sum over fragments of k3 * blocked_ends_i)

    Returns dict with totals and per-fragment arrays for sampling.
    """
    Lm, Lstar = P.Lm, P.Lstar

    free_ends = np.array([f.free_ends(Lm, Lstar) for f in fragments], dtype=np.int64)
    a_recruit_per = P.k1 * P.E * free_ends.astype(float)
    a_recruit_tot = a_recruit_per.sum()

    bound = np.array([f.bound for f in fragments], dtype=np.int64)
    bound_mask = bound >= 1
    n_bound_frags = int(bound_mask.sum())
    # unordered pairs of bound fragments
    a_join_tot = (P.k2 / P.V) * n_bound_frags * (n_bound_frags - 1) / 2.0

    blocked = np.array([f.blocked_ends for f in fragments], dtype=np.int64)
    a_release_per = P.k3 * blocked.astype(float)
    a_release_tot = a_release_per.sum()

    a_tot = a_recruit_tot + a_join_tot + a_release_tot

    return {
        "a_tot": a_tot,
        "a_recruit_tot": a_recruit_tot,
        "a_recruit_per": a_recruit_per,
        "a_join_tot": a_join_tot,
        "bound_mask": bound_mask,
        "a_release_tot": a_release_tot,
        "a_release_per": a_release_per,
    }


def simulate(
    initial_lengths: List[int],
    P: SimParams,
    record_every: int = 1,
) -> Tuple[float, List[TrajectoryPoint]]:
    """Run one Gillespie trajectory until 1 fragment remains.

    Returns (rejoining_time, trajectory).
    """
    rng = np.random.default_rng(P.rng_seed)

    fragments: List[Fragment] = [Fragment(length=int(n)) for n in initial_lengths]
    # Drop fragments < Lm: per paper, these are not counted in rejoining
    fragments = [f for f in fragments if f.length >= P.Lm]

    t = 0.0
    traj: List[TrajectoryPoint] = []

    def record(force: bool = False):
        n_frags = len(fragments)
        n_bound = sum(f.bound for f in fragments)
        n_res = sum(f.blocked_ends for f in fragments)
        traj.append(TrajectoryPoint(t=t, n_fragments=n_frags,
                                    n_bound=n_bound, n_residues=n_res))

    record(force=True)

    step = 0
    while len(fragments) > 1 and t < P.t_max:
        props = _propensities(fragments, P)
        a_tot = props["a_tot"]
        if a_tot <= 0.0:
            # Stuck (e.g., all fragments too short or otherwise blocked)
            break

        # Sample time to next event
        r1 = rng.random()
        dt = -np.log(max(r1, 1e-300)) / a_tot
        t += dt

        # Sample which channel
        r2 = rng.random() * a_tot

        if r2 < props["a_recruit_tot"]:
            # Recruitment: pick fragment proportional to per-fragment propensity
            per = props["a_recruit_per"]
            idx = _weighted_choice(rng, per)
            fragments[idx].bound += 1

        elif r2 < props["a_recruit_tot"] + props["a_join_tot"]:
            # Joining: pick unordered pair from bound fragments uniformly
            bound_idx = np.where(props["bound_mask"])[0]
            i, j = rng.choice(bound_idx, size=2, replace=False)
            i, j = int(i), int(j)
            fa, fb = fragments[i], fragments[j]
            new_len = fa.length + fb.length

            # Determine residue tag based on (n_a, n_b) vs Lstar (paper Fig 1)
            short_a = fa.length <= P.Lstar
            short_b = fb.length <= P.Lstar
            if short_a and short_b:
                # Both short -> residue R (both ends blocked)
                new_blocked = 2
            elif short_a != short_b:
                # One short, one long -> r (one end blocked)
                new_blocked = 1
            else:
                # Both long -> residue ignorable
                new_blocked = 0

            new_frag = Fragment(length=new_len, bound=0, blocked_ends=new_blocked)
            # Remove the two parents (delete higher index first)
            hi, lo = max(i, j), min(i, j)
            del fragments[hi]
            del fragments[lo]
            fragments.append(new_frag)

        else:
            # Release: pick fragment proportional to blocked_ends
            per = props["a_release_per"]
            idx = _weighted_choice(rng, per)
            if fragments[idx].blocked_ends > 0:
                fragments[idx].blocked_ends -= 1

        step += 1
        if (step % record_every) == 0:
            record()

    record(force=True)
    return t, traj


def _weighted_choice(rng: np.random.Generator, weights: np.ndarray) -> int:
    s = weights.sum()
    r = rng.random() * s
    c = 0.0
    for i, w in enumerate(weights):
        c += w
        if r < c:
            return i
    return int(len(weights) - 1)


def run_ensemble(
    initial_lengths_factory,
    P: SimParams,
    n_runs: int = 100,
    record_every: int = 1,
) -> Tuple[np.ndarray, List[List[TrajectoryPoint]]]:
    """Run n_runs trajectories. Returns (rejoining_times, list_of_traj).

    initial_lengths_factory: callable(rng) -> list of integer lengths (allows
    randomized initial distributions across runs, or returns same fixed list).
    """
    times = np.zeros(n_runs)
    all_traj = []
    base_seed = P.rng_seed
    rng_master = np.random.default_rng(base_seed)
    for k in range(n_runs):
        seed = int(rng_master.integers(0, 2**31 - 1))
        # New SimParams per run with fresh seed
        P_run = SimParams(**{**P.__dict__, "rng_seed": seed})
        lengths = initial_lengths_factory(np.random.default_rng(seed + 1))
        t_end, traj = simulate(lengths, P_run, record_every=record_every)
        times[k] = t_end
        all_traj.append(traj)
    return times, all_traj


# ---------- Helpers for figure replication ----------

def initial_uniform_same_length(n: int, count: int) -> List[int]:
    """All fragments have the same length n; total `count`."""
    return [int(n)] * int(count)


def initial_high_LET_Fe_1Gy(rng: np.random.Generator,
                            n_dsb: int = 30,
                            frac_short: float = 0.30,
                            short_range=(15, 45),
                            long_range=(46, 200)) -> List[int]:
    """Approximate initial fragment distribution for 1 Gy Fe ion (high LET).

    Per paper Fig 4 assumption: 70% long + 30% short fragments.
    We translate to N=n_dsb fragments (approx for 1 Gy: 25-35 DSBs ≈ 25-35 fragments)
    drawn uniformly from short and long ranges (bp).
    """
    short_lo, short_hi = short_range
    long_lo, long_hi = long_range
    n_short = int(round(frac_short * n_dsb))
    n_long = n_dsb - n_short
    lens = []
    if n_short > 0:
        lens.extend(rng.integers(short_lo, short_hi + 1, size=n_short).tolist())
    if n_long > 0:
        lens.extend(rng.integers(long_lo, long_hi + 1, size=n_long).tolist())
    rng.shuffle(lens)
    return [int(x) for x in lens]


def initial_low_LET_gamma_1Gy(rng: np.random.Generator,
                              n_dsb: int = 30,
                              frac_short: float = 0.03,
                              short_range=(15, 45),
                              long_range=(46, 200)) -> List[int]:
    """Approximate initial fragment distribution for 1 Gy gamma (low LET).
    Per Fig 4: 97% long + 3% short.
    """
    return initial_high_LET_Fe_1Gy(rng, n_dsb=n_dsb, frac_short=frac_short,
                                   short_range=short_range, long_range=long_range)


def mean_remaining_fraction_curve(
    all_traj: List[List[TrajectoryPoint]],
    t_grid: np.ndarray,
) -> np.ndarray:
    """Compute mean over trajectories of (M(t) - 1) / (M(0) - 1)
    on a fixed time grid. Curves are piecewise-constant (jumps at events).
    """
    curves = []
    for traj in all_traj:
        ts = np.array([p.t for p in traj])
        ms = np.array([p.n_fragments for p in traj])
        m0 = ms[0]
        if m0 <= 1:
            curves.append(np.zeros_like(t_grid))
            continue
        # piecewise constant: M(t) = last ms[i] with ts[i] <= t
        idx = np.searchsorted(ts, t_grid, side="right") - 1
        idx = np.clip(idx, 0, len(ms) - 1)
        m_at = ms[idx]
        frac = (m_at - 1) / (m0 - 1)
        curves.append(frac)
    return np.mean(np.stack(curves, axis=0), axis=0)
