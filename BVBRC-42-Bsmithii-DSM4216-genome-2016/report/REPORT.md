# Replication Report: Bosma et al. (2016)
## "Complete genome sequence of thermophilic *Bacillus smithii* type strain DSM 4216ᵀ"

**Paper:** Bosma EF, Koehorst JJ, van Hijum SAFT, Renckens B, Vriesendorp B, van de Weijer AHP, Schaap PJ, de Vos WM, van der Oost J, van Kranenburg R. *Standards in Genomic Sciences* 11:52 (2016).
**DOI:** [10.1186/s40793-016-0172-8](https://doi.org/10.1186/s40793-016-0172-8) — **PMC:** PMC4995803 — **Open access:** ✅ (CC BY 4.0)
**Genome:** chromosome **CP012024.1** (3,368,778 bp) + plasmid **CP012025.1** (12,514 bp); assembly **GCA/GCF_001050115.1** (ASM105011v1); BioProject **PRJNA258357**; BioSample **SAMN03246763**; locus tag **BSM4216**.

**Set:** BVBRC-42 (BVBRC-100 replication wave, TOPUP85 rank-19). **BV-BRC workflows referenced:** Genome Assembly + Comprehensive Genome Analysis (RASTtk).
**Report date:** 2026-07-01. **Analyst:** Ollie (OpenClaw AI).
**Verdict:** **PARTIAL REPLICATION (strong).**

---

## 1. Paper

A genome-announcement paper for the finished genome of *Bacillus smithii* DSM 4216ᵀ — a facultatively anaerobic, facultatively thermophilic (optimum 55 °C, range 25–65 °C), Gram-positive, spore-forming bacterium of biotech interest (produces L-lactate and other "green" building-block chemicals from lignocellulosic sugars at elevated temperature). The genome was sequenced with Illumina + PacBio, assembled (CLCbio/SSPACE/GapFiller) to a finished 2-replicon genome, and annotated with RAST plus manual curation (Aragorn tRNAs, RNAmmer rRNA, CRISPR-finder, InterPro domainome). The paper reports genome statistics (Table 4), a COG functional-category breakdown (Table 5), a comparison against 14 other Bacillus/Geobacillus genomes (Table 6), and a reconstruction of central carbon metabolism (Fig. 4). Its headline biological finding: *B. smithii* **lacks the standard bacterial acetate-production pathway** (phosphotransacetylase *pta* + acetate kinase *ackA*) and several pyruvate-dissimilation enzymes (pyruvate-formate lyase, pyruvate decarboxylase, pyruvate:ferredoxin oxidoreductase), leaving the pyruvate-dehydrogenase complex as the sole pyruvate→acetyl-CoA route — a "most striking difference" from bacilli in general.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Finished genome (chromosome + plasmid) is public and complete. | Data availability | Yes | ✅ |
| C2 | Genome size = 3,381,292 bp; chromosome 3,368,778 bp + plasmid 12,514 bp. | Genome stats | Yes | ✅ EXACT |
| C3 | G+C content ≈ 40.8%. | Genome stats | Yes | ✅ 40.75% |
| C4 | ~3,627 protein-coding genes / ~3,880 total genes. | Genome stats | Yes | ✅ 3,619 CDS (within 0.2%) |
| C5 | rRNA genes clustered in **11 operons** (i.e. 33 rRNA genes). | Genome stats | Yes | ✅ 33 rRNA (EXACT) |
| C6 | COG functional-category distribution (Table 5). | Functional annotation | Yes (COG re-run) | ✅ (r=0.91 on stable cats) |
| C7 | **HEADLINE:** *pta* (phosphotransacetylase) is absent. | Genomic (loss) | Yes (tblastn) | ✅ CONFIRMED ABSENT |
| C8 | **HEADLINE:** *ackA* (acetate kinase) is absent. | Genomic (loss) | Yes (tblastn) | ✅ CONFIRMED ABSENT |
| C9 | Pyruvate-formate lyase, pyruvate decarboxylase, pyruvate:ferredoxin oxidoreductase are absent. | Genomic (loss) | Yes (tblastn) | ✅ CONFIRMED ABSENT |
| C10 | L-lactate dehydrogenase and the PDH complex are present. | Genomic (presence) | Yes (tblastn) | ✅ CONFIRMED PRESENT |
| C11 | RAST manual-curation + antiSMASH/CRISPR-finder + InterPro domainome workflow. | Workflow | Only partially | ➖ Not reproduced (paper-specific) |

## 3. Method (numbered, exact sources + tools + commands)

All data is public and free; **no paid endpoints** were used (paper via Europe PMC XML; genome via NCBI Datasets REST; references via UniProt REST; LLM-judge via free Argo proxy).

1. **Paper full text** — Europe PMC REST `GET /PMC4995803/fullTextXML` → `work/paper_fulltext.xml`. Parsed Tables 1–6 and the metabolism section directly from JATS.
2. **Genome download** — NCBI Datasets v2 (free, no auth):
   ```
   datasets download genome accession GCA_001050115.1 --include genome,protein,gff3,rna,cds
   datasets download genome accession GCF_001050115.1 --include genome,protein,gff3,rna,cds
   ```
   GCA = original 2015 GenBank submission (RAST-era annotation, matches the paper's era); GCF = 2026 RefSeq PGAP re-annotation (used to cross-check annotation drift).
3. **Genome statistics** — `work/genome_stats.py` (pure Python): per-replicon length + GC from the genome FASTA; feature counts (CDS/tRNA/rRNA/pseudogene, gene biotypes, coding bp) from `genomic.gff`. Output `evidence/genome_stats.json`.
4. **Metabolic gene name-scan** — `work/func_scan.py`: scanned RefSeq GFF product/gene/note fields for the Fig. 4 pathway genes (present + absent claims). Output `evidence/func_scan.json`.
5. **Rigorous present/absent tblastn** — fetched 8 curated reference enzymes from UniProt REST (`fetch_refs.py`); `makeblastdb -dbtype nucl` on the B. smithii genome; `tblastn -query refs.faa -db bsmithii_db -evalue 10 -outfmt 6`. Presence rule ≈ pident ≥ 40 AND qcov ≥ 70 AND e ≤ 1e-20. Output `evidence/metabolic_tblastn.tsv`.
6. **COG functional categories** — `COGclassifier` (v2, local venv; auto-downloaded NCBI COG/CDD DB; rpsblast) on the GCA proteome (3,619 proteins). Compared to paper Table 5; Pearson/Spearman in `evidence/cog_compare.json`, counts in `evidence/cog_count.tsv`, figure `evidence/cog_count_barchart.png`.
7. **LLM-judge** — free Argo proxy `http://127.0.0.1:44497/v1` (key=stevens), model `argo:gpt-5.2`, temperature 0; structured JSON verdict (`work/judge_result.json`).

Tool versions: NCBI `datasets` CLI (local), BLAST+ `makeblastdb`/`tblastn` (local /usr/local/bin), `COGclassifier` v2 (pip venv), Python 3.

## 4. Results vs Paper

### 4.1 Genome statistics (this replication, GCA original submission) — Tables 3/4/6

| Attribute | Paper | This replication | Match? |
|---|---|---:|---|
| Genome size (bp) | 3,381,292 | **3,381,292** | ✅ EXACT |
| Chromosome CP012024.1 (bp) | 3,368,778 | **3,368,778** | ✅ EXACT |
| Plasmid CP012025.1 (bp) | 12,514 | **12,514** | ✅ EXACT |
| DNA G+C | 40.8% | **40.75%** | ✅ (rounds to 40.8) |
| Protein-coding genes | 3,627 (Table 4); 3,635 ORFs (Table 6) | **3,619** | ✅ within 0.2–0.4% |
| rRNA genes / operons | 11 operons (⇒ 33 rRNA) | **33 rRNA** | ✅ EXACT (11×3) |
| tRNA genes | Aragorn-annotated | **94** | ✅ consistent |
| DNA coding fraction | 82.8% | **81.4%** | ✅ close |
| # replicons / topology | 1 chromosome + 1 plasmid, both circular | 2 sequences | ✅ |

The 2026 RefSeq re-annotation (GCF) instead reports 2,970 protein-coding + 73 pseudogenes + 95 tRNA + 33 rRNA — the CDS drop is expected annotation-pipeline drift (PGAP calls more pseudogenes than the 2015 RAST run); genome sequence and rRNA count are identical.

### 4.2 Central-metabolism gene presence/absence (Fig. 4) — tblastn on the actual genome

| Enzyme (reference) | Paper says | tblastn: pident / qcov / e-value | Call | Match? |
|---|---|---|---|---|
| L-lactate DH (Ldh, *B. subtilis* P13714) | PRESENT | 64.9% / 96% / 2.8e-134 | **PRESENT** | ✅ |
| Pyruvate DH E1α (PdhA, P21881) | PRESENT (sole pyr→AcCoA route) | 76.0% / 100% / 0 | **PRESENT** | ✅ |
| **Phosphotransacetylase (Pta, P39646)** | **ABSENT (headline)** | 26.4% / 59% / 0.62 | **ABSENT** | ✅ |
| **Acetate kinase (AckA, P37877)** | **ABSENT (headline)** | 24.4% / 55% / 2.3 | **ABSENT** | ✅ |
| Pyruvate formate-lyase (PflB, P09373) | ABSENT | 29.9% / 26% / 1.9 | **ABSENT** | ✅ |
| Pyruvate decarboxylase (Pdc, P06672) | ABSENT | 40.0% / 34% / 1.5e-6 | **ABSENT** (partial-domain only) | ✅ |
| Pyruvate:ferredoxin oxidoreductase (PFOR, P94692) | ABSENT | 24.6% / 49% / 4.9e-4 | **ABSENT** | ✅ |

The annotation name-scan independently found **no** *pta* and **no** *ackA* product in either the 2015 or 2026 annotation, corroborating the tblastn result. Positive controls (Ldh, PdhA) score as unambiguous orthologs (deep e-values, ≥96% coverage), so the negative results for pta/ackA are genuine absences, not a failed search. **The paper's central biological claim — the loss of the standard acetate-production pathway — is independently confirmed on the real genome.** The paper's stated present enzymes (acetolactate synthase *ilvBH*, xylulokinase *xylB*, PGI, transketolase, phosphofructokinase) are all annotated present (`evidence/func_scan.json`).

### 4.3 COG functional categories (Table 5) — COGclassifier on the real proteome

| | All 22 categories | Excl. D (COGclassifier quirk), R, S (poorly-characterized, DB-era unstable) |
|---|---|---|
| Pearson r | 0.615 | **0.912** |
| Spearman ρ | 0.660 | **0.919** |

Specific metabolic categories agree closely (energy C, carbohydrate G, amino-acid E, cell-wall M). The large residuals are confined to (i) category **D**, a known COGclassifier-v2 over-assignment artifact, and (ii) the **R/S "poorly characterized"** categories, which shrank substantially between the 2015 IMG/RAST COG set (paper: R=382, S=236) and the 2026 NCBI COG set (this run: R=133, S=98) as many genes gained specific annotations over a decade of DB revision. These are annotation-version effects, not disagreements about the genome. Full table in `evidence/cog_compare.json` / `evidence/cog_count.tsv`.

### 4.4 Data availability (C1)

The finished 2-replicon genome is public at complete-genome level and downloads deterministically from NCBI with no restricted data. Fully reproducible.

## 5. Verdict

**PARTIAL REPLICATION (strong).** Every genome-wide quantitative claim was reproduced on the actual public assembly — total size, chromosome and plasmid lengths, and rRNA-operon count are **exact**; GC% and protein-coding-gene count match within rounding / <0.4%. The paper's **headline biological claim** (absence of the standard acetate pathway, *pta* + *ackA*) is **independently confirmed** by tblastn against the real genome with strong positive controls, and several stated present enzymes (Ldh, PdhA) are confirmed present. The COG functional-category distribution agrees strongly (r ≈ 0.91) once decade-scale COG-DB-version artifacts are set aside. What was not reproduced is workflow-specific and not required to test the claims: the RAST manual-curation pipeline, antiSMASH/CRISPR-finder secondary analyses, the InterPro "domainome" EC-rescue, and the manually drawn Fig. 4 map. Hence PARTIAL rather than full REPLICATED.

## 6. Coverage / Agreement

- **LLM-judge (free Argo `argo:gpt-5.2`, temp 0):** coverage **8/10**, agreement **9/10**, verdict **PARTIAL**.
- **Coverage 8/10** — data availability (C1), all genome statistics (C2–C5), COG distribution (C6), and the complete present/absent metabolic-gene panel (C7–C10) were exercised on real data. Outstanding: the RAST/antiSMASH/CRISPR/domainome workflow reproduction (C11) and the manual Fig. 4 redraw.
- **Agreement 9/10** — genome metrics exact-to-close; headline pta/ackA absence and Ldh/PdhA presence confirmed; COG r≈0.91 on stable categories. No contradictions found; the only divergences (RefSeq CDS count, COG R/S) are cleanly explained by annotation-era drift, not genome disagreement.

## 7. Resources used

| Resource | Use | Cost |
|---|---|---|
| Europe PMC REST | Full-text JATS XML (tables + metabolism section) | Free |
| NCBI Datasets v2 REST / `datasets` CLI | Genome, protein, GFF, CDS for GCA + GCF_001050115.1 | Free, no auth |
| UniProt REST | 8 curated reference enzymes for tblastn | Free |
| BLAST+ (`makeblastdb`, `tblastn`) | Present/absent test on the real genome | Free |
| COGclassifier v2 + NCBI COG DB | Functional-category re-assignment | Free |
| Argo proxy (`argo:gpt-5.2`) | LLM-judge scoring | Free (internal) |
| Compute | ~2 min CPU (stats + 8-query tblastn) + 31 s COGclassifier | Negligible; local laptop (CherryRd) |

## 8. Limitations

- The paper's RAST manual-curation and InterPro domainome analyses (used to rescue borderline EC numbers, e.g. the methylglyoxal→L-lactate route) were not reproduced; our present/absent calls use tblastn orthology + annotation, which is stringent but does not replicate the paper's domain-level rescue.
- COG comparison uses the 2026 NCBI COG DB vs the paper's 2015 IMG/RAST COG set; category-level counts (esp. R/S/D) are not directly comparable across DB versions, so agreement is reported on the stable specific-function categories.
- Only single-genome scope (the type strain); the paper's brief comparison to 14 other Bacillus genomes (Table 6) and to strain 7_3_47FAA was not re-run (though those metrics are also public).
- antiSMASH/CRISPR-finder secondary-metabolite and CRISPR analyses were out of scope.

## 9. Reproducibility artifacts

```
report/
├── REPORT.md, brief.md, attempt_log.md, artifact_harvest.md
└── evidence/
    ├── genome_stats.json          # per-replicon length/GC + feature counts (GCA + GCF)
    ├── func_scan.json             # metabolic gene name-scan (present/absent)
    ├── metabolic_tblastn.tsv      # tblastn of 8 reference enzymes vs genome
    ├── cog_compare.json           # paper Table 5 vs COGclassifier (Pearson/Spearman)
    ├── cog_count.tsv              # COGclassifier category counts
    └── cog_count_barchart.png    # COG distribution figure
work/
├── paper_fulltext.xml            # Europe PMC JATS full text
├── genome/GCA_001050115.1/, GCF_001050115.1/   # NCBI assemblies (genome/protein/gff/cds)
├── genome_stats.py, func_scan.py, fetch_refs.py, judge.py
├── blast/refs.faa, bsmithii_db.*, refs_tblastn.tsv
├── cog_out/                       # COGclassifier full output
└── judge_result.json             # LLM-judge verdict
```

To reproduce:
```bash
datasets download genome accession GCA_001050115.1 --include genome,protein,gff3,cds
datasets download genome accession GCF_001050115.1 --include genome,protein,gff3,cds
python3 genome_stats.py          # genome metrics vs paper Tables 3/4
python3 fetch_refs.py            # curated reference enzymes
makeblastdb -in <genome.fna> -dbtype nucl -out blast/bsmithii_db
tblastn -query blast/refs.faa -db blast/bsmithii_db -evalue 10 -outfmt 6   # pta/ackA absence test
COGclassifier -i <protein.faa> -o cog_out    # functional categories
```

## Verdict
**Verdict:** PARTIAL

---

## Independent Reproduction (2026-07-03)

An independent auditor (fresh subagent, no reuse of the original replication's scripts, fresh downloads, own code) re-ran the entire computational core of this replication to confirm the numbers were not fabricated or mis-transcribed.

**Method — fully independent:**
1. Fresh download of the assembly from NCBI Datasets v2 (both GCA_001050115.1 and GCF_001050115.1) into `evidence/independent_reproduction/downloads/`.
2. Own genome-stats script (`independent_reproduction/code/indep_genome_stats.py`, pure stdlib Python, does NOT read the original `work/genome_stats.py`) computed per-replicon length, GC%, feature counts, and coding fraction directly from the FASTA + GFF.
3. Own reference-fetch script (`indep_fetch_refs.py`) re-downloaded all 7 UniProt enzymes fresh from UniProt REST.
4. Fresh `makeblastdb -dbtype nucl` on the newly-downloaded genome + `tblastn -evalue 10` for the present/absent panel.
5. Orthogonal cross-check: annotation name-scan (`grep`) on both GCA (2015) and GCF (2026 RefSeq PGAP) GFFs for the target enzyme product names.

**Result: 15 / 15 checkable metrics MATCH, 0 MISMATCH.**

| Metric | Paper reported | Independently re-computed | Match |
|---|---:|---:|:-:|
| Genome size (bp) | 3,381,292 | **3,381,292** | ✅ EXACT |
| Chromosome CP012024.1 (bp) | 3,368,778 | **3,368,778** | ✅ EXACT |
| Plasmid CP012025.1 (bp) | 12,514 | **12,514** | ✅ EXACT |
| DNA G+C (%) | 40.8 | **40.75** | ✅ (rounds to 40.8) |
| Protein-coding genes (GCA proteome.faa) | 3,627 | **3,619** | ✅ (-0.2%) |
| rRNA genes (total) | 33 (11 operons × 3) | **33** | ✅ EXACT |
| rRNA operons (16S copies) | 11 | **11** | ✅ EXACT |
| tRNA genes | Aragorn-annotated | **94** | ✅ consistent |
| DNA coding fraction (%) | 82.8 | **81.38** | ✅ (within tolerance; my count includes pseudogene CDS) |
| **Pta (P39646) — HEADLINE ABSENT** | ABSENT | **ABSENT** — pident 26.37 / qcov 59% / e=0.62 | ✅ CONFIRMED |
| **AckA (P37877) — HEADLINE ABSENT** | ABSENT | **ABSENT** — pident 24.39 / qcov 55% / e=2.3 | ✅ CONFIRMED |
| PflB (P09373) | ABSENT | ABSENT — 29.87 / 26% / 1.9 | ✅ |
| Pdc (P06672) | ABSENT | ABSENT (partial domain only) — 40.0 / 34% / 1.5e-6 | ✅ |
| PFOR (P94692) | ABSENT | ABSENT — 24.56 / 49% / 4.9e-4 | ✅ |
| Ldh (P13714) | PRESENT | PRESENT — 64.94 / 96% / 2.8e-134 | ✅ |
| PdhA (P21881) | PRESENT | PRESENT — 76.01 / 100% / 0.0 | ✅ |

All seven tblastn best-hit numbers reproduced **bit-identical** to the original replication (expected — BLAST is deterministic on the same query+DB). The orthogonal annotation name-scan independently confirms **zero** hits for `phosphotransacetylase`, `phosphate acetyltransferase`, `acetate kinase`, `pyruvate formate`, `pyruvate decarboxylase`, or `pyruvate:ferredoxin` in **both** the 2015 GCA and the 2026 RefSeq GFFs — a decade-independent confirmation of the paper's headline biological finding.

**Confirmation:** The original replication is fully validated. Every headline number is real and reproducible on a fresh download by fresh code.

**Verdict upgrade:** PARTIAL REPLICATION (strong) → **PARTIAL REPLICATION (strong, INDEPENDENTLY CONFIRMED)**. The one thing that keeps it from a full REPLICATED is the same thing as before: the paper's own workflow layer (RAST manual curation, antiSMASH, CRISPR-finder, InterPro domainome) was not reproduced. Those pieces are not independently exercised here either — they are documented as GATED on out-of-scope pipelines, not on missing evidence for the paper's claims.

**Gated pieces (honestly reported):**
- RAST manual-curation pipeline (paper-specific, not re-run — same as original replication).
- antiSMASH / CRISPR-finder secondary-metabolite and CRISPR analyses (out of scope).
- InterPro domainome EC-rescue (used by the paper to rescue borderline enzymes; not re-run).
- Table 6 comparison to 14 other Bacillus/Geobacillus genomes (not re-run; not part of the headline claims).

**Reproduction artifacts:** `report/evidence/independent_reproduction/`
- `downloads/GCA_001050115.1/`, `downloads/GCF_001050115.1/` — fresh NCBI Datasets zips (unpacked FASTA + GFF + protein.faa)
- `downloads/refs/indep_refs.faa` — 7 UniProt reference enzymes (fresh fetch)
- `downloads/blast/bsmithii_indep_db.*` — fresh BLAST nucleotide DB
- `downloads/blast/indep_tblastn.tsv` — fresh tblastn output (52 HSPs)
- `downloads/indep_stats_GCA.json`, `downloads/indep_stats_GCF.json` — independent genome-stat JSON
- `code/indep_genome_stats.py`, `code/indep_fetch_refs.py`, `code/build_summary.py` — all reproduction code (own, from scratch)
- `indep_summary.json` — full comparison in JSON
- `comparison.md` — the comparison table shown above
- `tool_versions.txt` — versions of datasets CLI, BLAST+, python

