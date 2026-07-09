# Workflow — OSTI 2480245 (Energy-Conserving PIC Reweighting)

Replication executed on CherryRd, 2026-07-01. Aleph (Sandia's PIC-DSMC code) is proprietary and has no public code/data package, so the strategy was **operator-level reimplementation from the paper's equations** plus abstracted structural scaling tests, followed by an LLM judge.

## 0. Fetch

- Attempted `curl https://www.osti.gov/servlets/purl/2480245` from CherryRd → timeout (network path filtered).
- Fell back to `ssh uicgpu` (has full outbound internet), curl there, then `scp` back to `work/paper.pdf` (5.5 MB).
- `pdftotext -layout paper.pdf paper.txt` → readable UTF-8 text extraction.

## 1. Artifact discovery

- Searched OSTI record, GitHub, Zenodo, and paper text for code/data package. **None found** — the paper describes a scheme implemented inside Sandia's Aleph and does not release the code.
- Recorded in `report/artifact_harvest.md`.

## 2. Reimplementation (`work/reweight.py`)

- `split_particle`: implements Sec 3.1 exactly.
  - Eligibility: `W_parent >= 3 * W_min`.
  - Nearest-face bound `dx_max`.
  - Biased spherical sampling (Eq 4) with polar axis parallel to local **E**.
  - Symmetric ±dx displacement (COM/charge preserved).
  - Eq-5 parallel-velocity correction `v_∥² ± (2q/m) E·dx`.
  - Imaginary-velocity rejection with polar=π/2 fallback (Rick-verified logic).
- `merge_pair`: implements Sec 3.2 exactly.
  - Nearest-speed companion selection within the cell.
  - Eq-6 COM position; Eq-7 modified COM velocities (imaginary → reject).
  - Eq-8/9 cutoffs: `Δv < √(kT/m)` at T=5 eV, `α < 30°`.
  - Eq-10 mass-averaged velocity, Eq-11 KE_lost.

## 3. Conservation tests (`work/test_conservation.py`)

- 20,000 random splits and ~18,600 random merges of electron macroparticles.
- Field: Test-4.1 exponential sheath `Φ(x) = Φ_w · exp(-x/L)`, `Φ_w = -15 V`, `L = 5 µm`.
- Measured relative errors of every invariant (mass, COM, energy for splits; mass, COM-momentum, KE_lost sign, KE_lost magnitude for merges).
- Output: `evidence/conservation_results.json`.

## 4. Growth-independence test (`work/test_growth_independence.py`)

- 0D ionization at rate `ν = 3.06 s⁻¹`.
- Reweighting control loop maintains computational count within ±10 % of `N_c ∈ {10, 100, 1000, 10000}`.
- Fit `n_e(t) / n_e(0) = α · exp(β·t)` with scipy `curve_fit`.
- Compare `β` across `N_c`; check computational-count bounds.
- Output: `evidence/growth_independence.json`.

## 5. Precision sub-claim probe (`work/test_growth_stochastic.py`)

- Added Poisson ionization noise to try to isolate C7 (precision-improves-with-N_c).
- **Could not isolate:** abstract 0D bookkeeping recovers `β` to machine precision at every `N_c` because it lacks Aleph's stochastic DSMC event noise. Reported honestly rather than over-claimed.
- Output: `evidence/growth_stochastic.json`.

## 6. LLM-judge (`work/judge_prompt.txt`)

- Free Argo `gpt-5.2` at `http://localhost:44497/v1`.
- Fed all seven claims + all measured results + self-reported limitations.
- Structured JSON verdict.
- Output: `evidence/llm_judge_verdict.json` → coverage 0.78, agreement 0.80, verdict PARTIAL.

## 7. Report + backfill

- Primary replication report: `report/REPORT.md` (native), `report/REPORT.tex` (LaTeX, this backfill).
- Backfill artifacts (2026-07-06): `open_questions.json`, `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd` (placeholder stub).
- No simulations were rerun during backfill; no existing artifacts were overwritten.

## Reproduce this replication (skeleton)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/OSTI-2480245-energy-conserving-particle-reweighting-PIC/work
python3.14 -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # numpy 2.5.0, scipy 1.18.0
python test_conservation.py         # → evidence/conservation_results.json
python test_growth_independence.py  # → evidence/growth_independence.json
python test_growth_stochastic.py    # → evidence/growth_stochastic.json
# Judge (free Argo gpt-5.2 at localhost:44497 required):
python judge_run.py                  # → evidence/llm_judge_verdict.json
```
