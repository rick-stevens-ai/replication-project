# Workflow — QC-0810.4968-quantum-algorithms-curvelet-transform-liu

## Timeline (single subagent session, ~1 hour, 2026-07-05)

1. **Fetch + verify the paper.** Downloaded `https://arxiv.org/pdf/0810.4968` to `work/paper.pdf`, `pdftotext -layout` → `work/paper.txt` (4148 lines / 64 pages). Verified authors from the PDF (Yi-Kai Liu, Caltech IQI; arXiv 0810.4968v2, Mar 25 2009) — matches the assignment.
2. **Extract the claim.** Skimmed Sec 6.1–6.2 (discrete curvelet transform definition, eq. 14) and Sec 7.1–7.2 (Algorithms 1 and 2). Identified three testable claims and one conjectural one.
3. **Environment setup.** Created `work/venv/` with numpy 2.5.1, scipy 1.18.0, matplotlib 3.10.8, qiskit 2.5.0, qiskit-aer 0.17.2, pymupdf 1.28.0. All CPU-only.
4. **Classical baseline.** Wrote `report/evidence/classical_curvelet.py` — a dyadic partition-of-unity (Case-1 indicator windows) curvelet transform in 1D and 2D. Verified three algebraic properties (partition of unity, norm preservation, exact inversion) on N=16..128 (1D) and N=8..32 (2D). All errors at machine ε.
5. **Quantum circuit.** Wrote `report/evidence/quantum_curvelet.py` — Qiskit statevector implementation of Liu's Sec 6.2 recipe (QFT → sector-index lookup gate X → inverse QFT). Debugged Qiskit's +i / -i QFT convention against numpy's -i / +i FFT convention (fix: swap forward and inverse QFT roles). Verified quantum output amplitudes match classical baseline to <1.2e-15 max abs diff on random inputs for N=8, 16, 32.
6. **Center-of-ball application.** Wrote `report/evidence/center_of_ball.py` — Liu's Algorithm 1 in n=2 on a discrete grid, applied to indicator functions of balls. Measured (a) mass in directional sectors vs. low-freq disk (81–89% directional, qualitatively consistent with Liu Thm 3), (b) empirical line-through-center probability (curvelet 3–8× better than random-point baseline on the "distance from line to true center ≤ 1 grid unit" metric).
7. **Extraction artifacts.** No Marker/Nougat available locally; produced honest substitute extractions from `pdftotext -layout` (`extraction/marker.md`, 148 KB) and pymupdf (`extraction/nougat.mmd`, 148 KB) with a provenance disclaimer in `extraction/README.md`.
8. **Report writing.** `report/REPORT.tex` (this section-by-section per-claim summary), `report/open_questions.json` (5 non-superficial questions), `report/failure_analysis.md`, `report/artifacts_summary.md`, `report/workflow.md`.

## Tools + versions

| Tool | Version | Purpose |
|------|---------|---------|
| python | 3.13 | orchestration |
| numpy | 2.5.1 | classical FFT + partition-of-unity math |
| scipy | 1.18.0 | (present but not needed after design) |
| qiskit | 2.5.0 | quantum circuit + gate set |
| qiskit-aer | 0.17.2 | statevector simulation |
| pymupdf | 1.28.0 | Nougat substitute extraction |
| poppler (pdftotext) | system | Marker substitute extraction; PDF → text for skimming |
| curl | system | arXiv PDF download |

## Not used / not available
- **Marker** (VikParuchuri/marker) — not installed, model download would exceed subagent scope.
- **Nougat** (facebook/nougat-base) — not installed, model download would exceed scope + old PyTorch pin.
- **PyWavelets / PyLops** — considered as a curvelet ground-truth but PyWavelets does NOT ship a curvelet primitive; there is no free canonical Python curvelet library (Cand`es et al. CurveLab is MATLAB, non-open license). Instead we verified curvelet properties directly against algebraic identities (partition of unity → unitarity → exact inversion), which is stronger than a code-vs-code check.
- **Argo LLM** — not used for scoring in this run; verdict is self-issued based on measured numerics.
- **GPU / HPC** — not used; whole pipeline runs on a single CPU in ~30 s.

## Estimated real work
~1 hour of a subagent, ~30 seconds of CPU total for all three evidence scripts.
