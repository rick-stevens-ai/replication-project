# Failure Analysis — lucid100-dsb-repair-theoretical-framework

Written 2026-07-06 as part of the backfill pass. Purpose: an honest reading of what did and
did not work in this replication, and where the paper itself has issues. This is not a
whitewash. It preserves and augments the honest gaps section (§7) of REPORT.md.

## 0. Verdict cross-check with queue

- **Queue tag:** REPLICATED.
- **Audit verdict (REPORT.md §8, 2026-06-22):** PARTIAL. Coverage 8/10, Agreement 7/10.
- **Backfill (this file, 2026-07-06):** verdict preserved as PARTIAL. Queue tag is
  inconsistent with the on-disk audit and should be downgraded.
- **Why the mismatch matters:** the queue-vs-audit gap here is characteristic of what
  Rick's 2026-07-06 hard rule catches: without a per-dir cross-check, the aggregate
  "REPLICATED %" gets inflated because a rank-61 A-tier paper that in fact has a paper-side
  ODE instability and two figure-only data blockers gets counted as a clean pass.
- This dir is one of at least 6/21 LUCID dirs with a queue-vs-audit mismatch discovered in
  the 2026-07-06 backfill session.

## 1. Framing: this is a theory paper, not a data-driven prediction paper

Roughly two-thirds of what Murray et al. (2016) put forward is **definitional**:
- master equation (2.1) — a modelling choice;
- ad-hoc closure (2.5) and conditional closure (2.8) — derivations from that choice;
- antibody extension (4.1) — a modelling choice;
- Auger extension (4.3–4.4) — a modelling choice;
- AUC persistence measure (4.5) — a definition.

These items cannot be "verified" or "falsified" by re-running the same equations locally.
They can only be checked for internal consistency and for numerical implementability. We did
implement all of them, and they do run and match the paper's plotted qualitative shapes;
that is a real result. But it is **not** the same thing as an empirical replication in the
Wilson/Ioannidis sense.

An honest "REPLICATED" tag on this paper should therefore mean: *the equations are correctly
transcribed and simulate as advertised*, not *the paper's predictions have been re-tested
against fresh data*. The PARTIAL verdict is the honest one.

## 2. What actually worked

- Every equation (2.1, 2.5, 2.8, 4.1, 4.3–4.4, 4.5) implemented from Tables 1–2 alone.
- Two independent SSA implementations (tau-leap + exact Gillespie) agree with each other
  and with the printed bare eq (2.5) to 5–10% at t=1h on the MDA-MB-468 line.
- 8 of 11 testable claims verified quantitatively (with one — the "approx. 10×" k₅=0
  slowdown — reproduced to within 15–20%).
- The full audit runs in ~2 minutes on a single CPU core, pure Python + numpy + scipy, no
  external services after the one-time PDF/XML pull.

## 3. What did NOT work / where the replication is honestly weak

### 3.1 Data-side blockers (2 of 11 testable claims cannot be tested)

- **Figure 4 raw foci/DSB time series** — the single most impactful blocker. The paper's
  central empirical claim (that the 6-parameter fit reproduces MCF7 and MDA-MB-468
  γH2AX foci kinetics) rests on ~14 data points per cell line that are figure-only in this
  paper AND in the cited experimental papers (Cornelissen 2011 [12], Knight 2015 [17]). No
  supplementary CSV in any of the three papers. Without it the Nelder–Mead refit of eq (3.3)
  cannot be reproduced, and Table 1 cannot be independently verified.
- **Figure 7e antibody sweep** — 4–6 (TAT₀, k₈[TAT]₀/k₇) points, figure-only. Prevents
  independent recovery of k₈/k₇.
- **Figure 8b clonogenic survival vs R** — 5 rows × 2 cols, figure-only. Prevents
  independent test of the R²=0.97 clonogenic claim.

These are collectively a fixable problem: ~6 hours of WebPlotDigitizer + Nelder–Mead work on
CherryRd would close all three. We did not do it in this audit.

### 3.2 Paper-side reproducibility issue (new finding)

**Bare eq (2.5) as printed is dynamically unstable at the published MCF7 fit.** At MCF7's
Table 1 constants, k₃k₅/(k₄k₆) = 1.000374 > 1; the post-repair fixed point (Y,Z) = (0,0)
is a saddle with det J = –145; and bare integration of eq (2.5) to 24 h yields ⟨Y⟩ = 3622
(vs Y_max = 300) and ⟨Z⟩ = 11313 (vs Z_max = 1000). The Z_max/Y_max caps of Table 2 are
enforced by the SSA by construction, but they are absent from eq (2.5) as printed.
MDA-MB-468 sits at ratio 0.987 — just on the stable side of the same bifurcation. So the
paper's fitted parameter regime is generically *very* close to the saddle-node bifurcation,
a fragile place to be doing quantitative predictions.

This is a **paper-side bug**, not a data blocker. Either Fig 4b was integrated to a horizon
short enough to hide the divergence, or a Z_max cap was applied silently. Either way it
deserves an erratum or a re-fit under the constraint k₃k₅/(k₄k₆) < 1.

### 3.3 Framework claims left unchecked

- No cross-validation, held-out prediction, or comparison against a simpler bi-exponential
  baseline (open question Q2).
- No head-to-head against competing DSB-repair frameworks (Cucinotta–Nikjoo, MEDRAS)
  (open question Q3).
- No convergence study of SSA-vs-ODE as function of trajectory count (open question Q4).
- No test at parameter extremes: FLASH, ultra-low-dose, extreme-high-LET (open question Q5).

None of these are within the scope of a single-paper replication audit as defined here,
but each is a genuine loose end of the framework's scientific claim.

### 3.4 Where the audit itself is weaker than it should be

- **Tau-leap bias not quantified separately from closure bias.** Our closure-vs-SSA RMS of
  ~13% on the dynamic range of ⟨Z⟩ mixes both. A proper decomposition would need
  larger-n exact Gillespie (see Q4).
- **Only MDA-MB-468 got the exact-Gillespie cross-check.** MCF7 was skipped for SSA cost
  reasons. Given the MCF7 instability finding, that is exactly the line where the exact-SSA
  vs bare-ODE comparison would be most informative — we should have done it and did not.
- **Nominal k₇, k₈, k₉ values are guesses.** The antibody and Auger extension AUC numbers
  are qualitatively right but quantitatively rest on unpublished proportionality constants.
  We did not attempt a Fig 7e / Fig 8b WebPlotDigitizer extraction to fix them.

## 4. Framework-level vs testable-claim breakdown

| Type | Count | Status |
| --- | --- | --- |
| Definitional / framework-level | 6 (eqs 2.1, 2.5, 2.8, 4.1, 4.3-4.4, 4.5) | all implemented, internally consistent |
| Testable claim, tested | 9 | 6 verified, 2 partial, 1 contradicted (MCF7 stability, new) |
| Testable claim, blocked | 2 | Fig 4 fit quality, Fig 8b clonogenic R² |

So of the **testable** subset, 6/11 = 55% pass cleanly, 3/11 = 27% have caveats (partial or
contradicted), 2/11 = 18% cannot be tested from the public record. That composite is the
basis for the PARTIAL verdict, not "REPLICATED".

## 5. Lessons for the LUCID-100 audit process

1. **Queue tag ≠ audit verdict** — this dir is one of at least 6/21 sampled LUCID dirs where
   the two disagree. Rule (per Rick 2026-07-05): always cross-check REPORT.md's verdict
   against the queue and preserve the audit verdict; flag the mismatch. Applied here.
2. **Theory papers need a special rubric.** A "REPLICATED" tag on a framework paper without
   independent-data testing means something different than "REPLICATED" on a data-driven
   prediction paper. LUCID-100 should distinguish these.
3. **Figure-only data is the single largest gap** across LUCID replications. A shared
   WebPlotDigitizer pipeline would close ~6h × N papers of blocker gaps.

## 6. What was preserved

All pre-existing files (README.md, MANIFEST.json, PROGRESS.md, REPORT.md,
FIRST_PASS_REPORT.md, all `artifacts/`, all `scripts/`) are untouched. The backfill added
only files under `report/` and one stub at `extraction/nougat.mmd`. No sims re-run, no
existing verdict overwritten.
