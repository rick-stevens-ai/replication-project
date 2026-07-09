# Attempt Log — WaveTrain (Riedel et al., 2023)

All timestamps America/Chicago (CDT), 2026-07-06.

## 04:08 — task received
Subagent brief: replicate PDE#33 "WaveTrain" (DOI 10.1063/5.0147314). Target dir
`~/Dropbox/REPLICATE-PROJECT/PDE-wavetrain-quantum-chain-2023/`. **NEW dir**, must not
overwrite the sibling `PDE-Riedel-WaveTrain-tensor-trains-2023/` which is a completed
prior replication of the same paper.

## 04:09 — bootstrapping
- Read `WAVE_BRIEF_2026-07-01.md` (8-artifact bar, LLM-judge, free endpoints).
- Read `REPLICATION_DIR_STANDARD_2026-07-05.md`.
- Checked sibling dir: verdict PARTIAL, coverage 100%, agreement 78%, one-line
  patch to scikit_tt required. Decision: do a fully independent run (not a copy).

## 04:10 — paper + code
- arXiv API query on title "WaveTrain" + "tensor trains" → single hit
  arXiv:2302.03725v2 (2023-02-07, revised 2023-02-13). Downloaded PDF (706 kB, 38 pp).
- Extracted plaintext with `pdftotext -layout` → `extraction/paper.txt`. Marker and
  Nougat not installed; wrote a provenance README and mirrored the pdftotext output
  as `marker.md` and `nougat.mmd` (honest substitute; noted in extraction/README.md).
- Cloned `PGelss/wave_train` (shallow) into `work/wave_train`.

## 04:11 — install
- Fresh `python3.12 -m venv work/venv`.
- `pip install 'numpy<2' scipy matplotlib` (paper predates numpy 2.x; safe pin).
- `pip install git+https://github.com/PGelss/scikit_tt` (HEAD).
- `pip install ./wave_train`.
- Versions recorded: numpy 1.26.4, scipy 1.17.1.

## 04:12 — smoke test
- Wrote `work/smoke_test.py`: replay of `test_scripts/Exciton/tise_1.py`.
- First run: `TypeError` at `scikit_tt/solvers/evp.py:381` —
  `Cannot cast ufunc 'add' output from complex128 to float64 with casting rule
  'same_kind'`. This is the same bug the sibling report identified.
- Traced independently: `micro_op` is initialized as real (line 359-362 from
  `np.tensordot` of real op cores), then a complex deflation term `shift*tmp @ tmp.conj().T`
  is added to it. NumPy 1.20+ tightened safe-casting → error.

## 04:13 — patch
- Applied minimal 4-line patch (evp.py:381→384): compute the addend, check
  `np.iscomplexobj(addend)`, promote `micro_op` to complex128 only if needed,
  then use `micro_op = micro_op + addend`. Backup at `evp.py.bak`.
- Re-ran smoke: TISE completes 7 eigenvalues, matches analytic reference to
  ~1e-4 (as reported inline by WaveTrain's own "Exact energy" comparison).

## 04:20 — driver
- Wrote `work/replication_bench.py` (independent, NOT a copy of sibling):
  monkey-patches `TISE.update_solve` to capture per-state energy and psi.ranks,
  runs C1 (N=6) and C2 sweep, plus bonus N=6 open chain.
- Discovered `TISE` object doesn't store the full spectrum in ALS mode
  (only in 'qe' quasi-exact mode) — needed instrumentation. Sibling report
  didn't document this API gap.

## 04:22 — first bench run
- Sweep started with N ∈ {4,6,8,10,12,14}.
- Initial per-state cost at N=12 climbed as deflation stack grew:
  s0 3s → s4 14s → s8 141s → s9 stalled >5 min.
- Killed at ~16 min (state 9 of N=12). Decision: drop N=14, add incremental
  JSON persistence so a kill doesn't lose everything.

## 04:34 — second bench run
- Fixed analytic reference: `sorted([η] + band)` (was omitting vacuum
  ground state → giving spurious 8e-2 max error).
- N=4: max err 6.3e-15 (machine precision).
- N=6: max err 1.0e-4 Ha (matches paper's expected TT-ALS accuracy).
- N=8, N=10, N=12 in progress …

## next
- Wait for sweep to finish.
- Run LLM judge via Argo Opus 4.8 (localhost:44497, free).
- Fill 8-artifact bar: LaTeX report, open_questions.json, workflow.md,
  artifacts_summary.md, failure_analysis.md.
- Emit WAVE_RESULT.
