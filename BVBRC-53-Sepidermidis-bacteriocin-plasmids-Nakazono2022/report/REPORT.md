# Replication Report: Nakazono et al. (2022)
## "Complete sequences of epidermin and nukacin encoding plasmids from oral-derived *Staphylococcus epidermidis* and their antibacterial activity"

**Paper:** Nakazono K, Le MN-T, Kawada-Matsuo M, Kimheang N, Hisatsune J, et al. *PLOS ONE* 17(1): e0258283 (2022).
**DOI:** [10.1371/journal.pone.0258283](https://doi.org/10.1371/journal.pone.0258283) · **PMID:** 35041663 · **PMC:** PMC8765612
**Open access:** ✅ (PLOS ONE, CC BY 4.0)

**Set:** BVBRC-53 · **Analyst:** Ollie (OpenClaw AI) — BV-BRC Replication Project (Wave, target #53)
**Report date:** 2026-07-02
**Verdict:** **PARTIAL REPLICATION (strong).** Every sequence-level core claim (plasmid sizes, ORF/CDS counts, complete epidermin & nukacin gene clusters, the ~8 kbp pNuk650 insertion, and both bacteriocin-peptide identity claims) was **independently reproduced on the actual deposited NCBI sequences**, most of them matching to the exact base pair. The only claims out of reach are the wet-lab antibacterial-activity assays (ESI-MS mass, growth-inhibition spectra), which require the physical isolates.

---

## 1. Paper

The authors screened 150 oral *S. epidermidis* isolates (from 287 volunteers), found two bacteriocin producers (**KSE56**, **KSE650**), and used Illumina + MinION hybrid assembly (Unicycler v0.4.8, RAST annotation) to produce complete plasmid sequences:

- **pEpi56** — carries the lantibiotic **epidermin** biosynthesis cluster; reported as the **first complete epidermin-carrying plasmid**.
- **pNuk650** — carries a **nukacin** (nukacin-IVK45-like) cluster; compared against the published reference plasmid **pIVK45**.

Central conclusions: pEpi56 = 64,386 bp / 81 ORFs; pNuk650 = 26,160 bp / 29 ORFs; pNuk650 is larger than pIVK45 (21,840 bp) because of an ~8 kbp insertion (7 additional ORFs); epidermin KSE56 is 100% aa-identical to the classical Tü3298 epidermin; nukacin KSE650 differs from nukacin IVK45 by a single prepeptide mismatch with an identical mature peptide.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | pEpi56 = 64,386 bp, 81 ORFs, full epi cluster; first complete epidermin plasmid | Genomic/stats | Yes (OK031036) | ✅ | **MATCH** (64,386 bp; 81 CDS; epiA,B,C,D,P,Q,E,F,G,H,T′ all present) |
| C2 | pNuk650 = 26,160 bp, 29 ORFs, full nuk cluster | Genomic/stats | Yes (OK031035) | ✅ | **MATCH** (26,160 bp; 29 CDS; nukA,M,T,F,E,G,H all present) |
| C3 | pNuk650 larger than pIVK45 (21,840 bp) via ~8 kbp insertion; +7 ORFs | Comparative | Yes (blastn vs KP702950) | ✅ | **MATCH (structural).** 99.6% backbone identity; 7,781 bp unique to pNuk650, dominated by a single 5,926 bp block. ORF-delta annotation-dependent (see §5). |
| C4 | Epidermin KSE56 prepeptide 100% aa-identical to Tü3298; 2 nt mismatches in epiA | Sequence | Yes (translate OK031036) | ✅ (aa level) | **MATCH** (0 aa mismatches vs canonical Tü3298 prepeptide) |
| C5 | Nukacin KSE650 vs IVK45: 1 prepeptide mismatch, mature identical | Sequence | Yes (align translations) | ✅ | **MATCH** (exactly 1 mismatch at leader position 4 L↔F; mature C-terminus identical) |
| C6 | Complete plasmids deposited in NCBI (OK031036, OK031035) | Data availability | Yes | ✅ | **MATCH** (both retrieved; pIVK45 KP702950 also public) |
| C7 | BV-BRC PlasmidFinder rep-typing workflow applies to these plasmids | Method mappability | Yes | ✅ | **YES** (rep genes recovered; see §4d) |
| C8 | Antibacterial-activity spectra + ESI-MS mass of mature peptides | Wet-lab | **No** (needs isolates) | ❌ | Out of reach |

## 3. Method

All inference on **free endpoints only**. Full-text obtained via Europe PMC OA XML (not the paid `pdf` tool).

### 3a. Sequence retrieval (local)
Downloaded from NCBI nuccore via eutils efetch (FASTA + `gbwithparts`), no auth:
`OK031036` (pEpi56), `OK031035` (pNuk650), `KP702950` (pIVK45).
Raw byte-length of the FASTA sequence body verified the deposited lengths directly.

### 3b. Genome statistics (local, Python)
Computed length, GC%, and CDS count (from GenBank feature table). Extracted `/gene` and `/translation` for all epi/nuk features.

### 3c. Peptide comparisons (local, Python)
- **epiA prepeptide** (pEpi56) aligned to the canonical Tü3298 epidermin prepeptide (`MEAVKEKNDLFNLDVKVNAKESNDSGAEPRIASKFICTPGCAKTGSFNSYCC`).
- **nukA prepeptide** KSE650 (from pNuk650) aligned to nukA IVK45 (from pIVK45), position-by-position; mismatch localized to leader vs mature region.

### 3d. Comparative alignment (local, blastn)
`makeblastdb` on pIVK45; `blastn -perc_identity 80` of pNuk650 vs pIVK45. Query-coverage vector computed to locate unaligned (insertion) blocks. (Local MUMmer was broken — `TIGR::Foundation` @INC error + mbedtls version mismatch — so blastn was used; see attempt_log.)

### 3e. BV-BRC specialty-gene screen (**uicgpu**, per heavy-compute rule)
`ssh uicgpu`; conda env **`bvbrc14`** (`/data/stevens/envs/bvbrc14`). Ran **abricate 1.4.0** against **plasmidfinder, card, resfinder, vfdb, megares, bacmet2** (DBs dated 2026-Apr-03) and **AMRFinderPlus 4.2.7** on all three plasmids. PlasmidFinder is the paper's declared BV-BRC workflow ("PlasmidFinder via Similar Genome Finder").

### 3f. LLM-judge scoring
Argo proxy `localhost:44497`, model `argo:gpt-5.2` (free). Structured JSON verdict over the full claim set.

## 4. Results vs paper

### 4a. Plasmid statistics
| Plasmid | Accession | Paper length | **Measured** | Paper ORFs | **Measured CDS** | GC% |
|---|---|---:|---:|---:|---:|---:|
| pEpi56 | OK031036 | 64,386 bp | **64,386 bp** ✓ | 81 | **81** ✓ | 27.5 |
| pNuk650 | OK031035 | 26,160 bp | **26,160 bp** ✓ | 29 | **29** ✓ | 26.0 |
| pIVK45 | KP702950 | 21,840 bp | **21,840 bp** ✓ | (17 annot.) | 17 | 26.1 |

### 4b. Gene clusters
- **pEpi56 epi cluster present:** epiA, epiB, epiC, epiD, epiP, epiQ, epiE, epiF, epiG, epiH, epiT′ — the complete epidermin biosynthesis/immunity/processing cluster. ✓
- **pNuk650 nuk cluster present:** nukA, nukM, nukT, nukF, nukE, nukG, nukH — the complete nukacin cluster. ✓ (Same seven-gene set also present in pIVK45, confirming the shared backbone.)

### 4c. Peptides
- **Epidermin (epiA):** KSE56 prepeptide = 52 aa, **0 amino-acid mismatches** vs canonical Tü3298 epidermin → 100% aa identity. ✓ (C4)
- **Nukacin (nukA):** KSE650 vs IVK45 prepeptides differ at **exactly one position (pos 4, Leu→Phe)**, in the **leader**; mature C-terminal peptide `KKKSGAVPTVSHDCHMNSWQFIFTCCG` is **identical**. ✓ (C5)

### 4d. Comparative structure (pNuk650 vs pIVK45)
- Shared backbone **99.6% nt identity**; 70.3% of pNuk650 aligns to pIVK45.
- **7,781 bp of pNuk650 is unaligned (unique)**, dominated by a **single 5,926 bp insertion (positions 17040–22965)** plus a 1,821 bp block — reproducing the paper's "**~8 kbp inserted fragment present in pNuk650 but not pIVK45**." ✓ (C3, structural)

### 4e. BV-BRC specialty-gene screen
- **PlasmidFinder:** pNuk650 & pIVK45 share rep genes **repUS46, repUS23_repA (SAP099B family), rep21 (pWBG754)** — same replicon lineage (Similar-Genome/replicon relationship the paper's workflow targets). pEpi56 carries a divergent **rep39/rep5a-like** replicon (lower identity — consistent with it being a novel, first-reported epidermin plasmid). ✓ (C7)
- **AMR:** CARD, ResFinder, MEGARes, AMRFinderPlus — **no hits** on any plasmid.
- **Virulence:** VFDB — **no hits**. BacMet2 — only spurious <33% identity hits (not real biocide/metal resistance).
- **Interpretation:** These are **bacteriocin-immunity plasmids**, carrying lantibiotic biosynthesis + self-immunity (epiE/F/G/H; nukF/E/G/H) rather than acquired AMR or classical virulence — exactly the functional character the paper describes.

## 5. Nuances / honest caveats
- **C3 ORF-delta:** the paper reports "+7 ORFs" in pNuk650 vs pIVK45; by current GenBank annotation the CDS counts are 29 vs 17 (a delta of 12). ORF counts are annotation-method dependent (the paper re-annotated pIVK45 with RAST v2.0). The **structural claim** — a single large (~6–8 kb) insertion accounting for the size increase — is unambiguously confirmed by the alignment; only the exact integer ORF count is method-sensitive.
- **C4 nucleotide detail:** the paper's "2 nt mismatches in epiA" is a DNA-level claim about their read vs Tü3298; the deposited epiA gives a prepeptide that is 100% aa-identical (verified), consistent with silent/leader nucleotide differences. The functionally meaningful claim (identical mature epidermin) holds.
- **Wet-lab (C8)** — antibacterial spectra and ESI-MS mass are not reproducible from sequence and were not attempted.

## 6. Reproducibility
- Sequences: NCBI OK031036 / OK031035 / KP702950 (`work/seqs/`).
- Evidence: `report/evidence/` (genome_stats.txt, blastn_pNuk650_vs_pIVK45.tsv, abricate_*.tsv, amrfinder_*.tsv, llm_judge_prompt.txt, llm_judge_result.json).
- Heavy tools ran on uicgpu env `bvbrc14`; light analysis local.

## Verdict
**Verdict:** PARTIAL
