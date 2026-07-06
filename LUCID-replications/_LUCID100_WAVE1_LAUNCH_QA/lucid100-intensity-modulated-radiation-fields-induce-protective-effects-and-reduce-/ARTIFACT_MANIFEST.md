# Artifact Manifest — Matsuya et al. 2019 (s41598-019-45960-z)

Generated: 2026-06-09 (LUCID100 Wave 1, slot 3, Ollie subagent).

## Provenance

| Artifact | Path | sha256 | Source |
|---|---|---|---|
| Main paper PDF | `paper.pdf` | `001ca939e425346704f943172a6e66f664907af8f5f6495c7f7ea093e01fe85d` | Dropbox/XFER/LUCID-replication-targets/5f5b0d9df89a74d8abbe7143e9a2c9c1fb5e9cd3.pdf |
| Main paper text (pdftotext -layout) | `paper.txt` | — | local extraction |
| Supplementary PDF (MOESM1) | `supplement/41598_2019_45960_MOESM1_ESM.pdf` | `fcaefb6dbfba2da99adff7fa7f088b460513b717f02d48d0492ecc55a98bfaaa` | `https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-019-45960-z/MediaObjects/41598_2019_45960_MOESM1_ESM.pdf` |
| Supplementary text (pdftotext -layout) | `supplement/supplement.txt` | — | local extraction |
| Landing page snapshot | `supplement/landing.html` | — | nature.com/articles/s41598-019-45960-z |

License: CC BY 4.0 (open access). Re-use, redistribution, and re-implementation are explicitly permitted with citation.

## Data availability

- No formal "Data Availability" statement, no GitHub/Zenodo/figshare DOI in the paper.
- All experimental survival data published as figures (Figs 2–6 main, Figs S5–S8 supplement) with no machine-readable tables.
- Model parameter values (the only inputs needed for an analytical/numerical replication of the curves) are fully tabulated in **Table 1** of the main paper, with means and standard deviations for both cell lines (AGO1522, DU145) and both field geometries (modulated/half-field, uniform/full-field).
- Microdosimetric inputs (yD = 4.393 ± 0.007 keV/µm in-field, 4.769 ± 0.044 keV/µm out-of-field) are printed in main text §Monte Carlo.

## Code availability

- No public code repository cited.
- The model is fully specified by equations (1)–(10) in the main paper and (S1)–(S7) in the supplement.
- All equations are closed-form / quadrature-friendly; no numerical solver required for the forward model.
- MCMC parameter inference would only be needed for an independent _refit_ replication (out of scope for first pass).

## What is reproducible without contacting authors

1. **Forward model curves** (Figs 3, 4, 5, S5, S7): use Table 1 parameters and Eqs (1), (2), (5), (6) to regenerate predicted survival vs dose / vs dose-rate / vs fractionation pattern. This is what `src/imk_model.py` does.
2. **Sensitivity analysis** of how the published (a+c), β0, αb, βb, δ alterations between MF and UF translate to predicted survival differences — directly testable, no data needed.
3. **Cross-check** of the central qualitative claims: (i) lower in-field killing in half-field vs uniform, (ii) reduced SLDR rate in AGO1522 under MF, (iii) reduced β0 under MF. Verifiable from the parameter table alone.

## What requires digitization

1. **Quantitative agreement** of regenerated curves vs published experimental points → would require digitizing data points from Figs 2–6 (WebPlotDigitizer-grade pipeline, future pass).
2. **Multi-fractionation curves at 4 dose-rates** (Fig 4) for a numerical χ² comparison against Eq (1) at N>1.
3. **Split-dose recovery curves** (Fig 2) → derivation of (a+c) and β0 from Eqs (7), (8). Sanity check of Table 1 row 1.

## What is out of scope for any replication

- Re-running PHITS + WLTrack Monte Carlo for yD (requires PHITS license + in-house code WLTrack). The output (yD values for 60Co, 6MV, 200/225 kVp) is already in Table S1 / main text.
- Re-running MCMC parameter inference — needs the underlying clonogenic counts (not published), and any independent MCMC will just reproduce Table 1 within stated uncertainty given the same data.
- Wet-lab redo of clonogenic assays, flow cytometry, dose mapping with Gafchromic film.

## Replication scope decision

**Partial-scope, forward-model replication.**

- Implement the IMK forward model with TEs + IC for half-field and uniform-field geometries.
- Reproduce Figs 3 / 4 / 5 / S5 / S7 as predicted curves using Table 1 parameters.
- Compare qualitative shape and key landmarks (e.g., D10 = dose giving 10% survival; β0(MF) vs β0(UF); SLDR rate ratio) against the paper's claims.
- Defer digitization-driven χ² and MCMC re-inference to a Wave-2 pass.
