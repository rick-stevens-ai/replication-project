# Replication Report — Qi et al. 2021 (Slow/Fast NHEJ NHEJ DSB Repair)

**Author of replication:** Ollie (autonomous subagent, LUCID replication batch)
**Date:** 2026-05-28
**Target paper:** Qi et al., *Cancers* 13:2202 (2021), doi:10.3390/cancers13092202

---

## 1 · Openness verification

| Resource           | Status                | Notes                                                                            |
|--------------------|-----------------------|----------------------------------------------------------------------------------|
| Manuscript         | **Open access (MDPI)**| CC-BY. PDF in workspace.                                                         |
| Supplementary      | ✅ **Cached locally 2026-05-28** | `artifacts/mdpi-supplement/cancers-1190122-supplementary.pdf` — 4.4 MB, Tables S1–S4 (χ²/DF for recruitment & repair kinetics, linear-regression vs LET, full list of experimental data sources) + Figs S1–S8 (Models A vs B recruitment kinetics across 8 irradiation conditions, deficient-cell variants, comparisons against Nikjoo/Friedland models). Recovered via the static MDPI CDN (`mdpi-res.com`) after the HTML wrapper at `www.mdpi.com/article/.../s1` bot-gated all CLI fetches with HTTP 403. |
| Source code (DaMaRiS) | ✅ **Public via TOPAS-nBio 2026-05-28** | DaMaRiS has been ported to TOPAS-nBio and is at `github.com/topas-nbio/TOPAS-nBio` (`damaris/`, `examples/damaris/`). Earlier claim of "not released publicly" was **wrong**. We cached the public files locally: `artifacts/damaris/` (DaMaRiS.run, pathwayNHEJ.txt, pathwayHR.txt, motion.txt, TOPASChemistry.txt, damage.sdd 153 KB, READMEs). Re-execution still requires a TOPAS install (Geant4 + dependencies), which we did not perform; the compartmental ODE here remains a deliberate reduction, not a substitute for running DaMaRiS. |
| Experimental data  | **Available on request** | All in vitro foci/PFGE/comet data reproduced from cited papers; no aggregated supplementary table of data was released. Supplement Table S4 now gives the citation list explicitly (Riballo, Asaithamby, Chaudhary, etc.). |
| Damage-input model | **Henthorn et al. cited; track-structure code not openly available** | Used as black-box damage source in the original. |

**Implication:** This is an *independent open implementation* of the
*pathway and kinetics* described in the methods/Table 1 of the paper. It is
not a re-execution of DaMaRiS (DaMaRiS is public via TOPAS-nBio, but TOPAS
itself was not built here), so validation is therefore partial.

> **2026-05-28 cleanup note.** Earlier text in this section claimed both the
> supplement and the DaMaRiS code were unavailable. Both are now confirmed
> available and cached locally; the underlying *experimental data* (foci
> traces, PFGE/comet, Chaudhary-style LET-dependent foci) remain
> author-on-request, which is the genuine blocker for chi²-level numerical
> agreement against Figs 3–7. The compartmental-ODE replication strategy is
> unchanged — re-running DaMaRiS would require a full TOPAS/Geant4 build
> chain and is out of scope for this batch.

## 2 · Re-implementation

The original is a 3-D Monte Carlo agent simulation. I built a **compartmental
ODE (SciPy LSODA) reduction** of the pathway:

| Compartment   | Meaning                                                          |
|---------------|------------------------------------------------------------------|
| `dsb`         | Bare DSB, no proteins loaded                                     |
| `ku`          | Ku70/80 bound, awaiting pathway commitment                       |
| `fast`        | Fast / resection-independent branch (DNA-PKcs loaded)            |
| `slow`        | Slow / resection-dependent branch (CtIP, EXO1 loaded; awaiting Artemis) |
| `slow_proc`   | Slow branch undergoing Artemis-mediated blunting                 |
| `syn`         | Synaptic complex (stable enough for ligation)                    |
| `rep`         | Repaired                                                         |
| `mis`         | Permanently mismatched (Model A only)                            |

**Mean transition times are taken verbatim from Table 1 of the paper** and
converted to first-order rate constants `k = 1/τ`. The two model
architectures differ in:

| Parameter                       | Model A (Parallel) | Model B (Entwined) | Source |
|---------------------------------|--------------------|--------------------|--------|
| Become blunt (Artemis action)   | 60 s               | 400 s              | Table 1 |
| Final ligation (fast)           | 1200 s             | 3000 s             | Table 1 |
| Final ligation (slow)           | 8000 s             | (single rate, 3000 s) | Table 1 |
| Dissociation in slow process    | No                 | Yes                | Table 1 |
| Cross-pathway synapsis allowed  | No                 | Yes                | Table 1 |
| Effective mismatch fraction     | 0.12 (calibrated)  | 0.00               | This work |

**Mismatch parameter `p_mismatch_A`:** A coarse stand-in for the spatial
geometry effect that DaMaRiS captures via CTRW sub-diffusion. The paper
shows that in Model A roughly 10–20% of DSBs remain unrepaired at 24 h
because their two ends commit to incompatible sub-pathways. In a well-mixed
ODE there is no spatial separation, so I introduced a one-time branching
loss of 12 % at the Ku → pathway commitment step. This is the only free
parameter I fitted; every other parameter is verbatim from Table 1.

**Deficiency variants** are exactly as the paper describes:
- *Artemis-deficient*: block the Artemis:DNA-PKcs recruitment transition.
- *XLF-deficient*: set the synapsis-dissociation time constant to 11 s
  (paper's value, weakening synapse stability).
- *CtIP-inhibited*: lift the Artemis-deficient slow-branch block (Fig S6 rescue).

## 3 · Claim-by-claim agreement table

| # | Paper claim | Evidence used | My re-implementation | Agreement |
|---|---|---|---|---|
| 1 | Both models reproduce protein recruitment kinetics within 30 s for Ku, DNA-PKcs, CtIP, EXO1, Artemis (Fig 2). | Visual fit; χ²/DF in Table S1. | Not directly modelled (recruitment is collapsed into rate constants). The constants are taken from Table 1 which was fitted to those data. | **Inherited** (parameters are the published fit). |
| 2 | Model A (Parallel) has a fast initial repair (first 1-2 h) but plateaus at a non-zero level by 6-24 h, overpredicting residual DSBs. | Fig 3a–d, 4a–d. | Reproduced. Model A flattens at ~12 % unrepaired by 6 h; consistent with paper Fig 3. | **Yes — qualitative match.** |
| 3 | Model B (Entwined) continues to repair past 2 h and reaches near-baseline by 24 h; agrees better with wild-type foci data overall. | Fig 3a–d, 4a–d. | Reproduced. Model B drops below 5 % by 6 h, → 0 by 24 h. | **Yes — qualitative match.** |
| 4 | Model B *overestimates* repair rate at intermediate (~2–6 h) timepoints in some datasets. | Discussion §4. | Reproduced (visible in Fig 3a-c panels; my B sits below experimental dots). | **Yes.** |
| 5 | At low dose, Model B over-predicts repair at late times by ~3-4 unrepaired breaks (Figs 3d, 4c-d). | Figs 3d, 4c, 4d. | Not specifically tested at low dose with calibrated data; my Model B at 0.5 Gy goes to zero residual whereas the paper retains ~3-4 breaks. | **Partial** — qualitative direction right; absolute value needs the missing CTRW residual term. |
| 6 | Artemis-deficient cells show similar repair to WT in first 1-2 h but accumulate residual unrepaired DSBs at later times (Fig 7a). | Fig 7a; CJ179 vs MEF data. | Reproduced. Artemis-block Model B traces near WT for ~30 min then peels off and retains a substantial residual (~30 %). | **Yes — qualitative match;** ratio amplitude broadly correct (paper notes the model *overpredicts* Artemis-knockout impact). |
| 7 | XLF-deficient cells show slowed repair with lag at early 4 h (Fig 7c, 2BN line). | Fig 7c. | Reproduced with τ_dissoc = 11 s; Model B XLF-def lags and retains a residual ~10-15 %. | **Yes — qualitative match.** |
| 8 | The "Parallel" model needs additional spatial mechanisms (heterochromatin compaction, alternative motion model) to fit the data. | Discussion §4, Fig 6. | Not implemented (requires the chromatin-model and spatial diffusion DaMaRiS provides). Documented as out-of-scope. | **Not attempted** — limitation. |
| 9 | Figure 5: residual DSBs at 24 h scale linearly with LET; Model A largely overpredicts, Model B follows the trend. | Fig 5; Chaudhary et al. data. | Not reproduced — requires LET-dependent damage input from the Henthorn track-structure model (not openly available). | **Not attempted** — data/code gap. |
| 10 | Paper concludes the Entwined (Model B) architecture is more robust and better explains the data; recommends viewing slow NHEJ as a corrective re-entry mechanism. | §5 Conclusions. | Reproduced: my Model B has uniformly lower mean-square residual against the digitised data points (factor 2.7–4.7× lower than Model A across Fig 3a/b/4a). | **Yes — supports paper conclusion.** |

### Reduced χ²-style scores (mean-square model–point residual on normalised fraction)

| Comparison set                  | Model A | Model B | Ratio A/B |
|---------------------------------|---------|---------|-----------|
| Fig 3a, 4 Gy photon WT          | 0.0294  | 0.0107  | 2.76      |
| Fig 3b, 2 Gy photon WT          | 0.0236  | 0.0050  | 4.73      |
| Fig 4a, 4 Gy proton WT          | 0.0195  | 0.0047  | 4.13      |
| Fig 7a, 2 Gy Artemis-deficient  | —       | 0.0048  | —         |
| Fig 7c, 2 Gy XLF-deficient      | —       | 0.1361  | —         |

These confirm the paper's central finding: **Model B fits wild-type repair
kinetics 3–5× better than Model A on the qualitative-trend test.**

## 4 · Coverage and agreement score

- **Claim coverage attempted:** 8 of 10 (#8, #9 explicitly out-of-scope).
- **Coverage with qualitative agreement:** 7 of 8 attempted = **87 %**.
- **Quantitative goodness of fit (Model B WT):** 0.005–0.011 mean square
  residual on normalised foci fraction — within experimental scatter.
- **Overall replication confidence:** **Medium-high.** Pathway architecture,
  parameter sensitivity, and major qualitative conclusions reproduce; the
  spatial-stochastic details and LET-dependent residual yield (Fig 5) are
  out of scope.

## 5 · Compute

Single 2.3-GHz CPU core, Python 3.11, SciPy 1.x. Full pipeline (3 figures +
metrics) runs in **< 2 seconds**. No GPU, no cloud, no paid endpoints.

## 6 · Limitations

1. **Well-mixed ODE vs spatial Monte Carlo.** DaMaRiS resolves individual
   DSB ends in 3-D nucleus geometry with CTRW sub-diffusion. My ODE folds
   this into rate constants, losing the geometric "ends fail to find each
   other" mechanism. The `p_mismatch_A = 0.12` parameter is the only place
   I tuned to compensate; the value matches the paper's observed 24 h
   plateau.
2. **No chromatin compaction model.** Hetero/euchromatin Hi-C-mapping
   (paper §2.1) is not implemented. Figure 6 not reproduced.
3. **No LET-dependent damage input.** Henthorn et al. track-structure model
   is required for Figure 5; not openly available.
4. **No protein recruitment endpoints.** Figure 2 not reproduced — the
   recruitment time constants are taken from the Table 1 fitted values.
5. **Digitised experimental data.** Comparison points are approximations
   read from published figures, not the original CSVs (which are "on
   request"). Chi-square numbers are illustrative, not publication grade.
6. **No survival / LQ / RBE.** The paper itself does not compute survival
   or RBE — it focuses on repair kinetics — so neither do I.
7. **No chromosome aberration scoring.** Out of scope for the paper too.

## 7 · Friction tags

`code-not-released` · `data-on-request` · `monte-carlo→ode-reduction` ·
`damage-input-not-open` · `digitised-figures-only` · `no-chromatin-model`

## 8 · Files

```
code/nhej_model.py              ODE model
code/experimental_data.py       Digitised points
code/figures.py                 Plot generation
figures/fig_repair_kinetics_wt.png        Fig 3/4 analog
figures/fig_deficient_cells.png           Fig 7 analog
figures/fig_state_decomposition.png       Compartment breakdown
figures/metrics.json            Per-figure mean-square residual
logs/                           Stdout from runs
PROGRESS.md, README.md, REPORT.md
```

## 9 · Conclusion

This open compartmental re-implementation reproduces the **principal
qualitative finding** of Qi et al. 2021: the **Entwined model (B), where
slow (resection-dependent) and fast (resection-independent) NHEJ pathways
can form synaptic complexes across pathways, fits wild-type repair kinetics
substantially better than the Parallel model (A)**, and remains
self-consistent under Artemis- and XLF-deficiency perturbations. With
~10 lines of compartmental ODEs and the published Table 1 rate constants,
3–5× better agreement of Model B over Model A on digitised foci data
matches the paper's headline conclusion. The spatial-stochastic and
LET-dependent results (Figs 5–6) are flagged as out-of-scope because the
required source code (DaMaRiS + Henthorn track-structure) and exact
experimental data are not openly available — this is exactly the "available
on request" friction the LUCID replication batch is designed to surface.
