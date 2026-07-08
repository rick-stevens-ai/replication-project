# Artifacts summary — arXiv:2304.07917 replication

## Top-level layout

```
QC-2304.07917-non-unitary-trotter-ite/
├── report/
│   ├── REPORT.md                       # human-readable replication report
│   ├── REPORT.tex                      # LaTeX version (backfill)
│   ├── open_questions.json             # 5 open questions (structured)
│   ├── open_questions_section.tex      # LaTeX open-questions section
│   ├── workflow.md                     # step-by-step workflow (backfill)
│   ├── artifacts_summary.md            # this file
│   ├── failure_analysis.md             # honest post-mortem (backfill)
│   └── evidence/                       # runnable code + numeric outputs + plots
│       ├── ite_tim.py                  # 4-site TIM Trotter-PITE implementation
│       ├── ite_tim_result.json         # per-step energies, overlaps, p_success
│       ├── ite_tim_history.csv         # tabular per-step history
│       ├── ite_tim_summary.json        # final energy/error/p_success summary
│       ├── ite_hubbard.py              # 2-site Hubbard Trotter-PITE implementation
│       ├── ite_hubbard_result.json     # per-step Hubbard results
│       ├── cross_check_expm.py         # scipy.expm sanity check
│       ├── qiskit_gadget_verify.py     # partial ancilla-circuit reconstruction
│       ├── make_plots.py               # regenerates fig7 + fig8
│       ├── fig7_tim.png                # replication of paper Fig 7 layout
│       ├── fig8_hubbard.png            # replication of paper Fig 8 layout
│       └── llm_judge_verdict.txt       # early LLM cross-judge notes
├── work/                               # working dir (venv, paper.pdf/txt, scratch)
└── extraction/
    └── nougat.mmd                      # extracted paper text stub
```

## Artifact roles

- **`REPORT.md` / `REPORT.tex`** — headline replication write-up. Claim table
  (C1--C6), quantitative comparison of $\langle E\rangle$ and $p_{\rm success}$
  vs.\ paper Figs 7 & 8, verdict, critique.
- **`open_questions.json`** — machine-readable list of 5 open questions with
  `q`, `basis`, `next_steps`. Consumed by downstream survey/synthesis tools.
- **`open_questions_section.tex`** — same 5 questions rendered as a LaTeX
  section, included from `REPORT.tex`.
- **`workflow.md`** — end-to-end steps to reproduce, including the venv
  setup, run order, and enumeration of what was *not* attempted.
- **`failure_analysis.md`** — honest post-mortem: partial ancilla-circuit
  reconciliation, boundary-condition inference risk, missing baselines,
  no noise model, larger-system claim untested.
- **`evidence/*.py`** — runnable, deterministic implementations of the
  Trotter-PITE algorithm, the cross-check, the ancilla-gadget verifier,
  and the plot generator.
- **`evidence/*.json` / `*.csv`** — full per-step numeric results,
  reloadable by any downstream analysis.
- **`evidence/*.png`** — plots mirroring the paper's Fig 7 (TIM, three
  panels) and Fig 8 (Hubbard, three panels).
- **`evidence/llm_judge_verdict.txt`** — verdict cross-check notes from an
  LLM-judge second-opinion pass done at the time of the original run.
- **`extraction/nougat.mmd`** — extracted-text stub for the paper (see
  `failure_analysis.md` for the actual extraction path used).

## Quantitative headline (from evidence)

- 4-site TIM: $|\Delta E| = 2.40\times 10^{-4}$ at $\beta = 4.5$
  (exact $E_0 = -2.0202968496$, Trotter $\langle E\rangle = -2.0200572$),
  cumulative $p_{\rm success} = 5.92\times 10^{-3}$.
- 2-site Hubbard: $|\Delta E| = 1.78\times 10^{-3}$ at $\beta = 6$
  (exact $E_0 = -0.1561552813$, Trotter $\langle E\rangle = -0.1543761$),
  cumulative $p_{\rm success} = 0.111$.
- Cross-check: Trotter ITE state overlap $= 0.99994$ with `scipy.expm(-beta H)`
  across $\beta \in [0.5, 4.5]$ on the 4-site TIM.

## Reproducibility

Deterministic; no RNG dependence in the statevector code path. Rerun via the
steps listed in `workflow.md` §Reproducibility. Total wall-clock on m1
CPU: ~30 s for TIM, ~2 min for Hubbard.
