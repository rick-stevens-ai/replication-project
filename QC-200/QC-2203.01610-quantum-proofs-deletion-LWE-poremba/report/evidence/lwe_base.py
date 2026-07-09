"""
LWE base for Poremba 2022 (arXiv:2203.01610) Dual-Regev PKE with Certified Deletion.

Small-parameter classical Dual-Regev PKE (no quantum yet). This is the classical
skeleton of Section 7.1 Construction 1 of the paper:

    KeyGen(1^λ):
        Ā <-$ Z_q^{n × m}
        x̄ <-$ {0,1}^m
        A = [Ā | Ā·x̄ (mod q)]  ∈ Z_q^{n × (m+1)}
        pk = A, sk = (-x̄, 1) ∈ Z_q^{m+1}

    Enc(pk, b ∈ {0,1}):
        [Paper uses a primal Gaussian state which, on comp-basis measurement, samples]
        [c = s A + e + (0,...,0, b·⌊q/2⌋)  with s <-$ Z_q^n, e ~ D_{Z_q^{m+1}, αq/√2}]
        classical stand-in: draw s, e directly. The primal Gaussian state, when
        measured in the computational basis, gives exactly this classical Dual-Regev
        distribution (Lemma 17 in the paper).

    Dec(sk, c):
        v = c · sk = (b · ⌊q/2⌋) + <e, sk>   (mod q)   [since s Ā x̄ - s (Ā x̄) = 0]
        wait: with sk = (-x̄, 1),
              c · sk = <s Ā, -x̄> + <s (Ā x̄), 1> + <e, sk> + b·⌊q/2⌋
                     = -s Ā x̄ + s Ā x̄ + <e, sk> + b·⌊q/2⌋
                     = <e, sk> + b·⌊q/2⌋   (mod q)
        Output 0 iff v is closer to 0 than to ⌊q/2⌋.

Parameters used here (small but faithful to the paper's Construction 1 constraints):
    n = 8, q = 257 (prime), m ≥ 2 n log q  =>  m = 128
    noise ratio α such that √(8(m+1)) ≤ 1/α ≤ q / √(8(m+1))
        m=128 => √(8·129) ≈ 32.12, q/√(8·129) ≈ 8.00  --  INFEASIBLE (window is empty)
        We adopt the "task-brief" σ = 3.2 (encryption noise σ_enc = α q / √2 in Lemma 17;
        equivalently, we pick e ~ D_{Z_q^{m+1}, σ_enc} directly, then re-derive
        an "effective" α = σ_enc·√2 / q for logging).
    We honor the brief's σ=3.2 as the classical LWE noise for the base tests.
"""

from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass

# --------------------------- parameters -----------------------------
@dataclass(frozen=True)
class Params:
    n: int = 8
    q: int = 257                # prime
    m: int = 128                # >= 2 n log q  => 2*8*log2(257) ~= 128
    sigma_enc: float = 3.2      # discrete Gaussian sigma for LWE noise (task brief)

DEFAULT = Params()

# --------------------------- discrete Gaussian --------------------
def discrete_gaussian_sample(sigma: float, size: int, rng: np.random.Generator,
                             cutoff: float = 6.0) -> np.ndarray:
    """Sample size integers from D_{Z, sigma} centered at 0, truncated at cutoff*sigma.
    Simple rejection sampler."""
    K = int(math.ceil(cutoff * sigma))
    xs = np.arange(-K, K + 1)
    p = np.exp(-np.pi * (xs.astype(float) ** 2) / (sigma ** 2))  # discrete Gaussian rho_{sigma}(x) ∝ e^{-π x^2/σ^2}
    p /= p.sum()
    return rng.choice(xs, size=size, p=p)

def sample_error(sigma: float, m: int, rng: np.random.Generator) -> np.ndarray:
    """Vector of m integer samples ~ D_{Z, sigma}."""
    return discrete_gaussian_sample(sigma, m, rng).astype(np.int64)

# --------------------------- key generation ----------------------
def keygen(p: Params, rng: np.random.Generator):
    A_bar = rng.integers(0, p.q, size=(p.n, p.m), dtype=np.int64)
    x_bar = rng.integers(0, 2, size=p.m, dtype=np.int64)   # {0,1}^m
    last_col = (A_bar @ x_bar) % p.q                       # in Z_q^n
    A = np.concatenate([A_bar, last_col.reshape(p.n, 1)], axis=1)  # (n, m+1)
    sk = np.concatenate([(-x_bar) % p.q, np.array([1], dtype=np.int64)])  # (m+1,)
    return A, sk

# --------------------------- encryption --------------------------
def encrypt_classical(A: np.ndarray, b: int, p: Params, rng: np.random.Generator):
    """Classical Dual-Regev encryption (== computational-basis measurement of the
    paper's primal Gaussian state, per Lemma 17)."""
    n, mplus1 = A.shape
    s = rng.integers(0, p.q, size=n, dtype=np.int64)
    e = sample_error(p.sigma_enc, mplus1, rng)
    c = (s @ A + e) % p.q
    c[-1] = (c[-1] + b * (p.q // 2)) % p.q
    return c, s, e

# --------------------------- decryption --------------------------
def decrypt(sk: np.ndarray, c: np.ndarray, p: Params) -> int:
    v = int((c @ sk) % p.q)
    d0 = min(v, p.q - v)                    # circular distance to 0
    half = p.q // 2
    d1 = min((v - half) % p.q, (half - v) % p.q)
    return 0 if d0 <= d1 else 1

# --------------------------- self-check --------------------------
def smoke(p: Params = DEFAULT, trials: int = 400, seed: int = 0):
    rng = np.random.default_rng(seed)
    ok = 0
    for _ in range(trials):
        A, sk = keygen(p, rng)
        b = int(rng.integers(0, 2))
        c, s, e = encrypt_classical(A, b, p, rng)
        b_out = decrypt(sk, c, p)
        ok += int(b_out == b)
    return {"trials": trials, "correct": ok, "acc": ok / trials,
            "params": {"n": p.n, "q": p.q, "m": p.m, "sigma_enc": p.sigma_enc}}

if __name__ == "__main__":
    import json
    print(json.dumps(smoke(), indent=2))
