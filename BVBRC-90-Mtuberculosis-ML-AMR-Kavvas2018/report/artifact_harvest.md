# Artifact Harvest — BVBRC-90

All artifacts downloaded 2026-07-04. All from FREE public sources (Springer static-content CDN, NCBI E-utils). No auth required.

## Nature/Springer supplementary data (paper s41467-018-06634-y)

| File | URL (fetched from Springer static-content CDN) | Bytes | MD5 |
|---|---|---:|---|
| MOESM1 (Supplementary Information PDF) | https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-018-06634-y/MediaObjects/41467_2018_6634_MOESM1_ESM.pdf | 5,380,196 | 329bf089911d7cea664d160406cf9646 |
| MOESM4 (Sup Data 1: MI/χ²/ANOVA per drug) | .../41467_2018_6634_MOESM4_ESM.xlsx | 83,565 | e413c6416524d7bdf7ace8db9d56d75b |
| MOESM5 (Sup Data 2: SVM-SGD selected alleles) | .../41467_2018_6634_MOESM5_ESM.xlsx | 81,420 | fd6dd5ca9453215c8ccb7df357b9a680 |
| MOESM7 (Sup Data 4: epistatic interactions) | .../41467_2018_6634_MOESM7_ESM.xlsx | 41,339 | 950c9c0076ffd5de74f3dfcb253e7413 |
| MOESM8 (Sup Data 5: co-occurrence tables) | .../41467_2018_6634_MOESM8_ESM.xlsx | 866 | c05cfbcdabf777795d62c0e3bb168fd7 (**AccessDenied XML, not a real file**) |
| MOESM9 (Sup Data 6: 2000 alleles + sequences) | .../41467_2018_6634_MOESM9_ESM.xlsx | 479,416 | 9aca44afde7a1847f3df67448685bdfc |

**Total: 6.06 MB usable public artifacts.**

## NCBI H37Rv reference proteins (fetched via E-utils efetch, protein DB)

Independent verification of canonical AMR-gene wildtype sequences.

| Gene | Accession | Length (aa) | Fetch URL |
|---|---|---:|---|
| katG | NP_216424.1 | 740 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=NP_216424.1&rettype=fasta&retmode=text |
| pncA | NP_216559.1 | 186 | same, id=NP_216559.1 |
| rpoB | NP_215181.1 | 1172 | same, id=NP_215181.1 |
| gyrA | NP_214520.1 | 838 | same, id=NP_214520.1 |
| inhA | NP_216000.1 | 269 | same, id=NP_216000.1 |
| rpsL | NP_215196.1 | 124 | same, id=NP_215196.1 |

Saved to `work/intermediates/h37rv_reference_proteins.fasta`.

## Local tooling

- Python 3.13 (system) + `openpyxl` (already installed) — used for XLSX parsing.
- `curl` — supplementary download.
- `urllib.request` — NCBI E-utils.
- No pip installs required.
- Argo LLM proxy `http://127.0.0.1:44497` (`api_key=stevens`) — GPT-5.2 for LLM-judge scoring.

## Not fetched (out of scope for this replication)

- **PATRIC/BV-BRC 1595 strain assemblies** (~4 GB) — the paper's raw input. Would enable full SVM refit but not needed for the level of verification achieved here. PATRIC → BV-BRC migration (2022) would also require ID crosswalk.
- **RCSB PDB structures** referenced by the paper's structural analysis section — not required to verify the ML claims.
- Original code repository: **not identified** — the paper does not cite a GitHub URL in either the abstract or Methods section preview. May exist internal to SBRG (Palsson lab) but not publicly linked from the paper.
