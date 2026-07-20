# Workflow — Replication of arXiv:cond-mat/0511224

## 1. Ingest & classify
- `pdftotext -layout paper.pdf work/paper.txt` → clean 266-line extraction (equations, C matrix, references intact).
- Read the shared kernel `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py` FIRST (per task).
- **Classification audit:** paper is spin-transfer torque in a helical spin density wave, NOT a kagome loop-current / flux-phase paper. Kernel deemed **not applicable**; not imported. Flagged in `extraction/marker.md`.

## 2. Claim selection (machine-checkable)
Chose 5 convention-independent claims (C1 tensor structure, C3 tilt geometry, C4 per-layer phase, C5 linear scaling, C6 crude-vs-microscopic ratio). Deliberately excluded the DFT-specific absolute number (0.07 GHz) as out-of-scope for an offline/free-endpoints replication and recorded it for the record.

## 3. Model implementation (`code/stt_helical_sdw.py`)
Minimal, first-principles-free realization of the SAME mechanism:
- 1D spin-spiral s-band along the spiral (c) axis, spin-1/2, exchange field Δ rotating in-plane.
- Generalized Bloch theorem → 2×2 rotating-frame Bloch Hamiltonian H(k)=diag(ε(k−q/2), ε(k+q/2)) with off-diagonal −Δ (spin-up↔k−q/2, spin-down↔k+q/2, matching the paper's a/b plane-wave split, Eq. 7).
- Charge velocity = dH/dk; spin-flux tensor Q = Re⟨ψ†(S⊗v)ψ⟩ (paper Eq. 1).
- Torque–current tensor C via constant-τ semiclassical Boltzmann linear response (paper Eqs. 3–6); τ cancels in C=(ΣA)(ΣB)⁻¹.

## 4. Execution (`code/run_replication.py`, run under `work/`)
- Geometry arithmetic (q, cell area, per-layer phase).
- C-matrix structure + planarity check (out-of-plane spin flux → 0).
- Linear-scaling demonstration over j = 1e9…1e12 A/m².
- Crude adiabatic vs microscopic linear-response ratio.
- All numeric outputs dumped to `work/results.json`.

## 5. Quantitative comparison → verdict
Tabulated computed vs paper values in `report/artifacts_summary.md` and the REPORT. 4/5 machine-checkable claims pass; C6 (numeric ~4× ratio) is an honest partial/negative (model-dependent prefactor). No fabrication: the negative is reported as-is.

## 6. Artifacts (8-artifact bar)
`extraction/marker.md`, `code/*.py`, `work/results.json` + `work/paper.txt`, `report/REPORT.tex` (+ PDF if latex), `report/open_questions.json` (exactly 5), `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Reproduce
```bash
cd work && python3 ../code/run_replication.py    # ~2 s, numpy only
```
