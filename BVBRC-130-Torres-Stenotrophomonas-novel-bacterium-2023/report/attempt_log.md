# Attempt log — BVBRC-130

Date: 2026-07-06 (00:07–00:15 CDT)
Runner: OpenClaw subagent, on CherryRd, argo:claude-opus-4.7

## Chronological

1. Read wave brief + 8-artifact standard; created target dir with subdirs.
2. Fetched PMID metadata via NCBI EUtils esummary → confirmed F1000Research 2023, PMCID PMC10682605, DOI 10.12688/f1000research.134978.3.
3. Fetched abstract via efetch (43 lines) — confirmed methodology (PacBio, RAST, TYGS) and result (novel species).
4. **PDF fetch attempt #1 (PMC):** `curl` to PMC PDF endpoint returned a 1.8 KB HTML redirect — no dice.
5. **PDF fetch attempt #2 (F1000 direct):** `curl -L https://f1000research.com/articles/12-1373/v3/pdf` → 1.46 MB, 10-page PDF ✓.
6. `pdftotext` → 1327 lines; grep pulled the assembly accession (CP124620), genome size (4,487,389 bp), gene counts (4,147 / 4,066 CDS + 81 rRNA/tRNA), coverage (166×), GC (66.5 %), and the paper's own tool stack (Canu 1.7, TYGS, RAST, BlastKOALA, PHASTER, FastME).
7. Fetched CP124620 FASTA via EUtils efetch (`rettype=fasta`) → 4.55 MB.
8. Python one-liner over the FASTA → **length 4,487,489**, **GC 66.519 %**, **100 Ns**. Δ of 100 bp vs paper is fully explained by the Ns.
9. Linked CP124620 → assembly 16697841 → `GCF_030128875.1`, `ASM3012887v1`, submitter `Universidad de Córdoba`, submission date `2023-05-30`, chromosome-level, 1 contig, coverage 164.
10. Fetched feature table (`rettype=ft`) → parsed with regex → **4,081 genes, 3,995 CDS, 71 tRNA, 10 rRNA, 1 tmRNA, 4 ncRNA**. Compared vs paper's RAST (4,147/4,066/81) → within 1.6 % (expected annotator variance).
11. Extracted three 16S rRNA copies from feature table (positions on minus strand, coords 3541604–3543150; on plus strand 3944467–3946013 and 3950162–3951708), reverse-complemented as needed, wrote separate FASTA files. All three copies are 1,547 bp and identical.
12. `blastn -remote` against `nt` filtered to `Stenotrophomonas[Organism]` → **100 % identity to S. bentonitica, S. rhizophila, and other Stenotrophomonas assemblies** → confirms paper's C6 (16S is not a species-resolving marker in this genus).
13. Fetched two closest publicly-available *Stenotrophomonas* references (CP118898 *S. rhizophila*, OZ345833 *S. bentonitica*) via EUtils.
14. Ran `skani triangle` (learned-ANI) on the three-genome set:
    - *S. goyi* vs *S. rhizophila* = **86.30 % ANI** (align fraction ~30 %) → different species.
    - *S. goyi* vs *S. bentonitica* = **86.48 % ANI** (align fraction ~32 %) → different species.
    - Control *S. rhizophila* vs *S. bentonitica* = 94.00 % (near boundary).
    Both cross-species ANIs are far below the 95 % boundary → C5 ("novel species") independently supported.
15. Assembled evidence dir with features table, skani TSV, BLAST TSV, assembly summary JSON, genome_stats JSON, abstract.
16. Authored REPORT.md, brief.md, attempt_log.md, artifact_harvest.md, artifacts_summary.md, workflow.md, failure_analysis.md, open_questions.json, REPORT.tex.
17. Wrote extraction/marker.md (pdftotext fallback) and extraction/nougat.mmd (stub pointing to central manifest) — matches BVBRC-100/101/… pattern for fallback env.

## What worked
- F1000 direct PDF URL bypassed the PMC HTML wrapper.
- EUtils gave the assembly + feature table cleanly with no rate-limit trouble.
- skani `triangle` produced a defensible ANI-based species-boundary check in <100 ms.
- `blastn -remote` returned in ~30 s.

## What didn't
- PMC PDF endpoint returns HTML (needed F1000 direct fallback).
- No Marker/Nougat binaries in this host → fell back to pdftotext + stub (documented; matches project pattern).
- NCBI Datasets `datasets_report` REST endpoint returned `{}` for a raw nuccore accession; had to link nuccore → assembly first via elink, then hit `esummary db=assembly`.
