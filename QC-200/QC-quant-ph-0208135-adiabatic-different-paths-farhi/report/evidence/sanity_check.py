"""Sanity check: build H_P, H_B for small n and verify structure."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from adiabatic_paths import build_HP, build_HB, build_HE, A_FARHI
import numpy as np

for n in (3, 4, 5):
    HP = build_HP(n)
    HB = build_HB(n)
    HE = build_HE(n, A_FARHI)
    dim = 2 ** n
    print(f"\n=== n={n}, dim={dim} ===")

    # HP diagonal
    diag = np.diag(HP).real
    print(f"HP diag: min={diag.min()}, max={diag.max()}, ground state index={int(np.argmin(diag))}")
    # Expect: minimum at index 0 (|00...0>)
    assert np.argmin(diag) == 0, f"HP min should be at |00..0>, got {np.argmin(diag)}"
    # Also expect |11..1> corresponds to some non-minimum value
    ones_idx = dim - 1
    print(f"HP[|00..0>]={diag[0]:.1f}  HP[|11..1>]={diag[ones_idx]:.1f}")

    # Hermiticity
    assert np.allclose(HP, HP.conj().T)
    assert np.allclose(HB, HB.conj().T)
    assert np.allclose(HE, HE.conj().T), "HE not Hermitian!"

    # HB ground state should be uniform superposition at eigenvalue 0
    wB, vB = np.linalg.eigh(HB)
    print(f"HB spectrum: {wB[:3]} ... {wB[-1]:.3f}")
    print(f"HB ground state overlap with uniform |+>^n: {abs(vB[:,0] @ np.ones(dim)/np.sqrt(dim)):.6f}")

    # Symmetric spectrum check: HP should preserve total spin (Sz sector), so
    # eigenvalues should cluster by Hamming weight.
    from collections import defaultdict
    by_hw = defaultdict(list)
    for i in range(dim):
        hw = bin(i).count("1")
        by_hw[hw].append(diag[i])
    for hw in sorted(by_hw):
        vals = by_hw[hw]
        # All states with same Hamming weight should have same HP value (by symmetry)
        if len(set(vals)) > 1:
            print(f"  hw={hw}: values NOT identical: min={min(vals)}, max={max(vals)}  (would break symmetry ansatz!)")
        else:
            print(f"  hw={hw}: HP value={vals[0]:.1f}  ({len(vals)} states)")
    print(f"HE Frobenius norm={np.linalg.norm(HE):.3f}")
