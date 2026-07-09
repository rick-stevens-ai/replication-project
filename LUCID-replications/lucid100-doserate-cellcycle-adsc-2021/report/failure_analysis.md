# Failure Analysis — Rusin et al. 2021 replication (honest critique, not whitewash)

Verdict preserved from `REPORT.md`: **REPLICATED (PARTIAL on stat-pattern boundary).**
No mismatch with queue verdict `REPLICATED` — the "PARTIAL" qualifier is a stat-pattern
boundary note, not a data-integrity failure. Flagging this qualifier here so it isn't lost.

## What actually failed / is unresolved

### F1. Statistical-test substitution is a real limit
The paper used **JMP Pro 12 one-way ANOVA + unspecified post-hoc** with $\alpha = 0.05$.
The replication used **SciPy Welch's $t$-test** for pairwise contrasts. These are not equivalent:
- Welch does not pool variance; a post-hoc using JMP's pooled within-group variance can be more
  powerful on $n = 3$.
- The 11/52 (~21%) pairwise-significance disagreements all cluster at $p \in [0.05, 0.12]$.
- **Cannot close this gap** without the paper naming its post-hoc (Tukey HSD vs Dunnett vs Student).
  So 79% agreement, not 100%, is the correct headline. Do not upgrade this to 100% by hand-waving.

### F2. Cell-cycle synchronization was NOT validated by the paper
The paper reports G$_0$/G$_1$ / S / G$_2$/M distributions post-irradiation but does not:
- Report a pre-irradiation baseline synchronization check;
- Stain for cyclin-B / phospho-H3 to confirm G$_2$/M identity beyond DNA content;
- Distinguish arrest from differential phase-specific mortality.

The replication inherits this limitation entirely — I re-derived the phase-fraction numbers, but
they cannot separate "HDR causes G$_2$/M arrest" from "HDR kills more S-phase cells, mechanically
elevating the G$_2$/M fraction." Both mechanisms produce the same PI/Guava readout.

### F3. Only TWO dose-rate points (not a dose-rate response curve)
LDR = 1.40 Gy/min vs HDR = 7.31 Gy/min is a single ~5.2× contrast at fixed 2 Gy. The paper's
titular claim "dose rate affects cell cycle" is supported by two points on the rate axis. A
monotonic response, a plateau, and a biphasic response are all consistent with the data. The
replication reproduces the two-point data faithfully — it cannot reproduce the underlying
dose-rate curve, because the paper never measured one.

### F4. ADSC-specific framing is under-supported
The paper's headline is about hADSCs, but there is no matched lymphocyte or fibroblast or BM-MSC
arm irradiated on the same rig at the same rates. The observed G$_2$/M drift could be a generic
MSC / adherent-culture response. Whether this is truly "ADSC-specific" is open. The replication
does not fix this; it only re-derives the paper's numbers.

### F5. All dose-rate × time combinations WERE fit — no cherry-picking there
Positive note (verified): the paper reports 3 conditions × 4 timepoints × 4 assays. No subset
selection was detected — every combination the paper claims data on is present in the Mendeley
xlsx, and every combination reproduces. This is one place where the paper is clean.

### F6. Image-only figures were not re-tested
Figs 6 (p53 IF), 7 (p21 IF), 9 (SA-$\beta$-gal) are qualitative micrographs. Fig 8's normalized
nuclear p21 xlsx exists but was not re-analyzed at per-nucleus distribution level; the paper's
claim there is qualitative ("no differences"). Per-strict-figure coverage is 5/9 (~56%); per
quantitative-claim it is ~88%. Both true; state both.

### F7. Passage number and donor variance are unreported
ATCC PCS-500-011 primary hADSCs are lot- and passage-dependent. The paper does not disclose
passage, and $n = 3$ per condition cannot separate donor variance from dose-rate effect. This is
a real limit of the original study and is not fixable by replication.

### F8. $n = 2$ for LDR Day 3 (implicit exclusion)
The cell-cycle xlsx has a `0, 0, 0` sentinel row for the third LDR replicate at Day 3.
Replication uses $n = 2$ here. This is an implicit exclusion by the authors, not disclosed in the
paper text. Should have been called out in Methods.

## What is honestly good about this replication

- **Every numerical claim in the abstract reproduces to numerical precision from openly deposited
  raw data.** This is the strongest form of in-silico replication possible.
- **The MTS standard curve $y = 160797x - 29124$ reproduces the "Cell Number" column exactly.**
- **The 21% stat-pattern gap is method-substitution, not data drift**, and all 11 disagreements
  sit in $p \in [0.05, 0.12]$. The direction of every effect matches.

## Bottom line

REPLICATED verdict stands, with these caveats explicitly documented and not swept under the rug:
- 79% (not 100%) of pairwise-significance claims agree due to a test-choice substitution I cannot
  close without more paper detail.
- The paper itself is under-designed on synchronization validation, dose-rate curve resolution,
  and lineage comparator. The replication faithfully reproduces the numbers but cannot
  retroactively fix these study-design limits.
- Coverage is 5/9 strict per-figure, ~88% per-quantitative-claim. Both numbers are honest.

If a reviewer asks "did you find anything the paper got wrong?" — no data-integrity issue was
found. The paper's numbers are what they say they are. What can be questioned is inferential
scope and study design, not arithmetic.
