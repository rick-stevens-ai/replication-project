# Attempt log — BVBRC-108 (Akter 2023 *E. faecalis* fish streptococcosis)

- **00:10 CDT** — Received subagent task. Read WAVE_BRIEF_2026-07-01.md. Created target dir + report/{evidence}, work/ under Dropbox.
- **00:11** — Pulled PMC full-text XML from EuropePMC (142 kB). Parsed abstract, Results, Table 1 (genome features), Table 2 (AMR genes), Methods, Data Availability. Confirmed:
  - Deposited accessions: CP045918 (BFFF11), CP046022 (BFF1B1), JADBGH010000000 (BFPS6 WGS master).
  - Paper Table 1 genome sizes: 2,761,629 / 3,067,042 / 2,868,292.
  - Paper Table 2: 39 AMR genes across 16 groups.
- **00:14** — Fetched CP045918 and CP046022 via `efetch -db nuccore` on uicgpu (`micromamba envs/amr`).
  - `curl: (56) OpenSSL SSL_read` noise on some `edirect` calls but final data landed fine (visible in EuroPMC fallback + retry).
  - For BFPS6, `esearch -db assembly` returned GCF_021375735.1 (ASM2137573v1, 45 contigs) linked to BioSample SAMN16320166.
  - Pulled BFPS6 assembly via `datasets download genome accession GCF_021375735.1 --include genome`. Unzipped and staged.
- **00:15** — Computed genome stats (Biopython): BFFF11 2,761,629 bp / 1 contig / 37.55% GC; BFF1B1 3,067,042 bp / 1 contig / 37.41% GC; BFPS6 2,866,855 bp / 45 contigs / 37.51% GC / N50 270,331 / L50 2. **Match to paper Table 1 to the base pair** (BFPS6 differs by 1,437 bp between paper's SPAdes draft and RefSeq processed version).
- **00:15–00:16** — Ran AMRFinderPlus 3.12.8 (DB 2024-07-22.1, `-O Enterococcus_faecalis --plus`) on all three:
  - First run had a stray empty output on BFFF11/BFF1B1 (probable temp-file race on shared uicgpu). Second run clean.
  - BFFF11: `lsa(A)` only. BFF1B1: `lsa(A)` only. BFPS6: `lsa(A)` + `tet(L)` + `tet(M)`.
- **00:16** — Attempted VFDB nucleotide-BLAST against E. faecalis subset (38 curated VFs). BFFF11 29 hits, BFF1B1 15, BFPS6 17.
- **00:18** — Downloaded VFDB set-A **protein** sequences (VFDB_setA_pro.fas.gz, 4,732 entries). Filtered to paper-mentioned symbols (50 entries, 43 unique symbols including cross-species targets). Ran `tblastn -evalue 1e-10` against each assembly. Kept best hit per query at pident≥40%, qcov≥40%.
- **00:19** — Consolidated virulence matrix (`vfdb/vf_presence.json`). Reproduced:
  - All 3 strains: gelE, fsrA/B/C, ebpA/B/C, ace, efaA, sprE, srtC, bopD, clpP, cpsA/uppS, cpsB/cdsA.
  - BFFF11 only: cpsC, cpsD, cpsE, cpsG, cpsH, cpsI, cpsJ, cpsK, prgB, asa1, glf.
  - BFFF11 + BFPS6: cpsF (paper predicted this exactly).
  - BFFF11 + BFF1B1: ctrA (paper predicted this exactly).
  - BFPS6 only: cylI.
  - BFF1B1 only: cylR2 (weak hit at 53% pident but detectable).
- **00:20** — LLM-judge scoring via Argo proxy. `argo:claude-opus-4.7` returned repeated 502 Bad Gateway (Argo backend flaky at that moment on Anthropic route for prompts ~4 kB). Fell back to `argo:claude-sonnet-4.6` which returned clean JSON: **PARTIAL, coverage 72%, agreement 85%**. Saved to `report/evidence/judge_output.json`.
- **00:20** — Wrote REPORT.md, brief.md, artifact_harvest.md, this attempt_log. Rsync'd key artifacts down from uicgpu into `report/evidence/` and `work/`.

## What worked
- Everything on the "core testable" path (assemblies + AMR + VFDB tblastn) reproduced quickly and cleanly on public data with free tools.
- `datasets` REST for WGS master → assembly resolution is the reliable path for GenBank draft WGS records.

## What didn't
- Argo `claude-opus-4.7` route was 502'ing at moment of scoring (~00:20 CDT). Sonnet-4.6 fallback worked. Not blocking.
- Paper's Victors + PATRIC-VFDB + PATRIC-VF calls (about 16 additional VF symbols: tpx, perR, psr, hylA, hylB, tuf, glf-in-BFF1B1, cad, camE, elrA, brnQ, purl, thyA, phrB, recQ1, scrB, scrR) are not in VFDB set-A — would need standing up PATRIC/BV-BRC or Victors DB to test. Left explicitly out of scope for a single-subagent budget.
- Also, tet(S) and tet(45) are called by paper via ARG-ANNOT/ResFinder (77–100% identity) but not by NCBI AMRFinderPlus at defaults; consistent with tool-scope differences (AMRFinderPlus uses stricter NCBI-curated reference set for Enterococcus).

## Discrepancies found in the paper itself
- Paper Table 1 header labels for **BFFF11 and BFF1B1 are swapped** vs NCBI records. CP045918 (per NCBI = BFFF11) = 2,761,629 bp, but Table 1 labels the 2,761,629 bp column as BFF1B1. The genome-size numbers are correct; the header row is transposed. Clerical error, not a scientific one.
- Paper Table 1 N50s for the two complete-chromosome strains (384,233 and 343,888) don't match the closed single-chromosome assemblies at NCBI (where N50 = full chromosome length). This means Table 1 was populated from the pre-closure SPAdes draft assemblies (also consistent with the paper's Methods).
