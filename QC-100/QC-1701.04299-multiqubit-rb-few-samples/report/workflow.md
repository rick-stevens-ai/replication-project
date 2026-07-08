# Workflow — QC-1701.04299 multi-qubit RB few-samples replication

## Provenance
- Paper: Helsen, Wallman, Flammia, Wehner — *Multi-qubit RB Using Few Samples* — arXiv:1701.04299v3 (Aug 2019).
- Replicator: OpenClaw autonomous subagent, QC-100 wave.
- Original replication run: 2026-07-03 on CherryRd (macOS, Python 3.13).
- Backfill (LaTeX + open questions + workflow docs): 2026-07-06 by subagent, no re-run of numerics.

## Pipeline (top to bottom)

1. **Paper ingest** — download `arXiv:1701.04299v3` PDF into `work/1701.04299.pdf`; extract text to `work/1701.04299.txt` (marker/pdftotext).
2. **Claims extraction** — read paper, distill 5 testable claims (C1–C5) into REPORT.md §2. C3 is the practical headline; C1 is the analytical anchor number (N=173).
3. **Scope decision** — implement C1 (closed-form eq. 10) + C3 (real Aer simulation + bootstrap). C2/C4/C5 flagged UNTESTED.
4. **Environment** — `python3 -m venv venv && pip install qiskit qiskit-aer numpy scipy matplotlib`. Frozen versions in REPORT.md §3.1.
5. **Simulation** — `code/rb_2qubit.py`:
   - 2-qubit Clifford RB, lengths m ∈ {1,2,5,10,20,40,75,125,200}.
   - N_max=100 random Clifford sequences per m, 400 shots each.
   - Depolarizing noise: `p_cx=0.01`, `p_1q=0.001` attached to native gates via `NoiseModel`.
   - Inverse of group product appended; survival = P(|00⟩).
   - Emit raw survivals → `report/evidence/rb_raw_survivals.json`.
6. **Bootstrap** — same script: 300 resamples for N ∈ {5,10,15,20,30,50,75,100}, fit `A f^m + B` via bounded `scipy.optimize.curve_fit`, compute r = (d−1)/d·(1−f). Record (mean, std) → `rb_bootstrap_summary.json`.
7. **Analytical bound (C1)** — `code/paper_bound.py`: evaluate eq. (10) at paper example (d=2, m=100, r=1e-4, u=(1+f²)/2, ε=δ=0.01) + Chebyshev. Compare N=195 (ours, eq. 10) vs N=173 (paper, eq. 9) vs N=145–1631 (Wallman–Flammia [24]). Emit `paper_bound_comparison.json`.
8. **Figures** — `code/plot_results.py`: `rb_decay.png`, `r_vs_N.png`, `rel_std_vs_N.png`.
9. **Report** — REPORT.md written with claims table, method, results, verdicts, critique of untested items.
10. **Backfill (2026-07-06)** — package REPORT.tex (with honest critique), workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.{json,tex}, extraction/nougat.mmd stub. No new numerics.

## Reproduction commands
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1701.04299-multiqubit-rb-few-samples
python3 -m venv venv && source venv/bin/activate
pip install -q qiskit qiskit-aer numpy scipy matplotlib
python code/rb_2qubit.py       # ~32 s
python code/paper_bound.py     # <1 s
python code/plot_results.py    # <2 s
```

## What was NOT done
- Eq. (9) tight bound (would close the 13 % gap on C1).
- q-scaling of eq. (11) for q=1..6 (Fig. 2b, C5).
- OLS-vs-IRLS empirical comparison (C4).
- 4-qubit N=249 computation (C2 spot-checked analytically only).
- Non-Markovian / coherent / crosstalk noise robustness (out of scope but see open question #2).

## Provenance guarantees
- No LLM produced any numerical result. All numbers are direct stdout of `code/*.py` against Qiskit Aer.
- Wall-clock ≈35 s end-to-end after venv install.
- All raw data preserved in `report/evidence/*.json`.
