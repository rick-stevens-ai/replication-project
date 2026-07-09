# Workflow — s100-026

Paper: Klapproth et al. 2021, *Cancer Nanotechnology* 12:27, DOI 10.1186/s12645-021-00099-3.

## Stages executed

1. **Source acquisition.** Paper PDF pulled to `source/paper.pdf`. OCR/text via
   `pdftotext` (layout mode) to `ocr/paper.txt` (878 lines). Paper is open-access
   Springer, no paywall.
2. **Claim extraction.** REPORT.md §2 lists 3 claim clusters:
   (a) Table 3 chemical-species enhancement ratio matrix (6 species × 2 kVp × 3 depths),
   (b) qualitative dose/SB/DSB trends and indirect ≈ 2× direct SB,
   (c) numerical audit parameters (17.5 eV threshold, 40% OH→SB, 1.0 ns chemistry,
   10-bp DSB window, 0.225 wt% AuFeNP loading).
3. **Reproduction attempt.** Full MC pipeline ruled out (TOPAS + Geant4 + TOPAS-nBio +
   custom mouse-DNA voxel model; multi-week cluster job on GPU cluster). Substituted:
   a Python-only arithmetic + geometry audit in `code/reproduce_table3_and_audit.py`.
   The audit
   (i) re-encodes Table 3 and recomputes per-species min/max/mean and sign,
   (ii) recomputes the wt% claim from stated NP geometry and densities under 6
   denominator interpretations,
   (iii) uses OH/H mean ratio as a proxy for indirect:direct SB ordering.
4. **Result capture.** Machine-readable output at `evidence/spot_check.json`. Human
   summary in `report/REPORT.md`.
5. **Backfill (2026-07-05).** Added REPORT.tex, open_questions.json, open_questions_section.tex,
   workflow.md (this file), artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd
   stub. Verdict cross-check flagged queue label "REPLICATED" as over-optimistic; on-disk
   evidence supports PARTIAL / SPOT-CHECK.

## Tools and endpoints

- Python 3 (stdlib only) for the audit script.
- `pdftotext` for OCR.
- No LLM API calls; no external simulation endpoints. Free-endpoint policy satisfied
  by construction (no engine was run).

## What was NOT done

- No TOPAS/Geant4/TOPAS-nBio run. No mouse-DNA voxel geometry compiled. No AuFeNP
  cloud generated. No SDD file produced. No SSB/DSB time series regenerated.
- No author contact (no GitHub issue opened, no email sent). The open questions are
  candidates for such contact, not evidence of it.
- No compute-cluster booking. Full pipeline would belong on uicgpu / Polaris / ALCF Sophia,
  not on the OpenClaw workstation fleet.

## Reproducibility of the reproduction

The audit script is deterministic and dependency-free: `python3 reproduce_table3_and_audit.py`
regenerates `spot_check.json` byte-identically. Re-runners can re-derive our audit
verdict without any of the paper's engine machinery.
