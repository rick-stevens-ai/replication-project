# Open-artifact PDE/scientific-computing batch 3 launch — 2026-05-28 12:10 CDT

Rick said: "okay lets go" after reviewing the open-artifact candidate list.

## Targets
1. `pdebench` — PDEBench: An Extensive Benchmark for Scientific Machine Learning; public repo/data.
2. `fno-neuraloperator` — Fourier Neural Operator / NeuralOperator; MIT repo, generated/public PDE data.
3. `fipy` — FiPy finite-volume PDE solver; NIST open-source examples.
4. `pyclaw` — PyClaw/Clawpack hyperbolic PDE solver; public examples.
5. `wavetrain-scikit-tt` — WaveTrain/scikit_tt tensor-train quantum dynamics; repo + Zenodo signal.

## Rules
- Skip climate papers and climate datasets.
- Open data/open-source only. Verify license before claiming PASS.
- If a repo/package artifact is not open or unavailable, stop and propose replacement; do not pivot to closed data.
- Free LLM endpoints only: `argo/argo:claude-opus-4.7`.
- Output dirs under `~/Dropbox/REPLICATE-PROJECT/PDE-replications/<slug>/`.
- Progress JSON under `~/.openclaw/workspace/memory/subagent-progress/<slug>.json`.
- Write PROGRESS.md + progress JSON within 10 minutes.
