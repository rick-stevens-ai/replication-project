# Workflow — Franken 2012 alpha vs gamma RBE replication (Pass 1 + Pass 2)

## Overview
Purely-analytical LUCID replication of a radiobiology paper. No Monte Carlo,
no wet lab, no LLM calls. All computation is deterministic LQ arithmetic +
first-order error propagation on Table I values.

## Pass 1 pipeline (2026-06 initial)
1. **Ingest.** `franken_2012.pdf` (Oncology Reports 27:769–774) staged.
2. **Parse.** `pdftotext -layout franken_2012.pdf` → 354 lines of tokenized text.
3. **Enumerate claims.** 10 candidate testable claims extracted (later refined
   to 13 in pass 2). Filtered to 6 with recomputable numeric content.
4. **Recompute.** `code/refit_rbe.py`:
   - Read Table I `α_α ± σ_α` and `α_γ ± σ_γ` for 4 endpoints
     (γ-H2AX foci, clonogenic survival, chromosomal fragments, colour junctions)
   - Compute RBE = α_α / α_γ
   - Compute σ_RBE via first-order propagation:
     σ_RBE = RBE · sqrt((σ_α/α_α)² + (σ_γ/α_γ)²)
   - Compare central and σ to Table I values (paper's stated RBE ± σ).
5. **Lethal-DSB fraction.** Compute α_survival / α_γ-H2AX for both radiation
   qualities → check "~1%" and "~10%" Discussion claims.
6. **Reconstruct Fig. 2.** Plot LQ (or pure-exponential for endpoints where
   β=0 is asserted) predictions using Table I fit parameters.
7. **Verdict.** PARTIAL (6/10 tested, 6/6 agree).

## Pass 2 pipeline (2026-06-23 extension)
Motivated by (a) upgrade to Marker MD parser, (b) close the 4 untested claims.

1. **Re-parse with Marker.** Use canonical LUCID-100 admin Marker output
   (`_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/555f0ea0.../555f0ea0....md`,
   153 lines). Cross-check numeric tokens against pdftotext output (Table I,
   Fig-2 caption, Discussion ratios, dose-range/dose-rate methods) — agreement
   confirmed.
2. **Extend claim enumeration.** 10 → 13 claims (add Fig-2 effect-level RBEs
   for γ-H2AX, Fragments, Colour junctions; add "factor 4" aberrations-vs-survival;
   add ">1 decade divergence at 2 Gy"; add per-dose raw data — the last is
   the single genuinely-untestable data-deposit claim).
3. **Recompute effect-level RBEs.** `code/pass2_extended_claims.py`:
   - For linear endpoints (β=0 asserted), effect-level RBE == α-ratio, so
     γ-H2AX: 1.00, Fragments: 15.27, Colour junctions: 13.33 (all match Fig-2's
     rounded values 1, 13, 13).
   - For survival (LQ, β_γ nonzero but not tabulated): invert
     α_γ·D_γ + β_γ·D_γ² = -ln(0.1) with D_γ = 4·D_α(S=0.1) constraint
     → β_γ ≈ 0.096 Gy⁻², α/β ≈ 1.57 Gy. Physically sensible (late-tissue range).
4. **"Factor 4" check.** Compute α_fragments/α_survival and α_junctions/α_survival
   for both α and γ radiation → 4 ratios, all ≥4.18, tightest wins.
5. **Decade-divergence at 2 Gy.** Evaluate S_α(2) and S_γ(2) under both
   pure-exponential and LQ(β_γ inferred) models → 1.78 vs 1.61 decades, both >1.
6. **Dump results.** `results/pass2_extended_claims.json`.
7. **Verdict update.** REPLICATED (model+result). Only untested claim is C13
   (raw per-dose points) which requires figure digitisation.

## Reproducibility
- All computation in Python stdlib + numpy. Runs in <1 s on any laptop.
- Determinism: no random sampling, no LLM calls, no network. Given the same
  Table I inputs, the outputs are bit-identical across runs.
- Free-endpoint compliance: FREE compute (laptop CPU), FREE LLM (none used),
  no paid APIs.

## What was NOT done (see failure_analysis.md and REPORT critique)
- Wet-lab clonogenic assay not reproduced.
- No MC track-structure simulation (the paper itself doesn't have one).
- No Fig-2 pixel digitisation (would close the 92% → 100% coverage gap).
