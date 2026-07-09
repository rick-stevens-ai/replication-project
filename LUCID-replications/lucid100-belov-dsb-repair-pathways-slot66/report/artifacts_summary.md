# Artifacts Summary

**Slot:** lucid100-belov-dsb-repair-pathways-slot66
**Paper:** Belov et al. 2015, JTB 366:115–130 (DOI 10.1016/j.jtbi.2014.09.024, PMID 25261728)
**Verdict on disk:** PARTIAL (Coverage 7/10, Agreement 6/10)
**Tracker verdict:** REPLICATED (this backfill preserves both; see verdict-standardisation note in `REPORT.tex`)

## Inventory

### Primary source

| File | Bytes | Origin | SHA-256 verified in `MANIFEST.json` |
|------|------:|--------|:-:|
| `artifacts/belov2015_inis_iaea.pdf` | 703,666 | JINR Communication E19-2014-39 (INIS/IAEA mirror), HTTP 200 fetch | ✓ |
| `artifacts/belov2015_inis_iaea.txt` | 93,029 | `pdftotext -layout` on above | ✓ |
| `artifacts/epmc_meta.json` | 8,400 | Europe PMC `/search?query=DOI:...` | ✓ |

### Simulation code (verbatim from Appendix A + Tables A.1 / A.2)

| File | ~Bytes | Contents |
|------|-------:|----------|
| `scripts/smoke_belov2015.py` | 15,085 | Full 22-ODE NHEJ+HR+SSA+γ-H2AX integrator. All 46 rate constants (K, K⁻, P, P⁻, Q, Q⁻) typed in at top; RHS built from Appendix A eq (1)–(22); LSODA integration via `scipy.integrate.solve_ivp`. |
| `scripts/claim_audit.py` | 10,300 | 6-claim quantitative audit driver + 16-row Nir-table sweep + 80-point α(L) curve + Fig 11 reconstruction attempt. |

### Simulation outputs

| File | ~Bytes | Contents |
|------|-------:|----------|
| `results/smoke_results.json` | 96,139 | 12 scenarios × full state traces (n0, x2..x14, y2..y12, z2..z8) at 200 timepoints each |
| `results/smoke_traces.png` | 161,044 | 2×2 panel plot: n0(t) / γ-H2AX x14(t), as-published vs binding-speedup hypothesis |
| `results/claim_audit.json` | ~5,000 | Per-claim verified/contradicted/not_reproducible verdicts + Fig 11 reconstruction attempt log |
| `results/alpha_L_curve.csv` | ~3,000 | α(L) over 80 LET points, 0.2–440 keV/µm |
| `results/alpha_L_curve.png` | ~30,000 | Fig 2 (α(L)) plot with 16 Nir-table LET markers |

### Reports

| File | ~Bytes | Contents |
|------|-------:|----------|
| `REPORT.md` | ~17,000 | Full original replication report, verdict PARTIAL |
| `FIRST_PASS_REPORT.md` | 5,559 | First-pass smoke results + original units-typo caveat |
| `README.md` | 4,894 | Folder description, layout, how-to-run |
| `MANIFEST.json` | 1,923 | SHA-256 ledger of original first-pass artefacts |

### This backfill (2026-07-06)

| File | ~Bytes | Contents |
|------|-------:|----------|
| `report/REPORT.tex` | 12,594 | LaTeX report with paper summary, claims table, method, results-vs-paper, honest critique, `\input{open_questions_section.tex}` at end |
| `report/open_questions.json` | 5,617 | 5 truly-open questions with basis + concrete next_steps |
| `report/open_questions_section.tex` | 6,338 | LaTeX mirror of open_questions.json |
| `report/workflow.md` | 4,398 | Pipeline, tools/versions, work estimate, reproducer |
| `report/artifacts_summary.md` | this file | Inventory of artifacts + traces + friction tags |
| `report/failure_analysis.md` | ~pending | Honest critique — gaps, residual uncertainty |
| `extraction/nougat.mmd` | ~pending | Stub with paper.pdf sha256 pointer (no GPU parse in this pass) |

## Traces (what was actually verified against paper)

| Claim | Type | Verified? | Trace file |
|-------|------|:---------:|------------|
| α(L) at L=0.2 keV/µm | scalar | ✓ | `results/alpha_L_curve.csv` (row 1) |
| α(L) LET-decay b | scalar | ✓ | `results/claim_audit.json::C2` |
| Ku reservoir X1 | scalar | ✓ | `results/claim_audit.json::C3` |
| K10 Michaelis form | functional | ✓ | `results/claim_audit.json::C4` |
| 16 Nir-table rows integrate | 16×boolean | ✓ | `results/claim_audit.json::C5` |
| Fig 11 ratios | 3×scalar | ✗ | `results/claim_audit.json::C6` (degenerate) |
| Fig 5–11 qualitative narrative | pattern | ✓ (qualitative) | `results/smoke_traces.png` |

## Friction tags

Standard LUCID-100 friction taxonomy applied:

| Tag | Present? | Notes |
|-----|:-------:|-------|
| `no-code-deposit` | ✓ | Authors' driver code not on GitHub / Zenodo / Figshare / Code Ocean. Only contact = dem@jinr.ru (not pinged, offline protocol). |
| `paywalled-primary` | ✓ | JTB version paywalled (`isOpenAccess=N`); replication used JINR E19-2014-39 open-access preprint (equations + tables identical). |
| `units-inconsistency` | ✓ | Table A.1 K1..K7 pseudo-first-order binding rates imply Ku→DSB half-time ≈ 4.6×10⁶ min vs 15–30 s in the source data the paper fits. 6–7 orders of magnitude off; units typo or non-dimensionalisation hypothesis both possible. |
| `unstated-convention` | ✓ | γ-H2AX state x14 has no non-negativity constraint in the appendix; ODE as printed can drive x14 negative. Figure-generation clip / scaling rule undocumented. Direct cause of C6 failure. |
| `experimental-overlays-missing` | ✓ | Figs 3, 5, 7, 8, 9, 10, 11 overlay model curves on cited experimental data; none of those CSVs are deposited. Bit-exact reproduction requires WebPlotDigitizer extraction of 6+ panels. |
| `no-identifiability-analysis` | ✓ | 46 rate constants fit to ~10 literature time-courses; no profile likelihood, Fisher information, or Sobol sensitivity in the paper. Practical unidentifiability nearly certain. |
| `structural-omissions` | ✓ | Alt-EJ / MMEJ absent (acknowledged in Discussion); no cell-cycle compartment; no coupling to chromosome-aberration formation. |
| `integrator-substitution` | ✓ | Paper: RK4. Replication: LSODA (stiffer-safe). α(L) + Nir-row checks verified integrator-independent; γ-H2AX curves not formally tested. |
| `no-author-contact` | ✓ | dem@jinr.ru not pinged (offline-only protocol). |
| `verdict-mismatch` | ✓ | On-disk REPORT.md = PARTIAL (7/10, 6/10). Tracker slot = REPLICATED. Backfill preserves both; scientifically honest call is PARTIAL. |

## Provenance chain

1. Europe PMC metadata query (`isOpenAccess=N` on Elsevier version) → JINR preprint chosen as surrogate.
2. JINR E19-2014-39 PDF fetched from INIS/IAEA mirror, SHA-256 logged in `MANIFEST.json`.
3. `pdftotext -layout` extraction → text used for equation + table transcription.
4. Appendix A eq (1)–(22) transcribed verbatim into `scripts/smoke_belov2015.py`.
5. Table A.1 (46 rate constants) transcribed verbatim into the same script.
6. Table A.2 (16 Nir rows) transcribed verbatim into `scripts/claim_audit.py::NIR_TABLE`.
7. Forward-simulation → 12 scenarios, all state traces logged.
8. 6-claim audit → 5/6 PASS, 1/6 FAIL (C6 blocked on units + x14 clip).
9. Verdict: PARTIAL (Coverage 7/10, Agreement 6/10) with explicit blocker enumeration.
