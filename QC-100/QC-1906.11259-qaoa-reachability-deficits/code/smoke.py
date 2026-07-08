"""Smoke test: verify H_SAT construction + QAOA energy machinery."""
import numpy as np
from qaoa_reachability import (
    basis_bits, plus_state, apply_x_rotation_all,
    random_3sat_instance, hsat_diagonal, qaoa_energy, optimize_qaoa,
)
import random

n = 4
bits = basis_bits(n)
# Manual clause: x1 OR x2 OR x3   (positive literals on vars 0,1,2)
#   unsat only when x1=x2=x3=0 -> assignments 0000, 0001 (var3 free) i.e.
#   bits 000x: 8 assignments? No: only 2 (var 3 = 0 or 1). indices 0 and 1.
from qaoa_reachability import Clause
c = Clause(vars=(0, 1, 2), negs=(False, False, False))
diag = hsat_diagonal([c], n, bits)
unsat_idx = np.where(diag > 0)[0]
print("clause var0 OR var1 OR var2 (n=4). Unsat states =", unsat_idx.tolist())
# Expect: assignments where bits[:,0]=bits[:,1]=bits[:,2]=0 -> x=0000 and x=0001
# Using MSB=qubit 0 convention: state index 0 = 0000, state 1 = 0001 -> vars (0,1,2)=0, var3=0/1
assert set(unsat_idx.tolist()) == {0, 1}, "clause build broken"
print("H_SAT construction OK")

# Plus-state energy: uniform over 16 -> average diag = 2/16 = 0.125
psi = plus_state(n)
avg = float(np.sum(np.abs(psi)**2 * diag))
print(f"plus-state avg energy = {avg:.4f} (expect 0.1250)")
assert abs(avg - 0.125) < 1e-10

# Sum X mixer: exp(-i*pi/2 * X) = -i * X. Apply to |+> should give (-i)^n * |+>.
psi2 = apply_x_rotation_all(plus_state(n), np.pi/2, n)
overlap = np.vdot(plus_state(n), psi2)
print(f"|<+|exp(-i pi/2 X_all)|+>| = {abs(overlap):.6f} (expect 1)")
assert abs(abs(overlap) - 1.0) < 1e-8

# QAOA on very easy instance (satisfiable): min energy should be 0.
rng = random.Random(1)
inst = random_3sat_instance(6, 3, rng)   # only 3 clauses, very underconstrained
diag2 = hsat_diagonal(inst, 6, basis_bits(6))
print("min E =", diag2.min(), "n=6 m=3")
e, x = optimize_qaoa(diag2, 6, p=2, n_restarts=4, seed=42)
print(f"QAOA p=2 energy = {e:.4f}  min energy = {diag2.min()}  deficit f = {e - diag2.min():.4f}")

# Densely constrained instance -> min E > 0 typically
rng = random.Random(2)
inst2 = random_3sat_instance(6, 60, rng)  # alpha=10
diag3 = hsat_diagonal(inst2, 6, basis_bits(6))
print("min E dense =", diag3.min())
e, x = optimize_qaoa(diag3, 6, p=2, n_restarts=4, seed=42)
print(f"QAOA p=2 energy = {e:.4f}  min energy = {diag3.min()}  deficit f = {e - diag3.min():.4f}")
print("SMOKE OK")
