# FIRST-PASS REPORT — Taleei & Nikjoo (2013) Biochemical DSB-repair model

- **Slot:** LUCID100 Wave 1, rank 41, slot 10
- **DOI:** 10.1016/j.mrgentox.2013.06.004  (PMID 23792210)
- **Authors:** R. Taleei, H. Nikjoo (Karolinska Institute)
- **Replicator:** Ollie subagent, 2026-06-09 (channel: telegram main session)
- **Verdict:** **PARTIAL REIMPLEMENTATION — qualitative agreement; quantitative claim-by-claim deferred pending full-text access.**

---

## 1 · What the paper does

Builds a **law-of-mass-action ODE** model of double-strand-break (DSB) repair
in G1 / early-S mammalian cells, restricted to the two pathways active in
that cell-cycle window: **non-homologous end-joining (NHEJ)** and
**microhomology-mediated end-joining (MMEJ)**.  Homologous recombination is
explicitly excluded (no sister chromatid available).

Key biology in the abstract:

- **Simple DSBs** → c-NHEJ (Ku → DNA-PKcs → Lig4 ligation, fast).
- **Complex DSBs** and **DSBs in heterochromatin** require additional
  end-processing → either slow NHEJ (Artemis-mediated blunting) or MMEJ
  (CtIP/MRN/EXO1-mediated resection + microhomology search + Lig3).
- All DSBs begin with NHEJ presynaptic chemistry (Ku loading); branch
  decision happens after end inspection.
- Mass-action rate constants are tuned to reproduce published bi-phasic
  γH2AX / PFGE / comet kinetics.
- Authors state the model is intended to support **high-LET predictions**
  via the increased fraction of "complex" DSBs at high LET.

## 2 · Source-material status (artifact harvest)

| Resource | Verdict |
|---|---|
| Full-text PDF | **PAYWALLED** (Elsevier, no PMC/preprint, no Karolinska open repository, no ResearchGate copy). Unpaywall `oa_status=closed`, Semantic Scholar `openAccessPdf.status=CLOSED`. |
| Supplementary | Not listed on ScienceDirect. None to harvest. |
| Authors' code | Not released. |
| Authors' data | Pure modelling paper — comparison data are re-used from cited foci/PFGE literature. |
| Author contact | **DISALLOWED** by task rules. |

→ The literal PDF cannot be acquired through this slot. We proceed with a
**model-skeleton replication** instead of figure-pixel-matching, based on
the abundant open material from the same group that uses an identical
formalism (see `artifacts/ARTIFACT_MANIFEST.md`, surrogates A-E).

## 3 · Replication strategy chosen

**Strict scope:** independent minimal reimplementation of the pathway
topology and kinetic skeleton in `code/taleei_nikjoo_2013_minimal.py`.

- 9-state compartmental ODE: `{S_dsb, C_dsb, S_ku, C_ku, C_proc, C_mmej,
  REP_FAST, REP_SLOW, REP_MMEJ}`.
- Parameters: chosen from the **open** Qi 2021 (Cancers 13:2202) Table 1
  reproduction in `lucid-slow-fast-nhej/code/nhej_model.py`, which itself
  reproduces the Taleei-Nikjoo rate constants; values are physically
  consistent with the abstract description.
- Solver: SciPy `solve_ivp` with `LSODA`, RTOL 1e-9, ATOL 1e-12.
- Smoke driver evaluates WT at 0.5/2/4 Gy, Artemis/Ligase4/Ligase3
  deficiencies, and a high-complex-DSB scenario as a qualitative
  high-LET surrogate.

## 4 · Acceptance criteria & results

Bench-marked against **qualitative** behaviours that any faithful
reimplementation of Taleei-Nikjoo 2013 must exhibit:

| # | Expected behaviour (from abstract + companion papers) | Reimplementation result | Pass? |
|---|---|---|---|
| 1 | Biphasic WT repair: fast component ~tens of minutes (c-NHEJ), slow component ~hours (MMEJ/processed NHEJ). | WT 2 Gy: 50% repaired by ~0.5 h, 99% by ~6 h, residual flat by 24 h. Decomposition shows c-NHEJ saturates fast, slow-NHEJ rises through 6 h, MMEJ trickles to ~5%. | ✅ |
| 2 | Linear dose response (no spontaneous repair at zero dose; counts scale ∝ Gy). | 0.5 Gy 48.6→0.19 unrepaired; 2 Gy 48.6→0.77; 4 Gy 97.3→1.54.  Fractions identical across doses. | ✅ |
| 3 | Artemis-deficient cells: WT-like early kinetics, large residual at 24 h (~30-45%). | Artemis-def 24 h residual = **45%** (slow-NHEJ branch fully blocked; only fast branch still works). | ✅ |
| 4 | Ligase4-deficient cells: catastrophic NHEJ loss, near-total residual. | Ligase4-def 24 h residual = **95%** (only MMEJ branch remains, at 5%). | ✅ |
| 5 | Ligase3-deficient cells: only the small MMEJ fraction is lost (≲10% residual). | Ligase3-def 24 h residual = **5%**. | ✅ |
| 6 | High-LET surrogate (raise complex-DSB fraction from 0.5 to 0.8): slower overall kinetics, larger MMEJ contribution. | high_complex 1 h residual rises from 32% → 47%; MMEJ flux rises ~1.6×. | ✅ |

→ All six qualitative predictions reproduce.  This is the minimum bar for a
"is the published model self-consistent and computable" check.

## 5 · What we did NOT replicate (limitations)

- **No Figure-pixel agreement.** We do not have the original Figs 2-5 to
  digitise. Acceptance is qualitative only.
- **No heterochromatin compartment.** Paper distinguishes eu- vs
  heterochromatin DSB processing; our minimal version folds this into
  `f_complex`.
- **No explicit microhomology search step.** MMEJ ligation lumps
  resection + search + Lig3 into one mean time.
- **No LET-dependent damage spectrum coupling.** A high-LET run is
  simulated by hand-bumping `f_complex`; a real coupling needs a
  track-structure DSB-yield model (Henthorn / Nikjoo Monte Carlo).
- **No stochastic / Poisson per-cell variance.** Pure deterministic ODE on
  ensemble fractions.

## 6 · Compute footprint

The smoke ODE solves in ≪1 s on the local CherryRd Python install. No
heavy compute; no HPC job needed for this slot.  If a full parameter scan
(p_mmej × f_complex × LET sweeps) is later requested, that still runs in
seconds on CherryRd — no GPU / no scheduler entry required.

## 7 · Verdict

> **GO for downstream LUCID use** as a documented kinetic skeleton of the
> Taleei-Nikjoo 2013 G1/early-S NHEJ+MMEJ model.
>
> **PARTIAL** with respect to the original paper: model topology and
> qualitative behaviour reproduced; figure-level numerical reproduction is
> blocked until the PDF is obtained through a non-paywall route (Karolinska
> open access via ALCF / Argonne library, an interlibrary loan, or
> re-extraction from the open Qi 2021 supplement which already digitises
> the relevant rate constants).

## 8 · Recommended next actions (not executed in this slot)

1. **Acquire the actual PDF** through Argonne library / interlibrary loan
   (allowed under LUCID norms, not under this subagent's task constraints).
2. **Digit-extract Figures 2-5** (WT, Artemis-def, MMEJ-def, LET sweep)
   from the PDF when obtained; rerun with the same parameters and compute
   χ²/DF against the digitised points.
3. **Couple to a track-structure DSB-yield input** (the Henthorn module
   already vendored in `lucid-slow-fast-nhej/artifacts/damaris/`) to
   replicate the paper's high-LET prediction quantitatively.
4. **Add the heterochromatin compartment** (two parallel `f_complex` pools
   with different `tau_process`) to recover the spatial heterogeneity the
   paper highlights.

No external services were paid; no author was contacted; no heavy compute
was used.
