"""Broader smoke: check MULTIPLE seeds, and also check a different output
bitstring (not always |0...0>) since the H+CZ+T interference can hit 0 for
some circuits. Also check norm-preservation."""

import numpy as np
from tn_sim import (
    make_random_shallow_circuit,
    build_tn_amp_zero,
    tn_contract_amp_zero,
    SINGLE_GATES,
    CZ,
)

def statevector_full(gates, n):
    state = np.zeros(2 ** n, dtype=np.complex128)
    state[0] = 1.0
    def apply_single(state, U, q):
        shape = (2,) * n
        s = state.reshape(shape)
        s = np.tensordot(U, s, axes=([1], [q]))
        s = np.moveaxis(s, 0, q)
        return s.reshape(2 ** n)
    def apply_cz(state, q1, q2):
        shape = (2,) * n
        s = state.reshape(shape).copy()
        idx = [slice(None)] * n
        idx[q1] = 1; idx[q2] = 1
        s[tuple(idx)] *= -1.0
        return s.reshape(2 ** n)
    for g in gates:
        if g.kind == "CZ":
            state = apply_cz(state, g.qubits[0], g.qubits[1])
        else:
            state = apply_single(state, SINGLE_GATES[g.kind], g.qubits[0])
    return state

print("Config: (ell,m,n,d,seed) SV_amp0 TN_amp0 |diff| norm ")
for seed in range(6):
    for (ell, m, d) in [(1, 3, 2), (2, 2, 3), (2, 3, 3), (3, 3, 3)]:
        gates, n = make_random_shallow_circuit(ell, m, d, seed=seed)
        sv_full = statevector_full(gates, n)
        norm = float(np.vdot(sv_full, sv_full).real)
        sv0 = complex(sv_full[0])
        tensors, idx = build_tn_amp_zero(gates, n)
        tn0, info, path = tn_contract_amp_zero(tensors, idx)
        diff = abs(sv0 - tn0)
        ok = "OK" if diff < 1e-10 else "MISMATCH"
        print(f"({ell},{m},{n},{d},{seed}) sv0={sv0:+.4f} tn0={tn0:+.4f} |diff|={diff:.2e} norm={norm:.4f} {ok}")
