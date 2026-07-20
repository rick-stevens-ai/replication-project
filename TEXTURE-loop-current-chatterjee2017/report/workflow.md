# Workflow — replication of arXiv:1705.06289

## 1. Fetch & extract
- `paper.pdf` present in target dir (pre-fetched).
- `pdftotext -layout paper.pdf paper.txt` (poppler). Clean native text layer,
  974 lines, no OCR / vision route needed. See `extraction/marker.md`.

## 2. Scope triage
- Read full paper. Identified it as a **square-lattice SDW mean-field / SU(2)
  gauge theory** of the cuprate pseudogap, with loop-current order as phase C.
- Read the shared kernel `loop_current_kagome_kernel.py`: it is **kagome**
  Peierls-flux tight-binding — right *class* (loop current), wrong *lattice*.
- Decision (honest flag, `code/PROVENANCE.md`): do NOT force the kagome model.
  Reuse only the transferable idea — the real=charge / imag=loop-current
  bond-bilinear decomposition (`bond_current_and_charge`) — and rebuild the
  paper-specific core from Appendix B (Eqs. B4-B6) and Appendix C (Eq. C14).

## 3. Implement (`code/sdw_meanfield.py`)
- Square-lattice dispersion `xi_k` with tp, p=1..4.
- 2x2 SDW mean-field Hamiltonian `bands()` -> analytic E_{k,s} (Eq. B6).
- `filling()`, `solve_mu_for_filling()` (bisection), `free_energy()` (Eq. free-E).
- `self_consistent_h()` gap equation h = 2 U N0 via thermodynamic m = -dE/dh.
- `sdw_bond_current()` = Eq. C14 loop-current diagnostic (kernel concept).
- `classify_phase()` -> D0/A0/B0/C0/F0/PM labels.

## 4. Run checks (`code/run_checks.py` -> `work/`)
Five machine-checkable claims C1-C5 (see `artifacts_summary.md`). Every number
computed live; results serialized to `work/results.json` + `work/run_log.txt`.

## 5. Figures (`code/make_figs.py` -> `report/fig_sdw.png`)
- (a) self-consistent Néel gap h(U); (b) SDW band structure Gamma-X-M-Gamma.

## 6. Report (`report/`)
- `REPORT.tex` (+ compiled `REPORT.pdf` if latex available), `open_questions.json`
  (exactly 5), `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.

## Reproduce
```
cd code
python3 run_checks.py     # -> ../work/results.json, run_log.txt  (~5 s)
python3 make_figs.py      # -> ../report/fig_sdw.png
cd ../report && latexmk -pdf REPORT.tex   # optional
```
Deps: python3 + numpy + matplotlib. No network, no paid endpoints.
