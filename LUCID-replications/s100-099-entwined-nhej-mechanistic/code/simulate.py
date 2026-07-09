"""
Per-DSB Gillespie simulator of the DaMaRiS pathway.

Each DSB consists of TWO ends initially placed in close proximity (the
canonical DaMaRiS topology where the two ends of a break are spatially
correlated).  The synapsis (pair) reaction is therefore overwhelmingly
intra-DSB; we model it with a fast intra-DSB synapsis rate k_self plus a
slow inter-DSB mis-rejoin rate k_cross.  Both are calibrated from the
DaMaRiS sub-diffusion CTRW behaviour (DaMaRiS.run defaults: 25 nm reaction
range, 1.4 nm^2/s effective D).

For a given DSB with two ends both in DSBEnd_PKcs (or DSBEnd_PK_MRN), the
mean intra-pair synapsis time is governed by the local diffusion within
~50 nm.  Published DaMaRiS WT NHEJ kinetics show t1/2 ≈ 20-30 min for
the fast component, which is dominated by:
    end-cleaning (~4 s) + Ku (1.1) + PKcs (1.2) + synapsis (~few min)
    + stabilise (250 s) + clean backbone (300 s) + clean base (900 s)
    + ligate (1200 s)  ~ 45 min for full pipeline.
So intra-DSB synapsis mean must be ~30-60 s.  We use 60 s.

This model is well-mixed only ACROSS DSBs (used for cross-DSB pairing,
which is rare).  Within a DSB the two-end state vector is tracked
explicitly.
"""

from __future__ import annotations
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from damaris_pathway import (
    Transition, SCENARIOS, apply_deficiency,
    REPAIRED_STATES, SYNAPTIC_STATES, END_STATES_BROKEN,
)


# --- physics --- #
INTRA_SYNAPSIS_TAU_S = 60.0   # mean time for two adjacent PKcs ends to pair
CROSS_SYNAPSIS_TAU_S = 1e6    # mean time for inter-DSB mis-rejoin (very slow)


@dataclass
class DSB:
    """A single DSB owns two end-state slots.  Once paired, state is held
    on synaptic_state and end_a / end_b are None."""
    end_a: Optional[str] = "DSBEnd"
    end_b: Optional[str] = "DSBEnd"
    synaptic_state: Optional[str] = None    # one of SYNAPTIC_STATES if paired
    repaired_via: Optional[str] = None       # "NHEJ" or "HR" or None

    def is_repaired(self) -> bool:
        return self.repaired_via is not None

    def is_broken(self) -> bool:
        """Counts as a residual DSB (contributes a γ-H2AX focus)."""
        return self.repaired_via is None


def _first_order_transitions_for(state: str,
                                 first_idx: dict[str, list[Transition]]
                                 ) -> list[Transition]:
    return first_idx.get(state, [])


def _sim_one(
    n_dsb: int,
    transitions: list[Transition],
    pair_reactions: list[tuple[str, str, str]],
    t_end_s: float,
    sample_times_s: np.ndarray,
    rng: random.Random,
) -> "Trace":
    first_idx: dict[str, list[Transition]] = defaultdict(list)
    for t in transitions:
        first_idx[t.src].append(t)

    pair_set = set((a, b, p) for a, b, p in pair_reactions)
    pair_self = {(a, p) for a, b, p in pair_reactions if a == b}
    pair_cross = [(a, b, p) for a, b, p in pair_reactions if a != b]

    dsbs: list[DSB] = [DSB() for _ in range(n_dsb)]

    n_samples = len(sample_times_s)
    traj = np.empty(n_samples, dtype=np.float64)
    sample_idx = 0

    t = 0.0
    repaired_NHEJ = 0
    repaired_HR = 0

    def residual_dsb_count() -> int:
        return sum(1 for d in dsbs if d.is_broken())

    while t < t_end_s:
        # Build propensity list
        props: list[tuple[float, str, object]] = []

        # Per-DSB first-order transitions on each end OR on the synaptic state
        # Also intra-DSB synapsis (if both ends are pair-reactants)
        for di, d in enumerate(dsbs):
            if d.is_repaired():
                continue
            if d.synaptic_state is not None:
                # Only first-order on synaptic state
                for tr in first_idx.get(d.synaptic_state, ()):
                    props.append((1.0 / tr.tau, "synap", (di, tr)))
            else:
                # First-order on each end
                for slot, st in (("a", d.end_a), ("b", d.end_b)):
                    for tr in first_idx.get(st, ()):
                        props.append((1.0 / tr.tau, "end", (di, slot, tr)))
                # Intra-DSB synapsis (the two ends of this DSB pair)
                a, b = d.end_a, d.end_b
                # match against pair set in either order
                for ra, rb, prod in pair_reactions:
                    if (a == ra and b == rb) or (a == rb and b == ra):
                        props.append((1.0 / INTRA_SYNAPSIS_TAU_S,
                                      "synap_form_self", (di, prod)))
                        break  # one chance per DSB pair-product per step

        # Inter-DSB cross synapsis (very slow; treat as well-mixed across
        # the broken-end population).  Sum over distinct DSB pairs.
        if pair_cross:
            # Count end-states across DSBs
            end_states: dict[str, list[tuple[int, str]]] = defaultdict(list)
            for di, d in enumerate(dsbs):
                if d.is_repaired() or d.synaptic_state is not None:
                    continue
                end_states[d.end_a].append((di, "a"))
                end_states[d.end_b].append((di, "b"))
            for a, b, prod in pair_cross:
                la = end_states.get(a, [])
                lb = end_states.get(b, [])
                if not la or not lb:
                    continue
                pairs = len(la) * len(lb)
                rate = pairs / CROSS_SYNAPSIS_TAU_S
                props.append((rate, "synap_form_cross", (a, b, prod, la, lb)))

        a_tot = sum(r for r, _, _ in props)
        if a_tot <= 0:
            while sample_idx < n_samples:
                traj[sample_idx] = residual_dsb_count()
                sample_idx += 1
            break

        r1 = rng.random()
        dt = -math.log(r1 if r1 > 0 else 1e-300) / a_tot
        # Record samples up to t+dt
        cur_res = residual_dsb_count()
        while sample_idx < n_samples and sample_times_s[sample_idx] <= t + dt:
            traj[sample_idx] = cur_res
            sample_idx += 1
        t += dt
        if t >= t_end_s:
            break

        r2 = rng.random() * a_tot
        cum = 0.0
        chosen = props[-1]
        for entry in props:
            cum += entry[0]
            if cum >= r2:
                chosen = entry
                break

        kind = chosen[1]
        if kind == "end":
            di, slot, tr = chosen[2]
            d = dsbs[di]
            cur = d.end_a if slot == "a" else d.end_b
            if cur != tr.src:
                continue  # raced; skip
            if len(tr.dst) == 1:
                # single-end transition
                if slot == "a":
                    d.end_a = tr.dst[0]
                else:
                    d.end_b = tr.dst[0]
            else:
                # 2-product transition (only happens on synaptic dissociation
                # which won't be reached via "end" kind; ignore)
                if slot == "a":
                    d.end_a = tr.dst[0]
                else:
                    d.end_b = tr.dst[0]
            # Did this end reach a terminal state?
            for slot_name in ("a", "b"):
                end_state = d.end_a if slot_name == "a" else d.end_b
                if end_state == "DSB_Fixed_HR":
                    # HR completes per-end; once BOTH ends are repaired, the
                    # DSB is fixed via HR.  (DaMaRiS does this end-by-end.)
                    pass
            # If both ends have reached HR completion, DSB repaired via HR
            if d.end_a == "DSB_Fixed_HR" and d.end_b == "DSB_Fixed_HR":
                d.repaired_via = "HR"
                repaired_HR += 1
            # Special case: in DaMaRiS, even one end completing HR with the
            # partner still in earlier state is functionally an unresolved
            # break; we count repair only when both ends fixed.

        elif kind == "synap":
            di, tr = chosen[2]
            d = dsbs[di]
            if d.synaptic_state != tr.src:
                continue
            if len(tr.dst) == 1:
                d.synaptic_state = tr.dst[0]
                if tr.dst[0] == "DSB_Fixed":
                    d.repaired_via = "NHEJ"
                    repaired_NHEJ += 1
                    d.synaptic_state = None
            else:
                # 2-product (synaptic dissociation back to two ends)
                d.end_a, d.end_b = tr.dst[0], tr.dst[1]
                d.synaptic_state = None

        elif kind == "synap_form_self":
            di, prod = chosen[2]
            d = dsbs[di]
            d.synaptic_state = prod
            d.end_a = None
            d.end_b = None

        elif kind == "synap_form_cross":
            a, b, prod, la, lb = chosen[2]
            # Pick one (di_a, slot_a) and (di_b, slot_b) at random; merge into
            # a synapse owned by di_a.  This is a rare event.
            if not la or not lb:
                continue
            ia = la[rng.randrange(len(la))]
            ib = lb[rng.randrange(len(lb))]
            di_a, slot_a = ia
            di_b, slot_b = ib
            if di_a == di_b:
                continue  # same DSB; already handled by intra
            d_a = dsbs[di_a]
            d_b = dsbs[di_b]
            d_a.synaptic_state = prod
            d_a.end_a = None
            d_a.end_b = None
            # The other DSB loses one end; we model the orphan end as
            # immediately becoming unresolvable
            if slot_b == "a":
                d_b.end_a = "DSBEnd_Inhibited"  # orphan
            else:
                d_b.end_b = "DSBEnd_Inhibited"

    while sample_idx < n_samples:
        traj[sample_idx] = residual_dsb_count()
        sample_idx += 1

    resolved = repaired_NHEJ + repaired_HR
    unrepaired = max(0.0, 1.0 - resolved / max(n_dsb, 1))
    f_nhej = repaired_NHEJ / max(resolved, 1)
    f_hr = repaired_HR / max(resolved, 1)
    return Trace(sample_times_s.copy(), traj, f_nhej, f_hr, unrepaired)


@dataclass
class Trace:
    times: np.ndarray
    residual: np.ndarray
    fraction_NHEJ: float
    fraction_HR: float
    fraction_unrepaired: float


def run_scenario(
    scenario: str,
    deficiency: str,
    n_dsb: int = 70,
    n_repeats: int = 50,
    t_end_h: float = 8.0,
    n_samples: int = 33,
    seed: int = 1234,
) -> dict:
    transitions, pairs = SCENARIOS[scenario]()
    transitions = apply_deficiency(transitions, deficiency)
    t_end_s = t_end_h * 3600.0
    sample_times_s = np.linspace(0.0, t_end_s, n_samples)

    rng_master = random.Random(seed)
    traces = []
    fNH, fHR, fU = [], [], []
    for r in range(n_repeats):
        rng = random.Random(rng_master.random())
        tr = _sim_one(n_dsb, transitions, pairs, t_end_s, sample_times_s, rng)
        traces.append(tr)
        fNH.append(tr.fraction_NHEJ)
        fHR.append(tr.fraction_HR)
        fU.append(tr.fraction_unrepaired)

    residuals = np.stack([t.residual for t in traces], axis=0)
    mean_res = residuals.mean(axis=0)
    sem_res = residuals.std(axis=0, ddof=1) / math.sqrt(max(n_repeats, 2))

    t_norm_s = 0.5 * 3600.0
    norm_idx = int(np.argmin(np.abs(sample_times_s - t_norm_s)))
    norm = mean_res[norm_idx] if mean_res[norm_idx] > 0 else 1.0
    return {
        "scenario": scenario, "deficiency": deficiency,
        "n_dsb": n_dsb, "n_repeats": n_repeats,
        "times_h": sample_times_s / 3600.0,
        "residual_mean": mean_res, "residual_sem": sem_res,
        "residual_norm": mean_res / norm,
        "residual_norm_sem": sem_res / norm,
        "fraction_NHEJ": float(np.mean(fNH)),
        "fraction_HR": float(np.mean(fHR)),
        "fraction_unrepaired": float(np.mean(fU)),
    }


def goodness_of_fit(sim_t_h, sim_norm, exp_t_h, exp_norm, exp_sem) -> dict:
    sim_t = np.asarray(sim_t_h, dtype=float)
    sim_y = np.asarray(sim_norm, dtype=float)
    exp_t = np.asarray(exp_t_h, dtype=float)
    exp_y = np.asarray(exp_norm, dtype=float)
    exp_s = np.asarray(exp_sem, dtype=float)
    sim_at_exp = np.interp(exp_t, sim_t, sim_y)
    residuals = exp_y - sim_at_exp
    n = len(exp_t)
    scale = 100.0
    chi2 = float(np.sum((residuals * scale / (exp_s * scale)) ** 2))
    red_chi2 = chi2 / max(n - 1, 1)
    rmse = float(np.sqrt(np.mean((residuals * scale) ** 2)))
    return {"reduced_chi2": red_chi2, "rmse": rmse,
            "n_points": int(n), "residuals": residuals.tolist()}


if __name__ == "__main__":
    for sc in ("A", "B", "C", "D"):
        for cf in ("WT", "XLF", "Lig4"):
            out = run_scenario(sc, cf, n_dsb=50, n_repeats=20, t_end_h=8.0)
            print(f"  {sc} {cf:>4s}: fNHEJ={out['fraction_NHEJ']:.2f} "
                  f"fHR={out['fraction_HR']:.2f} fU={out['fraction_unrepaired']:.2f} "
                  f"resid8h/0.5h={out['residual_norm'][-1]:.3f}")
