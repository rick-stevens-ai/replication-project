# Workflow — QC-2003.02417 Faster Amplitude Estimation replication

Chronological, reproducible workflow (Ollie subagent, 2026-07-03; backfilled 2026-07-06).

## 0. Prereqs

- Python 3.14.6 (Homebrew system)
- Free endpoints only (no paid API calls). No external services used at runtime — everything is local statevector + Binomial sampling.
- Working host: any (2-qubit statevector fits on a laptop CPU; sweep runs in ~132 s).

## 1. Fetch paper

```bash
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2003.02417-faster-amplitude-estimation/work
cd $_
curl -L -o paper.pdf https://arxiv.org/pdf/2003.02417
# Extract text + Fig. 3 as a sanity check
pdftotext paper.pdf paper.txt
pdfimages -png paper.pdf img
# img-004.png ≈ Fig. 3
```

Fetched 2026-07-03T22:30Z.

## 2. Set up isolated env

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2003.02417-faster-amplitude-estimation
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install qiskit qiskit-aer numpy scipy matplotlib
```

Installed:
- `qiskit==2.5.0`, `qiskit-aer` (compiled), `numpy==2.5.0`, `scipy`, `matplotlib`

## 3. Implement Algorithm 1 clean-room

Read Algorithm 1 pseudocode + Chernoff constants (§2.3) + eq. 5 (Q) + eqs. 10, 24, 25 (two-stage updates) from `work/paper.txt` and write, in order:

- `code/oracle.py` — builds `A`, `R`, `X = A ⊗ R`, `Q = X S₀ X† S_good` as 4×4 matrices; `exact_prob_good_after_Qm(a, m)` returns `|<11|Q^m|Ψ'>|²`. This is the honest statevector — no shortcut.
- `code/fae.py` — Algorithm 1 verbatim (two stages, Chernoff intervals eq. 8, extended atan2 eq. 9, integer n_j update eq. 25). `COS(m, N_shot)` samples `Binomial(N_shot, p_good)` and returns `c_m = 1 − 2·N₁₁/N_shot`. Oracle-count tally = `Σ_k m_k · N_shot,k`.
- `code/mlae.py` — Suzuki MLAE baseline (schedule `m_k = 2^(k−1)`, likelihood grid+Brent over `θ ∈ [0, 0.4]`).
- `code/experiment.py` — main sweep driver.
- `code/make_plots.py` — Fig. 3 replica.

**Clean-room rule (self-imposed):** did NOT open the author's reference implementation at github.com/quantum-algorithm/faster-amplitude-estimation. Only the paper text.

## 4. Sanity checks

```bash
source .venv/bin/activate
python code/oracle.py    # exact_prob_good vs sin²((2m+1)θ) at 1e-15 for a∈{0.1,0.2,0.3,0.4}, m∈{0,1,2,4,8,16}
python code/fae.py       # smoke: FAE at ell = 3..6
python code/mlae.py      # smoke: MLAE at M = 3..7
```

Max deviation on the 24-check grid: 2.2×10⁻¹⁵. Green.

## 5. Main sweep

```bash
python code/experiment.py 2>&1 | tee report/evidence/experiment_log.txt
```

- FAE: `a ∈ {0.1, 0.2, 0.3, 0.4}`, `ℓ ∈ {3,4,5,6,7}`, 100 trials each
- MLAE: same `a`, `M ∈ {4,5,6,7,8,9}`, `N_shot = 100`, 200 trials each
- Runtime: 132.4 s
- Records per (algo, a, ell/M): `ε_p95, ε_median, ε_max, N_orac_median, N_orac_mean, j₀_mode, fraction_second_stage`
- Fits `log₁₀(N_orac) = slope · log₁₀(1/ε) + log₁₀ C` per (algo, a)

Outputs → `report/evidence/{sweep_raw.csv, fits.json, summary.json}`.

## 6. Figure

```bash
python code/make_plots.py
# → report/evidence/fig3_replication.png (4 panels, one per a, log-log)
```

## 7. Report

Wrote `report/REPORT.md` (this replication's canonical human-readable report) covering:
1. Paper summary
2. Claims table (C1–C5)
3. Method (env, files, commands)
4. Results (per claim)
5. Verdict (REPLICATED)
6. Evidence artifacts
7. Provenance

## 8. Backfill (2026-07-06)

Added, per BACKFILL_BRIEF_2026-07-05.md:
- `report/REPORT.tex` (LaTeX render with honest Critique section)
- `report/open_questions.json` (5 truly-open questions, bare JSON list)
- `report/open_questions_section.tex` (rendered inside REPORT.tex)
- `report/workflow.md` (this file)
- `report/artifacts_summary.md`
- `report/failure_analysis.md`
- `extraction/nougat.mmd` (stub — no OCR run, marker not yet exercised on this paper)

No re-runs. All existing artifacts preserved.

## Reproduce from scratch

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2003.02417-faster-amplitude-estimation
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit qiskit-aer numpy scipy matplotlib
python code/oracle.py && python code/fae.py && python code/mlae.py
python code/experiment.py 2>&1 | tee report/evidence/experiment_log.txt
python code/make_plots.py
```

Expected wallclock: ~2.5 min (setup + sweep + plot).
