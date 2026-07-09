"""Quick smoke test: run a single small simulation, check that it completes."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gillespie_rejoining import (
    SimParams, simulate, initial_uniform_same_length,
    initial_high_LET_Fe_1Gy,
)
import numpy as np


def main():
    print("Smoke test 1: 5 long fragments, V=1, default rates")
    P = SimParams(k1=0.1, k2=0.5, k3=0.05, E=10.0, V=1.0, rng_seed=42, t_max=1e5)
    t_end, traj = simulate(initial_uniform_same_length(60, 5), P)
    print(f"  Done t={t_end:.3f}, {len(traj)} traj points, final frags={traj[-1].n_fragments}")
    assert traj[-1].n_fragments == 1, "Expected 1 fragment at completion"

    print("Smoke test 2: 10 short fragments (n=20 < L*), needs release steps")
    P = SimParams(k1=0.1, k2=0.5, k3=0.05, E=10.0, V=1.0, rng_seed=7, t_max=1e5)
    t_end, traj = simulate(initial_uniform_same_length(20, 10), P)
    print(f"  Done t={t_end:.3f}, {len(traj)} traj points, final frags={traj[-1].n_fragments}")
    assert traj[-1].n_fragments == 1

    print("Smoke test 3: mixed 30-DSB high-LET initial")
    rng = np.random.default_rng(0)
    lens = initial_high_LET_Fe_1Gy(rng, n_dsb=30, frac_short=0.30)
    print(f"  Initial lengths: {lens}")
    P = SimParams(k1=0.05, k2=0.25, k3=0.02, E=10.0, V=1.0, rng_seed=1, t_max=5e5)
    t0 = time.time()
    t_end, traj = simulate(lens, P)
    print(f"  Done t={t_end:.2f}, wallclock={time.time()-t0:.2f}s, final frags={traj[-1].n_fragments}")

    print("Smoke test 4: include short (<Lm) fragments — they should be dropped")
    lens = [10, 12, 15, 20, 50, 60, 80, 5]
    P = SimParams(k1=0.1, k2=0.5, k3=0.05, E=10.0, V=1.0, rng_seed=2, t_max=1e5)
    t_end, traj = simulate(lens, P)
    print(f"  Done t={t_end:.3f}, final frags={traj[-1].n_fragments}")
    # lens >= Lm(=15): [15, 20, 50, 60, 80] -> 5
    assert traj[0].n_fragments == 5, f"Expected 5 (kept >=15), got {traj[0].n_fragments}"

    print("\nAll smoke tests passed.")


if __name__ == "__main__":
    main()
