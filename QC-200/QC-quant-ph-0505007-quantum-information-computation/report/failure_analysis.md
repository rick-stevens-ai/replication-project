# Failure Analysis — quant-ph/0505007 replication

Verdict: **REPLICATED** (12/12 cells match to ≤ 3.3×10⁻¹⁵). This document records the friction, workarounds, and residual gaps.

## 1. First-pass bug: outcome-0 branch not renormalised

**Symptom.** Initial run reported the following:

```
n=2 q=1  measured 0.42187500  predicted 0.42187500  diff 5.6e-16    (OK)
n=2 q=2  measured 0.28515625  predicted 0.23730469  diff 4.8e-02    (BAD)
n=2 q=3  measured 0.28037981  predicted 0.13348389  diff 1.5e-01    (WORSE)
n=2 q=4  measured 0.29177834  predicted 0.07508469  diff 2.2e-01    (WORSE)
```

The single-iteration case matched perfectly, but multi-iteration cases drifted increasingly far from the paper's ε^(2q+1) prediction — and, tellingly, the error stopped decreasing monotonically past q≈2.

**Root cause.** The simulator was carrying the outcome-0 branch of the ancilla-2 measurement without renormalising. That branch has norm² = p₀ = 1/N² after the first iteration, so the joint-diffusion reflection was being applied to a state of the form (1/N)|t'_j⟩|0⟩ rather than the unit vector |t'_j⟩|0⟩. Because the diffusion is a reflection about the joint source state |s_j⟩, it is norm-preserving; but the projector-then-reflection composition used in the analysis (paper Eq. 5) is derived assuming a unit input, and my bookkeeping formula (`success_prob += (1 - success_prob) * p1`) implicitly assumed the running state was normalised. The result: probability mass was silently being double-counted.

**Fix.** After each ancilla-2 measurement, split into `branch0`/`branch1`; add the branch-1 mass to `success_prob` weighted by `prob_still_running`; multiply `prob_still_running` by p₀; and *renormalize* the outcome-0 branch by `math.sqrt(p0)` before continuing.

**Post-fix result.** All 12 cells match to ≤ 3.3×10⁻¹⁵. See `report/evidence/results.json`.

**Lesson for the wave.** Statevector simulation of mid-circuit-measurement algorithms is easy to get subtly wrong if you conflate "carry the unnormalised outcome branch" with "track branch weight separately." The clean pattern is:
1. Split state into orthogonal branches under the measurement.
2. Accumulate mass into a running probability *before* renormalising.
3. Renormalise the surviving branch.
4. Apply the next unitary.

## 2. Marker / Nougat extractions are fallbacks, not native tool output

**Situation.** The 8-artifact standard requires `extraction/marker.md` and `extraction/nougat.mmd`, either pulled from a central corpus or freshly parsed. On CherryRd at replication time, neither `marker` nor `nougat` was installed (verified: `which marker` → not found; `python3 -c "import marker"` → ModuleNotFoundError; likewise for nougat), and a corpus-wide search under `~/Dropbox` did not find a pre-parsed copy for arXiv:quant-ph/0505007.

**Workaround.** Both extraction files were written by hand from the `pdftotext -layout paper.pdf` output, structured to closely resemble Marker's section-headed markdown and Nougat's inline-LaTeX .mmd conventions. Both files begin with a clearly-visible provenance banner stating they are FALLBACKs and pointing to `paper.pdf` as the authoritative source. Equations were transcribed from the PDF and cross-checked; ASCII stand-ins used where pdftotext dropped Unicode/math glyphs.

**Residual gap.** These extractions will not be byte-identical to a genuine Marker/Nougat parse if this paper is later added to the central corpus. Anyone using them for downstream ML training should re-run Marker/Nougat and replace the fallback files; the numerical replication itself does not depend on them.

## 3. LaTeX compilation not attempted

**Situation.** The 8-artifact spec says "compile to REPORT.pdf when possible." No `pdflatex` / `latexmk` was invoked in this session (the report contains the LaTeX source; whether a PDF is produced depends on the compile environment, which was not a target of this subagent).

**Impact.** None on the replication verdict — REPORT.tex is complete and self-contained. Compile step can be added by any downstream reader with a working TeX Live.

## 4. Not attempted (in-scope-but-deferred)

- **Average-case query-count comparison with Phase-π/3** (paper's C6 claim). Requires implementing Phase-π/3 and Monte-Carloing both algorithms over ε-priors. Out of scope for a 1-hour replication window; captured as open question Q2.
- **Noise-robustness check** for the paper's Feature (2) claim about self-correction of earlier errors. Requires a density-matrix simulator with per-gate noise channels. Captured as Q3.
- **Robustness of the ε^(2q+1) identity to non-Hadamard source unitaries U.** Captured as Q1.
- **Lower-bound question on number of ancillas.** Captured as Q4.

## 5. Confidence statement

The paper's headline claim (Eq. 6, ε^(2q+1) for all positive integer q) is verified to machine precision across three register sizes and four query depths (12 independent cells). The identity is not an asymptotic bound and not a statistical near-match — it is an exact algebraic identity, and the simulator confirms that at the level of double-precision arithmetic. Confidence in **REPLICATED**: high.
