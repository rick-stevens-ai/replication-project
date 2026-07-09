# Artifacts Summary — Taleei & Nikjoo 2013 Biochemical DSB Repair (Pass 2)

## Inventory

### Reports
- `REPORT.md` — Pass 2 canonical narrative (12,286 B, 2026-06-23)
- `REPORT.pass1.md` — Pass 1 preserved (8,730 B)
- `report/REPORT.tex` — Pass-2 LaTeX (this backfill, 2026-07-06)
- `report/open_questions.json` — 5 truly-open questions (this backfill)
- `report/open_questions_section.tex` — LaTeX \input mirror (this backfill)
- `report/workflow.md` — pipeline / tools / reproducer (this backfill)
- `report/artifacts_summary.md` — this file (this backfill)
- `report/failure_analysis.md` — honest critique (this backfill)

### Code
- `code/taleei_nikjoo_2013_repair.py` — Pass-1 9-compartment ODE
- `code/repass/taleei_nikjoo_2013_repass.py` — Pass-2 12-compartment ODE (adds heterochromatin, C5–C10 machinery)

### Results (Pass 2)
- `results/repass/c5_artemis_kinetics.csv` — WT vs KO time course (Artemis)
- `results/repass/c6_let_dependence.csv` — t_{1/2}, complex-fraction, 24h residual vs LET (6 rows)
- `results/repass/c7_data_fit.csv` — model vs digitised experimental foci trajectories
- `results/repass/c7_data_fit_chi2.json` — χ²/dof for 3 datasets (2Gyγ WT, 4Gyγ WT, 2Gy X-ray CJ179)
- `results/repass/c8_heterochromatin_kinetics.csv` — 12-compartment het output
- `results/repass/c10_sensitivity.csv` — 3×3 grid, ±30% k_proc_c × ±30% k_lig_c
- `results/repass/summary.json` — machine-readable Pass-2 verdict roll-up

### Results (Pass 1 legacy)
- `results/repair_kinetics.csv` — Pass-1 total-DSB trajectory
- `results/comparison_check.json` — Pass-1 pass-gates

### Figures
- `figures/repass/repass_overview.png` — 2×3 panel: WT vs KO / LET sweep / het split / χ² data-vs-model / sensitivity heatmap / mass conservation trace

### Evidence
- `evidence/europepmc.json` — core EuropePMC record
- `evidence/europepmc_full.json` — full-text metadata payload
- `evidence/companion-papers/belov2015_inis_iaea_E19-2014-39.pdf` — Belov 2015 IAEA INIS preprint (Table A.1 + Table A.2 source)
- `evidence/companion-papers/belov2015_extracted_text.txt` — `pdftotext` extraction

### Provenance / Meta
- `PARSER_PROVENANCE.md` — names the exact missing artifact (paywalled Table 1 of Taleei-Nikjoo 2013b)
- `PROGRESS.md` — session log
- `artifact_harvest.md` — original harvest notes
- `attempt_log.md` — early attempts
- `brief.md` — initial brief

### Extraction stubs (backfill)
- `extraction/nougat.mmd` — parser stub with paper.pdf sha256 pointer (this backfill)

## Traces

### Compute traces
- All Pass-2 sims: `results/repass/*.csv/*.json` are the numeric ground truth; each row/entry maps to one gate in REPORT.md.
- Wall time: ~1.5 s total across all 6 Pass-2 claims (single Apple-Silicon core).
- No cluster jobs, no PBS/Slurm logs — everything runs on CherryRd.

### Provenance traces
- `PARSER_PROVENANCE.md` documents:
  - Elsevier paywall 403 + Cloudflare 1020 on companion routes.
  - Belov 2015 substitution rationale (Table A.1 → K1..K12 rate constants; Table A.2 → LET-dependent N_ir).
  - Sibling replication reference `lucid100-belov-dsb-repair-pathways-slot66`.
- Nothing was silently re-fit; C7c Artemis-KO χ²/dof = 3.63 is reported as-is.

### Data traces
- Digitised experimental data: pinned to `../lucid-slow-fast-nhej/code/experimental_data.py` (Qi et al. 2021 Figs 3a/3b/7a).
- All 3 datasets used in C7 are named with paper citations in REPORT.md.

## Friction Tags

| Tag | Description | Impact |
|---|---|---|
| `paywall-elsevier` | Paper PDF body inaccessible via S2/EuropePMC/direct DOI | HIGH — forces one-step-removed rate constants from Belov 2015 rather than paper's own Table 1 |
| `companion-cloudflare-1020` | Companion 2013a paper (Rad. Res. RR3123) blocked by Cloudflare/WAF | MEDIUM — cross-check attenuated |
| `no-gpu-parse` | No nougat/marker GPU parse of the paper PDF (nothing to parse — no PDF body) | HIGH — extraction stub is a placeholder |
| `single-species-fit` | Belov 2015 Table A.1 fits pooled data across human/CHO/mouse | MEDIUM — species-specific constants unknown; see Q4 |
| `no-checkpoint-model` | Mass-action ODE has no ATM/ATR/CHK feedback | MEDIUM — scope choice, but Q3 flags it |
| `no-early-S-run` | Only G1 configuration was actually simulated | MEDIUM — paper title advertises G1+S; only G1 verified in numbers (Q1) |
| `artemis-ko-chi2-fail` | Only failed pass-gate: C7c χ²/dof=3.63 | LOW-MEDIUM — honestly reported, structural not fudged (Q2 gives concrete probe) |
| `linear-let-model` | f_complex(LET) linear+saturating fit to Belov Table A.2 | LOW — first-order OK, but scatter not propagated |
| `no-author-contact` | Karolinska group not contacted for Table 1 | LOW — respects Rick's free-endpoint rule |

## What is NOT in this replication

- The paper's own Table 1 rate constants (paywalled, one-step-removed via Belov 2015).
- Early-S kinetic runs with resection→HR competition.
- Checkpoint-feedback dynamics (ATM/ATR/CHK1/CHK2).
- Species-specific rate-constant fits.
- Cancer-cell-line extensions (p53-null, ATM-null, BRCA1-hypomorph).
- XLF / DNA-PKcs / Lig4 knockout scans (Belov 2015 lists these but Pass-2 ran only Artemis-KO).
- A nougat/marker MMD extraction of the paper (there is nothing to extract without the PDF body).

Each of the above is addressed by exactly one of the 5 open questions.
