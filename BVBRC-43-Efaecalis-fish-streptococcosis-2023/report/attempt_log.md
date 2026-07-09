# Attempt Log — BVBRC-43 (2026-07-01)

Chronological record of the replication.

1. **Dedup check.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "faecalis|streptococcosis"` → only `BVBRC-13-Efaecalis-envadapt-He2018` (env-adaptation, He 2018 — DIFFERENT paper). No dir for this fish-streptococcosis paper. Proceeded.
2. Read WAVE_BRIEF_2026-07-01.md + exemplar BVBRC-17 REPORT.md for structure/standard.
3. **Located paper on Europe PMC**: PMID 36707682, PMC9883459, DOI 10.1038/s41598-022-25968-8, Sci Rep 2023. Fetched full-text XML (free).
4. Parsed XML sections; extracted abstract, Methods, Results, and the **Data availability** statement giving nuccore accessions: BFFF11=CP045918, BFF1B1=CP046022, BFPS6=JADBGH010000000. Extracted Table 1 (genome features) and Table 2 (AMR genes) targets → `evidence/paper_targets.json`.
5. **Mapped nuccore → assembly accessions** via NCBI eutils elink/esummary: BFFF11→GCA_009685155.1, BFF1B1→GCF_017357805.1, BFPS6→GCF_021375735.1. Also pulled V583 reference GCF_000007785.1 (AE016830) as control (paper's BRIG/SNP reference).
6. **Downloaded all 4 genomes** (genome+protein+CDS+GFF) via NCBI Datasets v2alpha REST (free, no auth). Unzipped, checksummed.
7. **Computed genome statistics** (`genome_stats.py`, pure stdlib). Bug: initial glob matched `cds_from_genomic.fna` → wrong contig count for BFF1B1; fixed to exclude cds_from. Final sizes match paper Table 1 (BFF1B1 & BFFF11 EXACT; BFPS6 N50/L50 EXACT, size 99.95%). → `evidence/genome_stats.json`.
8. **Checked uicgpu tooling**: env `amr` (micromamba) has AMRFinderPlus 3.12.8 (DB 2024-07-22.1) + mlst; env bvbrc28 has fastANI/mash/blast. scp'd 4 genomes to uicgpu.
9. **Ran AMRFinderPlus** (`--organism Enterococcus_faecalis --plus`) + **mlst** on all 4 (`run_amr_mlst.sh`). Result: tet(L)+tet(M) at 100%/100% ONLY in BFPS6 (co-located tandem cassette on contig NZ_JADBGH010000009.1); lsa(A) in all three; V583 control shows vanB operon (positive control). MLST: BFFF11 untyped(V583-like), BFF1B1=ST482, BFPS6=ST81.
10. **Direct tet tblastn** with old GenBank tet accessions (CAA43857 etc.) did not hit — those alleles too divergent; AMRFinder's curated DB is authoritative and used for the C3 call. Confirmed BFPS6 tet cassette coordinates.
11. **Virulence markers**: built curated 13-marker query from V583 proteome (`build_vf_query.py`), ran tblastn vs the 3 fish genomes (`vf_blast.py`, local BLAST). Core VFs (fsrA/B, ace, ebpA/C, srtA/C, tpx) conserved in all three; **aggregation substance agg/prgB/Asa1 PRESENT only in BFFF11, ABSENT in BFF1B1 & BFPS6** → exact match to paper. Cytolysin weak/absent in all (paper reports inconsistent cyl detection — consistent).
12. **fastANI** pairwise: BFFF11↔V583 highest (99.5%), all inter-fish ~98.7% (species-saturated). Directionally supports "tilapia strains closer to reference"; cannot fully resolve exact topology.
13. **LLM-judge** via **free Argo argo:gpt-5.2** (`judge.py`) → VERDICT PARTIAL, coverage 6/7, agreement (C1b, C3, C6 full; C1, C2, C5 partial; C4 untested).
14. Wrote report/, evidence/, this log. No paid endpoints used; no sibling dirs touched.

## What worked
- NCBI Datasets REST genome pull, AMRFinderPlus tet detection, tblastn VF differential — all clean, high-signal.
- Genome-feature reproduction is essentially exact (strong C6).

## What was out of reach / not done
- antiSMASH bacteriocin clusters (C4) — not rerun this pass.
- Full 69-VF and 39-AMR count reproduction — paper's counts mix intrinsic/point-mutation "resistance" genes (gyrA, rpoB, murA, EF-Tu, etc. via CARD/ARG-ANNOT protein homology) that AMRFinderPlus classifies as core/intrinsic and does not report as acquired AMR; and VFDB/PATRIC VF counting is database-dependent. The specific differential claims reproduced cleanly; the aggregate counts are framework-dependent.
- PHASTER prophage, ISfinder IS families, PlasmidFinder replicons — not rerun (lower-signal descriptive claims).
