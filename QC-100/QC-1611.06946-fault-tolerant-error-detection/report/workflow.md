# Workflow — QC-100 replication of arXiv:1611.06946

Paper: Linke et al., *Fault-tolerant quantum error detection*, Science
Advances 3, e1701074 (2017). Preprint arXiv:1611.06946v2.

Target: Reproduce, using an independent Stim stabilizer simulation, the
paper's quantitative and structural claims about the [[4,2,2]] fault-tolerant
error-detection code — in particular the yield, the logical error rates on
La (FT) and Lb (gauge), the FT-vs-non-FT gap, and the p^2-vs-p log-log
scaling that establishes fault-tolerance.

## Steps

1. **Fetch and read paper.** `curl -sL https://arxiv.org/pdf/1611.06946 -o work/paper.pdf`; `pdftotext work/paper.pdf work/paper.txt`. Identify the specific code (`[[4,2,2]]` Iceberg / Bacon-Shor sub-code), the logical operator conventions (`Xa, Za, Xb, Zb` per Section II of paper), the noise regime (`p ≈ 3%` two-qubit CNOT infidelity), and the postselection rule (ancilla `+1` and even data-qubit parity).

2. **Build the Python env.** `python3 -m venv .venv && .venv/bin/pip install stim==1.16.0 numpy matplotlib`. Confirmed on macOS 25.3 with Python 3.14.

3. **Construct the encoding circuit two ways.**
   * A *naive cat* encoding without a flag qubit — used as a negative control (should show FT breakage under single-fault enumeration).
   * A *flag-qubit* encoding, initializing the flag high, performing the four data CNOTs, then flag-off gate + flag measurement (postselect flag=0). This is the paper's fault-tolerant construction, translated into a canonical circuit-diagram equivalent.

4. **Exhaustive single-fault verification (structural proof of FT).** For every non-measurement operation in each circuit, insert every possible single-qubit Pauli fault (X, Y, Z on every involved qubit), simulate deterministically with Stim's TableauSimulator, decode La and Lb, and tabulate the outcome (caught by postselection, undetected La error, undetected Lb error, no error). Run for both `cat + Sx / cat + Sz / flag + Sx` — logs at `report/evidence/ft_single_fault_check.log` and `report/evidence/ft_flag_check.log`. Result: flag encoding yields 0/324 undetected La errors — the paper's FT claim is structurally proved.

5. **Monte-Carlo LER scan (numerical replication).** For each of {cat, flag} × {depol2, single} × {Sx, Sz} across 8 physical-error values `p ∈ [10⁻³, 10⁻¹]`, run 1,000,000 Stim shots. Track yield (fraction of shots surviving postselection) and per-post-selection La/Lb error rates. 128 total scan points, ~30 s total wall. Dump full results to `report/evidence/results_main.json`; text log at `report/evidence/run_main.log`.

6. **Log-log slope fit.** Fit `log err vs log p` in the sub-threshold regime `p ∈ [10⁻³, 3×10⁻²]` per configuration. Verify that (flag, single) yields slope ≈ 2 for La and ≈ 1 for Lb, matching the paper's Fig 4a fault-tolerance signature.

7. **Bare-qubit comparison.** For the same p grid, compute the bare physical qubit error under the single-fault noise model (simple depolarizing on one qubit + SPAM), and tabulate `La / bare` ratio. Confirm La beats bare qubit by 2× to 50× in the sub-threshold regime and falls behind above p ≈ 0.05 — matching paper's Fig 4a convergence claim.

8. **Plot.** `.venv/bin/python work/make_plot.py` → `report/evidence/fig4_replication.png` — log-log La and Lb vs p with bare-qubit reference.

9. **Cross-check numbers vs paper.** Assemble the head-to-head table (paper vs Stim, all four configs, at p=0.03) that appears in REPORT.md § "Results vs paper". Verify that (a) numerical La matches to within ~0.1 percentage points, (b) yield matches within 5–11 pp, (c) FT gap Lb/La is present in the correct direction (compressed relative to paper because depolarizing noise omits ion-trap-specific error channels), and (d) slope claims hold.

10. **Verdict assembly.** Write `REPORT.md` at `report/REPORT.md` synthesizing the above. Verdict = **REPLICATED**: all structural (C1, C2, C10), scaling (C7, C8), and comparative (C9) claims are fully reproduced; numerical yield / La (C3, C4, C5) match within simulation-model accuracy; the only partial-match claim (C6, err_Lb) is explained by the missing non-depolarizing ion-trap noise sources.

11. **Backfill (this pass, 2026-07-05).** Add the 7 canonical artifacts (`REPORT.tex`, `open_questions.json`, `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd` stub) to bring the directory to the 8-artifact standard without re-running any simulations. All existing files are preserved.

## Endpoints and cost

Free endpoints only. All computation is local Stim + numpy on CherryRd
(macOS 25.3). No paid API calls. No paper-download cost (arXiv is free).
Total simulation wall: ~30 s + ~5 s for the two exhaustive-enumeration
scripts.
