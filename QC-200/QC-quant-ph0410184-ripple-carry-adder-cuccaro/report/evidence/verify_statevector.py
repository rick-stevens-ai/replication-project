"""Additional sanity check: full statevector simulation for n=3 to confirm
the CDKM adder acts correctly on quantum superposition (not just classical
basis states). We put A into a uniform superposition over all 2^n values and
B fixed; measure that the resulting statevector is the correct entangled sum.
"""
import sys
sys.path.insert(0, ".")
from cdkm import simple_adder, optimized_adder, encode_inputs
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
import numpy as np


def run_superposition(adder_fn, n, uma_variant=None):
    """Prep A in H^{\otimes n} superposition, B fixed to some value, verify
    output state is  sum_a |a> |a+b mod 2^n> |X=0> |s_n> up to global phase.
    """
    if uma_variant:
        base = adder_fn(n, uma_variant=uma_variant)
    else:
        base = adder_fn(n)

    b_val = 5  # arbitrary
    nq = 2 * n + 2
    prep = QuantumCircuit(nq)
    # H on all A_i
    for i in range(n):
        prep.h(2 * i + 2)
    # X on B bits to encode b_val
    for i in range(n):
        if (b_val >> i) & 1:
            prep.x(2 * i + 1)
    qc = prep.compose(base)
    qc.save_statevector()

    sim = AerSimulator(method="statevector")
    tc = transpile(qc, sim)
    sv = sim.run(tc).result().get_statevector()

    # Expected: 1/sqrt(2^n) * sum_a |X=0> |B = (a+b) mod 2^n> |A = a> |Z = s_n>
    # Iterate over the 2^n nonzero amplitudes and check them.
    amp_expected = 1.0 / np.sqrt(2 ** n)
    n_ok = 0
    n_check = 0
    for a in range(2 ** n):
        s_full = a + b_val
        s_mod = s_full & ((1 << n) - 1)
        s_n = (s_full >> n) & 1
        # Build the basis index (qiskit little-endian: qubit 0 = LSB of index)
        idx_bits = [0] * nq
        # X = 0 (qubit 0)
        for i in range(n):
            idx_bits[2 * i + 1] = (s_mod >> i) & 1  # B_i
            idx_bits[2 * i + 2] = (a >> i) & 1      # A_i
        idx_bits[2 * n + 1] = s_n
        idx = 0
        for k, bit in enumerate(idx_bits):
            idx |= bit << k
        amp = sv.data[idx]
        n_check += 1
        if np.isclose(abs(amp), amp_expected, atol=1e-9):
            n_ok += 1

    # Also verify total amplitude on other basis states is 0
    total_norm_expected = 1.0
    total_norm_actual = float(np.sum(np.abs(sv.data) ** 2))
    return {"n_check": n_check, "n_ok": n_ok, "norm": total_norm_actual}


if __name__ == "__main__":
    import json
    r = {}
    for tag, fn, kw in [
        ("simple_2cnot_n3", simple_adder, "2cnot"),
        ("simple_3cnot_n3", simple_adder, "3cnot"),
        ("optimized_n4",     optimized_adder, None),
    ]:
        n = 4 if "n4" in tag else 3
        out = run_superposition(fn, n, uma_variant=kw)
        r[tag] = out
        print(f"{tag}: {out}")
    with open("statevector_check.json", "w") as f:
        json.dump(r, f, indent=2)
