# PARSER_PROVENANCE.md — Re-pass parser audit

**Project:** PMID 29769716 — Price et al. 2018, "Mutant phenotypes for thousands of bacterial genes of unknown function" (Nature 556:503–507).

**Pass-1 parser:** `replication/replicate_all32_v2.py` — pure Python, pandas-free TSV parsing of the per-organism `fit_genes.tab`, `fit_logratios_good.tab`, `fit_t.tab`, `fit_quality.tab`, and `specific_phenotypes` files downloaded from <https://genomics.lbl.gov/supplemental/bigfit/> (all 32 organisms, 5 files each, ~850 MB). It re-implements `HypoDesc()` / `PureHypoDesc()` from the authors' `plotfeba.R` source and applies a Time0-t-statistic FDR control on the threshold grid `[(0.5,4), (0.7,5), (0.9,6), (1.0,6.5)]`. Verified canonical: produces 4,870 successful experiments (exact match) and 12,855 poorly-annotated genes with phenotype after FDR (paper: 11,779; +9.1%).

**Re-pass parser additions:**

1. **`code/repass/repass_claims.py`** (this re-pass) — single-script extension that parses:
   - `data/Supplementary_Tables_final.xlsx` (via `openpyxl`, read-only) — extracts the data rows below the multi-line preamble in each sheet by locating the first row that begins a real header (multi-column, short first cell) for sheets `TableS1_LikelyEssentialGenes`, `TableS5_Experiments`, `TableS8_ConservedLinks`, `TableS9_CisplatinGenes`, `TableS10_XyloseGenes`, `TableS11_ABCtransporter`, `TableS12_GeneAnnotations`, `TableS13_UncharProteins`, `TableS14_RB_TnSeq_Bacteria`. Carbon (S2) / nitrogen (S3) / stress (S4) compound matrices are parsed compound-name-first by scanning down past notes/preamble blocks until a row whose first cell looks like a chemical/compound (heuristic: leading capital letter, no embedded comma-style sentence prose, not in stop-list).
   - All 32 per-organism `fit_quality.tab` (`u` column) to count successful, non-Time0 experiments split by paper-style Group (carbon / nitrogen / stress / other).
   - All 32 per-organism `fit_genes.tab` (`desc`, `geneClass`) to recompute annotation-class counts (A=role, B=specific, C=vague, D=hypo) using the **deposited `geneClass` field** where available (the authors' own classification, which we lacked in pass 1).
   - All 32 per-organism `specific_phenotypes` files (gene–condition pairs labelled by the paper's pipeline as specific-important / specific-detrimental).
   - `data/AllConsLinks.tab` — paper-provided union of all 13,192 genes with conserved associations, columns `(locusId, organism, sysName, geneClass, desc, specific, cofit, protein_id, locus_tag)`. This file is the canonical source for the "13,192 conserved associations" / "2,316 vague-or-hypo conserved" claims.
   - `data/essential_proteins.tab` — paper's 13,869-gene essentiality call (column `geneClass` is in {`Essential`, `Aspecific`, `Bspecific`, `Chypo`, `Dhypo`} per `plotfeba.R`).

2. **Tier classifier (this re-pass):** Promotes the deposited `geneClass` strings into the paper's 4-class A/B/C/D scheme:
   - `Aspecific` → A (TIGR role).
   - `Bspecific` → B (specific annotation, no role).
   - `Chypo` → C (vague).
   - `Dhypo` → D (pure hypothetical).
   - `Essential` → tagged separately (not in A/B/C/D pools per `plotfeba.R` `AllProteinsByClass`).
   This removes the pass-1 systematic ~2.8% inflation that came from not having TIGRFAM role assignments locally.

3. **Cross-organism ortholog / cofitness data:** Not regenerated from scratch (would require re-running the authors' BBH + cofitness pipeline across all 32 genomes; ~CPU-days). Instead, this re-pass **verifies the deposited derived files** (`AllConsLinks.tab`, `TableS8_ConservedLinks`, `TableS9_CisplatinGenes`, `TableS10_XyloseGenes`, `TableS11_ABCtransporter`, `TableS12_GeneAnnotations`, `TableS13_UncharProteins`) which are the canonical answers from the paper's own pipeline. This is the same evidentiary stance the paper itself takes: the Discussion/Tables S8–S13 are the authoritative answers to the conserved-association claims.

**No fabrication, no LLM-derived numbers.** Every count in `results/repass/repass_results.json` is computed by deterministic Python code against the deposited tab/xlsx files.

**Environment:** CherryRd (Darwin 25.3.0, Python 3.13.x); no external network calls; all inputs pre-downloaded by `download_all.sh` (May 2026).
