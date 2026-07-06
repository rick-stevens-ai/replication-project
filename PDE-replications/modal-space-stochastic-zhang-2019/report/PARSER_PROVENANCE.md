# PARSER_PROVENANCE — Zhang et al. 2019 (Modal-Space SPDE)

**Date:** 2026-06-23 (re-pass)
**Operator:** Ollie (re-pass subagent)
**Paper PDF:** `paper/zhang2019_modal_space_spde.pdf`
**Citation:** D. Zhang, L. Guo, G.E. Karniadakis, "Learning in Modal Space:
Solving Time-Dependent Stochastic PDEs Using Physics-Informed Neural Networks",
SIAM J. Sci. Comput. 42(2):A639–A665 (2020), doi:10.1137/19M1260141. arXiv:1905.01205v2.

## Parser used
1. **Primary parser:** `pdftotext -layout` (Poppler, `/usr/local/bin/pdftotext`),
   producing `tmp_zhang/zhang.txt` (1560 lines). All claim numbers in this re-pass
   were extracted from the layout-preserved text file. Cross-checked by `grep`/`sed`
   region inspection (e.g., lines 950–990 for Table 1, 1170–1230 for Tables 3–4,
   1320–1410 for Tables 5–6).
2. **Secondary verification:** none required — pdftotext reproduced tables with
   correct ordering and numerical values matched both v1 REPORT.md and v2 REPORT_v2.md
   extractions (Tables 1–6).
3. **PDF-vision tools:** unavailable in this environment (Anthropic credit, gemini
   model name, openai PDF extraction all failed); not needed because pdftotext was
   sufficient for the tabular claims.

## Claim enumeration policy
Every quantitative item that a replicator can compare against was extracted, including
- All Table 1–6 numbers (16 per-component values + 8 statistical-error values).
- Stated KL truncation / energy threshold (19 modes capture ≥98% energy).
- Stated network architectures and training hyperparameters (per example).
- Stated qualitative claims with concrete witnesses (eigenvalue crossings,
  gPC vs NN-BO variance ranking, inverse a/b convergence).
- Stated MC reference sample sizes (1000 for Burgers/RD reference).
- Stated time/space/random-input dimensions.

## What was excluded
- Abstract/intro motivational claims with no numerical hook.
- Theorem statements (Th 3.1, 3.2) reproduced from cited references [15], [17].
- Plots without table backing (qualitative agreement only).

## v1/v2 claim-table provenance audit (errors found while re-parsing)
- v1 REPORT.md mis-listed Burgers errors as "Table 3 values" without
  per-component checks — confirmed correct against pdftotext.
- v2 REPORT_v2.md did not enumerate Tables 3, 4, 5, 6 per-component values
  — only the E[u]/Var[u] statistics. This is one source of the cov=7
  rating: the per-component (u_i, a_i, Y_i) claims were never tested
  in either pass.
- **Setup-mismatch bugs found in v2 implementation** (see REPORT.md §
  "Agreement-gap diagnosis"): paper Ex1 uses ξ~N(0, 0.8²) on x∈[−π,π];
  v2 code uses ξ~N(1.0, 0.5²) on x∈[0, 2π]. Paper Ex3 forward uses
  a=0.1, b=0.5, PDE u_t = a·u_xx + b·u² + (1−x²)g(x;ω) with σ_g=1, l_c=0.1,
  19 KL modes; v2 code uses a=0.5, b=0.3, PDE u_t = a·u_xx + b·u(1−u)
  (logistic, no forcing) with σ_KL=0.1, 6 KL modes on x∈[0,1].
- Per-component values were not enumerated in REPORT_v2.md, so the
  "PARTIAL/agreement=5" score in the pipeline reflected only the
  aggregate E[u]/Var[u] statistic claims, not the full per-component
  table.

## Files
- Source PDF (working copy): `/Users/stevens/.openclaw/workspace/tmp_zhang/zhang2019_modal_space_spde.pdf`
- Plain text: `/Users/stevens/.openclaw/workspace/tmp_zhang/zhang.txt`
- Original paper preserved: `paper/zhang2019_modal_space_spde.pdf` (unchanged)
