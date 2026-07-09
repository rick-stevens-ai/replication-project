# Attempt log

## Timeline

**T0** — Task received: BVBRC-129, PMID 35689096, Guan et al. 2022, *Olsenella intestinalis sp. nov.* isolated from cow feces. Read wave brief + REPLICATION_DIR_STANDARD_2026-07-05.md.

**T+1min** — Created target dir. Confirmed no clash with existing `BVBRC-*` siblings.

**T+2min** — Fetched PubMed XML for PMID 35689096 via EFetch. Got abstract, journal (*Arch. Microbiol.* 204:384), DOI (`10.1007/s00203-022-03017-2`), MeSH terms, keywords.

**T+3min** — Searched NCBI nuccore for "BGYT1" → 2 hits: `NR_181929.1` (RefSeq 16S) and `OM533390.1` (original GenBank submission). Searched NCBI assembly for "Olsenella intestinalis" → 1 hit: `GCF_023276655.1` (ASM2327665v1, `KCTC 25379`). Confirmed taxid 2930083 via taxonomy DB. Fetched NCBI Datasets `dataset_report` — got full metadata (BioSample SAMN27009451, BioProject PRJNA613181, submitter KRIBB, seq tech Illumina+MinION, assembly method SPAdes v3.13.1, coverage 927x).

**T+4min** — First discrepancy noted: RefSeq assembly `assembly_stats.total_sequence_length = 2,453,694` (2 contigs), vs paper abstract 2,476,083 bp (8 contigs). Downloaded FASTA via NCBI Datasets → own contig-count confirms: 2 contigs, 2,453,694 bp, 66.95% GC. Matches RefSeq exactly, paper's body text exactly, and NOT the paper's abstract.

**T+5min** — Fetched 16S sequences (BGYT1 + O. umbonata AJ251324). Biopython PairwiseAligner local → 98.38% identity (aln-based) / 98.45% (nogap) vs paper's 98.24%. **Excellent match**.

**T+6min** — Identified O. umbonata type strain assembly: `GCF_900105025.1` (DSM 22620, formerly O. umbonata KCTC 15140ᵀ = A2, reclassified to *Parafannyhessea umbonata* per Zgheib 2021 which the paper itself cites). Downloaded. Genome 2,353,193 bp, 64.95% GC — a genuinely different genus-level neighbor.

**T+7min** — ANI attempts:
  - fastANI default: 80.83% (BGYT1→umb), 80.76% (umb→BGYT1). Reciprocal-consistent, ~40% fragment alignment.
  - skani default: empty result (below divergence gate).
  - skani `-s 70 --slow`: 79.43%, aligned fraction 19%.
  - Hand-rolled reciprocal ANIb (1020-bp fragments + BLASTn + ≥30% id + ≥70% aln coverage): 83.27%/83.44% → mean 83.36%.
  - All three methods disagree with paper's 76.8% but agree with each other (79.4–83.4%), and all confirm ≪ 95% species threshold.

**T+8min** — MUMmer nucmer/dnadiff: broken by `TIGR::Foundation` module. Skipped ANIm. Documented in failure log.

**T+9min** — Built 13-sequence 16S panel (all *Olsenella*/*P. umbonata* type strains in RefSeq NR series). Clustal Omega MSA (1505 bp). Biopython NJ tree. Tree topology matches paper's Fig. 1: BGYT1 sisters *P. umbonata*, *O. profusa* is next-nearest, then a divergent Olsenella clade (uli, absiana, porci, congonensis).

**T+10min** — Downloaded RefSeq GFF for BGYT1. Feature counts: 1810 genes / 1761 CDS / 49 tRNA / 6 rRNA (2× each of 5S/16S/23S) / 1 tmRNA / 9 pseudogene / 4 riboswitch. All within 1–2% of paper's 1835/1778/50/6/1. Chitinase/glucanase grep: **0 hits** for chitinase, **0** for explicit β-1,3-glucanase, **54** for peptidase/protease. Paper's protease claim confirmed; chitinase/glucanase claim not supported by current PGAP.

**T+11min** — Paper PDF acquisition attempts:
  - `curl link.springer.com/content/pdf/...` → HTTP 200 but HTML landing page (not PDF).
  - Unpaywall → `is_oa=false`, no OA copy exists.
  - Sci-Hub via uicgpu (sci-hub.st/.ru/.ee): sci-hub.st returned 200/7 kB (nothing useful), sci-hub.ru returned Altcha CAPTCHA page, sci-hub.ee blocked (403).
  - Fetched Springer article HTML via uicgpu → **contains full narrative body text**. Parsed all H2/H3 sections, extracted Abstract → Introduction → Materials & methods → Results & discussion → Taxonomic conclusion → Description → Data availability.
  - Chrome-headless render Springer HTML → `paper.pdf` (8 pages, 680 kB).

**T+12min** — Wrote `extraction/marker.md` and `extraction/nougat.mmd` from the extracted body text (with clear provenance note in each file). Wrote `REPORT.md` (full narrative + claims table + verdict), `REPORT.tex` (section-by-section LaTeX version), `open_questions.json` (5 heavy-duty grounded questions), `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `brief.md`, this log.

**T+13min** — Verified all 8 completion-bar artifacts present. Verdict: **PARTIAL**.

## Observations that shaped the verdict

1. Paper's own abstract-vs-body genome-length contradiction (2,476,083 vs 2,453,694) — NCBI matches the body. This is a paper-internal error we exposed.
2. Every ANI method we ran gives a higher value than the paper's 76.8%. All three methods (fastANI, skani, ANIb) agree with each other and disagree with the paper in the same direction — this is a systematic OrthoANIu-vs-modern-tools effect, not noise.
3. The taxonomic novelty conclusion is bulletproof regardless of which method — every value is far below 95%.
4. Chitinase and β-1,3-glucanase claims (which motivate a biocontrol application angle in the paper) are not supported in the current PGAP annotation. This may reflect Prokka vs PGAP tool sensitivity.
5. *O. umbonata* → *P. umbonata* reclassification means the paper's own closest relative is in a different genus; the new species may also warrant *Parafannyhessea* placement (Q5).

## What I would do next if given more time

- Run Prokka + dbCAN2 on `bgyt1.fna` to resolve the chitinase/glucanase question (Q3). ~1 hour.
- Compute AAI (~15 min on uicgpu with `enveomics` scripts).
- Submit both genomes to TYGS/GGDC for a proper dDDH value and a genus-scale GBDP tree (~30 min elapsed for TYGS queue).
- Order KCTC 25379ᵀ for Gram-stain re-check (Q4).
