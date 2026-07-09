# Attempt Log — BVBRC-29

All times CDT, 2026-07-01. Compute host: uicgpu (`/data/stevens/bvbrc29`), env `/data/stevens/envs/bvbrc28`.

- **21:38** Task received. Prior attempts died on transient empty-LLM-response; PDF+txt already present in `work/`. Resumed from text.
- **21:39** Read WAVE_BRIEF. Confirmed uicgpu reachable (uicgpu01, 255 cores).
- **21:40** Extracted claims from `work/bazinet2017.txt`. NOTE: task metadata said "Liu et al." but the downloaded paper is **Bazinet AL 2017** (single author) — same PDF. Proceeded with Bazinet.
- **21:41** `bvbrc28` env not on default PATH; found at `/data/stevens/envs/bvbrc28`. Activated by full path — all tools present (Mash 2.3, FastANI 1.34, Roary 3.12.0, Prokka 1.12, datasets 18.32.0, FastTree, MAFFT).
- **21:42** Built 27-genome accession list (Table 1 references + root taxon B. manliponensis + extra anthracis/cereus/thuringiensis for clonality tests). Wrote REPORT.md scaffold + claims table + brief.md.
- **21:43** `datasets download genome accession` — 27 genomes, 41 MB zip, all validated. Flattened to `fasta/<label>.fna`.
- **21:44** Genome stats: mean 5.22 Mbp, GC ~35.4%. Flagged `B_cereus_4` (partial 2.1 Mbp) + `B_thuringiensis_7` (GC 37.8%).
- **21:44** Mash sketch (k=21 s=1000, paper's params) + all-vs-all dist (729 pairs). FastANI all-vs-all (627 pairs).
- **21:45** ANI analysis: B. anthracis near-clonal (99.99–100% ANI), anthracis nested in B. cereus s.s. (max 99.98%), group median ANI 91.8%. → C3, C4 supported. Saved evidence.
- **21:46–~22:20** Prokka annotation of all 27 genomes (background, ~1–1.5 min each). Completed 27/27 GFF.
- **~22:22** Roary launched (`-e --mafft -p 32 -i 95 -cd 99`) for core/pan-genome + core alignment. (cd 99 = core defined at 99% presence, matching Bazinet's core definition.)
- **~22:29** Roary Run A (full 27, blastp 95%): 0 strict core, 48,118 total pan-genome (open). Expected for full species span at 95%.
- **~22:32** Roary Run C (17-genome homogeneous Clade-1 subset, blastp 95%): **2,415 core**, 15,247 total. Roary Run B (26 genomes, blastp 80%): **251 core**, 26,839 total — both same order of magnitude as paper's ≈600.
- **~22:35** Core-gene alignment (MAFFT, 17 taxa) produced; accessory binary tree already present.
- **~22:40–22:53** FastTree GTR on Clade-1 core alignment. First attempts slow (GTR opt on ~2.5M cols); killed competing runs, ran one clean instance → `core_gene_tree_clade1.nwk` (502s). Topology: 7 anthracis clonal + intermingled with cereus/thuringiensis. Accessory binary tree concordant.
- **~22:55** Pan-genome accumulation curves: pan rises 5,523→15,247, new-genes stays high (17th genome +492) → open pan-genome (C6).
- **~22:56** LLM-judge via free Argo. `claude-opus-4.8` returned HTTP 502 ×3 (the transient empty-response failure mode) → retry+fallback loop fell through to `gpt-5.2`, which returned clean JSON. Overall **PARTIAL**; C3/C4/C6 REPRODUCED, C1/C5 PARTIAL, C2 OUT-OF-SCOPE.
- **~22:58** Finalized REPORT.md, harvested all evidence to `report/evidence/`. DONE.

## What worked / what failed
- **Worked:** NCBI datasets download; Mash/FastANI (fast, decisive for clonality); Prokka (all 27 clean); Roary at multiple identity thresholds to fairly test core across divergence; free-Argo judge with fallback.
- **Failed/handled:** Roary at default 95% gives 0 core for a whole-species-span set (expected, addressed with i80 + homogeneous subset). FastTree GTR is slow on large core alignments and only writes output at the end (looked like a hang — it wasn't). opus-4.8 transient 502 handled by model fallback.
- **Lesson:** the task's "empty-LLM-response deaths" = Argo `claude-opus-4.8` intermittently 502s. Always wrap free-Argo judge calls in retry + multi-model fallback; write REPORT.md incrementally so a mid-run death loses nothing.
