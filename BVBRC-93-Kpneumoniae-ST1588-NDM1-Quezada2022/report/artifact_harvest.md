# Artifact Harvest — BVBRC-93

All artifacts pulled 2026-07-04 to `/data/stevens/bvbrc93-kpneu-st1588-independent/` on uicgpu and mirrored under `report/evidence/`.

## Primary sequence data (paper deposit)

| Accession | Description | Length (bp) | Source | Local file |
|---|---|---|---|---|
| JAMJQY000000000 (parent) | K. pneumoniae UCO-361 WGS project | 15 contigs, 5,841,932 bp total | NCBI E-utils | `work/data/UCO361_all_contigs.fasta` (md5 `85adabb6d97992295a31f788fad0a1dc`) |
| NZ_JAMJQY010000001.1 | UCO-361 chromosome (contig 1) | 5,288,551 | NCBI nuccore | (included in FASTA above) |
| NZ_JAMJQY010000002.1 | plasmid pNDM-1_UCO-361 | 314,976 | NCBI nuccore (RefSeq annotated) | `work/data/pNDM1_UCO361.gb` + FASTA |
| NZ_JAMJQY010000003.1 | 197 kb IncFIB(K) plasmid | 197,209 | NCBI nuccore | (in FASTA) |
| NZ_JAMJQY010000004..015.1 | 12 additional small contigs | 385–9,438 | NCBI nuccore | (in FASTA) |
| BioProject PRJNA224116; BioSample SAMN28534325; Assembly GCF_023554495.1 | metadata linkages | — | RefSeq | (in GenBank file) |

## Reference plasmids for comparison

| Accession | Description | Length | Purpose |
|---|---|---|---|
| MN598004.1 | *Enterobacter cloacae* EC12 plasmid pNDM-1-EC12 | 351,777 | Paper's "closest" reference (mash-dist). BLASTed pairwise. |
| CP041388.1 | *K. ornithinolytica* pRAO166a | 382,325 | Paper's "different genetic environment" comparator. BLASTed pairwise. |

## Reference databases used

| DB | Version / date | Source |
|---|---|---|
| PubMLST klebsiella scheme (bundled with `mlst` 2.35.0) | scheme snapshot bundled in mlst 2.35.0 | tseemann/mlst |
| PlasmidFinder DB (enterobacteriales.fsa) | HEAD from bitbucket.org/genomicepidemiology/plasmidfinder_db (2025) | 159 replicon references |
| AMRFinderPlus DB | 2024-07-22.1 | NCBI (via micromamba env) |
| Kleborate DB (kpsc preset) | v3.2.4 bundled | Wyres/Holt lab |
| RefSeq PGAP annotation on the deposited plasmid | 2025-06-23 | NCBI (embedded in GenBank record) |

## Full text

| Item | Source | Local |
|---|---|---|
| Paper JATS XML | EuropePMC PMC9494972/fullTextXML | /tmp/quezada_2022.xml (working copy) |

## Generated analysis outputs (evidence/)

- `mlst_klebsiella.tsv` — Independent MLST call, ST1588 with 7 exact-match alleles.
- `amrfinder_out.tsv` — Independent AMRFinderPlus AMR/stress/virulence gene calls.
- `kleborate_output.txt` — Independent Kleborate kpsc profile (MLST + capsule + O-antigen + AMR + virulence).
- `pfinder_hits.tsv` — Independent BLASTn of the 15 assembly contigs against PlasmidFinder enterobacteriales replicon references.
- `blast_vs_EC12.tsv` — Independent full BLASTn pNDM-1_UCO361 vs MN598004.1.
- `blast_vs_Rornith.tsv` — Independent full BLASTn pNDM-1_UCO361 vs CP041388.1.
- `pfinder_run.sh` / `plasmid_compare.sh` / `local_env.sh` — the exact bash/python scripts run on uicgpu.
- `llm_judge_prompt.py` — full evidence pack + prompt used for the LLM-judge.
- `llm_judge_response.json` — the free-Argo LLM judge's single-line verdict.

## Chain of custody

All primary sequence data downloaded independently through NCBI E-utils (public, unauthenticated) on 2026-07-04 14:09 CDT. Local FASTA md5 recorded (`85adabb6d97992295a31f788fad0a1dc`). No dependence on any prior replication or workspace file — the prior BVBRC-46 dir on uicgpu was only inspected for cross-check, never sourced.
