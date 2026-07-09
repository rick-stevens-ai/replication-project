# Workflow — Subedi et al. (2019) PA34 Replication

**Project:** X-100 replication project, BVBRC set (index 92)
**Paper:** Subedi D, Kohli GS, Vijay AK, Willcox M, Rice SA. *Accessory genome of the multi-drug resistant ocular isolate of Pseudomonas aeruginosa PA34.* **PLoS ONE** 14(4):e0215038 (2019).
**Compute host:** `uicgpu` (8×A100, 255 cores, 2 TB RAM); LLM-judge step driven from `CherryRd` via Argo proxy `127.0.0.1:44497`.
**Working directory:** `/data/stevens/BVBRC-92-PA34/` on uicgpu.

---

## Stage 0 — Scope and claim enumeration
- **Input:** paper metadata + deposited-data pointers (GenBank CP032552 chromosome, MH547560 pMKPA34-1, MH547561 pMKPA34-2; BioProject PRJNA431326; BioSample SAMN08435059; BV-BRC `genome_id` 287.6355).
- **Action:** enumerated 18 discrete claims (C1–C18) covering data availability, genome/plasmid statistics, comparative-genomics counts, per-locus AMR/virulence/mobilome coordinates, phenotypic assays, and cross-pipeline validation. Partitioned into (a) testable from public artifacts, (b) requiring live strain / wet lab.
- **Output:** the claims-tested table in `REPORT.md` §2.

## Stage 1 — Artifact acquisition
1. **Paper PDF.** Fetched printable PLoS URL (`https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0215038&type=printable`, 3.7 MB, CC-BY 4.0). Rasterized with `pdftotext -layout` → `work/paper.txt` for full-text search.
2. **Genome sequences.** Six records via NCBI Entrez `efetch` (no auth required), both FASTA (for length/GC) and full GenBank (for feature annotation):
   - `CP032552` — PA34 chromosome
   - `MH547560` — pMKPA34-1
   - `MH547561` — pMKPA34-2
   - `AE004091` — PAO1 reference
   - `CP000438` — PA14 reference
   - `CP008739` — VRFPA04 reference (ocular)
3. **BV-BRC cross-reference.** Located PA34 by BioSample SAMN08435059 → `genome_id` 287.6355. Pulled the `sp_gene` specialty-gene table (Antibiotic Resistance + Metal Resistance) via public REST API:
   ```
   curl -H "Accept: application/json" \
     "https://www.bv-brc.org/api/sp_gene/?eq(genome_id,287.6355)&select(...)&limit(2500)"
   ```
   → `report/evidence/bvbrc_spgene_pa34.json` (295 KB, 288 records: 251 antibiotic + 37 metal).

## Stage 2 — Table 2 recomputation (chromosome + plasmids)
- **Tool:** Biopython 1.87 direct GenBank parse.
- **Length + GC%:** `SeqIO.read(...).seq` for each record; FASTA and GenBank agree.
- **Feature counts:** iterate `rec.features`, tally `feat.type ∈ {CDS, gene, tRNA, rRNA, ncRNA}`.
- **Protein FASTAs:** emit `>{genome}|{locus_tag}|{protein_id}\n{aa}` for every CDS with a `translation` qualifier → 23,555 proteins across the 4 genomes.
- **Output:** `report/evidence/summary_verification.json` (side-by-side paper-vs-recomputed).

## Stage 3 — Pan-genome analysis (Roary-style, DIAMOND+MCL)
1. Concatenate 23,555 proteins → `all_proteins.faa`.
2. Build DIAMOND 2.1.9 database; all-vs-all BLASTP (`--more-sensitive -p 32 --evalue 1e-5 --outfmt 6 ...`) → 246,824 raw hits.
3. Custom clustering script `work/pangenome_pa34.py` (Roary-core reimplementation):
   - Filter: %identity ≥ 50, alignment coverage ≥ 50% of shorter query/subject, e-value ≤ 1e-5, drop self-hits → 78,801 hits kept.
   - Build undirected weighted graph (edge weight = best bitscore between pair): **22,605 nodes / 39,655 edges**.
   - Add singleton nodes for isolated proteins.
   - Cluster connected components with `markov_clustering.run_mcl(inflation=1.5)`.
4. Tag each cluster by genome membership `{PA34, PAO1, PA14, VRFPA04}`. Compute core (all 4), soft-core (3), shell (2), cloud (1); PA34-containing clusters; PA34 singletons; PA34-clusters-missing-each-reference.
- **Output:** `report/evidence/pangenome_result.json` (paper vs rerun side-by-side).
- **Caveat (documented in critique):** our 50%/50% thresholds are softer than Roary's canonical 95%. This inflates cloud and depresses core; the PA34-accessory headline (any cluster missing ≥1 genome) happens to be robust to this and reproduces to within 1%.

## Stage 4 — Per-locus AMR / virulence / mobilome verification
- **Method:** regex on `product`, `gene`, and `note` qualifiers for every CDS in the 3 PA34 records; check whether each hit's coordinate falls inside the paper's Table 3 RGP interval.
- **Verified (chromosome CP032552):** exoU + SpcU in RGP7; AAC(3)-IId + tunicamycin + copper operon + phage gp37 in RGP23; mercury operon #1 in MKPA34-GI1; chromate operon in MKPA34-GI1; mercury operon #2 in RGP5 (full merR-T-P-A-B-D); pyoverdine NRPS + export flanking RGP73; flagellin adjacent to RGP9.
- **Verified (pMKPA34-1):** dfrA15, cmlA1, strA (APH(3")-Ib), strB (APH(6)-Id), blaNPS-1, sul1, intI1, Tn3 tnpA×2 + tnpR, acrA/acrB/oprM, qacEΔ1, repE/smc/parB/traN, xerC/xerD.
- **Verified (pMKPA34-2):** mepA, tnsA/B/C/D/E, phage integrase + resolvase.
- **Output:** written into `summary_verification.json` (per-locus positions).

## Stage 5 — Independent BV-BRC cross-check
- Pull all `sp_gene` records (Antibiotic Resistance + Metal Resistance) for `genome_id` 287.6355 — an independent SPAdes 3.11 draft assembly (128 contigs) of the same isolate, annotated by BV-BRC's PATRIC pipeline (CARD-like + curated).
- Count unique genes and property types.
- Independent evidence for two mercury-resistance operons (**merA×2, merB×2, merP×2, merR×3**), matching the paper's central mobilome claim from a totally different pipeline.

## Stage 6 — LLM judge
- Assemble structured evidence bundle (Table 2 recomputed vs paper; pan-genome side-by-side; per-locus verification with coordinates; BV-BRC agreement).
- Send to Argo `argo:gpt-5.2` (temperature 0.1) with expert-bioinformatician grading system prompt.
- Return JSON `{verdict, confidence, reasoning, one_line}`.
- **Result:** `PARTIAL` at `high` confidence.
- **Output:** `report/evidence/llm_judge_verdict.json` + `.txt`.

## Stage 7 — Report assembly
- Composed `REPORT.md` (main), `brief.md` (1-paragraph), `attempt_log.md` (chronological), `artifact_harvest.md` (URLs + sizes + checksums).
- This workflow doc, `artifacts_summary.md`, `failure_analysis.md`, `REPORT.tex`, and `open_questions.json` written post-hoc from `REPORT.md` (no new analysis).

---

## Reproduction pointers
- To re-run acquisition: `bash work/fetch_genomes.sh` (idempotent NCBI efetch loop).
- To re-run Table 2: `python work/recompute_table2.py`.
- To re-run pan-genome: `python work/pangenome_pa34.py` (needs DIAMOND 2.1.9 + Biopython 1.87 + `markov_clustering`).
- To re-run BV-BRC cross-check: single `curl` above → JSON pull.
- To re-run LLM judge: `python work/llm_judge.py` (needs Argo proxy live at 127.0.0.1:44497, key=stevens, model `argo:gpt-5.2`).

## Openness / licensing
All data used is open-access: paper CC-BY 4.0 (PLOS), sequences NCBI public, BV-BRC free public API. No private data, no paywalled sources.
