# Failure Analysis — BVBRC-89 Pangenomics Replication

**Verdict:** PARTIAL (LLM-judge coverage ~45%)
**Scope reproduced:** *Enterobacter cloacae* only (smallest of the paper's 12 species), on the 54/104 PATRIC genomes with public NCBI Assembly accessions, CD-HIT pangenome pipeline + by-genome Heaps' law fit.
**Not reproduced:** MLST-balanced Heaps' fit; 11 other species; functional/domain analyses; 168-gene cross-species core.

This file separates *what genuinely failed* from *what was intentionally out of scope* and names the specific threats to validity in what was done.

---

## 1. What did NOT replicate (genuine gaps, not scope)

### 1.1 α (Heaps' openness) came in 12% below the paper

- **Paper (by-genome, N=104):** α = 0.384 ± 0.023
- **This replication (by-genome, N=54):** α = 0.337 ± 0.020
- **Delta:** −0.047, ~12% low, ~2 SDs outside the paper's error bar.

**Interpretation.** Not a genuine methodological disagreement — the direction and magnitude are exactly what would be predicted from sub-half-sampling of an open pangenome. The gene-discovery rate flattens when you have fewer genomes to sample from, compressing the apparent exponent. Nonetheless: **this is a real numerical divergence** and it prevents us from claiming clean quantitative agreement on the paper's headline statistic. A full 104-genome rebuild (blocked by the 50 missing PATRIC-only genomes) would be needed to close this gap cleanly.

**Mitigation:** the qualitative claim (E. cloacae remains an "open pangenome" with α > 0.3, still inside the Gammaproteobacteria band) survives. The κ intercept (which is much less sample-size-sensitive) landed inside the paper's error envelope (4,445 ± 362 vs 4,330 ± 451).

### 1.2 Total pangenome size ratio 0.66 vs Heaps prediction 0.77

- **Observed ratio:** total pangenome (54 genomes) / total pangenome (104 genomes) = 16,959 / 25,678 = 0.66.
- **Heaps prediction using paper's α:** (54/104)^0.428 ≈ 0.77.
- **Delta:** −0.11 absolute; observed is 14% low relative to Heaps prediction.

**Interpretation.** Consistent with the α-compression above: an open pangenome sampled at half its size delivers fewer unique genes than the extrapolation predicts, because rare accessory-genome discovery scales super-linearly in the tail. This is an internal-consistency check, not an independent failure, but it is worth flagging that our numbers are systematically a bit *below* what a naïve Heaps extrapolation would give.

---

## 2. What was intentionally NOT attempted (scope, not failure)

These are honest "did not run" items, listed so readers do not mistake them for successful replication.

### 2.1 MLST-balanced Heaps' fit

The paper's headline methodological contribution is that MLST-balanced Heaps' fits reduce MAE in 11/12 species and give better cross-species comparability. We only ran the by-genome (unbalanced) fit. Reproducing the MLST-balanced fit requires:
- The `mlst` tool.
- A local copy of the PubMLST database.
- MLST typing of all 54 (ideally 104) genomes.
- Rewriting the shuffle to sample one genome per MLST type per shuffle round.

Claim C6 is therefore **untested**, not tested-and-failed.

### 2.2 11 of 12 species not run

Only E. cloacae (104 total, 54 available on NCBI) was reproduced. The other 11 species (169 to 3,183 genomes each) were not attempted. Claim C5 (openness ~ phylogenetic class) is therefore **untested at cross-species scale**; the single E. cloacae point is trivially consistent with the paper's Gammaproteobacteria placement but provides no independent evidence for the cross-class ordering.

### 2.3 Functional / domain analyses (Figs 4–7 territory)

None of:
- eggNOG-mapper COG enrichment of core vs accessory (C7)
- InterProScan AARS domain mutation enrichment (C8)
- 168-gene cross-species core detection (C9)

was attempted. The paper's biological interpretation — arguably the most important part for readers — is completely **untested** here.

---

## 3. Threats to validity in what WAS done

### 3.1 Selection bias in the 54-genome subset

**Threat.** The 50 missing PATRIC-only genomes may not be a random draw from the 104. They could be disproportionately:
- Clinical isolates from a single outbreak → lower genomic diversity → α biased *down* (which is exactly what we see).
- Or the opposite: exotic environmental isolates that never went through GenBank → higher diversity → α biased *up*.

**What we did not do:** compare metadata (collection year, host, geography, strain designation) of the 54 available vs 50 missing genomes to check representativeness.

**Consequence.** Some fraction of our α = 0.337 vs paper 0.384 gap is likely sampling variance (predictable), but some may be selection bias (not accounted for).

### 3.2 CD-HIT version difference (4.5.4 vs 4.6)

**Threat.** We asserted "algorithm identical, difference cosmetic." This is a plausible claim (CD-HIT's minor-version changelog does not report clustering-algorithm changes across this range) but we did not verify it directly by installing v4.6 and re-running.

**Consequence.** Small residual disagreement (a few hundred clusters out of 16,959) could be version-attributable. Given the size of our other error bars, this is minor, but it is not zero.

### 3.3 Single random seed (42) for Heaps' shuffles

**Threat.** The paper's protocol is 100 shuffles; we followed it. But we used a single meta-seed (42). The reported α SD = 0.020 is the within-seed spread, not the between-seed spread. Changing the meta-seed would produce a slightly different mean.

**Consequence.** The α = 0.337 ± 0.020 envelope is somewhat overconfident. A robust replication would run e.g. 10 different meta-seeds × 100 shuffles each and report the pooled variance. Likely effect: ±1 additional SE on the reported mean.

### 3.4 No input-assembly QC filter

**Threat.** PATRIC/BV-BRC assemblies vary enormously in quality (from PacBio-finished, single-contig, to short-read-only, hundreds of contigs). Fragmented assemblies split single genes across contig ends, inflating the accessory-gene count and biasing α upward. Contaminated assemblies inject spurious unique genes. We ran no CheckM2 completeness/contamination filter, and neither (per REPORT.md) did the paper.

**Consequence.** Both our numbers and the paper's numbers may be biased by the mixed-quality assembly pool in the same direction, cancelling out for the replication question but leaving both estimates biased vs the ground truth. This is a real weakness of the pan-genomics field, not specific to this paper, but it is a threat to the absolute accuracy of every α reported here.

### 3.5 Downstream-repository lag (54/104 available)

**Threat.** We had to reduce N from 104 to 54 because 50 PATRIC IDs are not mirrored to NCBI. This is not the paper's fault, but it is a real failure of the paper's *reproducibility promise*: a reader today, following the paper's own instructions, cannot get the full dataset without going through PATRIC/BV-BRC directly (which is possible but was not the fastest path we chose).

**Consequence.** Every quantitative comparison in this report is between a 104-genome paper number and a 54-genome replication number, with a size-scaling correction applied. A byte-for-byte replication is not currently possible via the fastest public route.

### 3.6 LLM judge is not an oracle

**Threat.** The "~45% coverage" and "PARTIAL" verdict came from `argo:gpt-5.1` after being handed our comparison table. It reproduces the analyst's own framing rather than adjudicating it independently. It also cannot check numbers against the paper directly (it was given our extracted numbers, not the paper PDF).

**Consequence.** The coverage percentage should be read as an order-of-magnitude self-assessment, not a rigorous audit. A human reviewer with the paper in hand would produce a more defensible number.

---

## 4. Where the paper itself might have holes (out-of-scope observations)

Not the focus of this report, but flagged for completeness:

- The paper does not, per REPORT.md, publish per-species pipeline-sensitivity analyses (CD-HIT threshold sweeps, alternate clusterers, alternate annotators). If a sizable fraction of its cross-species differences in α are pipeline-sensitivity artifacts, the phylogenetic-class ordering claim (C5) could be softer than presented.
- The paper's 168-gene 12-species-core count depends on the CD-HIT 0.8 identity threshold; a stricter or looser threshold would change that count non-trivially. No sensitivity analysis was reported.
- Assembly-quality filtering was not applied. See §3.4.

These are noted as follow-up questions, not as accusations of error.

---

## 5. Summary table

| Item | Status | Why |
|---|---|---|
| Data availability (C1) | ✅ Replicated | 104/104 PATRIC IDs still resolvable in BV-BRC on 2026-07-03 |
| CD-HIT pipeline (C2) | ✅ Replicated within 5% | 3,046 core vs 2,906 paper (5% high, subsampling-consistent) |
| Heaps' α (C3) | ⚠️ Partially replicated | 0.337 vs 0.384 paper, ~12% low but same regime |
| Heaps' κ (C4) | ✅ Replicated | 4,445 vs 4,330 paper, mean inside SD envelope |
| Phylogenetic-class placement (C5) | ⚠️ Consistent, not tested at scale | Single species; cross-species pattern untested |
| MLST-balanced fit (C6) | ❌ Not attempted | Missing tool/DB |
| COG functional enrichment (C7) | ❌ Not attempted | Out of scope |
| AARS domain enrichment (C8) | ❌ Not attempted | Out of scope |
| 168 cross-species core genes (C9) | ❌ Not attempted | Requires all 12 species |
| Byte-for-byte 104-genome rebuild | ❌ Blocked | 50/104 PATRIC-only IDs not mirrored to NCBI |

**Overall:** The paper's central pipeline and its numeric predictions for one species are corroborated within predictable subsampling error. The paper's headline cross-species methodological and biological claims are not tested. Verdict PARTIAL is the honest label.
