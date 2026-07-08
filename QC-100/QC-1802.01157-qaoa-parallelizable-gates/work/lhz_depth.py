"""
Reproduce Lechner 2018 (arXiv:1802.01157) headline claim:
  "Thus a total number of 28 parallel gates is required to
   realize all constraints independent of the system size."

The LHZ mapping encodes an all-to-all connected N-spin Ising problem
into K = N(N-1)/2 physical qubits arranged on a square-lattice-like
layout, with K-N+1 four-body plaquette constraints on the plaquettes.

Each 4-body plaquette constraint interaction e^{-i Omega C_l Z_a Z_b Z_c Z_d}
is realized (Fig. 1(b)) by:
   3 CNOTs (z-path) -> 1 Rz -> 3 CNOTs (reverse)
= 7 sequential gate operations per plaquette.

Key architectural fact (Fig. 1(e), text): the plaquettes tile the square
lattice, and because pairs of CNOTs used by adjacent plaquettes overlap on
shared qubits, the plaquettes cannot ALL be applied in one parallel batch.
Instead, they are grouped into 4 non-overlapping shift classes (original,
shift-row, shift-col, shift-row-and-col), each of which can be executed
in parallel:
   4 shift positions * 7 parallel operations per position = 28 parallel gates.

This depth is *independent of N*.

We verify this two ways:
  (a) Build the constraint layer symbolically as sets of gates per plaquette,
      then greedily 2-color into commuting parallel layers by qubit overlap
      and count layers.
  (b) Build the actual Qiskit circuit implementing the constraints for
      several N, transpile with basis {cx, rz, u} on an all-to-all coupling
      map, and measure circuit depth().

Compared to sequential (one plaquette at a time), depth = 7 * (K-N+1),
which GROWS as O(N^2). Parallel depth = 28 (constant).
"""
import json
import sys
from math import comb
from qiskit import QuantumCircuit, transpile


# ---- LHZ geometry -------------------------------------------------------

def lhz_qubits(N):
    """Return a dict mapping (i,j) with i<j to qubit index [0..K-1]
    and its (row, col) position on the LHZ triangular/square layout.

    Lechner's LHZ arrangement: physical qubit q_{ij} (i<j, both in [1..N])
    is placed at logical position (row=i, col=j-1) in an upper-triangular
    grid. There are N-1 rows and N-1 columns; plaquettes (l,n)(l,e)(l,s)(l,w)
    tile the interior with 4 physical qubits per plaquette:
        n=(i,   j+1), e=(i+1, j+1), s=(i+1, j), w=(i, j)  for a plaquette
    with 1<=i<=N-2, i<j<=N-2, using the (i,j) index convention.
    """
    idx = {}
    pos = {}
    q = 0
    for i in range(1, N):
        for j in range(i + 1, N + 1):
            idx[(i, j)] = q
            pos[q] = (i, j)   # logical (row=i, col=j)
            q += 1
    return idx, pos


def lhz_plaquettes(N):
    """Return list of 4-tuples of qubit indices for each LHZ plaquette.
    Per Lechner Fig. 1(a)/(d): plaquettes are indexed by (i, j) with
    1<=i<j-1<=N-1 (need j-i>=2 so both (i,j) and (i+1,j) exist as edges).
    Each plaquette groups the four LHZ qubits:
        w=(i, j-1),  n=(i, j),  s=(i+1, j),  e=(i+1, j-1)
        (west, north, south, east; the four edges sharing the plaquette).
    There are K - N + 1 such plaquettes with K = N(N-1)/2.
    """
    idx, _ = lhz_qubits(N)
    plaqs = []
    for i in range(1, N - 1):
        for j in range(i + 2, N + 1):
            try:
                w = idx[(i, j - 1)]
                n = idx[(i, j)]
                s = idx[(i + 1, j)]
                e = idx[(i + 1, j - 1)]
            except KeyError:
                continue
            plaqs.append((w, n, s, e))
    return plaqs


def z_path_cnots(plaq):
    """Return the ordered CNOTs (control, target) that Fig. 1(b) uses
    to route the ZZZZ interaction to a single Rz on the last qubit.
    Standard chain: CNOT(a,b), CNOT(b,c), CNOT(c,d) then Rz on d,
    then CNOTs in reverse. This is the 'z-shaped path' the paper draws.
    """
    a, b, c, d = plaq
    forward = [(a, b), (b, c), (c, d)]
    reverse = list(reversed(forward))
    return forward, reverse


# ---- Depth analysis (a): symbolic parallel-layer counting ---------------

def sequential_depth(N):
    """One plaquette at a time: 7 ops each * P plaquettes."""
    P = len(lhz_plaquettes(N))
    return 7 * P, P


def parallel_depth_symbolic(N):
    """Greedy layering: for each of the 7 slots (cnot1, cnot2, cnot3, rz,
    cnot3', cnot2', cnot1'), collect the gates from all plaquettes at that
    slot and greedily pack into parallel sub-layers so that gates in a
    sub-layer never share a qubit.

    The paper argues this yields 4 sub-layers per slot => 4*7 = 28 total.
    """
    plaqs = lhz_plaquettes(N)
    slots = [[], [], [], [], [], [], []]  # 7 slots
    for p in plaqs:
        fwd, rev = z_path_cnots(p)
        # slot 0..2: forward CNOTs
        for k, cx in enumerate(fwd):
            slots[k].append(("cx", cx[0], cx[1]))
        # slot 3: Rz on the tail qubit
        slots[3].append(("rz", p[3]))
        # slot 4..6: reverse CNOTs
        for k, cx in enumerate(rev):
            slots[4 + k].append(("cx", cx[0], cx[1]))

    total_layers = 0
    per_slot_layers = []
    for slot in slots:
        # Greedy graph-coloring: pack gates into layers with disjoint qubits.
        remaining = list(slot)
        layers_here = 0
        while remaining:
            layers_here += 1
            used = set()
            next_remaining = []
            for g in remaining:
                qs = set(g[1:])
                if used.isdisjoint(qs):
                    used.update(qs)
                else:
                    next_remaining.append(g)
            remaining = next_remaining
        per_slot_layers.append(layers_here)
        total_layers += layers_here
    return total_layers, per_slot_layers, len(plaqs)


# ---- Depth analysis (b): real Qiskit circuit --------------------------

def build_constraint_circuit_sequential(N, omega=0.3):
    """Apply each plaquette's e^{-i Omega Z^4} sequentially."""
    K = N * (N - 1) // 2
    qc = QuantumCircuit(K)
    for p in lhz_plaquettes(N):
        a, b, c, d = p
        qc.cx(a, b)
        qc.cx(b, c)
        qc.cx(c, d)
        qc.rz(2 * omega, d)
        qc.cx(c, d)
        qc.cx(b, c)
        qc.cx(a, b)
    return qc


def build_constraint_circuit_parallel(N, omega=0.3):
    """Same physical operations but grouped so that within each of the 4
    shift-classes of plaquettes, gates go into parallel barriers.
    We reorder plaquettes by (i+j) mod 2 shift class and interleave
    to minimize depth after transpilation."""
    K = N * (N - 1) // 2
    qc = QuantumCircuit(K)
    plaqs = lhz_plaquettes(N)
    # 4 shift classes based on plaquette (i,j) parities.
    classes = {(0, 0): [], (0, 1): [], (1, 0): [], (1, 1): []}
    idx, _ = lhz_qubits(N)
    for i in range(1, N - 1):
        for j in range(i + 2, N + 1):
            try:
                w = idx[(i, j - 1)]
                n = idx[(i, j)]
                s = idx[(i + 1, j)]
                e = idx[(i + 1, j - 1)]
            except KeyError:
                continue
            classes[(i % 2, j % 2)].append((w, n, s, e))

    for cls_key in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        cls = classes[cls_key]
        if not cls:
            continue
        # Slot 0-2: forward CNOTs
        for slot in range(3):
            for p in cls:
                a, b, c, d = p
                pairs = [(a, b), (b, c), (c, d)]
                qc.cx(*pairs[slot])
        # Slot 3: Rz
        for p in cls:
            qc.rz(2 * omega, p[3])
        # Slot 4-6: reverse CNOTs
        for slot in range(3):
            for p in cls:
                a, b, c, d = p
                pairs = [(c, d), (b, c), (a, b)]
                qc.cx(*pairs[slot])
    return qc


def qiskit_depths(N):
    K = N * (N - 1) // 2
    qc_seq = build_constraint_circuit_sequential(N)
    qc_par = build_constraint_circuit_parallel(N)
    # Transpile on all-to-all connectivity to canonical basis (does not
    # add SWAPs since we already used qubit indices that map 1-to-1).
    t_seq = transpile(qc_seq, basis_gates=["cx", "rz", "u"], optimization_level=0)
    t_par = transpile(qc_par, basis_gates=["cx", "rz", "u"], optimization_level=0)
    return {
        "N": N,
        "K": K,
        "num_plaquettes": len(lhz_plaquettes(N)),
        "sequential_gates": qc_seq.size(),
        "sequential_depth": t_seq.depth(),
        "parallel_gates":   qc_par.size(),
        "parallel_depth":   t_par.depth(),
    }


# ---- Main ---------------------------------------------------------------

if __name__ == "__main__":
    results = {"paper_claim_parallel_depth": 28, "N_range": [], "by_N": {}}
    print(f"{'N':>3} {'K':>4} {'#pl':>4} "
          f"{'seq(sym)':>10} {'par(sym)':>10} "
          f"{'seq(qk)':>9} {'par(qk)':>9} "
          f"{'ratio':>7}")
    for N in [4, 5, 6, 7, 8, 9, 10, 12, 15, 20]:
        seq_sym, P = sequential_depth(N)
        par_sym, per_slot, P2 = parallel_depth_symbolic(N)
        qk = qiskit_depths(N)
        ratio = qk["sequential_depth"] / qk["parallel_depth"] if qk["parallel_depth"] else 0
        row = {
            "N": N,
            "K": qk["K"],
            "num_plaquettes": P,
            "sequential_depth_symbolic": seq_sym,
            "parallel_depth_symbolic":  par_sym,
            "per_slot_layers":          per_slot,
            "qiskit_sequential_depth":  qk["sequential_depth"],
            "qiskit_parallel_depth":    qk["parallel_depth"],
            "qiskit_sequential_gates":  qk["sequential_gates"],
            "qiskit_parallel_gates":    qk["parallel_gates"],
            "depth_reduction_ratio":    ratio,
        }
        results["by_N"].append(row) if isinstance(results["by_N"], list) else None
        results["by_N"][str(N)] = row
        results["N_range"].append(N)
        print(f"{N:>3d} {qk['K']:>4d} {P:>4d} "
              f"{seq_sym:>10d} {par_sym:>10d} "
              f"{qk['sequential_depth']:>9d} {qk['parallel_depth']:>9d} "
              f"{ratio:>7.2f}")

    out = "../report/evidence/depth_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out}")
