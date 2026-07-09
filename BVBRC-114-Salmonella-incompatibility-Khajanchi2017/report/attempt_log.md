# Attempt Log — BVBRC-114 Salmonella IncFIB (Khajanchi 2017)

**Executor:** Ollie (OpenClaw subagent, bvbrc-114 wave-keeper)
**Wave:** BVBRC_TOPUP85_2026-06-26 (rank 46) — WAVE_BRIEF_2026-07-01
**Session:** agent:main:subagent:4acb73d8-e2d5-4805-9a19-27ff58425be0
**Date:** 2026-07-05 (CDT)
**Compute host:** uicgpu (heavy work); CherryRd (report drafting)
**LLM endpoint for judge:** Argo proxy → argo:claude-opus-4.7 (free)

## 12:10 CDT — Bootstrap
- Read wave brief + 8-artifact standard.
- Confirmed target dir did not pre-exist. Created scaffold.
- Fetched paper PDF: BMC Genomics track PDF (2.27 MB, PDF v1.4) — PMC pdf endpoint returned HTML wrapper, BMC track/pdf worked.
- pdftotext → 768 lines of text; parsed to identify:
  * BioProject **PRJNA312617**
  * 7 focal strains and their WGS master accessions (LSZD/LXHA/LXGZ/LSZE/LYRR/LYRS/LYRT)
  * Table 1 comparator set (45 additional Typhimurium/Heidelberg strains, mostly CP0…/AMN…/AMM… accessions)

## 12:14–12:25 CDT — Genome retrieval on uicgpu
- Attempted `esearch | efetch -format fasta` route by WGS project code (`LSZD01[WGS]` etc.) — silently returned empty files (bvbrc56 env). Root cause: WGS master → contig fanout via esearch does not always populate reliably in this NCBI env.
- Fell back to `datasets summary genome taxon "Salmonella enterica" --search <strain>` filtered by `bioproject_accession = PRJNA312617` — resolved 4/7 (SE163A, SE696A, SE710A, SE819).
- For remaining 3 (SE397/SE452/SE478, WGS: LYRR/LYRS/LYRT), lookup via NCBI E-utilities `esearch db=assembly` returned assembly UIDs → mapped to GCF accessions (GCF_001729025/GCF_001729035/GCF_001729045).
- `datasets download` hit an intermittent NCBI-datasets DNS timeout (127.0.0.53 misbehaved) — mid-session.
- Bypassed by direct HTTPS FTP fetch (`ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/729/...`) through the uicgpu HTTPS proxy (<lan-host>:3128 — required `source ~/env.sh`).
- All 7 assemblies landed: SE163A 5.20 Mb, SE397 5.43 Mb, SE452 5.13 Mb, SE478 5.16 Mb, SE696A 5.10 Mb, SE710A 5.10 Mb, SE819 4.91 Mb.

**Lesson (append to workspace notes-to-self):** `datasets` NCBI CLI has occasional DNS instability on uicgpu; direct `ftp.ncbi.nlm.nih.gov/genomes/all/` HTTPS fetch is the reliable fallback, provided `source ~/env.sh` is done first (proxy).

## 12:26 CDT — Env discovery
- `bvbrc56` conda env (BLAST + datasets + efetch) — used for retrieval / BLAST.
- `~/micromamba/envs/amr` (was NOT in `conda env list` output — micromamba store) — has SeqSero2 v1.3+, mlst 2.35.0, mash, amrfinder. Activated by `PATH=~/micromamba/envs/amr/bin:$PATH` (micromamba shell init was fiddly; direct PATH prepend worked).

## 12:27–12:29 CDT — Analysis 1: SeqSero2 serotype prediction (C2)
- k-mer mode (`-m k`) on each of the 7 assemblies, 4 threads each, 8 processes.
- Result: **6 Typhimurium + 1 Heidelberg (SE819)** — exact match to paper Table 1.
- All 7 gave antigenic profile "1,2" (O-antigen serogroup B — consistent with both Typhimurium 1,4,[5],12:i:1,2 and Heidelberg 1,4,[5],12:r:1,2).
- MLST auto-scheme: 6/6 Typhimurium strains = identical `salmonella` ST19 (canonical Typhimurium ST); SE819 = ST15 (canonical Heidelberg ST).

## 12:29–12:31 CDT — Analysis 2: PlasmidFinder-style Inc rep detection (C4)
- Cloned CGE PlasmidFinder DB from bitbucket (488 Inc rep sequences).
- makeblastdb + blastn (evalue ≤ 1e-20, %id ≥ 80, coverage ≥ 60%) per genome.
- **6 Typhimurium strains all carry IncFIB(AP001918)** at 98.09% identity, full 682/682 coverage.
- **SE819 has NO IncFIB hits** — consistent with paper's own reason for using SE819 as recipient in conjugation experiments (it is the IncFIB-deficient strain).
- Additional Inc rep types (IncFIA, IncFII variants, IncA, IncI1, IncX4, ColRNAI, ColpVC) detected across strains — matches the paper's multi-replicon description.

## 12:31–12:34 CDT — Analysis 3: Iron acquisition operons (Sit + iuc) (C4/C5)
- V1 iteration: used stale WP_ accessions for iuc genes — returned 35% ID hits (wrong ref proteins). Rejected.
- V2 iteration: pulled pCVM29188_146 (**CP001122.1**, 146811 bp, IncFIB(K) Salmonella-plasmid explicitly listed in paper Table 1) GenBank record and extracted CDS translations for sitABCD + iucABC + iutA + iroB.
  * iucD, iroC, iroN not annotated on CP001122 (paper's plasmid used a slightly older annotation).
- tblastn results:
  * **sitA-D + iucA-C all present at 99.65–100% AA identity in all 6 Typhimurium strains, on the SAME assembly contig each time.**
  * SE819 (Heidelberg): sitA-D detected at 68–86% ID — this is the chromosomal *sit* copy (paper explicitly notes chromosome carries a separate sit locus); iucA-C absent (matches paper's IncFIB-deficient claim).
  * The 99–100% identity across 6 independently sequenced strains from 3+ US states and 1992–2002 is *strong* independent replication of the paper's "conservation" claim (C5) at the intra-Typhimurium level.

## 12:34–12:36 CDT — Analysis 4: Phylogeny (C3)
- Fetched 5 reference genomes: LT2 (NC_003197), CVM29188 (CP001121 — 101k Kentucky plasmid), and 3 bovine Typhimurium (BovineChina/SA972816 CP007484, USDA-USMARC-1808/1880 CP014969/CP014981).
- mash sketch (default k=21, s=1000) + all-vs-all `mash dist` → pairwise distance matrix.
- Biopython DistanceTreeConstructor.nj → newick tree.
- **Result:** 5 of 6 Typhimurium strains (SE163A/SE452/SE478/SE696A/SE710A) form a *tight subclade* — mean pairwise mash distance 1.4–1.8×10⁻³ within group; SE397 has ~2.5× higher mean intra-group distance (4.29×10⁻³). This matches the paper's Fig 1b topology of 5+1.
- The NJ tree does not resolve SE397 as sister to bovine references (mash is low-resolution); the paper used core-genome SNP alignment which is more discriminating. Direction of the outlier signal is correct.

## 12:36–12:39 CDT — Artifact assembly
- Marker/nougat: no central corpus hit for PMID 28768482 on Eagle SCOUT/LUCID/OSTI manifests (not run locally to save the wave subagent budget; used pdftotext -layout as a clearly-marked fallback for the .md and .mmd artifacts).
- Wrote LaTeX REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json.

## 12:39 CDT — LLM judge
- Argo Opus 4.7 (free) judged verdict against paper claims + reproduced evidence.
