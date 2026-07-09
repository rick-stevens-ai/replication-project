# Artifacts summary — QC-2007.11157

All paths are relative to `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2007.11157-teleportation-quantum-internet-valivarthi/`.

## 8 mandated artifacts (Rick 2026-07-05 standard)

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Original PDF | `paper.pdf` | ✅ (931,900 B, SHA-256 d83389f3…7e17a95d) |
| 2 | Marker parse | `extraction/marker.md` | ✅ (curated substitution; documented) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ (curated substitution; documented) |
| 4 | LaTeX report | `report/REPORT.tex` | ✅ (verdict = PARTIAL) |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✅ (5 grounded questions) |
| 6 | Workflow | `report/workflow.md` | ✅ (timeline + tools + versions + effort) |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Simulation evidence (under `report/evidence/`)

| File | Description |
|------|-------------|
| `teleport_sim.py` | Main 3-qubit BBCJPW teleportation + noise-regime simulation (12 KB). |
| `make_plots.py` | 25-point dephasing sweep + figure generator. |
| `results.json` | Full ideal + 3-regime noisy fidelity results with paper anchor. |
| `results.csv` | CSV summary (regime, lambda_pd, mean_F). |
| `sim_run.log` | Live log of the main simulation run. |
| `sweep.json` | 25-point lambda_pd sweep data. |
| `fig_fidelity_vs_noise.png` | Sweep plot with paper's F=0.89 anchor + classical F=2/3 limit. |
| `fig_fidelity_vs_noise.pdf` | Vector version of the same figure. |
| `example_circuit_plus.qasm` | OpenQASM 2.0 dump of the teleportation circuit for the |+> input. |
| `example_circuit_plus.txt` | Human-readable circuit diagram. |

## Working files (under `work/`)

| File | Description |
|------|-------------|
| `paper.txt` | `pdftotext -layout` extraction of the full paper. |

## Provenance chain

```
arXiv:2007.11157
  → paper.pdf (verified via SHA-256)
    → work/paper.txt (poppler pdftotext -layout)
      → extraction/marker.md + extraction/nougat.mmd (curated)
        → report/evidence/teleport_sim.py (fixed seed 20260705)
          → results.json + results.csv + sim_run.log
            → make_plots.py → fig_fidelity_vs_noise.{png,pdf} + sweep.json
              → REPORT.tex + open_questions.json + workflow.md + artifacts_summary.md + failure_analysis.md
```

## Headline reproduction

- **Ideal-protocol fidelity:** $\langle F \rangle = 1.000000000000$ across 10 input states (matches paper's protocol target).
- **Noise-swept fidelity crosses paper's F = 0.89 anchor at lambda_pd ~ 0.24.**
- **Verdict:** PARTIAL (protocol + model-consistency reproduced; hardware numbers out of scope).
