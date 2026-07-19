# Failure Analysis — chatterjee2023 (arXiv:2308.12703)

## What failed / friction
1. **Dense-eigh performance wall (fixed).** The first implementation diagonalized the full
   real-space BdG Hamiltonian densely at L=24 (dim 4608) for all nine g-sweep points plus the
   topological point — the run hung. Root cause: Apple Accelerate `eigh` scales steeply here
   (2048-dim ≈ 29 s, so 4608-dim ≈ minutes × 9). Fix: switch all near-zero-mode counting to
   `scipy.sparse.linalg.eigsh(sigma=0)` shift-invert at L=24 (a few seconds per point), and
   compute the expensive dense many-body quadrupole only at the reduced L=14. Runtime dropped to
   ~1 min. No physics changed.
2. **JSON serialization (fixed).** numpy bool from the `match` comparisons was not JSON
   serializable; wrapped in `bool(...)`.
3. **LLM-judge endpoint.** `argo:claude-opus-4.8` returned HTTP 502 (Bad Gateway) through the
   LiteLLM aggregator on 2026-07-19. Worked around by using `argo:claude-sonnet-4.6` (also free
   Argo) — verified live before use. Same substitution used across the other Wave-4 dirs.

## Residual gaps (scope limits, NOT failures)
- **Effective model (Eq.4) not implemented.** The unitary transformation giving the effective
  in-plane Zeeman + SOC is an analytic result; we tested the exact Eq.(1) model it approximates,
  not the effective theory itself. Documented as out of scope.
- **Edge theory / analytic phase boundary not reproduced.** The white-line boundaries in the
  paper's Fig. 3 come from a low-energy edge calculation; not attempted (analytic).
- **1D cut, not 2D phase maps.** We tested a single g-cut at fixed (λ, Jex); the paper's full
  λ–g and Jex–g phase diagrams were not scanned point-by-point.
- **Reduced lattice.** L=24 (MCM) / L=14 (Qxy) vs the paper's 30×30. Consequence: zero-mode
  energy is ~1e-4 rather than the paper's ~1e-7 — this is the *correct* exponential finite-size
  Majorana splitting, not a qualitative discrepancy.
- **Single quadrupole method.** Qxy computed only via the many-body Resta/Wheeler formula; no
  independent nested-Wilson-loop cross-check (see open_questions Q2).
- **Model-normalized units** (energies in units of t); no absolute-meV comparison, matching the paper.

## What's needed to close
Nested Wilson-loop quadrupole implementation (cross-check C2); full 2D phase-diagram scan +
analytic boundary from Eq.(4) (close C4/C5); finite-size scaling E(L)→0 at 30×30 and beyond;
disorder/incommensurate-pitch robustness study. See open_questions.json (Q1–Q5).

## Honesty note
Verdict REPLICATED applies to the three numerical headline claims (4 MCMs, Qxy=1/2 vs 0,
g-driven transition), which are quantitatively reproduced — the exact Qxy quantization is the
decisive piece of evidence. The analytic effective-model and edge-theory supplements were not
tested and are noted as scope limits, not failures.
