# Workflow — lucid-stochastic-rejoining

## Paper
Li Y, Qian H, Wang Y, Cucinotta FA (2012). *A Stochastic Model of DNA Fragments Rejoining.* PLoS ONE 7(9): e44293. DOI [10.1371/journal.pone.0044293](https://doi.org/10.1371/journal.pone.0044293).

## Set / lane
- **Set:** LUCID (LUCID-100 replication track)
- **Verdict:** REPLICATED (STRONG, 4-tier)
- **Coverage:** 13/13 explicit claims — 8 STRONG, 3 PARTIAL, 1 structural, 1 deferred

## Reproduction workflow

### Pass-1 (2026-05-28)
1. Read paper (ad-hoc pdftotext extraction, pre-Marker).
2. Enumerate 8 testable claims (C1–C8).
3. Reimplement Gillespie SSA from paper eqs → `code/gillespie_rejoining.py`.
4. Run three primary experiments: `run_fig3_impact_factors.py` (L̄, V, M_T sweeps), `run_fig4_kinetics.py` (biphasic kinetics under high/low LET), `smoke_test.py` (single-run correctness).
5. Verdict: 6 directly run + 2 structural + 1 deferred = 9 total addressed; PARTIAL/STRONG mix.

### REPASS-1 (2026-06-23)
1. Re-parse paper from **canonical Marker parse** (`_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/10_1371_journal_pone_0044293/…md`, 9 pages, LaTeX-preserved equations).
2. Enumerate **5 additional claims** (C9, C10, C11, C12, C13) + revisit C7 as C7-revisit.
3. One script per claim in `code/repass1/`:
   - `c7_revisit_biphasic_fit.py` — two-exponential fit of model kinetic curve
   - `c9_secondary_jump.py` — sweep L̄ ∈ [15,100] to detect L*/m plateaus
   - `c10_event_count_check.py` — audit recruit/join/release counts vs paper's structural claim
   - `c11_2d_fraction_surface.py` — 6×6 (r1,r2) heatmap
   - `c12_variance_check.py` — std/spread discontinuity at L*
   - `c13_k3_sweep.py` — k3 ∈ {0.025, 0.05, 0.1, 0.2, 0.4} at L̄=30 and L̄=80
4. Each script writes JSON summary to `logs/repass1/*.json`, NPZ arrays to `results/repass1/*.npz`, figures to `figures/repass1/*.png`.
5. Report update in `REPORT.md` (pass-1 preserved verbatim as `REPORT.pass1.md`).

### Backfill (2026-07-06)
LaTeX conversion + open-questions + failure-analysis + workflow/artifact/nougat stubs (this file).

## Tools & versions

| Tool | Version | Where |
|------|---------|-------|
| Python | 3.13 | CherryRd (iMac) |
| NumPy | 2.4.3 | pip |
| SciPy | 1.18.0 | pip |
| Matplotlib | 3.10.8 | pip |
| PDF parser (REPASS-1 source) | Marker (Datalab marker_pdf hybrid) | uicgpu 2026-06-22 run |

## Compute

- **Host:** CherryRd (iMac), CPU-only
- **Total wallclock:**
  - Pass-1: ~2 min for three sweep scripts
  - REPASS-1: **43 seconds** across all 6 scripts (Gillespie SSA is embarrassingly small for M_T ≤ 50)
  - Backfill: ~1 min human/AI text authoring (no re-runs)
- **No GPU. No network. No paid API.**

## Work estimate (recreate from scratch)

For an independent replicator starting from the paper PDF:

| Phase | Hours (skilled) |
|-------|-----------------|
| Read paper + enumerate claims | 3 |
| Implement Gillespie SSA (~200 lines) | 4 |
| Verify against paper figures 2, 3, 4 | 3 |
| REPASS-1 scripts (6 additional claims) | 4 |
| Write-up | 3 |
| **Total** | **~17 h** |

## Reproducer (from a clean CherryRd shell)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-stochastic-rejoining/
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib

# Pass-1 core sweeps
python code/run_fig3_impact_factors.py      # L̄, V, M_T sweeps
python code/run_fig4_kinetics.py            # biphasic kinetics
python code/smoke_test.py                    # single-run sanity

# REPASS-1 six-claim battery
python code/repass1/c7_revisit_biphasic_fit.py
python code/repass1/c9_secondary_jump.py
python code/repass1/c10_event_count_check.py
python code/repass1/c11_2d_fraction_surface.py
python code/repass1/c12_variance_check.py
python code/repass1/c13_k3_sweep.py

# Rebuild the LaTeX report
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

Expected wallclock: **~50 s** total for the full 6-script REPASS-1 battery on any modern laptop CPU. Determinism: seed=42 baked into every script; per-claim seed sweeps use seed ∈ {42, 43, ..., 44} where noted.

## Endpoints used

- Local CPU only.
- No LLM inference used in the model runs.
- Backfill text-authoring used Argo (`argo:claude-opus-4.7`) via free localhost:44497 (per Rick's free-endpoints-only policy).

## Parser provenance

- **Pass-1:** ad-hoc pdftotext extraction (pre-Marker era). No provenance file.
- **REPASS-1:** canonical Marker parse from uicgpu 2026-06-22 batch → `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/10_1371_journal_pone_0044293/10_1371_journal_pone_0044293.md`. See sibling file `PARSER_PROVENANCE` for the sha256.
- **Nougat:** not required — Marker parse was already LaTeX-clean for all equations (page-2 rate laws, page-4 event-count derivation). See `extraction/nougat.mmd` for a stub with the paper.pdf sha256 pointer.
