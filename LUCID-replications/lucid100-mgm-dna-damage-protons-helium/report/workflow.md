# Workflow — LUCID-100 slot: `lucid100-mgm-dna-damage-protons-helium`

Reproduction workflow for the on-disk replication of Onecha et al.
(Phys Med Biol 70(20), 2025) — MGM extension for proton + helium DNA damage.

## 0. Prerequisites

- Python 3.10+ with `numpy`, `scipy`, `matplotlib`.
- No TOPAS / TOPAS-nBio required (the extension code is unavailable and
  the replication deliberately does NOT re-run any Monte-Carlo transport).
- Sibling BNCT slot must be present at
  `../lucid100-bnct-dna-damage-repair-model/` for P1–P3 LET anchors.

```bash
python3 -m pip install --user numpy scipy matplotlib
```

## 1. Fetch source artifacts (already staged; commands documented for reproducibility)

- Paper PDF: EuropePMC `PMC12905799?pdf=render` → `artifacts/paper.pdf`
  (SHA-256 `3a7c1cad4b590eedd0be983fabbee00213fe4a743fa7be50c68b90c142d2c476`).
- Paper text: `pdftotext artifacts/paper.pdf artifacts/paper.txt`.
- MGM analytical engine (public, MIT):
  `git clone https://github.com/MGHPhysicsResearch/MGM artifacts/mgm-repo`.
- Bertolet 2023 theory paper (open, CC-BY): `artifacts/mgm2023.pdf`.
- Sibling BNCT slot's Geant4-DNA LET tables:
  `../lucid100-bnct-dna-damage-repair-model/artifacts/medras_analytic/Data/TrackData/{Proton,Helium}/`
  (19 proton files, 10 helium files).

## 2. Run analytical replication

```bash
cd lucid100-mgm-dna-damage-protons-helium
python3 scripts/smoke_mgm.py            # first-pass smoke: 5 anchors
python3 scripts/extended_audit.py       # SPOT-CHECK claims C1..C9 (E1..E5)
python3 scripts/promotion_audit.py      # PROMOTION checks P1..P5
```

## 3. Inspect outputs

```bash
cat scripts/smoke_results.json          # smoke numbers
cat results/extended_results.json       # SPOT-CHECK numbers
cat results/promotion_results.json      # PROMOTION numbers
ls results/plots/                       # PNG plots for P2, P3, P4
```

Expected plots:

- `results/plots/P2_full_sweep.png` — MDS/Gy/Gbp and mean complexity vs
  LET, protons + helium.
- `results/plots/P3_he_over_p_ratio.png` — MGM He/p MDS-per-dose ratio at
  matched LET (~1.0 at LET ≤ 35 keV/μm, documents MGM LIMIT).
- `results/plots/P4_yF_spectrum_norm.png` — spectrum-averaged 20 MeV p
  MDS across 4 log-normal σ, 4 tail fractions (all 9.4–11.6, none
  reaches paper's 30).

## 4. Verdict logic

`promotion_audit.py` writes single-line `PROMO_RESULT.txt` with:

```
VERDICT=<PARTIAL|REPLICATED> COVERAGE=<n>/10 AGREEMENT=<m>/10
```

On-disk actual line: `VERDICT=PARTIAL COVERAGE=4/10 AGREEMENT=7/10`.

## 5. Explicit non-steps (what this workflow does NOT do)

- Does NOT install or run TOPAS or TOPAS-nBio.
- Does NOT re-derive TOPAS-nBio Geant4-DNA option-2 yF spectra.
- Does NOT reproduce Figure 4 per-cell histograms, Figure 5 FWHM scan,
  Figure 6 Bragg-peak depth scan, Figure 7 RPT histograms, or Table 1
  timing benchmark (all require the unreleased TOPAS-MGM C++ extension).
- Does NOT retrieve the PMC supplementary material (reCAPTCHA-gated).
- Does NOT start any long-running MC jobs on any host (CherryRd is
  disallowed for heavy MC per project policy).

## 6. Provenance and mesh conventions

- Replication host: CherryRd (analytical only, no MC).
- Language: Python 3 (numpy/scipy).
- LLM assistance: gpt-oss / Claude Opus (Argo, free tier) for structural
  editing only; no numerical values were LLM-generated.
- Endpoints: free only (Argo, CELS free tier, Sophia). No paid endpoint
  was used per project rule.

## 7. Backfill notes (2026-07-06)

- 7 documentation artifacts added under `report/` and `extraction/` to
  meet the 8-artifact standard: REPORT.tex, open_questions.json (5-item
  bare list), open_questions_section.tex, workflow.md,
  artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub.
- No numerical values were re-derived; all figures come from the
  existing `REPORT.md`, `results/`, and `scripts/` files. Backfill did
  NOT re-run any code.
- **Verdict mismatch flagged**: queue label REPLICATED, on-disk actual
  PARTIAL. On-disk verdict preserved as authoritative; see
  `failure_analysis.md`.
