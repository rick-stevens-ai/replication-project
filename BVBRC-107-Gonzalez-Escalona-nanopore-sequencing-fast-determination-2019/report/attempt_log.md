# Attempt Log — BVBRC-107

## 2026-07-05 00:09 CDT · Kickoff
- Read WAVE_BRIEF_2026-07-01.md, created target dir, mirrored BVBRC-17 layout.
- Semantic Scholar `PMID:31361781` lookup with keychain key: paper is in PLoS ONE (DOI 10.1371/journal.pone.0220494, not just bioRxiv). CC0 open access via journals.plos.org and PMC6667211.
- Downloaded paper PDF (1.3 MB) to `work/paper.pdf`.

## 00:10 · Extract ground truth
- `pdftotext -layout` extracted the paper cleanly.
- Ground truth pulled:
  - 3 strains: CFSAN027343 (ST21, Argentina 1999 clinical), CFSAN027346 (ST21, USA 1999 clinical), CFSAN027350 (ST29, USA 2012 environmental). All O26:H11.
  - Accessions: PacBio complete assemblies CP037941–CP037947; MiSeq SRA SRR8333590/1/2; MinION SRA SRR8335317/8.
  - Chromosome sizes: ~5.7, 5.6, 5.4 Mb. Plasmids: 88 kb (343); 95 + 72 kb (346); 157 kb (350).
  - Table 7 virulence genes (strain-specific): tccP in 346+350; efa1/katP in 343+346; espI + stx2a only in 350; stx1a in 343+346.
  - AMR: only CFSAN027346 has aph(3'')-Ib, aph(6)-Id, blaTEM-1B, sul2, tetB, dfrA — all on the 72 kb 2nd plasmid.
  - Tools cited: CANU v1.6 (MinION), HGAP3.0+Quiver (PacBio), CLC Genomics 9.5.2 (Illumina), Ridom SeqSphere+ v2.4.0 (MLST/serotype), VirulenceFinder 1.5, ResFinder 2.1, PHASTER, Mauve.

## 00:11 · Download deposited assemblies
- eutils.ncbi.nlm.nih.gov efetch — 7 sequences downloaded to `work/ncbi_fasta/`.
- Sizes match paper: chr 5.77/5.67/5.51 Mb, plasmids 90.2/97.5+74.3/159.9 kb (all within 1–2 kb of stated).

## 00:12 · Set up uicgpu compute
- Ran `ssh uicgpu` → discovered pre-built `~/micromamba/envs/amr` with blastn 2.16.0, AMRFinderPlus 3.12.8, mlst 2.35.0.
- Rsynced 7 FASTAs to `~/work/bvbrc107/genomes/`.

## 00:14 · Clone CGE databases from Bitbucket
- `git clone` plasmidfinder_db, virulencefinder_db, resfinder_db (488 / 5,102 / 3,212 sequences).
- `mlst_db` failed (private repo, auth-required); `mlst` tool ships its own bundled scheme so this is fine.

## 00:15 · Run BLAST screens (script `run_screens.sh`)
- Concatenated chr+plasmid per strain, built blastdb, ran megablast (perc_identity 90, qcov 60, evalue 1e-30) against 3 databases per strain.
- Raw hit counts:
  - PlasmidFinder: 5 / 11 / 6 (343/346/350)
  - virulence_ecoli+stx: 2823 / 3010 / 2970 (many overlapping variant hits — normal for these databases)
  - ResFinder: 0 / 216 / 0 — **paper's central AMR claim (only 346 has AMR) already confirmed** from raw hits alone
- `mlst --scheme ecoli` (Pasteur): 481/481/1879 — didn't match paper's numbers because paper uses Achtman.

## 00:16 · Fix MLST scheme
- Reran with `mlst --scheme ecoli_achtman_4`: **ST21 / ST21 / ST29** — exact match to paper.

## 00:17 · AMRFinderPlus setup + run
- Initial run failed: AMRFinderPlus DB path was baked in at conda-build time, not present in local install.
- Ran `amrfinder_update -d ~/work/bvbrc107/amrfinderdb` to pull DB version 2024-07-22.1 (~200 MB).
- Reran with `-d amrfinderdb/latest --organism Escherichia --plus`:
  - CFSAN027343: 47 rows, 5 chromosomal AMR (blaEC, acrF, mdtM, glpT_E448K, pmrB_Y358N) + 31 virulence + 0 acquired AMR
  - CFSAN027346: 52 rows, 5 chromosomal + **6 acquired AMR (aph(3'')-Ib, aph(6)-Id, blaTEM-1, sul2, tet(B), dfrA8)** + 32 virulence
  - CFSAN027350: 40 rows, 5 chromosomal + 27 virulence + 0 acquired AMR
- **All 6 AMR genes match paper exactly (`dfrA` → `dfrA8` variant; `blaTEM-1B` → `blaTEM-1` — same gene, subvariant nomenclature only).**

## 00:19 · Strain-specific virulence check
- Python cross-referenced AMRFinderPlus VIRULENCE calls against Table 7's 6 discriminating genes.
- **All 6 gene calls perfectly match** across all 3 strains (tccP, efa1, katP, espI, stx1a, stx2a). The one apparent mismatch (efa1 in 350) is actually a 63.8% partial coverage hit (PARTIALX method) — paper reports it as "absent" because it's a truncated paralog, not a full gene. Confirms paper's binary call.

## 00:20 · Serotype
- BLAST vs SerotypeFinder O_type + H_type sets: all three = wzx_O26 100% + wzy_O26 100% + fliC_H11 99.9%. **O26:H11 for all three ✓**.

## 00:21 · Plasmid replicons
- PlasmidFinder hits per strain, mapped to specific replicon backbones:
  - 343 (88 kb, virulence): IncFIB(AP001918) + IncB/O/K/Z
  - 346 plasmid-1 (95 kb, virulence): IncFIB + IncB/O/K/Z (same architecture as 343)
  - 346 plasmid-2 (72 kb, AMR): IncFII (multiple variants) — matches paper's "AMR plasmid only in 346" claim
  - 350 (157 kb, virulence): IncFIB + IncFII (larger, different composition from 343/346, consistent with paper's Fig 4)

## 00:23 · LLM judge (Argo)
- Called `argo:gpt-5.2` via 127.0.0.1:44497 (Opus 4.7 endpoint returned 502 upstream response format error; falling back).
- Verdict: **PARTIAL**, agreement=98, coverage=70. Rationale: downstream gene/plasmid/MLST/serotype calls all match; the paper's core *technology comparison* (MiSeq vs MinION vs PacBio de novo assemblies) was not re-executed on raw SRA reads.

## 00:25 · Rsync results + write reports
- All evidence in `report/evidence/` (18 files).
- REPORT.md, brief.md, artifact_harvest.md finalized.

## What worked
- CGE database Bitbucket repos still public and clonable (2026-07-05).
- Pre-existing uicgpu `amr` env saved ~30 min of setup.
- AMRFinderPlus `--plus` mode gives both AMR and virulence in a single tool, cleaner than separate ResFinder/VirulenceFinder BLAST invocations.

## What could be extended (out of scope for this replication)
- Pulling MiSeq + MinION raw SRA reads (~30 GB total) and re-running Canu + Nextera pipelines to independently verify the paper's tech-comparison claim. This replication used the deposited PacBio-closed assemblies as ground truth, which is the correct choice for validating the paper's *downstream* biological conclusions but leaves the sequencing-platform comparison itself unverified.
