# Artifact Harvest — OSTI-2588304

## Original paper
- `work/2588304.pdf` — 6.77 MB — Sandia SAND2025-11245J preprint via OSTI cache.

## Code (upstream reference, cloned)
- `report/evidence/cgcnn/` — `git clone --depth 1 https://github.com/txie-93/cgcnn.git` (Xie & Grossman 2018 CGCNN reference implementation, the exact code the paper cites).

## Real DFT data (v2, added 2026-07-04)
- **Source:** Materials Project OPTIMADE endpoint `https://optimade.materialsproject.org/v1/structures` (public, no API key)
- **Harvest script:** `work/harvest_optimade.py`
- **Raw JSON:** `work/mp_hydrides.json` — 86 records
- **CGCNN-format dataset:** `report/evidence/dataset_real_mp/` — 86 CIFs + `id_prop.csv` + `atom_init.json`
- **Filter:** binary M-H or ternary M-H-N with M ∈ {Lu, Y, Sc, La, Ce, Pr, Nd, Sm, Gd, Er, Yb, Ti, Zr, Hf, V, Nb, Ta}, `nsites ≤ 60`
- **Property:** `formation_energy_per_atom` from `_mp_stability.gga_gga+u` (matches paper's PBE)
- **Range:** −0.816 to +0.382 eV/atom
- **Lu-H specifically:** 3 entries only (`mp-24288`, `mp-865610`, `mp-1191245`)

## Rare-earth family subset
- **Dataset:** `report/evidence/dataset_rareearth_h/` — 51 CIFs (subset of the 86)
- **Filter:** at least one element in {Lu, Y, Sc, La, Ce, Pr, Nd, Sm, Gd, Er, Yb}

## Synthetic pseudo-DFT (v1)
- **Generator:** `report/evidence/make_dataset.py`
- **Dataset:** `report/evidence/dataset_lu_h_n/` — 1000 CIFs
- **Rationale:** paper's SI CIFs are locked in a PDF; this is a topology-preserving pseudo-DFT stand-in with the same qualitative Fig-2a energetic structure.

## Trained CGCNN models
- `report/evidence/model_best.pth.tar` — 81 KB — best val checkpoint (most recent run: real MP 86-config dataset).
- `report/evidence/checkpoint.pth.tar` — 81 KB — last-epoch checkpoint (same run).

## Data NOT obtained (blockers logged in attempt_log.md)
- Paper SI (`10.26434/chemrxiv-2024-6g37p` supplement) — Cloudflare gate on ChemRxiv, OSTI API DNS failed on this host.
- ASAP MC (`gitlab.com/asap/asap`) — not installed; wrote independent Metropolis MC in `mc_free_energy.py`.

## LLM-judge artifact
- `report/evidence/llm_judge_verdict.txt` — Argo `gpt-4.1` independent per-claim scoring, verdict PARTIAL.

## Reproducibility hash
- Data seeds: `20260703` (synthetic dataset build), `20260704` (MC).
- Numpy/Torch RNG default (CGCNN's own random split).
