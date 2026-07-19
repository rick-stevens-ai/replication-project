# Failure Analysis — cheon2018 (arXiv:1803.06428)

## What failed / friction
1. **Extra interband Berry SOT not resolved (root cause + workaround).** The raw off-diagonal Kubo
   sum sum_{n!=n'} Im[<n|s|n'><n'|v|n>](f_n-f_n')/((E_n-E_n')^2+Sigma^2) returned ~1e-18 for the
   symmetry-sensitive spin components (delta_S^y for E||x, delta_S^z) at BOTH m=0 and m!=0 — i.e. it
   did NOT resolve the small extra-Berry piece that turns on with m. Root cause: the symmetry-allowed
   and symmetry-forbidden contributions are not separated; the forbidden piece is a tiny difference
   swamped by cancellation. Workaround: refocused the replication on the cleanly computable MECHANISM
   (Eq.2 degeneracy + its lifting + the collinear-allowed SOT), and honestly flagged the absolute
   extra-Berry magnitude as method-limited (Open Q1). Diagnosis via a full (spin-comp x E-dir) scan.
2. **LLM-judge endpoint.** opus-4.x aggregator parse error 2026-07-19; used free sonnet-4.6.

## Residual gaps (=> PARTIAL)
- **C4 method-limited:** absolute extra interband Berry SOT vs m unresolved (needs symmetry-odd
  operator projection + proper clean-limit Bastin/Streda weighting). This is the paper's headline
  NUMBER; only the enabling mechanism is demonstrated.
- **C5 not done:** 2D bipartite model (Eq.9), threshold m*(Sigma,T) phase boundary, DW-motion estimate.
- **Model-normalized units.**

## What's needed to close
Symmetry decomposition of delta_S into m=0-even/odd parts; evaluate the odd part with a constant-Gamma
Bastin formula; implement Eq.9; sweep (m,Sigma,T) for the threshold. See open_questions.json.

## Honesty note
Verdict PARTIAL is correct: the full Eq.1 Hamiltonian and the paper's symmetry MECHANISM (degeneracy
protected at m=0, lifted linearly by noncollinearity) are reproduced rigorously; the absolute
extra-Berry-SOT magnitude is method-limited. Recurring reduced-scope PARTIAL for this campaign.
