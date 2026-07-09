# Attempt Log — BVBRC-81

Chronological, 2026-07-03 (CDT).

1. **10:06** Read wave brief `WAVE_BRIEF_2026-07-01.md`. Created target dir with `report/{evidence,}/` and `work/`.
2. **10:07** Fetched PubMed abstract for PMID 37894099 via NCBI EUtils efetch. Extracted key claims: 3,180,940-bp chromosome, 9 plasmids, 2,962 genes, 150+ probiotic markers, no virulence factors, bacteriocin cluster.
3. **10:07** Tried MDPI PDF direct — HTML "Access Denied" (Akamai geo/bot block) from CherryRd.
4. **10:08** Tried MDPI PDF from uicgpu — same Akamai block via proxy. Pivoted to Europe PMC full-text XML → **200,906-byte XML successfully retrieved**. This contains the full paper text.
5. **10:08** Parsed XML for key quantitative claims (grep-around-context). Extracted:
   - Chromosome 3,180,940 bp, coverage 162×, GC 44.65%
   - 9 plasmids 44,900 – 3,512 bp, GC 35.22–41.08%
   - Accessions **CP120642** (chromosome) + **CP120643–CP120651** (plasmids)
   - Genes: 2,962 total = 2,874 CDS + 88 RNA (72 tRNA + 16 rRNA)
   - Top ANI hit: M19 (**GCA_018588605.2**) at 99.60%
   - No virulence factors via Abricate/VFDB/CARD/MEGARes
   - Bacteriocin cluster at chromosome 1,561,101–1,586,810 (Plantaricin E/F/K + PlnT/U/V/W + LagD/LcnD)
   - CRISPR array at chromosome 1,306,053–1,306,616
6. **10:08** Verified all 10 accessions via NCBI EUtils esummary — every one exists, correct strain, correct sizes.
7. **10:08** Downloaded combined FASTA (3.4 MB) for all 10 replicons.
8. **10:08** Independently computed per-replicon and total length + GC using Python. Chromosome length **exactly 3,180,940 bp**; chromosome GC = 44.66% (paper 44.65%, matches within rounding); plasmid GC range 35.23–41.09% (paper 35.22–41.08%, matches within rounding); plasmid sizes match paper's Table 1 rows and bounds.
9. **10:09** Downloaded GenBank record. Feature counts (current 2024-11-18 PGAP re-annotation): 3,273 CDS, 72 tRNA, 16 rRNA, 3 ncRNA, 1 tmRNA — **rRNA/tRNA match paper exactly**; CDS differs from paper's 2,874 because record was re-annotated after publication.
10. **10:10** Queried BV-BRC API: found **genome ID 1590.5192**, confirming all 10 accessions, Nanopore platform, Flye assembly, Bulgaria/human host.
11. **10:11** Pulled BV-BRC specialty-gene tables: 3 low-quality Victors "virulence" hits (housekeeping metabolic genes only), 30 PATRIC AMR "paralog-of-known-target" hits (all core housekeeping genes) — consistent with paper.
12. **10:12** Copied `PU3_all.fasta` to `uicgpu:/data/stevens/replicate/BVBRC-81/` for heavy compute. Found `bvbrc28` conda env with prokka, mash, blastn, makeblastdb.
13. **10:13** Ran **Prokka 1.14.6** with `--fast --kingdom Bacteria --gcode 11 --cpus 32` → completed in 24 s. **Independent annotation**: 3,617 CDS, **16 rRNA (exact match to paper)**, **71 tRNA (one-off vs paper's 72, likely a boundary call)**, 1 tmRNA.
14. **10:13** Downloaded L. plantarum M19 (GCA_018588605.2) and WCFS1 (GCF_000203855.3) reference genomes.
15. **10:14** Ran **Mash 2.3** distance: PU3 vs M19 = 0.0031 (~99.7% ANI), PU3 vs WCFS1 = 0.0138 (~98.6% ANI).
16. **10:15** Installed fastANI via conda-bioconda in bvbrc28 env. Ran **FastANI**: PU3 vs M19 = **99.6132%** (paper claim: 99.60%) — essentially exact match; PU3 vs WCFS1 = 98.6118%.
17. **10:16** Installed **abricate 0.5** with bundled CARD, VFDB, ResFinder, ARG-ANNOT DBs.
18. **10:17** Ran abricate with default parameters (mincov 80, minid 80) — same tool + defaults as paper:
    - CARD: 1 hit (dfrE at 67.6% cov / 75.5% id — below default threshold)
    - VFDB: 5 fragment hits of clfA/clfB at 12–33% coverage (all below default threshold)
    - ResFinder: 0 hits
    - ARG-ANNOT: 0 hits
    → Under paper's stated method, **zero passing virulence/AMR calls**; paper's "no virulence factors" claim independently confirmed.
19. **10:18** Grepped Prokka GFF at the paper's bacteriocin coordinates (chromosome 1,561,101–1,586,810). Found bacteriocin/plantaricin-family machinery: **AgrA (accessory gene regulator)**, **LagD (Lactococcin-G-processing ATP-binding protein) × 2**, **LcnD (Lactococcin A secretion protein)**. Prokka's default databases do not annotate the tiny (30–50 aa) PlnE/F/K core peptides, but the secretion/regulation cluster is present at the exact coordinates — structural/positional match.
20. **10:19** Copied Prokka summary + FastANI + all 4 Abricate TSVs to `report/evidence/`.
21. **10:20** Attempted LLM-judge with `argo:claude-opus-4.7` — HTTP 502. Retried opus-4.8 — also 502 (Anthropic backend having a bad afternoon). Fell back to `argo:gpt-4o`.
22. **10:20** LLM-judge with **argo:gpt-4o** → **REPLICATED**.
23. **10:21** Cross-verified with **argo:gpt-5** → **REPLICATED**.
24. **10:21** Cross-verified with **argo:gemini-2.5-pro** → **PARTIAL** (dissent based on C8 gene-count discrepancy).
25. **10:22** Wrote report brief, artifact harvest, attempt log, evidence bundle, final report.

## What worked
- Europe PMC full-text XML as a reliable open-access proxy when MDPI is Akamai-blocked.
- NCBI EUtils for accession validation, FASTA/GenBank retrieval.
- `bvbrc28` conda env on uicgpu had all needed tools (prokka, mash, fastANI, blast, abricate) with only one small bioconda install for abricate.
- Independent FastANI reproduced paper's headline 99.6% ANI number **exactly**.

## What failed (recoverable)
- MDPI PDF direct — Akamai bot detection. Recovered via Europe PMC full-text XML.
- Argo `claude-opus-4.7` and `-4.8` returned HTTP 502 during the judge call. Recovered by switching to gpt-4o + gpt-5 + gemini-2.5-pro as free Argo alternatives.

## What could not be reproduced (honest)
- The paper's exact 2,962-gene total count (2,874 CDS + 88 RNA). This is fundamentally annotation-pipeline dependent: NCBI's current 2024-11-18 PGAP re-annotation gives 3,273 CDS, Prokka+Prodigal gives 3,617, BV-BRC gives 3,794. The paper's snapshot of the pre-publication PGAP output isn't recoverable without their exact tool/DB versions. This is a well-known bioinformatics limitation, not a scientific contradiction; the underlying assembly and RNA-gene counts (which are structural, not statistical) match exactly.
