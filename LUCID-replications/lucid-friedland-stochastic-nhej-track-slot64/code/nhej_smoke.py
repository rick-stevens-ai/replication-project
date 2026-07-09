"""
Architectural smoke replication of the Friedland-Jacob-Kundrát 2010 stochastic
NHEJ model (Radiat Res 173:677, DOI 10.1667/RR1965.1).

The original paper is closed-access and PARTRAC is not public. This module
implements the *qualitative* model structure from the published abstract +
open-access companion papers (Li 2014 PLoS ONE; Henthorn 2018 Sci Rep; Kundrát
2021 Front Phys) — see ../source/model_notes.md for the curated description and
parameter provenance.

State machine per DSB end:
    0  naked end
    1  Ku70/80 attached
    2  Ku + DNA-PKcs attached (DNA-PK complex, competent for synapsis)
    3  synapsed (paired with a partner)
    4  post-synaptic processing (clean: single rate-limiting step;
                                 dirty: Erlang-distributed multi-step cleaning)
    5  ligated (joined, terminal)

A DSB has two ends; we track pairs. A "correct" pair is the two ends originally
generated together; an "incorrect" pair is two ends from different DSBs whose
DNA-PK complexes happened to find each other first (misrejoin).

Synapsis is modeled by a 1D effective-proximity abstraction: each DSB end is
assigned an effective position that diffuses with D ~ 1.6e-3 µm^2/min (so that
RMS displacement ~ sqrt(2 D t) ~ 168 nm in 24 h, matching Henthorn 2018). Two
DNA-PK-complex ends within `synapsis_radius` (25 nm) can react to form a
synapsis at rate `k_syn`.

This is a structural smoke, not a parameter-faithful reproduction. The headline
output is a biphasic DSB rejoining curve with a few-percent residual at 24 h —
the qualitative behaviour the RR1965 abstract reports.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import math
import numpy as np


# --- Parameter set ----------------------------------------------------------
# Units: rate constants in min^-1, distances in micrometres.
# Numerical values are from Li 2014 PLoS ONE (DOI 10.1371/journal.pone.0085816,
# Table p.5, equation block (10)), which fits an NHEJ scheme of the same
# topology citing RR1965. They are *not* the verbatim RR1965 Table values
# (which are paywalled), but sit in the same fast/slow regime that RR1965
# fits to the 137Cs fibroblast benchmark.

@dataclass(frozen=True)
class NHEJParams:
    # Presynaptic phase: we collapse the rapid Ku attach/detach equilibrium
    # into an effective NAKED -> DNA-PK loading rate that yields ~1-2 min
    # mean loading time, consistent with Mari et al. 2006 and Uematsu 2007.
    k_ku_on:        float = 4.5      # Ku attachment rate, min^-1 (reference)
    k_ku_off:       float = 2.52     # Ku detachment rate (reference)
    k_dnapk_on:     float = 4.5      # DNA-PKcs recruitment rate (reference)
    k_dnapk_off:    float = 0.05     # DNA-PKcs essentially does not freely
                                     # dissociate before synapsis (Uematsu 2007)
    k_load:         float = 1.5      # Effective NAKED -> DNA-PK loading rate
                                     # (steady-state of k_ku_on, k_ku_off,
                                     # k_dnapk_on; mean 0.7 min)
    k_unload:       float = 0.05     # Effective DNA-PK -> NAKED rate (small;
                                     # reflects pre-synapsis dissociation
                                     # of the DNA-PK complex)
    p_stuck_dirty:  float = 0.08     # per-DSB probability of a permanent
                                     # complex-damage failure (= ends never
                                     # finish processing); produces residual
                                     # DSBs at 24 h and chromosomal aberrations
    k_syn:          float = 0.4      # synapsis rate given partner within
                                     # radius (tuned so fast-phase half-time
                                     # is ~ 20 min consistent with PFGE
                                     # benchmarks fit by RR1965)
    k_lig_clean:    float = 0.15     # single rate-limiting ligation step for
                                     # clean ends (~ 5 min half-time)
    k_clean_step:   float = 0.02     # per-step "dirty-end cleaning" rate
                                     # (slow phase: hours)
    n_dirty_steps:  int   = 3        # number of cleaning steps before ligation
    k_lig_dirty:    float = 0.05     # ligation rate after cleaning of dirty end
    synapsis_radius: float = 0.08    # 80 nm partner-reach kernel
    D_end:          float = 4.0e-4   # OU diffusion intensity (µm^2 / min)
                                     # so RMS displacement saturates ~150 nm
    ou_relax_rate:  float = 0.02     # Ornstein-Uhlenbeck relaxation rate
                                     # (min^-1); ends are tethered to nuclear
                                     # attachment sites near the initial DSB
    ou_anchor_jitter: float = 0.025  # initial offset between an end and its
                                     # tether anchor (µm); ~25 nm
    dirty_fraction_lowLET:  float = 0.30
    dirty_fraction_highLET: float = 0.70


# --- DSB end and pair structures -------------------------------------------

# state codes
S_NAKED   = 0
S_KU      = 1
S_DNAPK   = 2
S_SYNAP   = 3
S_PROC    = 4
S_DONE    = 5


@dataclass
class End:
    eid: int
    pair_id: int                 # id of the original partner (for correctness)
    pos: np.ndarray              # 3-vector, µm
    anchor: np.ndarray = None    # type: ignore  # OU tether anchor
    state: int = S_NAKED
    is_dirty: bool = False
    proc_step: int = 0           # current cleaning step (0..n_dirty_steps)
    synap_partner: int = -1      # eid of the end this one is synapsed with


@dataclass
class SimResult:
    times: np.ndarray
    surviving_dsb_frac: np.ndarray
    misrejoined_cum: np.ndarray
    correct_rejoined_cum: np.ndarray
    final_residual_frac: float
    final_misrejoin_frac: float
    final_correct_frac: float
    dirty_fraction: float
    n_dsb: int
    n_repeats: int
    n_steps: int


# --- Simulation --------------------------------------------------------------

def _new_dsb_population(n_dsb: int, dirty_fraction: float,
                        nucleus_radius_um: float, rng: np.random.Generator,
                        cluster_fraction: float = 0.12,
                        cluster_separation_um: float = 0.10,
                        ) -> list[End]:
    """Generate n_dsb DSBs (= 2*n_dsb ends) in a spherical nucleus.

    A `cluster_fraction` of DSBs are placed in pairs near another DSB
    (separation ~ `cluster_separation_um`, default 70 nm) to allow for
    occasional misrejoin events. The remainder are uniformly distributed.

    Each DSB is dirty with probability `dirty_fraction`. The two ends of a
    given DSB are colocated initially (within ~5 nm jitter).
    """
    ends: list[End] = []
    R = nucleus_radius_um
    centres: list[np.ndarray] = []
    k = 0
    while k < n_dsb:
        # rejection-sample uniform in sphere
        while True:
            xyz = rng.uniform(-R, R, size=3)
            if np.linalg.norm(xyz) <= R:
                break
        centres.append(xyz)
        # with prob cluster_fraction, immediately add a neighbour
        if (k + 1) < n_dsb and rng.random() < cluster_fraction:
            direction = rng.normal(0.0, 1.0, size=3)
            direction /= max(1e-12, float(np.linalg.norm(direction)))
            sep = cluster_separation_um
            centres.append(xyz + sep * direction)
            k += 2
        else:
            k += 1
    centres = centres[:n_dsb]
    for k, xyz in enumerate(centres):
        is_dirty = bool(rng.random() < dirty_fraction)
        for j in range(2):
            jitter = rng.normal(0.0, 0.0025, size=3)  # 2.5 nm
            pos = xyz + jitter
            ends.append(End(
                eid=2 * k + j,
                pair_id=2 * k + (1 - j),
                pos=pos,
                anchor=pos.copy(),
                is_dirty=is_dirty,
            ))
    # Mark a small permanent-fail fraction of dirty DSBs as "stuck":
    # their ends will never advance past S_PROC. We tag via the End.eid
    # parity is not enough; mark via a sentinel proc_step value of -1.
    pass
    return ends


def _diffuse(end: End, dt: float, params: NHEJParams,
             rng: np.random.Generator, R_nucleus: float) -> None:
    """Ornstein-Uhlenbeck step: tether the end to its anchor.

    dx = -k * (x - anchor) * dt + sqrt(2 D dt) * dW
    Stationary RMS displacement from anchor = sqrt(D / k) per axis.
    With D = 4e-4 µm²/min, k = 0.02 min⁻¹ => sqrt(0.02) = ~141 nm 1D RMS,
    ~245 nm 3D RMS, comfortably encompassing the synapsis radius.
    """
    sigma = math.sqrt(2.0 * params.D_end * dt)
    drift = -params.ou_relax_rate * (end.pos - end.anchor) * dt
    end.pos = end.pos + drift + rng.normal(0.0, sigma, size=3)
    r = np.linalg.norm(end.pos)
    if r > R_nucleus:
        end.pos *= (R_nucleus / r) * 0.999


def _try_synapsis(ends: list[End], params: NHEJParams, dt: float,
                  rng: np.random.Generator,
                  correct_pairs: list[tuple[int, int]],
                  misrejoin_pairs: list[tuple[int, int]]) -> None:
    """Spatial check among DNA-PK-complex ends within synapsis_radius using
    cKDTree for O(N log N) neighbour queries.
    """
    candidates = [e for e in ends if e.state == S_DNAPK]
    if len(candidates) < 2:
        return
    p_syn = 1.0 - math.exp(-params.k_syn * dt)
    try:
        from scipy.spatial import cKDTree  # type: ignore
        pts = np.array([c.pos for c in candidates])
        tree = cKDTree(pts)
        pairs = tree.query_pairs(r=params.synapsis_radius)
    except Exception:
        # fallback to brute pairwise (only if scipy missing)
        pairs = set()
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                d2 = float(np.sum((candidates[i].pos - candidates[j].pos) ** 2))
                if d2 <= params.synapsis_radius ** 2:
                    pairs.add((i, j))
    if not pairs:
        return
    # randomise iteration order
    pair_list = list(pairs)
    rng.shuffle(pair_list)
    used: set[int] = set()
    for i, j in pair_list:
        a, b = candidates[i], candidates[j]
        if a.eid in used or b.eid in used:
            continue
        if rng.random() >= p_syn:
            continue
        a.state = S_SYNAP
        b.state = S_SYNAP
        a.synap_partner = b.eid
        b.synap_partner = a.eid
        used.add(a.eid); used.add(b.eid)
        if b.eid == a.pair_id:
            correct_pairs.append((a.eid, b.eid))
        else:
            misrejoin_pairs.append((a.eid, b.eid))


def _first_order(state: int, params: NHEJParams) -> list[tuple[int, float]]:
    """Return list of (target_state, rate) transitions for first-order moves.

    We use a *collapsed* presynaptic phase: NAKED <-> DNA-PK directly at
    effective rates k_load, k_unload. The rapid Ku attach/detach equilibrium
    is absorbed into k_load. This avoids the timestep discretization artifact
    where, at dt comparable to 1/k_ku_off, ends would oscillate between
    NAKED and Ku states without progressing to DNA-PK.
    """
    if state == S_NAKED:
        return [(S_DNAPK, params.k_load)]
    if state == S_DNAPK:
        return [(S_NAKED, params.k_unload)]
    if state == S_SYNAP:
        return [(S_PROC, 1e6)]   # essentially instantaneous: synapsis -> proc
    return []


def _step_processing(end: End, dt: float, params: NHEJParams,
                     rng: np.random.Generator) -> bool:
    """Advance the processing state of a synapsed/processing end.

    A `proc_step` value of -1 marks a permanently stuck end (residual DSB).
    Returns True if this end has reached S_DONE *during this step*.
    """
    if end.proc_step < 0:
        # permanently stuck
        return False
    if not end.is_dirty:
        if rng.random() < (1.0 - math.exp(-params.k_lig_clean * dt)):
            end.state = S_DONE
            return True
        return False
    # dirty end: stepwise cleaning then ligation
    if end.proc_step < params.n_dirty_steps:
        if rng.random() < (1.0 - math.exp(-params.k_clean_step * dt)):
            end.proc_step += 1
        return False
    if rng.random() < (1.0 - math.exp(-params.k_lig_dirty * dt)):
        end.state = S_DONE
        return True
    return False


def simulate_once(n_dsb: int, dirty_fraction: float, params: NHEJParams,
                  t_max_min: float = 24 * 60, dt_min: float = 0.5,
                  nucleus_radius_um: float = 5.0,
                  cluster_fraction: float = 0.12,
                  seed: int | None = None
                  ) -> SimResult:
    """Single-run stochastic simulation; returns time-series of DSB resolution."""
    rng = np.random.default_rng(seed)
    ends = _new_dsb_population(n_dsb, dirty_fraction, nucleus_radius_um, rng,
                                cluster_fraction=cluster_fraction)
    # Mark stuck-fraction of dirty DSBs as permanent failures (proc_step = -1
    # on both ends).
    dirty_dsb_ids = sorted({e.eid // 2 for e in ends if e.is_dirty})
    n_stuck = int(round(len(dirty_dsb_ids) * params.p_stuck_dirty))
    if n_stuck > 0:
        stuck_ids = set(rng.choice(dirty_dsb_ids, size=n_stuck, replace=False))
        for e in ends:
            if (e.eid // 2) in stuck_ids:
                e.proc_step = -1
    n_steps = int(t_max_min / dt_min) + 1
    times = np.arange(n_steps) * dt_min
    surviving = np.ones(n_steps)
    misrej = np.zeros(n_steps)
    correct = np.zeros(n_steps)
    correct_pairs: list[tuple[int, int]] = []
    misrejoin_pairs: list[tuple[int, int]] = []

    # initial joined-pair sets keyed by frozenset of partner pair_ids
    joined_correct: set[int] = set()
    joined_misrej: set[int] = set()

    for s in range(1, n_steps):
        # 1. Diffuse all ends not yet done
        for e in ends:
            if e.state in (S_DONE,):
                continue
            _diffuse(e, dt_min, params, rng, nucleus_radius_um)
        # 2. First-order state transitions (competing reactions: pick none
        # or one based on competing-exponential probabilities, avoiding
        # order bias for any future multi-transition state).
        for e in ends:
            if e.state in (S_SYNAP, S_PROC, S_DONE):
                continue
            transitions = _first_order(e.state, params)
            if not transitions:
                continue
            total_rate = sum(r for _, r in transitions if r > 0)
            if total_rate <= 0:
                continue
            p_any = 1.0 - math.exp(-total_rate * dt_min)
            if rng.random() < p_any:
                # choose which transition fired
                u = rng.random() * total_rate
                acc = 0.0
                for target, rate in transitions:
                    if rate <= 0:
                        continue
                    acc += rate
                    if u <= acc:
                        e.state = target
                        break
        # 3. Synapsis
        _try_synapsis(ends, params, dt_min, rng,
                      correct_pairs, misrejoin_pairs)
        # 4. Synapsed -> proc instantly
        for e in ends:
            if e.state == S_SYNAP:
                e.state = S_PROC
        # 5. Processing step
        for e in ends:
            if e.state == S_PROC:
                _step_processing(e, dt_min, params, rng)

        # 6. Tally surviving DSBs: a DSB is "resolved" when *both* its ends
        # are in S_DONE *and* they are synapsed to each other (correct) or
        # to a partner from another DSB (incorrect).
        # For survival accounting, count any DSB end that is not yet S_DONE
        # as "surviving" (one half of an unresolved DSB).
        n_done = sum(1 for e in ends if e.state == S_DONE)
        # each completed end represents one half of a rejoined pair
        surviving_dsb = max(0, n_dsb - n_done // 2)
        surviving[s] = surviving_dsb / n_dsb

        # correct vs misrejoin tally: at this time, count pairs where both
        # ends are S_DONE
        nc = sum(1 for (a, b) in correct_pairs
                 if ends[a].state == S_DONE and ends[b].state == S_DONE)
        nm = sum(1 for (a, b) in misrejoin_pairs
                 if ends[a].state == S_DONE and ends[b].state == S_DONE)
        correct[s] = nc / n_dsb
        misrej[s] = nm / n_dsb

    return SimResult(
        times=times,
        surviving_dsb_frac=surviving,
        misrejoined_cum=misrej,
        correct_rejoined_cum=correct,
        final_residual_frac=float(surviving[-1]),
        final_misrejoin_frac=float(misrej[-1]),
        final_correct_frac=float(correct[-1]),
        dirty_fraction=dirty_fraction,
        n_dsb=n_dsb,
        n_repeats=1,
        n_steps=n_steps,
    )


def simulate_ensemble(n_dsb: int, dirty_fraction: float, params: NHEJParams,
                      n_repeats: int = 10,
                      t_max_min: float = 24 * 60, dt_min: float = 0.5,
                      nucleus_radius_um: float = 5.0,
                      cluster_fraction: float = 0.12,
                      base_seed: int = 1234,
                      ) -> SimResult:
    """Run multiple repeats and average."""
    runs = [simulate_once(n_dsb, dirty_fraction, params,
                          t_max_min=t_max_min, dt_min=dt_min,
                          nucleus_radius_um=nucleus_radius_um,
                          cluster_fraction=cluster_fraction,
                          seed=base_seed + i)
            for i in range(n_repeats)]
    times = runs[0].times
    s = np.mean([r.surviving_dsb_frac for r in runs], axis=0)
    m = np.mean([r.misrejoined_cum for r in runs], axis=0)
    c = np.mean([r.correct_rejoined_cum for r in runs], axis=0)
    return SimResult(
        times=times,
        surviving_dsb_frac=s,
        misrejoined_cum=m,
        correct_rejoined_cum=c,
        final_residual_frac=float(s[-1]),
        final_misrejoin_frac=float(m[-1]),
        final_correct_frac=float(c[-1]),
        dirty_fraction=dirty_fraction,
        n_dsb=n_dsb,
        n_repeats=n_repeats,
        n_steps=len(times),
    )
