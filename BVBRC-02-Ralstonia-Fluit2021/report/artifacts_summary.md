# Artifacts Summary — BVBRC-02-Ralstonia-Fluit2021

Enumerates every artefact referenced by `report/REPORT.md`. Split by pass so
provenance is unambiguous. Sizes / paths are logical (per REPORT.md); this file
does not itself inspect the filesystem.

## Paper / provenance

| Path                                    | Origin | Description |
|-----------------------------------------|--------|-------------|
| `paper/paper.pdf`                       | pass-2 | Self-sourced full-text PDF, 1.29 MB, 8 pages, fetched from `https://europepmc.org/articles/PMC8448721?pdf=render` (PMC native was proof-of-work challenged). |
| `paper/paper.txt`                       | pass-2 | `pdftotext -layout` extraction of `paper.pdf`. Basis for pass-2 claim re-check. |
| `paper/paper_notes.md`                  | pass-1 | Hand-curated abstract + table 1 notes; pass-1 relied on this in absence of full PDF. |
| `PARSER_PROVENANCE.md`                  | pass-2 | Trail: what parsed what, when, and with what tool. |

## Input data

| Path                                    | Origin | Description |
|-----------------------------------------|--------|-------------|
| `data/sra/`                             | pass-1 | 18 clinical *Ralstonia* SRA read pairs (Illumina NextSeq). |
| `data/genomes/`                         | pass-1 | 18 assembled genome FASTA files (SPAdes v4.2.0 `--only-assembler`, ≥500 bp). |
| `data/strain_info.tsv`                  | pass-1 | Per-strain metadata (species assignment, group). |
| `data/resfinder_db/`                    | pass-1 | ResFinder acquired-AMR database snapshot. |
| `data/refs/Rpickettii_16S.fna`          | pass-2 | *R. pickettii* ATCC 27511 16S rRNA (GenBank `NR_043152.1`, 1491 bp). |
| `data/refs/Rmannitolilytica_16S.fna`    | pass-2 | *R. mannitolilytica* 16S rRNA reference. |
| `data/refs/OXA-22.faa`                  | pass-2 | OXA-22 protein reference (`AAD12233.1`, 326 aa). |
| `data/refs/OXA-60.faa`                  | pass-2 | OXA-60 protein reference (`YFD08942.1`, 271 aa). |

## Analysis outputs

| Path                                    | Origin | Description |
|-----------------------------------------|--------|-------------|
| `analysis/ani/`                         | pass-1 | `pyani` ANIb BLAST files + distance matrix over the 18 assemblies. Basis for Claims 5–7. |
| `analysis/resfinder/`                   | pass-1 | Per-strain ResFinder BLAST results. Basis for Claims 3 and 4. |
| `results/repass/16S.fasta`              | pass-2 | Extracted 16S sequences (18 strains, including 4 stitched from split contigs). |
| `results/repass/OXA22.fasta`            | pass-2 | Extracted OXA-22 family nucleotide/protein sequences (18 strains). |
| `results/repass/OXA60.fasta`            | pass-2 | Extracted OXA-60 family nucleotide/protein sequences (18 strains). |
| `results/repass/16S.aln.fasta`          | pass-2 | MAFFT alignment, 1491 columns. |
| `results/repass/OXA22.aln.fasta`        | pass-2 | MAFFT alignment, 278 columns (paper: 279). |
| `results/repass/OXA60.aln.fasta`        | pass-2 | MAFFT alignment, **271 columns (paper: 271, exact match)**. |
| `results/repass/16S.nwk`                | pass-2 | FastTree GTR ML tree (Newick), 18 tips. |
| `results/repass/OXA22.nwk`              | pass-2 | FastTree JTT ML tree, 18 tips. |
| `results/repass/OXA60.nwk`              | pass-2 | FastTree JTT ML tree, 18 tips. |
| `results/repass/16S.fasttree.log`       | pass-2 | FastTree run log, GTR model, log-likelihood ~ −2351.7 (not directly comparable to paper's −2740.49 because different tip set). |
| `results/repass/OXA22.fasttree.log`     | pass-2 | FastTree run log. |
| `results/repass/OXA60.fasttree.log`     | pass-2 | FastTree run log. |
| `results/repass/extract_summary.json`   | pass-2 | Per-strain hit metadata: pident, coverage, contig, region for 16S / OXA-22 / OXA-60. Key numbers: OXA-22 pident 84.3–100.0% (mean 91.6%); OXA-60 pident 84.9–95.2% (mean 92.7%). |
| `results/repass/tree_validation.json`   | pass-2 | Per-group monophyly verdicts (D1, D2, E1, E2, F, G) for each of the 3 trees. |

## Code

| Path                                    | Origin | Description |
|-----------------------------------------|--------|-------------|
| `code/repass/extract_and_tree.py`       | pass-2 | Extraction driver: blastn/tblastn against the 4 reference files; emits per-family FASTA + `extract_summary.json`. |
| `code/repass/rescue_16S.py`             | pass-2 | Stitches non-overlapping 16S fragments across short SPAdes contigs (fix for the 4 R. pickettii strains whose 16S was split). |
| `code/repass/build_trees.sh`            | pass-2 | Wrapper: `mafft --auto` → `FastTree` for each of 16S / OXA-22 / OXA-60. |
| `code/repass/validate_trees.py`         | pass-2 | Custom Newick parser + per-group monophyly check; writes `tree_validation.json`. |

## Reports

| Path                                    | Origin | Description |
|-----------------------------------------|--------|-------------|
| `report/REPORT.md`                      | pass-2 | Main report (18 KB). Verdict: PARTIAL, coverage 8/10, agreement 8/10, 0 contradictions. |
| `report/REPORT.pass1.md`                | pass-1 | Pass-1 report preserved verbatim for diff/audit. Original verdict: PARTIAL, coverage 6/10, agreement 8/10. |
| `report/REPORT.tex`                     | pass-2 | LaTeX version of the pass-2 report with a dedicated Genuine Critique section. |
| `report/open_questions.json`            | pass-2 | 5 open scientific questions (clinical metadata linkage, AMR panel completeness at expanded set, phylogeny sensitivity to reference choice, virulence-factor annotation across R. pickettii vs R. mannitolilytica, host-pathogen adaptation signals in accessory genome). |
| `report/workflow.md`                    | pass-2 | Reconstructed 2-pass pipeline description. |
| `report/artifacts_summary.md`           | pass-2 | This file. |
| `report/failure_analysis.md`            | pass-2 | What did not replicate, why, and how it could. |

## Tool / environment inventory (per REPORT.md §2)

- BLAST+ 2.x (`/usr/local/bin/blastn`, `/usr/local/bin/tblastn`)
- MAFFT 7.526 (Homebrew)
- FastTree 2.1.11 (Homebrew `brewsci/bio`)
- Python 3 + Biopython 1.87 (Biopython used only via pre-existing tooling;
  pass-2 scripts use stdlib + `subprocess` only)
- SPAdes v4.2.0 for pass-1 assembly (paper used v3.11.1)
- `pyani` for ANIb
- `pdftotext -layout` for PDF extraction

## Summary counts

- **Genomes analysed:** 18 (paper cohort). Full ANIb reference set (~78) not attempted.
- **Reference sequences pulled (pass-2):** 4 files, 4 accessions.
- **Alignments built:** 3 (16S 1491 cols; OXA-22 278 cols; OXA-60 271 cols).
- **Trees built:** 3 (all FastTree ML, 18 tips each).
- **JSON outputs:** 2 (`extract_summary.json`, `tree_validation.json`).
- **Scripts added (pass-2):** 4 (`extract_and_tree.py`, `rescue_16S.py`,
  `build_trees.sh`, `validate_trees.py`).
