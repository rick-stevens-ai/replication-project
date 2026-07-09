# Artifact harvest — OSTI-3364938

## Public artifacts pulled

| Item | URL | Local path | Size | sha256 | Retrieved |
|---|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3364938 | `paper.pdf` | 2.2M | 816a15f3454ef35f9e286b8fad67832f233211a26c209db284c14f0964af7c4d | 2026-07-06 06:12 CDT (uicgpu) |

## Data / code repositories
None referenced. Paper's "Data availability statement" says data available
from corresponding authors upon reasonable request. No public GitHub or
Zenodo repository is cited in the paper.

## Inputs to replication that were NOT downloaded (transcribed from paper)
- Table I: He IFEs at 1NN-4NN T/O sites in Ni-Cr, plus pure-Ni references
- Table II: He interstitial diffusion energy barriers (12 values)
- Text §3.2: in-basin barriers 0.034/0.054 eV; exit barriers 0.27/0.36 eV;
  bulk T-O'-T barrier 0.086 eV; direct 1NN-O to 1NN-O barrier 0.32 eV
- Text §2.2: attempt frequency nu_0 = 1e12 s^-1, T = 600 K nominal, cubic
  box 80 a0, 10 Cr distributions x 160 He seeds = 1600 trajectories per
  data point
- Table III: paper's own AKMC results, used as ground truth for comparison

All transcriptions live in `work/rom_models.py` and `work/kmc_he_nicr_v2.py`
as clearly commented constants (`BARRIER`, `IFE`, `Nti_per_Cr`, etc.).

## API endpoints hit
- Argo proxy `localhost:44497` (FREE, per project rules)
  - model `argo:gpt-5.2` for LLM-judge scoring
  - one call, ~1000 output tokens, ~90s
