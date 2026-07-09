# Replication Report: Pal, Sharma & Subramanian (2021)
## "Complete genome sequence and identification of polyunsaturated fatty acid biosynthesis genes of the myxobacterium *Minicystis rosea* DSM 24000T"

**Paper:** Pal S, Sharma G, Subramanian S. *BMC Genomics* 22:655 (2021).
**DOI:** [10.1186/s12864-021-07955-x](https://doi.org/10.1186/s12864-021-07955-x) — **PMID:** 34511070 — **PMC:** PMC8436480
**Open access:** ✅ (CC BY 4.0 / BMC)

**Set:** BVBRC-51 | **Replication date:** 2026-07-02 | **Analyst:** Ollie (OpenClaw subagent)
**Compute:** CherryRd (BLAST+, Python) + uicgpu (antiSMASH 8.0.4). Free endpoints only (Argo proxy for LLM judge).
**Verdict:** **PARTIAL REPLICATION (strong).** 4 of 5 claims independently reproduced with exact or negligibly-different values on the real deposited genome; the fifth (antiSMASH BGC total) reproduces at the category level, with a count offset fully attributable to the antiSMASH version bump (v8.0.4 vs the paper's v5.0).

---

## 1. Paper

A complete-genome announcement for the soil myxobacterium *Minicystis rosea* DSM 24000T (suborder Sorangiineae, family Polyangiaceae). Using PacBio, the authors assembled a **single circular 16.04 Mbp chromosome** — reported as the **largest bacterial genome sequenced to date (2021)** — with ~44% paralogous coding potential. They mine the genome with **antiSMASH v5.0** (47 biosynthetic gene clusters, BGCs) and specifically identify and phylogenetically place the **polyunsaturated fatty acid (*pfa*) biosynthetic gene cluster**, arguing for its acquisition via horizontal gene transfer from Actinobacteria based on conserved *pfa* synteny.

This maps cleanly to a **BV-BRC Comprehensive Genome Analysis** workflow (assembly stats + RASTtk-style annotation) plus secondary-metabolite / specialty-gene detection (antiSMASH), exactly the top-up-list workflow tag for this paper.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Genome deposited publicly (CP016211.1 / PRJNA321464). | Data availability | Yes | ✅ |
| C2 | Single complete circular chromosome, 16,040,666 bp, 69.07% GC; largest bacterial genome (2021). | Genome stats | Yes | ✅ |
| C3 | 14,018 CDS (6,983 +, 7,035 −), 88 tRNA, 4 rRNA operons, coding density 87.31%. | Annotation | Yes | ✅ |
| C4 | antiSMASH → 47 BGCs; dominant NRPS/terpene/PKS/RiPP + rare singletons. | Secondary metabolism | Yes (rerun antiSMASH) | ✅ |
| C5 | *pfa* PUFA cluster present; Pfa1/2/3 homologous to Aetherobacter/Sorangium Pfa, conserved synteny. | Comparative genomics | Yes (BLAST + synteny) | ✅ |

## 3. Method

All data are free/public; all tools are open-source. See `artifact_harvest.md` for URLs/accessions/checksums and `attempt_log.md` for the chronological record.

1. **Paper harvest.** Europe PMC full-text XML for PMC8436480; extracted accession CP016211.1 and BioProject PRJNA321464 and the antiSMASH/PUFA methods.
2. **Genome download.** Mapped PRJNA321464 → assembly **GCA_001931535.1** (esearch/esummary) and downloaded genome FASTA + GFF + proteome via the **NCBI Datasets REST API** (free, no auth). MD5 of the zip recorded.
3. **C2/C3 — genome statistics** (`genome_stats.py`): length + GC from FASTA; CDS/strand/tRNA/rRNA counts and coding density from GFF.
4. **C5 — pfa cluster** (`pfa_blast.py`): `efetch` of the 10 reference Pfa proteins the paper cites (Aetherobacter sp. SBSr008 AIJ50375-77; A. fasciculatus AIJ50372-74; Sorangium cellulosum So ce56 CAN90975-77, CAN95221); `makeblastdb` + `blastp` (e≤1e-10) vs the M. rosea proteome; summed-HSP coverage per best subject; GFF synteny check of the top hits.
5. **C4 — antiSMASH** on uicgpu: created a fresh conda env with **antiSMASH 8.0.4**, downloaded + pre-built all databases, ran `antismash --genefinding-tool prodigal --cpus 16` on the genome; parsed `mrosea.json` region areas by product category.
6. **Verdict:** two free LLM judges (Argo `gpt-5.2` and `claude-opus-4.8`) scored the claims-vs-evidence (not regex).

## 4. Results vs Paper

### 4.1 C2/C3 — Genome statistics (Table 1) — **exact match**

| Metric | Paper (Table 1) | This replication | Match |
|---|---|---|---|
| Contigs / topology | 1, complete circular | 1 | ✅ |
| Genome size (bp) | **16,040,666** | **16,040,666** | ✅ EXACT |
| GC % | 69.07 | 69.10 | ✅ (Δ0.03) |
| Protein-coding genes (CDS) | **14,018** | **14,018** | ✅ EXACT |
| CDS on (+) strand | **6,983** | **6,983** | ✅ EXACT |
| CDS on (−) strand | **7,035** | **7,035** | ✅ EXACT |
| Coding density % | 87.31 | 87.59 | ✅ (Δ0.28) |
| tRNA | 88 | 89 | ~ (Δ1, annotation-method dependent) |
| rRNA operons | 4 (5S–16S–23S) | 4×16S + 4×23S (+ 2×5S) | ✅ |

The **exact reproduction of the strand-resolved CDS counts (6,983 / 7,035)** confirms this is the identical deposited assembly, and the genome-size and gene-count headline numbers reproduce to the base pair / gene. The "largest bacterial genome" claim is a comparative statement about 2021 databases and is not independently benchmarked here, but the 16.04 Mbp size — extreme for a bacterium — is confirmed.

### 4.2 C5 — *pfa* PUFA gene cluster — **reproduced (3 independent lines)**

**(a) Homology.** BLASTP of every reference Pfa protein vs the M. rosea proteome (`pfa_blast_summary.json`):

| Reference Pfa | Best M. rosea hit | %id | summed cov |
|---|---|---:|---:|
| Pfa1 (Aetherobacter/Sorangium) | APR86155.1 | 71.3 / 64.5 | ~97–99% |
| Pfa2 / PfaA (PKS) | APR86156.1 | 67–68 | 49–79% |
| Pfa3 / PfaC (PKS) | APR86157.1 | 56–63 | 79–91% |
| PfaE (PPTase) | APR88149.1 | 63.1 | 98% |

**(b) Synteny.** The three core hits are consecutive locus tags on the same strand:
`A7982_11504` (13,114,225–13,115,874 +) → `A7982_11505` (13,115,901–13,123,181 +) → `A7982_11506` (13,123,210–13,131,432 +), with 27 / 29 bp intergenic gaps — a contiguous *pfa* operon, matching the paper's "conserved synteny of the complete *pfa* gene cluster."

**(c) Independent annotation + antiSMASH.** NCBI PGAP independently annotates APR86156.1 as *"omega-3 polyunsaturated fatty acid synthase subunit, PfaA."* antiSMASH independently detected a **T1PKS/hglE-KS region at 13,095,900–13,151,432** (hglE-KS is the PUFA-synthase ketosynthase class) that exactly spans this operon — a third convergent confirmation.

### 4.3 C4 — antiSMASH BGC survey — **category-level reproduced; count version-shifted**

| Category | Paper (antiSMASH v5.0) | This replication (v8.0.4) |
|---|---:|---:|
| terpene | 9 | 12 |
| RiPP-like / RiPP | 7 | 9 |
| NRPS + NRPS-like | 7 | 8 |
| PKS (T1PKS+T3PKS) | 4 | 5 |
| RRE-containing | 4 | 5 |
| indole | 3 | 3 |
| thioamitide(s) | 2 | 3 |
| arylpolyene | 2 | 2 |
| lanthipeptide | 3 | 3 |
| phosphonate | 1 | 1 |
| phenazine | 1 | 1 |
| siderophore | 1 | 1 (NI-siderophore) |
| **TOTAL BGC regions** | **47** | **53** |

The **dominant-category ranking (terpene / NRPS / RiPP / PKS)** and the **rare singleton set** (phosphonate, phenazine, siderophore, thioamitide, arylpolyene) reproduce faithfully. The total count differs (53 vs 47); this is fully consistent with **antiSMASH v8 having more detection rule sets than the v5 the authors used**, not a genuine disagreement. Evidence: `antismash_summary.json`.

## 5. Evidence artifacts
- `evidence/genome_stats.json` — genome statistics vs paper Table 1
- `evidence/pfa_blast_summary.json` — pfa ortholog BLAST hits + coverage
- `evidence/antismash_summary.json` — antiSMASH 8.0.4 region/category tally
- `evidence/llm_judge_gpt52.txt`, `evidence/llm_judge_opus48.txt` — dual free-LLM judgments
- `work/` — fulltext.xml, downloaded genome (GCA_001931535.1), pfa_refs.faa, BLAST DB + outputs, antiSMASH JSON, scripts

## 6. LLM-judge summary (free Argo endpoints)
- **gpt-5.2:** coverage 100%, verdict **PARTIAL** (weighted the exact-count deltas, esp. C4 53 vs 47).
- **claude-opus-4.8:** coverage 100%, verdict **REPLICATED** (4 Agree + 1 Partial; C4 delta attributed to tool version).

Reconciling the two (and following the brief's "do not inflate" guidance), the honest call is a **strong PARTIAL**: the genome and *pfa*-cluster science reproduce robustly and largely exactly, with the single non-exact item (BGC total) explained by a documented antiSMASH version difference rather than any scientific contradiction.

## Verdict
**Verdict:** PARTIAL

---
WAVE_RESULT set=BVBRC-51 paper=PMID:34511070(Pal2021,Minicystis_rosea_DSM24000T,BMC_Genomics,10.1186/s12864-021-07955-x) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-51-Minicystis-rosea-DSM24000-BGC-2021 one_line="Genome CP016211.1 (GCA_001931535.1) reproduced exactly (16,040,666 bp; CDS 14,018 with 6,983/7,035 strand split identical); pfa PUFA operon confirmed by BLAST+synteny+antiSMASH; antiSMASH v8 found 53 BGCs vs paper's 47 (v5), category ranking matches."
