# Parser Provenance — Kandasamy et al. 2022 Re-pass

## Source PDF
- **File:** `paper/paper.pdf` (already present in project)
- **Size:** 1,215,843 bytes
- **DOI:** 10.3390/ijms232214494
- **PMID:** 36430971
- **MDPI URL:** https://www.mdpi.com/1422-0067/23/22/14494 (open access, no self-fetch needed; file already in repo from pass 1)

## Parser used in re-pass (2026-06-23)
Pass-2 claim extraction was done from text rendered with `pdftotext -layout`:

```bash
pdftotext -layout paper/paper.pdf /tmp/paper.txt
```

- Tool: `pdftotext` from Poppler (`/usr/local/bin/pdftotext`).
- Reason: managed pdf-vision tool unavailable in this subagent context (Anthropic credit error; gpt-5.5 extract plugin disabled). Plain-text extraction is sufficient because the paper's quantitative claims live in numbered tables (Tables 1–6) and inline counts; `-layout` preserves table column alignment well enough to read every number verbatim.
- All numbers cited in REPORT.md re-pass were cross-checked by line number in `paper.txt` (line numbers preserved in working notes).

## Pass-1 parser
Pass 1 used a different (now-unavailable in this context) vision PDF reader. Pass 1's claim list was loaded from `report/REPORT.md` and re-examined; no claim count or value was altered without re-reading the corresponding source line in `paper.txt`.

## Provenance of input artifacts re-used from pass 1
Re-pass does NOT regenerate the genome assembly or Prokka annotation; it consumes the pass-1 outputs:

| Artifact | Path | Pass-1 origin |
|---|---|---|
| Assembly FASTA | `data/DJF10_assembly.fasta` | SPAdes v4.2 `--isolate --only-assembler` on subsampled trimmed reads |
| Prokka GFF | `data/prokka_annotation_final/DJF10.gff` | Prokka v1.15.6 (`--noanno`) |
| Prokka GBK | `data/prokka_annotation_final/DJF10.gbk` | Prokka v1.15.6 (`--noanno`) |
| Predicted proteins | `data/DJF10_proteins.faa` (3,169 CDS) | Prokka v1.15.6 |
| SwissProt blastp hits | `data/sprot_annotation.tsv` | manual blastp vs Prokka-bundled SwissProt |
| Raw reads | `data/SRR14598288_{1,2}.fastq` | SRA toolkit `prefetch`+`fasterq-dump` |

## Re-pass code/output layout
- New scripts: `code/repass/<step>.sh` and `.py`
- New outputs: `results/repass/<topic>/`
- Topics: `prophage/`, `subsystems/`, `kegg/`, `cazy/`, `islands/`, `bacteriocin/`, `databases/`

## Honesty notes
- This re-pass uses ONLY free / locally-installable tools (no BV-BRC web jobs, no PHASTER/PHASTEST API, no BAGEL4, no IslandViewer, no BlastKOALA, no dbCAN webserver, no antiSMASH).
- Where a specific tool is web-only, the re-pass uses the closest open-source equivalent and explicitly labels the substitution.
- Where a free equivalent cannot be installed in this session, the claim is marked BLOCKED with the exact missing artifact named.
