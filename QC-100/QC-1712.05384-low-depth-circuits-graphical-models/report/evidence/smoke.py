"""Quick smoke test: for tiny circuits (n=2, 3), the tensor-network amplitude
must equal the statevector amplitude within 1e-10. If not, gate conventions
disagree between the two paths."""

from tn_sim import (
    make_random_shallow_circuit,
    statevector_amp_zero,
    build_tn_amp_zero,
    tn_contract_amp_zero,
)

for (ell, m, d, seed) in [(1, 2, 1, 0), (1, 2, 3, 1), (1, 3, 2, 2), (2, 2, 2, 3), (2, 3, 3, 4), (3, 3, 3, 5)]:
    gates, n = make_random_shallow_circuit(ell, m, d, seed=seed)
    sv = statevector_amp_zero(gates, n)
    tensors, idx = build_tn_amp_zero(gates, n)
    tn, info, path = tn_contract_amp_zero(tensors, idx)
    diff = abs(sv - tn)
    ok = "OK" if diff < 1e-10 else "MISMATCH"
    print(f"ell={ell} m={m} n={n} d={d}: sv={sv:.6f} tn={tn:.6f} diff={diff:.2e}  {ok}")
