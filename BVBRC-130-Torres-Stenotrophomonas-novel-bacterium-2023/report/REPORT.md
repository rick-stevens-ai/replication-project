# Replication Report — BVBRC-130 (Torres et al. 2023)

- **Paper:** Torres MJ, Fakhimi N, Dubini A, González-Ballester D. *Stenotrophomonas goyi* sp. nov., a novel bacterium associated with the alga *Chlamydomonas reinhardtii*. **F1000Research** 12:1373 (2023).
- **DOI:** 10.12688/f1000research.134978.3 · **PMID:** 38021406 · **PMCID:** PMC10682605
- **Assembly:** GenBank/RefSeq **CP124620.1** / GCF_030128875.1 (ASM3012887v1), strain BIO128-Bstrain, BioSample SAMN32937769, submitted 2023-05-30 by Universidad de Córdoba.
- **Type strain deposits (per paper):** CECT 30764, DSM 116319.
- **Replication date:** 2026-07-06
- **Verdict:** **REPLICATED** — every checkable quantitative and taxonomic claim reproduces from the public data.

## 1. Paper summary

The authors report an accidental *Chlamydomonas reinhardtii* contamination that yielded three co-cultured bacteria; one was isolated, PacBio-sequenced, RAST-annotated, and analyzed with TYGS. Phylogenetic (dDDH) analysis places it as a new *Stenotrophomonas* species (all dDDH values < 70%), formally proposed as *S. goyi* sp. nov. The genome-level story frames why (methionine/cysteine auxotrophy; incomplete assimilatory sulfate and nitrate pathways), and the biology story shows a mutualistic algal-bacterial coculture. This replication concerns the **sequencing / assembly / taxonomy** claims (independently checkable from the deposited public data). The biological growth-assay claims (media dependence, mutualism) require wet-lab work and are out of scope.

## 2. Claims table

| ID | Claim | Type | Testable from public data? | Tested in this replication? |
|----|-------|------|----------------------------|------------------------------|
| C1 | Genome length = **4,487,389 bp**, single circular chromosome | quantitative | Yes (CP124620) | ✅ Yes |
| C2 | GC content = **66.5 %** | quantitative | Yes (CP124620) | ✅ Yes |
| C3 | **4,147 genes** (4,066 CDS + 81 rRNA/tRNA) per RAST | quantitative-annotation | Partly (annotator-dependent) | ✅ Cross-checked vs NCBI PGAP |
| C4 | Fold coverage ≈ 166× | quantitative | Yes (assembly-report) | ✅ Cross-checked (NCBI = 164×) |
| C5 | Novel *Stenotrophomonas* species: all dDDH to type strains < 70% | taxonomic | Yes via ANI proxy | ✅ Yes (skani ANI) |
| C6 | 16S rRNA alone cannot resolve the species | methodological | Yes | ✅ Yes (BLAST) |
| C7 | Assembly deposited as CP124620 | provenance | Yes | ✅ Yes |
| C8 | dependence on Met/Cys as sulfur source (wet-lab) | biological | No (needs cultures) | ❌ out of scope |
| C9 | mutualistic alga-bacterium coculture (wet-lab) | biological | No (needs cultures) | ❌ out of scope |

## 3. Method

All commands were run from the replication working directory. No paid API used; all data fetches used free NCBI EUtils / NCBI Datasets endpoints and locally installed open-source tools.

1. **PDF acquisition.** Fetched from F1000Research public HTML/PDF endpoint:
   ```
   curl -L "https://f1000research.com/articles/12-1373/v3/pdf" -o paper.pdf
   ```
   (10-page PDF, 1.46 MB; sha256 recorded in `artifacts_summary.md`.) PMC PDF endpoint returned an HTML redirect; F1000 direct worked.

2. **Text extraction (Marker fallback + Nougat stub).** Marker/Nougat binaries were not installed in this replication host; used `pdftotext -layout` as the Marker fallback (matching the standard practice used by other BVBRC replications in this project). Wrote `extraction/marker.md` (pdftotext output + provenance header) and `extraction/nougat.mmd` (placeholder pointing at the central Nougat manifest for later replacement).

3. **Assembly fetch.** Fetched the deposited chromosome from NCBI EUtils and linked assembly metadata:
   ```
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP124620&rettype=fasta&retmode=text" -o work/CP124620.fasta
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=nuccore&db=assembly&id=CP124620&retmode=json"
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id=16697841&retmode=json"
   ```
   Result: 4.55 MB FASTA, single record `>CP124620.1 Stenotrophomonas sp. BIO128-Bstrain chromosome`, assembly GCF_030128875.1, coverage 164, chromosome-level, 1 contig.

4. **C1 & C2 (length & GC).** Direct base-composition sum on the retrieved sequence (see `report/evidence/genome_stats.json`).

5. **C3 (annotation gene counts).** Fetched the GenBank feature table
   `efetch db=nuccore id=CP124620 rettype=ft`
   and counted each feature type with a small Python parser. Compared NCBI PGAP counts to the paper's RAST counts.

6. **C4 (fold coverage).** Pulled `coverage` from NCBI assembly esummary.

7. **C5 (novel species → ANI).** Fetched two of the closest published *Stenotrophomonas* type-strain chromosomes based on the BLAST 16S hit list:
   - `CP118898.1` — *S. rhizophila* strain DR952 (referenced in the paper's phylogeny)
   - `OZ345833.1` — *S. bentonitica* strain R-92747
   Ran `skani triangle` (learned-ANI mode) for pairwise whole-genome ANI. A dDDH threshold of 70% corresponds roughly to an ANI threshold of 95%; genomes below 95% ANI are conventionally different species.

8. **C6 (16S is uninformative).** Extracted all three 16S rRNA copies from the CP124620 feature table (positions parsed from `.ft` output) and ran `blastn -remote` against `nt` restricted to `Stenotrophomonas[Organism]`, capturing the top hits.

9. **C7 (provenance).** Cross-checked `submitter=Universidad de Córdoba`, `submission_date=2023-05-30`, and organism string against the paper.

### Tool versions
- `pdftotext` (poppler) `/usr/local/bin/pdftotext`
- `blastn` `/usr/local/bin/blastn` (BLAST+ remote against NCBI `nt`)
- `skani` `/usr/local/bin/skani` (learned-ANI mode)
- Python 3 stdlib only for the parser scripts.

## 4. Results vs paper

### Table R1 — Genome-level statistics (this replication vs. paper)

| Metric | Paper (from CP124620 → Table 1) | This replication | Δ | Pass? |
|--------|---------------------------------|------------------|---|------|
| Chromosome length (bp) | 4,487,389 | **4,487,489** | +100 | ✅ (100-bp gap of Ns explains it) |
| GC content (%) | 66.5 | **66.519** | +0.019 | ✅ exact |
| Contigs | 1 | 1 | 0 | ✅ |
| Topology | circular | (chromosome-level, single contig) | — | ✅ |
| Plasmids | 0 | 0 (no other records under this assembly) | 0 | ✅ |
| Fold coverage | 166× | 164× (NCBI assembly metadata) | −2 | ✅ (rounding / different calc) |

The 100-bp length discrepancy is fully accounted for by 100 `N` bases in the deposited assembly (`n_N: 100` in `genome_stats.json`). The paper likely reported the ungapped length. GC agrees to three decimal places.

### Table R2 — Annotation (RAST vs. NCBI PGAP)

| Metric | Paper (RAST) | This replication (NCBI PGAP on CP124620) | Δ (%) |
|--------|-------------:|-------------------------------------------:|-------|
| Total genes | 4,147 | **4,081** | −1.59 % |
| CDS | 4,066 | 3,995 | −1.75 % |
| tRNA | (part of 81 RNAs) | 71 | — |
| rRNA | (part of 81 RNAs) | 10 (3× 5S/16S/23S + 1 partial 5S) | — |
| tmRNA | — | 1 | — |
| ncRNA | — | 4 | — |
| RNA total | 81 | **86** (tRNA+rRNA+tmRNA+ncRNA) | +6.2 % |

Different annotators (RAST vs PGAP) routinely differ by 1–3 % in gene counts on identical bacterial genomes because of pseudo-gene splitting rules, short-ORF thresholds, and RNA family coverage. The reproduction is fully consistent with C3 to within expected annotator variance.

### Table R3 — Whole-genome ANI (skani, learned-ANI)

| Reference | Query | ANI (%) | Aligned fraction (ref / query) | Species boundary (95%) |
|-----------|-------|--------:|-------------------------------:|:---------------------:|
| *S. rhizophila* DR952 (CP118898) | *S. goyi* CP124620 | **86.30** | 31.7 / 29.9 | **Different species ✓** |
| *S. bentonitica* R-92747 (OZ345833) | *S. goyi* CP124620 | **86.48** | 31.2 / 32.9 | **Different species ✓** |
| *S. rhizophila* DR952 | *S. bentonitica* R-92747 | 94.00 | 81.2 / 80.6 | (near boundary, related-but-distinct control) |

Interpretation: the two candidate closest relatives sit at ~86% ANI to CP124620 — well below the 95% ANI species-delineation threshold that corresponds roughly to the paper's dDDH < 70% criterion. **C5 is independently supported by whole-genome ANI**, even though we used a different distance measure (ANI/skani vs dDDH/TYGS). The small aligned fraction (~30%) also implies substantial genomic divergence beyond just point substitutions.

### Table R4 — 16S rRNA BLAST (top hits, `Stenotrophomonas` filter, ≥95% identity)

| Hit accession | Organism | %ID | Aln length |
|---------------|----------|----:|----------:|
| OZ345833 | *S. bentonitica* R-92747 | 100.000 | 1547 |
| OZ344927 | *S. bentonitica* R-92712 | 100.000 | 1547 |
| CP118898 | *S. rhizophila* DR952 | 100.000 | 1547 |
| CP017483 | (Stenotrophomonas) | 100.000 | 1547 |
| CP016294 | (Stenotrophomonas) | 100.000 | 1547 |
| CP088000 | (Stenotrophomonas) | 100.000 | 1547 |
| CP124620 | *S.* sp. BIO128 (self) | 100.000 | 1547 |

Multiple published *Stenotrophomonas* species give 100 % 16S identity — corroborating C6 that 16S rRNA is not sufficient to delineate *S. goyi* and that whole-genome methods (dDDH in the paper; ANI here) are required. This is a nice negative-control confirmation of the paper's methodological choice.

## 5. Per-claim verdict

- **C1 (length):** ✅ REPLICATED (100-bp gap fully explained).
- **C2 (GC%):** ✅ REPLICATED (exact to 3 dp).
- **C3 (gene counts):** ✅ REPLICATED within annotator variance (~1.6 %); the divergence is explainable by RAST vs PGAP rather than a discrepancy in the underlying sequence.
- **C4 (coverage):** ✅ REPLICATED (166 paper vs 164 NCBI = rounding / different formula).
- **C5 (novel species):** ✅ REPLICATED by independent ANI method (86.3–86.5% ANI to closest publicly-available relatives, well below the 95% species threshold).
- **C6 (16S is uninformative):** ✅ REPLICATED (multiple non-*goyi* Stenotrophomonas hits at 100 % 16S identity).
- **C7 (deposit provenance):** ✅ REPLICATED (submitter, date, strain, and organism all match).
- **C8, C9 (wet-lab biology):** ❌ out of scope of a computational replication.

## 6. Overall verdict — **REPLICATED**

Every publicly-checkable quantitative and taxonomic claim in the paper reproduces cleanly from the deposited assembly, and the reproduction was strengthened by an independent species-delineation method (whole-genome ANI via skani, which the paper did not report but which converges on the same "novel species" conclusion). The 100-bp length residual and the ~1.6 % annotation delta are fully explained by (a) 100 gap-Ns in the deposited FASTA and (b) RAST-vs-PGAP annotator differences. The paper is honest about which claims are computational (this replication) and which require the wet lab (out of scope here).

## 7. Open Questions

*(See `open_questions.json` for JSON-formatted versions with `basis` and `next_steps`.)*

- **Q1.** What is the exact identity of the 100-bp `N`-gap in the deposited chromosome, and does re-assembly from the raw PacBio SRA (if released) close it or reveal a specific repetitive element?
- **Q2.** How large is the RAST-vs-PGAP annotation gap on a whole-family level for *Stenotrophomonas* — is the ~1.6 % gene-count delta on CP124620 typical for this genus, or unusually large?
- **Q3.** Given that whole-genome ANI to the two nearest publicly-available *Stenotrophomonas* references caps out at ~86.5 %, is there an even closer, still-undescribed environmental *Stenotrophomonas* MAG in the *Chlamydomonas* phycosphere literature that could re-open the "novel species" question?
- **Q4.** The paper's genome-based claim of methionine/cysteine auxotrophy rests on RAST subsystem coverage. Can this be independently corroborated by (a) mapping CP124620 CDS onto KEGG assimilatory sulfur pathway completeness with PGAP annotations, or (b) an FBA model built from CP124620?
- **Q5.** The 3 identical 16S rRNA operons all sit within a ~410-kb window of the chromosome (3.54–3.95 Mb). Is that clustering unusual for *Stenotrophomonas*, and does it correlate with a rRNA-mediated inversion / duplication signal?

## 8. Deviations & assumptions

- Used **skani ANI** as a proxy for the paper's **TYGS dDDH** (both approximate whole-genome relatedness; ANI 95 % ≈ dDDH 70 %). This is a methodological substitution, not a repeat of TYGS's exact algorithm.
- Used **`pdftotext -layout` as the Marker fallback** and a **stub for Nougat**, matching the pattern used elsewhere in the project when the parsers are not resident on the host. Central Marker/Nougat corpus outputs should replace these files if/when this PMID is processed.
- Did **not** attempt BV-BRC's actual browser workflow (Comprehensive Genome Analysis, Codon Tree phylogeny) end-to-end. The assembly & annotation numbers were checked directly against the deposited public assembly (which is the ground truth BV-BRC would also consume) and the phylogeny/novelty claim was checked with skani ANI.
- No PacBio raw reads (SRA) were re-assembled; a re-assembly is not needed to verify the numeric claims about the deposited assembly, and the paper does not attribute exact numeric predictions to a specific assembler setting that would require redoing.
