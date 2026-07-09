# FNO / NeuralOperator Replication — PROGRESS

**Started:** 2026-05-28 12:12 CDT
**Finished:** 2026-05-28 12:23 CDT (≈11 min total wall-clock)
**Subagent:** Ollie (Claude Opus 4.7 via Argo)
**Target:** `neuraloperator/neuraloperator` (FNO, MIT license, PyTorch Ecosystem)
**Task choice:** Darcy flow 2-D (non-climate elliptic PDE)
**Compute target:** CPU on cherryrd (no GPU needed at small scale)

## Plan vs. actual

| Step | Planned | Actual | Notes |
|------|---------|--------|-------|
| Verify license + repo health | ✅ | ✅ | MIT confirmed; 3.6k★, last commit today |
| Set up venv + deps | ✅ | ✅ | `uv venv` Python 3.12, `uv pip install neuraloperator matplotlib torch` |
| Resolve install friction | — | ⚠️ | NumPy 2 ABI vs torch 2.2.2 — pinned `numpy<2` |
| Get small public dataset | ✅ | ✅ | `load_darcy_flow_small` (bundled, ~30 MB from HF) |
| Sanity train (2 ep) | ✅ | ✅ | 53 s, rel-L2 0.44 → confirms working |
| Full train (20 ep) | ✅ | ✅ | **184 s, rel-L2 0.121 @ 16² / 0.144 @ 32² (Trainer L2)** |
| Figures (in-dist + super-res) | ✅ | ✅ | `figures/darcy_{16,32_zeroshot}.png` |
| Machine-readable metrics | ✅ | ✅ | `results/metrics.json` |
| REPORT.md with claim table | ✅ | ✅ | 4/4 claims PASS, strong agreement |

## Headline numbers

| Metric | Value |
|--------|-------|
| Model | FNO(8 modes, 24 hidden) — 191,881 params |
| Train data | 1000 samples @ 16×16 Darcy permeability→pressure |
| Train time | 183.8 s on CPU (20 epochs) |
| Rel-L2 @ 16² (in-dist) | **0.121** (Trainer LpLoss) / 0.185 (custom) |
| Rel-L2 @ 32² (zero-shot SR) | **0.144** (Trainer LpLoss) / 0.228 (custom) |
| Pre-training rel-L2 | ≈ 1.0 (random model) → 5× reduction post-training |
| Verdict | **PASS, strong agreement at tutorial scale** |

## Log

- 12:12 — created scaffolding, wrote initial PROGRESS + JSON state.
- 12:13 — confirmed MIT license + active repo via GitHub API.
- 12:14 — pulled `examples/models/plot_FNO_darcy.py` (303 lines) as the canonical example.
- 12:15 — created venv, installed `neuraloperator` (pulls torch 2.2.2).
- 12:16 — hit NumPy 2 vs torch 2.2.2 ABI mismatch; downgraded numpy to 1.26.4. Friction logged.
- 12:16 — wrote `scripts/train_fno_darcy.py` (non-interactive, seeded, dumps JSON + figures).
- 12:17 — 2-epoch sanity passed (rel-L2 0.44 in 53 s).
- 12:20 — 20-epoch full run completed in 184 s.
- 12:22 — wrote README.md, REPORT.md, finalized PROGRESS.md.
- 12:23 — done; updated subagent-progress JSON to status=done.

## Artifacts

```
fno-neuraloperator/
├── README.md           # how to run, what's where
├── REPORT.md           # full claim-by-claim report
├── PROGRESS.md         # this file
├── scripts/
│   └── train_fno_darcy.py
├── logs/
│   ├── sanity_2ep.log
│   └── train_20ep.log
├── results/
│   └── metrics.json
├── figures/
│   ├── darcy_16.png
│   └── darcy_32_zeroshot.png
└── .venv/              # local Python env (not part of report)
```
