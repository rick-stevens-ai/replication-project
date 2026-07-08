# Failure Analysis — QC-1907.02359 (Benchmarking QAOA)

This document is the deliberately-blunt companion to `REPORT.md` / `REPORT.tex`. Its job is to state, without hedging, what this replication did **not** establish and where a naive reader could mistakenly upgrade the verdict from "REPLICATED on the simulator-testable claims" to something stronger.

## Was the paper's headline claim exercised?

**Partially, and at reduced scale.** The paper's testable headline is a benchmark of QAOA on MaxCut and 2-SAT problem families across depths $p$ up to 10, with three quality measures (success probability, energy expectation, ratio $r$). The central *qualitative* claim — quality improves monotonically with $p$ — was exercised on 6 MaxCut instances at $n \in \{6, 8, 10\}$, $p \in \{1, 2, 3\}$. It reproduces cleanly.

The paper's *scale* was not exercised: no 16-var weighted MaxCut, no 18-var 2-SAT, no $p \ge 4$. Its hardware storyline was not exercised at all.

## What was independently regenerated

- **Approximation ratios at $p=1,2,3$** on 3 random 3-regular graphs and 3 Erdős–Rényi graphs at $n \in \{6, 8, 10\}$. All 18 (graph, p) cells were computed from an independently written Qiskit implementation, not copied from the paper.
- **Success probability $P_{\text{ground}}$** on the same 18 cells.
- **Farhi–Goldstone–Gutmann $\alpha \ge 0.6924$ p=1 lower bound**: our 3-regular instances all sit at $\alpha \in [0.79, 0.85]$ at $p=1$, above the bound.
- **A cross-backend sanity check**: statevector expectation vs. 20 000-shot Aer QASM on 3reg\_n8 at $p=1$; agrees to $5.6 \times 10^{-5}$ in $\alpha$.

## What was NOT regenerated (honest gaps)

1. **The paper's actual benchmark scale.** We ran $n \le 10$, $p \le 3$. Willsch et al. go to $n=16$ (weighted MaxCut), $n=18$ (2-SAT), $p=10$. The specific numeric curves the paper's figures show are therefore *not* independently reproduced — only the qualitative monotone-$p$ trend.

2. **The 2-SAT problem family.** Zero 2-SAT instances were touched. The paper's headline success-probability number (~40% at $p=10$ on 18-var 2-SAT) is untested here.

3. **Weighted MaxCut.** Zero weighted-MaxCut instances were touched. Half of the paper's two headline problem families is missing.

4. **Landscape figures.** Willsch et al. Figs. 2–4 show $(\gamma, \beta)$ contour plots of $E_p$. We did not raster the 2D landscape; we only infer landscape smoothness from the fact that COBYLA converges reproducibly from multiple restarts. That is weaker evidence than the paper's actual figure.

5. **Optimizer match.** The paper uses Nelder–Mead. We used COBYLA. Both are derivative-free and reach comparable optima at small $n$, but a strict optimizer-controlled reproduction would use Nelder–Mead with the paper's restart schedule and function-eval budget.

6. **D-Wave 2000Q comparison (C5).** No annealer access. The paper's cross-platform claim that D-Wave outperforms simulated QAOA on the tested instances is *not* tested.

7. **IBM Q hardware landscape (C6).** No hardware access. The paper's noisy-hardware landscape claim is *not* tested.

8. **Classical baselines.** Goemans–Williamson, SDP rounding, simulated annealing, tabu search — none were run on the same graphs. Without them, "QAOA reaches $\alpha \approx 0.95$ at $p=3$" is a QAOA-internal statement, not evidence about relative merit. Recall Goemans–Williamson guarantees $\alpha \ge 0.878$ on MaxCut with no quantum hardware at all.

9. **Instance-family variance.** Three graphs per family shows the trend but is too few to make meaningful statistical claims about the 3-regular or ER *distributions*. A proper variance analysis would use ~30 seeds per (family, n, p).

10. **Nougat text extraction.** `extraction/nougat.mmd` is a stub in this pass. The report was written from `pdftotext` output, which is acceptable for prose extraction from arXiv preprints but does not capture equations cleanly.

## What would flip the verdict?

- If someone reran the same code on the exact seeds and got materially different $\alpha$ values, that would flip the verdict to NO-GO (contradicts our own numbers).
- If someone extended the run to $n = 16$ weighted MaxCut and $p = 10$ and got a *non*-monotone $\alpha(p)$ trend, that would contradict C1 as we replicated it and would push toward PARTIAL.
- If someone ran D-Wave on the tested instances and did not see the annealer beat QAOA, C5 would be contradicted (and that IS the interesting question).

None of these were attempted here.

## Honest verdict-preserving statement

**REPLICATED** applies to the simulator-testable MaxCut claims exercised at $n \le 10$, $p \le 3$. It does *not* mean the full paper (in particular its 2-SAT, weighted-MaxCut, $n \ge 12$, and hardware storylines) is independently re-established. The verdict is defensible for the QC-100 free-simulator scope but should not be misread as a full re-execution of Willsch et al.'s benchmark suite.
