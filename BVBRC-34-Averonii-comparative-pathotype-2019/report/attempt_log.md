# Attempt Log — BVBRC-34 (A. veronii comparative pathotype, Tekedar et al. 2019)

Date: 2026-07-01 (evening). Analyst: Ollie (subagent). Compute: uicgpu.

1. **Dedup** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "aeromonas|veronii"` → empty. No existing dir. Proceeded.
2. **Read** wave brief + BVBRC-17 exemplar REPORT.md (structure/standard).
3. **Located paper** via Europe PMC → PMC6715197, doi 10.1371/journal.pone.0221018. Fetched PDF (5.9 MB) + full-text XML (256 KB).
4. **Extracted claims + Table 1** from XML. Found the paper's central accession (ML09-123 = PPUW00000000) and the full 41-genome Table 1 with 2018 accessions. Key quantitative claims: pan=8710/core=2855; ML09-123≈TH0426; secretion-system conservation pattern; ~30% VF variation.
5. **uicgpu recon** — no bioinf tools on default PATH, but conda envs `bvbrc28` (datasets, mash, fastANI, cd-hit, prodigal, roary, prokka, fasttree) and `bvbrc14` (abricate + VFDB, blast, muscle, fasttree) exist from sibling waves. Reused them.
6. **Accession resolution** — pulled current NCBI A. veronii index (1927 genomes) via `datasets summary`; wrote `match_accessions.py` to map each Table-1 WGS/nuc accession → current assembly by WGS-prefix or strain name. **41/41 resolved.**
7. **Download** — `datasets download genome accession --inputfile acc_list.txt --include genome,protein` → av41.zip (92 MB). All 41 have protein.faa.
8. **Genome stats** — `setup_and_stats.py`: length/GC/contigs/proteins. **41/41 sizes & GC match Table 1** (only Hm21 +0.082 Mb, now a complete genome).
9. **fastANI** all-vs-all (1681 pairs). ML09-123×TH0426 = **99.927%**; next-closest 96.48%; species range [95.9,100], 0 pairs <95%.
10. **Pan/core** — CD-HIT 70/70 on 166,630 proteins → pan=9664, core(≥99%)=2834 (paper 2855), core%=29.3% (paper 30.9%). Core matches; pan +11% (algorithm diff).
11. **mash phylogeny** — ML09-123 nearest = TH0426 (0.00171), ~18× closer than next. Third independent confirmation of C1.
12. **VFDB** — abricate+VFDB on all 41 (first pass produced 40/41 due to a summary-line race; reran the 1 missing → 41/41). ML09-123 & TH0426 = **identical 136-VF profile (Jaccard 1.0)**. Secretion systems: T1SS/T2SS/T4P/flagellum = 41/41 conserved; T3SS 31, T6SS 28, TAD 12 = variable — matches paper. T5SS not labeled in VFDB (gap).
13. **Figures** — local venv (numpy/scipy/matplotlib): ANI heatmap, mash dendrogram, per-genome VF bar.
14. **LLM judge** — Argo. `argo:claude-opus-4.8` → transient HTTP 502; fell back to **`argo:gpt-5.2`** (free) per brief rule. Verdict: PARTIAL, coverage 5/5, agreement 5/5.
15. **Wrote report/** files; pulled evidence JSONs + figures back to Dropbox. Genome FASTAs (232 MB total incl. venv) kept on uicgpu; small evidence synced to Dropbox.

## What worked
- WGS-prefix accession resolution: clean 41/41.
- fastANI + mash + VFDB triangulation of the central pathotype claim — unusually strong, three independent signals all agree.
- Reusing sibling bvbrc conda envs saved a full bioconda install.

## What differed / caveats
- Pan-genome count algorithm-dependent (CD-HIT 9664 vs EDGAR 8710); core matches.
- T5SS un-testable via VFDB product labels.
- VFDB (abricate bundle) ≠ paper's VFDB-setB + CLC thresholds → %-variable differs, direction agrees.

## Failures logged
- VFDB primary source `mgc.ac.cn` unreachable through uicgpu proxy (squid ERR_DNS_FAIL). Fix: used abricate's bundled VFDB (identical 4592-seq DB) — the standard route anyway.
