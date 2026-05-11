# Replication: ML-Accelerated CFD (Kochkov et al., PNAS 2021)

**Paper:** Kochkov, D. et al. "Machine learning–accelerated computational fluid dynamics." PNAS 118(21), 2021.  
**Citations:** ~1123  
**Repository:** https://github.com/google/jax-cfd

## Summary

This replication verifies the paper's core claim: a learned interpolation (LI) scheme on a 64×64 grid achieves accuracy comparable to DNS at 256×256 resolution, at ~23× lower computational cost.

## Key Results

| Model | Vorticity corr @ t=2 | Vorticity corr @ t=5 | Decorrelation time (>0.95) | Cost/step |
|-------|---------------------|---------------------|---------------------------|-----------|
| LI(64) | 0.990 | 0.856 | 3.93 | 0.670 ms |
| DNS64 | 0.929 | 0.542 | 1.68 | 0.242 ms |
| DNS128 | 0.980 | 0.782 | 2.88 | ~1.93 ms |
| DNS256 | 0.996 | 0.931 | 4.63 | ~15.5 ms |

## Reproducibility

- **Training:** 22 min on 1× A100 (4,000 steps with curriculum learning)
- **Evaluation:** 8 independent ICs, 201 frames each
- **Environment:** JAX 0.10.0, CUDA 12, Python 3.11

## Structure

```
replication/
├── train_li.py         # Training script with curriculum learning
├── evaluate.py         # Evaluation: correlation, spectra, timing
├── li_config.gin       # Gin configuration for LI model
├── results/            # Plots and numerical results
│   ├── vorticity_correlation.png
│   ├── energy_spectrum.png
│   ├── pareto.png
│   ├── vorticity_snapshots.png
│   └── results.npz
└── report/
    └── report.pdf      # 5-page replication report
```

## Self-Assessment (post 2026-04-28 gap-fill)

- **Coverage:** 9/10 — Re=1000 + Re=4000 + decaying turbulence all replicated
  end-to-end. Re=7000 documented as known gap (see REPORT.md).
- **Agreement:** 8/10 — Quantitative agreement excellent at Re=4000 (LI(128) sits
  between DNS256 and DNS512 in correlation); qualitative agreement on decaying
  turbulence (LI(64) ≈ DNS128).

See top-level `REPORT.md` for the gap-fill pass details and `replication/results_high_re.json`
+ `replication/results_decaying.json` for machine-readable summaries.

## How to Run

```bash
# On a machine with GPU and internet access
pip install "jax[cuda12]" jax-cfd[complete] optax dm-haiku

# Train (adjust --steps and --curriculum as needed)
python replication/train_li.py --steps 4000 --batch 8 --inner 4

# Evaluate
python replication/evaluate.py --ckpt checkpoints/li_re1000.pkl
```
