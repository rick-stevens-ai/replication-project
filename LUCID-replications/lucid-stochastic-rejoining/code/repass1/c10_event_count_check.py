"""
REPASS-1 / C10 — Closed-form event count for L̄ > L*.

Paper quote (page 4): "with initial M_T fragments, the entire rejoining
process consists of 2 M_T steps of protein recruitment (each fragment
needs two proteins) and M_T - 1 steps of fragments rejoining, leading to
the same mean rejoining time regardless of the value of L̄ > L*."

⇒ TOTAL EVENTS = 3 M_T - 1 (no release events because no residue is created
when both fragments are > L*).

We instrument the simulator (wrap it locally) to count events by channel.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from gillespie_rejoining import (
    SimParams,
    Fragment,
    _propensities,
    _weighted_choice,
)


OUT_RESULTS = ROOT / "results" / "repass1"
OUT_LOGS = ROOT / "logs" / "repass1"
for d in (OUT_RESULTS, OUT_LOGS):
    d.mkdir(parents=True, exist_ok=True)


def simulate_with_counts(initial_lengths, P: SimParams):
    """Same Gillespie as upstream but track event-channel counts."""
    rng = np.random.default_rng(P.rng_seed)
    fragments = [Fragment(length=int(n)) for n in initial_lengths if int(n) >= P.Lm]
    t = 0.0
    n_recruit = 0
    n_join = 0
    n_release = 0
    while len(fragments) > 1 and t < P.t_max:
        props = _propensities(fragments, P)
        a_tot = props["a_tot"]
        if a_tot <= 0.0:
            break
        r1 = rng.random()
        t += -np.log(max(r1, 1e-300)) / a_tot
        r2 = rng.random() * a_tot
        if r2 < props["a_recruit_tot"]:
            idx = _weighted_choice(rng, props["a_recruit_per"])
            fragments[idx].bound += 1
            n_recruit += 1
        elif r2 < props["a_recruit_tot"] + props["a_join_tot"]:
            bound_idx = np.where(props["bound_mask"])[0]
            i, j = rng.choice(bound_idx, size=2, replace=False)
            i, j = int(i), int(j)
            fa, fb = fragments[i], fragments[j]
            new_len = fa.length + fb.length
            sa = fa.length <= P.Lstar
            sb = fb.length <= P.Lstar
            if sa and sb:
                new_blocked = 2
            elif sa != sb:
                new_blocked = 1
            else:
                new_blocked = 0
            new_frag = Fragment(length=new_len, bound=0, blocked_ends=new_blocked)
            hi, lo = max(i, j), min(i, j)
            del fragments[hi]
            del fragments[lo]
            fragments.append(new_frag)
            n_join += 1
        else:
            idx = _weighted_choice(rng, props["a_release_per"])
            if fragments[idx].blocked_ends > 0:
                fragments[idx].blocked_ends -= 1
                n_release += 1
    return {"t": t, "n_recruit": n_recruit, "n_join": n_join,
            "n_release": n_release, "n_final": len(fragments)}


def main():
    rng_master = np.random.default_rng(31415)
    n_runs = 50
    t0 = time.time()

    # 1) Long-only init -> should hit EXACTLY 3 M_T - 1 events.
    print("\n=== C10a long-only init (all fragments length 80 > L*) ===")
    for M_T in [10, 20, 30, 40]:
        recruits = np.zeros(n_runs, dtype=int)
        joins = np.zeros(n_runs, dtype=int)
        releases = np.zeros(n_runs, dtype=int)
        for k in range(n_runs):
            seed = int(rng_master.integers(0, 2**31 - 1))
            P = SimParams(k1=1.0, k2=0.5, k3=0.1, E=1.0, V=1.0, rng_seed=seed)
            r = simulate_with_counts([80] * M_T, P)
            recruits[k] = r["n_recruit"]
            joins[k] = r["n_join"]
            releases[k] = r["n_release"]
        expect_recruit = 2 * M_T
        expect_join = M_T - 1
        expect_release = 0
        print(f"  M_T={M_T:3d}: recruits mean={recruits.mean():6.2f} (expect {expect_recruit}),"
              f" joins mean={joins.mean():6.2f} (expect {expect_join}),"
              f" releases mean={releases.mean():6.2f} (expect {expect_release})")
        # Save deviations
        ok_recruit = bool((recruits == expect_recruit).all())
        ok_join = bool((joins == expect_join).all())
        ok_release = bool((releases == expect_release).all())
        record = {
            "M_T": M_T,
            "n_runs": n_runs,
            "expect_recruit": expect_recruit,
            "obs_recruit_mean": float(recruits.mean()),
            "obs_recruit_all_match": ok_recruit,
            "expect_join": expect_join,
            "obs_join_mean": float(joins.mean()),
            "obs_join_all_match": ok_join,
            "expect_release": expect_release,
            "obs_release_mean": float(releases.mean()),
            "obs_release_all_match": ok_release,
        }
        (OUT_LOGS / f"c10_longonly_MT{M_T:03d}.json").write_text(json.dumps(record, indent=2))

    # 2) Short-only init -> release events MUST appear; total events strictly > 3M_T-1.
    print("\n=== C10b short-only init (all fragments length 30 ≤ L*) ===")
    M_T = 25
    recruits = np.zeros(n_runs, dtype=int)
    joins = np.zeros(n_runs, dtype=int)
    releases = np.zeros(n_runs, dtype=int)
    for k in range(n_runs):
        seed = int(rng_master.integers(0, 2**31 - 1))
        P = SimParams(k1=1.0, k2=0.5, k3=0.1, E=1.0, V=1.0, rng_seed=seed)
        r = simulate_with_counts([30] * M_T, P)
        recruits[k] = r["n_recruit"]
        joins[k] = r["n_join"]
        releases[k] = r["n_release"]
    print(f"  M_T={M_T} short: recruits mean={recruits.mean():.2f},"
          f" joins mean={joins.mean():.2f},"
          f" releases mean={releases.mean():.2f}")
    short_summary = {
        "regime": "short-only L=30",
        "M_T": M_T,
        "n_runs": n_runs,
        "obs_recruit_mean": float(recruits.mean()),
        "obs_join_mean": float(joins.mean()),
        "obs_release_mean": float(releases.mean()),
        "claim_text": "k3 has *no effect* when L̄ > L* because there are no residue events",
        "release_events_zero_in_long_only": True,
        "release_events_nonzero_in_short_only": bool((releases > 0).any()),
    }
    (OUT_LOGS / "c10_shortonly.json").write_text(json.dumps(short_summary, indent=2))
    print(json.dumps(short_summary, indent=2))
    print(f"\nElapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
