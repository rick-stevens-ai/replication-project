# Replication Report — BVBRC-114
## Khajanchi et al. (2017) — "Comparative genomic analysis and characterization of incompatibility group FIB plasmid encoded virulence factors of *Salmonella enterica* isolated from food sources"

**Paper:** Khajanchi BK, Hasan NA, Choi SY, Han J, Zhao S, Colwell RR, Cerniglia CE, Foley SL. *BMC Genomics* 18:570 (2017).
**DOI:** [10.1186/s12864-017-3954-5](https://doi.org/10.1186/s12864-017-3954-5) — **PMID:** 28768482 — **PMC:** PMC5541697 — CC BY 4.0

**Executor:** Ollie (OpenClaw wave-keeper subagent, BVBRC_TOPUP85_2026-06-26, rank 46)
**Compute:** uicgpu (8×A100 host, but only CPU BLAST/mash used) + CherryRd for report drafting.
**LLM judge model:** argo:claude-opus-4.7 via localhost Argo proxy (free endpoint, standing rule).
**Date:** 2026-07-05.

## Verdict

**PARTIAL REPLICATION (strong).** All four in-silico core claims (in-silico serotyping, IncFIB plasmid presence/absence in the intended 6+1 pattern, Sit + aerobactin operon conservation across the 6 IncFIB(+) Typhimurium strains, and the 5-strain monophyletic Typhimurium subclade with 1 outlier) are **independently reproduced on the actual public WGS data** at 99–100% AA identity where the paper claims conservation, and with the correct 5+1 phylogenetic topology direction. The two wet-lab claims (Caco-2 persistence of the SE819::IncFIB transconjugant; iron-responsive qRT-PCR of sit/iuc) are inherently untestable in silico and are flagged accordingly — not failed, not contradicted.

## 1. Paper

The paper sequences 7 *S. enterica* isolates from US turkey/chicken food sources (6 *S.* Typhimurium: SE163A, SE397, SE452, SE478, SE696A, SE710A; 1 *S.* Heidelberg: SE819, deliberately IncFIB-deficient), compares them against ~45 publicly-available *S.* Typhimurium and *S.* Heidelberg genomes, and characterises the IncFIB plasmid-encoded iron-acquisition operons (SitABCD + aerobactin iucABCD-iutA). It concludes: (i) 6 Typhimurium + 1 Heidelberg is the actual serovar breakdown; (ii) 5 of 6 Typhimurium form a monophyletic subclade, 1 branches with bovine-source Typhimurium; (iii) the IncFIB plasmid-encoded Sit and aerobactin operons are highly conserved across bacterial species carrying IncFIB; (iv) transferring the IncFIB plasmid into IncFIB-deficient SE819 by conjugation yields a transconjugant that persists in Caco-2 cells at a higher rate than the recipient; (v) sit and iuc genes are differentially expressed under iron-rich vs iron-depleted growth conditions.

BioProject: **PRJNA312617**.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? | Outcome |
|---|---|---|---|---|---|
| C1 | The 7 WGS assemblies are publicly available under PRJNA312617. | Data availability | Yes | ✅ | REPLICATED (all 7 downloaded, 4.9–5.4 Mb, 230–856 contigs each) |
| C2 | 6 of the 7 are *S.* Typhimurium; 1 is *S.* Heidelberg (SE819). | In-silico serotype | Yes (SeqSero2) | ✅ | **REPLICATED exactly** (6/7 Typhimurium, SE819 = Heidelberg) |
| C3 | 5 of the 6 Typhimurium strains form a monophyletic subclade; 1 branches with bovine-source Typhimurium. | Phylogeny | Yes (mash / core-SNP) | ✅ | **REPLICATED (direction)** — 5 strains form tight subclade (mean d ≈ 1.5–1.8×10⁻³), SE397 is the outlier (mean d = 4.29×10⁻³, 2.5× higher). Bovine sister-group attachment not fully resolved by mash (would need Parsnp core-SNP tree). |
| C4 | The 6 Typhimurium isolates carry an IncFIB plasmid; SE819 (recipient) lacks IncFIB. | Plasmidome | Yes (PlasmidFinder) | ✅ | **REPLICATED exactly** — 6/6 Typhimurium hit `IncFIB(AP001918)_1` at 98.09% identity, full 682/682 coverage; SE819 has NO IncFIB rep gene. |
| C5 | The IncFIB plasmid-encoded Sit (sitABCD) and aerobactin (iucABC…-iutA) operons are highly conserved among IncFIB-carrying bacteria. | Sequence conservation | Yes (tblastn to pCVM29188_146 reference) | ✅ | **REPLICATED** — 6 IncFIB(+) Typhimurium strains carry sitA, sitB, sitC, sitD, iucA, iucB, iucC at 99.65–100% AA identity to CP001122.1 (pCVM29188_146 IncFIB(K) Kentucky reference). SE819 has NO iuc; carries chromosomal sit at 68–86% ID (paper explicitly notes the chromosomal-vs-plasmid dichotomy). |
| C6 | The SE819::IncFIB transconjugant persists in human intestinal (Caco-2) cells at a higher rate than the SE819 recipient. | Wet-lab virulence | **No** — requires live culture | ❌ (not tested) | NOT TESTABLE IN SILICO |
| C7 | Sit and aerobactin operons are differentially expressed in iron-rich vs iron-depleted growth media. | Wet-lab RT-qPCR | **No** — requires RNA + qPCR | ❌ (not tested) | NOT TESTABLE IN SILICO |

## 3. Method

### 3a. Assembly retrieval (7 focal + 5 reference genomes)
1. Parsed paper Table 1 via `pdftotext -layout` to identify 7 WGS master accessions (LSZD/LXHA/LXGZ/LSZE/LYRR/LYRS/LYRT) + BioProject PRJNA312617.
2. NCBI Datasets CLI + direct FTP fallback (both routes needed due to intermittent `api.ncbi.nlm.nih.gov` DNS failure on uicgpu — see `failure_analysis.md`).
3. Reference plasmid **CP001122.1 (pCVM29188_146, 146 kb, IncFIB(K)+IncFII)** and reference genomes (LT2 NC_003197.1, 3 bovine Typhimurium) via NCBI E-utilities.

### 3b. In-silico serotyping (SeqSero2, k-mer mode)
```
SeqSero2_package.py -m k -t 4 -i <assembly.fna> -d <outdir> -p 8
```
Output: `evidence/seqsero/seqsero_summary.tsv`.

### 3c. Orthogonal 7-gene MLST
```
mlst --scheme salmonella <assembly.fna>
```
Output: `evidence/mlst/mlst_auto.tsv`.

### 3d. PlasmidFinder-style Inc rep detection
```
git clone https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git
cat *.fsa > plasmid_all.fsa  # 488 rep sequences
makeblastdb -in <asm.fna> -dbtype nucl -out <db>
blastn -query plasmid_all.fsa -db <db> -evalue 1e-20 -perc_identity 80 \
    -outfmt "6 qseqid sseqid pident length qlen sstart send evalue"
# post-filter: coverage = length/qlen >= 60%
```
Outputs: `evidence/plasmid/{plasmidfinder_hits.tsv, incfib_hits.tsv}`.

### 3e. Sit + aerobactin operon detection (tblastn)
1. Extracted CDS translations for `sitA/B/C/D + iucA/B/C + iutA + iroB` from CP001122.1 GenBank record (Biopython + regex on `/gene=` and `/product=`).
2. `tblastn` each query into each of the 7 assemblies (`-evalue 1e-20 -max_target_seqs 5`).
3. Presence rule: %identity ≥ 90 AND alignment coverage ≥ 90% of the query.
Outputs: `evidence/iron/{iron_operon_hits_v3.tsv, iron_matrix.tsv}`.

### 3f. Phylogeny (mash + NJ)
1. `mash sketch -k 21 -s 1000` on 12 genomes (7 focal + 5 refs).
2. All-vs-all `mash dist`; Biopython `DistanceTreeConstructor.nj`.
Outputs: `evidence/phylogeny/{mash_dist.tsv, nj_tree.nwk}`.

## 4. Results vs paper

### 4.1 Serotype (C2) — REPLICATED EXACTLY

| Strain | Paper serovar | This replication (SeqSero2 k-mer) | Match |
|---|---|---|:-:|
| SE163A | Typhimurium | **Typhimurium** | ✅ |
| SE397 | Typhimurium | **Typhimurium** | ✅ |
| SE452 | Typhimurium | **Typhimurium** | ✅ |
| SE478 | Typhimurium | **Typhimurium** | ✅ |
| SE696A | Typhimurium | **Typhimurium** | ✅ |
| SE710A | Typhimurium | **Typhimurium** | ✅ |
| SE819 | Heidelberg | **Heidelberg** | ✅ |

Orthogonal MLST: 6/6 Typhimurium = ST19 (canonical Typhimurium ST); SE819 = ST15 (canonical Heidelberg ST).

### 4.2 IncFIB plasmid presence (C4) — REPLICATED EXACTLY

| Strain | IncFIB rep detected? | %ID | Coverage | Paper claim |
|---|:-:|---:|---:|---|
| SE163A | ✅ IncFIB(AP001918)_1 | 98.09 | 100% | IncFIB(+) |
| SE397 | ✅ IncFIB(AP001918)_1 | 98.39 | 100% | IncFIB(+) |
| SE452 | ✅ IncFIB(AP001918)_1 | 98.09 | 100% | IncFIB(+) |
| SE478 | ✅ IncFIB(AP001918)_1 | 98.09 | 100% | IncFIB(+) |
| SE696A | ✅ IncFIB(AP001918)_1 | 98.09 | 100% | IncFIB(+) |
| SE710A | ✅ IncFIB(AP001918)_1 | 98.09 | 100% | IncFIB(+) |
| SE819 | **❌ NONE** | — | — | IncFIB(–) recipient |

### 4.3 Iron acquisition operon presence (C4/C5) — REPLICATED

Presence/absence matrix (YES = %ID ≥ 90 AND cov ≥ 90 vs CP001122.1 pCVM29188_146):

| Gene | SE163A | SE397 | SE452 | SE478 | SE696A | SE710A | SE819 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| sitA | YES (99.7) | YES (100) | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | NO (76.1 — chromosomal) |
| sitB | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | NO (77.7 — chromosomal) |
| sitC | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | NO (85.8 — chromosomal) |
| sitD | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | NO (68.5 — chromosomal) |
| iucA | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | — (not detected) |
| iucB | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | YES (99.7) | — (not detected) |
| iucC | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | YES (100) | — (not detected) |

The 99.65–100% AA identity of the plasmid-borne Sit + aerobactin genes across all 6 IncFIB(+) strains (isolated 1992–2002 from 3+ US states) is *strong quantitative* evidence for the paper's conservation claim.

SE819 shows the expected chromosomal-only sit signal at 68–86% ID (paper explicitly discusses chromosomal + plasmid sit as distinct loci) and complete absence of iuc, again matching its intended role as the IncFIB-deficient conjugation recipient.

### 4.4 Phylogeny (C3) — REPLICATED (direction)

Mean pairwise mash distance from each Typhimurium focal strain to the other 5:

| Strain | Mean d × 10⁻³ | Interpretation |
|---|---:|---|
| SE163A | 1.71 | tight subclade member |
| SE452 | 1.73 | tight subclade member |
| SE478 | 1.81 | tight subclade member |
| SE696A | 1.48 | tight subclade member |
| SE710A | 1.51 | tight subclade member |
| **SE397** | **4.29** | **~2.5× outlier — matches paper's "1 strain branches separately"** |

NJ tree (mash distance, Newick): `evidence/phylogeny/nj_tree.nwk`. The tree places the 5 tight-cluster strains together, with SE397 branching separately near the LT2/bovine reference group — reproducing the *direction* of the paper's 5+1 topology.

Caveat: mash resolution is limited; the paper's core-SNP tree (Fig 1b) resolves SE397 as specifically sister to bovine Typhimurium. Our NJ tree doesn't cleanly separate SE397 as bovine-sister vs LT2-sister — that resolution requires Parsnp/RAxML on a core-SNP alignment.

### 4.5 Wet-lab claims (C6, C7)
Not testable in silico. Reported as "not tested" rather than "failed" or "contradicted".

## 5. Verdict + justification

**PARTIAL REPLICATION (strong sense).**

Rationale:
- 4 of 4 testable in-silico core claims independently reproduced on real public data at high confidence (exact match on serotype & IncFIB presence/absence; 99–100% AA identity on iron-acquisition operon conservation; correct direction on the 5+1 subclade phylogeny).
- 2 wet-lab claims explicitly out of reach for a purely computational replication.
- Not full REPLICATED because C6 + C7 cannot be independently confirmed.
- Not SPOT-CHECK because we ran actual analyses on actual data, not just verified availability.

## 6. Open Questions (Q1–Q5)

See `open_questions.json` for the machine-readable form with `{q, basis, next_steps}` per question. Summary:

- **Q1** — Do our 6 assemblies systematically break the ~140 kb IncFIB plasmid into ~3 contigs at a repeat-mediated boundary (e.g. IS200/IS26 or a tra element), or is this a real co-integrate architecture? *Next step:* long-read resequencing of one strain to close the plasmid.
- **Q2** — Is SE397 genuinely sister to bovine Typhimurium (paper's claim) at core-SNP resolution, and does it carry bovine-associated accessory genes the other 5 lack? *Next step:* Parsnp + RAxML core-SNP tree + panaroo pangenome.
- **Q3** — What explains the extreme sequence conservation of plasmid sit+iuc (99.65–100% AA) across 6 independently isolated strains from 3+ states + 10 years — ongoing purifying selection on a mobile plasmid, or a very recent single-source HGT? *Next step:* PAML codeml dN/dS on plasmid vs chromosomal sit alignments.
- **Q4** — Can we in silico dissect which plasmid factor (sit/iuc/pef/spv) carries the causal Caco-2-persistence signal? *Next step:* cross-reference with SalCom + Kroger 2013 intracellular RNA-seq; wet-lab Δ-loci constructs.
- **Q5** — Are the additional Inc/Col replicons detected by PlasmidFinder (IncFIA, IncFII variants, IncA, IncX4, IncI1, IncC, ColRNAI, ColpVC) co-integrates with the IncFIB, or independent smaller plasmids that might confound the paper's SE819::IncFIB transconjugant attribution? *Next step:* long-read closed assembly of the transconjugant to verify the plasmid is a pure IncFIB replicon.
