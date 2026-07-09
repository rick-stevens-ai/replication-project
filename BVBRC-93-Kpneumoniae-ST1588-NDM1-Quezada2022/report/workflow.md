# BVBRC-93 Replication Workflow

**Target paper:** Quezada-Aguiluz et al., *Antibiotics* 2022, 11(9):1207 (PMID 36139987).
**Isolate:** *K. pneumoniae* UCO-361 (ST1588, KL108, O1; Chile 2014).
**Deposit:** WGS `JAMJQY010000000`; plasmid `NZ_JAMJQY010000002.1` (314,976 bp).
**Compute host:** `uicgpu` (8×A100, 255 cores, 2 TB RAM).
**Working dir:** `/data/stevens/bvbrc93-kpneu-st1588-independent/`.

---

## Stage 0 — Paper + accession retrieval

1. **PubMed lookup** — ESummary on PMID 36139987 confirms DOI (10.3390/antibiotics11091207), journal (*Antibiotics (Basel)*), PMC ID (PMC9494972).
2. **Full-text pull** — Fetch JATS XML from EuropePMC:
   `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9494972/fullTextXML`.
3. **Data-availability parse** — Extract deposited accession `JAMJQY010000000` from the data-availability statement.
4. **Assembly enumeration** — ESearch `nuccore` for `JAMJQY01[All Fields]` → 15 contigs.

## Stage 1 — Sequence retrieval

5. **All 15 contigs** — EFetch (`rettype=fasta`) → `work/data/UCO361_all_contigs.fasta`
   (5,841,932 bp; md5 `85adabb6d97992295a31f788fad0a1dc`).
6. **Plasmid contig with annotation** — EFetch (`rettype=gbwithparts`) for `NZ_JAMJQY010000002.1`
   → `work/data/pNDM1_UCO361.gb` (RefSeq PGAP, 326 CDS).

## Stage 2 — Environment setup

7. **Tool envs on uicgpu:**
   - `micromamba activate amr` → `mlst` 2.35.0, AMRFinderPlus 3.12.8 (DB 2024-07-22.1), `blastn` 2.16.0.
   - `micromamba activate /data/stevens/envs/kleborate` → Kleborate v3.2.4.

## Stage 3 — Independent genotyping

8. **MLST** — `mlst --scheme klebsiella UCO361_all_contigs.fasta > mlst_klebsiella.tsv`
   → **ST1588** with alleles `gapA(2) infB(6) mdh(1) pgi(3) phoE(10) rpoB(1) tonB(56)`, all exact matches.
9. **AMRFinderPlus** — `amrfinder -n UCO361_all_contigs.fasta -O Klebsiella_pneumoniae --plus -o amrfinder_out.tsv`
   → 46 rows, 19 AMR-class hits.
10. **Kleborate** — `kleborate -a UCO361_all_contigs.fasta -o kleborate_out -p kpsc`
    → ST1588, KL108 (99.23% id), OL2α.2 → O1αβ,2β (99.02% id), virulence_score=0.

## Stage 4 — Plasmid typing

11. **PlasmidFinder DB fetch** —
    `git clone --depth 1 https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git`.
12. **BLAST DB build** —
    `makeblastdb -in plasmidfinder_db/enterobacteriales.fsa -dbtype nucl -out pfinder_db`.
13. **Replicon BLAST** —
    `blastn -query UCO361_all_contigs.fasta -db pfinder_db -perc_identity 60 -outfmt 6 -out pfinder_hits.tsv`.
    Apply PF-standard thresholds (≥95% id AND ≥60% ref cov).

## Stage 5 — Comparative plasmid BLASTn

14. **Reference plasmids** — EFetch `MN598004.1` (pNDM-1-EC12, 351,777 bp) and `CP041388.1` (pRAO166a, 382,325 bp).
15. **Extract query plasmid only** — Slice contig 2 → `pNDM1_UCO361_only.fasta`.
16. **Pairwise BLASTn** — `makeblastdb` on each reference, then `blastn`; tabulate HSPs, longest match, total ≥90%-id aligned length.

## Stage 6 — blaNDM-1 local environment (Fig. 1B check)

17. **Feature parse** — Parse all CDS/gene features from `pNDM1_UCO361.gb` in interval 300000–315000 bp.
18. **Landmark validation** — Confirm the 6 canonical landmarks (IS3000, ΔISAba125, blaNDM-1, bleMBL, trpF, dsdD, ΔgroES, groEL) in the exact expected order and strand.

## Stage 7 — LLM-judge (free Argo GPT-5.1)

19. **Evidence pack assembly** — Bundle Claims table, Methods table, Results table, and raw evidence pointers.
20. **Judge call** — POST to `http://127.0.0.1:44497/v1/chat/completions`, model `argo:gpt-5.1`, key `stevens`.
21. **Verdict capture** — `{"verdict":"REPLICATED","coverage_frac":0.9,"agreement_frac":0.98,...}`.

## Stage 8 — Report generation

22. **Write REPORT.md** — Claims table, methods, results-vs-paper table, verdict + nuances.
23. **Backfill artifacts** — REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md.
24. **Preserve evidence** — All raw outputs kept under `report/evidence/`; scripts and downloaded data under `work/`.

---

## Rules honoured

- **Free endpoints only** — NCBI E-utilities, EuropePMC REST, Argo proxy `:44497`. No paid API calls.
- **HPC compute** — uicgpu A100 pool; no local Mac cycles used for BLASTn or annotation.
- **Independent replication** — Fresh working dir; no reuse of prior BVBRC-46 outputs.
- **Provenance preserved** — md5-checksummed inputs; all tool versions logged.
