# PROGRESS — GLOBLE kinetic photon cell-killing replication

Target paper: Herr L, Friedrich T, Durante M, Scholz M (2014). "A Model of Photon Cell Killing Based on the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures." PLOS ONE 9(1): e83923. DOI:10.1371/journal.pone.0083923.

Subagent run started: 2026-05-29.

## Stage 1 — paper ingestion (DONE)
- Copied source markdown from uicgpu (`/data/stevens/lucid-corpus-extracted/LUCID-papers/30afbb7d84f54d5d.md`) to repo as `paper.md`.
- Read full text (540 lines).  Five ODEs (Eqs 13–17), survival expression (Eq 18), split-dose formulae (Eqs 22–32), low-dose-rate limit closed form (Eq 38), high-dose-rate limit reduction, LQ–Lea-Catcheside comparison (Eqs 40–41), and the cell-line parameter table (Table 2) all captured.
- Fixed-by-paper constants: α_DSB = 30 DSB/Gy/cell; N_L = 3000 domains; HLT_c = 5 h.
- Adjustable per cell line: ε_i, ε_c, HLT_i.

## Stage 2 — model implementation
- `code/globle.py` — core ODE model (scipy.solve_ivp) + analytic helpers (static GLOBLE, split-dose closed form, low-dose-rate Eq. 38, LQ + Lea-Catcheside).
- Verified ODE limits programmatically:
  - high dose rate (instantaneous) → matches static GLOBLE (Eqs 6–7).
  - low dose rate → matches closed-form Eq. 38.
  - LQ–GLOBLE second-order equivalence (Fig. 4) reproduced.

## Stage 3 — figure reproductions
- Fig 2A (RT112): dose-rate family (76.8 / 30 / 12 / 6 / 3 / 1.2 / 0.6 Gy/h) with Table 2 params (ε_i=0.00529, ε_c=0.195, HLT_i=0.485 h).
- Fig 2B (MT): dose-rate family (90 / 24 / 8.4 / 4.56 / 0.96 Gy/h) with Table 2 params from "Dose rate experiments" column (ε_i=0.00865, ε_c=0.178, HLT_i=0.0859 h).
- Fig 3 (MT split dose): 5+5 Gy and 6+6 Gy vs separation time t1, Table 2 "Split dose" params (ε_i=0.00958, ε_c=0.119, HLT_i=0.288 h).
- Fig 4 (LQ vs GLOBLE Lea–Catcheside equivalence): three α/β ratios (1, 5.26, 9 Gy).
- Fig 5 (deterministic effects: pneumonitis & bone-marrow): isoeffective dose vs dose rate vs empirical Eq. 42.
- Fig 6 (LL split-dose prediction from dose-rate fit): predicts the well-known maximum-shift bias the paper documents.

## Stage 4 — claim-by-claim ledger and verdict (REPORT.md)
- Quantitative agreement table; friction tags; verdict using AUDIT_PROTOCOL standard (Recovered / Partial / Unrecoverable).

## Blockers / friction
- **No supplement (File S1).** Approximate closed-form in S1 is referenced but not in the markdown extraction. We implement the ODE numerically per Eqs 13–17; not blocking, just slightly limits the analytical-equivalence demo.
- **No raw experimental data points distributed.** The paper digitised graphs with "GetData Graph Digitalizer"; raw points are not in the source. We reproduce model curves under the published parameters (Table 2) and confirm the *qualitative* and *parameter-consistent* claims. Hard pointwise overlay of measured markers would require digitising the figures or contacting the authors.
- **DOI source code release.** Author repository / code release not referenced in paper; replication is from-scratch from the equations.

- **2026-05-29 17:31** Main agent gate check found missing `REPORT.md` despite otherwise complete code/results/figures. Wrote final REPORT.md from generated artifacts. Final gate now expected to pass. Verdict: REPLICATED, with F1/F2/F3/F8 limitations.

---

## Stage 5 — Re-pass to lift coverage (2026-06-23)

Subagent run started: 2026-06-23.

### Parser check
- Canonical Marker merge `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/` does **not** include DOI 10.1371/journal.pone.0083923 (verified by name + content scan; only papers citing Herr 2014 are present).
- Re-pass therefore uses pre-existing `paper.md` (md5 cb54cfea58b7e35f222e5ea942e032c0, 90621 B, 540 lines).
- Cross-checked against `pdftotext -layout artifacts/paper.pdf` (md5 7595c7482330b346e91311d316e1afd4, 1048 lines). Tables 2 and 3 and all numerical values used by re-pass code agree between the two parses.
- Recorded in `PARSER_PROVENANCE.md`.

### What got added
Single re-pass driver `code/repass/repass_globle.py` (compute: CherryRd CPU only, no GPU, no network), generating six independent claim batches:
- **Claim A — Table 2 self-consistency** (all 17 cell lines, 22 param sets): ε_i < ε_c 22/22, split-dose-column median HLT_i = 0.458 h exactly matches paper text. → `results/repass/claim_A_table2.json`.
- **Claim B — Dose-rate survival families for all 17 cell lines** (pass 1 only had RT112+MT): all monotonic in dose at every dose rate. → `figures/repass/dose_rate_all_cell_lines.png` (5×4 grid, 2080×1950 px) + `results/repass/claim_B_dose_rate_all.json`.
- **Claim C — Split-dose recovery for all 5 split-dose cell lines** (pass 1 only had MT): all 5 recover, S(t=10h)>S(t=0). → `figures/repass/split_dose_all_cell_lines.png` + `results/repass/claim_C_split_dose_all.json`.
- **Claim D — Table 3 reproduction**: GLOBLE HLT_i dose-rate and split-dose columns equal Table 2 HLT_i row-by-row, 11/11 dose-rate match, 11/11 split-dose match. → `results/repass/claim_D_table3.json`.
- **Claim E — Analytical limits**: high-dose-rate (10^6 Gy/h) ODE → static GLOBLE (Eqs 6-7) with max |Δ ln L| = 1.46e-2; low-dose-rate (10^-3 Gy/h) ODE → closed-form Eq. 38 with max |Δ ln L| = 1.02e-2. Both pass at 0.05 log-tolerance across all 17 cell lines × 3 doses. → `results/repass/claim_E_limits.json`.
- **Claim F — Eq. (8) Taylor identity**: α_initial = ε_i · α_DSB across all 17 cell lines, max relative error 2.80e-3. → `results/repass/claim_F_alpha_taylor.json`.

### Honest negatives recorded
- High-DR convergence needed ≥ 10^6 Gy/h to satisfy 0.05 log-tolerance for the smallest-HLT_i cell line (CHO K1, HLT_i = 0.035 h). Not a paper-vs-replication issue; documents the limit physics.
- Paper's "median HLT_i = 0.458 h" matches only the split-dose column (5 cell lines), not the dose-rate column (0.487 h) or the pooled 22 sets (0.486 h). Recorded explicitly.
- Claim 7 (raw-data pointwise overlay) still BLOCKED on author-undistributed digitized points. F2 unchanged.

### Coverage / agreement update
- Pass 1: Coverage 7, Agreement 8, REPLICATED.
- Re-pass: **Coverage 9** (+claims 9–16), **Agreement 9**, REPLICATED.
- Single remaining ceiling: Claim 7 raw-data overlay (BLOCKED on missing external data).

### Files
- Original pass-1 report preserved as `REPORT.pass1.md`.
- New report at `REPORT.md`.
- Parser provenance at `PARSER_PROVENANCE.md`.
- Re-pass code at `code/repass/repass_globle.py`.
- Re-pass outputs at `results/repass/` (7 JSON files) and `figures/repass/` (2 PNG files).
