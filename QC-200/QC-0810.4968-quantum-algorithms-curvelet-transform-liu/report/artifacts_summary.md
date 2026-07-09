# Artifacts Summary — QC-0810.4968

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0810.4968-quantum-algorithms-curvelet-transform-liu/`

## Required 8-artifact bar (per `QC_WAVE_BRIEF_2026-07-03.md`)

| # | Artifact | Path | Present | Notes |
|---|----------|------|---------|-------|
| 1 | `paper.pdf` | `paper.pdf` (600,675 B, 64 pp) | ✔ | Downloaded from arxiv.org/pdf/0810.4968, verified Yi-Kai Liu (Caltech IQI) |
| 2 | `extraction/marker.md` | `extraction/marker.md` (~148 KB) | ✔ *(substitute)* | `pdftotext -layout` fallback; Marker not installed. See `extraction/README.md`. |
| 3 | `extraction/nougat.mmd` | `extraction/nougat.mmd` (148,512 B) | ✔ *(substitute)* | pymupdf fallback; Nougat not installed. See `extraction/README.md`. |
| 4 | `report/REPORT.tex` | `report/REPORT.tex` | ✔ | Section-by-section per-claim replication with numeric checks; `REPORT.pdf` compiled if pdflatex available. |
| 5 | `report/open_questions.json` + `## Open Questions` in report | `report/open_questions.json` (5741 B) | ✔ | Five NON-superficial questions grounded in what was actually observed in this replication. |
| 6 | `report/workflow.md` | `report/workflow.md` | ✔ | Tools/versions + timeline + estimated work. |
| 7 | `report/artifacts_summary.md` | this file | ✔ | You are here. |
| 8 | `report/failure_analysis.md` | `report/failure_analysis.md` | ✔ | Honest gaps + friction points. |

## Evidence code + numeric results

| Path | Kind | Bytes | Description |
|------|------|-------|-------------|
| `report/evidence/classical_curvelet.py` | Python | 9556 | 1D + 2D discrete curvelet transform via dyadic partition-of-unity; algebraic self-tests |
| `report/evidence/classical_curvelet_results.json` | JSON | – | Partition-of-unity, norm-preservation, inversion errors at N=8..128 (1D) and N=8..32 (2D) — all machine-ε |
| `report/evidence/quantum_curvelet.py` | Python | 6404 | Qiskit statevector circuit (QFT → sector-lookup gate X → iQFT); compares to classical baseline |
| `report/evidence/quantum_curvelet_results.json` | JSON | – | Max amplitude diff quantum-vs-classical: 5.7e-16, 6.8e-16, 1.1e-15 for N=8, 16, 32 |
| `report/evidence/center_of_ball.py` | Python | 7935 | Liu Algorithm 1 in n=2; ball indicator → quantum curvelet → line-through-center metric |
| `report/evidence/center_of_ball_results.json` | JSON | – | P(directional sectors) 81–89%, curvelet 3–8× better than random on line-distance-≤1 metric |

## Intermediate + auxiliary
- `work/paper.pdf` — verbatim arXiv PDF (same bytes as `paper.pdf`)
- `work/paper.txt` — `pdftotext -layout` of paper.pdf, used for skimming
- `work/venv/` — throwaway venv (not tracked; can be rebuilt via `python3 -m venv work/venv && source work/venv/bin/activate && pip install numpy scipy matplotlib qiskit qiskit-aer pymupdf`)
- `extraction/README.md` — provenance disclaimer for the marker.md / nougat.mmd substitutes
- `extraction/make_nougat_substitute.py` — pymupdf → nougat.mmd generator

## Reproduce all numbers

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0810.4968-quantum-algorithms-curvelet-transform-liu
source work/venv/bin/activate

python report/evidence/classical_curvelet.py    # verifies partition-of-unity + isometry
python report/evidence/quantum_curvelet.py      # verifies quantum ≡ classical to <1.2e-15
python report/evidence/center_of_ball.py        # empirical center-of-ball test in n=2
```

Total wall clock: about 30 seconds on a laptop CPU.
