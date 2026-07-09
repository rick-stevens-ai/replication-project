# Workflow

**Slot:** lucid100-belov-dsb-repair-pathways-slot66
**Set:** LUCID-100 (Wave 7, B-tier, rank 97)
**Paper:** Belov et al. 2015, JTB 366:115–130 (open-access surrogate: JINR E19-2014-39)
**Verdict on disk:** PARTIAL (Coverage 7/10, Agreement 6/10) — see verdict-standardisation note in `REPORT.tex`.
**Original replication date:** 2026-06-22
**Backfill date:** 2026-07-06

## Pipeline

```
Fetch open-access surrogate      →  artifacts/belov2015_inis_iaea.pdf (JINR preprint, HTTP 200)
   ↓
Extract text (pdftotext -layout) →  artifacts/belov2015_inis_iaea.txt (1476 lines, 93 KB)
   ↓
Verify metadata (Europe PMC)      →  artifacts/epmc_meta.json (confirms PMID 25261728)
   ↓
Transcribe 22-ODE system + 46     →  scripts/smoke_belov2015.py (verbatim from Appendix A)
constants + 16-row Nir table      →  scripts/claim_audit.py::NIR_TABLE (verbatim from Table A.2)
   ↓
Forward-simulate 12 scenarios     →  results/smoke_results.json + results/smoke_traces.png
(WT + 4 KO × dose/LET grid)
   ↓
6-claim quantitative audit        →  results/claim_audit.json
+ α(L) sweep (80 LET points)     →  results/alpha_L_curve.{csv,png}
   ↓
Write REPORT.md (verdict PARTIAL)
```

## Tools & versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.13 | driver |
| numpy | ≥1.26 | array math |
| scipy | ≥1.11 (used `solve_ivp` LSODA) | stiff ODE integrator |
| matplotlib | ≥3.8 | plots |
| pdftotext (poppler-utils) | 24.x | text extraction |
| curl | 8.x | HTTP fetch of preprint + Europe PMC |
| bash / zsh | system | orchestration |
| CherryRd | Darwin 25.3.0 x86_64, single CPU | host |

**Free endpoints only** (Rick's standing rule). Argo localhost:44497 available for
LLM-in-loop tasks (report drafting only, not in the numerical simulation loop).

## Work estimate (honest, backward-look)

| Phase | Wall-clock |
|-------|-----------:|
| Paper fetch + text extraction | ~2 min |
| Appendix A/B transcription (22 ODEs + 46 constants) | ~90 min |
| Table A.2 transcription (16 rows × 5 columns) | ~15 min |
| Smoke driver debugging + LSODA switch | ~45 min |
| Claim-audit script (6 claims + Nir sweep) | ~30 min |
| Fig 11 reconstruction attempt (blocked on units + x14 clip) | ~60 min |
| REPORT.md drafting + honest gap enumeration | ~40 min |
| **Total** | **~5 hours** wall-clock, single operator |

Backfill (this pass): ~30 min (7 files, no re-simulation).

## Reproducer

From a clean shell on any Unix with Python 3.11+, numpy, scipy, matplotlib:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-belov-dsb-repair-pathways-slot66

# Full 22-ODE integration, 12 scenarios
python3 scripts/smoke_belov2015.py
# → results/smoke_results.json (~96 KB)
# → results/smoke_traces.png (~161 KB)

# 6-claim audit + α(L) sweep + 16-row Nir spot-check
python3 scripts/claim_audit.py
# → results/claim_audit.json (~5 KB)
# → results/alpha_L_curve.csv (~3 KB)
# → results/alpha_L_curve.png (~30 KB)
```

Expected wall-clock: <10 s per script on any modern CPU. No GPU, no LLM calls,
no network access needed at run time (only for original artefact fetch).

## Verification

- **α(L) at L=0.2 keV/µm:** 27.487 vs paper's 27.5 (C1 PASS)
- **α(L) LET-decay b:** 2.43×10⁻³ vs paper's 2.43×10⁻³ (C2 PASS)
- **Ku reservoir X1:** 9.190×10⁻⁷ M vs paper's 9.19×10⁻⁷ M (C3 PASS)
- **K10 Michaelis form:** 1.93×10⁻⁷/Nir M vs paper's 1.93×10⁻⁷/Nir M (C4 PASS)
- **All 16 Nir-table rows integrate cleanly:** 16/16 (C5 PASS)
- **Fig 11 ratios (ERCC1/XPF⁻:WT at 12/24/48 h):** degenerate ∞ vs paper's 2.2/2.5/2.9 (C6 FAIL)

## Non-reproducibility notes

- **Author code not deposited** (JINR LIT internal). Corresponding author dem@jinr.ru
  not contacted (offline-only protocol).
- **Table A.1 K1..K7 units inconsistent** with the source data the paper fits
  (~6–7 orders of magnitude off). Two independent hypotheses (units typo,
  non-dimensionalisation) both possible; cannot disambiguate without driver code.
- **γ-H2AX x14 non-negativity convention unstated** in the appendix; ODE as
  printed can drive x14 negative. Direct cause of C6 failure.
- **Experimental overlays not deposited** for Figs 3, 5, 7, 8, 9, 10, 11.
  Would need WebPlotDigitizer extraction to make figure-level comparisons.
- **Integrator substitution:** paper used RK4, replication used LSODA. Verified
  integrator-independent for α(L) and Nir-row checks; not formally tested for
  γ-H2AX curves.
