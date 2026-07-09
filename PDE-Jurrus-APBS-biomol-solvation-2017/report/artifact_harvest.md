# Artifact Harvest — Jurrus-APBS-2017

Every public artifact pulled during this replication, with source URL, size, and provenance.

## Paper
| Artifact | URL | Size | Notes |
|---|---|---|---|
| paper.pdf | https://europepmc.org/articles/PMC5734301?pdf=render | 1,711,819 B | PDF v1.5, zip-deflate. Downloaded via ssh uicgpu (Cloudflare blocks direct fetch from CherryRd). |

## Structural data (PDB, public domain)
| Artifact | URL | Size | Notes |
|---|---|---|---|
| 1FAS.pdb | https://files.rcsb.org/download/1FAS.pdb | 75,816 B | Fasciculin-2, 470 heavy atoms. Paper's Fig 4/5 demo protein. |
| 1CRN.pdb | https://files.rcsb.org/download/1CRN.pdb | 49,491 B | Crambin, 327 heavy atoms, net-neutral. |

## Software (conda-forge)
| Package | Version | Location |
|---|---|---|
| APBS | 3.4.1 | /data/stevens/envs/apbs-repl/bin/apbs (uicgpu) |
| PDB2PQR | 3.6.1 | /data/stevens/envs/apbs-repl/bin/pdb2pqr30 |
| Python | 3.10 | in same env |
| marker | 1.x | /data/stevens/envs/marker |
| nougat | 0.1 | /gpustor/stevens/anaconda3/envs/nougat |

## Derived files (this run)
| File | Size | Description |
|---|---|---|
| work/1fas.pqr | 85,967 B | PDB2PQR output (AMBER FF), 1228 atoms |
| work/1crn.pqr | 44,947 B | PDB2PQR output (AMBER FF), 642 atoms |
| work/1fas.in | 419 B | pdb2pqr30 auto-generated APBS input |
| work/1crn.in | 417 B | pdb2pqr30 auto-generated APBS input |
| work/1crn_salt.in | ~530 B | LPBE + 0.15 M NaCl |
| work/1fas_npbe.in | ~530 B | NPBE + 0.15 M NaCl |
| work/1fas_pot.dx | 21,579,321 B | OpenDX potential grid, 1.6M points |
| work/1crn_pot.dx | 12,562,609 B | OpenDX potential grid, 912k points |
| work/1fas.apbs.log | ~4 KB | Full APBS stdout |
| work/1crn.apbs.log | ~4 KB | |
| work/1crn_salt.log | ~4 KB | |
| work/1fas_npbe.log | ~4 KB | |

## Extraction
| File | Size / lines | Method |
|---|---|---|
| extraction/marker.md | 555 lines | marker 1.x on uicgpu (51 s) |
| extraction/nougat.mmd | 415 lines | nougat 0.1 on uicgpu GPU 6 (19 s) |

## Evidence (subset in report/)
| File | Description |
|---|---|
| report/evidence/potential_stats.json | Grid min/max/mean/std for 1FAS + 1CRN |
| report/evidence/1fas.apbs.log | APBS full log for 1FAS baseline run |
| report/evidence/1crn.apbs.log | APBS full log for 1CRN baseline run |
| report/evidence/1crn_salt.log | APBS log for 0.15 M NaCl run |
| report/evidence/1fas_npbe.log | APBS log for NPBE run |
| report/evidence/1fas.pqr | Prepared PQR (input evidence) |
| report/evidence/1crn.pqr | Prepared PQR |
| report/evidence/1fas.in | APBS input |
| report/evidence/1crn.in | APBS input |
| report/evidence/1crn_salt.in | APBS input (salt) |
| report/evidence/1fas_npbe.in | APBS input (NPBE) |
| report/evidence/llm_judge_argo.json | LLM judge output (argo:gpt-5.2, PARTIAL) |

## LLM endpoints used (free per project rules)
- LiteLLM aggregator: http://<tailnet-aggregator>:4000/v1
  - argo:claude-opus-4.7 → 502 (endpoint intermittent)
  - argo:claude-opus-4.8 → 502
  - argo:gpt-5.2 → success (used for verdict)
