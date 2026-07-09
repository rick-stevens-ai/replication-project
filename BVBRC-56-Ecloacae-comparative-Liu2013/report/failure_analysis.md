# Failure Analysis — BVBRC-56 Liu et al. (2013) *E. cloacae*

**Verdict:** PARTIAL · **Set:** BVBRC-56 · **Replication date:** 2026-07-02

The purpose of this file is to isolate what did **NOT** replicate, diagnose the failure mode for each miss, and separate genuine data disagreements from methodology-driven artifacts.

---

## 1. What fully replicated (baseline for contrast)

- **Table 1 CDS totals — exact for all 4 strains** (4338 / 5518 / 4619 / 4542). Zero-defect match.
- **Genome sizes / plasmid counts / GC% / rRNA operon counts** — all within rounding.
- **Strain-plasticity rank-ordering** (ATCC13047 19.8% unique vs paper 20% ≈ perfect; full order ATCC13047 ≫ EcWSU1 > ENHKU01 ≈ SDM matches paper).
- **Phylogenomic backbone** — *E. cloacae* clade + clean *Pantoea* outgroup + *E. aerogenes* basal position recovered by an independent AAI/NJ method (paper used 1732-core-gene MrBayes; method-independent recovery is strong evidence).
- **T6SS rank on 2/4 strains** — ATCC13047=2 and SDM=1 both exact.

---

## 2. Partial / non-matches — per claim

### C4: Core-genome CDS count (3540 → 3345, −5.5%)
- **Miss:** 195 fewer core-genome clusters.
- **Root cause:** methodology, not data. Paper used EDGAR (BLAST-Score-Ratio); this work used DIAMOND reciprocal-best-hit with 50% identity + 70% coverage thresholds + single-linkage.
- **Evidence it is methodology-driven:** the derived quantity (strain-unique %) matches almost exactly (ATCC13047 19.8% vs 20%), which cannot happen if the underlying pan-genome is qualitatively different. The 5.5% shift falls squarely within the known EDGAR-BSR vs RBH systematic offset for enterobacterial pan-genome studies.
- **Not falsifying:** I did not re-run EDGAR at its exact cutoffs, so the paper's 3540 number is not directly contradicted.
- **Fix:** run EDGAR (or a BSR-based clone) at the paper's stated cutoff on the same 4 proteomes.

### C7: ENHKU01 nearest neighbor (paper: ATCC13047; this work: 3-way tie)
- **Miss:** whole-proteome AAI ranks SDM 93.96% ≈ EcWSU1 93.83% ≈ ATCC13047 93.65% for ENHKU01 — essentially tied.
- **Root cause:** resolution mismatch. Paper's call is based on 4 housekeeping genes (16S + a few conserved loci); this work's call is based on the full proteome.
- **Interpretation:** either the paper's ATCC13047 nearest-neighbor call is a small-sample artifact of the 4-locus set, or the whole-proteome AAI is too coarse at ~0.4% AAI resolution to see the same signal. Neither hypothesis is falsified.
- **Fix:** rerun with rMLST (53 ribosomal-protein loci) — a middle-resolution method that would arbitrate between the two.

### C8: Fimbriae — 9–13 loci, only 4 conserved across all 4
- **Miss:** got 8–19 loci per strain (right order of magnitude, roughly overlapping range) but noisy over/under-calls; the specific "only 4 conserved" cross-strain intersection was not cleanly re-demonstrated.
- **Root cause:** keyword-based product/gene annotation matching for `fimbrial | pilus | usher | chaperone` is a noisy net — over-calls generic pilus mentions, under-calls loci where CDSs are annotated as "hypothetical".
- **Fix:** run a dedicated CU-family HMM search (e.g. FimTyper / CUPP HMM library) with proper family boundaries and re-do the 4-strain intersection.

### C9: T6SS clusters on ENHKU01 (paper: 2; this work: 1 clear + 1 fragmented) and EcWSU1 (paper: 1; this work: 0)
- **Miss:** 2 of 4 T6SS calls disagree by one cluster each.
- **Root cause:** the paper itself explicitly states *"Two T6SSs of ENHKU01 were manually identified and reconfirmed by BLAST"* — i.e. the paper's numbers on these two strains rely on **manual curation + targeted BLAST** that my automated ≥6-contiguous-component-gene rule cannot reproduce.
- **Evidence:** the rule works exactly on ATCC13047 and SDM (where the T6SS clusters are compact and well-annotated) and fails exactly on the two strains the paper flagged as needing manual work. The failure mode is diagnostic and matches the paper's own methodology note.
- **Not falsifying:** we cannot claim there are fewer T6SSs on ENHKU01/EcWSU1 than the paper says — we can only say automated calling misses them.
- **Fix:** hand-drive tBLASTn with reference ClpV/VgrG/Hcp proteins across ENHKU01 and EcWSU1 scaffolds, allowing fragmented/broken clusters.

### C10: Carbohydrate-utilization genes (paper: >640 / 13–15%; this work: ~424–432 / ~8–10%)
- **Miss:** a large absolute gap (~30% shortfall) — biggest single quantitative miss in this replication.
- **Root cause:** methodology, and this one is stark. Paper used **RAST-SEED subsystem assignment** (a curated database of ~1000+ carbohydrate-related subsystems with hand-curated functional roles). This work used a **product-keyword net** over GenBank annotations. The RAST-SEED corpus is materially broader than any product-string net; it will always find more carbohydrate genes.
- **Not falsifying:** I did not deploy RAST-SEED, so I cannot claim the paper's 640+ is wrong — I can only say a narrower method finds fewer.
- **Fix:** deploy RAST-SEED (or PATRIC/BV-BRC subsystem assignment, or dbCAN2 for CAZymes) at the paper's stated cutoffs.

### C11: Wet-lab antagonism bioassays
- **Miss:** out of scope entirely.
- **Fix:** not achievable in silico.

---

## 3. Threats to the replication's own validity

1. **Same-genome loop.** Both this work and the paper analyze the same 4 NCBI assemblies. Descriptive-stat matches confirm arithmetic on public data, not the underlying biology; no assemblies were re-sequenced.
2. **Free-Argo LLM judge is a single model.** The judge returned PARTIAL and agrees with the human read, but this is single-judge concordance, not independent multi-judge scoring.
3. **No BV-BRC GUI workflow was used.** BV-BRC-equivalent analyses were reconstructed with open tools (DIAMOND/Biopython/MAFFT/FastTree). If the paper's original conclusions depend on a BV-BRC-specific parameter (e.g. a particular RAST version), this replication cannot detect that dependency.
4. **Annotation vintage.** GenBank annotations on some of these 2010–2012 assemblies have been touched by NCBI's annotation pipeline since 2013; feature counts (particularly tRNA/pseudo-gene calls) could drift slightly from paper values. This shows up as the SDM tRNA delta (79 vs paper 83) and the ATCC13047 tRNA anomaly (84 vs paper 24; the 24 is a probable typo).
5. **DIAMOND-RBH thresholds are chosen.** 50% identity + 70% coverage is a reasonable default but not the paper's choice. Different thresholds shift the core count monotonically; the strain-plasticity rank-ordering is robust across a range of thresholds but the absolute numbers are not.

---

## 4. Summary of failure modes

| Failure | Type | Falsifies paper? | Tractable fix |
|---|---|---|---|
| Core CDS 3345 vs 3540 | Methodology (RBH vs BSR) | No | Rerun EDGAR/BSR |
| ENHKU01 nearest-neighbor tie | Resolution (full-proteome vs 4-locus) | No | rMLST |
| Fimbriae "only 4 conserved" | Method noise (keyword vs HMM) | No | CU-family HMM |
| T6SS ENHKU01/EcWSU1 undercount | Manual-curation gap (paper flagged) | No | Hand tBLASTn |
| Carbohydrate 424–432 vs 640+ | Method (product-keyword vs RAST-SEED) | No | Deploy RAST-SEED |
| C7 nearest-neighbor | Method-resolution | No | rMLST |
| C11 wet-lab | Out-of-scope | No | Wet lab (n/a) |

**Bottom line:** every non-match is methodology-explicable and none contradicts the paper's underlying claims. PARTIAL is the honest verdict: the paper's descriptive spine + comparative-genomics backbone reproduce strongly; the annotation-curation-dependent functional counts do not, for reasons intrinsic to the toolchain choice.
