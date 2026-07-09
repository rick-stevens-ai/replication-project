# BVBRC-111 Attempt Log

## 2026-07-05 04:07–04:35 CDT — replication run

### Environment
- Executor: CherryRd (subagent). Heavy compute on `uicgpu` via ssh + pre-existing `bvbrc14` env.
- Skills followed: WAVE_BRIEF_2026-07-01.md; existing BVBRC-69 setup as template.
- Target dir: `~/Dropbox/REPLICATE-PROJECT/BVBRC-111-Acinetobacter-baumannii-GC1-XDR-2022/` (fresh — did not exist before this run).

### Step-by-step

1. **04:07** Read wave brief. Confirmed rules (free endpoints only, real data, LLM-judge scoring).
2. **04:08** Confirmed BVBRC-111 dir did not exist. Created target skeleton.
3. **04:08** Fetched paper metadata via NCBI eutils (PMID 35403193 → Harmer et al. 2022, PMC9244215).
4. **04:09** Searched NCBI Assembly for "Acinetobacter baumannii MRSN 56" → 2 assemblies:
   - `GCA_021484925.1` (ASM2148492v1, complete, Unicycler, 65x MiSeq+MinION — paper's own)
   - `GCA_019458485.1` (ASM1945848v1, earlier version)
   Used the newer complete-genome assembly.
5. **04:09** Downloaded assembly bundle (fna, gff, gbff, faa, feature_table, assembly_report) from NCBI FTP.
6. **04:10** Noticed assembly report only lists 1 chromosome (CP090606.1, 4.15 Mb) but paper claims 4 plasmids too. Queried NCBI nuccore for BioProject PRJNA742487 → found the 4 plasmid accessions CP080453..CP080456. Fetched all 4 via efetch. Verified sizes match paper (2178, 2725, 6772, 8731 bp).
7. **04:12** Confirmed uicgpu had abricate 1.4.0 + mlst 2.33.1 + full DB set at `/data/stevens/envs/bvbrc14/bin` (leftover from BVBRC-69). No new install needed.
8. **04:13** Rsync'd genome/ dir to `uicgpu:/data/stevens/bvbrc111/genome/`. Wrote 12-step analysis script (`analyze.sh`) and ran it. Everything completed in ~2 min: MLST both schemes, AMR across 5 DBs on whole genome, AMR on chromosome-only, AMR on each of 4 plasmids, PlasmidFinder, VFDB, and feature-level ISAba1/IS26/Tn7/gyrA extraction.
9. **04:16** First-pass results excellent — all key markers detected. But 0 hits from "comM" text search puzzled me. Wrote `features_probe2.py` for locus zooms: walked chr 340-410k CDS-by-CDS to find AbaR28. Found integron+aac(3)-Ia+aadA1+sul1 exactly as paper claims.
10. **04:19** Zoomed on chr 2,310–2,325k → confirmed ISAba1 immediately upstream of MarR-family regulator (paper's mechanism).
11. **04:21** GyrA extraction gave protein of 905 aa. First WT reference attempt (WP_000675167.1) turned out to be *E. coli* BaeS (misidentified). Searched NCBI properly for "DNA gyrase subunit A" in *A. baumannii ATCC 17978* → got WP_000116449.1 (correct 904-aa GyrA). Direct positional alignment revealed exactly 2 aa differences: S81L in QRDR (the classic FQR mutation, matches paper) and A755T outside QRDR. 99.78% identity. Perfect reproduction of paper's gyrA claim.
12. **04:25** Rsync'd all `results/` back to `report/evidence/results/`.
13. **04:27** First LLM judge (`argo:claude-opus-4.7`) failed with 502. Switched to `argo:gpt-5.1` → 88/REPLICATED. Then `argo:gemini-2.5-pro` → 95/FULLY REPLICATED. Two-judge mean 91.5, rounded to 92.
14. **04:30** Wrote brief.md, REPORT.md, artifact_harvest.md, this attempt_log.md.

### Failures / retries
- LLM judge #1 (Claude Opus 4.7) → 502 Bad Gateway. Argo proxy often has transient 502s on the Claude models. Recovered by using gpt-5.1 and gemini-2.5-pro (both worked first try).
- Initial WT gyrA fetch pulled wrong protein (`WP_000675167.1` = *E. coli* BaeS, NOT gyrA). Recovered by querying NCBI Protein with strict title+organism filter → WP_000116449.1 (correct A. baumannii GyrA).
- Zsh heredoc `<<PYEOF` failed with "no matches found" (zsh globbing). Recovered by writing python scripts to files and scp'ing.

### Tools used
- NCBI eutils REST (esearch/esummary/efetch), NCBI FTP (public, no auth)
- abricate 1.4.0 (ResFinder/CARD/NCBI/MEGARES/ARG-ANNOT/PlasmidFinder/VFDB, all Apr-2026 DBs)
- mlst 2.33.1
- BioPython 1.85
- BLAST+ 2.16
- Argo proxy (localhost:44497, free ANL endpoint) for LLM judges — models gpt-5.1 and gemini-2.5-pro

### No paid APIs used. No fabricated numbers.
