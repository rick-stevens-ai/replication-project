# LUCID100 slot 23 — Shuryak & Brenner (2012)

**Paper.** Mechanistic Analysis of the Contributions of DNA and Protein Damage to Radiation-Induced Cell Death.
*Radiat. Res.* 178(1), 17–24 (2012). DOI [10.1667/RR2877.1](https://doi.org/10.1667/RR2877.1).
PMID 22687051 · PMCID [PMC3580191](https://pmc.ncbi.nlm.nih.gov/articles/PMC3580191/).
Authors: Igor Shuryak, David J. Brenner (Center for Radiological Research, Columbia University).
Funding: NIH NIAID U19 AI067773.

**LUCID100 metadata.** Wave 3 · Tier A · slot 23 (rank 54) · priority 16 · themes: DNA repair / DDR, radiation quality / RBE, microbial / extremophile, computational model / simulation.

## What the paper is

A 5-equation closed-form mechanistic model for bacterial cell survival under
ionizing (γ) and UV radiation that splits cell death into:

- **Q₁** — DNA double-strand breaks whose repair fidelity decays with
  cumulative protein carbonylation (Eq. 3),
- **Q₂** — direct loss of viability from carbonylation of essential
  metabolic / replication proteins (Eq. 4),
- with total survival **S = Q₁ · Q₂** (Eq. 5).

Protein-damage state `P(D)` is read directly from measured protein
carbonylation `F(D)` via Eq. 2. The model has only 4 free parameters
(`Fmax`, `Kdam`, `Krep`, `X`), most of which are pinned across strains.
Fits are reported in Table 1; mechanistic interpretations (which of Q₁ or
Q₂ dominates cell death for each strain × radiation × dose range) in
Table 2.

The model is fit to data from [Krisko & Radman (2010) PNAS
107:14373](https://doi.org/10.1073/pnas.1009312107) (PMC2922536) on
*D. radiodurans* (R1 wild-type, recA- mutant), *E. coli* (MG1655
wild-type, CB1000/CB2000 radioresistant) and λ-phage infective centers
grown in irradiated *E. coli* hosts.

## Artifact harvest status

| Artifact                       | Status      | Where                                              |
|--------------------------------|-------------|----------------------------------------------------|
| PMC JATS XML full text         | ✅ OK       | `artifacts/paper_oai.xml` (80 KB, via PMC OAI-PMH) |
| Plain text body                | ✅ OK       | `artifacts/paper.txt` (25 KB)                      |
| EuropePMC abstract page        | ✅ OK       | `artifacts/europepmc_abstract.html`                |
| Unpaywall record               | ✅ OK       | `artifacts/unpaywall.json` (oa_status = green)     |
| Author PDF                     | ❌ blocked  | EuropePMC render → HTTP 500; NCBI PMC PDF → reCAPTCHA; PNAS / Radiation Research → 403 / paywall. JATS XML is sufficient. |
| Figure JPGs                    | ❌ blocked  | All PMC + EuropePMC image endpoints return reCAPTCHA HTML. Figure captions and equations were extracted from JATS. |
| Supplementary material         | n/a         | Zero `<supplementary-material>` elements in JATS — none was published. |
| Source data (Krisko & Radman)  | ⚠️ no tabular form | PNAS landing reachable, but raw `F(D)` / `S(D)` points only appear inside published figures; would need WebPlotDigitizer to lift. |
| Authors' fitting code (FORTRAN simulated annealing) | ❌ not public | No GitHub repo under `igorshuryak`; code search for "Shuryak Krisko Radman" → 0 hits; no repository URL in paper or references. |

## Reusable model spec (extracted from JATS)

| Parameter | Best-fit value | 95 % CI | Strain/condition scope | Fixed? |
|-----------|---------------|---------|-------------------------|--------|
| `Fmax`    | 8.50 nmol carb./mg | — | all strains + IC | yes (data) |
| `Kdam_γ`  | 10.0 kGy⁻¹        | — | all γ-irradiated strains | yes (literature, ref 13) |
| `Kdam_UV` | 3.99 m²/kJ        | (3.7, 4.2) | all UV-irradiated strains | no |
| `Krep`    | 13.9              | (6.7, 19)  | *D.r.* R1, *E.c.* WT, *E.c.* Res | no |
| `Krep`    | 0                 | —          | *D.r.* recA- | yes |
| `X`       | 3.88              | (3.4, 5.3) | *D. radiodurans* (both) | no |
| `X`       | 6.76              | (6.1, 8.0) | *E. coli* (all) + λ IC  | no |

For the bacteriophage-infective-centers endpoint, the paper sets `Q1 = 1`
(unirradiated phage DNA) so S = Q₂ = P^X.

## Minimal smoke replication

`scripts/smoke_shuryak_2012.py` (pure Python 3, no third-party deps for the
core run; optional `matplotlib` for figures) implements Eqs. 1–5 with the
Table 1 parameter values and integrates strain-specific approximate `F(D)`
curves whose shapes match the qualitative descriptions in the paper
(*E. coli* proteins oxidize rapidly toward Fmax; *D. radiodurans* proteins
resist oxidation, only approaching half-saturation at the upper dose
limits studied). Replace the `_logistic_F` placeholders with digitized
Krisko & Radman 2010 data points to lift this to a numeric replication.

Run:

```bash
cd lucid100-dna-protein-damage-cell-death
python3 scripts/smoke_shuryak_2012.py --plot
```

Outputs to `results/`:

- `summary.csv` — per (strain, radiation) `P_end`, `Q1_end`, `Q2_end`,
  `S_end`, `log Q1 / log S`, `log Q2 / log S`, dominant mechanism.
- `{strain}_{γ|UV}.csv` — full dose grid with `P`, `Q1`, `Q2`, `S`.
- `survival_{γ|UV}.png` — log-survival curves (5 strains each).

### Smoke result

Dominant-mechanism agreement with Table 2 of the paper: **10 / 10** rows
(*D.r. R1 γ + UV, D.r. recA- γ + UV, E.c. WT γ + UV, E.c. Res γ + UV,
λ IC γ + UV*). Survival values are within several orders of magnitude
of the published ranges — exact quantitative match awaits the digitized
input data.

## Replication scope

| Reproducibility tier      | Achievable? | Path |
|---------------------------|-------------|------|
| Re-derive Eqs. 1–5        | ✅ done     | `scripts/smoke_shuryak_2012.py` |
| Re-fit parameters         | ⚠️ blocked on data | need Krisko & Radman 2010 raw F(D)/S(D); digitize figures with WebPlotDigitizer or contact authors |
| Reproduce Tables 1 + 2    | ✅ qualitatively / ⚠️ numerically | qualitative now; numeric after data lift |
| Reproduce Figs. 1, 3–5    | ⚠️ partial | shapes reproduced with placeholder F(D); exact overlay awaits digitized data |
| Compute budget            | trivial    | < 1 s single core; safe to run on CherryRd |

No heavy compute. No author contact needed for the first-pass goal.
No paid endpoints used.

## Files

```
lucid100-dna-protein-damage-cell-death/
├── README.md                         (this file)
├── PROGRESS.md                       (timestamped run log)
├── MANIFEST.json                     (machine-readable artifact list)
├── FIRST_PASS_REPORT.md              (verdict + recommendation)
├── artifacts/
│   ├── paper_oai.xml                 (PMC JATS XML, 80 KB)
│   ├── paper.txt                     (plain text body, 25 KB)
│   ├── europepmc_abstract.html
│   └── unpaywall.json
├── scripts/
│   └── smoke_shuryak_2012.py
├── results/
│   ├── summary.csv
│   ├── {Dr_R1,Dr_recA,Ec_WT,Ec_Res,Ec_IC}_{gamma,UV}.csv
│   ├── survival_gamma.png
│   └── survival_UV.png
└── notes/                            (kept empty; reserved for digitization scratch)
```
