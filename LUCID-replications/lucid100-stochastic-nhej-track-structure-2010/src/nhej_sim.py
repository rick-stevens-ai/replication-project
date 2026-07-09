"""
Structural replication of the qualitative stochastic-NHEJ model in
Friedland, Jacob, Kundrát, Radiat. Res. 173:677-688 (2010), DOI 10.1667/RR1965.1.

WHY 'structural': the paper is paywalled, no PMC copy, no preprint. The
abstract specifies the architecture but not the numerical rate constants,
the four scenario parameter sets, or the per-dose Tables. We therefore
implement the architecture and fit a small number of free parameters to
the well-known biexponential gamma-DSB rejoining kinetics for human
fibroblasts (fast component half-life ~10-30 min, slow component
half-life ~2-4 h, ~5-10% residual DSBs at 24 h - widely reported in
the open literature, e.g. Karlsson & Stenerlow 2004, Rothkamm & Lobrich 2003).

The replication is a CPU Monte Carlo with these pieces:

  - PARTRAC-style spatial input: replaced by a uniform-random distribution
    of DSB midpoints inside a spherical nucleus (r = 4.65 um, V ~ 421 um^3),
    with an LET-independent yield of ~35 DSB / Gy / cell (gamma reference),
    plus a per-DSB 'complexity' tag drawn Bernoulli with p_dirty = 0.30
    (literature range 0.25-0.40 for low-LET).

  - Each DSB produces two DNA termini at the same spatial coordinate.

  - Presynaptic phase: each free terminus undergoes first-order
    Ku/DNA-PK attachment with rate k_on and dissociation with rate k_off
    (single lumped step rather than the paper's two-step Ku then DNA-PK).

  - Diffusion: termini take small Gaussian steps with diffusion
    coefficient D_t per unit time (free-end mobility from
    Soutoglou et al. 2007 / Jakob et al. 2009 in the same group's later
    papers, D ~ 1e-3 um^2/min).

  - Synapsis: any two DNA-PK-loaded termini within R_syn = 25 nm
    coalesce into a synapsis.

  - Postsynaptic phase:
      clean-clean   -> single ligation step with rate k_clean
      any-dirty     -> stepwise lesion removal, n_clean steps of
                       rate k_dirty_step, then single ligation
                       (this is the source of the slow component).

  - Misrejoining: when synapsis forms, the partner is the spatially
    nearest available DNA-PK terminus; if it is NOT the cognate
    sister terminus of the original DSB, that synapsis (if it ligates)
    is counted as a misrejoin.

Outputs:
  - residual DSB fraction vs time
  - misrejoin fraction vs dose
  - cumulative chromosome-aberration-like exchange count

This script is fully deterministic given --seed and runs on CPU only.
"""

import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Parameters (defaults; can be overridden on CLI). All times in MINUTES.
# ---------------------------------------------------------------------------
DEFAULTS = dict(
    nucleus_radius_um=4.65,         # ~ V_nucleus 421 um^3 (typical human fibroblast)
    dsb_per_gy=35.0,                # ~35 DSB/Gy/cell, low-LET gamma
    p_dirty=0.30,                   # fraction of complex/dirty DSBs at low LET
    k_on=0.5,                       # Ku/DNA-PK attachment rate (min^-1)
    k_off=0.05,                     # dissociation rate (min^-1)
    D_t=1.0e-3,                     # terminus diffusion coefficient (um^2 / min)
    R_syn_um=0.025,                 # synapsis spatial-proximity threshold (um)
    k_clean=0.35,                   # clean ligation rate (min^-1)  -> t1/2 ~ 2.0 min after synapsis
    k_dirty_step=0.06,              # per-step lesion removal rate (min^-1)
    n_dirty_steps=4,                # number of cleanup steps for a dirty end
    dt=0.5,                         # integration time-step (min)
    t_end=1440.0,                   # total simulated time (min) = 24 h
    sample_times_min=(0.0, 5.0, 15.0, 30.0, 60.0, 120.0, 240.0, 480.0, 1440.0),
)


@dataclass
class Terminus:
    pos: np.ndarray            # (3,) position in um
    partner_id: int            # id of the original sister terminus (for misrejoin tracking)
    dirty: bool                # complexity tag of the originating DSB
    ku_loaded: bool = False    # Ku/DNA-PK currently bound?
    in_synapsis: bool = False  # currently engaged in a synapsis?
    dirty_steps_remaining: int = 0   # for dirty-end stepwise cleanup
    cleaned: bool = False      # finished cleanup, ready for ligation


# ---------------------------------------------------------------------------
def sample_uniform_sphere(n: int, R: float, rng: np.random.Generator) -> np.ndarray:
    """Sample n points uniformly inside a sphere of radius R."""
    u = rng.random(n)
    r = R * np.cbrt(u)
    phi = rng.random(n) * 2.0 * math.pi
    cos_th = 1.0 - 2.0 * rng.random(n)
    sin_th = np.sqrt(np.clip(1.0 - cos_th * cos_th, 0.0, 1.0))
    x = r * sin_th * np.cos(phi)
    y = r * sin_th * np.sin(phi)
    z = r * cos_th
    return np.stack([x, y, z], axis=1)


# ---------------------------------------------------------------------------
def init_dsbs(dose_gy: float, P: dict, rng: np.random.Generator) -> List[Terminus]:
    """Create initial set of termini for the given dose."""
    n_dsb = rng.poisson(P["dsb_per_gy"] * dose_gy)
    if n_dsb == 0:
        return []
    midpts = sample_uniform_sphere(n_dsb, P["nucleus_radius_um"], rng)
    dirty_flags = rng.random(n_dsb) < P["p_dirty"]

    termini: List[Terminus] = []
    for i in range(n_dsb):
        # both termini start at the DSB midpoint
        a_id = 2 * i
        b_id = 2 * i + 1
        termini.append(Terminus(pos=midpts[i].copy(), partner_id=b_id,
                                dirty=bool(dirty_flags[i])))
        termini.append(Terminus(pos=midpts[i].copy(), partner_id=a_id,
                                dirty=bool(dirty_flags[i])))
    return termini


# ---------------------------------------------------------------------------
def step_presynaptic(termini: List[Terminus], P: dict, rng: np.random.Generator):
    """First-order Ku/DNA-PK loading/unloading + diffusion on free termini."""
    dt = P["dt"]
    p_on = 1.0 - math.exp(-P["k_on"] * dt)
    p_off = 1.0 - math.exp(-P["k_off"] * dt)
    sigma = math.sqrt(2.0 * P["D_t"] * dt)
    R = P["nucleus_radius_um"]
    live_idx = [j for j, t in enumerate(termini) if t is not None]
    if not live_idx:
        return
    # vectorised diffusion + reflection over live termini only
    poss = np.array([termini[j].pos for j in live_idx])
    free_mask = np.array([not termini[j].in_synapsis for j in live_idx])
    n_free = int(free_mask.sum())
    if n_free > 0:
        steps = rng.normal(0.0, sigma, size=(n_free, 3))
        poss[free_mask] += steps
        # reflect back into sphere if needed
        r = np.linalg.norm(poss[free_mask], axis=1)
        over = r > R
        if over.any():
            idx_free_local = np.where(free_mask)[0]
            for jj in np.where(over)[0]:
                v = poss[idx_free_local[jj]]
                poss[idx_free_local[jj]] = v * (R / max(np.linalg.norm(v), 1e-12))
        for k_local, j in enumerate(live_idx):
            termini[j].pos = poss[k_local]

    # Ku/DNA-PK on/off (live + free only)
    rolls_on = rng.random(len(live_idx))
    rolls_off = rng.random(len(live_idx))
    for k_local, j in enumerate(live_idx):
        t = termini[j]
        if t.in_synapsis:
            continue
        if not t.ku_loaded and rolls_on[k_local] < p_on:
            t.ku_loaded = True
        elif t.ku_loaded and rolls_off[k_local] < p_off:
            t.ku_loaded = False


def step_synapsis(termini: List[Terminus], P: dict, rng: np.random.Generator,
                  misrejoin_log: List[Tuple[int, int]]):
    """Pair up Ku-loaded free termini within R_syn into synapses (KD-tree)."""
    R_syn = P["R_syn_um"]
    free_loaded = [i for i, t in enumerate(termini)
                   if t is not None and t.ku_loaded and not t.in_synapsis]
    if len(free_loaded) < 2:
        return
    poss = np.array([termini[i].pos for i in free_loaded])

    try:
        from scipy.spatial import cKDTree
        tree = cKDTree(poss)
        # k=2 -> nearest neighbour is self, second is real NN
        dists, idxs = tree.query(poss, k=2)
        # column 1 = nearest non-self
        order = list(range(len(free_loaded)))
        rng.shuffle(order)
        used = set()
        for j in order:
            if j in used:
                continue
            k_local = int(idxs[j, 1])
            if dists[j, 1] > R_syn:
                continue
            if k_local in used:
                continue
            a = free_loaded[j]
            b = free_loaded[k_local]
            if termini[a].in_synapsis or termini[b].in_synapsis:
                continue
            termini[a].in_synapsis = True
            termini[b].in_synapsis = True
            used.add(j); used.add(k_local)
            if termini[a].dirty or termini[b].dirty:
                steps = P["n_dirty_steps"]
                termini[a].dirty_steps_remaining = steps
                termini[b].dirty_steps_remaining = steps
            else:
                termini[a].cleaned = True
                termini[b].cleaned = True
            misrejoin_log.append((a, b))
    except Exception:
        # fallback: naive O(n^2)
        diffs = poss[:, None, :] - poss[None, :, :]
        d = np.linalg.norm(diffs, axis=-1)
        np.fill_diagonal(d, np.inf)
        used = set()
        order = list(range(len(free_loaded)))
        rng.shuffle(order)
        for j in order:
            if j in used:
                continue
            k_local = int(np.argmin(d[j]))
            if d[j, k_local] > R_syn:
                continue
            if k_local in used:
                continue
            a = free_loaded[j]
            b = free_loaded[k_local]
            if termini[a].in_synapsis or termini[b].in_synapsis:
                continue
            termini[a].in_synapsis = True
            termini[b].in_synapsis = True
            used.add(j); used.add(k_local)
            if termini[a].dirty or termini[b].dirty:
                steps = P["n_dirty_steps"]
                termini[a].dirty_steps_remaining = steps
                termini[b].dirty_steps_remaining = steps
            else:
                termini[a].cleaned = True
                termini[b].cleaned = True
            misrejoin_log.append((a, b))


def step_postsynaptic(termini: List[Terminus], P: dict, rng: np.random.Generator,
                      synapses: List[Tuple[int, int]],
                      rejoin_log: List[Tuple[float, int, int, bool]],
                      t_now: float):
    """Advance synapses through cleanup + ligation; mark ligated pairs as removed."""
    dt = P["dt"]
    p_clean = 1.0 - math.exp(-P["k_clean"] * dt)
    p_step = 1.0 - math.exp(-P["k_dirty_step"] * dt)
    # iterate over surviving synapses
    next_syn = []
    for (a, b) in synapses:
        ta = termini[a]; tb = termini[b]
        if ta is None or tb is None:
            continue
        # dirty cleanup
        if ta.dirty_steps_remaining > 0 and rng.random() < p_step:
            ta.dirty_steps_remaining -= 1
            if ta.dirty_steps_remaining == 0:
                ta.cleaned = True
        if tb.dirty_steps_remaining > 0 and rng.random() < p_step:
            tb.dirty_steps_remaining -= 1
            if tb.dirty_steps_remaining == 0:
                tb.cleaned = True
        if ta.cleaned and tb.cleaned:
            # attempt ligation
            if rng.random() < p_clean:
                mis = (tb.partner_id != a) or (ta.partner_id != b)
                rejoin_log.append((t_now, a, b, mis))
                # mark for removal -- we'll filter outside
                termini[a] = None
                termini[b] = None
                continue
        next_syn.append((a, b))
    synapses.clear()
    synapses.extend(next_syn)


# ---------------------------------------------------------------------------
def simulate_cell(dose_gy: float, P: dict, seed: int):
    rng = np.random.default_rng(seed)
    termini = init_dsbs(dose_gy, P, rng)
    n_init_termini = len(termini)
    n_init_dsb = n_init_termini // 2

    synapses: List[Tuple[int, int]] = []
    rejoin_log: List[Tuple[float, int, int, bool]] = []
    misrejoin_log: List[Tuple[int, int]] = []

    sample_times = list(P["sample_times_min"])
    next_sample = 0
    sample_records = []     # (time, remaining_dsb_equivalent)

    t = 0.0
    steps = int(round(P["t_end"] / P["dt"]))
    for _ in range(steps):
        # sample BEFORE advancing
        while next_sample < len(sample_times) and t >= sample_times[next_sample]:
            # remaining DSBs = pairs of termini that have not yet ligated
            # a DSB is "remaining" if either of its two termini is still alive
            alive = [tt for tt in termini if tt is not None]
            ids_alive = set(id(tt) for tt in alive)
            n_alive = len(alive)
            # # of DSBs remaining = (# alive termini + # in synapsis still alive) / 2
            sample_records.append((sample_times[next_sample],
                                   n_alive / 2.0,
                                   sum(1 for tt in alive if tt.in_synapsis),
                                   len(synapses)))
            next_sample += 1
        step_presynaptic(termini, P, rng)
        step_synapsis(termini, P, rng, misrejoin_log)
        step_postsynaptic(termini, P, rng, synapses, rejoin_log, t)
        # newly-formed synapses are in misrejoin_log; move them to synapses
        for s in misrejoin_log:
            if s not in synapses:
                synapses.append(s)
        misrejoin_log.clear()
        t += P["dt"]

    # final sample
    while next_sample < len(sample_times):
        alive = [tt for tt in termini if tt is not None]
        sample_records.append((sample_times[next_sample],
                               len(alive) / 2.0,
                               sum(1 for tt in alive if tt.in_synapsis),
                               len(synapses)))
        next_sample += 1

    n_rejoined = len(rejoin_log)
    n_mis = sum(1 for r in rejoin_log if r[3])
    misrejoin_fraction = (n_mis / n_rejoined) if n_rejoined else 0.0
    return dict(
        dose_gy=dose_gy,
        n_init_dsb=n_init_dsb,
        n_rejoined=n_rejoined,
        n_misrejoined=n_mis,
        misrejoin_fraction=misrejoin_fraction,
        residual_dsb=(n_init_dsb - n_rejoined),
        samples=sample_records,
    )


# ---------------------------------------------------------------------------
def run_dose_response(doses, n_cells, P, base_seed=42):
    out = []
    for d in doses:
        per_cell = []
        for c in range(n_cells):
            r = simulate_cell(d, P, seed=base_seed + 1000 * int(d * 10) + c)
            per_cell.append(r)
        # aggregate
        agg_init = np.mean([x["n_init_dsb"] for x in per_cell])
        agg_rej = np.mean([x["n_rejoined"] for x in per_cell])
        agg_mis = np.mean([x["n_misrejoined"] for x in per_cell])
        agg_mf = np.mean([x["misrejoin_fraction"] for x in per_cell])
        agg_res = np.mean([x["residual_dsb"] for x in per_cell])
        # mean residual fraction at each sample time
        sample_times = [s[0] for s in per_cell[0]["samples"]]
        mean_frac = []
        for k, st in enumerate(sample_times):
            num = np.mean([x["samples"][k][1] for x in per_cell])
            denom = max(agg_init, 1e-9)
            mean_frac.append(num / denom)
        out.append(dict(
            dose_gy=d, n_cells=n_cells,
            init_dsb=agg_init, rejoined=agg_rej, misrejoined=agg_mis,
            misrejoin_fraction=agg_mf, residual_dsb=agg_res,
            sample_times=sample_times, mean_residual_fraction=mean_frac,
        ))
    return out


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doses", type=str, default="1,2,5,10,20",
                    help="comma-separated Gy")
    ap.add_argument("--n-cells", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20100501)
    ap.add_argument("--out", type=str, required=True)
    # tunable knobs (overrides of DEFAULTS)
    for k, v in DEFAULTS.items():
        if isinstance(v, tuple):
            continue
        ap.add_argument(f"--{k.replace('_','-')}", type=float, default=v)
    args = ap.parse_args()

    P = dict(DEFAULTS)
    for k in DEFAULTS:
        if isinstance(DEFAULTS[k], tuple):
            continue
        val = getattr(args, k)
        P[k] = type(DEFAULTS[k])(val) if not isinstance(DEFAULTS[k], bool) else bool(val)

    # Coerce n_dirty_steps to int (argparse made it float)
    P["n_dirty_steps"] = int(round(P["n_dirty_steps"]))

    doses = [float(x) for x in args.doses.split(",")]
    print(f"# NHEJ replication run: doses={doses} n_cells={args.n_cells} seed={args.seed}")
    print(f"# Parameters: {json.dumps({k:v for k,v in P.items() if not isinstance(v,tuple)})}")
    t0 = time.time()
    results = run_dose_response(doses, args.n_cells, P, base_seed=args.seed)
    elapsed = time.time() - t0
    print(f"# wall time = {elapsed:.1f} s")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(dict(parameters=P, doses=doses, n_cells=args.n_cells,
                       seed=args.seed, wall_time_s=elapsed, results=results),
                  f, indent=2)
    # console summary
    print("\nDose(Gy)  init_DSB  rejoined  mis_frac  residual_DSB  frac@24h")
    for r in results:
        f24 = r["mean_residual_fraction"][-1]
        print(f" {r['dose_gy']:6.2f}   {r['init_dsb']:7.1f}  {r['rejoined']:7.1f}  "
              f"{r['misrejoin_fraction']:6.3f}    {r['residual_dsb']:7.2f}    {f24:6.3f}")


if __name__ == "__main__":
    main()
