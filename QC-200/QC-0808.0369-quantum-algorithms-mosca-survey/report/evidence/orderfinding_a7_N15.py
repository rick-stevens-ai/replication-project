"""
Order-finding subroutine — reproduces the QFT-peak-at-multiples-of-1/r
claim that Mosca surveys in Section 4 (Factoring, Discrete Logs, Abelian HSP).

Setup: N = 15, a = 7. Classical order r = ord_{15}(7) = 4  (7,49=4,28=13,91=1).
Standard Shor circuit: m counting qubits, n = ceil(log2(N)) = 4 work qubits.
We use m = 8 counting qubits, apply H^m, then modular-exponentiation via
diagonal action on eigenstates (we implement it as the full permutation
|x>|y> -> |x>|y * a^x mod N> for y in the range [0..N-1]; y>=N is left fixed).
Then QFT^dagger on the counting register and inspect the probability distribution.

Expected: sharp peaks at k * 2^m / r for k = 0, 1, ..., r-1
         i.e. k = 0, 64, 128, 192 when m=8, r=4.
Real Qiskit statevector, no shots, no noise.
"""
import json, math, sys
from fractions import Fraction
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit.quantum_info import Statevector, Operator

N = 15
a = 7
n_work = math.ceil(math.log2(N))  # 4 qubits to hold values 0..15
m = 8  # counting register precision

# Sanity: classical order of a mod N
r_classical = None
x = 1 % N
for i in range(1, N + 1):
    x = (x * a) % N
    if x == 1:
        r_classical = i
        break
print(f"Classical order r of a={a} mod N={N} is r={r_classical}")
assert r_classical == 4

# Build controlled-U^{2^j} for j=0..m-1 where U|y> = |a*y mod N>, y=0..2^n_work-1,
# extended to the identity for y>=N.
dim_work = 2 ** n_work
# Precompute a^(2^j) mod N for each counting bit
powers = [pow(a, 2 ** j, N) for j in range(m)]
print(f"a^(2^j) mod N for j=0..{m-1}: {powers}")


def perm_unitary(mult: int) -> np.ndarray:
    """Return the 2^n_work x 2^n_work permutation matrix implementing
    |y> -> |y*mult mod N> for y in [0..N-1], identity for y in [N..2^n_work-1]."""
    U = np.zeros((dim_work, dim_work), dtype=complex)
    for y in range(dim_work):
        if y < N:
            yprime = (y * mult) % N
        else:
            yprime = y
        U[yprime, y] = 1.0
    return U


qc = QuantumCircuit(m + n_work)

# 1) Superposition on counting register
for q in range(m):
    qc.h(q)

# 2) Initialize work register to |1>  (qubit indices m..m+n_work-1, LSB first)
qc.x(m)  # sets qubit m -> |1>, others stay |0> -> value 1

# 3) Controlled-U^{2^j}
for j in range(m):
    Uj = perm_unitary(powers[j])
    gate = UnitaryGate(Uj, label=f"U^{2**j}").control(1)
    qc.append(gate, [j] + list(range(m, m + n_work)))

# 4) Inverse QFT on counting register (Qiskit QFT is on qubits 0..m-1)
qc.append(QFT(num_qubits=m, do_swaps=True, inverse=True), range(m))

# 5) Statevector -> marginal over counting register
sv = Statevector.from_instruction(qc)
probs_full = np.abs(sv.data) ** 2
counts = np.zeros(2 ** m)
for idx, p in enumerate(probs_full):
    # counting register = low m bits (Qiskit little-endian)
    k = idx & ((1 << m) - 1)
    counts[k] += p

# Find peaks
top = np.argsort(counts)[::-1][:8]
print(f"\nTop counting-register outcomes (m={m}, total={2**m}):")
for idx in top:
    print(f"  k={idx}  P={counts[idx]:.6f}   k/2^m = {idx/2**m:.6f}   ~ {Fraction(int(idx), 2**m).limit_denominator(N)}")

expected_peaks = [k * (2 ** m) // r_classical for k in range(r_classical)]
print(f"\nExpected peak positions (k*2^m/r) for r={r_classical}: {expected_peaks}")

# Verify: sum of the 4 expected peaks should be ~1
p_expected = float(sum(counts[k] for k in expected_peaks))
print(f"Sum of prob at expected peaks: {p_expected:.6f}")

# Peaks should each be near 1/r = 0.25
peak_probs = [float(counts[k]) for k in expected_peaks]
print(f"Peak probs: {peak_probs} (target ~ {1/r_classical})")

# Continued-fraction recovery: for each observed k, k/2^m ~ s/r
def recover_r(k, m_bits, N):
    if k == 0:
        return None
    frac = Fraction(int(k), 2 ** m_bits).limit_denominator(N)
    return frac.denominator

recovered = sorted(set(recover_r(k, m, N) for k in top if recover_r(k, m, N)))
print(f"Recovered candidate orders (denominators of continued-fraction rounds): {recovered}")

match_peaks = all(counts[k] > 0.2 for k in expected_peaks) and (0.99 <= p_expected <= 1.001)
match_r = r_classical in recovered
overall_match = match_peaks and match_r

out = {
    "algorithm": "Shor order-finding subroutine",
    "N": N,
    "a": a,
    "r_classical": r_classical,
    "m_counting_qubits": m,
    "n_work_qubits": n_work,
    "expected_peak_positions_k": expected_peaks,
    "peak_probabilities": peak_probs,
    "sum_peak_probabilities": p_expected,
    "peak_target_each": 1.0 / r_classical,
    "top_8_outcomes": [{"k": int(k), "p": float(counts[k]), "k_over_2m": k / 2 ** m} for k in top],
    "recovered_order_candidates": recovered,
    "match_peaks": bool(match_peaks),
    "match_recovered_r": bool(match_r),
    "match_overall": bool(overall_match),
    "qiskit_version": __import__("qiskit").__version__,
    "circuit_depth": qc.depth(),
}
with open("orderfinding_a7_N15_result.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\nOverall MATCH: {overall_match}")
print("Wrote orderfinding_a7_N15_result.json")
sys.exit(0 if overall_match else 1)
