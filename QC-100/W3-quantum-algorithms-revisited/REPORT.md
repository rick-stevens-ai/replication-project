# Replication Report — "Quantum Algorithms Revisited"

**Paper:** R. Cleve, A. Ekert, C. Macchiavello, M. Mosca, *Quantum Algorithms Revisited*, Proc. R. Soc. Lond. A **454**, 339–354 (1998).
**Wave:** QC-100 W3 · **Owner:** Ollie · **Verdict:** **REPLICATED**

## Scope
The paper unifies the major early quantum algorithms as instances of the pattern
*(Hadamard/QFT → f-controlled-U → QFT)* / quantum phase estimation. Its testable
headline claims:

1. **Deutsch-Jozsa** — a *single* f-controlled query distinguishes constant vs
   balanced with **certainty** (improvement over Deutsch-Jozsa's original 2-query version).
2. **Bernstein-Vazirani** — the *same* network recovers the hidden string `a` in one query.
3. **Phase estimation** — the best m-bit estimate of an arbitrary eigenphase φ is
   obtained with probability **≥ 4/π² = 0.405…** (Sect. 5 + Appendix C), and this can be
   amplified with extra counting bits (dyadic φ → P=1).
4. **Shor order-finding via phase estimation** — QPE on U:|y⟩→|ay mod N⟩ yields
   eigenphases s/r; continued fractions extract r and factor N.
5. **Grover** — repeating the sequence ~(π/4)2^{n/2} times finds the tagged k with
   **"probability greater than 0.5"** (paper, Fig. 7 caption).

All five are pure simulator targets. Coverage of the paper's algorithm catalog: 5/5 of the
explicitly-stated quantitative algorithm claims (Simon/discrete-log mentioned but only
qualitatively in this paper; the QFT-as-interferometry framing in Sect. 4 is conceptual).

## Methods
Exact state-vector simulator built directly in numpy (no framework), so all bit/index
conventions are under explicit control and checked against analytic values. Inverse-QFT
implemented as the exact unitary matrix. Phase oracles for DJ/BV; eigenphase injection for
QPE; full classical-quantum Shor loop (random a, gcd, order-finding by QPE, continued
fractions, even-order/non-trivial-root test). Grover uses exact oracle + diffusion
operators. Seed = 12345.

## Results (all numbers from `results.json`, this run)

| Claim | Paper | Replication | Tol / status |
|---|---|---|---|
| DJ constant → P(|0…0⟩) | 1 | 1.000000 (n=1–4) | exact ✓ |
| DJ balanced → P(|0…0⟩) | 0 | 0.0 (≤1e-16, n=1–4) | exact ✓ |
| BV recover hidden a (1 query) | P=1 | P=1.0000, match=True (n=3,5,8) | exact ✓ |
| QPE min P(best m-bit), m=8 | ≥ 0.4053 | **0.4056** (min over 2000 random φ) | ✓ (0/2000 below bound) |
| QPE dyadic φ | P=1 | 1.0000 | exact ✓ |
| Shor eigenphases s/r (a=7,N=15,r=4) | {0,¼,½,¾} | a_meas/2^m = {0,0.25,0.5,0.75}, P=1 each | exact ✓ |
| Shor factors of 15 | {3,5} | {3,5}, success 0.983 (300 trials) | ✓ |
| Grover P_k > 0.5 | >0.5 | 0.945–0.999 (n=3–8) | ✓ |

## Verdict: REPLICATED
- **Coverage 9/10** — every quantitative algorithm claim in the paper was implemented and
  tested; only qualitative mentions (Simon, discrete log) left untested.
- **Agreement 10/10** — DJ/BV/QPE-dyadic/Shor-eigenphases are exact to machine precision;
  the QPE 4/π² lower bound holds with 0 violations across 2000 random phases (observed min
  0.4056, just above the analytic 0.4053); Grover and Shor success rates match the paper's
  ">0.5" / "factors N" claims.
- No bit-ordering pathologies: QPE eigenphases land exactly on s/r, confirming index
  convention is correct.

**Files:** `paper.md`, `replicate.py`, `results.json`.
