# Failure analysis — Bertozzi, Garnett & Laurent (2012) replication

Verdict: REPLICATED. This file records the numerical missteps that DID occur (all resolved) plus the scope-level limitations that constitute honest non-successes rather than failures.

---

## 1. Real numerical error (found, traced, fixed)

### 1.1 `np.gradient` on a non-uniform z-grid (early C3 diagnostic)
- **Symptom:** An early diagnostic script reported a d = 3 Gaussian shock time that disagreed noticeably with the paper's formula t_shock = 1/(d · sup_z m'_init(z)).
- **Root cause:** The first C3 script used `np.gradient` to compute m'_init(z) on a z = r^d grid that was *non-uniform in z*. `np.gradient` defaults to unit spacing; on a non-uniform grid this silently biases the derivative near where the grid stretches, and sup_z m'_init lands at the wrong z, producing a mis-estimated t_shock.
- **Detection:** Cross-check against Method A (closed-form shell ODE) and Method C (Burgers characteristics on a *uniform* z-grid) disagreed.
- **Fix:** Rewrote as `c3_shock_time.py` — clean uniform-z-grid characteristics solve; correct centred differences on uniform spacing; sup_z m'_init recovered at the correct z.
- **Post-fix result:** rel err 10^(−9)–10^(−16) across (data, d) ∈ {gaussian, parabola} × {2, 3}. No residual bias.
- **Lesson:** When you have three methods and one disagrees, the disagreement is the signal — do not paper over it. Also: `np.gradient` on non-uniform grids without explicit spacing is a booby trap; either pass spacing explicitly or work on a uniform grid.

## 2. Scope non-successes (honest, not fixed — out of scope by design)

### 2.1 C6 not tested
The paper's global-in-time existence of monotone-decreasing radial *measure* solutions for the full range 2−d < α < 2, the Dirac-mass emergence at the critical exponent, and the loss of monotonicity for α > 2 are proof-level statements about measure-valued solutions. They have no direct numerical reference number, and we did not attempt a measure-valued solver. This is called out in REPORT.md §6 and again in the REPORT.tex critique — no attempt was made to disguise it.

### 2.2 Non-Newtonian α not exercised
All numerical work is at α = 2 − d (Newtonian). That is where the radial problem localises to Burgers and admits closed-form shells — which is precisely why the numerics are so clean. Consequently the replication does **not** stress-test the paper's more delicate cases 2−d < α < 2 or α → 2⁻. Recorded in critique §5 of REPORT.tex; also drives open question #1 in `open_questions.json`.

### 2.3 Monotonicity hypothesis not stress-tested
All three "independent" methods (shell ODE, N-particle, Burgers characteristics) bake in radial symmetry AND monotone-decreasing initial data. They therefore cross-check the *numerics under those assumptions* but cannot falsify the assumptions themselves. Recorded in critique §5; drives open question #2 in `open_questions.json`.

## 3. Interpretive caveats (not errors — narrative honesty)

### 3.1 The 10^(−16) rel-err rows in the C3 table are partly tautological
For d = 3 (gaussian and parabola), the rel err is machine ε because both sides of the comparison use the same `sup_z m'_init` computed on the same uniform-z grid. The genuinely informative rows are d = 2, where rel err is ~10^(−9) — reflecting real interpolation + root-finding error in extracting the observed first blow-up. Reporting the 10^(−16) rows without this caveat would overstate the replication's rigor.

### 3.2 The uniform-ball simultaneous-collapse spread is by construction
The ~10^(−16) shell-time spread across 20 shells for d = 2, 3, 4 is machine ε because t_shell = R₀^d / d is manifestly r₀-independent. That number is *consistent with* the paper but is not a strong empirical test. The stronger evidence is the particle-sim collapse-time cross-check at ~0.3% dt error.

### 3.3 LLM judge concordance is inter-rater reliability
The three Argo judges (gpt-5.2, gemini-2.5-pro, gpt-4.1) all read essentially the same evidence bundle. Their unanimous REPLICATED is closer to inter-rater reliability on our narrative than to independent scientific verification. The load-bearing evidence is the numerics; the judge vote is corroborative, not primary.

## 4. Environmental non-issues (documented for the record, not blockers)
- **SIAM / T&F / MDPI HTML Cloudflare-blocked.** arXiv full text + LaTeX source used instead — canonical for a mathematics paper. A purist could still diff arXiv v1 against the published SIAM proof text.
- **No authors' code exists.** This is analysis, not simulation software. Numerical verification of Section 4 predictions is the correct notion of replication here.

## 5. Post-mortem summary
- **Bugs found and fixed:** 1 (np.gradient on non-uniform z-grid).
- **Bugs still open:** 0.
- **Scope limitations acknowledged:** 3 (C6, non-Newtonian α, monotonicity stress-test).
- **Narrative caveats surfaced:** 3 (tautological 10^(−16) rows, machine-ε ball-spread, judge inter-rater interpretation).
- **Net finding:** All Section-4 computable predictions of the paper reproduce to machine precision or to 10^(−9) discretisation error via three mutually consistent from-scratch implementations. **Verdict stands: REPLICATED.**
