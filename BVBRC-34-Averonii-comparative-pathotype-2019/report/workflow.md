# Workflow — BVBRC-34 Replication of Tekedar et al. (2019)

**Paper:** Tekedar HC et al., *Comparative genomics of Aeromonas veronii: Identification of a pathotype impacting aquaculture globally*, PLoS ONE 14(9):e0221018 (2019). DOI 10.1371/journal.pone.0221018.
**Compute:** uicgpu (8×A100), envs `/data/stevens/envs/bvbrc28` + `bvbrc14`. Free tools only.
**Wall-clock:** ~30 min (dominated by 41 parallel abricate BLAST runs).

## Stage 0 — paper + Table 1 acquisition
1. Fetch Europe PMC OA XML + PDF for PMC6715197.
2. Extract Table 1 (41 strains + their 2018 GenBank/WGS accessions).
3. Save `paper.pdf` and `paper_fulltext.xml` under `work/`.

## Stage 1 — resolve 2018 accessions to current NCBI assemblies
4. Query NCBI Datasets v2: `datasets summary genome taxon "Aeromonas veronii"` → today's corpus size (1,927 genomes vs 41 in 2018).
5. Run `match_accessions.py`: map each Table-1 accession to a current assembly by WGS-project prefix (e.g. `LXJN` → `GCF_001696435.1`) or by strain-name lookup (e.g. `TH0426` → `GCF_001593245.1`).
6. **Outcome: 41/41 resolved.** Write `resolved.tsv`.

## Stage 2 — download genomes + proteins
7. `datasets download genome accession --inputfile acc_list.txt --include genome,protein --filename av41.zip` (92 MB).
8. Unpack into `work/av41/` with per-strain subdirs.

## Stage 3 — genome statistics (C2)
9. `setup_and_stats.py` (pure Python, no Biopython dep): per assembly compute length, GC%, contig count, protein count.
10. Compare each row to Table 1 (size delta, GC delta). 41/41 match within noise; Hm21 differs by 0.082 Mb because NCBI upgraded it to a complete assembly (`GCF_000464515.2`).

## Stage 4 — Average Nucleotide Identity (C1, C2)
11. `run_ani.sh`: fastANI all-vs-all with `--ql` and `--rl` over the 41 genome FASTAs → 1,681 pairs → `ani_all.tsv`.
12. `analyze_ani_pan.py`: extract ML09-123's ranked neighbours; compute species-wide ANI distribution; render 41×41 heatmap (`ani_heatmap.png`).
13. **Key readout:** ML09-123 × TH0426 = 99.927%; 2nd-nearest = 96.484% (AVNIH2 / CCM4359). Species coherence: all 1,640 non-self pairs in [95.9%, 100.0%], 0 pairs below the 95% species boundary.

## Stage 5 — mash-distance phylogeny (C1)
14. `run_phylo.sh`: `mash sketch -s 100000` on each assembly + all-vs-all distance → `mash_dist.tsv`.
15. `make_figures.py`: SciPy average-linkage dendrogram → `phylo_dendrogram.png`; write ML09-123 nearest neighbours to `mash_ml_nearest.json`.
16. **Key readout:** ML09-123 nearest = TH0426 (d = 0.00171); next-nearest = Hm21 (d = 0.03151), ~18× farther.

## Stage 6 — Pan/core genome (C3)
17. `run_pangenome.sh`: concatenate all 166,630 predicted proteins with strain-tagged headers.
18. Cluster with CD-HIT at 70% identity / 70% coverage (`cd-hit -c 0.70 -aL 0.7`) — free ortholog-cluster proxy for EDGAR's BLAST-score-ratio method.
19. `analyze_ani_pan.py` counts pan (all clusters), core (≥99% of genomes), strict core (100%), and the frequency spectrum → `ani_pan_results.json`.
20. **Key readout:** pan 9664 (vs paper 8710, +11% algorithm delta); core 2834 (vs paper 2855, within 0.7%); core fraction 29.3% (vs paper 30.9%); 3,319 genome-unique cloud genes ⇒ open pan-genome supported.

## Stage 7 — Virulence-factor profiling (C4, C5)
21. `run_vfdb.sh`: abricate 1.4.0 with bundled VFDB (4,592 sequences — the same DB the paper used) run on each of the 41 genomes.
22. `analyze_vfdb.py` builds the strain × VF-gene presence matrix; computes per-genome VF load, core vs variable VF genes, ML09-123↔TH0426 overlap, and secretion-system / T4P / flagellum / TAD keyword buckets → `vfdb_results.json` + `vf_counts.png`.
23. **Key readouts:** ML09-123 (136 VFs) ∩ TH0426 (136 VFs) = 136 shared, Jaccard 1.000 (identical). 159 total VF genes across 41 genomes; 58 core, 101 variable (63.5%). T1SS/T2SS/T4P/flagellum in 41/41; T3SS in 31/41; T6SS in 28/41; TAD in 12/41; T5SS un-labelled in VFDB (untestable).

## Stage 8 — Independent LLM-judge verdict
24. `judge.py` assembles the evidence bundle (all Section 4 tables + numbers) and posts to a free Argo endpoint.
25. Try `argo:claude-opus-4.8` first — got a transient 502.
26. Fall back to `argo:gpt-5.2` (free) per the wave brief's free-endpoint rule (never paid). Save verdict to `evidence/llm_judge_verdict.txt`.
27. **Judge output:** PARTIAL, coverage 5/5, agreement 5/5.

## Stage 9 — report assembly
28. Write REPORT.md with the paper summary, claim table, method, results-vs-paper, coverage/agreement, honest caveats, and reproducibility artifacts.
29. Package `evidence/` (all TSVs, JSONs, PNGs, judge verdict) and `work/` (scripts + downloaded data manifest).

## Reproduction one-liner
```bash
export PATH=/data/stevens/envs/bvbrc28/bin:/data/stevens/envs/bvbrc14/bin:$PATH
datasets download genome accession --inputfile acc_list.txt --include genome,protein --filename av41.zip
python3 setup_and_stats.py
bash run_ani.sh && bash run_pangenome.sh && bash run_phylo.sh && bash run_vfdb.sh
python3 analyze_ani_pan.py && python3 analyze_vfdb.py
python3 make_figures.py && python3 judge.py
```

## Wave rules honored
- Free endpoints only (Argo opus 502 → gpt-5.2 fallback, never paid).
- Real public data (NCBI Datasets, VFDB) — no fabricated numbers.
- Independent LLM-judge verdict included.
- Wrote only inside the assigned target dir; no sibling directories touched.
- No paid API calls in the entire pipeline.
