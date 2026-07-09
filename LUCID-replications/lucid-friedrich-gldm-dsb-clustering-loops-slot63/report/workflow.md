# Workflow — LUCID slot 63 (Friedrich et al. 2012, GLOBLE static / GLDM)

## Environment
- Host: CherryRd (macOS, x64 branch of mesh)
- Runtime: Python 3, numpy + matplotlib + scipy on system stack; no venv,
  no GPU, no HPC, no paid endpoints
- Total wall-clock: < 5 s for all numerics + figures
- Paper access: **abstract-only** (PubMed). Full PDF closed-access
  (Unpaywall `is_oa=false`), not obtained. Formula transcription cross-
  checked against the well-documented sibling kinetic-GLOBLE paper
  (Herr et al.\ 2014, PLoS ONE), which explicitly re-cites Eqs. 1–7.

## Sequence of steps

1. **Paper identification and open-access check**
   - Confirmed DOI `10.1667/RR2964.1`, PubMed 22998227, 105 citations
     (Semantic Scholar, 2026-06-09). Unpaywall probe returned
     `is_oa=false`; no repository copy. Recorded as "PDF NOT obtained,
     working from abstract + sibling paper" in REPORT.md.

2. **Model reconstruction**
   - Wrote Eqs. 1–7 (Poisson placement of DSBs into N_L identical loops,
     isolated/clustered probabilities, survival curve) plus the LQ
     correspondence Eqs. 12–13 into a single self-contained module
     `code/globle_static.py`. Paper-fixed constants
     `alpha_DSB = 30 DSB/Gy/cell`, `N_L = 3000`, transcribed via Herr 2014
     Table 1.
   - Exposed `StaticParams` dataclass with `alpha_lq` / `beta_lq`
     properties derived analytically from `(eps_i, eps_c, alpha_DSB, N_L)`.

3. **Cell-line parameter ingest**
   - Transcribed 17-line `(eps_i, eps_c)` catalogue from Herr 2014
     PLoS ONE Table 2 into a plain Python dict inside
     `code/globle_static.py`.

4. **Figure production**
   - Fig. 1 (`figures/fig1_dose_response_RT112.png`): RT112 dose-response,
     `-ln S(D)` on 0–20 Gy grid, with LQ tangent overlay.
   - Fig. 2 (`figures/fig2_alpha_beta_anticorr.png`): scatter of
     derived `(alpha_LQ, beta_LQ)` for 17 lines, with Pearson r and
     Spearman rho annotated.
   - Fig. 3 (`figures/fig3_decomposition.png`): isolated vs clustered
     term decomposition of `-ln S(D)` for RT112.
   - Driver script: `code/make_figures.py`.

5. **Claim-by-claim audit**
   - Claim 1 (LQ→linear crossover): visual + numerical check, REPLICATED.
   - Claim 2 (β vs α anti-correlation): Pearson r=+0.655, Spearman ρ=+0.512
     — opposite sign. Recorded as INCONCLUSIVE because our subset is
     17 lines vs the paper's 150+, and the eps_i / eps_c positive
     covariance in this subset masks the predicted anti-correlation.
   - Claim 3 (LQ from micro parameters): analytic derivation + numerical
     check on RT112 gives alpha/beta ≈ 5.7 Gy, in literature ballpark;
     REPLICATED.

6. **Self-verdict**
   - PARTIAL FIRST-PASS REPLICATED. Recommended QA retag
     `candidate_curated` → `completed_first_pass`.

7. **External audit (2026-06-20)**
   - 3-judge LLM panel (argo:gpt-5, argo:gemini-2.5-pro,
     argo:claude-opus-4.6) per AUDIT_PROTOCOL.md.
   - Judges returned PARTIAL / PARTIAL / SPOT-CHECK.
   - Aggregated (majority + conservative-on-tie): PARTIAL.
   - Median Coverage 4/10, Agreement 6/10. Flagged as coverage-limited.

8. **Backfill (2026-07-06, this pass)**
   - Standardised the report/*.tex + open_questions.json + workflow +
     failure_analysis + extraction stub package per LUCID 8-artifact
     standard. Preserved existing REPORT.md, code, figures, and audit
     record unchanged. No re-runs performed.

## What we deliberately did NOT do
- No track-structure Monte Carlo (PARTRAC / TOPAS-nBio) rerun to derive
  `alpha_DSB` from first principles — inherited as a paper-fixed constant.
- No DSB-clustering algorithm reimplemented on explicit chromatin
  geometry (Hi-C loops, fractal-globule, polymer sim) — Poisson placement
  used per the paper.
- No PIDE-scale (150+ line) re-fit for the β-vs-α claim — 17 lines only.
- No ion / high-LET exercise — RR2964 is photon-only and we stayed
  in-scope.
- No PDF-based verification of formula transcription — cross-checked via
  Herr 2014 sibling paper instead.

## Reproducibility
Full re-run: `python code/make_figures.py` from the slot root. Produces
all three figures + a stdout dump of the (D, n_iso, n_clu, -ln S) table
and the 17-line (alpha_LQ, beta_LQ) table with correlation stats.
