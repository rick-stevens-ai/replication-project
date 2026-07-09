# Artifacts inventory — quant-ph/0301023

## Required 8 (per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Artifact | Path | Present? | Size | Notes |
|---|----------|------|----------|------|-------|
| 1 | Original PDF | `paper.pdf` | ✅ | 363 KB | fetched from https://arxiv.org/pdf/quant-ph/0301023 |
| 2 | Marker markdown | `extraction/marker.md` | ✅ | 86 KB | **pdftotext fallback** (marker-pdf not installable on host; noted in file header) |
| 3 | Nougat mmd | `extraction/nougat.mmd` | ✅ | (produced by nougat 0.1.17 background run) | full-paper LaTeX-preserving parse |
| 4 | LaTeX report | `report/REPORT.tex` | ✅ | 16 KB | detailed section-by-section; verdict = REPLICATED |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✅ | 6 KB | 5 substantive questions each with `q/basis/next_steps` |
| 6 | Workflow | `report/workflow.md` | ✅ | 5 KB | narrative + tool/version table + effort estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ | (this file) | inventory + traces |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | | honest analysis of gaps + workarounds |

## Evidence + code (`report/evidence/`)

| File | Purpose |
|------|---------|
| `adiabatic_state_gen.py` | Full simulation code (400 LOC, self-contained) |
| `adiabatic_results.json` | Raw numeric results (fidelities per T, gap_min, scan, sanity, meta) |
| `run.log` | Stdout log of the reproducing run (15.4 s wall) |

## Working data (`work/`)

| File | Purpose |
|------|---------|
| `paper.pdf` | duplicate copy of arXiv PDF |
| `paper.txt` | pdftotext extraction (source for marker.md fallback) |

## Extraction (`extraction/`)

| File | Purpose |
|------|---------|
| `marker.md` | pdftotext-based fallback (marker-pdf unavailable on host) |
| `nougat.mmd` | Nougat LaTeX-preserving parse |
| `nougat.log` | Nougat run log |

## Provenance / traces

- Paper: `arXiv:quant-ph/0301023v2` (2003-01-07). Authors: Dorit Aharonov (Hebrew University); Amnon Ta-Shma (Tel Aviv University). Title verified against fetched PDF page 1.
- Reproduction seed: `numpy.random.default_rng(20260705)` — used only for experiment D's random 32-subset support (deterministic).
- Reproduction host: CherryRd (macOS, Python 3.13, numpy 2.4.3, scipy 1.18.0). All computations on CPU.
- No LLM endpoints called (100% mathematical simulation). No paid APIs.

## Key numeric results

| Claim | Result |
|-------|--------|
| C1 (A. uniform)   | F(T=10)  = 1.000000, F(T=200) = 1.000000  ✅ |
| C1 (B. Bernoulli) | F(T=10)  = 0.998812, F(T=200) = 0.999488  ✅ |
| C1 (C. coset)     | F(T=10)  = 0.999571, F(T=200) = 0.999789  ✅ |
| C1 (D. two-peak)  | F(T=10)  = 0.998000, F(T=200) = 0.997226  ✅ |
| C2 (t_tot vs 1/gap) | monotonic: 5,5,5,10,20,40 as gap 1.00→0.27  ✅ (~1/gap² scaling) |
| C3 (SZK Claim 1)  | \|LHS − RHS\| = 1.11 × 10⁻¹⁶ (machine precision)  ✅ |
| Sanity (2D vs 256d) | ‖Δψ‖₂ = 1.7 × 10⁻¹⁴, \|ΔF\| = 3.8 × 10⁻¹⁵  ✅ |
