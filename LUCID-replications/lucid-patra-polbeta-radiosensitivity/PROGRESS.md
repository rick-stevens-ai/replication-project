# PROGRESS — LUCID replication: Patra et al. PA1 / PolβΔ radiosensitivity

- **Status:** COMPLETE
- **Started:** 2026-05-30 18:07 CDT
- **Finished:** 2026-05-30 18:25 CDT (~18 min single session)
- **Target:** Patra et al., Radiat Oncol J 2022;40(1):66-78. DOI 10.3857/roj.2021.00689
- **Source PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/aa68c63a2b171934b37881b6dd1b4ff17bb85a2b.pdf`
- **Verdict:** **PARTIAL** (coverage 5/10, agreement 7/10, internal-consistency 4/10)

## Timeline / log

- **18:07** dirs created; progress JSON `status=running` written within 10-min gate.
- **18:08** pdftotext extracted full text (66 kB, 712 lines); identified reproducible computational targets:
  - Supplementary Table S1 nucleotide sequences (translatable in silico)
  - Supplementary Table S2 ClusPro scores (numeric)
  - HDOCK protein-DNA scores in Results section (numeric)
  - Fig. 2 colony-forming dose-response (digitizable for LQ refit)
- **18:09** downloaded all 4 supplementary files from e-roj.org (no auth, no paywall).
- **18:11** wrote `code/01_sequence_check.py` — Biopython translation + global pairwise alignment of WT vs ΔPolβ cDNA from Suppl Table S1.
- **18:12** ran 01: **major finding** — published ΔPolβ cDNA does NOT match the paper's textual claim of "97-aa in-frame deletion at residues 208–304". Actual: 413-nt frameshift deletion between codons 121–257; product is 198 aa with ≥6 premature stop codons. Verified all 22 paper-cited WT residue numbers match canonical Polβ (P06746, 335 aa).
- **18:13** rendered key pages, digitized Fig. 2 plating-efficiency plot (two independent visual reads).
- **18:14** wrote `code/02_lq_fit.py` — weighted LQ fit of SF = exp(-αD - βD²) for both lines.
- **18:15** ran 02: **WT** α=0.045/Gy, β=0.0047/Gy², D10=17.8 Gy. **Δ** α=0.009/Gy, β=0.028/Gy², D10=8.85 Gy. **DMF=1.80 at 10 Gy**. Confirms paper's central claim.
- **18:17** wrote `code/03_quantitative_audit.py` — tabulated every numeric assertion (ROS, cell-cycle, apoptosis, docking) and ran consistency checks.
- **18:18** ran 03: flagged **ROS non-monotonicity** (10 Gy < 5 Gy in mutant), **WT > Δ at 10 Gy in ROS** (opposite of BER-failure hypothesis), 2× baseline G2/M difference, 3 different stated deletion ranges in the paper text, **kcal/mol unit error** on both ClusPro and HDOCK scores.
- **18:20** wrote REPORT.md, README.md (this file).
- **18:25** finalised; progress JSON `status=complete`.

## Decisions logged

- **Did NOT re-run ClusPro / HDOCK.** Public-server queues would cost hours-to-days for 13 separate jobs; AUP forbids parallelism; the numerical output is in arbitrary units that the paper itself mislabels — re-running cannot resolve the underlying issues. Spot-check via inputs (sequences, PDB IDs) and units is more informative per unit time.
- **Did NOT contact authors** (hard gate #2).
- **Did NOT wet-replicate cell experiments** — out of scope for LUCID computational triage and no raw data exists publicly.
- Visual digitization of Fig. 2 cross-checked by two independent vision-model passes; values used for LQ fit are midpoints with conservative SD; results note this is digitization-based not raw.
- Did not attempt to fix the broken ΔPolβ cDNA by guessing an "intended" sequence — the paper is internally inconsistent (3 different deletion ranges) so any reconstruction would be speculation.

## Deliverables (under outdir)

- `REPORT.md` (full write-up, ~12 kB)
- `README.md`
- `PROGRESS.md` (this file)
- `code/01_sequence_check.py`, `02_lq_fit.py`, `03_quantitative_audit.py`
- `data/paper.pdf` + 4 supplementary PDFs + text extractions
- `results/sequence_check.json`, `alignment.txt`, `wt_protein.fasta`, `del_protein.fasta`, `wt_nt.fasta`, `del_nt.fasta`, `lq_fit.json`, `quant_audit.{json,txt}`
- `figures/fig2_replication.png` + raw page renders
