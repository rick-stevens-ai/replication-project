# Artifact Harvest — OSTI 2470381 (UNNT)

## Paper
| Artifact | URL | Size | SHA-256 (16 hex) |
|---|---|---|---|
| PDF (OSTI Open-Access purl) | https://www.osti.gov/servlets/purl/2470381 | 456,529 B | `80fcdaf83356718f` |
| PLoS Comput Biol DOI | https://doi.org/10.1371/journal.pcbi.1011504 | (canonical) | — |

Retrieval note: `curl` from CherryRd times out on `osti.gov`; the fetch was routed through `ssh uicgpu` (which reaches osti.gov via the standard proxy in `~/env.sh`).

## Code — GitHub `vgutta/UNNT`
- URL: https://github.com/vgutta/UNNT.git
- Commit at replication: `c34567b1c9595879a0eade8cb641c7630b69a7ed` ("update readme and remove files")
- License: MIT

## Bundled data (`data/` in the repo)
| File | Size (B) | SHA-256 (16 hex) | Role |
|---|---|---|---|
| `cell_exp_nci.tsv` | 18,330,851 | `eed9a75bc5b1c4f3` | NCI60 RNA-seq expression (cell × ~5,000 genes), 60 rows |
| `lincs1000.tsv` | 76,918 | `aa5d7fa7ed2745a8` | LINCS 1000 landmark-gene symbols to keep from expression |
| `fda_drug_desc.tsv` | 3,772,716 | `cbf24fa54bf23f10` | Dragon 7.0 molecular descriptors for FDA-approved drug list |
| `nci_fda_drugs.csv` | 14,007 | `524887f97eb9fd3d` | FDA-approved drug NSC list |
| `nci_fda_drug_response.tsv` | 3,859,243 | `bad1ad54dce72921` | AUC drug-response labels (drug × cell) |
| `val_data_nci60.csv` | 87,188,460 | `aa71854a18d289ac` | Held-out validation split (new cell lines) |
| `val_nci60_cell.csv` | 46 | `7d4e97ce712583ae` | List of validation cell-line names |
| `val_nci60_fda_drugs.csv` | 110 | `40f535bffecd4d71` | Small FDA drug list for validation |

Original data provenance per paper §Data:
- RNA-seq expression: NCI60 CellMiner processed dataset (Reinhold, https://discover.nci.nih.gov/cellminer/…). Batch-corrected with ComBat-seq.
- Drug response (AUC): MoDaC `combined_single_response_agg` (JDACS4C Pilot 1). Hill-slope normalized.
- Drug descriptors: MoDaC `descriptors.2D-NSC.5dose.filtered.txt` — computed with Dragon 7.0.

## LLM-judge endpoint used
- Argo proxy free endpoint (`http://localhost:44497/v1`, key=`stevens`), model `argo:gpt-5.2` (default free Argo judge per WAVE brief). Judge run recorded in `report/evidence/llm_judge_verdict.json`.
