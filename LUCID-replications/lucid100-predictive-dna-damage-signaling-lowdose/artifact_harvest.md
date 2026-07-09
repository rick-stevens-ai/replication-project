# Artifact Harvest — Park et al. 2024

## Files in `evidence/`
| File | Size | Description |
|---|---|---|
| `europepmc.json` | 9.8 KB | EuropePMC core record. Title, full author list (9 authors, KIRAMS / Korea Institute of Radiological & Medical Sciences), journal *Int J Mol Med*, 2024, DOI 10.3892/ijmm.2024.5380. Includes full abstract. |
| `fullText.xml` | 99 KB | EuropePMC full-text XML (open-access body, methods, figures captions, references). Confirms: HuT 78 + IM-9 + PBMC + western-blot methods; mouse radioprotection studies with cinobufagin / KU60019 / BML-277 / pifithrin-α / nutlin-3a. |

## What full text reports (string searches in `fullText.xml`, 2026-06-16 21:19 CDT)
- "CHK2": 43 mentions
- "ATM": 40 mentions
- "H2AX" (incl. γH2AX): 25 mentions
- "HuT 78" (cell line): 19 mentions
- "IM-9" (cell line): 18 mentions
- "PBMC": 16 mentions
- "western blot": 7 mentions
- **No GEO/PRJNA/PRJEB/E-MTAB/SRP accession** — no transcriptomic deposition.
- No published table of band-intensity values, dose-response coefficients, or rate constants found in the body.

## What is NOT here
- No model code, no parameter table, no fitted dose-response equations, no DSB-repair rate constants, no Monte Carlo input, no LQ α/β, no microdosimetric outputs.
- No supplementary data tables (the paper appears to be figures-only for quantitative content).
- No public code repository cited.
- No omics dataset accession (RNA-seq, ChIP-seq, etc.).

## Conclusion of harvest
Paper is a **wet-lab biomarker + in vivo drug-screen study**, not a computational radiobiology paper. There is no model, no rate constants, no released numerical dataset, and no analysis code to re-run. **NO-GO for computational replication.**
