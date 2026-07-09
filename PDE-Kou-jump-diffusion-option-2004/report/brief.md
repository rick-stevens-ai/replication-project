# Brief — Kou (2002) double-exponential jump-diffusion option pricing

Independent reproduction of the closed-form European call price reported in
Kou (2002) "A Jump-Diffusion Model for Option Pricing" (Management Science
48(8):1086–1101) for the paper's numerical example (footnote 9, p.1095):
S0=100, K=98, r=5%, T=0.5, sigma=0.16, lambda=1, p=0.4, eta1=10, eta2=5, giving
C = 9.14732.  Three independent numerical routes were built from scratch in
Python: (C1) closed-form via the Kou characteristic function and the
Fang–Oosterlee Fourier-cosine (COS) expansion, which reproduces the paper
value to 2.7 × 10⁻⁶; (C2) direct Monte-Carlo simulation of the exact log-return
distribution (2M paths), matching within MC standard error (z = +0.13); and
(C3) an explicit finite-difference solve of the associated PIDE, matching to
~2 × 10⁻². Cross-checks: put-call parity between COS and MC, a sensitivity
sweep over K ∈ {90, 95, 100, 105, 110} where all three routes agree, and the
Black–Scholes limit (λ → 0) recovered to 7 × 10⁻¹². Verdict: **REPLICATED**.
