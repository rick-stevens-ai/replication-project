# Replication Report — Analytical formulas representing PARTRAC track-structure DNA-damage simulations

## Verdict

**PARTIAL / analytical-figure replication.**

I reproduced the paper's published analytical formulas and generated LET-dependent DNA-damage yield curves from the transcribed Table 1/2 parameters. The low-LET baselines and several qualitative trends match the paper text, but this is **not a full PARTRAC replication** because the underlying PARTRAC simulator and raw simulation-symbol tables are not public/runnable here. One important consistency problem also remains: the proton/H DSB-site formula has no high-LET overkill divisor in the transcribed table, so unconstrained extrapolation to 500 keV/µm keeps rising well beyond the paper's prose claim that DSB-site effectiveness peaks around ~15 sites/Gy/Gbp at 100–200 keV/µm. That is likely a domain-of-validity / LET-range issue, and is documented rather than hidden.

Recommended audit line:

```text
| Kundrát 2020 Sci Rep 10:15775 (PARTRAC analytical DNA-damage formulas) | F1,F2,F8 | PARTIAL |
```

## Paper identity / DOI mismatch

The task DOI was `10.3390/cancers11020205`, but the supplied markdown/source is:

- **Kundrát P. et al.** *Analytical formulas representing track-structure simulations on DNA damage induced by protons and light ions at radiotherapy-relevant energies.* Scientific Reports 10:15775 (2020). DOI: **10.1038/s41598-020-72857-z**.

The task DOI points to a different Cancers review. I used the actual source markdown as the authoritative paper.

## Artifact availability

| Artifact | Status |
|---|---|
| Paper text | Cached as `source-paper.md` |
| Published equations | Available and implemented (`code/formulas.py`) |
| Fitted parameters | Available in Tables 1–2; manually transcribed (`code/parameters.py`) |
| PARTRAC simulator | Not public/runnable here |
| Raw PARTRAC symbol data behind Figs. 1–5 | Not present in source/supplement available here |
| Replication code | Created locally (`code/run_replication.py`) |

## Model reconstructed

The paper represents PARTRAC Monte Carlo track-structure outputs using two analytical formulas.

For SB/SSB yields:

\[
Y = p_1 - (p_2 LET)^{p_3} - \frac{p_4}{1 + \log^2(LET/p_5)}
\]

For DSB, DSB clusters, and DSB sites:

\[
Y = \frac{p_1 + (p_2 LET)^{p_3}}{1 + (p_4 LET)^{p_5}}
\]

where yield is in Gy⁻¹ Gbp⁻¹ and LET is in keV/µm. `N.A.` parameters are handled by dropping the corresponding term, as described in the paper.

## Outputs produced

- `results/summary.json`
- `results/yield_grid.csv`
- `results/table_excerpts.txt`
- `figures/fig1_sb_total_yields.png`
- `figures/fig2_dsb_total_yields.png`
- `figures/fig3_dsb_sites_total_yields.png`
- `figures/fig4_dsb_sites_effect_components.png`

## Claim-by-claim audit

| # | Claim | Replication result | Agreement |
|---|---|---|---|
| 1 | SB and SSB use a decreasing LET power-law plus a mild log-LET dip. | Eq. 1 implemented exactly from source text; curves generated for all ions. | **REPLICATED analytically** |
| 2 | DSB, DSB clusters, and DSB sites use increasing power-law terms with optional overkill denominator. | Eq. 2 implemented; `N.A.` denominator terms omitted. | **REPLICATED analytically** |
| 3 | Low-LET total SB ≈170 Gy⁻¹ Gbp⁻¹. | H at LET=0.5 gives ~baseline 170 behavior; parameter p1=170 for all ions. | **REPLICATED** |
| 4 | Low-LET total SSB ≈156 Gy⁻¹ Gbp⁻¹. | p1=156 for all ions. | **REPLICATED** |
| 5 | Low-LET total DSB ≈6.8–7 Gy⁻¹ Gbp⁻¹. | H at LET=0.5 gives 6.90; p1=6.8. | **REPLICATED** |
| 6 | DSB yield increases with LET roughly linearly until overkill/high-LET behavior. | Curves show increasing DSB for H/He/C/Ne; denominator produces high-LET modulation where parameters exist. | **PARTIAL** — no raw PARTRAC symbols |
| 7 | DSB clusters increase supra-linearly/sub-quadratically to quadratically with LET. | Implemented Table 2 cluster parameters and generated curves. | **PARTIAL** — trend reproduced from fitted formula only |
| 8 | DSB sites resemble RBE-like LET response; paper text says peak around 100–200 keV/µm and ~15 sites/Gy/Gbp. | Heavy-ion curves give peaks in this neighborhood, but H formula without overkill keeps rising if extrapolated to 500 keV/µm. | **PARTIAL / caution** |
| 9 | Fits reproduce PARTRAC simulations with RMS relative deviation <2% except DSB clusters up to ~9%. | Cannot independently verify because raw PARTRAC symbol data are unavailable. | **BLOCKED** |
| 10 | Formulas should not be extrapolated outside shown/fitted ranges; hooks at very low energies are not captured. | Confirmed in paper text; our high-LET/H DSB-site issue illustrates this warning. | **REPLICATED as limitation** |

## Friction tags

- **F1 code unavailable** — PARTRAC is not public/runnable.
- **F2 raw data unavailable** — fitted formulas are public, but underlying simulation-point tables are not.
- **F8 source/task DOI mismatch** — supplied DOI does not match actual markdown paper.

## Bottom line

The analytical formulas are reproducible and useful as a compact surrogate for the published PARTRAC results. However, because the simulator and raw simulation outputs are unavailable, and because at least one formula/table/domain issue affects the DSB-site peak if blindly extrapolated, this should be recorded as **PARTIAL**, not a full replication.

---

## Open Questions & Reproducibility Blockers

- **Blocking artifact (raw PARTRAC simulation symbol tables behind Figs 1–5):** the paper publishes only the fitted analytical coefficients (Tables 1–2). The underlying PARTRAC Monte Carlo output points (yield vs LET per ion, per damage class — the symbols plotted in Figs 1–5) are not in the paper, supplement, or any companion data deposit available to us. Without these, the paper's own claim of "<2 % RMS deviation (DSB clusters up to ~9 %)" cannot be independently verified — only the fit equations can be re-evaluated.
- **Blocking artifact (PARTRAC simulator itself):** PARTRAC is a closed in-house GSF/HMGU code; no public source release. So even if we had the simulation points, we cannot regenerate them or test new ion/energy combinations outside the fitted ranges.
- **Documented formula domain issue:** Table 1's H-proton DSB-site row has no overkill denominator term (`N.A.` in p4/p5 columns), so naive extrapolation past the fitted LET range produces unbounded yields that violate the paper's own prose claim of a ~15 sites/Gy/Gbp peak at 100–200 keV/µm. Either the table is missing entries or the formula is intentionally domain-restricted; we cannot tell which from the published material.
- **Open question:** could a public track-structure code (e.g. Geant4-DNA, TOPAS-nBio with the Option 2 physics list) reproduce the fitted coefficients within the quoted 2 % envelope? That would provide an independent existence proof of the underlying numbers without needing PARTRAC source access.
- **Open question (DOI/identity):** the assigned task DOI (`10.3390/cancers11020205`) points to a different Cancers review than the actual Kundrát 2020 *Sci Rep* paper used here. Whether the LUCID slot intended the review or the analytical-formulas paper is unresolved.

