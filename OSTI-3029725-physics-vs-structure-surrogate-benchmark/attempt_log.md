# Attempt Log — OSTI 3029725

## Environment
- Host: `uicgpu` (8×A100), CUDA_VISIBLE_DEVICES=0
- Workdir: `/tmp/osti3029725/`
- Python 3, PyTorch, single-GPU

## Timeline
1. **Setup** — fetched paper PDF (`work/paper.pdf`), authored `repro.py` implementing the RC building proxy simulator plus all 11 model variants (LSSM, MLP, NSSM, NODE, PCNN, LSSM-EncDec × {WBM, IZM}, minus PCNN-IZM which has an incompatible energy-balance parameterisation).
2. **Smoke run** — `results_smoke.json` (few epochs) confirmed models train and the WBM/IZM plumbing works.
3. **20-epoch check** — `results_20.json` confirmed IZM helps every model class in the same direction as paper.
4. **100-epoch canonical run** — `python3 -u repro.py --seed 0 --epochs 100 --out results_100.json > run_100.log`, launched via `nohup`. Original driver session hit its own wall-clock timeout while the training was still going.
5. **Finisher (this session)** — polled the running process on uicgpu, waited for the final two models (LSSM-EncDec-WBM, LSSM-EncDec-IZM) to finish, then pulled `results_100.json`, `run_100.log`, `repro.py`, and the earlier smoke/20-epoch JSONs into `report/evidence/` and `work/`, and wrote the report.

## Honest deltas vs the paper
- **Simulator**: 5-zone 2R2C RC proxy — not the paper's EnergyPlus co-simulation. Absolute MAEs are therefore not directly comparable; only directions are.
- **Data volume**: 672 train / 672 val / 672 shoulder-test / 672 cooling-test steps — much smaller than the paper's dataset.
- **No 50-model seed averaging**: single seed=0. The paper reports mean over 50 random initialisations; we do not, so per-model variance is not characterised.
- **No PCNN-IZM**: PCNN's energy-balance parameterisation in our implementation is coupled to the WBM operator; we did not port it to the IZM sparsity mask.

These decisions were made explicit so that a PARTIAL verdict on directions-not-magnitudes is honest, not a hidden gap.
