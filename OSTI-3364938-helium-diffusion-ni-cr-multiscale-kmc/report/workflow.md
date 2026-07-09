# Workflow — OSTI-3364938 replication

## Pipeline

```
1. Fetch OSTI PDF                (uicgpu curl + scp,               ~5 s)
2. Extract paper text            (pdftotext -layout,               ~2 s)
3. Read + summarize paper claims (manual + LLM assist,            ~15 min)
4. Implement two ROMs            (rom_models.py, ~200 loc,        ~10 min)
5. Run ROMs sweep 0-12% at 600K  (local Python, ~1 s)
6. Implement vectorized KMC      (kmc_he_nicr_v2.py, ~350 loc,    ~30 min)
7. Sweep KMC c_Cr = 0-12%        (uicgpu, 12 concs, ~12 s)
8. T-sweep KMC 700/800/1000 K    (uicgpu, ~40 s total)
9. Comparison plots + CSV        (make_figures.py, matplotlib,    ~5 s)
10. LLM-judge verdict            (Argo argo:gpt-5.2,              ~90 s)
11. Write REPORT.md/tex, QAs     (manual, ~25 min)
```

Total wall-clock ≈ 1.5 h. Total compute negligible (< 1 min CPU on uicgpu).

## Tools + codes

| Tool | Purpose | Version |
|---|---|---|
| `curl` (via uicgpu) | Fetch OSTI PDF | 8.x |
| `scp` | Move PDF to Dropbox | OpenSSH 9 |
| `pdftotext` (poppler) | Text extraction | 25.02 (local) / 22.02 (uicgpu) |
| Python | All numerics | 3.14 (local) / 3.8 (uicgpu) |
| NumPy | Vectorized KMC | 2.x (local) / 1.23.5 (uicgpu) |
| SciPy cKDTree | PBC-aware nearest-Cr for shell map | 1.x |
| Matplotlib | Comparison figures | 3.x |
| Argo proxy `localhost:44497` (FREE) | LLM judge | argo:gpt-5.2 |
| `rom_models.py` | Independent simplified-MF & modified-Oriani | v1 (2026-07-06) |
| `kmc_he_nicr_v2.py` | Independent residence-time KMC (percolation-aware) | v2 (2026-07-06) |
| `make_figures.py` | Plotting + summary CSV | v1 |
| `llm_judge.py` | Argo verdict script | v1 |

## Effort estimate

- **~1.5 h wall-clock** for a single independent replicator with the paper open.
- **~1 min compute** on uicgpu (255-core AMD box; single-thread runs).
- **Zero paid API calls** — Argo proxy only (per project rules).

## Compute topology

- Paper PDF download and KMC production runs: `uicgpu` (Tailscale
  <tailnet-uicgpu>), source `~/env.sh` for proxy internet.
- ROM sweep and figure generation: local (macOS on CherryRd) — trivial.
- LLM-judge (Argo): local via ssh tunnel to `localhost:44497`.

## Reproducibility notes

- KMC RNG seed = `42 + int(c_Cr*100)` per concentration (deterministic).
- All figures + CSV + JSON verdict live under `report/evidence/`.
- Scripts under `work/` are self-contained (paper Table I/II values are
  hard-coded so no re-parse of PDF is needed).
