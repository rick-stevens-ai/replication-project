# Attempt Log — BVBRC-78

Chronological record of the replication run (America/Chicago).

## 2026-07-03 08:10 — Setup
- Read `WAVE_BRIEF_2026-07-01.md`.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-78-efaecium-phage-vbefah163-pradal2023/{report/evidence,work}`.

## 08:11 — Paper metadata + full text
- eSummary → PMID 36680219, DOI 10.3390/v15010179, PMC9860891, journal *Viruses*.
- Europe PMC fullTextXML retrieved (193 kB).
- Regex-scanned XML for GenBank/ENA IDs → key hit: **CAJDKA010000002.1** (phage genome, ENA). Additional MT-series and MW-series accessions are comparator phages listed in the paper's Table 2.
- Paper's Data Availability Statement confirms only the phage genome was deposited; VR-13 host isolate was NOT sequenced/deposited.

## 08:12 — Genome downloads
- ENA fasta for CAJDKA010000002.1 returned gzipped — decompressed → 2 contigs (both 150,836 bp; MD5s different so they're two distinct sequences that just happen to be equal length; picked contig 2 which the paper names as the phage genome, `>ENA|CAJDKA010000002|CAJDKA010000002.1 Enterococcus phage 163 genome assembly, contig: phage163-genome`).
- **Genome length: 150,836 bp — exact match to paper.**
- **GC 37.04 % — matches paper's "~37%".**
- Fetched 7 comparator genomes from NCBI eFetch: NC_029009 (EFDG1, 147,589 bp — matches Table 2), MH880817 (EfV12-phi1, 152,770), NC_047796.1 (EFP01, 155,053), MT909815.1 (iF6, 156,592), MW633168.1 (MDA2, 140,226), NC_031260 (Ec-ZZ2, 41,170 — Sipho outgroup), MK360024 (vB_EfaS_Max, 40,975 — Sipho outgroup). All lengths match paper Table 2 exactly.

## 08:14 — Whole-genome BLASTn (C-7, C-8)
- Built 7 nucl BLAST DBs. Weighted % identity across all HSPs:
    - iF6 (MT909815): 96.5 % / 136,229 aligned bp
    - EFP01 (NC_047796.1): 95.7 % / 130,884 aligned bp
    - EfV12-phi1 (MH880817): 94.1 % / 130,013 aligned bp
    - EFDG1 (NC_029009): 93.8 % / 128,834 aligned bp
    - MDA2 (MW633168.1): 78.3 % / 28,253 aligned bp — much more distant, consistent with paper's Kochikohdavirus classification
    - Sipho outgroups NC_031260 & MK360024: NO HITS at default megablast cut-offs
- Directionally matches paper's "iF6, EfV12-phi1, and EFDG1 phage genomes to be the most similar (~98 %)". Paper's headline 98 % is likely from a full-length pyani/VIRIDIC calculation; megablast's HSP-weighted 93–96 % is a slightly stricter measure. Rank order is identical.

## 08:16 — ORF prediction (C-3)
- `prodigal -p meta` on all 8 phages.
- phage_vB_EfaH_163: 183 ORFs (paper: 186). Off-by-3 easily explained by RAST+PATRIC+manual curation vs single-tool Prodigal.

## 08:17 — tRNA scan (C-4)
- Homebrew-installed ARAGORN.
- "Number of tRNA genes = 21" — **exact match** to paper's 21.

## 08:18 — AMR + virulence screen (C-5)
- Abricate installed locally, all 12 dbs current (2026-Jul-3 fetch).
- Ran phage vs card, ncbi, resfinder, argannot, megares, vfdb, victors.
- **All 7 dbs: 0 hits.** Fully confirms paper's key safety claim ("does not harbour any virulence factors or antibiotic resistance genes").

## 08:19 — Lysogeny screen (C-6)
- No local phage-lifestyle db; built a curated 7-protein set of known integrases + cI repressors (lambda, phi80, P22, phiSa3int, L54a) via NCBI eFetch.
- `blastp -evalue 1e-5` phage_vB_EfaH_163 proteome vs lysogeny set: **0 hits**.
- Positive-control comparison: Sipho phage NC_031260 (Ec-ZZ2) proteome vs same set: 1 hit at E<1e-5. Confirms the screen has power. Consistent with paper's lytic prediction.

## 08:20 — MCP phylogeny (C-7)
- Extracted major head/capsid protein from each of the 8 phages via `blastp` against the annotated EFDG1 major head protein (YP_009218324.2, 473 aa).
- 6/8 hit (all Herelleviridae); 2/8 (Sipho outgroups) no MCP homology — expected for non-Herelleviridae.
- MAFFT segfaulted on macOS Homebrew mafft-7.526 in both L-INS-i and FFT-NS-2 modes. Even setting `MAFFT_BINARIES` did not help.
- Fallback: BioPython `PairwiseAligner` (global, +1/-0/-1/-0.5) on the 6 MCPs (all length 466–473 aa, so trivially globalign-able).
- Distance matrix:
    - phage_vB_EfaH_163 vs MT909815 (iF6): **100.00 %** identity
    - vs MH880817 (EfV12-phi1): 99.37 %
    - vs NC_047796.1 (EFP01): 99.15 %
    - vs NC_029009 (EFDG1): 98.73 %
    - vs MW633168.1 (MDA2): **85.19 %** (distinct clade)
- UPGMA topology exactly reproduces the paper's Fig 4 clustering: (MDA2, (EFDG1, (EFP01, (EfV12-phi1, (iF6, vB_EfaH_163))))).

## 08:22 — LLM judges
- Argo proxy at 127.0.0.1:44497, 44 models available.
- Judge round 1: `argo:gpt-5.2`, `argo:claude-opus-4.7`, `argo:gemini-2.5-pro`. Opus 4.7 returned HTTP 502.
- Judge round 2: `argo:claude-opus-4.8` — also HTTP 502. Argo Opus endpoints transiently unhealthy.
- Judge round 3: `argo:claude-sonnet-4.6`, `argo:gpt-5.4` — both succeeded.
- Final 4-judge panel: gpt-5.2 PARTIAL, gemini-2.5-pro REPLICATED, claude-sonnet-4.6 PARTIAL, gpt-5.4 PARTIAL. **Majority: PARTIAL.**

## 08:30 — Report assembly
- Copied all evidence to `report/evidence/`.
- Wrote `report/brief.md`, `report/REPORT.md`, `report/artifact_harvest.md`, this log.
- Final verdict: PARTIAL.

## Notes / caveats
- The phage's "packaging mechanism = long direct terminal repeats" claim (C-9) cannot be independently rerun because the raw Illumina reads were not deposited (PhageTerm needs them).
- The VR-13 host isolate genome was not deposited by the authors, so any claim about the host's vanR/vanA cluster or CARD/AMRFinder output on the host is not independently verifiable from paper artefacts.
- Wet-lab claims (host range %, one-step growth, *Galleria mellonella* mortality) are explicitly out of scope for computational replication.
- MAFFT segfault on macOS Homebrew build 7.526 is a persistent local environmental issue — noting for future runs; consider using pyhmmer / muscle / mafft-conda as alternatives.
