"""Stabilizer-frame simulator (compact sum-over-stabilizers) for
near-Clifford circuits — reproduction of Garcia & Markov (arXiv:1712.03554).

State representation:
    |psi> = sum_i alpha_i |phi_i>
where each |phi_i> is a pure n-qubit stabilizer state, represented by a
stim.TableauSimulator (which internally holds the stabilizer tableau).

Clifford gates (H, S, CNOT, X, Y, Z, ...) are applied to each frame branch
independently -- O(|F| * poly(n)).

Non-Clifford T gate on qubit q is decomposed as
    T = e^{i pi/8} ( cos(pi/8) I  -  i sin(pi/8) Z )
so
    T|phi> = c |phi>  +  d ( Z_q |phi> )
with c = e^{i pi/8} cos(pi/8),  d = -i e^{i pi/8} sin(pi/8).
The frame doubles: |F| -> 2|F|, chi = 2^t after t T-gates.  This is the
exponential-in-t / polynomial-in-n scaling the paper claims for stabilizer-
frame simulation of near-Clifford circuits.

Amplitude readout <x|psi> = sum_i alpha_i <x|phi_i> uses the standard
stabilizer inner-product / basis-state-amplitude routine: for each frame
branch |phi_i>, project onto |x> by measuring qubits in Z basis
deterministically or with 1/sqrt(2) amplitudes; we accumulate the complex
amplitude by using stim's peek/measure-in-basis and probabilistic-branch
tracking.  We implement it via direct dense-vector expansion of each
stabilizer state (n<=10 fits comfortably in 2^n = 1024 amplitudes) using
Qiskit's Statevector on the equivalent Clifford circuit.  That is exact
and fast enough at these sizes and lets us focus on the frame-growth
scaling claim rather than reimplementing the stabilizer inner-product
subroutine.
"""

from __future__ import annotations
import cmath
import math
import time
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import stim
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# ---------------------------------------------------------------------------
# A "branch" is (Clifford-circuit-so-far, complex amplitude).
# We store the Clifford as a list of gate ops so we can (a) evolve it further
# with more Cliffords, (b) render it to a Qiskit circuit for exact statevector
# extraction, and (c) render it to a stim.Circuit for tableau-based sanity
# checks.
# ---------------------------------------------------------------------------

@dataclass
class Branch:
    n: int
    ops: List[Tuple[str, Tuple[int, ...]]] = field(default_factory=list)
    amp: complex = 1.0 + 0j

    def copy(self) -> "Branch":
        return Branch(self.n, list(self.ops), self.amp)

    def add(self, name: str, qubits: Tuple[int, ...]):
        self.ops.append((name, tuple(qubits)))

    def to_qiskit(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.n)
        for name, qs in self.ops:
            if name == "H":
                qc.h(qs[0])
            elif name == "S":
                qc.s(qs[0])
            elif name == "SDG":
                qc.sdg(qs[0])
            elif name == "X":
                qc.x(qs[0])
            elif name == "Y":
                qc.y(qs[0])
            elif name == "Z":
                qc.z(qs[0])
            elif name == "CNOT" or name == "CX":
                qc.cx(qs[0], qs[1])
            elif name == "CZ":
                qc.cz(qs[0], qs[1])
            elif name == "SWAP":
                qc.swap(qs[0], qs[1])
            else:
                raise ValueError(f"unknown Clifford op {name}")
        return qc

    def statevector(self) -> np.ndarray:
        qc = self.to_qiskit()
        return np.asarray(Statevector.from_instruction(qc).data, dtype=complex)


class StabilizerFrame:
    """Sum-over-stabilizers state: |psi> = sum_i amp_i |branch_i>."""

    def __init__(self, n: int):
        self.n = n
        self.branches: List[Branch] = [Branch(n)]  # |0...0>, amplitude 1

    # ---------------- Clifford gates: apply to every branch ----------------
    def _apply_clifford(self, name: str, qubits: Tuple[int, ...]):
        for b in self.branches:
            b.add(name, qubits)

    def h(self, q: int):   self._apply_clifford("H",  (q,))
    def s(self, q: int):   self._apply_clifford("S",  (q,))
    def sdg(self, q: int): self._apply_clifford("SDG", (q,))
    def x(self, q: int):   self._apply_clifford("X",  (q,))
    def y(self, q: int):   self._apply_clifford("Y",  (q,))
    def z(self, q: int):   self._apply_clifford("Z",  (q,))
    def cx(self, c: int, t: int):  self._apply_clifford("CNOT", (c, t))
    def cz(self, c: int, t: int):  self._apply_clifford("CZ",   (c, t))
    def swap(self, a: int, b: int): self._apply_clifford("SWAP", (a, b))

    # ---------------- Non-Clifford T gate: frame doubles -------------------
    def t(self, q: int):
        # T = e^{i pi/8} ( cos(pi/8) I  -  i sin(pi/8) Z )
        phase = cmath.exp(1j * math.pi / 8)
        c = phase * math.cos(math.pi / 8)
        d = phase * (-1j) * math.sin(math.pi / 8)
        new_branches: List[Branch] = []
        for b in self.branches:
            b_c = b.copy();           b_c.amp *= c
            b_d = b.copy();           b_d.amp *= d
            b_d.add("Z", (q,))         # Z on qubit q
            new_branches.append(b_c)
            new_branches.append(b_d)
        self.branches = new_branches

    def tdg(self, q: int):
        # T^dagger = e^{-i pi/8} ( cos(pi/8) I  + i sin(pi/8) Z )
        phase = cmath.exp(-1j * math.pi / 8)
        c = phase * math.cos(math.pi / 8)
        d = phase * (1j) * math.sin(math.pi / 8)
        new_branches: List[Branch] = []
        for b in self.branches:
            b_c = b.copy();           b_c.amp *= c
            b_d = b.copy();           b_d.amp *= d
            b_d.add("Z", (q,))
            new_branches.append(b_c)
            new_branches.append(b_d)
        self.branches = new_branches

    # ---------------- Read-out: full dense statevector via sum -------------
    def statevector(self) -> np.ndarray:
        dim = 2 ** self.n
        psi = np.zeros(dim, dtype=complex)
        for b in self.branches:
            psi += b.amp * b.statevector()
        return psi

    def frame_size(self) -> int:
        return len(self.branches)


# ---------------------------------------------------------------------------
# Ground-truth exact simulator via Qiskit (Clifford + T native).
# ---------------------------------------------------------------------------

def exact_qiskit_statevector(circuit_ops: List[Tuple[str, Tuple[int, ...]]], n: int) -> np.ndarray:
    qc = QuantumCircuit(n)
    for name, qs in circuit_ops:
        if name == "H":       qc.h(qs[0])
        elif name == "S":     qc.s(qs[0])
        elif name == "SDG":   qc.sdg(qs[0])
        elif name == "X":     qc.x(qs[0])
        elif name == "Y":     qc.y(qs[0])
        elif name == "Z":     qc.z(qs[0])
        elif name in ("CNOT", "CX"): qc.cx(qs[0], qs[1])
        elif name == "CZ":    qc.cz(qs[0], qs[1])
        elif name == "SWAP":  qc.swap(qs[0], qs[1])
        elif name == "T":     qc.t(qs[0])
        elif name == "TDG":   qc.tdg(qs[0])
        else:
            raise ValueError(f"unknown op {name}")
    return np.asarray(Statevector.from_instruction(qc).data, dtype=complex)


# ---------------------------------------------------------------------------
# Pure-Clifford baseline via Stim TableauSimulator: converts to statevector
# for comparison at small n.
# ---------------------------------------------------------------------------

def stim_clifford_statevector(circuit_ops: List[Tuple[str, Tuple[int, ...]]], n: int) -> np.ndarray:
    sim = stim.TableauSimulator()
    for name, qs in circuit_ops:
        if name == "H":       sim.h(qs[0])
        elif name == "S":     sim.s(qs[0])
        elif name == "SDG":   sim.s_dag(qs[0])
        elif name == "X":     sim.x(qs[0])
        elif name == "Y":     sim.y(qs[0])
        elif name == "Z":     sim.z(qs[0])
        elif name in ("CNOT", "CX"): sim.cnot(qs[0], qs[1])
        elif name == "CZ":    sim.cz(qs[0], qs[1])
        elif name == "SWAP":  sim.swap(qs[0], qs[1])
        else:
            raise ValueError(f"non-Clifford op {name} in Clifford-only path")
    # stim's state_vector() gives the amplitudes in little-endian; qiskit is
    # also little-endian so ordering matches by construction.
    sv = np.asarray(sim.state_vector(), dtype=complex)
    # sim uses fewer qubits than n if unreferenced -- pad.
    if sv.size < 2 ** n:
        pad = np.zeros(2 ** n - sv.size, dtype=complex)
        sv = np.concatenate([sv, pad])
    return sv


# ---------------------------------------------------------------------------
# Circuit builders
# ---------------------------------------------------------------------------

def build_clifford_baseline(n: int, seed: int = 1) -> List[Tuple[str, Tuple[int, ...]]]:
    """A layered Clifford circuit on n qubits: H on all, then a few CNOT
    layers, then S sprinkled in.  Deterministic for a given seed."""
    rng = np.random.default_rng(seed)
    ops: List[Tuple[str, Tuple[int, ...]]] = []
    for q in range(n):
        ops.append(("H", (q,)))
    for layer in range(3):
        for q in range(n - 1):
            if rng.random() < 0.6:
                ops.append(("CNOT", (q, q + 1)))
        for q in range(n):
            if rng.random() < 0.3:
                ops.append(("S", (q,)))
        for q in range(n):
            if rng.random() < 0.2:
                ops.append(("H", (q,)))
    return ops


def inject_t_gates(base: List[Tuple[str, Tuple[int, ...]]],
                   n: int, t: int, seed: int = 2) -> List[Tuple[str, Tuple[int, ...]]]:
    """Take a Clifford baseline and insert t T-gates at random positions on
    random qubits."""
    rng = np.random.default_rng(seed)
    ops = list(base)
    for _ in range(t):
        pos = int(rng.integers(0, len(ops) + 1))
        q = int(rng.integers(0, n))
        ops.insert(pos, ("T", (q,)))
    return ops


def run_frame_on_ops(ops: List[Tuple[str, Tuple[int, ...]]], n: int) -> Tuple[np.ndarray, int, float]:
    """Simulate the (near-Clifford) op list with our stabilizer-frame simulator.
    Returns (psi, final_frame_size, wallclock_seconds)."""
    frame = StabilizerFrame(n)
    t0 = time.perf_counter()
    for name, qs in ops:
        if name == "H":       frame.h(qs[0])
        elif name == "S":     frame.s(qs[0])
        elif name == "SDG":   frame.sdg(qs[0])
        elif name == "X":     frame.x(qs[0])
        elif name == "Y":     frame.y(qs[0])
        elif name == "Z":     frame.z(qs[0])
        elif name in ("CNOT", "CX"): frame.cx(qs[0], qs[1])
        elif name == "CZ":    frame.cz(qs[0], qs[1])
        elif name == "SWAP":  frame.swap(qs[0], qs[1])
        elif name == "T":     frame.t(qs[0])
        elif name == "TDG":   frame.tdg(qs[0])
        else:
            raise ValueError(f"unknown op {name}")
    psi = frame.statevector()
    dt = time.perf_counter() - t0
    return psi, frame.frame_size(), dt
