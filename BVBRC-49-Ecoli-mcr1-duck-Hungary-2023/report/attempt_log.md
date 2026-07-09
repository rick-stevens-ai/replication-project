# Attempt Log — BVBRC-49

**Date:** 2026-07-01 (evening CDT), Analyst: Ollie (subagent)

1. **Dedup check.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "mcr-1|mcr1|duck"` → no match. Scanned BVBRC-01..48 dir list: no existing dir for this mcr-1 duck Hungary paper (BVBRC-14/17/21/26/36 are different E. coli papers). Safe to proceed. Created target dir BVBRC-49-Ecoli-mcr1-duck-Hungary-2023/{report/evidence,work}.
2. **Read briefs.** WAVE_BRIEF_2026-07-01.md (free endpoints only, real data, LLM-judge, no overwrite) + BVBRC-17 exemplar REPORT.md (structure template).
3. **Found paper.** Europe PMC TITLE search → PMID 37887221, PMC10604428, DOI 10.3390/antibiotics12101519, Antibiotics 2023, OA=Y. Exact 1-hit.
4. **Pulled full text XML** (fullTextXML, 120 KB) — free. Extracted abstract + body to fulltext.txt.
5. **Extracted accessions from full text:** BioProject **PRJNA1012593**; replicons **CP134085** (chromosome 4,966,963 bp), CP134086/87/88/89/90 (5 plasmids). mcr-1 → CP134089 (33,541 bp, IncX4). MDR → CP134088 (254 kb, IncH). Strain Ec45-2020, ST162, phenotype Amp-Chl-Cip-Col-Sul-Tet-Tmp, MIC colistin 8 µg/mL, serotype H10:O55.
6. **Resolved assembly:** NCBI Datasets REST `/genome/bioproject/PRJNA1012593/dataset_report` → GCF_038709795.1 / GCA_038709795.1 (ASM3870979v1, Chromosome level, biosample SAMN37265790).
7. **Downloaded** GCF_038709795.1 (genome+protein+GFF+seq_report), 3.2 MB. 6 replicons present.
8. **Genome stats** (Python): chromosome 4,967,063 bp + 5 plasmids incl. 33,541 bp mcr-1 plasmid (exact) → C1 ✅.
9. **uicgpu tooling.** `bvbrc28` env had prokka/blast/datasets but NOT amrfinder/mlst/abricate. `bvbrc14` env HAS amrfinder 4.2.7 / mlst 2.33.1 / abricate 1.4.0. Activated bvbrc14 by full path (`conda activate /data/stevens/envs/bvbrc14`; name-only activation failed — env not in default envs dir list).
10. **scp genome to uicgpu:~/bvbrc49/work**, ran:
    - `mlst` → **ST162** (exact allele profile) → C3 ✅.
    - `abricate plasmidfinder` → CP134089=IncX4, CP134088=IncHI1A/B → C2/C4 replicon ✅.
    - `abricate resfinder` → mcr-1.1 ONLY on CP134089; full MDR set on CP134088 → C2/C4 ✅.
    - `AMRFinderPlus -O Escherichia --plus` (63 s) → mcr-1.1 (COLISTIN) on CP134089; gyrA S83L/D87N + parC S80I QRDR; astA/lpfA/ybt virulence; full ARG list → C2/C5/C6 ✅.
    - `abricate vfdb` → 124 virulence hits incl. hlyE.
11. **Copied 7 evidence files** back to report/evidence/.
12. **LLM-judge** via free Argo `argo:gpt-5.2` (localhost:44497) on a structured claim-vs-result sheet → Coverage 8/10, Agreement 9/10, Verdict **PARTIAL**. Saved to evidence/llm_judge_gpt52.md.
13. **Wrote** brief.md, REPORT.md, attempt_log.md, artifact_harvest.md.

## What worked
- Europe PMC XML gave every accession directly — no PDF/paid tool needed.
- NCBI Datasets bioproject→assembly resolution was clean.
- bvbrc14 had the full typing toolchain; AMRFinder + mlst + abricate reproduced the genomic core exactly.

## What failed / gotchas
- `conda activate bvbrc14` (name) failed — envs live under /data/stevens/envs and aren't all registered; must activate by full path.
- No offline serotyper (ectyper/SerotypeFinder); pip install had no network in bvbrc28 → C7 (H10:O55) not tested.
- MIC (8 µg/mL) not reproducible from sequence alone (no wet lab) → C5 genotype-only.
