# Failure Analysis: BVBRC-50 Shewanella oncorhynchi Z-P2 Pan-Genome

**Verdict:** PARTIAL REPLICATION (strong) — 5/7 claims tested, 2 STRONG + 3 MODERATE, no FAIL, no contradictions.

This document collects, honestly, what did **not** replicate cleanly and where the replication design itself is weak.

---

## 1. Claims not tested at all

### 1.1 C6 — UPLC-MS m/z 373.21 (out of scope)
- **Status:** Not tested. Genuine wet-lab measurement, not computationally reproducible from public sequence data alone.
- **Impact on verdict:** Neutral — the biological identity of putrebactin is strongly supported by the BGC-content verification (C3): the NIS operon at 1,858,771–1,862,960 carries the textbook putrebactin enzyme set (ornithine N5-oxygenase → hydroxamate; IucA/IucC synthetase → macrocyclization; TonB-dependent receptor for ferri-putrebactin uptake). This is enzyme-level, not molecule-level, evidence.
- **How to close:** requires the actual bench chemistry — outside the scope of a purely computational replication.

### 1.2 C7 — 8 genomic islands / 30 virulence genes / 5 CRISPR arrays / 3 cas sets (subtype I-Fv)
- **Status:** Not re-run. Computationally reproducible in principle, but not attempted in this pass.
- **Weak circumstantial signal only:** the RefSeq PGAP GFF annotates 5 direct-repeat features and 12 riboswitches. This is *broadly consistent* with a CRISPR-bearing genome, but is **not** equivalent evidence for 5 CRISPR arrays with 3 subtype-I-Fv cas sets, nor for the 8 GIs / 30 VFs numbers.
- **Impact on verdict:** honestly reduces coverage from 6/7 to 5/7 of computationally testable claims.
- **How to close:** re-run IslandPath-DIMOB (GIs), VFDB BLAST at >70% identity / >70% coverage (VFs), CRISPRCasFinder or CRISPRdigger (arrays + cas typing). All three are open-source and free to run.

---

## 2. Claims replicated with quantitative gaps

### 2.1 C2 CDS count — 4290 (PGAP) vs 4544 (RAST paper), ~5.6% gap
- **Root cause (inferred, not demonstrated):** systematic RAST-vs-PGAP annotation-pipeline difference. RAST tends to call more/shorter ORFs and treats pseudogenes differently (RefSeq lists 42 pseudogenes here, which PGAP folds out of the CDS pool).
- **Weakness of the explanation:** we did **not** re-run RAST on the same FASTA to demonstrate the reconciliation numerically. The pipeline-gap attribution is textbook-plausible but remains inferred.
- **How to close:** re-run RAST (or use RASTtk) on GCF_030848765.1 FASTA; count CDS; show the numerical gap matches expectation. Alternative: pseudogene reconciliation script that adds PGAP's 42 pseudogenes + short-ORF permissive re-calling and shows convergence toward 4544.

### 2.2 C5 ANI — 91.25% (fastANI) vs 90.09% (paper MUMmer/kSNP), ~1.2 pts gap
- **Root cause (plausible):** different ANI algorithms. fastANI uses Mash-style k-mer sketching + orthologous-fragment identity; the paper uses MUMmer-alignment-based ANI derived through kSNP-style comparisons. These are known to differ by 0.5–2 percentage points on real genomes.
- **Weakness:** we did not implement a MUMmer-based ANI as a second bracket to isolate the algorithm effect.
- **Impact on the biological conclusion:** minimal — the closest-strain identity (YZ08) is exact, and the <95% species-boundary conclusion holds (91.25% is still well under 95%). But the ANI value itself is an *approximate* reproduction.
- **How to close:** add pyani (MUMmer-based) or JSpeciesWS as a second ANI algorithm; report both alongside fastANI to bracket the paper's value.

### 2.3 C4 Z-P2 unique-cluster count — 531 (Roary @70%) vs 618 (paper IPGA/PanOCT), ~14% gap
- **Root cause (well-known):** singleton counts in pan-genome analyses are extremely sensitive to (a) orthology-clustering threshold, (b) tool internals (Roary uses CD-HIT + BLASTp; PanOCT uses reciprocal-best-BLAST with conserved-neighborhood scoring), and (c) upstream annotation-tool splits.
- **Weakness:** we did not run IPGA/PanOCT directly to close the gap. Also, the pan-genome and core-genome cluster counts *do* reproduce to within ~1%, so the singleton-count gap is likely a tail effect on the accessory-vs-strain-unique boundary, not a whole-methodology failure.
- **How to close:** install IPGA + PanOCT, re-run on the same 11 Prokka annotations, and compare Z-P2-unique counts directly. Alternatively, sweep Roary identity thresholds (60/65/70/75/80/85) and show the singleton count crosses 618.

### 2.4 Roary at default 95% identity over-splits — 17,326 pan / 684 core / 1756 Z-P2-unique
- **This is not a failure — it is a control.** It explicitly demonstrates the well-known sensitivity of pan-genome size to orthology threshold. The paper's IPGA/PanOCT default is closer to 70% than 95%; the 70% Roary run is the fair comparison.
- **Impact on verdict:** none — presented in the report as a diagnostic, not a competing result.

---

## 3. Weaknesses of the replication design itself

### 3.1 BGC verification is coordinate-anchored to the paper
- We verified only that the paper's stated cluster windows contain the expected marker enzymes — this checks the paper's cluster annotations for **internal consistency**, not for **independent discovery**.
- **How to close:** re-run antiSMASH on GCF_030848765.1 and compare cluster count and boundaries independently. (antiSMASH is not installed in `bvbrc28`; a container run or a fresh env is needed.)

### 3.2 Comparator set is inherited, not re-derived
- We used the same 10 *S. putrefaciens* genomes referenced by the paper. If the paper's comparator choice biased pan-genome or ANI results (e.g., over-representation of one sub-clade), our replication inherits that bias.
- **How to close:** re-derive the comparator set from an independent taxonomic query (all complete *S. putrefaciens* + *S. baltica* + *S. oneidensis* RefSeq genomes as of 2026-07-01), re-run pan-genome + ANI, and compare.

### 3.3 No pseudogene reconciliation
- PGAP calls 42 pseudogenes on GCF_030848765.1; RAST typically merges some of these into the CDS pool. Without an explicit pseudogene bridge, the CDS-count gap in §2.1 remains partly unexplained.

### 3.4 LLM judge is a self-report, not ground truth
- Per-claim ratings by Argo `argo:gpt-5.2` (STRONG / MODERATE / FAIL) are a useful narrative sanity-check but are computed from our own evidence bundle — they are **not** independent scientific validation.
- **How to close:** cross-run a second judge model (e.g., Argo `argo:claude-opus-4.8` or the CELS nemotron-3-ultra endpoint) on the same evidence bundle and report inter-judge agreement.

### 3.5 No independent species-boundary adjudication
- We accept the paper's *S. oncorhynchi* species designation as given. A stricter replication would compute 16S rRNA identity and dDDH against *Shewanella* type strains (*S. baltica*, *S. putrefaciens*, *S. oncorhynchi* type) to independently support or contest the novel-species claim.
- See `open_questions.json` Q1 for the concrete follow-up plan.

### 3.6 Coverage 5/7 is honest but partial
- Coverage = 5/7 = **71% of all claims**. C7 is the honestly-addressable gap: it could have been run and was not.
- The verdict PARTIAL is accurate — this replication is strong on what it covers but does not attempt full end-to-end reproduction.

---

## 4. What would upgrade this to FULL replication

1. **Re-run antiSMASH** on GCF_030848765.1; compare cluster count and boundaries directly.
2. **Re-run RAST** on the same FASTA; reconcile the CDS-count gap explicitly.
3. **Run IslandPath-DIMOB + VFDB BLAST + CRISPRCasFinder** to test C7 like-for-like (8 GIs / 30 VFs / 5 CRISPR / 3 cas subtype I-Fv).
4. **Compute 16S rRNA identity and dDDH** vs *Shewanella* type strains to independently support the species boundary.
5. **Add MUMmer-based ANI** (pyani or JSpeciesWS) as a second ANI algorithm to bracket the fastANI value against the paper's 90.09%.
6. **Run IPGA/PanOCT directly** on the same 11 Prokka annotations to close the Z-P2 unique-cluster count gap (531 vs 618).
7. **Add a second LLM judge** (Argo Opus or CELS nemotron-3-ultra) for inter-judge agreement on the evidence bundle.

---

## 5. Summary

| Category | Count |
|---|---|
| Claims replicated exactly | 5 (length, GC, tRNA, rRNA, closest-strain identity) |
| Claims replicated within tool-variance | 3 (pan-genome, core-genome, ANI value) |
| Claims with method-dependent gap (partially replicated) | 2 (CDS count, Z-P2 unique clusters) |
| Claims not tested (wet-lab) | 1 (C6 UPLC-MS m/z) |
| Claims not tested (out of scope this pass) | 1 (C7 GIs / VFs / CRISPR) |
| Claims contradicted | **0** |
| Verdict | **PARTIAL REPLICATION (strong)** |
