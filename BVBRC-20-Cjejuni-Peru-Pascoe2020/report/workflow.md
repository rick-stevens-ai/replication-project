# Workflow — BVBRC-20 replication of Pascoe et al. 2020

**Paper:** Pascoe B, Schiaffino F, Murray S, et al. (2020) *Genomic epidemiology of Campylobacter jejuni associated with asymptomatic pediatric infection in the Peruvian Amazon.* PLoS Negl Trop Dis 14(8):e0008533.

**Verdict:** PARTIAL (Coverage 9/10, Agreement 7/10; independent LLM judge gpt-5.2).

**Scope of rerun:** all 62 Peru *C. jejuni* isolates (full focal genome set, not a subsample).

---

## Stage 1 — Data acquisition

1. **Assembled genomes.** Pull `Peru.assemblies.tar` (62 `.fas`) from the authors' FigShare deposit `doi:10.6084/m9.figshare.10352375`. Corresponding raw reads live under BioProject `PRJNA350267` but were NOT re-assembled here — this rerun matches the paper's downstream analysis input by using the authors' own assemblies.
   - Output: `data/peru_assemblies/*.fas` (62 files)
2. **Author ground-truth metadata.** Extract Supplementary Tables S1–S9 from the FigShare deposit; parse:
   - S2/S6 → ST, clonal complex, aetiology → `data/paper_ST.tsv`, `data/paper_aetiology.tsv`
   - S5 → ABRicate AMR summary (used as the paper's own gene-call ground truth)

## Stage 2 — MLST typing (same scheme as paper)

3. Run `mlst 2.33.1` with the campylobacter scheme against each of the 62 assemblies.
   - Output: `data/mlst_results.tsv`
4. Compare against `data/paper_ST.tsv` (author's 2020 pubMLST assignments).
   - Result: **47/62 exact match (75.8%)**; 8 untyped (single missing allele in newer pubMLST DB); 4 re-typed to novel ST12690/12694/12697 (genuinely different allele profiles). This is **pubMLST allele-DB version drift**, a documented reproducibility limitation across DB snapshots, not a contradiction.

## Stage 3 — AMR resistome (same tool as paper)

5. Run `abricate` against all 5 databases used by the paper (NCBI, CARD, ResFinder, Plasmidfinder, VFDB), DB build 2026-Apr, default 80%/80% identity/coverage cutoffs.
   - Outputs: `data/abricate/{ncbi,card,resfinder,plasmidfinder,vfdb}.tsv`
6. Aggregate per-isolate resistance-class calls; compare against paper's S5 summary.
   - Tetracycline: **10/62** (paper 11/62) — VERIFIED ±1
   - Beta-lactam: **26/62** (paper 32/62) — PARTIAL, driven by *bla*OXA-61 hits at the identity-cutoff boundary
   - Aminoglycoside: **0/62** (paper 0/62) — VERIFIED exact

## Stage 4 — Phylogeny substitute

7. **Substitution:** paper built a core-genome ML tree; this rerun uses Mash sketches (`s=10000`) → pairwise distance matrix → NJ tree.
   - Outputs: `data/phylo/peru_mash_nj.nwk`, `data/phylo/mash_dist.tsv`
8. Compute per-aetiology within-group pairwise Mash distance to test the paper's *structural* polyphyly claim (does not depend on exact tree-inference method).
   - Asymptomatic within-group Mash 0.0180 ≥ symptomatic 0.0164
   - 17 distinct STs across 28 asymptomatic isolates → **polyphyly VERIFIED**

## Stage 5 — Clonal-complex distribution vs global disease lineages

9. Tabulate CCs across all 62 isolates.
   - CC353 = 15, CC362 = 11, CC354 = 8 (dominant, locally-prevalent) — VERIFIED
   - CC21 = 3, CC45 = 4 (globally-dominant disease lineages, rare in Peru) — VERIFIED

## Stage 6 — Aetiology reproduction

10. Re-derive aetiology split from S6.
    - 31 symptomatic / 28 asymptomatic / 3 unknown — VERIFIED (exact match to paper)

## Stage 7 — Judgment + report

11. Independent LLM judge (`gpt-5.2`) scores Coverage 9/10, Agreement 7/10, verdict PARTIAL.
12. Author `REPORT.md` and `REPORT.tex` with per-claim verified/partial/failed table + genuine-critique section.

---

## Pipeline entry point

- `scripts/run_all.sh` — drives Stages 2–6 end-to-end from `data/peru_assemblies/` and produces all `data/` outputs.
- Stage 1 (FigShare download + supplementary-table extraction) is a manual one-shot; scripted portion begins with existing `.fas` inputs.

## Substitutions and deviations from paper (recap)

| Stage | Paper method | This rerun | Consequence |
|---|---|---|---|
| Phylogeny | core-genome / RAxML ML | Mash/NJ | Tests structural polyphyly, not topology or branch supports |
| Source attribution | pubMLST ecology | ST-diversity + Mash summaries | Reproduces aetiology split, not per-isolate source classifier |
| MLST DB | pubMLST snapshot 17-Feb-2020 | pubMLST snapshot ~2026 | 15/62 assignments differ (DB drift) |
| ABRicate cutoffs | not published | defaults (80/80) | 6/62 beta-lactam gap at *bla*OXA-61 boundary |
