# Artifacts Summary — BVBRC-104

Inventory of every artifact produced/pulled + traces of the replication.

## 1. Paper (item 1 of 8-artifact standard)

| Path | Source | Size | Notes |
|---|---|---|---|
| `paper.pdf` | MDPI open access (CC BY 4.0, https://www.mdpi.com/2079-6382/12/10/1519/pdf) | backfilled 2026-07-05 | 8-artifact backfill pass; direct MDPI PDF (not the HTML that was blocked) |
| `work/paper_pmc.xml` | NCBI E-utils `efetch db=pmc id=10604428 rettype=xml` | 124,828 bytes | JATS XML full text |
| `work/paper_text.md` | Python 3.14 ET parse of `paper_pmc.xml` | 26,853 bytes | Plain-text extraction of abstract + all sections + methods; source of truth for re-reading |
| `work/pubmed_meta.json` | eutils esummary | 2,113 bytes | PubMed record metadata |
| `work/pmc_link.json` | eutils elink | 291 bytes | PubMed→PMC linkage record |
| `work/abstract.txt` | first section of `paper_text.md` | 1,347 bytes | Standalone abstract |

## 2 & 3. Marker / Nougat extractions (items 2, 3 of 8-artifact standard)

| Path | Source | Status |
|---|---|---|
| `extraction/marker.md` | `pdftotext -layout paper.pdf` fallback (2026-07-05 backfill) | Fallback extraction; central Marker corpus pull pending sha256 resolution |
| `extraction/nougat.mmd` | Header stub with sha256 pointer for later corpus sweep | **Pending** central Nougat parse (GPU-only on Polaris) |

Notes:
- Central Eagle corpora (`/eagle/projects/AuroraGPT/stevens/scout_corpus/{md,mmd}/<sha256>.{md,mmd}` and `.../osti_marker/...`) were not queried live in this pass (Polaris auth + 90 s PDF-fetch cap); a follow-up corpus sweep should resolve by sha256(paper.pdf).
- pdftotext extraction is a valid marker fallback per the brief (`extraction/marker.md` header records the fallback status).

## 4–8. Report artifacts (items 4–8 of 8-artifact standard)

| Path | Purpose | Status |
|---|---|---|
| `report/REPORT.tex` | Detailed LaTeX section-by-section report with genuine critique | ✅ Written 2026-07-05 backfill |
| `report/REPORT.pdf` | pdflatex compile of REPORT.tex | Attempted; leave .tex only if latex missing (per brief) |
| `report/REPORT.md` | Original markdown report (kept per standard) | ✅ Original run 2026-07-05 |
| `report/open_questions.json` | 5 heavy-duty grounded open questions with next steps | ✅ Written 2026-07-05 backfill |
| `report/workflow.md` | Workflow narrative + tools + effort | ✅ Written 2026-07-05 backfill |
| `report/artifacts_summary.md` | This file | ✅ Written 2026-07-05 backfill |
| `report/failure_analysis.md` | Honest failure/gap analysis + critique | ✅ Written 2026-07-05 backfill |
| `report/brief.md` | Compact one-paragraph brief | ✅ Original |
| `report/attempt_log.md` | Chronological execution log | ✅ Original |
| `report/artifact_harvest.md` | Detailed URL/accession/tool provenance | ✅ Original |

## Strain assembly (BioProject PRJNA1012593)

| Accession | Molecule | Length (bp) | Local path | Source |
|---|---|---:|---|---|
| CP134085.1 | Chromosome | 4,967,063 | `work/genomes/CP134085.fasta` | efetch nuccore |
| CP134086.1 | Plasmid pEc45-2020-101kb | 101,848 | `work/genomes/CP134086.fasta` | efetch nuccore |
| CP134087.1 | Plasmid pEc45-2020-190kb | 190,488 | `work/genomes/CP134087.fasta` | efetch nuccore |
| CP134088.1 | Plasmid pEc45-2020-254kb (IncH MDR) | 254,224 | `work/genomes/CP134088.fasta` | efetch nuccore |
| CP134089.1 | Plasmid pEc45-2020-33kb (IncX4, mcr-1) | 33,541 | `work/genomes/CP134089.fasta` | efetch nuccore |
| CP134090.1 | Plasmid pEc45-2020-5kb | 5,714 | `work/genomes/CP134090.fasta` | efetch nuccore |
| — | Combined | 5,632,718 (bytes on disk) | `work/genomes/Ec45-2020_all.fasta` | cat |

## Reference proteins + plasmid refs

| Accession | Product | Local path |
|---|---|---|
| WP_049589868.1 | MCR-1.1 phosphoethanolamine–lipid A transferase (541 aa) | `work/mcr1_ref.faa` |

Reference IncX4/mcr-1 plasmid set for backbone-conservation BLAST (17 accessions, 30–40 kb, complete):
CP075733.1, CP195929.1, CP017246.1, CP046418.1, MK940857.1, MK940858.1, KY964067.1, MF136779.1,
CP064013.1, CP064014.1, CP064009.1, CP064021.1, CP064023.1, CP064007.1, CP048826.1, KX711707.1,
KX711708.1. Combined FASTA on uicgpu at `/data/stevens/scratch/bvbrc104/refs2/all_incx4.fasta`
(~570 KB). Not mirrored locally (staged on uicgpu scratch).

## Evidence files (report/evidence/)

| File | Size | Content |
|---|---:|---|
| `amrfinder_full.tsv` | 11,794 B | AMRFinderPlus 4.2.7 full 53-hit output across CP134085–CP134090 |
| `amrfinder.log` | 597 B | AMRFinderPlus run log (DB version, options, wall clock) |
| `mlst_warwick.tsv` | 103 B | mlst 2.33.1 `--scheme ecoli_achtman_4` → ST162 |
| `mlst_pasteur.tsv` | 110 B | mlst 2.33.1 `--scheme ecoli` (Pasteur, control) → ST355 |
| `plasmidfinder.tsv` | 1,363 B | abricate plasmidfinder hits per contig |
| `serotype.tsv` | 563 B | abricate ecoh hits → O55:H10 |
| `blast_incx4_v1.tsv` | 754 B | First-attempt BLAST vs 3 unfiltered refs (false negative from bad refs; kept for provenance) |
| `blast_incx4_v2.tsv` | 4,029 B | Final BLAST vs 17 filtered IncX4/mcr-1 refs (104 HSPs) |
| `blast_incx4_v2_summary.json` | 1,820 B | Per-subject qcov + weighted pident merged from v2 |
| `llm_judge_prompt.txt` (in work/) | 7,666 B | Full LLM judge prompt |
| `llm_judge_model.txt` | 12 B | `argo:gpt-5.2` (model that returned the verdict after Opus 4.7 502-flap) |
| `llm_judge_verdict.json` | 216 B | JSON verdict + coverage + agreement + confidence |

## Traces

- Wave brief resolved: `/Users/stevens/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`
- Subagent ID (original run): 5106e116
- Backfill brief: `/Users/stevens/Dropbox/REPLICATE-PROJECT/scripts/BACKFILL_BRIEF_2026-07-05.md`
- Standard: `/Users/stevens/Dropbox/REPLICATE-PROJECT/scripts/REPLICATION_DIR_STANDARD_2026-07-05.md`
- uicgpu scratch (not mirrored back to Dropbox): `/data/stevens/scratch/bvbrc104/`
  (contains combined FASTA, BLAST DB, ref FASTAs, mlst/amrfinder/abricate raw stdout).
- Argo endpoint: `http://127.0.0.1:44497/v1/chat/completions` (localhost tunnel, key `stevens`).

## Checksums (paper.pdf)

To be populated by post-download `sha256sum paper.pdf > paper.sha256`; expected format:
```
<64 hex>  paper.pdf
```
Used later by the central corpus resolver to pull the Marker.md and Nougat.mmd from the Eagle
manifests.
