# Artifact Manifest — LUCID100 Wave 2 slot 19

**Paper:** Belov O., Chigasova A., Pustovalova M., Osipov A., Eremin P., Vorobyeva N., Osipov A.N. (2023) *Dose-Dependent Shift in Relative Contribution of Homologous Recombination to DNA Repair after Low-LET Ionizing Radiation Exposure: Empirical Evidence and Numerical Simulation*. **Current Issues in Molecular Biology** 45(9):7352–7373.
**DOI:** 10.3390/cimb45090465
**PMID:** 37754249
**PMCID:** PMC10528584
**License:** CC BY 4.0 (MDPI open access).

## Source artifacts harvested

| Path | Source | Size | Notes |
|---|---|---|---|
| `paper/paper_pmc.pdf` | Europe PMC render PDF (`europepmc.org/articles/PMC10528584?pdf=render`) | 2.9 MB, 10 pages | Authoritative full text. MDPI PDF endpoint blocked by Akamai for non-browser UAs. |
| `paper/fulltext.xml` | Europe PMC JATS XML (`/PMC10528584/fullTextXML`) | 250 KB | Used to parse equations, parameter table, reference list. |
| `paper/fulltext.md` | Locally stripped markdown of XML | 50 KB | Section-segmented text for grepping. |
| `paper/europepmc.json` | Europe PMC search result (DOI lookup) | 7 KB | Author affiliations + IDs. |

## Code / data availability (verbatim from paper)

> **Data Availability Statement.** Not applicable.

There is **no** released code, no Zenodo/GitHub link, no supplementary file with raw foci counts. The only software citation is `https://github.com/varnivey/darfi` (DARFI v.2016) for **manual γH2AX/Rad51 foci counting from microscopy** — not for the simulation. The simulation itself is described as authors' own code (Author Contributions: "software, A.C. and O.B."), built on the model first published in:

> **[Ref 23]** Belov O., Krasavin E., Lyashko M., Batmunkh M., Sweilam N. *A quantitative model of the major pathways for radiation-induced DNA double-strand break repair.* **J. Theor. Biol.** 366:115–130 (2015). DOI 10.1016/j.jtbi.2014.09.024. **(Paywalled, no public code repo found.)**

## Quantitative artifacts that ARE in the 2023 paper

The paper is unusually self-contained on the **modeling side** (in contrast to the empirical data, which are figure-only).

- Eqs. (1)–(29) in main text: the full mass-action chemical kinetics scheme — NHEJ (Eqs 2–8), HR (9–16), SSA + micro-SSA (17–20), Alt-EJ (21–24), γH2AX foci dynamics (25–27), HR percent contribution (28–29).
- Appendix A: integration scheme (RK4, dt = 1e-10 s), cell-cycle weighting (45% G0/G1+early S, 55% late S+G2/M), DSB cluster routing (Eq A3).
- Appendix B Eqs (A4)–(A7): the full ODE systems (NHEJ 11 ODEs, HR 10 ODEs, SSA 5 ODEs, Alt-EJ 4 ODEs) — extracted verbatim into `artifacts/equations_A4_A7.txt`.
- Appendix C **Table A1**: complete rate-constant table (K1..K12, P1..P12, Q1..Q6, R1..R5, plus α(L) parameters a=27.5, b=2.43e-3 and the closed-form Nirrep(D) piecewise function). Extracted into `artifacts/table_A1_parameters.csv`.

## Empirical data NOT shared

Numerical foci-count tables behind Figures 2, 3, 5, 6, 7, 8 are **not** provided as supplementary data. Only the figure curves themselves (PNGs embedded in the PDF) are publicly visible. To replicate the full PHR(D) fit one would have to digitize Figs 2/3 to recover the experimental points, then re-fit the rate constants in Table A1 — the paper notes that "the majority of the rate constants of enzymatic reactions were determined by fitting the corresponding model curves … to the experimental data" without specifying which constants were fitted vs. taken from literature.

## Smoke-replicable items

Two closed-form quantities from the paper that can be reproduced without solving any ODE:

1. **α(L)·D** initial DSB yield (Eq A1) — at L≈0.3 keV/μm X-rays: 0.55 DSB at 20 mGy, 27.5 DSB at 1 Gy.
2. **Nirrep(D)** irreparable fraction (Table A1) — piecewise: peaks ~0.087 at ~250 mGy, decays to 0.01 at ≥1 Gy. This non-monotonic shape directly supports the paper's qualitative claim that **low-to-moderate doses leave a disproportionately elevated residual foci pool**.

Implemented in `scripts/smoke_dsb_yield.py` → `results/smoke_dsb_yield.csv`, `results/smoke_dsb_yield_grid.csv`, `figures/smoke_dsb_yield.png`. Runtime <1 s on CPU.

## Generated artifacts

| Path | Provenance |
|---|---|
| `artifacts/equations_A4_A7.txt` | Parsed from `paper/fulltext.xml` `<disp-formula>` blocks. |
| `artifacts/table_A1_parameters.csv` | Hand-transcribed from §Appendix C of `paper/fulltext.md`, cross-checked against rendered PDF. |
| `scripts/smoke_dsb_yield.py` | New, no external deps beyond numpy + matplotlib. |
| `results/smoke_dsb_yield.csv` | 7 paper dose points. |
| `results/smoke_dsb_yield_grid.csv` | 1001-point fine grid for plot. |
| `figures/smoke_dsb_yield.png` | 2-panel smoke figure. |
| `logs/smoke_dsb_yield.log` | Stdout of smoke run. |
