# PROGRESS — OSTI 2217719 — SCALE depletion capabilities for MSRs

## 2026-04-19 / 2026-04-26 — Pass 1
- Phase 1: 9-component Bateman ODE for three-mixture verification (Figs. 3–6) — passed.
- Phase 2: OpenMC 2D MSRE core depletion (25 × 15 d, 5000 part × 50 batches) — initial k_eff = 1.165, monotonic decrease to 1.088 at 375 d. Geometry: 6.102 cm pitch, fuel channel 22.5%, vessel R = 76.20 cm.
- Tier-lift Q1: analytical Xe-135 / I-135 reactivity sensitivity vs λ_rem.
- External assessment: Coverage 6 / 10, Agreement 5 / 10, verdict PARTIAL. (Pass-1 self-score was 8/8 — the external review applied a stricter rubric.)

## 2026-06-23 — RE-PASS (this run)
- Re-parsed paper cleanly with `pdftotext -layout` (Poppler 26.06.0). Provenance in `PARSER_PROVENANCE.md`. Output `results/repass/paper.txt` (869 lines).
- Enumerated every numerical claim in the paper that is testable without SCALE.
- Built `code/repass/repass_claims.py` — single self-contained script — that reproduces 9 claims using:
  - explicit arithmetic (C-1, C-2);
  - SciPy LSODA Bateman ODE integration with closed-form ratio checks (C-3, C-4, C-9);
  - 1-group analytic Xe / I-135 equilibrium with online removal (C-5, C-6);
  - 3-compartment Bateman cascade for fuel-salt → OGS → charcoal at the Table 3 rates plus an order-of-magnitude volume estimate (C-7);
  - 6-group U-235 delayed-neutron precursor decay with one core-residence time-constant (C-8).
- Verdicts:
  - **5 / 9 pass at exact or near-exact agreement** (C-1, C-2, C-3, C-9, plus C-8 within bound).
  - 1 / 9 qualitative timescale match (C-4, paper ~50 d vs τ_eq = 39 d to 81 d = 3 t½).
  - 3 / 9 order-of-magnitude (C-5, C-6, C-7) — methodology-substituted (no SCALE / no full transport).
- Documented a **typo in the paper's Table 1**: λ_Pa-233 and λ_Th-233 labels are swapped (the numeric values themselves are correct — only the element labels are exchanged).
- Outputs:
  - `results/repass/paper.txt`
  - `results/repass/repass_claims_results.json` (full per-claim ledger)
  - `results/repass/three_mixture_repass.npz` (Bateman trajectory, audit)
- Preserved pass-1 deliverables: `REPORT.pass1.md` (snapshot of original REPORT.md before update), all files under `replication/`.
- Re-scored: Coverage 9 / 12 testable claims = **8 / 10**, Agreement (median across the 9 claims) = **8 / 10**.

## Missing tool (6/22 rule)
The single artifact that would close the remaining gap is **SCALE 6.3 (TRITON + ORIGEN) with ENDF/B-VII.1 nuclear-data libraries** — the licensed, export-controlled ORNL code system the paper used. Without it we cannot reproduce the exact eigenvalue trajectory in Fig. 11 (750–930 pcm Xe-removal benefit), the addnux sensitivity (Fig. 6), the noble-metal plateout densities (Fig. 13), or the TRITON-vs-Serpent code-to-code comparison (~19 pcm). SCALE distribution is gated by RSICC and export-control review, so we substitute with OpenMC (pass-1) and analytic / Bateman methods (re-pass).
