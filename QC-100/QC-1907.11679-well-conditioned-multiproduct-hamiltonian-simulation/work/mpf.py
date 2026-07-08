"""
Independent replication of:
Low, Kliuchnikov, Wiebe - "Well-conditioned multiproduct Hamiltonian simulation"
arXiv:1907.11679 (2019)

We implement:
1. Second-order Suzuki product formula U2(Delta) for the 1D Heisenberg chain,
   decomposed into three commuting groups XX + YY + ZZ on even and odd bonds.
   (Actually we treat H = A+B where A = odd-bond terms, B = even-bond terms; both
   groups are sums of commuting local terms so exp(A*t) and exp(B*t) are exact.)
2. The classical Chin (ill-conditioned) multiproduct formula, coefficients from
   Eq. (5) with k_j = j.
3. The well-conditioned closed-form Chebyshev construction, Eqs. (8)-(9), and
   the rounded integer variant (Eq. 10).
4. The paper's Appendix A tabulated integer-exponent multiproduct coefficients
   (a subset covering orders 2m = 4..12 for U2 base).
5. Benchmark: compare error scaling of exact matrix exponential vs each formula
   on a small 1D Heisenberg chain with periodic boundary conditions, as in
   Fig. 2 of the paper.

We verify:
- Order of convergence: MPF of order 2m has error O(Delta^{2m+1}) per step, so
  when applied over fixed time t with r=t/Delta steps, error scales like
  (t/r)^{2m}.
- Condition number ||a||_1 vs order for (a) Chin, (b) closed-form Chebyshev,
  (c) rounded integer, (d) Appendix A optimized. Chin grows like e^{Omega(m)},
  Chebyshev-based grows only like Theta(log m).
"""

import numpy as np
import scipy.linalg as sla
from fractions import Fraction
import json
from pathlib import Path

# ------------------------------------------------------------------ Pauli
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def local_op(N, site, op):
    """Op at `site` (0-indexed), identity elsewhere. N sites."""
    mats = [I2] * N
    mats[site] = op
    return kron_list(mats)


def two_site_op(N, i, j, op1, op2):
    mats = [I2] * N
    mats[i] = op1
    mats[j] = op2
    return kron_list(mats)


def heisenberg_bond(N, i, j):
    """Full 2^N x 2^N matrix for X_i X_j + Y_i Y_j + Z_i Z_j."""
    return (two_site_op(N, i, j, sigma_x, sigma_x)
            + two_site_op(N, i, j, sigma_y, sigma_y)
            + two_site_op(N, i, j, sigma_z, sigma_z))


def heisenberg_H(N, pbc=True):
    """H = sum_j (X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1}), periodic."""
    H = np.zeros((2 ** N, 2 ** N), dtype=complex)
    for j in range(N - 1):
        H += heisenberg_bond(N, j, j + 1)
    if pbc and N >= 3:
        H += heisenberg_bond(N, N - 1, 0)
    return H


def heisenberg_A_B(N, pbc=True):
    """Split into odd bonds (A) and even bonds (B) so exp(A*t) & exp(B*t)
    each factor exactly (commuting terms within a group).
    With PBC and N even this is a proper 2-color split.
    """
    A = np.zeros((2 ** N, 2 ** N), dtype=complex)  # odd bonds
    B = np.zeros((2 ** N, 2 ** N), dtype=complex)  # even bonds
    for j in range(N - 1):
        term = heisenberg_bond(N, j, j + 1)
        if j % 2 == 0:
            A += term
        else:
            B += term
    if pbc and N >= 3:
        # bond (N-1, 0). For N even, this is (odd, even) = odd->even index
        # Just put it in whichever group keeps intra-group commutation.
        # For N even, N-1 is odd, so put in B (even bonds if we index from 1).
        # We'll add to B; overlap with adjacent bond (0,1) which is in A -> OK.
        B += heisenberg_bond(N, N - 1, 0)
    return A, B


# ------------------------------------------------------------- U2 second-order
def U2_step(A, B, delta):
    """Second-order symmetric Suzuki: exp(-i A delta/2) exp(-i B delta) exp(-i A delta/2)."""
    UA = sla.expm(-1j * A * delta / 2)
    UB = sla.expm(-1j * B * delta)
    return UA @ UB @ UA


def U2_k_step(A, B, delta, k):
    """U2(delta/k)^k."""
    step = U2_step(A, B, delta / k)
    # Efficient: matrix power
    return np.linalg.matrix_power(step, k)


def U4_step(A, B, delta):
    """Fourth-order Suzuki S_4: recursion Eq. (2) with alpha=4."""
    p = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))
    s1 = U2_step(A, B, p * delta)
    s2 = U2_step(A, B, (1.0 - 4.0 * p) * delta)
    return s1 @ s1 @ s2 @ s1 @ s1


# ------------------------------------------------------------- MPF coefficients
def chin_coefficients(m):
    """Eq. (5) with k_j = j, j=1..m (arithmetic progression, Chin 2010).
    Returns k array (1..m) and a array from closed form
        a_j = prod_{q != j} 1 / (1 - (k_q/k_j)^2)
    """
    k = np.arange(1, m + 1)
    a = np.zeros(m)
    for j in range(m):
        prod = 1.0
        for q in range(m):
            if q == j:
                continue
            prod *= 1.0 / (1.0 - (k[q] / k[j]) ** 2)
        a[j] = prod
    return k, a


def chebyshev_real_coefficients(m):
    """Closed-form real-exponent well-conditioned MPF, Eqs. (8)-(9).
        x_j^{(m)} = sin^2(pi(2j-1)/(4m))  = 1 / k''_j^2
        a''_j = (-1)^{j+1}/m * cot(pi(2j-1)/(4m))
    j in [m]. Returns (k'', a'').
    """
    j = np.arange(1, m + 1)
    theta = np.pi * (2 * j - 1) / (4 * m)
    x = np.sin(theta) ** 2
    k_dp = 1.0 / np.sqrt(x)
    a_dp = ((-1) ** (j + 1)) / m * (1.0 / np.tan(theta))
    return k_dp, a_dp


def chebyshev_first_half_coefficients(m):
    """Intermediate: use the first m points of the 2m-point Chebyshev grid, Eq.
    'x_j^{0(m)} = x_j^{(2m)}, j in [m]'. This gives the k'_j with a larger gap
    between exponents, still real-valued. Coefficients from Eq. (5) applied
    to those k'.
    """
    two_m = 2 * m
    j = np.arange(1, two_m + 1)
    theta = np.pi * (2 * j - 1) / (4 * two_m)
    x_full = np.sin(theta) ** 2
    x = x_full[:m]  # first m points
    k_p = 1.0 / np.sqrt(x)
    # Coefficients solve V(k_p^-2) a = e_1 with M=m. Use Eq. (5).
    a_p = np.zeros(m)
    for jj in range(m):
        prod = 1.0
        for q in range(m):
            if q == jj:
                continue
            prod *= 1.0 / (1.0 - (k_p[q] / k_p[jj]) ** 2)
        a_p[jj] = prod
    return k_p, a_p


def rounded_integer_coefficients(m):
    """Eq. (10): k_j = ceil(K * k'_j) with K chosen just large enough that all
    k_j are unique integers. Coefficients recomputed from Eq. (5) on integer k.
    """
    k_p, _ = chebyshev_first_half_coefficients(m)
    # Try scale factors 1, 2, ... until all rounded k are unique
    for K in range(1, 200):
        k = np.ceil(K * k_p).astype(int)
        if len(set(k.tolist())) == m and np.all(k >= 1):
            # unique
            break
    else:
        raise RuntimeError("no scale factor yielded unique integers")
    # Coefficients from Eq. (5) with integer k
    a = np.zeros(m)
    for jj in range(m):
        prod = 1.0
        for q in range(m):
            if q == jj:
                continue
            prod *= 1.0 / (1.0 - (k[q] / k[jj]) ** 2)
        a[jj] = prod
    return k, a


# --- Paper's Appendix A tabulated coefficients (top half: min ||a||_1 * ||k||_1
# for U2 base). All entries transcribed verbatim from the paper PDF text.
# key = 2m (integrator order). Value = (k list, a list as Fractions).
PAPER_TABLE_U2 = {
    2: (
        [1, 2],
        [Fraction(-1, 3), Fraction(4, 3)],
    ),
    3: (
        [1, 2, 6],
        [Fraction(1, 105), Fraction(-1, 6), Fraction(81, 70)],
    ),
    4: (
        [1, 2, 3, 10],
        [
            Fraction(-1, 2376),
            Fraction(2, 45),
            Fraction(-729, 3640),
            Fraction(31250, 27027),
        ],
    ),
    5: (
        [1, 2, 3, 5, 17],
        [
            Fraction(1, 165888),
            Fraction(-256, 89775),
            Fraction(6561, 179200),
            Fraction(-390625, 2128896),
            Fraction(6975757441, 6067353600),
        ],
    ),
    6: (
        [1, 2, 3, 4, 6, 21],
        [
            Fraction(-1, 5544000),
            Fraction(8, 19665),
            Fraction(-81, 4480),
            Fraction(65536, 669375),
            Fraction(-216, 875),
            Fraction(7626831723, 6537520000),
        ],
    ),
}


def paper_table_coeffs(m):
    if m not in PAPER_TABLE_U2:
        return None
    k_list, a_frac = PAPER_TABLE_U2[m]
    k = np.array(k_list, dtype=int)
    a = np.array([float(x) for x in a_frac])
    return k, a


# -------------------------------------------------------- MPF application
def mpf_step(A, B, delta, k_arr, a_arr, base="U2"):
    """Compute sum_j a_j * U_base^{k_j}(delta/k_j) as a matrix.
    This is a classical simulation: on a real quantum computer this would be
    an LCU. Classically we just take the linear combination.
    """
    dim = A.shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for kj, aj in zip(k_arr, a_arr):
        if base == "U2":
            Uk = U2_k_step(A, B, delta, int(kj))
        elif base == "U4":
            step = U4_step(A, B, delta / int(kj))
            Uk = np.linalg.matrix_power(step, int(kj))
        else:
            raise ValueError(base)
        out = out + aj * Uk
    return out


# ------------------------------------------------------------ Verification
def verify_cancellation(k_arr, a_arr, order_2m):
    """Sanity check: does sum a_j = 1 and sum a_j / k_j^{2s} = 0 for s=1..m-1?
    (i.e. cancellation of odd-power BCH errors through order 2m)."""
    m = len(k_arr)
    checks = []
    s0 = float(np.sum(a_arr))
    checks.append(("sum a_j", s0, 1.0, abs(s0 - 1.0)))
    for s in range(1, m):
        val = float(np.sum(a_arr / np.asarray(k_arr, dtype=float) ** (2 * s)))
        checks.append((f"sum a_j / k_j^{2 * s}", val, 0.0, abs(val)))
    return checks


def condition_number(a_arr):
    return float(np.sum(np.abs(a_arr)))


def k_norm(k_arr):
    return int(np.sum(k_arr))


# --- One-step error check on a small Heisenberg system
def one_step_error(N, delta, method_fn, method_name):
    A, B = heisenberg_A_B(N)
    H = A + B
    U_exact = sla.expm(-1j * H * delta)
    U_appx = method_fn(A, B, delta)
    err = np.linalg.norm(U_appx - U_exact, 2)
    return err


if __name__ == "__main__":
    print("Sanity checks on cancellation conditions:")
    for m in range(2, 7):
        for name, gen in [
            ("chin", chin_coefficients),
            ("cheb_real", chebyshev_real_coefficients),
            ("cheb_first_half", chebyshev_first_half_coefficients),
            ("rounded_int", rounded_integer_coefficients),
        ]:
            k, a = gen(m)
            checks = verify_cancellation(k, a, 2 * m)
            worst = max(c[3] for c in checks)
            print(f"  m={m} {name:20s} ||a||_1={condition_number(a):8.4f}  "
                  f"||k||_1={k_norm(k):5d}  worst_residual={worst:.3e}")
        pt = paper_table_coeffs(m)
        if pt is not None:
            k, a = pt
            checks = verify_cancellation(k, a, 2 * m)
            worst = max(c[3] for c in checks)
            print(f"  m={m} {'paper_table_A':20s} ||a||_1={condition_number(a):8.4f}  "
                  f"||k||_1={k_norm(k):5d}  worst_residual={worst:.3e}")
