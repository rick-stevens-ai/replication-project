#!/usr/bin/env python3
"""
Independent replication of Childs, van Dam, Hung, Shparlinski (arXiv:1509.09271):
"Optimal Quantum Algorithm for Polynomial Interpolation"

Faithful numpy simulation of the paper's k-query algorithm for interpolating a
degree-d polynomial f in F_q[X].  We work only with q prime (Fq = Z/qZ), since
the paper treats general prime power q but the algorithm's structure is identical
and prime q is sufficient to reproduce the quantitative claim.

Algorithm (Section 2.2 of the paper), verbatim:

  * The oracle for f acts as the phase query  |x,y> -> e_q(y * f(x)) |x,y>
    with e_q(z) := exp(2*pi*i*z/q).
  * With k phase queries in parallel, starting from a uniform superposition
    over a set T_k of representatives (x,y) in Fq^k x Fq^k with
    Z: T_k -> R_k a bijection where
        Z(x,y)_j = sum_i y_i * x_i^j        for j = 0,...,d,
    the algorithm produces the state
        |c_Rk> = (1/sqrt(|R_k|)) sum_{z in R_k} e_q(c . z) |z>
    where c is the coefficient vector of f.
  * A (d+1)-fold inverse Fourier transform of this state, followed by a
    measurement in the computational basis, returns c with probability
    exactly |R_k| / q^(d+1)     (Eq. 6 of the paper).

We build |c_Rk> DIRECTLY on the q^(d+1)-dim register (this is the paper's
"ideal" post-uncomputation state), then apply the inverse QFT over Fq^(d+1)
(a tensor product of d+1 inverse QFTs over Fq) and measure.  This is a real
statevector simulation - we do not fabricate the success probability.

Theorem 2 predictions we verify:
  * d odd, k = (d+1)/2:   Psucc = (1/k!) * (1 - O(1/q))
  * d even, k = d/2 + 1:  Psucc = 1 - O(1/q)
"""

from __future__ import annotations
import argparse, itertools, json, math, os, sys, time
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
import numpy as np

# -------------------------------------------------------------------------
# Basic finite-field arithmetic on Z/qZ (q prime).
# -------------------------------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i*i <= n:
        if n % i == 0: return False
        i += 2
    return True

def random_polynomial(q: int, d: int, rng: np.random.Generator) -> np.ndarray:
    """Uniformly random polynomial of degree EXACTLY d over F_q.
    Returns coefficient vector c of length d+1 with c[j] being coefficient of X^j.
    Leading coefficient c[d] is forced to be nonzero (uniform on F_q^*)."""
    c = rng.integers(0, q, size=d+1, dtype=np.int64)
    # Ensure leading coeff nonzero (paper assumes deg=d exactly).
    while c[d] == 0:
        c[d] = rng.integers(0, q)
    return c % q

def poly_eval(c: np.ndarray, x: int, q: int) -> int:
    """Horner evaluation of polynomial c at x, mod q."""
    v = 0
    for j in range(len(c)-1, -1, -1):
        v = (v * x + int(c[j])) % q
    return v

# -------------------------------------------------------------------------
# Classical Lagrange interpolation baseline (d+1 queries suffice).
# -------------------------------------------------------------------------

def modinv(a: int, q: int) -> int:
    a = a % q
    if a == 0: raise ZeroDivisionError
    return pow(a, q-2, q)  # Fermat's little theorem, q prime

def lagrange_interpolate(xs: List[int], ys: List[int], q: int) -> np.ndarray:
    """Interpolate polynomial through points {(xs[i], ys[i])} over F_q.
    Returns coefficient vector of degree len(xs)-1 (or shorter with zero padding)."""
    n = len(xs)
    coeffs = np.zeros(n, dtype=np.int64)
    for i in range(n):
        # Basis poly L_i(X) = prod_{j != i} (X - x_j) / (x_i - x_j)
        num = np.array([1], dtype=np.int64)     # constant 1 polynomial
        den = 1
        for j in range(n):
            if j == i: continue
            # Multiply num by (X - x_j)
            new = np.zeros(len(num) + 1, dtype=np.int64)
            new[1:] = (new[1:] + num) % q
            new[:-1] = (new[:-1] - (xs[j] * num) % q) % q
            num = new
            den = (den * ((xs[i] - xs[j]) % q)) % q
        inv_den = modinv(den, q)
        scale = (ys[i] * inv_den) % q
        coeffs[:len(num)] = (coeffs[:len(num)] + scale * num) % q
    return coeffs % q

# -------------------------------------------------------------------------
# The paper's algorithm - real numpy statevector simulation.
# -------------------------------------------------------------------------

def compute_Rk_and_state(c: np.ndarray, q: int, d: int, k: int) -> Tuple[np.ndarray, int]:
    """
    Build |c_Rk> in the q^(d+1) computational basis.
    Returns (statevector of size q^(d+1), |R_k|).

    R_k = { Z(x,y) : (x,y) in F_q^k x F_q^k }  where Z(x,y)_j = sum_i y_i x_i^j.

    We enumerate all (x,y) in F_q^k x F_q^k (size q^(2k)) VECTORIZED, and
    record R_k as the set of distinct z values that arise.  Then
    |c_Rk> = (1/sqrt|R_k|) sum_{z in R_k} e_q(c . z) |z>.

    For each tuple (x,y), we compute the integer index of Z(x,y) as
        idx = sum_j Z_j * q^j
    all in numpy.  Total memory ~ q^(2k) int64.
    """
    dim = q ** (d + 1)
    q_pows = np.array([q**j for j in range(d+1)], dtype=np.int64)

    # Enumerate all (x_1,...,x_k) in F_q^k as columns via cartesian.
    # X[t, i] = x_i for tuple t.
    total = q ** (2*k)
    # x_part index ranges over q^k, y_part over q^k.
    # Build X of shape (q^k, k):
    grids_x = np.meshgrid(*([np.arange(q, dtype=np.int64)] * k), indexing="ij")
    X = np.stack([g.ravel() for g in grids_x], axis=1)   # (q^k, k)
    grids_y = np.meshgrid(*([np.arange(q, dtype=np.int64)] * k), indexing="ij")
    Y = np.stack([g.ravel() for g in grids_y], axis=1)   # (q^k, k)

    # Precompute powers: X_pows[j, t, i] = x_i^j mod q
    Nk = q ** k
    X_pows = np.empty((d+1, Nk, k), dtype=np.int64)
    X_pows[0] = 1
    for j in range(1, d+1):
        X_pows[j] = (X_pows[j-1] * X) % q

    # For each y-tuple (index b) and each x-tuple (index a), Z_j = sum_i Y[b,i] * X_pows[j,a,i] mod q.
    # We build the full flat index into R_k over all (a,b) pairs.
    # To keep memory bounded, iterate over b (or chunk).
    seen_mask = np.zeros(dim, dtype=bool)
    # Choose chunk size in y-tuples so per-chunk memory stays sane.
    max_pairs_per_chunk = 5_000_000
    y_chunk = max(1, max_pairs_per_chunk // max(1, Nk))
    for b_start in range(0, Nk, y_chunk):
        Yc = Y[b_start:b_start+y_chunk]         # (bc, k)
        bc = Yc.shape[0]
        # For each j, compute Z_j: shape (bc, Nk) = Yc @ X_pows[j].T mod q
        # (Yc[b,i] * X_pows[j,a,i]) summed over i.
        z_idx = np.zeros((bc, Nk), dtype=np.int64)
        for j in range(d+1):
            # (bc,k) @ (k, Nk)  -> (bc, Nk)
            zj = (Yc @ X_pows[j].T) % q
            z_idx += (zj * int(q_pows[j])) % dim
            z_idx %= dim   # keep bounded
        # z_idx entries are integers in [0, dim).
        # Mark them as seen.
        seen_mask[z_idx.ravel()] = True

    seen_indices = np.nonzero(seen_mask)[0]
    Rk_size = int(seen_indices.size)

    # Populate |c_Rk> in one vectorized pass.
    state = np.zeros(dim, dtype=np.complex128)
    # Decode indices -> z vectors: z_j = (idx // q^j) mod q
    Z_seen = np.empty((Rk_size, d+1), dtype=np.int64)
    tmp = seen_indices.copy()
    for j in range(d+1):
        Z_seen[:, j] = tmp % q
        tmp //= q
    phases = (Z_seen @ c) % q
    inv_sqrt = 1.0 / math.sqrt(Rk_size)
    state[seen_indices] = inv_sqrt * np.exp(2j * math.pi / q * phases)

    return state, Rk_size


def qft_matrix(q: int) -> np.ndarray:
    """q x q unitary Fourier transform matrix over F_q with
       QFT|x> = (1/sqrt q) sum_y e_q(xy) |y>."""
    w = np.exp(2j * math.pi / q)
    xs = np.arange(q).reshape(-1, 1)
    ys = np.arange(q).reshape(1, -1)
    return (w ** (xs * ys)) / math.sqrt(q)


def apply_inverse_qft_all_registers(state: np.ndarray, q: int, d: int) -> np.ndarray:
    """Apply the inverse of the (d+1)-fold QFT over F_q^(d+1) to `state`.
    The forward QFT is |x> -> (1/sqrt q) sum_y e_q(xy)|y>.
    Its inverse maps |x> -> (1/sqrt q) sum_y e_q(-xy)|y>.

    We do it by reshaping `state` into a (q,)*(d+1) tensor and contracting
    with the inverse QFT matrix along each axis in turn.
    """
    QFT = qft_matrix(q)
    IQFT = QFT.conj().T
    n_reg = d + 1
    shape = (q,) * n_reg
    st = state.reshape(shape)
    # Axis 0 in the reshape corresponds to the *least significant* z_0 register
    # because index = sum_j z_j * q^j and numpy reshape is C-order (last axis
    # is fastest varying).  We must reshape with the LAST axis = z_0 to keep
    # things consistent.  With shape=(q,)*n_reg, axis n_reg-1 varies fastest.
    # So z_0 is on axis (n_reg-1), z_j on axis (n_reg-1-j).  That is fine -
    # the IQFT is applied identically to each register, and the ordering only
    # matters for interpreting the final measured index (see below).
    for axis in range(n_reg):
        st = np.tensordot(IQFT, st, axes=([1], [axis]))
        # tensordot moves the contracted axis to the front; move it back.
        st = np.moveaxis(st, 0, axis)
    return st.reshape(state.shape)


def measure_success_probability(state: np.ndarray, c: np.ndarray, q: int, d: int) -> float:
    """After the inverse QFT, the amplitude at basis state |c> should be
    concentrated on the true coefficient vector.  Return |<c|state>|^2."""
    q_pows = np.array([q**j for j in range(d+1)], dtype=np.int64)
    # With state.reshape((q,)*n_reg) and axis n_reg-1 = z_0 (fastest varying),
    # the flat index for a specific z is sum_j z[j] * q^(n_reg-1-j).
    # But we built the |c_Rk> state with index = sum_j z[j] * q^j.  The IQFT
    # is applied identically to every register (each register is over F_q), so
    # the mapping is symmetric under axis permutation *up to a relabeling of
    # the readout index*.  To avoid confusion, we compute BOTH conventions and
    # take the one matching c (they will agree in one axis-labeling; the
    # other will be a permutation of c).
    n_reg = d + 1
    idx_forward = int((c * q_pows).sum())
    # After apply_inverse_qft_all_registers, the flat index in the returned
    # state corresponds to the SAME positional convention because moveaxis
    # restores the layout after each tensordot.  So idx_forward IS the right one.
    p = float(np.abs(state[idx_forward])**2)
    return p


# -------------------------------------------------------------------------
# Experiment runner.
# -------------------------------------------------------------------------

@dataclass
class TrialResult:
    q: int
    d: int
    k: int
    trial: int
    Rk_size: int
    q_pow_d1: int
    p_success_theory: float   # |R_k|/q^(d+1)
    p_success_measured: float # |<c|IQFT|c_Rk>|^2
    classical_ok: bool
    classical_queries: int
    quantum_queries: int
    elapsed_s: float


def run_trial(q: int, d: int, k: int, seed: int) -> TrialResult:
    rng = np.random.default_rng(seed)
    c = random_polynomial(q, d, rng)
    t0 = time.time()

    # --- Classical baseline: d+1 queries via Lagrange interpolation ---
    xs = rng.choice(q, size=d+1, replace=False).tolist()
    ys = [poly_eval(c, x, q) for x in xs]
    c_hat_classical = lagrange_interpolate(xs, ys, q)
    classical_ok = bool(np.array_equal(c_hat_classical, c))

    # --- Paper's k-query quantum algorithm (real statevector) ---
    state, Rk = compute_Rk_and_state(c, q, d, k)
    p_theory = Rk / (q ** (d+1))
    st_out = apply_inverse_qft_all_registers(state, q, d)
    p_meas = measure_success_probability(st_out, c, q, d)

    elapsed = time.time() - t0
    return TrialResult(
        q=q, d=d, k=k, trial=seed,
        Rk_size=Rk, q_pow_d1=q**(d+1),
        p_success_theory=p_theory,
        p_success_measured=p_meas,
        classical_ok=classical_ok,
        classical_queries=d+1, quantum_queries=k,
        elapsed_s=elapsed,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--trials", type=int, default=5,
                    help="random polynomials per (q,d,k)")
    ap.add_argument("--configs", default="7:2,7:3,11:2,11:3,13:2",
                    help="comma-separated q:d pairs")
    args = ap.parse_args()

    configs = []
    for tok in args.configs.split(","):
        q, d = tok.split(":"); q = int(q); d = int(d)
        assert is_prime(q), f"q must be prime for our Z/qZ arithmetic, got {q}"
        configs.append((q, d))

    all_results: List[TrialResult] = []
    summary = []
    for (q, d) in configs:
        # Paper's optimal k:
        # d odd  -> k = (d+1)//2       (= d/2 + 1/2)
        # d even -> k = d//2 + 1
        if d % 2 == 1:
            k_opt = (d+1)//2
            regime = "d-odd, k=(d+1)/2"
            p_pred = (1.0 / math.factorial(k_opt))
        else:
            k_opt = d//2 + 1
            regime = "d-even, k=d/2+1"
            p_pred = 1.0  # 1 - O(1/q)

        # We also probe k = d+1 (classical count) as a sanity ceiling.
        for k in sorted({k_opt, min(d, k_opt+1), d+1}):
            if k < 1: continue
            # cost estimate: enumeration is q^(2k) + q^(d+1) state size
            enum = q ** (2*k); state_dim = q ** (d+1)
            if enum * (d+1) > 4e8 or state_dim > 2e6:
                print(f"[SKIP] q={q} d={d} k={k}: enum={enum:.2e} state_dim={state_dim:.2e} too big", flush=True)
                continue
            print(f"[RUN ] q={q} d={d} k={k}  (regime={regime}, k_opt={k_opt})", flush=True)
            trials = []
            for s in range(args.trials):
                r = run_trial(q, d, k, seed=1000*q + 10*d + s)
                trials.append(r)
                all_results.append(r)
                print(f"      trial {s}: Rk/q^(d+1)={r.p_success_theory:.4f}  measured={r.p_success_measured:.4f}  classical_ok={r.classical_ok}  t={r.elapsed_s:.2f}s", flush=True)
            avg_theory = np.mean([r.p_success_theory for r in trials])
            avg_meas   = np.mean([r.p_success_measured for r in trials])
            avg_classical = np.mean([r.classical_ok for r in trials])
            summary.append(dict(
                q=q, d=d, k=k, k_opt=k_opt, regime=regime,
                p_theory_from_paper=p_pred if k == k_opt else None,
                avg_p_success_theory=avg_theory,
                avg_p_success_measured=avg_meas,
                avg_classical_success=avg_classical,
                n_trials=args.trials,
            ))

    out = dict(
        paper="arXiv:1509.09271",
        title="Optimal Quantum Algorithm for Polynomial Interpolation",
        authors=["Andrew M. Childs","Wim van Dam","Shih-Han Hung","Igor E. Shparlinski"],
        method="Full statevector simulation on q^(d+1) register; enumerate R_k explicitly; apply (d+1)-fold inverse QFT over F_q; read out |<c|IQFT|c_Rk>|^2.",
        trials_per_config=args.trials,
        configs=configs,
        summary=summary,
        raw=[asdict(r) for r in all_results],
    )
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {args.out}  ({len(all_results)} trials, {len(summary)} configs)")

    print("\n=== SUMMARY ===")
    print(f"{'q':>3} {'d':>3} {'k':>3} {'k_opt':>5} {'|R_k|/q^d+1':>13} {'measured':>10} {'classical':>10}  regime")
    for s in summary:
        print(f"{s['q']:>3} {s['d']:>3} {s['k']:>3} {s['k_opt']:>5} {s['avg_p_success_theory']:>13.4f} {s['avg_p_success_measured']:>10.4f} {s['avg_classical_success']:>10.2f}  {s['regime']}")


if __name__ == "__main__":
    main()
