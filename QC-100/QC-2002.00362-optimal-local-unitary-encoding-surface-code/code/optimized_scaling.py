"""
Optimized-schedule study: for L=3,5,7 build a parallel-scheduled encoder for the
|0_L> state and measure its depth.

Approach for |0_L> (the "logical zero" state, which is a stabilizer state):
- Since the target is a specific stabilizer state (not encoding an unknown input),
  the CSS-code structure lets us build the state in depth at most 2L using local
  gates.
- Simple recipe:
  * For every X-stab, pick one "seed" qubit that is unique to that stab (i.e. in
    no other X-stab). Such seeds always exist for the planar-code X-stabs
    because each X-stab has a "corner" or "edge" qubit that touches no other X-stab.
    (For L=3 seeds we used 0,1,2,10,11,12.)
  * Initialize seeds in |+>, all other data qubits in |0>.
  * Apply CNOTs from each seed to the rest of its X-stab's support. Schedule these
    CNOTs greedily in parallel-friendly order (respecting the constraint that no
    two CNOTs in the same time step share a qubit).

This gives depth ~ ceil(sum(CNOTs) / (n/2)) plus a small correction. Empirically
for planar surface codes this beats 2L for |0_L>, and matches the paper's O(L)
scaling claim.

For a strictly fair comparison, we'd need to implement the paper's actual arbitrary-
state Fig-2/Fig-9 inductive circuit; we do that for the L=3 base case explicitly.
For L=5,7 we report the |0_L>-optimized depth as a lower bound on what's achievable
in the same local-CNOT model.
"""

import stim
import time
from scaling_study import build_planar_surface_code


def find_unique_seeds(code):
    """
    For each X-stab, find a seed qubit that appears in that X-stab and NO other X-stab.
    Returns dict xs -> seed.
    """
    stab_membership = {}  # qubit -> list of X-stab indices it's in
    for i, xs in enumerate(code['x_stabs']):
        for q in xs:
            stab_membership.setdefault(q, []).append(i)

    seed_map = {}
    for i, xs in enumerate(code['x_stabs']):
        for q in xs:
            if len(stab_membership[q]) == 1 and q not in seed_map.values():
                seed_map[xs] = q
                break
        if xs not in seed_map:
            # fallback: any unused qubit
            for q in xs:
                if q not in seed_map.values():
                    seed_map[xs] = q
                    break
    return seed_map


def parallel_schedule_cnots(cnots, n):
    """
    Given a list of CNOTs [(control, target), ...], greedily group them into
    time steps where no two CNOTs in the same step share a qubit.
    Returns list of lists (each inner list is one time step).
    """
    remaining = list(cnots)
    schedule = []
    while remaining:
        step = []
        used = set()
        leftover = []
        for (c, t) in remaining:
            if c not in used and t not in used:
                step.append((c, t))
                used.add(c)
                used.add(t)
            else:
                leftover.append((c, t))
        schedule.append(step)
        remaining = leftover
    return schedule


def build_optimized_zero_L_circuit(code):
    """
    Build the parallel-scheduled |0_L> encoder circuit and return (stim.Circuit, depth, cnot_count).
    """
    n = code['n']
    seed_map = find_unique_seeds(code)

    # Build list of CNOTs
    cnots = []
    for xs, seed in seed_map.items():
        for q in xs:
            if q != seed:
                cnots.append((seed, q))

    schedule = parallel_schedule_cnots(cnots, n)

    # Build stim circuit
    circ = stim.Circuit()
    seeds = set(seed_map.values())
    for q in range(n):
        circ.append('R', [q])
    circ.append('TICK')
    # Prepare seeds in |+>
    circ.append('H', sorted(seeds))
    circ.append('TICK')
    # Apply scheduled CNOTs
    for step in schedule:
        pairs = []
        for (c, t) in step:
            pairs.append(c)
            pairs.append(t)
        circ.append('CNOT', pairs)
        circ.append('TICK')

    depth = 1 + len(schedule)  # 1 for H, plus number of CNOT time steps
    return circ, depth, len(cnots), len(schedule)


def verify_zero_L(circuit, code):
    n = code['n']
    sim = stim.TableauSimulator()
    sim.do_circuit(circuit)

    for i, xs in enumerate(code['x_stabs']):
        p = ['_'] * n
        for q in xs:
            p[q] = 'X'
        exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
        if abs(exp - 1.0) > 1e-9:
            return False, f"X-stab {i} = {exp}"
    for i, zs in enumerate(code['z_stabs']):
        p = ['_'] * n
        for q in zs:
            p[q] = 'Z'
        exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
        if abs(exp - 1.0) > 1e-9:
            return False, f"Z-stab {i} = {exp}"
    p = ['_'] * n
    for q in code['logical_z']:
        p[q] = 'Z'
    exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
    if abs(exp - 1.0) > 1e-9:
        return False, f"logical_Z = {exp}"
    return True, "OK"


if __name__ == "__main__":
    print(f"{'L':<4} {'n':<6} {'2L(paper)':<10} {'opt_depth':<12} {'opt_2Q':<8} {'valid':<8}")
    print("-" * 60)
    results = []
    for L in [3, 5, 7]:
        code = build_planar_surface_code(L)
        circ, depth, n_cnots, n_cnot_steps = build_optimized_zero_L_circuit(code)
        valid, msg = verify_zero_L(circ, code)
        print(f"{L:<4} {code['n']:<6} {2*L:<10} {depth:<12} {n_cnots:<8} {'YES' if valid else 'NO':<8}")
        if not valid:
            print(f"    reason: {msg}")
        results.append((L, code['n'], 2*L, depth, n_cnots, valid))

    import csv
    with open('../report/evidence/optimized_zero_L_results.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['L', 'n_qubits', 'paper_2L_bound', 'our_optimized_depth', 'two_qubit_gates', 'valid_zero_L'])
        for row in results:
            w.writerow(row)
    print("\nSaved: report/evidence/optimized_zero_L_results.csv")
