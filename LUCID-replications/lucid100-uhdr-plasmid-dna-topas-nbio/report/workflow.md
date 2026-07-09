# Workflow: LUCID-100 UHDR + Plasmid DNA + TOPAS-nBio Replication

**Slot:** `lucid100-uhdr-plasmid-dna-topas-nbio`
**Paper:** Masilela et al., Phys. Med. Biol. 71 (2026) 095013 (DOI 10.1088/1361-6560/ae62c6, CC-BY 4.0)
**Executed:** 2026-06-09 (first pass), 2026-06-22 (deep audit), 2026-07-06 (backfill)
**Actual verdict on disk:** SPOT-CHECK (analytic), Coverage 4/10, Agreement 9/10

## 1. Discovery
- Slot assigned via LUCID-100 Wave 5 (rank 79, tier A, priority 14).
- Confirmed OA status via Unpaywall (`is_oa: true`, CC-BY hybrid, publisher OA location).

## 2. Metadata harvest (all free endpoints)
- Crossref → `artifacts/crossref.json` (refs count, funding, license).
- Semantic Scholar (S2 key from macOS Keychain `semantic-scholar-api-key`) → `artifacts/semanticscholar.json`.
- OpenAlex → `artifacts/openalex.json`.
- Unpaywall → `artifacts/unpaywall.json`; also `unpaywall_dkondo2021.json`, `unpaywall_dkondo2024.json` for precursor chemistry parameters.
- NCBI esummary (PMID 42013902) → `artifacts/ae62c6_esummary.json`.
- EuropePMC → `artifacts/ae62c6_epmc.xml` (empty; not in EPMC fulltext).

## 3. Full-text acquisition
- Paper PDF fetched from IOPscience via Unpaywall OA URL → `artifacts/paper.pdf` (2.0 MB, 15 pp).
- `pdftotext -layout` → `artifacts/paper.txt` (1116 lines).
- SHA-256 ledgered in `artifacts/SHA256SUMS.txt`.

## 4. Analytic re-derivation (pure Python)
- Extracted 43-reaction chemistry table verbatim → `scripts/chemistry_table1.csv`.
- Implemented Eq. (4) `k_obs = 1.32e7 * σ^0.29` with branching efficiencies η_OH=0.24, η_H=0.008 → `scripts/smoke_scavenging_capacity.py`.
- Implemented DSB pair-acceptance Poisson-position MC (200,000 iters, seed 1234) for bp-threshold monotonicity → `scripts/smoke_dsb_audit.py`.
- Compute cost: <30 s single-core CPU on CherryRd. No GPU. No HPC. No paid endpoints. No author contact.

## 5. Claim audit
- Cross-checked 26 quantitative headline claims from Abstract + §3.1 + §3.2 + Table 2.
- 18 tested; 17 within tolerance (<1% or paper's stated rounding).
- 2 apparent paper-side text errata flagged (claim 12: probable missing exponent on DSB(UHDR) at 1e-3 M DMSO; claim 24: Eq. 3 algebra inconsistency in oxygen Henry's-law derivation — value used is correct, printed derivation is off by ~5 orders of magnitude).

## 6. Figures reproduced (analytic shape only)
- `figures/smoke_ssb_vs_sigma.png` — SSB shape vs paper, normalized.
- `figures/smoke_intertrack_vs_oh_lifetime.png` — Fig. 4 reproducer.
- `figures/smoke_dsb_ratio_vs_sigma.png` — DSB UHDR/CONV vs σ.
- `figures/smoke_dsb_bp_sensitivity.png` — bp-threshold sensitivity.

## 7. Documentation
- `REPORT.md` (top-level, 18.5 KB) — full narrative + 26-row claim table.
- `report/REPORT.tex` — condensed audit for cross-set indexing.
- `report/failure_analysis.md` — honest critique.
- `report/open_questions.json` + `open_questions_section.tex` — 5 open questions.
- `notes/HPC_JOB_PLAN.md` — concrete plan for full MC rerun on Aurora/uicgpu when TOPAS-nBio chemistry decks release.
- `notes/REPRODUCIBILITY_SCORECARD.md` — 3.6/5 roll-up.

## 8. What was NOT done (see failure_analysis.md)
- No TOPAS-nBio Monte Carlo simulation was run.
- No independent absolute G-value derivation (all absolute numbers are read-through from the paper).
- No cross-code comparison against Geant4-DNA or PARTRAC.
- No chromatin-scale extrapolation.
- No author contact; no chemistry-deck acquisition (both author GitHub profiles empty).

## 9. Blockers to full replication
1. TOPAS-nBio v4.0 dev branch with ELSEPA + Meesungnoen patches not publicly tagged.
2. Models 1 & 2 `TsChemistry` `.topas` decks + Python DSB post-processor not released.
3. ~5k CPU-h per condition / ~0.5-1M CPU-h for full 16-cell matrix on Aurora-class hardware.

## 10. Recommended follow-up
- Heartbeat-monitor `topas-nbio/TOPAS-nBio-v2.0` releases.
- When chemistry deck lands, escalate per `notes/HPC_JOB_PLAN.md` (Aurora UAN preferred; uicgpu 8×A100 acceptable for reduced-matrix run).
- Optional: contact Ramos-Méndez re: chromatin-scale geometry extension (open question #1).
