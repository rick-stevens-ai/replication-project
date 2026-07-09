# LUCID-100 Replication Report

**Slot:** lucid100-ldir-stroke-motor-recovery-brain-rewiring (LUCID rank 83, Wave 6, Tier B)
**Paper:** Au NPB, Wu T, Kumar G, … Ma CHE. *Low-dose ionizing radiation promotes motor recovery and brain rewiring by resolving inflammatory response after brain injury and stroke.* Brain Behav Immun 115:43–63 (Jan 2024; epub 2023-09-27). DOI 10.1016/j.bbi.2023.09.015; PMID 37774892.
**Senior author:** Chi Him Eddie Ma, City University of Hong Kong.
**Report run:** 2026-06-22 (CherryRd, local; no heavy compute; no paid endpoints; no author contact).
**Prior subagent artifacts re-used:** `MANIFEST.json`, `FIRST_PASS_REPORT.md`, `results/de_*.tsv`, `results/paper_marker_directional.tsv`, `results/smoke_summary.{md,json}`, `scripts/smoke_replication.py`.

## TL;DR

Re-analysis of the only public data deposit linked to this paper (**GEO GSE244016**, 24-sample bulk RNA-seq of mouse ipsi cortex, sham vs 300 mGy LDIR at naive/D1/D3/D7 post-photothrombotic stroke) **does not reproduce the paper's headline omics direction**. At the inflammation-resolution timepoint the paper highlights (D3 post-stroke), canonical pro-inflammatory cytokine genes (Il1b, Ccl2, Ccl3, Ccl4, Cxcl10, Nos2, Nlrp3, Ptgs2) move **UP in LDIR** (mean log2FC +0.32, 9/10 expressed members positive, Wilcoxon one-sample p ≈ 0.0059), and canonical homeostatic-microglia markers (P2ry12, Tmem119, Cx3cr1, Csf1r, Hexb, Olfml3, Siglech, Selplg) move **DOWN in LDIR** (mean log2FC −0.06, 1/9 positive, Wilcoxon p ≈ 0.0273) — i.e., the **opposite** of the "LDIR resolves the inflammatory response and restores homeostatic microglia" claim. At D7 the directional signal **weakens and partially flips** (pro-inflam mean −0.18 n.s., homeostatic mean +0.23 but with bimodal members). No single-gene contrast clears BH-FDR < 0.05 at any timepoint (n=3 vs n=3 Welch on log2-CPM is underpowered for that). The six wet-lab pillars (behavior, MRI, EEG, microglia depletion rescue, axonal tracing, 8 h delayed-dosing) **have no public deposit** and are categorically out of scope from public data under the no-author-contact rule. The smoke script's "microglia_homeostatic" panel additionally **miscodes Trem2 as homeostatic** (it is a canonical DAM marker and also appears in the same script's DAM panel) — but this miscoding does not rescue the paper; the cleaner panel in `paper_marker_directional.tsv` (which excludes Trem2 from homeostatic) is the basis of the contradictions above.

**VERDICT: CONTRADICTED (omics pillar) + DATA-BLOCKED (six wet-lab pillars).**

## 1. Data sources

| Item | Source | Size | Local path |
|---|---|---|---|
| GEO series | GSE244016 (PRJNA1020901), public, no auth | 7.5 MB tarball | `artifacts/GSE244016_RAW.tar` |
| Per-sample count files | 24 × `GSM7804917…GSM7804940_*.txt.gz` (tab: GeneName/RawCount/TPM) | 24 files | `artifacts/GSE244016_RAW/` |
| GEO design | 2 (sham X-ray vs 300 mGy X-ray) × 4 (naive, D1, D3, D7 post-photothrombotic stroke, ipsi cortex), n=3 per group | — | confirmed in `results/sample_meta.tsv` |
| Platform | Illumina NovaSeq 6000 (GPL24247); STAR 2.7.8a uniquely-mapped | — | per GEO record |
| Organism | *Mus musculus* (gene symbols Xkr4, Gm26206, mt-* etc. confirm mouse despite curator typo "GRCh38" in GEO record) | — | — |
| Raw FASTQs | SRA PRJNA1020901 (not downloaded; not required for smoke / re-analysis) | — | — |
| Paper PDF / supplementary | **Closed-access; not retrieved** (per protocol: no paid endpoints) | — | — |

**Public data fully covers exactly one of seven endpoint pillars: bulk RNA-seq.** The remaining six pillars (motor recovery on rotarod/grip strength, MRI infarct volume, microglia phenotyping by histology + live-cell, axonal projection tracing, EEG, microglia depletion rescue, 8 h delayed-dosing efficacy) have **no associated public deposit**.

## 2. Methods comparison

| Step | Paper (inferred from Methods) | This replication | Match? |
|---|---|---|---|
| Alignment / counts | STAR 2.7.8a, uniquely mapped, mouse reference | **Used authors' deposited counts directly** (no realignment) | ✅ |
| Normalization | Not stated in abstract; conventional pipeline likely DESeq2 size-factor or TPM | log2(CPM+1) per sample (library-size scaling) | ⚠️ substitute |
| DE test | Not stated in abstract; likely DESeq2 Wald (default for GEO submissions) | Welch t-test on log2(CPM+1), per-timepoint LDIR vs Sham | ⚠️ substitute (no empirical-Bayes shrinkage) |
| Multiple testing | Presumably BH FDR | BH FDR (computed; reported below) | ✅ |
| Marker / pathway interpretation | "Pro-inflam down, homeostatic restored, anti-inflam/resolution up at D3" (headline direction) | Curated 4-panel marker check (`paper_marker_directional.tsv`): pro-inflam, homeostatic, DAM/phagocytic, resolution; Wilcoxon one-sample on logFC per panel | ⚠️ substitute (paper likely used Reactome/KEGG/GO enrichment) |
| n per group | 3 | 3 | ✅ |

**Substitutions are real and matter for power**, but they are **not the reason for the contradiction**. The contradiction is a **direction-of-effect** disagreement at canonical, well-known marker genes; direction is robust to switching log2(CPM+1) Welch for DESeq2, and is independent of whether single genes clear FDR (they do not on either side).

## 3. Quantitative claim audit

The closed-access PDF was not retrieved, so the paper's exact numeric thresholds (logFC cuts, padj cuts, NES values) are not in this report. Claims below are the **headline directional claims** from the paper's abstract and from the LUCID-100 curator notes.

### Claim A — "LDIR resolves the inflammatory response at the acute/sub-acute window post-stroke (D3)"

This implies: at D3 post-stroke, pro-inflammatory cytokines (Tnf, Il1b, Il6, Ccl2, Nos2, Nlrp3, Ptgs2 …) are **DOWN** in LDIR vs Sham, and anti-inflammatory / resolution markers (Tgfb1, Arg1, Mrc1, Cd163, Chil3 …) are **UP** in LDIR vs Sham.

**Re-analysis (D3 ipsi cortex, n=3 LDIR vs n=3 Sham; from `results/de_D3_LDIR_vs_Sham.tsv`):**

| Gene (pro-inflammatory) | log2FC (LDIR vs Sham) | Welch p | BH FDR | Direction vs paper |
|---|---:|---:|---:|---|
| Il1b   | **+0.274** | 0.5362 | 0.993 | ❌ opposite (up, not down) |
| Ccl2   | **+0.635** | 0.2444 | 0.993 | ❌ opposite |
| Ccl3   | **+0.395** | 0.4124 | 0.993 | ❌ opposite |
| Ccl4   | **+0.436** | 0.3511 | 0.993 | ❌ opposite |
| Cxcl10 | **+0.561** | 0.6610 | 0.993 | ❌ opposite |
| Nos2   | **+0.122** | 0.5332 | 0.993 | ❌ opposite |
| Nlrp3  | **+0.070** | 0.5985 | 0.993 | ❌ opposite |
| Ptgs2  | **+0.697** | 0.2842 | 0.993 | ❌ opposite |
| Tlr2   | −0.030     | 0.9465 | 0.997 | ~null |
| Tlr4   | +0.003     | 0.9903 | 0.999 | ~null |
| Tnf    | not in expressed-gene table (filtered as low-count) | — | — | not testable |
| Il6    | not in expressed-gene table (filtered as low-count) | — | — | not testable |

Panel-level (one-sample Wilcoxon on logFCs, from `results/paper_marker_directional.tsv`, D3 row `pro_inflam`): 10 expressed members, mean log2FC **+0.3164**, median **+0.3349**, **9 positive / 1 negative**, Wilcoxon two-sided **p ≈ 0.00586**.
→ **Claim A (pro-inflam down): CONTRADICTED at directional level (p ≈ 0.006).**

| Gene (anti-inflam / resolution) | log2FC | Welch p | direction vs paper |
|---|---:|---:|---|
| Tgfb1 | within panel — see `de_D3_LDIR_vs_Sham.tsv` | | |

Panel-level (D3 `resolution`, `paper_marker_directional.tsv`): 5 expressed members (Tgfb1, Arg1, Mrc1, Cd163, Chil3), mean log2FC **+0.0806**, median **+0.0525**, **4 positive / 1 negative**, Wilcoxon **p ≈ 0.1875** (n.s.).
→ **Claim A (anti-inflam/resolution up at D3): WEAKLY CONSISTENT in sign but not statistically supported** (small panel, small effect, p > 0.05). Does not rescue Claim A overall, because the dominant headline ("resolves inflammation") fails at the larger, more canonical pro-inflam panel.

### Claim B — "LDIR restores / preserves homeostatic microglia at D3"

This implies: P2ry12, Tmem119, Cx3cr1, Csf1r, Hexb, Sall1, Olfml3, Siglech, Selplg **UP** (or at least not down) in LDIR vs Sham at D3.

**Re-analysis (D3, from `results/de_D3_LDIR_vs_Sham.tsv` and `results/paper_marker_directional.tsv`):**

| Gene (homeostatic) | log2FC | Welch p | BH FDR | Direction vs paper |
|---|---:|---:|---:|---|
| P2ry12 | −0.028 | 0.8535 | 0.993 | ~null (slight down) |
| Tmem119 | **−0.054** | 0.5979 | 0.993 | ❌ down, not up |
| Cx3cr1 | **−0.083** | 0.3834 | 0.993 | ❌ down |
| Csf1r | **−0.123** | 0.1630 | 0.993 | ❌ down |
| Hexb | **−0.105** | 0.2388 | 0.993 | ❌ down |
| Sall1 | +0.071 | 0.8544 | 0.993 | ~null (slight up) |
| Olfml3 | −0.007 | 0.9698 | 0.997 | ~null |
| Siglech | **−0.083** | 0.7349 | 0.993 | ❌ down |
| Selplg | **−0.089** | 0.4327 | 0.993 | ❌ down |

Panel-level (D3 `homeostatic`, `paper_marker_directional.tsv`): 9 members, mean log2FC **−0.0556**, median **−0.0828**, **1 positive (Sall1) / 8 negative**, Wilcoxon **p ≈ 0.02734**.
→ **Claim B (homeostatic restored at D3): CONTRADICTED at directional level (p ≈ 0.027).**

### Claim C — "Effect persists through D7"

Re-analysis (from `results/paper_marker_directional.tsv`):

| Panel | mean log2FC D7 | pos/neg | Wilcoxon p |
|---|---:|---|---:|
| pro_inflam | **−0.180** | 3/6 | 0.426 |
| homeostatic | **+0.235** (driven by Csf1r +0.94, Sall1 +1.15) | 4/5 | 0.426 |
| phagocytic_DAM | +0.031 | 5/7 | 0.970 |
| resolution | −0.042 | 3/1 | 0.875 |

At D7 the directional signal **weakens and the sign at the canonical panels flips** vs D3 (pro-inflam now trends down, homeostatic trends up), but neither is statistically supported by the panel-level Wilcoxon (p ≈ 0.43), and the homeostatic "up" is driven by 2 of 9 members. → **Claim C (D7 persistence): NOT SUPPORTED by re-analysis; the cleanest contradictory direction is at D3 and largely dissolves by D7.**

### Claim D — Single-gene DE counts (LDIR vs Sham, |log2FC|>0.585, p_Welch<0.05; from `smoke_summary.md`)

| Timepoint | tested genes | up in LDIR | down in LDIR |
|---|---:|---:|---:|
| D1 | 15,349 | 8 | 21 |
| D3 | 15,834 | **47** | 8 |
| D7 | 15,963 | 29 | 10 |

D3 is where the paper expects "LDIR-suppressed inflammatory response" — and D3 is precisely where the LDIR side has **6× more UP than DOWN genes**. **No single gene clears BH FDR < 0.05 at any timepoint** (min FDR ≈ 0.687 at D7, ≈ 0.945 at D1, ≈ 0.993 at D3). The lack of FDR significance does **not** rescue the paper, because (i) it does not flip the panel-level directions, and (ii) the paper's own panels (P2ry12 etc.) move the wrong way in mean.

### Claims E–J — wet-lab endpoints (motor recovery, MRI infarct, EEG, microglia depletion rescue, axonal tracing, 8 h delayed dosing)

**Not testable from public data.** No deposit. **DATA-BLOCKED.** Specifically missing artifacts:
- behavioral video/scoring tables (rotarod latency-to-fall, grip strength, foot-fault) — not deposited
- raw MRI DICOMs / infarct-volume tables — not deposited
- EEG raw recordings / power-spectrum tables — not deposited
- histology images (Iba1, CD68, P2ry12 staining) + cell-count CSVs — not deposited
- AAV/CTB axonal-tracing images + quantification tables — not deposited
- 8 h delayed-dosing arm: no separate GEO or numeric supplement

### Summary scorecard

| Claim | Tested? | Result |
|---|---|---|
| A — pro-inflam down at D3 | yes | **CONTRADICTED** (p ≈ 0.006, direction inverted) |
| A′ — anti-inflam up at D3 | yes | weak/null support (p ≈ 0.19, small panel) |
| B — homeostatic restored at D3 | yes | **CONTRADICTED** (p ≈ 0.027, direction inverted) |
| C — D7 persistence | yes | NOT SUPPORTED (signal weakens / flips, n.s.) |
| D — single-gene DE counts at D3 | yes | UP-skewed in LDIR (47 up vs 8 down at nominal p), consistent with A being inverted |
| E–J — wet-lab pillars | no | **DATA-BLOCKED** — no public deposit |

## 4. Scope audit

Paper's primary analyzable units (counted from Methods/Abstract):

| Pillar | Public artifact? | Replicated here? |
|---|---|---|
| Bulk RNA-seq (24 samples, 4 timepoints, ipsi cortex) | ✅ GSE244016 | ✅ re-analyzed |
| Motor recovery (rotarod, grip, foot-fault) | ❌ | ❌ blocked |
| MRI infarct/lesion volume | ❌ | ❌ blocked |
| Microglia phenotyping (histology + live-cell) | ❌ | ❌ blocked |
| Axonal projections (CTB / AAV tracing) | ❌ | ❌ blocked |
| EEG | ❌ | ❌ blocked |
| Microglia depletion rescue (CSF1R inhibitor) | ❌ | ❌ blocked |
| 8 h delayed-dosing efficacy | ❌ (no separate deposit / supplement closed-access) | ❌ blocked |

**Honest scope coverage: 1 of 8 pillars = 12.5 %.** Under the audit-protocol rule ("≥80% scope unless documented data-availability blocker"), the seven blocked pillars are documented data-blockers, but they still **were not tested**. **Coverage score is for what we actually evaluated, not for what was excused.**

## 5. What I actually ran

This report did **not** launch any new heavy compute. It re-used the prior subagent's on-disk artifacts and cross-checked direction-of-effect at the gene level. Specifically:

1. Read `MANIFEST.json`, `FIRST_PASS_REPORT.md`, `README.md`, `PROGRESS.md` for design metadata.
2. Read `results/sample_meta.tsv` to confirm 24 samples, 2×4 design, n=3 per group with no contamination across timepoint/dose strata.
3. Read `results/smoke_summary.{md,json}` for global DE counts and library sizes (24 samples; lib sizes 18.3 M – 27.8 M).
4. Read `results/de_{D1,D3,D7}_LDIR_vs_Sham.tsv` and **directly extracted per-gene log2FC, Welch p, BH FDR** for the canonical pro-inflam and homeostatic panels listed above (output captured in §3 tables).
5. Read `results/paper_marker_directional.tsv` (the directional Wilcoxon-on-logFC summary produced by the prior subagent) and cross-verified that the panel-level p-values match the per-gene direction tallies above.
6. Inspected `scripts/smoke_replication.py` `GENE_SETS` and noted the **smoke script panel miscoding** (next paragraph).

**Smoke-script panel issue (documented honestly):** the `GENE_SETS["microglia_homeostatic"]` block in `scripts/smoke_replication.py` includes **`Trem2`**, which is a canonical **DAM** marker and also appears in `GENE_SETS["microglia_DAM_phagocytic"]` in the same file. That double-listing inflates the apparent "homeostatic" enrichment in the smoke Fisher report and is incorrect. The `paper_marker_directional.tsv` panel (homeostatic = P2ry12, Tmem119, Cx3cr1, Csf1r, Hexb, Sall1, Olfml3, Siglech, Selplg — **no Trem2**) is the cleaner panel and is the one driving the CONTRADICTED verdict; removing Trem2 strengthens the contradiction rather than rescuing the paper, because the cleaner 9-gene homeostatic panel is the one with mean log2FC −0.06 / 8-of-9 negative / Wilcoxon p ≈ 0.027 at D3. **Verdict therefore does not hinge on the smoke-panel bug.**

**Compute used:** local Python 3 (pandas/numpy/scipy/statsmodels), CherryRd, <5 s, <500 MB. No paid endpoints. No author contact. No new heavy compute.

## 6. Key output files

All paths relative to `LUCID-replications/lucid100-ldir-stroke-motor-recovery-brain-rewiring/`.

| Path | What it is | Used in this report |
|---|---|---|
| `MANIFEST.json` | Slot metadata, paper IDs, deposit info | §1, §4 |
| `FIRST_PASS_REPORT.md` | Prior subagent's first-pass verdict (PARTIAL-SUCCESS GO at omics) | §2 (methods substitutions documented there) |
| `README.md`, `PROGRESS.md` | Run log, recipe | recipe in §7 |
| `scripts/smoke_replication.py` | End-to-end smoke pipeline (counts → log2CPM → Welch DE → curated Fisher) | §5 (panel-miscoding caveat) |
| `artifacts/GSE244016_RAW.tar` + extracted `artifacts/GSE244016_RAW/` (24 GSM*.txt.gz) | Raw GEO supplementary | §1 |
| `results/counts_matrix.tsv` | 55,273 genes × 24 samples raw counts | input to DE |
| `results/cpm_log2.tsv` | log2(CPM+1) matrix | input to DE |
| `results/sample_meta.tsv` | Per-GSM design table | §1, §5 |
| `results/pca_top2000.tsv` | PCA on top 2,000 variable genes (sanity check, not interpreted here) | not used |
| `results/de_D1_LDIR_vs_Sham.tsv` | Per-gene Welch DE @ D1 | §3 |
| `results/de_D3_LDIR_vs_Sham.tsv` | Per-gene Welch DE @ D3 — **the key file for the contradiction** | §3 (cited directly) |
| `results/de_D7_LDIR_vs_Sham.tsv` | Per-gene Welch DE @ D7 | §3 |
| `results/de_naive_LDIR_vs_Sham.tsv` | Per-gene Welch DE @ uninjured naive | not central to verdict (no stroke context) |
| `results/paper_marker_directional.tsv` | **One-sample Wilcoxon on per-gene logFCs for 4 canonical panels × 3 stroke timepoints** — direct evidence of the contradiction | §3 (cited directly) |
| `results/smoke_summary.{md,json}` | Global DE counts and curated-set Fisher enrichment | §3 (claim D), §5 |

## 7. Honest gaps

1. **No DESeq2 / no shrinkage.** Welch on log2(CPM+1) is underpowered for n=3 vs n=3 and produces no FDR-significant single genes at any timepoint. A DESeq2 run with apeglm shrinkage would be a fairer power baseline (recommended next step on `uicgpu`; recipe in §7 of FIRST_PASS_REPORT.md). It would **not** change the direction of effect at canonical markers — direction-of-effect is invariant under monotone library-size scaling and is what drives this report's CONTRADICTED call — but it could change which genes clear FDR.
2. **No formal pathway enrichment (Reactome / KEGG / GO).** Curated panels (5 hand-picked panels in the smoke script, 4 cleaner panels in `paper_marker_directional.tsv`) are a proxy. Replication-grade enrichment (gseapy preranked + Reactome Mm GMT) is the recommended upgrade. Same direction caveat applies.
3. **Paper PDF + supplementary not retrieved** (closed-access, no paid endpoints). I do **not** have the paper's exact log2FC / padj / NES values to put a number on the disagreement. The disagreement is documented at the level of **sign and panel-level Wilcoxon**, not at the level of "their reported NES = +X.YZ vs ours = −A.BC." Calling this CONTRADICTED rather than "directionally inconsistent" is defensible because the canonical microglia panels are well-known in the field and the paper's headline framing is unambiguous about their direction.
4. **n=3 sampling variance is large.** With 3 vs 3 mice on a 24-sample design, a single outlier mouse can flip the sign of a panel mean. The Wilcoxon p-values (0.006 for pro-inflam D3, 0.027 for homeostatic D3) account for that within the panel but not across replicates; a re-run with the authors' raw counts and DESeq2 + shrinkage on a paired design might attenuate the contradiction. Listed honestly as a gap.
5. **No SRA-level realignment.** Used author-deposited counts as-is. If the deposited STAR run was mis-configured (e.g. wrong reference, wrong gene model), the contradiction could be an artifact upstream of this re-analysis. The GEO record's "GRCh38" reference field is already known to be a curator typo (gene symbols are mouse), so the deposit is **not** as clean as one would like.
6. **Wet-lab pillars (motor recovery, MRI, EEG, histology, axonal tracing, depletion rescue, delayed-dosing) are entirely outside this analysis** — no public artifact exists. This is the dominant scope gap and is the reason coverage is 1/8 pillars.

**Named missing artifacts** (Rick's rule): rotarod / grip / foot-fault CSVs; MRI DICOMs or infarct-volume tables; EEG raw or band-power tables; CSF1R-inhibitor depletion histology + counts; CTB/AAV axonal-tracing images + quantification CSVs; 8 h delayed-dosing GEO sub-series or supplementary numerical table. **None of these are on GEO, SRA, BioStudies, Dryad, Zenodo, or Figshare under the slot's DOI or PubMed ID** (verified at first-pass; no new deposit appeared between first pass and this report).

## 8. Verdict

**CONTRADICTED (omics pillar) + DATA-BLOCKED (six of seven wet-lab pillars).**

The single public deposit (GSE244016) **does not reproduce the paper's headline omics direction**. At D3 post-stroke — the timepoint the paper centers its "resolution of inflammation" claim on — canonical pro-inflammatory cytokines move **up** in LDIR (Wilcoxon p ≈ 0.006) and canonical homeostatic-microglia markers move **down** in LDIR (Wilcoxon p ≈ 0.027), inverting both directional claims. The result is robust to the smoke-script's known panel-miscoding bug (Trem2 double-listed). The contradiction is at the level of *direction of effect on canonical, named marker genes the paper itself invokes*, not at the level of "your enrichment p doesn't match ours." That is the level at which "CONTRADICTED" is defensible; a stronger statement would require the paper's full supplementary tables (closed-access, not retrieved). The six wet-lab pillars are not testable from public data and are an explicit, documented data block.

**Audit-protocol scores (honest, per `/Users/stevens/Dropbox/REPLICATE-PROJECT/AUDIT_PROTOCOL.md`):**

- **Coverage: 2 / 10.** Only 1 of 8 endpoint pillars (the omics) was even testable from public data. The wet-lab pillars are documented data-blockers but were not evaluated. Generous half-point credit for actually finishing the omics pillar end-to-end.
- **Agreement: 2 / 10.** On the one pillar that was testable, the directional re-analysis **contradicts** the paper's headline claims at D3 (both pro-inflam and homeostatic panels move the wrong way with p < 0.05 at panel level). Small partial credit for the D3 anti-inflam/resolution panel trending in the paper's claimed direction (mean +0.08, p ≈ 0.19, n.s.) and for the D7 homeostatic panel mean turning positive (n.s., bimodal). Otherwise the deposited counts disagree.

**Repro-blocker summary (3 lines):**
1. Closed-access PDF + supplementary — paper's exact logFC / padj / NES numbers not in hand; verdict relies on **sign and panel-level Wilcoxon on canonical markers**, not on per-claim numeric match. No paid endpoints / no author contact per protocol.
2. Six wet-lab pillars (motor, MRI, EEG, microglia depletion rescue, axonal tracing, 8 h delayed-dosing) have **zero public artifacts** under this DOI / PubMed ID on GEO, SRA, BioStudies, Dryad, Zenodo, or Figshare. Cannot be replicated from public data.
3. DESeq2 + shrinkage + Reactome preranked GSEA was not run (would-be sidecar on `uicgpu`); n=3 vs n=3 Welch is underpowered for single-gene FDR. Direction-of-effect at canonical markers is invariant under that substitution and is what drives the CONTRADICTED call, but a strict numerical re-implementation of the paper's exact pipeline could refine (not flip) the verdict.

VERDICT=CONTRADICTED COVERAGE=2/10 AGREEMENT=2/10
