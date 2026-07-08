# Workflow — arXiv:1808.00128 replication

**Paper:** Bravyi, Browne, Calpin, Campbell, Gosset, Howard — *Simulation of quantum circuits by low-rank stabilizer decompositions*, Quantum 3, 181 (2019).
**Set:** QC-100 · **Verdict:** REPLICATED · **Cost:** free-endpoint only (CPU numpy)

## Stage 1 — Paper acquisition & extraction
1. Pull arXiv PDF `1808.00128v2.pdf` into `paper/`.
2. Run OCR/extraction (nougat) → `extraction/nougat.mmd` (stub in this backfill; equations parsed by hand for the small closed-form claims that matter — Eqs. 28, 30, 31, and the $\alpha$ definition).
3. Manually enumerate claim list into §2 of REPORT.md. Nine claims total (C1–C9); five exact-number claims, two algorithmic claims, one large-scale-search claim (not attempted), one flagship-demo claim (not attempted).

## Stage 2 — Environment setup
1. `python3 -m venv work/venv`
2. `work/venv/bin/pip install numpy` (only dep: numpy 2.5.0, Python 3.14).
3. No paid endpoints, no LLM inference used in the numerical pipeline. All computation on host CPU.

## Stage 3 — Independent reimplementation
Three driver scripts, run in order:

| Script | Claims tested | Output |
|---|---|---|
| `src/verify_extent.py` | C1, C2, C3, C4, C5, C7-analytic | `evidence/verify_extent_results.json` |
| `src/verify_soc_sim.py` | C6 (sum-over-Cliffords, corrected) | `evidence/exp2_soc_corrected.json` |
| `src/stabilizer_rank_sim.py` | C7 (H-state sparse decomp), α scan | `evidence/exp1_H_decomposition.json`, `evidence/verify_scaling.json` |

### Key implementation choices
- **Stabilizer-state enumerator** built from scratch: BFS from $|0\ldots 0\rangle$ under Clifford generators $\{H_i, S_i, \mathrm{CNOT}_{i,j}\}$, deduping up to global phase. Validated by recovering the exact known counts $\{6, 1080\}$ for $n=1, 3$.
- **CCZ headline (C1/C2)**: direct fidelity maximization over the full 1080-state set — obtains $F = 9/16$ exactly, so $\xi = 16/9$ exactly. Independent of paper derivation.
- **Eq. (30) cross-check (C3)**: explicitly construct the 8 Clifford operators, verify $\ell_1$-norm equals $8 \cdot (2/9) = 16/9$.
- **T-state (C4)**: solve $T = aI + bS$ exactly by $a = 1-b$, $b = (e^{i\pi/4}-1)/(i-1)$; three routes to $\xi(T)$: $(|a|+|b|)^2$, Eq.~(28) closed form, $1/F(|T\rangle)$. All agree to $\sim 10^{-16}$.
- **α (C5)**: closed form $-2\log_2\cos(\pi/8) = 0.228447$, rounds to paper's 0.23.
- **Sum-over-Cliffords (C6)**: at $t = 2..10$, all-branch summation matches statevector to $1.7\times 10^{-15}$; $k \sim 100$ importance-sampled version gives $0.01$–$0.08$ error, consistent with paper's $O(\delta)$ claim.

## Stage 4 — Bug hunt & correction
- **Discovered mid-run**: initial SoC implementation used incorrect single-$T$ coefficients $a = (1 + e^{i\pi/4})/2$, which is wrong. Fixed by deriving from $T = aI + bS$ eigenvalue equations. Bad artifact preserved as `exp2_runtime_scaling_SUPERSEDED_buggy_T_coeffs.json` for audit trail; do NOT cite it.
- Corrected version: `exp2_soc_corrected.json`.

## Stage 5 — Not attempted (honestly flagged)
- **C8** (exact rank table $\chi(T^m)$): paper itself notes it required heavy compute. Recorded as target, not re-derived.
- **C9** (50-qubit QAOA / 40–64-$T$-gate Hidden Shift at $\chi \sim 10^6$): out of minutes-scale CPU scope. This IS the paper's flagship performance demonstration; the analytic backbone that makes it possible ($\xi$ values + SoC decomposition) is what we verified.

## Stage 6 — Report generation
1. Draft `report/REPORT.md` with claims table, method, results-vs-paper table, verdict paragraph.
2. Backfill (2026-07-06):
   - `report/REPORT.tex` — LaTeX version with §7 Critique + `\input{open_questions_section.tex}`.
   - `report/open_questions.json` — 5 bare-list open questions.
   - `report/open_questions_section.tex` — pretty-printed version for LaTeX.
   - `report/workflow.md` — this file.
   - `report/artifacts_summary.md` — inventory.
   - `report/failure_analysis.md` — honest critique of what was NOT verified.
   - `extraction/nougat.mmd` stub.

## Stage 7 — Verdict adjudication
- Match against decision criteria: exact headline number reproduced to $\Delta = 0$ via independent method ⇒ **REPLICATED** (for the analytic core).
- Explicitly scope the verdict: applies to analytic backbone, NOT to flagship large-scale performance demonstrations. See `failure_analysis.md`.

## Cost & compute footprint
- Total wall-clock: a few CPU-minutes (numpy on host).
- LLM cost: $0 (no LLM inference on numerical results; free endpoints only for report drafting).
- No GPU used.
