# Workflow — QC-2207.06431 Google Surface Code replication

## Timeline (2026-07-05, single subagent turn, ~10 min wall clock)

1. **T+0:00** — Read `QC_WAVE_BRIEF_2026-07-03.md`, created target directory tree.
2. **T+0:30** — `curl` arXiv PDF (`https://arxiv.org/pdf/2207.06431`, 12.4 MB, SHA256 `38e1fc02…22896`).
3. **T+1:00** — `pdftotext -layout paper.pdf work/paper.txt` (2754 lines); grepped for `lambda|threshold|logical error|per cycle|per round` to lock the headline numbers.
4. **T+2:00** — Extracted headline claims into `extraction/marker.md` and `extraction/nougat.mmd` (Marker/Nougat proper skipped because their PyTorch model install would exceed the subagent's time budget; documented substitution).
5. **T+3:00** — Created `.venv` (Python 3.14.6), `pip install stim pymatching numpy matplotlib`.
6. **T+3:45** — Wrote `report/evidence/surface_code_sim.py`: rotated-memory-Z surface-code circuits via `stim.Circuit.generated`, 4-knob uniform circuit-level depolarizing noise, DEM → PyMatching MWPM decoder, per-round rate via `eps = 1 - (1-p_L)^(1/r)`. Sweep over `d ∈ {3,5,7}` × `p ∈ {1e-3, 3e-3, 5e-3, 1e-2, 2e-2}` with per-config shot budget tuned so `# logical errors ≥ 29` in the worst corner.
7. **T+5:00** — Ran sim (80.8 s wall). Saved `results.json`, `results.csv`, `sim_run.log`, plus `example_circuit_d5_r25_p1e-3.stim`.
8. **T+7:00** — Wrote `report/evidence/make_plots.py`, produced `fig_eps_vs_p.{png,pdf}` and `fig_lambda_vs_p.{png,pdf}`.
9. **T+8:00** — Wrote `report/REPORT.tex` (verdict + claims table + method + results + Open Questions section).
10. **T+9:00** — Wrote `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
11. **T+10:00** — Final artifact audit, compile LaTeX if `pdflatex` available.

## Tools + versions
| Tool | Version | Role |
|------|---------|------|
| Python | 3.14.6 | venv interpreter |
| stim | 1.16.0 | Clifford + noise circuit builder, syndrome sampler, DEM |
| pymatching | 2.4.0 | MWPM decoder (`Matching.from_detector_error_model`, `decode_batch`) |
| numpy | 2.5.1 | array ops |
| matplotlib | latest at install | figure rendering |
| poppler `pdftotext` | (system) | linearized text extraction |
| `curl` | (system) | PDF fetch |
| `shasum` | (system) | integrity |

## Compute
- **Host:** CherryRd (Mac, M-series Apple silicon, CPU only for this sim).
- **Wall clock:** ~80 s for the full 15-config sweep (Stim + PyMatching are extremely fast; the whole sweep would run in ~2 min on any laptop).
- **LLM inference:** 0 tokens — no LLM judge invoked (Argo would be free; results are self-checkable against the paper's own quantitative headline).

## Estimated work
- Discovery + reading: ~15 min human-equivalent (paper skim, key-number lock).
- Coding: ~30 min (write + debug sim + plots).
- Reporting: ~30 min (LaTeX + JSON + inventory).
- Total: ~1.5 h human-equivalent, delivered in ~10 min subagent wall clock.

## Data lineage
```
arXiv:2207.06431 (upstream, unmodified)
   ├── paper.pdf                                     (12.4 MB, SHA256 recorded)
   └── work/paper.txt                                (pdftotext, 2754 lines)
         └── extraction/marker.md, extraction/nougat.mmd  (curated highlights)

Stim + PyMatching sim (report/evidence/surface_code_sim.py)
   └── results.json, results.csv, sim_run.log, example_circuit_d5_r25_p1e-3.stim
         └── make_plots.py → fig_eps_vs_p.{png,pdf}, fig_lambda_vs_p.{png,pdf}
               └── REPORT.tex, open_questions.json
```

## Reproducibility (one-command replay)
```bash
cd QC-2207.06431-google-surface-code-logical-qubit
python3 -m venv .venv && source .venv/bin/activate
pip install stim==1.16.0 pymatching==2.4.0 numpy matplotlib
python report/evidence/surface_code_sim.py    # 80 s, deterministic seeds
python report/evidence/make_plots.py
```
