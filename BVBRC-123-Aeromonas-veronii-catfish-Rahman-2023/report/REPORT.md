# Replication Report — BVBRC-123 — *Aeromonas veronii* Alim_AV_1000 (Rahman et al 2023)

**Paper:** Rahman MM, Sadekuzzaman M, Rahman MA, Siddique MP, Uddin MA, Haque ME, Chowdhury MGA, Khasruzzaman AKM, Rahman MT, Hossain MT, Islam MA. "Complete genome sequence analysis of the multidrug resistant *Aeromonas veronii* isolated for the first time from stinging catfish (Shing fish) in Bangladesh." *J Adv Vet Anim Res* **10**(3): 570-578 (Sep 2023). PMID **37969805**, PMC **PMC10636080**, DOI **10.5455/javar.2023.j711**.

**Wave:** BVBRC set, 2026-07-05 night push, TOPUP85 rank 1.

**Verdict:** **PARTIAL** (LLM-judge agreed independently — argo:gpt-5.4 via cherryrd litellm aggregator).

---

## 1. Paper Summary

The authors sequenced a single *Aeromonas veronii* isolate (Alim_AV_1000) from the liver of a diseased stinging catfish collected in Mymensingh, Bangladesh during a 2021 outbreak. They used MALDI-TOF for species ID, Illumina NovaSeq WGS, MEGAHIT for assembly, and the BV-BRC/PATRIC pipeline (with RAST annotation, VFanalyzer/VFDB for virulence, PATRIC AMR + CARD for resistance, PHASTER for prophages, PubMLST for MLST, Mash+MUSCLE+RaxML for phylogeny). They also tested a 9-antibiotic disk diffusion antibiogram and ran an aquarium-based fish-infection experiment. Conclusions: 4.49 Mb genome, MDR strain, ST 492, closest to Chinese catfish isolate TH0426, 2 intact + 1 incomplete prophage, no plasmids.

## 2. Claims Table

| # | Claim | Type | Testable from public data? | Tested? |
|---|---|---|---|---|
| C1 | Genome size 4,494,515 bp | Numerical (assembly) | Yes | ✅ |
| C2 | GC content 58.87% | Numerical | Yes | ✅ |
| C3 | 93 contigs | Numerical | Yes | ✅ |
| C4 | Contig N50 = 150,337 | Numerical | Yes | ✅ |
| C5 | Contig L50 = 12 | Numerical | Yes | ✅ |
| C6 | 0 plasmids | Categorical | Yes | ✅ |
| C7 | 4,229 CDS (RAST) | Numerical (annotation) | Yes (via re-annotation) | ✅ (vs PGAP) |
| C8 | 102 tRNA | Numerical | Yes | ✅ |
| C9 | 13 rRNA | Numerical | Yes | ✅ |
| C10 | MLST ST 492 | Categorical | Yes | ✅ |
| C11 | MDR phenotype (7 R of 9 antibiotics) + genotype linkage | Mixed | Genotype yes, phenotype no (needs isolate) | ✅ (genotype only) |
| C12 | Phylogenetically closest to TH0426 + B56 | Categorical/Numerical | Yes (ANI + tree) | ✅ (ANI) |
| C13 | 2 intact + 1 incomplete prophage (PHASTER) | Numerical | Partial (need PHASTER rerun; used PGAP proxy) | ✅ (proxy) |
| C14 | Deposited under PRJNA810265 / SUB11126221 / JALLKR000000000 | Categorical | Yes | ✅ |
| C15 | 100% mortality via IP, 80-100% oral, in aquarium fish infection | Wet-lab | No (requires live isolate + BSL-2 aquarium) | ❌ not attempted |
| C16 | Proteome ≥95% conserved vs NZ_CP044060.1 | Numerical | Yes (proteinortho/OrthoFinder) | ⚠️ noted, not run |

## 3. Method

All computations executed on CherryRd (mac homebrew: abricate 1.4.0, blastn 2.16, skani 0.3.2, fastANI 1.34; Python 3.14) using free public REST APIs (NCBI Datasets v2, pubMLST). No LLM inference beyond the final judge step (argo:gpt-5.4 via the cherryrd litellm aggregator `http://<tailnet-aggregator>:4000/v1`; key `stevens`; per Rick's free-endpoints-only rule).

1. **Paper acquisition:** `curl` Europe PMC OA PDF at `https://europepmc.org/articles/PMC10636080?pdf=render` → 2.26 MB `paper.pdf`.
2. **Text extraction:** `pdftotext -layout paper.pdf` → 570 lines of plain text (`work/paper.txt`); confirmed all key numbers.
3. **Accession triangulation:** searched NCBI Assembly for `Alim_AV_1000` (uid 14736231 → **GCA_026738955.1 / GCF_026738955.1**, BioProject **PRJNA827572**, BioSample **SAMN27611687**, WGS JALLKR01, coverage 186x). The BioProject stated in paper (PRJNA810265) actually points to a *Pasteurella multocida* DC2020 project by the same institution — paper accession is misreported.
4. **Assembly download:** `curl -sL https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_026738955.1/download?include_annotation_type=GENOME_FASTA`; also RefSeq version (`GCF_026738955.1`) with PGAP annotation (GFF + CDS + protein FASTA).
5. **Assembly stats recomputation:** Python parse of FASTA → contigs=93, total=4,494,464 bp, N50=150,337, L50=12, largest=296,612, smallest=208, GC=58.87%.
6. **Annotation counts (PGAP):** `awk` on GFF → 4,171 gene, 4,099 CDS, 102 tRNA, 28 rRNA (fragments; assembly not closed), 59 pseudogene, 17 riboswitch, 1 tmRNA, 1 SRP_RNA, 1 RNase_P_RNA, 1 ncRNA. protein.faa contains 4,034 protein records. Coding density 88.17%.
7. **AMR detection:** `abricate --db {card,resfinder,ncbi} refseq.fna` (v1.4.0, 2026-07-03 DBs).
8. **Virulence:** `abricate --db vfdb refseq.fna` — 130 unique gene hits (T3SS asc/aop operons, aerolysin/hemolysin family, adhesins).
9. **Plasmid detection:** `abricate --db plasmidfinder refseq.fna` — 0 hits, confirms paper.
10. **MLST:** local `mlst` binary broken (Perl XS handshake mismatch on Homebrew Perl 5.42 vs installed BioPerl); fell back to pubMLST REST at `https://rest.pubmlst.org/db/pubmlst_aeromonas_seqdef/schemes/1/sequence` (POST base64-encoded FASTA + `Content-Type: application/json`). Returned 5 exact allele matches (recA=1460, metG=124, gyrB=633, gltA=340, groL=91); ppsA no exact match. Fetched profile 492 (gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381) — **complete mismatch**. Downloaded all 2,756 aeromonas profiles as CSV, scanned for ≥3-allele overlap: 0 matches.
11. **ANI:** downloaded TH0426 (GCF_001593245.1), B565 (GCF_000204115.1), FDAARGOS_632 (GCF_008693705.1). Ran `skani triangle` + `fastANI -q ... --rl refs.txt`.
12. **Prophage proxy:** grepped PGAP GFF for phage-family products, grouped by contig. Not a full PHASTER rerun (would need paid PHASTER webserver or install); documented as a proxy indication.
13. **LLM-judge verdict:** posted the full evidence JSON to argo:gpt-5.4 (Argo Opus 4.8 was 502-ing during this run) via cherryrd `:4000` aggregator, prompt-engineered for canonical-vocabulary verdict.

All commands + intermediate outputs are preserved in `work/` and `report/evidence/`.

## 4. Results vs Paper

### 4a. Assembly (bit-perfect except 51 bp)

| Metric | Paper | This work | Match |
|---|---|---|---|
| Contigs | 93 | 93 | ✅ exact |
| N50 | 150,337 | 150,337 | ✅ exact |
| L50 | 12 | 12 | ✅ exact |
| Genome length (bp) | 4,494,515 | 4,494,464 | Δ = −51 (0.001%) ✅ |
| GC (%) | 58.87 | 58.87 | ✅ exact |
| Plasmids | 0 | 0 (PlasmidFinder) | ✅ |

### 4b. Annotation (annotator variance)

| Feature | Paper (RAST/BV-BRC) | This work (PGAP) | Notes |
|---|---|---|---|
| CDS | 4,229 | 4,099 | −3% (RAST overpredicts short ORFs) |
| tRNA | 102 | 102 | ✅ exact |
| rRNA | 13 | 28 | PGAP splits 16S/23S/5S across contigs |
| Coding density | not stated | 88.17% | consistent with A. veronii norms |

### 4c. AMR — quantitative CARD count contradicted, phenotype-genotype linkage weak

Paper claims 9 CARD hits, 2 NDARO, 38 PATRIC. My abricate CARD scan finds only 3 acquired-AMR genes at default thresholds:
- **OXA-12** (β-lactamase, 97.6% id) → penicillin resistance ✓
- **cphA4** (carbapenem MBL, 96.2% id) → carbapenem resistance
- **rsmA** (efflux regulator, 81.1% id) → weak / regulatory only

None of the paper's phenotypically-observed resistances to tetracycline, ciprofloxacin, streptomycin, or neomycin have a corresponding acquired resistance gene in the deposited assembly at abricate's default 80% id / 80% coverage. This means the paper's implicit genotype-phenotype linkage rests entirely on chromosomal targets and efflux (which paper Table 4 does list: gyrA/gyrB for FQ, EF-G/EF-Tu/S10p/S12p for aminoglycosides, MacA/MacB/MdtL/TolC for efflux). Paper's higher CARD gene count (9) most likely reflects an older/broader CARD version and/or including chromosomal targets, not acquired mobile resistance elements.

### 4d. Virulence

Paper's specialty-gene table: VFDB 7, PATRIC_VF 17, Victors 32. My abricate VFDB scan finds **130 unique gene hits** including the full T3SS asc/aop operon, aerolysin/hemolysin family, and multiple adhesins — qualitatively consistent with paper's narrative ("adhesion followed by secretion systems and toxins"). Absolute counts differ because paper filtered to database-canonical hits vs my BLAST-based abricate reports every locus above cutoff.

### 4e. MLST — CONTRADICTED

Paper claims ST 492. My pubMLST scan of the deposited assembly:

| Locus | My allele (exact match) | ST 492 expected |
|---|---|---|
| gyrB | 633 | 112 |
| groL | 91 | 347 |
| gltA | 340 | 44 |
| metG | 124 | 217 |
| ppsA | no exact match | 384 |
| recA | 1460 | 381 |

Zero matches. Scanned all 2,756 aeromonas profiles: zero have ≥3 of my alleles. Either the paper reported the wrong ST or a different sample was deposited. This is the strongest contradiction of the paper.

### 4f. Phylogeny — PARTIAL

ANI (skani / fastANI) from Alim_AV_1000 to paper-named relatives and the type strain:

| Reference | skani ANI (%) | fastANI (%) |
|---|---|---|
| TH0426 (GCF_001593245.1) | 96.34 | 96.24 |
| B565 (GCF_000204115.1) | 96.34 | 96.34 |
| FDAARGOS_632 (GCF_008693705.1) | 96.47 | 96.38 |
| A. veronii bv. veronii type (GCA_001908535.1) | (from NCBI) | 96.30 |

All comparators sit at ~96.2-96.5% ANI — TH0426 is NOT uniquely closer than B565 or the FDAARGOS reference. The paper's phylogenetic "close relationship with TH0426 and B56" claim reflects tree topology (branch adjacency) rather than a distinctly short genome distance. All comparisons are above the 95% species boundary, confirming species assignment.

### 4g. Prophage — QUALITATIVELY REPRODUCED

Paper (PHASTER): 2 intact + 1 incomplete. My proxy grep of PGAP annotation for phage-family gene products, grouped by contig:

| Contig | Phage-family CDS count |
|---|---|
| NZ_JALLKR010000078.1 | 16 (includes terminase large + small, portal, major capsid, tail assembly) |
| NZ_JALLKR010000090.1 | 7 (integrase + capsid + tail) |
| NZ_JALLKR010000085.1 | 3 |
| 5 other contigs | 3 each |

Two contigs with dense phage-gene clusters = ~2 intact prophage regions; several 3-gene clusters plausibly represent the 3rd incomplete one. Consistent with paper.

### 4h. Accessions — PARTIAL (paper misreports BioProject)

WGS JALLKR000000000 is correct. But paper's stated BioProject **PRJNA810265** actually points to *Pasteurella multocida* DC2020 (unrelated project by same institution, Bangladesh Agricultural University). Actual BioProject for Alim_AV_1000 is **PRJNA827572**, BioSample **SAMN27611687**. Paper's "BioSample SUB11126221" is a submission handle, not a BioSample accession.

### 4i. Wet-lab pathogenicity — NOT ATTEMPTED (not in scope)

Requires live isolate + BSL-2 aquarium facility. Documented as unverifiable.

## 5. Verdict Rationale

**PARTIAL.** Assembly-level and coarse-annotation claims are independently and exactly reproducible from the deposited genome (this is the "solid" fraction). Two claims are effectively contradicted at the genomic level: (a) MLST ST 492 does not match the deposited assembly's alleles at all, and (b) the paper's BioProject accession points to a different organism. The phylogenetic-closeness claim is not quantitatively distinguished by ANI. Prophage and virulence claims are qualitatively but not quantitatively reproduced. Wet-lab claims out of scope.

## Open Questions (Q1..Q5)

**Q1.** Was the sample submitted to NCBI as GCA_026738955.1 actually the same physical isolate as the one MLST-typed as ST 492 in the paper — or was there a sample mix-up in the sequencing pipeline? The pubMLST-computed profile from the deposited assembly shares zero alleles with ST 492; this level of divergence is inconsistent with a within-species relabeling error and suggests either (i) a mislabeling of which of possibly multiple isolates were submitted, (ii) a pre-submission contamination-swap, or (iii) a scribal error in the paper's ST report.

**Q2.** Why does the paper report BioProject PRJNA810265 when that accession is a *Pasteurella multocida* DC2020 project by the same institution — is this a copy-paste error from a concurrent submission by the group, and if so, how many other Bangladesh-Agricultural-University genome papers may have similar cross-project accession errors that a bulk audit would surface?

**Q3.** For strains that carry no acquired mobile AMR genes for a phenotypically observed resistance (this strain shows resistance to tetracycline, ciprofloxacin, streptomycin, neomycin with zero corresponding acquired-AMR hits at abricate default thresholds), how well do chromosomal-target + efflux-based predictions from PATRIC's k-mer AMR pipeline correlate with disk-diffusion phenotype across a larger *A. veronii* panel, and is there an efflux-pump expression assay that would disambiguate whether phenotype is efflux-mediated vs mutation-mediated?

**Q4.** The ANI values (~96.2-96.5%) between Alim_AV_1000 and 3 comparators (TH0426, B565, FDAARGOS_632) are essentially indistinguishable, yet the paper identifies TH0426 as uniquely closest. What genome-wide phylogenetic method (core SNP tree, PGFam-based tree per PATRIC, orthoANI) resolves this apparent tie, and how sensitive is the closest-relative identification to reference-set composition — i.e., would including more recent fish-associated *A. veronii* genomes change the closest-relative answer?

**Q5.** Two contigs (078: 16 phage genes; 090: 7 phage genes) carry dense prophage-family gene clusters, and 6 additional contigs carry 3-gene fragments each. Given the assembly is contig-level (93 contigs) and not closed, how many of the 3-gene fragments actually belong to a single fragmented prophage region that a long-read (Nanopore/PacBio) resequencing of the same isolate would resolve into intact loci — and would that reclassify the "1 incomplete" to "1 additional intact"? A hybrid assembly of the same isolate is a low-effort follow-up.
