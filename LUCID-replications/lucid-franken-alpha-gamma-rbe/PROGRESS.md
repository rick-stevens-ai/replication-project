# PROGRESS — Franken et al. α vs γ RBE replication

**Status:** done (pass 2)
**Verdict:** REPLICATED (model-level), PARTIAL (data-level)
**Coverage:** 12 / 13 testable claims (was 6 / 10 in pass 1)
**Agreement:** 12 / 12 on what was recomputed (was 10 / 10 in pass 1)
**Started:** 2026-05-30 18:01 CDT (pass 1)
**Pass 2 added:** 2026-06-23 12:15 CDT
**Target:** Franken et al., *Oncology Reports* 27: 769-774, 2012
(DOI 10.3892/or.2011.1604).

## Pass 1 (preserved at PROGRESS.pass1.md, REPORT.pass1.md)
- Parser: pdftotext (Anthropic/Gemini PDF endpoints 400'd on this file).
- Reproduced four Table-I RBE values + σ + two Discussion ratios.
- Coverage 6/10, agreement 10/10. PARTIAL verdict.

## Pass 2 (this run)
- [x] Re-parsed from canonical Marker MD output
      (`_LUCID100_ADMIN/marker_md_uicgpu_20260622/.../555f0ea0...md`).
- [x] Cross-checked Table I tokens against pdftotext baseline; identical.
- [x] Enumerated all 13 testable claims; identified 7 missed in pass 1.
- [x] Recomputed 4 effect-level RBE values from Fig. 2 caption (C7-C10).
- [x] Inferred β_γ-survival ≈ 0.096 Gy⁻² (α/β ≈ 1.57 Gy) from the
      Fig-2 iso-survival RBE = 4 — the paper itself does not tabulate this.
- [x] Verified "factor 4 larger" Discussion claim (C11) for both
      fragments/survival (7.6, 7.3) and colour-junctions/survival (4.2, 4.6).
- [x] Verified >1 decade of S_γ/S_α divergence at 2 Gy (C12, 1.6-1.8 dec).
- [x] Named the single missing artifact (per-dose Fig. 2 raw points; C13).
- [x] PARSER_PROVENANCE.md written.
- [x] REPORT.md rewritten with 8-section audit-shape format
      (verdict + 4-tier table + coverage/agreement + claims table +
      new computations + pass-1 retained + honest assessment +
      missing-artifact + files + checklist).

## Key new numbers (pass 2)
| Claim | Recomputed | Paper |
|-------|------------|-------|
| Effect-level RBE H2AX | 1.00 | 1 |
| Effect-level RBE fragments | 15.27 | 13 (1-digit round) |
| Effect-level RBE colour | 13.33 | 13 |
| Effect-level RBE survival → β_γ | 0.096 Gy⁻² (α/β=1.57 Gy) | not tabulated; sensible vs canonical late-tissue range |
| factor-4 fragments/survival (α, γ) | 7.64, 7.33 | "≥4" ✓ |
| factor-4 colour/survival (α, γ) | 4.18, 4.60 | "≥4" ✓ |
| Decade divergence at 2 Gy | 1.61-1.78 dec | ">1 decade" ✓ |

## Why not full data-level REPLICATED
- Raw per-dose Fig. 2 data points still not in any deposit (checked
  again 2026-06-23 — no supplement at *Oncology Reports*, no
  Dryad/Zenodo/figshare deposit found).
- Figure digitization remains an option but adds noise without
  changing any of the model-level conclusions above. The 6/22 rule
  artifact is named exactly in REPORT.md §7.
