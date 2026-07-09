# Workflow — BVBRC-38 Gen2Epi *N. gonorrhoeae* AMR Replication

Method reproduction of the Gen2Epi pipeline (Sundaraj Suchindran et al., *BMC Genomics* 2019, DOI 10.1186/s12864-019-5542-3). We did **not** run the shipped CentOS-7 VirtualBox image; we independently re-implemented the paper's method using the same tool families (BLAST+, SPAdes, fastp/Trimmomatic-equivalent, Biopython, pubMLST).

Replication target: the **11 WHO 2016 reference strains** (WHO F, G, K, L, M, N, O, P, X, Y, Z) that Gen2Epi itself used as its validation set (paper's ref 17 = Unemo *et al.* 2016). All data free and public.

## Stage 0 — Paper acquisition
- Fetched full-text XML of Sundaraj Suchindran et al. 2019 from Europe PMC (`fullTextXML`).
- Stored at `work/gen2epi_fulltext.xml` (also mirrored in `report/evidence/`).
- Used to extract the five-module architecture, tool parameters, and Table 1 / Table 2 quantitative results.

## Stage 1 — Reference genome + annotation acquisition
- **11 WHO PacBio finished genomes** from ENA project **PRJEB14020** via the ENA browser FASTA API (`/ena/browser/api/fasta/<GCA>`), one FASTA per strain.
- **FA1090 reference** (GCA/GCF_000006845.1) via NCBI Datasets REST — used as the wild-type source for the AMR/typing reference genes.
- **FA1090 annotation** (CDS/protein/GFF) via NCBI Datasets v2alpha REST — used to locate the seven AMR/typing loci by gene name and coordinates.
- Manifest of downloads recorded in `work/genome_manifest.json`.
- Scripts: `work/fetch_genomes.py`.
- Outputs: `work/genomes/WHO_{F,G,K,L,M,N,O,P,X,Y,Z}.fna`, `work/genomes/FA1090.fna`.

## Stage 2 — pubMLST allele + profile snapshot
- Pulled the 7 NG-MLST housekeeping-locus allele FASTAs (abcZ, adk, aroE, fumC, gdh, pdhC, pgm; 1036–1397 alleles each) from the pubMLST Neisseria REST API (`pubmlst_neisseria_seqdef`, scheme 1).
- Pulled the full 18,488-row ST profile table (allele vector → ST).
- Outputs: `work/alleles/*.fas`, `work/alleles/profiles_mlst.tsv`.

## Stage 3 — Wild-type reference-gene extraction (for AMR determinant detection)
- `work/extract_refgenes.py` pulls wild-type coding sequences for the six protein-coding AMR/typing loci from the FA1090 CDS set:
  - **penA** (PBP2 / FtsI)
  - **gyrA**, **parC** (fluoroquinolone QRDR)
  - **ponA** (PBP1A)
  - **mtrR** (efflux repressor)
  - **porB** (penB locus)
- Plus **23S rRNA** by FA1090 genome coordinates (macrolide-resistance locus).
- Outputs: `work/refgenes/*.fna`.

## Stage 4 — Assembly statistics (Claim C1a)
- `work/genome_stats.py` (Biopython): per-genome contig count, total length, longest scaffold, GC%, N50; median across the 11-strain panel.
- Compared to paper Table 1 (WHO column, median).
- Output: `work/genome_stats.json` → `report/evidence/genome_stats.json`.
- **Result:** median chromosome length 2,172,826 bp, GC 52.52%, N50 chromosome-level — matches Table 1 (2,167,463 bp, 52.64%).

## Stage 5 — NG-MLST typing (Claim C2)
- `work/mlst_typing.py`:
  1. `makeblastdb` on each WHO genome FASTA.
  2. `blastn` each of the 7 locus allele FASTAs against each genome database.
  3. Select the exact allele per locus (100% identity, 100% length).
  4. Map the resulting 7-allele vector to an ST via the pubMLST profile table.
- Output: `work/mlst_results.json` → `report/evidence/mlst_results.json`.
- **Result:** 11/11 strains resolved to a defined ST with full 7/7 allele profiles (paper Table 2 reported 9/9 for WHO NG-MLST; we resolved 11/11 because two WHO strains' STs are now in the profile table).

## Stage 6 — NG-STAR AMR-determinant detection (Claim C3)
- `work/amr_detect.py`:
  1. `blastn` each reference gene (from Stage 3) vs each WHO genome.
  2. Extract the best-hit region.
  3. Translate (genetic code table 11) and align to the wild-type protein via BLOSUM62 global alignment (robust to indels).
  4. Read canonical resistance codons:
     - **gyrA** S91, D95 (fluoroquinolone QRDR)
     - **parC** S87, S88, E91 (FQ QRDR)
     - **penA** — **mosaic call by nucleotide identity** (<96% vs FA1090 wt = mosaic PBP2 → ESC/penicillin R)
     - **ponA** L421 (penicillin R)
     - **mtrR** A39, G45 (efflux → azithromycin/tetracycline)
     - **porB** G120, A121 (*penB* → penicillin/tetracycline)
- `work/rrna23S_azithro.py` counts full-length 23S rRNA copies per genome (should be 4 for a complete assembly; occasional loss under scaffold filtering on low-quality inputs).
- Outputs: `work/amr_results.json`, `work/rrna23S_results.json` → `report/evidence/`.
- **Result:** all 7 loci recovered for all 11 strains; all 4 23S operons recovered in every genome.

## Stage 7 — Biological validation vs known phenotypes (Claim C3b)
- Cross-referenced each strain's determinant profile with the published Unemo 2016 WHO-panel phenotypes.
- **Key check:** the three ceftriaxone-resistant strains (WHO X = H041, WHO Y = F89, WHO Z = A8806 — the clinically famous XDR gonococci) should carry mosaic penA in our detection; the pan-susceptible reference WHO F should carry wild-type penA with no QRDR mutations.
- **Result:** all six spot-checks concordant (WHO F pan-susceptible; WHO P penicillin I; WHO K/L CMRNG; WHO X/Y/Z ceftriaxone-R with mosaic penA + QRDR + ponA + penB).

## Stage 8 — Live end-to-end de-novo assembly (Claims C1b + C4)
Run on **uicgpu**, conda env `/data/stevens/envs/bvbrc38` (SPAdes 4.3.0, fastp 1.3.6, BLAST 2.17).
- Input: **WHO_F Illumina paired reads ERR5860304** (1.31M pairs, 343 Mb) from ENA fastq FTP.
- Pipeline mirroring Gen2Epi steps 1–2:
  1. **fastp Q15 trim** (equivalent to the paper's Trimmomatic Q15 stage).
  2. **SPAdes 4.3.0** `--careful -k 21,33,55,77,99,127 --cov-cutoff auto` (exact paper params).
- `work/denovo_type_amr.py` then re-runs NG-MLST + penA detection on the resulting scaffolds and compares to the finished WHO_F reference.
- Outputs: `work/assembly/WHO_F_denovo.fna`, `work/assembly/spades.log`, `work/assembly/fastp.json`, `work/denovo_results.json` → `report/evidence/denovo_results.json`.
- **Result:** 2,197,379 bp / 52.30% GC / **99.96% genome fraction** vs WHO_F reference; N50 64,607 bp (pre-scaffolding). NG-MLST returns **ST 10934** (same as finished WHO_F reference) with full 7/7 profile; penA non-mosaic (99.657%) — identical to the finished reference. **The paper's core loop is closed.**

## Stage 9 — LLM-judge scoring (free Argo)
- `work/llm_judge.py` fed the full evidence package (all JSON outputs + tables) to `argo:gpt-5.2` on the free Argo proxy (key=stevens, opus fallback).
- Verdict was elicited as a structured judgment on coverage / agreement — **never regex-scored**.
- Output: `report/evidence/llm_judge_verdict.txt`.
- **Result:** VERDICT REPLICATED, Coverage 8/10, Agreement 9/10.

## Stage 10 — Report authoring
- Consolidated all stages into `report/REPORT.md` and this workflow document (`report/workflow.md`).
- Companion artifacts: `report/artifacts_summary.md`, `report/failure_analysis.md`, `report/open_questions.json`, `report/REPORT.tex`.
- Canonical verdict recorded as **PARTIAL REPLICATION (strong; near-REPLICATED)** — conservative label because the scope is the 11-strain WHO reference panel rather than the full 1484-sample paper cohort, and the Ragout scaffolding module was not run.

## Compute footprint

| Stage | Host | Wall time |
|---|---|---|
| Data acquisition (Stages 1–3) | laptop | ~5 min (network-bound) |
| Assembly stats + typing + AMR (Stages 4–7) | laptop | ~2 min BLAST |
| De-novo assembly (Stage 8) | uicgpu (16 cores) | ~5 min SPAdes |
| LLM judge (Stage 9) | free Argo proxy | seconds |

Total end-to-end: order of minutes, all free.

## Reproduction script (post-download)

```bash
python3 fetch_genomes.py       # Stage 1
python3 extract_refgenes.py    # Stage 3
python3 mlst_typing.py         # Stage 5
python3 amr_detect.py          # Stage 6
python3 rrna23S_azithro.py     # Stage 6
python3 genome_stats.py        # Stage 4
# Then, on uicgpu:
# fastp Q15 trim on ERR5860304
# spades.py --careful -k 21,33,55,77,99,127 --cov-cutoff auto
python3 denovo_type_amr.py     # Stage 8
python3 llm_judge.py           # Stage 9
```

All inputs free and public; no paid data or software.
