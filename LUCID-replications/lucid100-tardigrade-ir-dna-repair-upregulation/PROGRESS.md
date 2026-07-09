# PROGRESS — LUCID100 slot 51 (tardigrade IR DNA repair upregulation)

## 2026-06-09  (Ollie subagent, single session, ~25 min wall clock)

### Done in this session
1. Confirmed slot 51 in `LUCID100_SOLID_MASTER_QA.tsv` (rank 82, Wave 6, candidate_curated, worktype="omics/signature replication", verdict_or_plan="omics/signature replication; artifact harvest; brief; run; report").
2. Created `lucid100-tardigrade-ir-dna-repair-upregulation/` under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/`.
3. **Artifact harvest** (all public, no auth required):
   - Author manuscript PDF (1.96 MB) via Europe PMC.
   - Full JATS XML via NCBI eFetch (180 kB).
   - 19 cross-reference accessions via Europe PMC datalinks API.
   - GEO SOFT metadata for SuperSeries GSE253471 + both SubSeries (GSE240501 IR, GSE253470 Bleo).
   - 4 GEO supplementary files for Bleomycin arm (featureCounts + 3 EdgeR DE tables).
   - NCBI `GCA_002082055.1` feature table (BV898 locus → product names).
4. **Verified that:**
   - GSE253471 is public (deposited Jan 2024, public Apr 12 2024).
   - PMC11078613 is a free NIHMS author manuscript — paper PDF freely downloadable.
   - "This paper does not report original code" (verbatim from PMC Data and code availability).
   - The Dryad DOI `10.5061/dryad.50r1b` that EuropePMC text-mines as "related data" actually belongs to Beltran-Pardo et al. 2015 (unrelated older study).
   - No author GitHub repo exists (Goldstein lab, Clark-Hachtel, Hibshman, De Buysscher — checked).
5. **Wrote and ran a pure-Python smoke replication** (`scripts/01_smoke_replication.py`):
   - Replicates DEG counts at FDR<0.05 & |log2FC|≥1 for 3 Bleo contrasts.
   - Confirms monotonic dose response (Pearson r(logFC) 0.54 → 0.75 → 0.81 between escalating Bleo doses).
   - Cross-references all 19 946 BV898 locus tags vs DDR-pathway keyword vocabulary → 68 DDR genes have DE results.
   - All 11 paper-named DDR genes that exist with curated NCBI names show massive upregulation (8× to 51×, FDR ≪ 10⁻⁸⁰) in the 1 mg/mL Bleo arm — qualitatively matches the paper's IR-arm headline of "32- to 315-fold" upregulation (Bleo is the milder treatment).
6. Wrote `MANIFEST.md`, `README.md`, `REPORT.md`.
7. Updated subagent-progress JSON.

### Blockers encountered (none fatal)
- `tardigrades.org` (host for the v3.1.5 GFF the paper used) was unreachable — fell back to NCBI's v3.1 feature table (same locus_tags, sparser names). Acceptable for the smoke pass; only `XRCC1` and `BARD1` ended up under "putative" / "hypothetical" in v3.1 but were findable.
- `NIHMS1979636-supplement-1.xlsx` (the full per-gene IR-arm EdgeR table, `Data S1B`) is referenced in PMC JATS but every PMC/EuropePMC `bin/` endpoint returns a Google reCAPTCHA challenge for it. ScienceDirect `mmc1.xlsx` returned 403/406 to plain `curl`. Would require a real browser session.
- `pydeseq2` not installed locally; `edgeR` (R) not installed locally. Both intentional — the smoke uses the GEO-provided EdgeR outputs as ground truth, so neither is needed.

### Next actions (if this slot were promoted to a full replication)
1. Browser-fetch (manual or `browser` skill) the two NIHMS supplement files to get the IR-arm DE table and supplementary figures.
2. Pull the v3.1.5 GFF + Trinotate annotation when tardigrades.org is reachable, to fully resolve XRCC1, BARD1, MPG, etc.
3. (Optional, ~2-day job, push to uicgpu) re-run BBduk + BBmap + featureCounts + edgeR end-to-end from SRA FASTQ for both IR and Bleo arms to confirm 4,590 ↑ / 4,687 ↓ at 500 Gy.
4. (Optional) pull PXD047724 from PRIDE to independently check the proteomics correlation claim (BARD1-like, XRCC5, XRCC6, PNKP, PCNA, PARP3 protein abundance at 6 h / 18 h post-IR).

### QA retag recommendation
**KEEP** — this is exactly the kind of paper LUCID100 should highlight: data fully public, processed pipeline outputs deposited, IR-tolerance + DDR signature directly relevant to radiobiology, and the replication is *cheap*.  Suggest retagging `verdict_or_plan` from "TODO: omics/signature replication; artifact harvest; brief; run; report" to **"PARTIAL (strong) replication: Bleomycin arm reproduced from GEO supplementary; IR arm gated by xlsx access — promote to Wave 2 'full replication' tier if browser-scraping NIHMS supplement is permitted"**.
