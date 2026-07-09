# Failure analysis — lucid100-pprm-small-rna-deinococcus

**Real verdict: PARTIAL.** Queue verdict of REPLICATED is **wrong** for this slot and needs reconciliation.

This is the honest critique: where the paper is fragile, where the reproduction fails, and where the audit itself falls short.

## 1. Queue-verdict mismatch (governance, not science)

**Queue records REPLICATED. Bench report records PARTIAL.** The mismatch is real and material:

- The MAPS pull-down and IR-effect contrasts DO replicate cleanly — that likely fed the REPLICATED tag.
- But the genotype-effect contrasts (S4 sham + S5 IR) DO NOT replicate in PyDeseq2 from the same public counts. The paper's flagship gene **pprM (DR_0907)** headline padj $= 1.3\times10^{-9}$ becomes $0.52$ in my redo — a categorical failure, not boundary drift.
- In-silico-testable scope coverage is 5/7 (71%), below the 80% protocol bar for a clean REPLICATED call.

Anyone reading the queue as "REPLICATED" will over-trust this paper's headline sRNA→pprM regulatory quantification. The bench report says PARTIAL for good reason. **The queue tag should be corrected to PARTIAL** (or at minimum flagged for re-review with the S4/S5 discrepancy noted).

## 2. Where the reproduction fails

### 2.1 S4 PprSKD-0 vs WT-0 (sham genotype effect) — categorical failure

- Paper reports 53 significant DEGs at α=0.05; my redo finds 3.
- Spearman ρ between paper L2FC and my L2FC = 0.024 (essentially zero rank correlation).
- Sign concordance = 62% (only marginally above chance).
- padj concordance = 6%.
- **pprM specifically**: paper L2FC = -2.52, padj = 1.3e-9 → my redo L2FC = -0.76, padj = 0.52.

### 2.2 S5 PprSKD-10 vs WT-10 (IR genotype effect) — categorical failure

- Paper reports 31 significant DEGs; my redo finds 0.
- Spearman ρ = 0.205, sign concordance 55%.
- padj concordance at α=0.05 = 0%.

### 2.3 Why S4/S5 fail (three-part diagnosis)

**(a) Numerical drift between PyDeseq2 0.5.4 and R-DESeq2.** PyDeseq2 is a Python port, not a bit-for-bit clone; small differences in dispersion estimation, Cook's outlier refit, and independent filtering are known. At n=3 with a noisy sham baseline these small differences compound into different significance calls.

**(b) WT-0 library-size CV = 0.51.** WTA0 has 22k reads; WTC0 has 63k; WTB0 has 74k. That's a 3.3× spread within a single treatment group of size 3. DESeq2's size-factor normalization can absorb this only if dispersion is estimated stably, which is hard when one of the three samples is a 3× outlier low.

**(c) Six S4 genes tied at padj = 6.28e-14.** This is the BH floor pattern — many p-values hitting the multiple-testing correction limit simultaneously, which suggests the paper's R-DESeq2 run had qualitatively different size factors or dispersions than mine. This is a smoking gun that the paper's S4 list is fragile to analysis choices.

### 2.4 What I did NOT do to resolve (2.3)

- Did not install R + Bioconductor + DESeq2 and run the paper's contrast in the actual R stack.
- Did not test alternative design matrices (`~strain+dose+strain:dose` with interaction term, per-contrast pairwise, etc.).
- Did not turn off Cook's outlier refit and re-check.
- Did not apply `lfcShrink` (apeglm or normal) — paper does not specify.
- Did not contact the authors for their R script.

**Any one of these would resolve open question #4.** The audit was Python-first per protocol, so R-DESeq2 was out of scope, but this leaves a real gap in the reproduction story.

## 3. Where the paper is fragile (independent of my reproduction)

### 3.1 n=3 with a 3.3× library-size range is under-powered

The paper reports 53 significant DEGs for S4 (PprSKD sham vs WT sham) at α=0.05 with n=3 per group. Even the paper's own numbers show 6 genes tied at the BH FDR floor. A sensitivity analysis (leave-one-out, alternative reference, alternative dispersion estimator) is not provided. My redo suggests those calls are fragile.

### 3.2 Mechanism claim (direct base-pair binding) rests on non-direct evidence

MAPS pull-down (genome-scale) + EMSA (in vitro, purified) + Northern (co-migration) → all consistent with a PprS:pprM interaction, but none is base-pair-resolved. A CLIP-seq / CLASH / PARE-seq footprint would give direct evidence; none is provided. This is open question #1.

### 3.3 Deinococcus-specificity vs pan-bacterial IR response not separated

The IR-effect gene lists (S6/S7) are dominated by DNA-repair categories that respond to genotoxic stress in essentially every bacterium (recA, recFOR, uvr, ssb). The paper implicitly treats PprS/pprM as a Deinococcus-specific radioresistance axis, but does not separate the Deinococcus-unique signature (Mn-antioxidant loading, DdrABC, PprA) from the pan-bacterial SOS response. Open question #2.

### 3.4 sRNA-target scope is a single edge

The paper reports one sRNA (PprS/Dsr2) → one target (pprM), out of 31 annotated Dsr* sRNAs in the D. radiodurans genome. The reproduction's raw counts include all 31 Dsr* features but the paper never attempts a network-scale analysis. Open question #5.

## 4. Where the audit itself falls short

### 4.1 In-silico coverage: 5/7 (71%), below 80% bar

- Table S1 proteomics: NOT re-analyzed (PXD026633 raw ~tens of GB, would need uicgpu + FragPipe/MaxQuant, ~1-2 days). Documented as compute-envelope blocker, not data-availability blocker.
- Table S2 GO enrichment: NOT re-run (would need PANTHER API or locally cached GAF). Small DEG lists (33-61 genes) with high sensitivity to reference universe.

### 4.2 No R-DESeq2 sanity check on the failing contrasts (repeat)

This is the single most important audit gap. Installing R + DESeq2 on CherryRd or uicgpu and running the same 12 htseq files would either (a) reproduce the paper's numbers and blame PyDeseq2, or (b) fail to reproduce and blame the paper's specific parameterization. Either outcome resolves the S4/S5 mystery. I did not do it because protocol said Python-first, but the protocol is meant to be adapted when the science requires it.

### 4.3 No author contact

The paper's design matrix is not fully specified in Methods. One email to Contreras lab requesting the R script would clarify (a) whether the paper used `~group` pairwise or `~strain+dose+strain:dose` interaction, (b) whether `lfcShrink` was applied, (c) whether any samples were excluded. Not done per protocol.

### 4.4 Trust of published htseq counts (no re-alignment)

I trust the gene IDs in the deposited htseq counts without re-aligning the raw FASTQ to NC_001263/etc. This is the correct choice for a count-level DEG audit but leaves the possibility that the counts themselves have a bug (e.g. reads assigned to the wrong strand or reads over-counting for overlapping features).

## 5. Honest summary

- **Paper's central biological claim (PprS binds pprM):** REPLICATED. High confidence.
- **Paper's IR-response transcriptomic gene lists (S6/S7):** REPLICATED perfectly. High confidence.
- **Paper's genotype-effect gene lists including the pprM sham down-regulation headline (S4/S5):** NOT REPLICATED in this audit. Confidence in the paper's specific S4 numerical claims is LOW pending R-DESeq2 check.
- **Paper's mechanism claim of direct base-pairing:** not directly supported by any base-pair-resolved assay; MAPS + EMSA + Northern are all indirect.
- **Reproduction coverage:** 5/7 in-silico units (71%), below the 80% bar.

**Overall: PARTIAL, with the queue tag of REPLICATED being incorrect for this slot.** The correct action is (a) fix the queue tag, (b) run R-DESeq2 as open question #4 next steps, (c) note the mechanism gap (open question #1) as a limitation of the paper independent of the reproduction, (d) do NOT propagate the pprM sham down-regulation headline padj without a caveat.
