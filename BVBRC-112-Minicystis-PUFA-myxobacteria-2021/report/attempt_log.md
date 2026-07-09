# Attempt Log — BVBRC-112

Times UTC.

- **2026-07-05T09:07** — Assignment received (BVBRC-112, PMID 34511070, PMC8436480, DOI 10.1186/s12864-021-07955-x). Read WAVE_BRIEF_2026-07-01.md.
- **09:07** — Created target dir tree.
- **09:07** — Fetched PubMed esummary → confirmed DOI + PMC.
- **09:07** — web_fetch PMC full text (readability extraction) → captured abstract, Background, Table 1, and up through Secretome analysis + BGC/pfa results (via a second XML-based extraction to reach the "47 BGCs / 7.71%" figure and the pfa cluster locus tags).
- **09:08** — efetch nuccore CP016211.1 → FASTA (16.27 MB) and GenBank flat file (32.31 MB). Both landed cleanly.
- **09:08** — Python stdlib script on GenBank: length=16,040,666 bp, GC%=69.10, CDS=14,018, +strand=6,983, −strand=7,035, tRNA=89, rRNA=10, genes=14,117 — exact/near-exact match to paper Table 1.
- **09:09** — Located pfa1 locus tag A7982_11504 in GenBank (index 11500 in CDS list). Confirmed A7982_11504=Enoyl-ACP reductase (PfaD/pfa1), A7982_11505=omega-3 PUFA synthase subunit PfaA (pfa2), A7982_11506=omega-3 PUFA synthase subunit protein (pfa3/PfaC). All (+) strand, consecutive. Extracted protein translations to .faa files.
- **09:09** — RAST/NCBI annotation of CP016211 does not label any CDS as "PPTase" / "phosphopantetheinyl transferase" / "Sfp" by keyword → cannot confirm pfaE-at-separate-locus by keyword alone. Flagged as limitation (would need HMMER + PFAM PF01648).
- **09:10** — Regex-based motif hunt for ACP/KS/KR sites in PfaA (A7982_11505) failed (regex too strict). Decision: rely on antiSMASH's professional-grade HMM domain scan instead of ad-hoc regex.
- **09:11** — SSH uicgpu → antismash/standalone:6.1.1 docker image already present. scp'd CP016211.gbk to uicgpu.
- **09:12** — Kicked antiSMASH docker run (minimal mode, 32 CPUs) on uicgpu. First launch failed because `-v .../input:/input` + full path in argv double-prefixed → fixed by mounting + using `-w /input` and basename argv.
- **09:13** — antiSMASH finished (small genome by BGC standards; --minimal skips ClusterBlast). Output: 47 region GBKs. Fetched CP016211.json (26.8 MB), index.html, and pfa_region042.gbk back to local evidence dir.
- **09:14** — Parsed antiSMASH JSON: **47 regions**, dominant classes = terpene (10) + NRPS/NRPS-like (8) + RiPP-like (9). Region #42 (start 13,095,900 end 13,151,432) = ['hglE-KS','T1PKS'] — contains all three pfa loci exactly. Total CDS in BGCs = 1,096 = 7.82 % of 14,018 — matches paper's 1,081 / 7.71 % within tool-version tolerance.
- **09:15** — Arithmetic check on "M. rosea is ~1.26 Mb larger than S. cellulosum So0157-2 at 14,782,125 bp": 16,040,666 − 14,782,125 = 1,258,541 bp = 1.26 Mb. Exact.
- **09:16** — Wrote brief.md, REPORT.md, artifact_harvest.md, this attempt_log.md. Ran LLM judge. Emitted WAVE_RESULT.

## What worked
- Genome numeric claims (length, GC, CDS, strand split): trivial to verify from public GenBank record — perfect match.
- antiSMASH 6.1.1 on uicgpu: single docker command, ~1 min wall time, exactly reproduced the paper's 47-BGC count and pfa cluster location.
- pfa locus tags: exactly at paper-cited positions, on the correct strand, with the correct product annotations from NCBI.

## What was skipped / flagged
- ELK/phosphatase HMM search across 20 myxobacteria (C9) — too costly for one-paper scope.
- Formal HGT-from-Actinobacteria phylogeny (C10) — presence confirmed, origin not independently retested.
- pfaE keyword-based confirmation of separate locus — annotation gap, needs HMMER+PFAM (non-blocking).
- Full HMMER-3 domain scan of PfaA/PfaC — length + antiSMASH region call are strong indirect confirmation; explicit domain scan deferred.

## What failed and was recovered
- Initial docker run: double-prefix path bug (`/input//input/CP016211.gbk`) → fixed by using `-w /input` and basename.
- Regex-based domain motif hunt in PfaA: too strict, 0 hits → switched to antiSMASH (correct approach anyway).
- `f-string with backslash` python error on remote SSH — fixed by moving the regex out or using non-`\d` characters escape.
