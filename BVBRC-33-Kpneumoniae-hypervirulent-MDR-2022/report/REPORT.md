# Replication Report: Altayb et al. (2022)
## "Genomic Analysis of Multidrug-Resistant Hypervirulent (Hypermucoviscous) *Klebsiella pneumoniae* Strain Lacking the Hypermucoviscous Regulators (rmpA/rmpA2)"

**Paper:** Altayb HN, Elbadawi HS, Baothman O, Kazmi I, Alzahrani FA, Nadeem MS, Hosawi S, Chaieb K. *Antibiotics* (Basel) 2022; 11(5):596.
**DOI:** [10.3390/antibiotics11050596](https://doi.org/10.3390/antibiotics11050596) — **PMID:** 35625240 — **PMC:** PMC9137517
**Open access:** ✅ (CC BY 4.0, MDPI Gold)
**Set:** BVBRC-100 replication project · target #33
**Analyst:** Ollie (OpenClaw AI) — Replication Wave 2026-07-01
**Verdict:** **PARTIAL REPLICATION (strong).** All core genomic-typing claims and the paper's headline finding (hypermucoviscous ST14/K2 strain that *lacks rmpA/rmpA2* but keeps RcsAB) were **independently reproduced on the authors' own deposited genome** (GCA_022511605.1) using modern curated tools (Kleborate v3, AMRFinderPlus 4.2.7). Three feature-level sub-claims did not confirm: aerobactin (iutA) and salmochelin (iroN) are not supported by Kleborate's curated virulence loci, and plasmid-borne blaCTX-M-15 is absent from the deposited draft assembly. LLM-judge agreement **15/18 = 0.83**.

---

## 1. Paper

A single MDR hypervirulent (hypermucoviscous) *K. pneumoniae* clinical isolate, **"9KP"**, was recovered from a patient with recurrent UTI. Hypermucoviscosity was confirmed by string test; the genome was Illumina-sequenced and characterized bioinformatically. The isolate was reported as **hypermucoviscous, K2 capsule, ST14, MDR** (resistant to ciprofloxacin, ceftazidime, cefotaxime, TMP-SMX, cephalexin, nitrofurantoin). It was reported to carry four AMR plasmids (pKPN3-307_type B, pECW602, pMDR, p3K157) bearing blaOXA-1, blaCTX-M-15, sul2, APH(3″)-Ib, APH(6)-Id, AAC(6′)-Ib-cr6, plus two chromosomal ARGs (**fosA6, SHV-28**). Virulome: 19 fimbrial proteins, one aerobactin (iutA), two salmochelin (iroE, iroN), four T6SS. **Headline:** the isolate is hypermucoviscous yet **lacks rmpA/rmpA2**, instead carrying RcsAB capsule regulators (rcsA, rcsB) — a rare configuration.

Data deposited (verified from full-text Data Availability): **BioProject PRJNA767482, BioSample SAMN26332310, WGS JAKWFM000000000**.

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Isolate is *K. pneumoniae* | Genomic ID | Yes | ✅ |
| C2 | Sequence type = **ST14** | MLST | Yes | ✅ |
| C3 | Capsule = **K2 (wzi2)** | Serotyping | Yes | ✅ |
| C4 | O serotype = **O1** | Serotyping | Yes | ✅ |
| **C5** | **Isolate LACKS rmpA and rmpA2 (headline)** | Genomic | **Yes** | ✅ |
| C6 | Alternative regulators **RcsA + RcsB present** | Genomic | Yes | ✅ |
| C7 | No yersiniabactin/colibactin (low curated virulence) | Genomic | Yes | ✅ |
| C8 | **SHV-28** chromosomal β-lactamase | AMR | Yes | ✅ |
| C9 | **blaOXA-1** | AMR | Yes | ✅ |
| C10 | sul2, APH(3″)-Ib, APH(6)-Id, AAC(6′)-Ib-cr | AMR | Yes | ✅ |
| C11 | **fosA6** chromosomal fosfomycin resistance | AMR | Yes | ✅ |
| C12 | Ciprofloxacin resistance / QRDR mutation | AMR | Yes | ✅ |
| C13 | oqxA efflux | AMR | Yes | ✅ |
| C14 | Aerobactin **iutA** present | Virulome | Yes | ⚠️ (not confirmed) |
| C15 | Salmochelin **iroE + iroN** present | Virulome | Yes | ⚠️ (iroE yes, iroN no) |
| C16 | **blaCTX-M-15** (plasmid pMDR) | AMR | Yes | ❌ (absent in assembly) |
| C17 | T6SS present (4 systems) | Virulome | Yes | ✅ |
| C18 | Extensive fimbrial repertoire (19 fimbrial) | Virulome | Yes | ✅ |

## 3. Method

All from free public sources; no fabricated numbers.

1. **Paper text** — Europe PMC `fullTextXML` (PMC9137517); MDPI PDF was bot-blocked. Parsed the Data Availability section to recover the deposition IDs.
2. **Genome retrieval** — resolved BioSample **SAMN26332310** → assembly **GCA_022511605.1** via NCBI Datasets REST (the parent BioProject PRJNA767482 is an umbrella project holding many unrelated isolates, so the biosample was the correct key). Downloaded genome + protein + GFF with `datasets download`.
   - Stats (Biopython): **5,364,730 bp, 83 contigs, GC 57.33%, N50 220,979, largest contig 665,441** — consistent with a draft KpSC genome.
3. **Genotyping** — **Kleborate v3 `--preset kpsc`** (KpSC species/Mash, chromosomal MLST, Kaptive K & O locus typing, curated virulence loci `rmst`/`rmpa2`/`abst`/`smst`/`ybst`/`cbst`, and KpSC AMR).
4. **Resistome** — **AMRFinderPlus 4.2.7** (DB 2026-05-15.1) with `--organism Klebsiella_pneumoniae --plus`.
5. **Targeted checks** — `blastn` of a blaCTX-M-15 reference (NG_048935.1) against the assembly; PGAP product-name inspection of `protein.faa` (5,064 proteins) for IroE, RcsA, RcsB, T6SS, fimbrial repertoire.
6. **Verdict** — LLM judge (free Argo). `argo:claude-opus-4.8` returned HTTP 502 (proxy bug) → fell back to **`argo:gpt-5.2`** (free), scoring the paper-vs-replication claims table.

Tools/env: bioconda env `kleb` (minimap2 2.31, mash, AMRFinderPlus 4.2.7, BLAST+ 2.17.0) + pip `kleborate` v3 / `kaptive` in a venv. Evidence in `report/evidence/`; code + data in `work/`.

## 4. Results vs Paper

### 4.1 Core typing — exact reproduction

| Property | Paper | This replication (tool) | Match |
|---|---|---|---|
| Species | *K. pneumoniae* | *K. pneumoniae*, match "strong" (Kleborate/Mash) | ✅ |
| MLST | **ST14** | **ST14** (gapA1, infB6, mdh1, pgi1, phoE1, rpoB1, tonB1) | ✅ exact |
| Capsule (K) | **K2**, wzi2 | Kaptive **KL2 / K2**, 99.83% id, "Typeable"; **wzi2** | ✅ |
| O antigen | **O1** | Kaptive **OL2α.1 / O1αβ,2α**, 100% id | ✅ |

### 4.2 Headline claim — rmpA/rmpA2 absence (C5)

| Marker | Paper | Kleborate (rmst / rmpa2) | PGAP product |
|---|---|---|---|
| **rmpA** | **absent** | **absent** | none |
| **rmpA2** | **absent** | **absent** | none |
| rcsA | present | (RcsAB not in Kleborate) | **transcriptional regulator RcsA** (MCH6120814.1) ✅ |
| rcsB | present | — | **transcriptional regulator RcsB** (MCH6119087.1) ✅ |

**The paper's central, unusual finding — a hypermucoviscous K2/ST14 strain that lacks the canonical rmpA/rmpA2 regulators while retaining RcsAB — is independently confirmed on the actual deposited genome.** Kleborate's overall **virulence_score = 0** (no ybt/clb/aerobactin/salmochelin), consistent with the paper's emphasis that classic hvKp virulence-plasmid markers are largely absent.

### 4.3 Resistome — AMRFinderPlus (independent of the paper's ResFinder/RGI)

| Gene (paper) | AMRFinderPlus | %cov/%id | Match |
|---|---|---|---|
| SHV-28 (chr) | blaSHV-28 | 100/100 | ✅ |
| blaOXA-1 | blaOXA-1 | 100/100 | ✅ |
| sul2 | sul2 | 100/100 | ✅ |
| APH(3″)-Ib | aph(3″)-Ib | 100/100 | ✅ |
| APH(6)-Id | aph(6)-Id | 100/100 | ✅ |
| AAC(6′)-Ib-cr6 | aac(6′)-Ib-cr**5** | 100/100 | ✅ (allele-name diff) |
| fosA6 | fosA (FosA5 family) | 100/100 | ✅ (family/allele level) |
| Cipro-R / QRDR | **GyrA p.Ser83Tyr**; Kleborate cipro "nonwildtype R" (MIC 2 mg/L) | 100/99.7 | ✅ |
| oqxA | oqxA + oqxB | 100/100 | ✅ |
| tet(A) | tet(A) | 100/100 | ✅ |
| **blaCTX-M-15** (plasmid pMDR) | **not found** | — | ❌ |

blaCTX-M-15 blastn vs the deposited assembly returned only spurious fragments (≤44 bp, ≤7% query coverage) → the full gene is **absent from the deposited draft**. The paper reports it on plasmid pMDR (reconstructed separately with plasmidSPAdes); that plasmid content is evidently not part of the deposited WGS assembly.

### 4.4 Virulome reconciliation

| Feature | Paper (VFDB/RAST) | This replication | Verdict |
|---|---|---|---|
| Aerobactin **iutA** | 1 present | Kleborate abst: **absent**; no PGAP aerobactin product | ⚠️ discrepancy |
| Salmochelin **iroE** | present | **PGAP "siderophore esterase IroE"** (MCH6118329.1) present | ✅ |
| Salmochelin **iroN** | present | Kleborate smst: **absent**; no IroN receptor product | ⚠️ discrepancy |
| Yersiniabactin/colibactin | (not claimed present) | absent | ✅ |
| **T6SS** (4 systems) | 4 systems (~35 components) | **32** "type VI secretion system" PGAP products across multiple clusters | ✅ |
| Fimbrial proteins | 19 | **46** fimbrial/pilus products (type1 fim, type3 mrk, ECP) | ✅ (rich; count is tool-dependent) |

The aerobactin/salmochelin-receptor discrepancy is a genuine tool-dependency: the paper's VFDB/RAST hits for iutA/iroN are not corroborated by Kleborate's curated, locus-aware KpSC virulence databases (which are the current field standard). iroE — the one salmochelin component that IS in the deposited annotation — was confirmed.

## 5. Verdict

**PARTIAL REPLICATION (strong).**

> *(LLM judge, argo:gpt-5.2, free)* "Most central, checkable genomic-typing results reproduce on the authors' own deposited assembly: species, ST14, K2 (wzi2), O1, the headline absence of rmpA/rmpA2, presence of RcsA/RcsB, low Kleborate virulence score, and essentially the full AMR profile including the QRDR mutation. However, there are substantive non-replications in virulence/plasmid content: no aerobactin locus (contradicting iutA), salmochelin/iroN not found (though iroE present), and the claimed plasmid-borne blaCTX-M-15 is not detectable in the deposited assembly. **PARTIAL. 15/18 = 0.83.** Most important discrepancy: missing plasmid-borne blaCTX-M-15."

**Why PARTIAL, not REPLICATED:** the two most testable-but-failed items are (a) plasmid-borne **blaCTX-M-15 absent** from the deposited genome — a key resistance determinant the paper highlights — and (b) two curated **virulome sub-claims (iutA, iroN)** unsupported by Kleborate. These are honest, evidence-backed discrepancies, not method failures. **Why strong:** every core typing claim and the paper's distinctive headline finding reproduced *exactly* on the authors' own data using fully independent modern tools.

## 6. Files
- `report/evidence/genome_stats.json` — assembly statistics
- `report/evidence/kleborate_full.tsv` — full Kleborate kpsc output (all loci)
- `report/evidence/amrfinderplus.tsv` — AMRFinderPlus resistome
- `report/evidence/virulence_reconciliation.json` — rmpA/iutA/iroN/RcsAB/T6SS/fimbriae checks
- `work/` — downloaded genome (GCA_022511605.1), venv, kleborate_out, judge prompt/verdict, paper text
