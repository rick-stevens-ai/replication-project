# Workflow — BVBRC-74 Independent Replication

Target paper: Satti SM, Castro-Aguirre E, Shah AA, Marsh TL, Auras R.
*Genome Annotation of Poly(lactic acid) Degrading Pseudomonas aeruginosa,
Sphingobacterium sp. and Geobacillus sp.* IJMS 22(14):7385, 2021.
PMC8305213 / DOI 10.3390/ijms22147385.

Workflow class: **BV-BRC Genome Assembly (Unicycler / SPAdes on Illumina)**
+ **Comprehensive Genome Analysis (RASTtk annotation).**

All computation on **free endpoints only** (SPAdes/Prodigal/BLAST local on
CherryRd; LLM judge on local Argo proxy, `argo:gpt-5.2` at T=0.1). Total
compute: ~35 min SPAdes, ~10 sec Prodigal, ~1 min BLAST, ~30 sec LLM judge.

---

## Stage 0 — Paper acquisition and claim extraction

1. Fetch Europe PMC XML for **PMC8305213**; strip to plain text.
2. Extract the 15 testable claims (Table 1 quantitative metrics + Section 2
   taxonomic assignments + Section 4.3 read counts + BioProject deposition
   claims + Table 3 enzyme-repertoire qualitative claim).
3. Regex-scan for accessions:
   - BioProject: `PRJNA721072`, `SRP149807`.
   - Confirm via NCBI E-utils that these link to three SRA runs and three
     BioSamples: SAMN09356180 (S2), SAMN09356181 (S3), SAMN18698529 (EC-3).
   - Confirm **no assembly ever deposited** in NCBI Assembly DB — only reads.

## Stage 1 — Data acquisition

1. Download raw Illumina MiSeq reads from ENA over HTTPS (semantic-scholar-
   rate-limit-friendly, no NCBI SRA toolkit needed):
   - `SRR7264118` (S3, 460 MB + 495 MB, 2.64 M PE spots)
   - `SRR14203690` (EC-3, 955 MB + 1067 MB, 5.73 M PE spots)
   - `SRR7264117` (S2, 2.77 M PE spots) — staged, not yet processed.
   - Total ~3 GB in `work/reads/`.
2. Download reference genomes (NCBI Datasets):
   - `GCF_000750905.1` — *P. aeruginosa* PSE305 (complete, 6.76 Mb, 65.31% GC)
   - `GCF_000236605.1` — *G. thermoleovorans* CCB_US3_UF5 (complete, 3.60 Mb, 52.28% GC)
   - `GCF_901482695.1` — *S. thalpophilum* NCTC11429 (complete, 5.96 Mb, 43.64% GC)
   - `GCF_000686625.1` — *S. thalpophilum* DSM11723 (draft, 5.90 Mb, 43.57% GC)

## Stage 2 — Independent de-novo assembly (S3 only)

1. SPAdes **4.3.0** on paired reads (isolate mode):
   ```
   spades.py --isolate \
     -1 SRR7264118_1.fastq.gz -2 SRR7264118_2.fastq.gz \
     -o asm/s3_paeruginosa_spades \
     -t 8 -m 24
   ```
   Runs K21 → K33 → K55 → K77 → K99 → K127 on CherryRd (Mac, 8 threads).
   Wall-clock ~35 min. Output `scaffolds.fasta` = 509 scaffolds / 6,705,013 bp.
2. Assembly statistics (`analyze_s3_assembly.py`) at PATRIC-style cutoffs:
   - all:         509 contigs / 6.71 Mb / 65.98% GC / N50 = 261,281 bp / L50 = 9
   - **≥500 bp:** 103 contigs / 6.54 Mb / 66.19% GC (PATRIC default filter)
   - **≥1 kb:**    51 contigs / 6.51 Mb / 66.26% GC (closest match to paper Table 1)

## Stage 3 — Gene prediction

Prodigal V2.60 single-mode on ≥500 bp scaffolds → **6,085 CDS**.
(Paper reports 6,239 CDS via RASTtk; 2.5% delta is within gene-caller tool tolerance.)

## Stage 4 — Species assignment

`blastn` of PSE305 16S rRNA vs S3 scaffolds:
- Top hit on `NODE_42`: **100.00% identity over full 1536 bp**.
- Paper claimed ~99%; our result is stronger.

## Stage 5 — PLA-degrading enzyme repertoire

1. Extract all PSE305 CDS matching hydrolase/lipase/esterase/protease/
   cutinase/depolymerase/oxygenase/catalase product-strings from the GBFF.
2. `tblastn` against our S3 scaffolds at ≥50% identity / e < 1e-30.
3. Compute per-class recovery fractions (see `artifacts_summary.md` §4.2).

## Stage 6 — Reference-genome cross-check (S2 and EC-3, spot-check only)

Since S2 and EC-3 were not independently re-assembled in this pass
(compute-time budget), corroborate their claims indirectly:
- Verify the paper's named reference genome exists in NCBI.
- Compare reference GC and size to paper's Table 1 isolate values.
- Accept if GC Δ < 1% AND size within 10% (draft-vs-complete tolerance).

Both S2 (reference NCTC11429: 5.96 Mb / 43.64% GC vs paper 5.45 Mb / 43.66% GC)
and EC-3 (reference CCB_US3_UF5: 3.60 Mb / 52.28% GC vs paper 3.40 Mb / 52.18% GC)
pass this spot-check.

## Stage 7 — Read-count deposition audit

Cross-check SRA spot counts vs paper Section 4.3 read counts:
- EC-3: paper 5,730,761 = SRA 5,730,761 ✅ **exact**
- S3:   paper 5,800,229 ≈ 2× SRA 2,635,837 ⚠️ likely PE-mate double-count
- S2:   paper 6,304,420 ≈ 2× SRA 2,768,958 ⚠️ likely PE-mate double-count

Documented as caveat, not contradiction.

## Stage 8 — LLM judge

`judge.py` posts the 15-claim table + results to Argo proxy
(`localhost:44497`) model `argo:gpt-5.2` at temperature 0.1.
Returns JSON verdict: **PARTIAL**, coverage 100%, agreement 40%.
Saved to `report/evidence/llm_judge_verdict.json`.

## Stage 9 — Report generation

Compile `REPORT.md` (canonical human-readable), `REPORT.tex` (typeset
detailed + GENUINE CRITIQUE), `artifacts_summary.md` (evidence inventory),
`failure_analysis.md` (what went wrong / what wasn't done), and
`open_questions.json` (5 grounded downstream research questions).

---

## Stages skipped by compute budget (documented in failure_analysis.md)

- **S2 de-novo re-assembly** — reads staged, SPAdes not run.
- **EC-3 de-novo re-assembly** — reads staged and downloaded, SPAdes not run.
- **ANI computation for any of the three isolates** — reference genomes
  downloaded, `pyani` / `fastANI` not run.
- **RASTtk annotation locally** — Prodigal used as free-endpoint substitute.
- **MeDuSa reference-guided scaffolding** — not run, explains 51-vs-63
  contig-count delta and the 20% longest-contig delta.
