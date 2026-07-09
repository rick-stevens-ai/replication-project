# Attempt Log — BVBRC-50 (2026-07-01 night)

1. **Dedup check.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "oncorhynchi|Z-P2|ZP2"` → no existing dir (BVBRC-41 is S. algae 2NE11, different). Proceeded.
2. **Read** wave brief + BVBRC-17 exemplar REPORT.md for structure.
3. **Paper harvest.** web_search + web_fetch of PMC10745600 (OA, CC BY). Extracted all quantitative claims (genome 5,034,612 bp / 45.4% GC / 4544 CDS / 109 tRNA / 31 rRNA; 5 BGCs w/ coordinates; pan 9228 / core 2681 / 618 unique; closest YZ08 ANI 90.09%; UPLC-MS m/z 373.21). Genome accession CP132914.
4. **Env.** uicgpu; bioinformatics tools in conda env at `/data/stevens/envs/bvbrc28` (datasets, prokka 1.12, roary 3.12, fastANI, blast, mash). Note: conda not on non-interactive PATH; used explicit `/data/stevens/envs/bvbrc28/bin` prefix. env vars via `~/env.sh` (proxy for internet).
5. **Resolve strain.** `datasets summary genome taxon "Shewanella oncorhynchi"` → Z-P2 = GCF_030848765.1 (len 5,034,612 = exact paper match).
6. **Download** Z-P2 + 10 S. putrefaciens complete RefSeq genomes (incl. YZ08 = GCF_019599085.1) via NCBI Datasets REST. Extracted fna/faa/gff.
7. **C1/C2.** `genome_stats.py` on FASTA → length 5,034,612 EXACT, GC 45.40 EXACT, 1 contig. GFF feature counts → 109 tRNA EXACT, 31 rRNA EXACT, 4290 CDS (PGAP; vs 4544 RAST — pipeline difference).
8. **C5.** fastANI Z-P2 vs all → closest = YZ08 91.25% (paper 90.09%), all comparators <95%. Closest-strain identity EXACT.
9. **C3.** Extracted CDS products in each of the paper's 5 antiSMASH coordinate windows from RefSeq GFF → all 5 BGC types verified by marker enzymes (putrebactin: IucA/IucC + ornithine monooxygenase; EPA: PfaD/PfaB; RiPP: YcaO; etc.). antiSMASH not re-run (not installed).
10. **C4.** Prokka on all 11 genomes (6-way parallel, ~3–4 min). Roary at default 95% id → over-split (17326 pan / 684 core). Reran at 70% id → 9332 pan (+1.1% vs 9228), 2656 core (−0.9% vs 2681), Z-P2 unique 531 (paper 618). Threshold sensitivity documented.
11. **Scoring.** LLM-judge via Argo gpt-5.2 (free) with full claim evidence → PARTIAL, 2 STRONG + 3 MODERATE, coverage 5/7, no contradictions.
12. **Assembled** report/ (REPORT.md, brief.md, attempt_log.md, artifact_harvest.md) + evidence/ + work/. Genomes/annotations retained on uicgpu.

## What worked
- NCBI Datasets strain resolution nailed the exact assembly (length match confirmed correct genome).
- Genome-level stats + tRNA/rRNA + closest strain reproduced exactly.
- Pan/core reproduced within ~1% once orthology threshold was matched to PanOCT-style grouping.

## What was tricky / failed
- conda not on PATH in `ssh uicgpu` non-interactive shells; had to hardcode env bin path. Env actually at `/data/stevens/envs/bvbrc28`, not `~/anaconda3/envs`.
- antiSMASH absent → used marker-gene verification at published coordinates instead of full BGC re-call.
- Roary 95% default massively inflates pan-genome vs PanOCT; had to rerun at 70% for a fair comparison (lesson: pan-genome counts are only comparable at matched identity thresholds).
- C6 (UPLC-MS) and C7 (islands/virulence/CRISPR) not reproduced (wet-lab / extra tools) — honestly scoped out.
