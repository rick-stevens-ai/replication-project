#!/usr/bin/env python3
"""Diagnose bit ordering and phase distribution."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shor_replicate import (
    build_shor_semiclassical, counts_to_probs, theoretical_distribution,
    sso, run_experiment, multiplicative_order
)
import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator

# N=15 a=2, r=4, Q=8. Expected ideal peaks at s in {0, 2, 4, 6}.
qc, n_q = build_shor_semiclassical(15, 2, 3)
sim = AerSimulator(seed_simulator=42)
tqc = transpile(qc, sim, basis_gates=["u1","u2","u3","rz","sx","x","h","p","cx","cz"], optimization_level=1)
res = sim.run(tqc, shots=10000).result()
counts = res.get_counts()
print("Raw counts (Qiskit ordering, keys are c[n-1]...c[0]):")
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}")

print("\nphase s counts (using MSB-first = c[0] first-measured):")
probs_msb = counts_to_probs(counts, 3)
for s, p in enumerate(probs_msb):
    print(f"  s={s}: p={p:.4f}")

# Try both orderings
print("\nphase s counts (LSB-first = c[0] is LSB):")
probs_lsb = np.zeros(8)
for bitstr, cnt in counts.items():
    b = bitstr.replace(" ", "")
    # c[i] = bit at position -1-i. LSB-first means c[0] contributes 2^0
    s = 0
    for i in range(3):
        bit = int(b[-1 - i])
        s += bit * (2 ** i)
    probs_lsb[s] += cnt
probs_lsb /= probs_lsb.sum()
for s, p in enumerate(probs_lsb):
    print(f"  s={s}: p={p:.4f}")

print("\nTheoretical for r=4, Q=8 (should peak at s in {0,2,4,6}):")
th4 = theoretical_distribution(4, 3)
for s, p in enumerate(th4):
    print(f"  s={s}: p={p:.4f}")

print("\nTheoretical for r=2, Q=8:")
th2 = theoretical_distribution(2, 3)
for s, p in enumerate(th2):
    print(f"  s={s}: p={p:.4f}")

print("\nSSO(measured_MSB, r=4):", sso(probs_msb, th4))
print("SSO(measured_LSB, r=4):", sso(probs_lsb, th4))
