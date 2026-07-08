# Attempt log

## 2026-07-06 14:08 CDT — start

- Read wave brief + REPLICATION_DIR_STANDARD_2026-07-05.
- Created target dir `QC-quantum-minimum-finding-durr-hoyer-1996/`.
- Pulled `paper.pdf` from `https://arxiv.org/pdf/quant-ph/9607014` (77 KB, 2 pages).
- Discovered an existing sibling QC-200 replication of the same paper. Per Rick's rule
  ("do not overwrite existing sibling replication dirs"), left QC-200 untouched. Copied
  its `extraction/marker.md` and `extraction/nougat.mmd` (deterministic PDF text
  extractions — no work-product duplication).
- Skimmed marker.md; identified core claims C1-C4.

## Implementation phase

- Wrote `work/durr_hoyer_independent.py` from scratch: pure numpy, no external quantum
  SDK. Independent of the QC-200 implementation.
  - Grover: `uniform_superposition`, `oracle_flip` (phase-flip marked amplitudes),
    `diffusion` (reflect about mean), `measure` (inverse-CDF sampling).
  - BBHT: m starts at 1, multiplier λ = 6/5, capped at √N; random Grover-count draw.
  - Outer loop: uniform-random initial threshold, iteration budget
    ⌈22.5·√N + 1.4·lg²N⌉ matching paper text.
- Wrote `work/grover_sanity.py`: cross-check against closed-form Grover probability
  `sin²((2r+1)θ)` with `sinθ=√(k/N)`, r = round(π/4·√(N/k)). All 12 grid cells matched
  within |Δ| ≤ 0.027 (2000 trials each).
- Wrote `work/bbht_t_sweep.py`: measures BBHT expected iterations vs t. Confirmed
  ratio mean_iters/√(N/t) is bounded (< 0.81) across (N, t) grid, N up to 128.
- Wrote `work/classical_baseline.py`: measured classical linear-scan probes = N always,
  matching O(N) reference.

## Execution

- Smoke run N=8,16 trials=50 — success prob 1.0, ~0.02s.
- Full run N=4,8,16,32,64 trials=300 — success prob 1.0 across the board, 0.4s wall.
- Grover sanity: 0.5s wall, matches closed form to <3%.
- BBHT t-sweep: 21 (N,t) cells, 300 trials each, ~1s wall.
- Classical baseline: 800 trials total, <0.1s wall.

## LLM-judge

- First run (`argo:claude-opus-4.7`): 502 Bad Gateway (upstream Argo hiccup) — 3 retries
  failed; same for `argo:claude-opus-4.8`. Fell back to `argo:gpt-5.2` — OK.
  First verdict: **PARTIAL** — flagged (a) no t-sweep for C3, (b) no classical baseline.
- Added `bbht_t_sweep.py` and `classical_baseline.py` addressing both concerns; re-judged.
- Second verdict (same model, richer evidence): **PARTIAL** — still PARTIAL because
  success_prob = 1.0 across N∈{4..64} doesn't stress-test the tightness of the ≥1/2 bound
  and no scaling of success-prob vs N at fixed budget is run. Accepted as honest verdict.

## Artifact production

- Wrote REPORT.tex (very detailed), open_questions.json (5 questions with next_steps),
  workflow.md, artifacts_summary.md, failure_analysis.md.
- Did NOT compile REPORT.tex to PDF (no `pdflatex` guaranteed on cherryrd; the standard
  says "compile to REPORT.pdf when possible" — attempted below).
