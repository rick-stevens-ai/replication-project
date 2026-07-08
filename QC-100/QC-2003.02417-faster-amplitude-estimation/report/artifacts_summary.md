# Artifacts Summary — QC-2003.02417 Faster Amplitude Estimation

Every artefact under this replication directory, with a one-line description and a role tag.

## Report artefacts (`report/`)

| File | Role | Description |
|---|---|---|
| `REPORT.md` | canonical | Human-readable replication report, verdict REPLICATED |
| `REPORT.tex` | render | LaTeX render of the same content + explicit Critique section; `\input{open_questions_section.tex}` |
| `open_questions.json` | machine | Bare JSON list of 5 open questions (`{q, basis, next_steps}`) |
| `open_questions_section.tex` | render | LaTeX version of the same 5 questions, prose form |
| `workflow.md` | reproducibility | Chronological workflow, prereqs, exact commands |
| `artifacts_summary.md` | index | This file |
| `failure_analysis.md` | critique | Honest self-assessment of what didn't get done and why |

## Evidence artefacts (`report/evidence/`)

| File | Role | Description |
|---|---|---|
| `sweep_raw.csv` | data | Every (algo, a, ℓ/M) row: ε_p95, ε_median, ε_max, N_orac_median, N_orac_mean, j₀_mode, fraction_second_stage |
| `fits.json` | data | Per-a linear fits `log10(N_orac) = slope · log10(1/ε) + log10 C` for FAE and MLAE, R², prefactor ratio |
| `summary.json` | data | Condensed table used in §4 of REPORT.md |
| `fig3_replication.png` | figure | 4-panel log-log plot replicating paper Fig. 3 (FAE green, MLAE red) |
| `experiment_log.txt` | log | Full stdout of `python code/experiment.py` |

## Source code (`code/`)

| File | Role | Description |
|---|---|---|
| `oracle.py` | source | Builds `A`, `R`, `X = A ⊗ R`, `Q = X S₀ X† S_good` (paper eq. 5); `exact_prob_good_after_Qm(a, m)` |
| `fae.py` | source | Algorithm 1 verbatim: two stages, Chernoff shot counts, `atan2` extension, `n_j` update |
| `mlae.py` | source | Suzuki MLAE baseline (paper's ref [13]): schedule `m_k = 2^(k-1)`, likelihood via grid+Brent |
| `experiment.py` | source | Main sweep: FAE (a×ℓ×100 trials) + MLAE (a×M×200 trials), fits, dumps |
| `make_plots.py` | source | Produces `report/evidence/fig3_replication.png` |

## Working files (`work/`)

| File | Role | Description |
|---|---|---|
| `paper.pdf` | source | arXiv 2003.02417v3, fetched 2026-07-03T22:30Z |
| `paper.txt` | source | `pdftotext` extraction (used for clean-room reading of Algorithm 1) |
| `img-004.png` | source | `pdfimages` extract of paper Fig. 3 |

## Extraction (`extraction/`)

| File | Role | Description |
|---|---|---|
| `nougat.mmd` | stub | Placeholder — full-paper OCR (nougat/marker) not run for this replication; Algorithm 1 was clean-room from `paper.txt` |

## Environment (`.venv/`)

Standard `python3 -m venv .venv` with `qiskit 2.5.0 + qiskit-aer + numpy 2.5.0 + scipy + matplotlib`. Not checked in.

## Verdict

**REPLICATED.** Paper's headline claim — near-Heisenberg query complexity `N_orac ∝ 1/ε` with a small constant for `a ∈ {0.1, 0.2, 0.3, 0.4}` — reproduced end-to-end on a real 2-qubit statevector simulation. Fitted slopes 0.85, 1.20, 1.26, 0.96 (all consistent with the ideal Heisenberg slope 1 within 100-trial sampling noise). Grover-operator correctness at machine precision (2×10⁻¹⁵). Two-stage trigger j₀ decreases monotonically with a as reported. Prefactor sits ~30× below the proven upper bound.

Principal open gap: Grinko IQAE was NOT independently implemented, so the paper's headline "~280× tighter proven prefactor than IQAE" was not empirically raced. See `failure_analysis.md` and `open_questions.json`.
