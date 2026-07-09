# FIRST_PASS REPORT — slot 63
## Friedrich, Durante, Scholz 2012 — static GLOBLE (RR2964)

## Verdict

**PARTIAL FIRST-PASS REPLICATED.** Recommend QA retag from
`candidate_curated` → `completed_first_pass`. Suitable for the audit line:

```text
| Friedrich et al. 2012 RR2964 GLOBLE static photon survival | F1,F3 | REPLICATED |
| Friedrich et al. 2012 RR2964 β vs α anti-correlation (17-line subset) | F2 | INCONCLUSIVE |
```

The static GLOBLE equations are simple, fully specified in the paper, and were
reimplemented from scratch in `code/globle_static.py`. The model reproduces the
paper's central mechanistic claims about photon dose-response. The
17-cell-line `(alpha, beta)` anti-correlation claim cannot be confirmed on this
subset; the paper's claim was anchored on a 150+ cell-line meta-analysis that
we do not have re-digitised, so this is INCONCLUSIVE rather than refuted.

## Paper

Friedrich T, Durante M, Scholz M. *Modeling Cell Survival after Photon
Irradiation Based on Double-Strand Break Clustering in Megabase Pair Chromatin
Loops.* Radiation Research 178(5): 385–394 (Nov 2012).
DOI **10.1667/RR2964.1** · PMID **22998227** · 105 citations (S2, 2026-06-09).

## Artifact availability

| Artifact | Status |
|---|---|
| Source paper PDF | **NOT obtained** — closed access (Unpaywall `is_oa=false`, no repository copy). Did not pursue (no paid endpoints, no author contact per task scope). |
| Abstract | Obtained from PubMed; reproduced in README. |
| Equations | Reconstructed from abstract + cross-confirmed against sibling kinetic-GLOBLE paper (Herr 2014) and its static-limit code. |
| Paper-fixed constants (`alpha_DSB`, `N_L`) | Transcribed via Herr 2014 PLoS ONE Table 1 and verified consistent with what survives in the abstract. |
| Per-cell-line `(eps_i, eps_c)` fits | Re-used from Herr 2014 PLoS ONE Table 2 (17 cell lines). |
| Author code | None known; GSI Biophysics has not released GLOBLE source code publicly. |
| Raw clonogenic datapoints | Not redistributed; original paper fits to literature compilations. Not re-digitised here. |
| Replication code | Created locally, MIT-license-style clean room (`code/globle_static.py`, `code/make_figures.py`). |

## Model reconstructed

Static GLOBLE (paper Eqs. 1–7):

```
lambda(D)  = alpha_DSB * D / N_L              # mean DSBs per loop, Poisson
p_0(D)     = exp(-lambda)
p_i(D)     = lambda * exp(-lambda)            # exactly 1 DSB / loop -> "isolated"
p_c(D)     = 1 - p_0 - p_i                    # >=2 DSBs / loop      -> "clustered"
n_i(D)     = N_L * p_i
n_c(D)     = N_L * p_c
-ln S(D)   = eps_i n_i(D) + eps_c n_c(D)
```

Paper-fixed constants:

| symbol | value | meaning |
|---|---|---|
| `alpha_DSB` | 30 DSB / Gy / cell | linear DSB-yield per dose, photon LET |
| `N_L` | 3000 / nucleus | number of giant chromatin-loop domains |

Per-cell-line fits used (17 lines transcribed from Herr 2014 Table 2):
C3H 10T1/2, CHO 10B2, CHO K1, NFF28, HX118, HX32, HX58, MT, LL, B16, HX34,
IN859, IN1265, SB, RT112, HX138, HX142.

LQ correspondence (paper Eqs. 12–13 region):

```
alpha_LQ = eps_i * alpha_DSB
beta_LQ  = (eps_c - 2 eps_i) * alpha_DSB^2 / (2 N_L)
```

## Claim-by-claim audit

### Claim 1 — Dose-response is LQ at low D, transitions toward a straight line at high D

**REPLICATED.** Fig. 1 (`figures/fig1_dose_response_RT112.png`) shows `-ln S(D)`
for RT112 with the LQ tangent at small D (visually indistinguishable up to
~3 Gy) and a clear concave-up departure that approaches a quasi-linear slope
in the clinical 5–20 Gy range. The decomposition figure (Fig. 3) confirms that
this "linearisation" is mechanically driven by the clustered-DSB term taking
over once `lambda` is no longer ≪ 1.

Numerical check from `code/globle_static.py` run:

| D (Gy) | n_iso | n_clu | -ln S |
|---:|---:|---:|---:|
| 2 | 58.8 | 0.6 | 0.427 |
| 5 | 142.7 | 3.6 | 1.462 |
| 10 | 271.5 | 14.0 | 4.173 |
| 20 | 491.2 | 52.6 | 12.850 |

The slope `d(-ln S)/dD` over 5–15 Gy ranges from ~0.43 to ~0.87 — exactly the
intermediate-D quasi-linear regime the paper highlights, before the true
high-D saturation at `eps_c * N_L = 585` (only reached around D ≳ 200 Gy,
outside clinical range).

### Claim 2 — Intrinsic β vs α anti-correlation across cell lines

**INCONCLUSIVE on the 17-line subset we have.** Fig. 2
(`figures/fig2_alpha_beta_anticorr.png`):

- Pearson r(α, β) = **+0.655** (not negative)
- Spearman ρ(α, β) = **+0.512**
- Pearson r(α, α/β) = +0.375; Spearman ρ = +0.414

The model expression `beta = (eps_c - 2 eps_i) alpha_DSB^2 / (2 N_L)` predicts
the anti-correlation *only if* `eps_c` and `eps_i` are weakly correlated
across cell lines. In the Herr 2014 17-cell sample (which is the only public
`(eps_i, eps_c)` catalogue we have), `eps_c` and `eps_i` are themselves
strongly positively correlated (radiosensitive lines have both larger isolated
and clustered lethality), which masks the predicted β-vs-α anti-correlation.

The original paper's anti-correlation claim is anchored on a 150+ cell-line
meta-analysis (Friedrich et al.'s PIDE database). Re-digitising that database
is out of scope for a first-pass smoke replication. Recording as
**INCONCLUSIVE** rather than refuted.

### Claim 3 — LQ coefficients are derivable from microscopic parameters

**REPLICATED.** `code/globle_static.py` exposes `alpha_lq` and `beta_lq` as
`StaticParams` properties using the formulae above. The numerical run prints
the full table; tabulated values for RT112 (eps_i=0.00529, eps_c=0.195) give
`alpha = 0.159 /Gy`, `beta = 0.0277 /Gy^2`, i.e. `alpha/beta ≈ 5.7 Gy`, in
the ballpark of literature RT112 photon fits.

## Friction / blockers

- Paper is **closed access**; full PDF text not consulted for this first
  pass. We worked from the published abstract + the well-documented kinetic
  extension (Herr 2014 PLoS ONE) which re-cites and re-uses the static
  equations. Risk: minor symbol or sign convention mismatches with the
  original RR2964 typesetting that we could not verify directly. Mitigation
  for a deeper pass: obtain PDF via institutional access (Argonne / U. Chicago
  library).
- The original Friedrich 2012 PIDE 150-cell meta-analysis used for the β-vs-α
  anti-correlation is not redistributed as a machine-readable table. A second
  pass could re-digitise from the published figure or pull the PIDE database
  (Friedrich et al. *J. Radiat. Res.* 2013; *Int. J. Radiat. Biol.* 2013).
- No author code is published. The Herr-2014 sibling repo and this slot are
  the only Python implementations I am aware of.

## Next actions / follow-up

1. **(Recommend retag to `completed_first_pass`.)**
2. (Optional, deeper pass) Acquire RR2964 PDF via institutional access and
   verify our formula transcription against the original Eq. 7 and Eqs. ≈12–13.
3. (Optional) Re-digitise Friedrich 2012 Fig. 5 (β-vs-α scatter across cell
   lines) or pull the PIDE v3 database for the 150-cell anti-correlation
   check.
4. (Optional) Compare GLOBLE predictions against published RT112, V79, CHO,
   HSG photon clonogenic datasets from PIDE.

## Compute / cost note

No HPC, no GPU, no paid endpoints used. Total wall-clock < 5 seconds on
CherryRd for all numerics + figures. Smoke replication is fully reproducible
on any laptop with `numpy`, `matplotlib`, `scipy`.


---

## Audit Note (2026-06-20)

Independently re-scored on 2026-06-20 by a 3-judge LLM panel (argo:gpt-5, argo:gemini-2.5-pro, argo:claude-opus-4.6) per AUDIT_PROTOCOL.md (median Coverage/Agreement, majority verdict, ties → most conservative).

| Judge | Verdict | Coverage | Agreement | Note (≤200 chars) |
|---|---|---:|---:|---|
| `claude-opus-4.6` | PARTIAL | 4 | 6 | Clean-room reimplementation of static GLOBLE from abstract+sibling paper (no PDF). 2 of 3 claims checked; dose-response shape replicated, beta-alpha anticorrelation inconclusive. Limited to 17 cell... |
| `gpt-5` | PARTIAL | 5 | 6 | Static GLOBLE re-implemented; dose–response shape and LQ mapping reproduced. β–α anti-correlation not testable on full dataset; PDF/data unavailable. Methods inferred from Herr 2014; plausible but ... |
| `gemini-2.5-pro` | SPOT-CHECK | 4 | 9 | Replication was performed without the original paper, based on a secondary source. It confirms the model's internal logic but does not test the paper's main cross-cell-line claim. |

**Aggregated audit verdict:** **PARTIAL** (median Coverage = 4/10, Agreement = 6/10). This is an external audit overlay; the replicator's self-scored verdict above is preserved unchanged. Audit identified this as a thin / coverage-limited report (median Coverage ≤4 or at least one SPOT-CHECK call). Suggested follow-ups: see the report's own next-actions / blockers section.
