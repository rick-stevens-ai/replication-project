"""
Symmetric-subspace (dim = n+1) diagonalization for the paper's problem.

By the paper's arg (sec 3), H_B, H_P, and H_E (P2 with the specific A_FARHI)
all preserve total-spin j = n/2 sector. We work in the basis |j, m> for
m = -j, ..., +j (dimension n+1). Then everything is a matrix polynomial in
S_x, S_y, S_z with well-known matrix elements.

Verified: matches full 2^n exact-diag values for small n (see cross_check.py).

This lets us push n up to n = 100+ trivially, testing asymptotic scaling of
g_min^linear vs g_min^Farhi-A that the paper argues qualitatively.
"""
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def spin_ops(j):
    """Return (Sx, Sy, Sz, Sp, Sm) as (2j+1)x(2j+1) matrices in the |j,m> basis,
    m from -j (index 0) to +j (index 2j)."""
    dim = int(2 * j + 1)
    m_vals = np.arange(-j, j + 1)
    Sz = np.diag(m_vals).astype(complex)
    Sp = np.zeros((dim, dim), dtype=complex)  # S+ |j,m> = sqrt(j(j+1)-m(m+1)) |j,m+1>
    Sm = np.zeros((dim, dim), dtype=complex)
    for i, m in enumerate(m_vals):
        if i + 1 < dim:
            Sp[i + 1, i] = np.sqrt(j * (j + 1) - m * (m + 1))
        if i - 1 >= 0:
            Sm[i - 1, i] = np.sqrt(j * (j + 1) - m * (m - 1))
    Sx = 0.5 * (Sp + Sm)
    Sy = 0.5j * (Sm - Sp)  # NOTE sign convention
    return Sx, Sy, Sz, Sp, Sm


def build_HP_sym(n):
    """H_P in symmetric subspace using eq (15) of the paper.
    HP = (3n/2)*(n/2 - Sz)*(n/2 + Sz)(n/2 + Sz - 1)
       + (1/2)*(n/2 + Sz)*(n/2 - Sz)*(n/2 - Sz - 1)
       + (1/6)*(n/2 - Sz)*(n/2 - Sz - 1)*(n/2 - Sz - 2)   [from eq 15]

    Wait -- reading eq (15) more carefully:
       H_P = 3n * (n/2 - Sz)(n/2 + Sz)(n/2 + Sz - 1) * (1/(2*2*2)?)   no

    Let's just re-derive: h_3(z,z',z'') summed over i<j<k, where z takes values
    in {0,1}.  z_i = (1 - sigma_z_i)/2 in the +1/-1 convention (z=0 -> spin up).

    n_up = # of bits with z=0 = (n + 2 Sz) / 2 (in spin-1/2 convention)? Let's
    check: if S_z = sum_i sigma_z_i / 2, and z=0 -> sigma_z=+1, z=1 -> sigma_z=-1,
    then # of z=0 bits = n/2 + Sz.

    Then for a triple (i,j,k), let u = # bits with z=0 among the three (u = 0,1,2,3).
    Then sum = 3 - u, so h_3 = { u=3: 0, u=2: 3, u=1: 1, u=0: 1 }.

    But h_3 depends only on the sum, not the specific bits.  So
      sum_{i<j<k} h_3 = (# triples with u=3)*0 + (# triples with u=2)*3
                     + (# triples with u=1)*1 + (# triples with u=0)*1.

    Let N0 = n/2 + Sz = # z=0 bits (operator).  N1 = n - N0 = n/2 - Sz.
      # triples with u=3 = C(N0, 3)
      # triples with u=2 = C(N0, 2) * N1
      # triples with u=1 = N0 * C(N1, 2)
      # triples with u=0 = C(N1, 3)

    So HP = 3 * C(N0, 2) * N1  + N0 * C(N1, 2) + C(N1, 3)
          = 3 * (N0(N0-1)/2) * N1 + N0 * (N1(N1-1)/2) + N1(N1-1)(N1-2)/6.
    """
    j = n / 2
    Sx, Sy, Sz, _, _ = spin_ops(j)
    N0 = (n / 2) * np.eye(int(2 * j + 1)) + Sz
    N1 = (n / 2) * np.eye(int(2 * j + 1)) - Sz
    # Everything commutes here (all functions of Sz), so we can just build diag.
    n0 = np.diag(N0).real
    n1 = np.diag(N1).real
    diag = 3 * (n0 * (n0 - 1) / 2) * n1 + n0 * (n1 * (n1 - 1) / 2) + n1 * (n1 - 1) * (n1 - 2) / 6
    return np.diag(diag).astype(complex)


def build_HB_sym(n):
    """HB = C(n-1,2) * (n/2)(1 - 2 Sx / n)   [from eq 17: HB = (n-1)/2 * (n/2 - Sx)]

    Wait eq 17 says HB = C(n-1,2)*... no it says HB = ((n-1) choose 2) * ...
    Let me re-check with eq 17 in the paper: "HB = ((n-1 choose 2)) * (n/2 - Sx)".
    Actually the paper writes:  HB = (n-1 choose 2) * (n/2 - Sx).
    But wait the paper actually wrote (from the PDF text):
       HB = ((n-1)/2) * (n/2 - Sx)  ??? Let me re-look... it wrote
        H_B = ( (n-1)   * (n/2 - Sx) ) / 2   with the "n-1 over 2" style.
    Actually from the PDF: "HB = (n − 1)/2 * (n/2 − Sx)" -- ambiguous formatting.

    From (8): HB = sum_C HB,C, and each bit q is in C(n-1, 2) clauses.
    HB,C for one clause = sum_{q in C} (1 - sx_q)/2 = 3/2 - sx_i/2 - sx_j/2 - sx_k/2.
    Summing over all C(n,3) clauses:
      HB = C(n,3) * 3/2 - (1/2) * sum_q sx_q * C(n-1, 2)
         = (3/2) * n(n-1)(n-2)/6 - (1/2) * (2 Sx) * (n-1)(n-2)/2
         = n(n-1)(n-2)/4 - Sx * (n-1)(n-2)/2
         = (n-1)(n-2)/2 * (n/2 - Sx).

    So HB = C(n-1, 2) * (n/2 - Sx).  Consistent with paper's (17)
    (which the PDF-to-text mangled as "(n−1)/2" but should be the binomial).
    """
    from math import comb
    j = n / 2
    Sx, Sy, Sz, _, _ = spin_ops(j)
    dim = int(2 * j + 1)
    return comb(n - 1, 2) * (j * np.eye(dim) - Sx)


def build_HE_sym_farhi(n):
    """H_E from Farhi's specific A in eq (28), yielding (paper eq 29 in large-n):
        H_E = -2n (Sx Sz + Sz Sx) + O(n^2)  ??? Paper says (29): HE = -2n(SxSz+SzSx)+O(n^2).
    But that's only the leading term. For faithful small-n test we need the full
    HE. That requires re-doing the P2 sum in the symmetric subspace.

    Easiest: build HE from the full 2^n and project. But that's expensive.
    Alternative: use the fact that HE = sum_{i<j<k} A_{ijk} with A a fixed 8x8,
    and expand A in Pauli basis on 3 qubits. Since HE preserves total spin
    (because A is applied identically to every triple), HE_sym is a polynomial
    in Sx, Sy, Sz.

    For the paper's asymptotic argument (eq 30), only Sx Sz + Sz Sx enters at
    O(n^2). At small n the sub-leading terms matter but the qualitative behavior
    should hold.

    We provide TWO versions:
        (i) Leading-order: HE = -2n (Sx Sz + Sz Sx)  -- matches paper's asymptotic
        (ii) Full: compute from Pauli decomposition of A_FARHI (deferred).
    Use (i) for large-n scaling; use full 2^n for small-n validation.
    """
    j = n / 2
    Sx, Sy, Sz, _, _ = spin_ops(j)
    return -2 * n * (Sx @ Sz + Sz @ Sx)


def full_pauli_decomp(A):
    """Decompose 8x8 A into sum c_{abc} sigma_a otimes sigma_b otimes sigma_c."""
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    P = [I, X, Y, Z]
    names = ['I', 'X', 'Y', 'Z']
    coeffs = {}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                op = np.kron(P[a], np.kron(P[b], P[c]))
                coef = np.trace(op.conj().T @ A) / 8
                if abs(coef) > 1e-10:
                    coeffs[names[a] + names[b] + names[c]] = complex(coef)
    return coeffs


def build_HE_sym_full(n, A):
    """Build H_E in the symmetric subspace exactly for arbitrary 8x8 A.

    H_E = sum_{i<j<k} A on bits (i,j,k)
        = sum_{(a,b,c) Pauli-string of A} coef * sum_{i<j<k} sigma_a^i sigma_b^j sigma_c^k.

    For a Pauli string P_a P_b P_c on (i,j,k), summed over all i<j<k,
    the result is a symmetric-group-invariant operator, so it acts within
    the fully symmetric spin-n/2 subspace as some polynomial in Sx, Sy, Sz.

    Simplest robust route: for each Pauli string (a,b,c) with coeff c_{abc},
    compute sum_{i<j<k} sigma_a^i sigma_b^j sigma_c^k on the full 2^n space
    once, then project to symmetric subspace. But that's expensive at large n.

    ALTERNATIVE (elegant): use collective spin operators.
    sum_i sigma_a^i = 2 S_a. So:
       sum_{i,j,k distinct, ordered} sigma_a^i sigma_b^j sigma_c^k
         = expansion involving (2S_a)(2S_b)(2S_c) minus lower-order overlap terms.
    Then divide by 6 (unordered) or 1 depending.

    We just do it fully-symmetric properly:
       sum_{i<j<k} P_a^i P_b^j P_c^k
    is 1/6 of the sum over all ordered distinct triples, PLUS symmetrization
    over the 6 permutations of (a,b,c) IF (a,b,c) not all distinct... too messy.

    Simplest: just build H_E on the full 2^n, project to permutation-symmetric
    subspace. Cost is 2^n x 2^n; for n up to ~14 this is fine (16384 x 16384
    is 2 GB, but we only need the symmetric block). For larger n we use the
    leading-order approximation.
    """
    if n > 14:
        # Fall back to leading order
        return build_HE_sym_farhi(n)
    # Build full HE via adiabatic_paths module
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from adiabatic_paths import build_HE
    HE_full = build_HE(n, A)
    # Project to symmetric subspace: build basis |j=n/2, m> as symmetric sum
    # over all bit strings with fixed Hamming weight = # of |1>'s = j - m
    # (with z_i=0 -> |0>, z_i=1 -> |1>, and Sz = sum_i sigma_z/2 = (n - 2*hw)/2 - hmm need care)
    j = n / 2
    dim_sym = int(2 * j + 1)
    dim = 2 ** n
    # In our indexing, sigma_z eigenvalue on |z_i=0> is +1, on |z_i=1> is -1.
    # So Sz-eigenvalue = (n - 2 * hw)/2 = n/2 - hw. So m = n/2 - hw, i.e. hw = n/2 - m.
    # We construct symmetric basis vector |sym, m> = normalized sum over all
    # bit strings with Hamming weight (n/2 - m).
    from math import comb
    P = np.zeros((dim, dim_sym), dtype=complex)
    for m_idx in range(dim_sym):
        m = -j + m_idx  # m from -j to +j
        hw = int(n / 2 - m)
        # sum over all states with Hamming weight hw
        indices = [s for s in range(dim) if bin(s).count("1") == hw]
        norm = 1.0 / np.sqrt(len(indices))
        for s in indices:
            P[s, m_idx] = norm
    HE_sym = P.conj().T @ HE_full @ P
    return HE_sym


def gap_sweep_sym(HB, HP, HE, n_s=400, use_HE=True):
    s_grid = np.linspace(0, 1, n_s)
    gaps = np.zeros(n_s)
    for idx, s in enumerate(s_grid):
        H = (1 - s) * HB + s * HP
        if use_HE and HE is not None:
            H = H + s * (1 - s) * HE
        w = np.linalg.eigvalsh(H)
        gaps[idx] = w[1] - w[0]
    return s_grid, gaps


def run_scaling(ns=(4, 6, 8, 10, 12, 16, 20, 30, 50, 80), n_s=400):
    from adiabatic_paths import A_FARHI
    results = {}
    for n in ns:
        t0 = time.time()
        HP = build_HP_sym(n)
        HB = build_HB_sym(n)
        # Full HE (with A_FARHI) if n small enough, else leading-order asymptotic
        if n <= 12:
            HE = build_HE_sym_full(n, A_FARHI)
            HE_kind = "full-from-A_FARHI"
        else:
            HE = build_HE_sym_farhi(n)
            HE_kind = "leading-order-only (-2n(SxSz+SzSx))"

        _, g_lin = gap_sweep_sym(HB, HP, None, n_s=n_s, use_HE=False)
        _, g_far = gap_sweep_sym(HB, HP, HE, n_s=n_s, use_HE=True)
        gm_lin = float(np.min(g_lin))
        gm_far = float(np.min(g_far))
        results[str(n)] = {
            "n": n,
            "dim_sym": int(n + 1),
            "HE_kind": HE_kind,
            "g_min_linear": gm_lin,
            "g_min_farhi_A": gm_far,
            "ratio": gm_far / gm_lin,
            "wall_seconds": time.time() - t0,
        }
        print(f"[n={n:3d}] g_min(lin)={gm_lin:.6f}  g_min(FarhiA)={gm_far:.6f}  ratio={gm_far/gm_lin:.3f}  ({HE_kind})  [{time.time()-t0:.1f}s]")
    with open(HERE / "scaling_results.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    print("Testing symmetric subspace against full 2^n (small n):")
    from adiabatic_paths import build_HP, build_HB, build_HE, A_FARHI
    for n in (4, 5, 6):
        HP_full = build_HP(n)
        HB_full = build_HB(n)
        HE_full = build_HE(n, A_FARHI)
        HP_sym = build_HP_sym(n)
        HB_sym = build_HB_sym(n)
        HE_sym = build_HE_sym_full(n, A_FARHI)

        # Ground energies at s=0.5
        for label, H_full, H_sym in [("HB", HB_full, HB_sym), ("HP", HP_full, HP_sym), ("HE", HE_full, HE_sym)]:
            e_full = float(np.min(np.linalg.eigvalsh(H_full)))
            e_sym = float(np.min(np.linalg.eigvalsh(H_sym)))
            print(f"  n={n} {label}: min eig full={e_full:.6f}  sym-subspace={e_sym:.6f}  diff={e_full-e_sym:.2e}")
        # Also compare g_min for linear path
        _, g_lin_full = gap_sweep_sym(HB_full, HP_full, None, n_s=200, use_HE=False)
        _, g_lin_sym = gap_sweep_sym(HB_sym, HP_sym, None, n_s=200, use_HE=False)
        print(f"  n={n} g_min(lin): full={np.min(g_lin_full):.6f}  sym={np.min(g_lin_sym):.6f}")
        _, g_far_full = gap_sweep_sym(HB_full, HP_full, HE_full, n_s=200)
        _, g_far_sym = gap_sweep_sym(HB_sym, HP_sym, HE_sym, n_s=200)
        print(f"  n={n} g_min(FarhiA): full={np.min(g_far_full):.6f}  sym={np.min(g_far_sym):.6f}")

    print("\n=== Scaling with n ===")
    run_scaling(ns=(4, 6, 8, 10, 12, 16, 20, 30, 50, 80), n_s=400)
