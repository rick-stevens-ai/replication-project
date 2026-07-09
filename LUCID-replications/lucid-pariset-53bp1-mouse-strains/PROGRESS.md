# PROGRESS - LUCID Pariset/Penninckx 53BP1 Mouse Strains Replication

**Status:** done
**Started:** 2026-05-30 18:01 CDT
**Finished:** 2026-05-30 18:10 CDT
**Paper:** Pariset/Penninckx et al. 2020, Radiat Res 194:485-499, DOI 10.1667/RADE-20-00122.1
**Verdict:** PARTIAL (analytical core replicated, wet-lab and in-vivo data not deposited)

## Log
- 18:01 - workspace created, JSON status=running
- 18:02 - PDF triage: paper text + tables extracted (`pdftotext -layout`)
- 18:03 - PDF too large for the `pdf` tool (12 MB > 10 MB cap); pivoted to direct text extraction + per-page image OCR
- 18:04 - identified that Fig 4 (per-strain τ, ρ) is on PDF page 10 (journal page 493), and the data are bar charts not a scatter
- 18:05 - vision-digitized 15-strain τ and ρ values from Fig 4 panels A and B
- 18:06 - searched for supplementary data: none deposited (no Table S, no Fig S, no GitHub/Zenodo/figshare); confirmed
- 18:07 - vision-digitized Fig 7C cancer correlation values (19/27 organs readable)
- 18:08 - wrote `code/replicate_pariset.py` implementing all 5 model equations
- 18:09 - ran replication: paper's headline correlation r(τ_4Gy, q_4Gy) = -0.75 reproduced as r = -0.758 (p = 0.0011) — essentially exact match
- 18:09 - identifiability check passed: 200-trial Monte Carlo recovers (τ, q, RIFmax) within 10-20% with 10% noise
- 18:10 - wrote REPORT.md and README.md
- 18:10 - status=done

## Key result (orig pass)
Paper Table 1B: r(τ at 4 Gy X-ray, q at 4 Gy X-ray) = -0.75 across 15 strains.
This replication, from vision-digitized Fig 4 bar charts: r = -0.758, p = 0.0011.
This is the strongest available numerical validation, and it agrees to within 1% of the paper's reported value, confirming that the digitization and the paper's statistical analysis are internally consistent.

## Re-pass 2026-06-23
- Status: done (coverage lift)
- Goal: raise Coverage from 6/10 toward >=8 by attempting previously-skipped claims.
- Parser: pdftotext -layout (Marker output absent for DOI 10.1667/RADE-20-00122.1 in marker_md_uicgpu_20260622/merged/); recorded in PARSER_PROVENANCE.md.
- New claims attempted and verified: C (LET ratio MATCH), D (Eq. 3 prefactor EXACT), E (sublinear dose-response CONSISTENT), F (Table 2 quadrant placement 11/15 = 73% STRONG MATCH), G (Fig. 7C n=4 critical |r|=0.95 — paper overreaches inferentially), H (Fig. 7C positives 13/19 = 68% MATCH), J (forward sim of Eq. 5/6 — 15/15 monotone, residual band overlaps Fig. 3B), K (Table 1B with second estimator Spearman -0.672 confirms Pearson -0.758).
- New honest data-blocks named: I (Fig. 7B raw B-cell counts not deposited; statistical ceiling p_two-sided ≈ 0.061 at r=0.61, n=10) and L (Table 1A per-particle, per-strain (τ, q, RIFmax) inputs not deposited — Fig. 4 shows combined HZE only).
- Regression: all four prior-pass correlations identical to 3 dp.
- New scores: Coverage 8/10 (up from 6/10), Agreement 8/10 (held).
- 4-tier verdict: PARTIAL.
- Original REPORT preserved as REPORT.pass1.md.
