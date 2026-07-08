"""
Two encoders for the d=3 planar surface code |0_L> state:

1. NAIVE encoder (Gottesman-style, O(L^2) depth):
   - For each X-stabilizer, use one ancilla qubit prepared in |+>, apply CNOTs
     from ancilla to each data qubit in the stabilizer's support.
   - Actually simpler for |0_L> state: use the direct Gottesman "measurement-free"
     approach: initialize data qubits in |0>, then for each X-stab, use a
     Hadamard+CNOT chain to project onto its +1 eigenstate. This gives depth
     scaling roughly O(number_of_X_stabs * max_weight) = O(L^2).
   - This is essentially the Dennis et al. construction.

2. OPTIMIZED encoder (Higgott et al. 2020, depth 2L = 6 for L=3):
   - Uses the base-case construction from Appendix B: 6 time steps of
     nearest-neighbor CNOT + H gates that prepare a valid d=3 planar |0_L>.
   - We construct it explicitly by (a) initializing each data qubit in |0> or |+>
     according to the stabilizer type it "belongs to", and (b) applying a small
     sequence of local CNOTs that builds up each stabilizer's +1 eigenvalue.

For both, we verify the output using Stim's TableauSimulator:
- Compute the reduced stabilizer generators of the output state.
- Check every code stabilizer is in the stabilizer group of the output state
  (evaluates to +1 with high probability, deterministically for a stabilizer state).
- Check the logical Z is also a +1 stabilizer of the output state (that's the
  |0_L> criterion).

For |0_L>: the state should be a +1 eigenstate of all X-stabs, all Z-stabs, AND logical Z.

Depth counting: we count the number of "time steps" where a time step is a set
of gates that can be applied in parallel because they act on disjoint qubit sets.
"""

import stim
from surface_code_d3 import build_d3_planar_surface_code, verify_code_structure


class Encoder:
    """Records a sequence of gates as (time_step, gate_type, qubits)."""

    def __init__(self, n):
        self.n = n
        self.ops = []  # list of (time_step, gate, qubits_tuple)
        self.current_step = 0
        self.step_qubits = set()  # qubits used in the current step

    def _reserve(self, qubits):
        """Bump to a new time step if any qubit is already used in the current step."""
        qset = set(qubits)
        if qset & self.step_qubits:
            self.current_step += 1
            self.step_qubits = set()
        self.step_qubits |= qset

    def H(self, q):
        self._reserve([q])
        self.ops.append((self.current_step, 'H', (q,)))

    def CNOT(self, c, t):
        self._reserve([c, t])
        self.ops.append((self.current_step, 'CNOT', (c, t)))

    def RESET_Z(self, q):
        # |0> reset, done at the start (time_step 0 by convention; not counted in depth)
        self.ops.append((-1, 'R', (q,)))

    def RESET_X(self, q):
        # |+> reset (R then H)
        self.ops.append((-1, 'RX', (q,)))

    def depth(self):
        gate_steps = [t for (t, g, q) in self.ops if t >= 0]
        if not gate_steps:
            return 0
        return max(gate_steps) + 1

    def two_qubit_gate_count(self):
        return sum(1 for (t, g, q) in self.ops if g == 'CNOT')

    def one_qubit_gate_count(self):
        return sum(1 for (t, g, q) in self.ops if g == 'H')

    def to_stim_circuit(self):
        c = stim.Circuit()
        # Group by time step; put resets first
        resets = [(g, q) for (t, g, q) in self.ops if t == -1]
        # Group data qubits — those not explicitly reset — into R (|0>) by default
        reset_qubits = set()
        for g, q in resets:
            reset_qubits.add(q[0])
            if g == 'R':
                c.append('R', list(q))
            elif g == 'RX':
                c.append('R', list(q))
                c.append('H', list(q))
        # Any qubit 0..n-1 not reset explicitly: reset to |0> so simulator is well-defined
        for q in range(self.n):
            if q not in reset_qubits:
                c.append('R', [q])
        # Now gates in order of time step
        gates_by_step = {}
        for (t, g, q) in self.ops:
            if t < 0:
                continue
            gates_by_step.setdefault(t, []).append((g, q))
        for step in sorted(gates_by_step.keys()):
            c.append('TICK')
            for g, q in gates_by_step[step]:
                if g == 'H':
                    c.append('H', list(q))
                elif g == 'CNOT':
                    c.append('CNOT', list(q))
        return c


def build_naive_encoder(code):
    """
    Naive Dennis-et-al style encoder for |0_L> of the d=3 planar surface code.

    Strategy (measurement-free version):
    - Initialize every data qubit in |0>. This is already a +1 eigenstate of every Z-stab
      and of the logical Z.
    - For each X-stab, we need to project the state onto its +1 eigenspace.
      For a Pauli operator P with |0..0> as input, applying the "controlled Pauli chain"
      of the form:
          H q0; CNOT q0->q1; CNOT q0->q2; ... CNOT q0->qk
      creates the state (|0...0> + |1...1>)/sqrt(2) supported on q0..qk, which is a
      +1 eigenstate of X_{q0}X_{q1}...X_{qk}. This adds Z-stabilizer ZZ pairs but those
      commute with the existing Z-stabs.
    - Because each X-stab shares qubits with others, this needs to be done sequentially
      per X-stab to avoid violating already-established stabilizers. So depth ~ sum over
      X-stabs of (1 H + weight-1 CNOTs) done serially = O(sum weights) = O(L^2).

    IMPORTANT: this simple approach only works if the X-stabs are independent (their +1
    eigenstates are compatible with the |0..0> Z-stab structure). For the surface code,
    all X-stabs and Z-stabs are compatible by construction. However doing the H+CNOTs
    per-stab naively will destroy earlier stabs unless we're careful.

    Correct approach: Use the Cleve-Gottesman canonical encoder built from row-reduction
    of the stabilizer generators. Here we use a simpler variant that works for CSS codes:
    - Start with |0...0>.
    - For each X-stab in some fixed order, do: H q_first; CNOT q_first -> q_others.
      Do NOT reuse q_first as a "seed" for a subsequent stab. Choose a distinct seed
      qubit for each X-stab. If we can pick a distinct seed qubit for each X-stab (each
      being in only that one X-stab's "seed slot"), the CNOTs from that seed to others
      don't collide.

    For d=3 planar code with 6 X-stabs of weight 3-4, we need 6 distinct seed qubits.
    Total qubits = 13, so this is feasible. We pick seeds that appear in only one X-stab
    if possible.

    Depth analysis of the naive: each X-stab needs 1 H + (weight-1) sequential CNOTs.
    Doing them all serially: sum = 6 H's + (3+3+3+3+3+3 with weights 3,4,3,3,4,3) - 6 = 20 - 6 = 14.
    Wait, weights are 3,4,3,3,4,3 => CNOTs = 2+3+2+2+3+2 = 14. Plus 6 H's.
    In serial, that's 6+14 = 20 time steps. That's the "naive" depth for L=3.

    Compare paper: 2L = 6 time steps.
    Ratio: 20/6 ≈ 3.3x.
    """
    enc = Encoder(code['n'])
    # All qubits start in |0>
    for q in range(code['n']):
        enc.RESET_Z(q)

    # For each X-stab, apply H to the "seed" qubit, then CNOTs from seed to others.
    # Pick seeds: for stabs (0,3,5),(1,3,4,6),(2,4,7),(5,8,10),(6,8,9,11),(7,9,12)
    # pick 0, 1, 2, 10, 11, 12 as seeds (each unique to its stab except position within)
    seed_map = {
        (0, 3, 5): 0,
        (1, 3, 4, 6): 1,
        (2, 4, 7): 2,
        (5, 8, 10): 10,
        (6, 8, 9, 11): 11,
        (7, 9, 12): 12,
    }
    # Force serial execution: after each H, do CNOTs, then bump step
    for xs in code['x_stabs']:
        seed = seed_map[xs]
        others = [q for q in xs if q != seed]
        # Force new time step (serial for naive)
        enc.current_step += 1
        enc.step_qubits = set()
        enc.H(seed)
        for o in others:
            enc.current_step += 1
            enc.step_qubits = set()
            enc.CNOT(seed, o)
    return enc


def build_optimized_encoder_d3(code):
    """
    Optimized d=3 planar surface code encoder for |0_L>, aiming for depth 2L=6.

    Strategy (based on Higgott et al. Appendix B / Fig. 9 for L=3):
    Since we're encoding |0_L> (not an arbitrary state), we can use a slightly
    simpler approach than the general Higgott circuit while still hitting depth ≤ 2L.

    Approach:
    1. Initialize data qubits: those that are "X-stab seeds" in |+>, rest in |0>.
       For the d=3 planar code, we can pick 6 "X-seed" qubits (one per X-stab) that
       are also mutually disjoint from the point of view of the CNOTs to be applied.
       Choose seeds: one per X-stab, at a qubit that's ONLY in that X-stab (not shared).
       Looking at X-stabs:
         X0: (0,3,5)      — qubit 0 is only in X0 (also in Z0)
         X1: (1,3,4,6)    — qubit 1 is only in X1
         X2: (2,4,7)      — qubit 2 is only in X2
         X3: (5,8,10)     — qubit 10 is only in X3
         X4: (6,8,9,11)   — qubit 11 is only in X4
         X5: (7,9,12)     — qubit 12 is only in X5
       Seeds: 0,1,2,10,11,12. Initialize these 6 in |+>, rest (3,4,5,6,7,8,9) in |0>.
    2. For each X-stab, apply CNOTs from its seed to the other qubits in the stab.
       To hit depth ≤ 2L = 6, we need to schedule these CNOTs in parallel as much as possible.
       Total CNOTs = 2+3+2+2+3+2 = 14. Distributed over 6 time steps, we need to average
       ~2.3 CNOTs per step, all disjoint. Given only 6 seeds and 13 qubits, this should
       be schedulable with a careful ordering.

    Manual schedule (verified below):
      seeds: 0(→3,5), 1(→3,4,6), 2(→4,7), 10(→5,8), 11(→6,8,9), 12(→7,9)
      
    Step 1: (0→3), (1→4), (2→7), (11→6), (12→9)      [5 CNOTs, disjoint]
    Step 2: (0→5), (1→3), (2→4), (10→8), (11→9)      [wait, need to check]

    Actually let me schedule by grouping by target-qubit conflicts.
    A CNOT (c,t) conflicts with (c',t') if {c,t} & {c',t'} != empty.

    List of CNOTs: [(0,3),(0,5),(1,3),(1,4),(1,6),(2,4),(2,7),(10,5),(10,8),(11,6),(11,8),(11,9),(12,7),(12,9)]
    Greedy scheduling (14 CNOTs):

    Step 1 (qubits used): (0,3), (1,4), (2,7), (11,6), (10,8) — uses {0,3,1,4,2,7,11,6,10,8}, leaves {5,9,12}
       Can we add (12,9)? qubits {12,9} not in used set ✓. Add it.
       Step 1: (0,3),(1,4),(2,7),(11,6),(10,8),(12,9) — 6 CNOTs, uses 12 qubits.
    Step 2: remaining = [(0,5),(1,3),(1,6),(2,4),(10,5),(11,8),(11,9),(12,7)]
       (0,5): uses 0,5. (1,3): uses 1,3. (2,4): uses 2,4. (11,8): uses 11,8. (12,7): uses 12,7.
       => (0,5),(1,3),(2,4),(11,8),(12,7): 5 CNOTs, disjoint. Used {0,5,1,3,2,4,11,8,12,7}.
       Left over: (1,6),(10,5),(11,9). Can't add (1,6) (1 used), (10,5) (5 used), (11,9) (11 used).
       Step 2: 5 CNOTs.
    Step 3: remaining = [(1,6),(10,5),(11,9)]
       All 3 are disjoint from each other: (1,6),(10,5),(11,9). Add all.
       Step 3: 3 CNOTs.

    Total: 6 + 5 + 3 = 14 CNOTs in 3 time steps.
    Plus initial |+> preparation = 1 H time step (parallel on 6 qubits).
    Total depth = 1 (H) + 3 (CNOTs) = 4 time steps.

    But wait — the CORRECTNESS is what needs checking. The naive seed-then-CNOTs
    approach, when done in parallel across X-stabs, only works if the CNOTs from
    different seeds don't interfere.

    Two CNOTs (a→b) and (c→d) commute UNLESS b=c or a=d (in which case they don't
    fully commute; a=c or b=d is fine).

    For the state semantics: after applying H on seed s, the state is a superposition
    that gets entangled with CNOTs. If we apply CNOT(s1, t) then CNOT(s2, t) where s1 ≠ s2,
    the result is more complex than just doing them per-stab.

    Let me verify with Stim: I'll BUILD this schedule and CHECK whether the resulting
    state has all stabilizers = +1. If it does, the parallel schedule is valid.
    """

    enc = Encoder(code['n'])
    seeds = {0, 1, 2, 10, 11, 12}
    # Init: seeds in |+>, others in |0>
    for q in range(code['n']):
        if q in seeds:
            enc.RESET_X(q)
        else:
            enc.RESET_Z(q)
    # Time step 0: no H needed here since RX handles it. Move to CNOTs.

    # Step 1
    for (c, t) in [(0, 3), (1, 4), (2, 7), (11, 6), (10, 8), (12, 9)]:
        enc.CNOT(c, t)
    # Force new step
    enc.current_step += 1
    enc.step_qubits = set()
    # Step 2
    for (c, t) in [(0, 5), (1, 3), (2, 4), (11, 8), (12, 7)]:
        enc.CNOT(c, t)
    enc.current_step += 1
    enc.step_qubits = set()
    # Step 3
    for (c, t) in [(1, 6), (10, 5), (11, 9)]:
        enc.CNOT(c, t)

    return enc


def verify_encoder(enc, code):
    """
    Use Stim's TableauSimulator to verify the encoded state is a valid |0_L>:
    all X-stabs, Z-stabs, and logical_Z are +1 stabilizers of the output state.
    """
    circuit = enc.to_stim_circuit()
    sim = stim.TableauSimulator()
    sim.do_circuit(circuit)

    n = code['n']

    results = {}

    # Check every X stabilizer: measure X_S; must be +1 deterministic
    for i, xs in enumerate(code['x_stabs']):
        pauli_str = ['_'] * n
        for q in xs:
            pauli_str[q] = 'X'
        p = stim.PauliString(''.join(pauli_str))
        # peek_observable_expectation is deterministic for stabilizer states
        exp = sim.peek_observable_expectation(p)
        results[f'X_stab_{i}'] = (xs, exp)

    for i, zs in enumerate(code['z_stabs']):
        pauli_str = ['_'] * n
        for q in zs:
            pauli_str[q] = 'Z'
        p = stim.PauliString(''.join(pauli_str))
        exp = sim.peek_observable_expectation(p)
        results[f'Z_stab_{i}'] = (zs, exp)

    # Check logical Z (must be +1 for |0_L>)
    pauli_str = ['_'] * n
    for q in code['logical_z']:
        pauli_str[q] = 'Z'
    p = stim.PauliString(''.join(pauli_str))
    exp = sim.peek_observable_expectation(p)
    results['logical_Z'] = (code['logical_z'], exp)

    # Check logical X (should be 0 - undefined, since |0_L> is not X eigenstate)
    pauli_str = ['_'] * n
    for q in code['logical_x']:
        pauli_str[q] = 'X'
    p = stim.PauliString(''.join(pauli_str))
    exp = sim.peek_observable_expectation(p)
    results['logical_X'] = (code['logical_x'], exp)

    return results


if __name__ == "__main__":
    code = build_d3_planar_surface_code()
    verify_code_structure(code)

    print("=" * 70)
    print("NAIVE ENCODER (Dennis-et-al-style, serial)")
    print("=" * 70)
    naive = build_naive_encoder(code)
    print(f"Depth: {naive.depth()} time steps")
    print(f"2-qubit gates (CNOT): {naive.two_qubit_gate_count()}")
    print(f"1-qubit gates (H): {naive.one_qubit_gate_count()}")
    naive_results = verify_encoder(naive, code)
    all_naive_ok = True
    for name, (supp, exp) in naive_results.items():
        expected = 1 if name != 'logical_X' else 0
        # For logical_X we expect uncertain (either +1 or 0). Just note it.
        ok = ('+1' if abs(exp - 1.0) < 1e-9 else ('-1' if abs(exp + 1.0) < 1e-9 else f'undefined({exp:.3f})'))
        if name != 'logical_X':
            valid = abs(exp - 1.0) < 1e-9
            all_naive_ok = all_naive_ok and valid
            print(f"  {name}: qubits {supp} -> {ok} {'✓' if valid else '✗'}")
        else:
            print(f"  {name}: qubits {supp} -> {ok} (expected undefined for |0_L>)")
    print(f"NAIVE valid |0_L>: {'YES' if all_naive_ok else 'NO'}")

    print()
    print("=" * 70)
    print("OPTIMIZED ENCODER (parallel-scheduled, paper claims 2L=6 for d=3)")
    print("=" * 70)
    opt = build_optimized_encoder_d3(code)
    print(f"Depth: {opt.depth()} time steps")
    print(f"2-qubit gates (CNOT): {opt.two_qubit_gate_count()}")
    print(f"1-qubit gates (H): {opt.one_qubit_gate_count()}")
    opt_results = verify_encoder(opt, code)
    all_opt_ok = True
    for name, (supp, exp) in opt_results.items():
        ok = ('+1' if abs(exp - 1.0) < 1e-9 else ('-1' if abs(exp + 1.0) < 1e-9 else f'undefined({exp:.3f})'))
        if name != 'logical_X':
            valid = abs(exp - 1.0) < 1e-9
            all_opt_ok = all_opt_ok and valid
            print(f"  {name}: qubits {supp} -> {ok} {'✓' if valid else '✗'}")
        else:
            print(f"  {name}: qubits {supp} -> {ok} (expected undefined for |0_L>)")
    print(f"OPTIMIZED valid |0_L>: {'YES' if all_opt_ok else 'NO'}")

    print()
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print(f"Naive depth:      {naive.depth()} time steps  ({naive.two_qubit_gate_count()} CNOTs)")
    print(f"Optimized depth:  {opt.depth()} time steps  ({opt.two_qubit_gate_count()} CNOTs)")
    print(f"Paper claim (2L): {2*code['L']} time steps for d={code['L']}")
    print(f"Speedup:          {naive.depth() / opt.depth():.2f}x depth reduction")
