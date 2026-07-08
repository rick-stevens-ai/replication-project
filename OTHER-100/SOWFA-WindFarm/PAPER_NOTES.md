# PAPER_NOTES.md — Slot G-RETRY (SOWFA-class wind-farm LES NN-surrogate replication)

**Slot:** G-RETRY (P077 reinforcement)
**Author (Ollie):** subagent run, 2026-05-27
**Reporting dir:** `~/Dropbox/REPLICATE-PROJECT/SOWFA-WindFarm/`
**Workspace name kept:** "SOWFA-WindFarm" although the paper used is PyWake-based, not strict-SOWFA LES. See "Pivot rationale" below.

---

## 1. Target paper (selected)

**Title:** "Local flow and loads estimation on wake-affected wind turbines using graph neural networks and PyWake"

**Authors:** G. Duthé, F. de Nolasco Santos, I. Abdallah, P.-É. Réthoré, W. Weijtjens, E. Chatzi, C. Devriendt
**Venue:** Journal of Physics: Conference Series, Vol. 2505, No. 1, p. 012014 (WAKE conference / Wind Energy Science)
**Year:** 2023 (May)
**DOI:** [10.1088/1742-6596/2505/1/012014](https://doi.org/10.1088/1742-6596/2505/1/012014)
**Open-access PDF:** https://iopscience.iop.org/article/10.1088/1742-6596/2505/1/012014/pdf (IOP open-access; behind Radware bot wall via curl, but accessible in browsers)

**Companion paper (same repo, fuller method):**
> Duthé G, de N Santos F, Abdallah I, Weijtjens W, Devriendt C, Chatzi E. **"Flexible multi-fidelity framework for load estimation of wind farms through graph neural networks and transfer learning."** *Data-Centric Engineering* (Cambridge UP) 2024;5:e29. DOI: [10.1017/dce.2024.35](https://doi.org/10.1017/dce.2024.35)

These two papers share the same code repo (`gduthe/windfarm-gnn`), and the DCE 2024 paper is the fuller version of the 2023 conference paper. We will primarily target the **2023 Duthé paper's headline metrics**, but rely on the more complete training infrastructure documented in the DCE 2024 paper for reproduction.

## 2. Pivot rationale (vs. brief's "EllipSys3D LES" framing)

The brief named Duthé 2023 as "Applied Energy, EllipSys3D LES." This appears to be a misattribution: **Duthé 2023 is in J. Phys. Conf. Ser., and its training data is PyWake (engineering wake model), not EllipSys3D LES.** The Duthé group's other 2024 work (Multivariate prediction… EURODYN) does explore higher fidelities, but the public dataset/code uses PyWake.

**Decision:** Adopt the actual Duthé 2023 paper (PyWake-based) as the target. The brief explicitly mentions PyWake+windfarm-gnn as the fallback — but Duthé 2023 itself uses PyWake, so primary and fallback collapse into the same repo. This eliminates the data-blocker risk entirely.

**Honesty note for REPORT.md:** PyWake is an engineering wake model (Gaussian deficits, dynamic wake meandering), not LES. So this slot is NOT a SOWFA/EllipSys3D LES surrogate replication — it is a *wake-model surrogate replication*. The GNN learns to mimic PyWake's outputs (power, rotor-avg wind speed, effective TI, damage-equivalent loads), not LES turbulence resolved fields. This is a less ambitious slot than "GNN surrogate for LES" but it is a real, working, reproducible deep-learning-for-wind-farms paper with public code.

## 3. Code repository

**URL:** https://github.com/gduthe/windfarm-gnn
**License:** MIT
**Language:** Python (Jupyter Notebook listed as primary language)
**Last commit:** 2025-07-07 (active)
**Stars:** 27
**Owner:** G. Duthé (lead author)

**Top-level layout:**
- `gnn_framework/` — training (`train.py`), evaluation (`predict.py`), config templates, fine-tuning (LoRA)
- `graph_farms/` — `generate_graphs.py` (PyWake-based data generator), config templates
- `notebooks/` — examples
- `plotting/` — plotting utilities
- `requirements.txt`

**Pretrained model:** 4-layer GEN GNN, downloadable via polybox: https://polybox.ethz.ch/index.php/s/4ItZPWY2gAus8ld

## 4. Data

**No public dataset to download.** Data is generated locally via `graph_farms/generate_graphs.py`, which:
1. Uses **Sobol sampling** for inflow conditions (wind speed, direction, TI)
2. Generates **random wind-farm layouts**
3. Calls **PyWake** (DTUWindEnergy/PyWake — DTU's open-source engineering wake model) to compute power, rotor-averaged wind speed, effective TI, and damage-equivalent loads (DELs)
4. Parallelizes across threads
5. Saves graphs (probably `torch_geometric.data.Data` objects)

Example invocation from the README:
```
python3 generate_graphs.py -c custom_config.yml -nl 200 -ni 15 -d /data/path -t 6
# 200 layouts × 15 inflows = 3,000 graphs, 6 threads
```

For paper-scale: per the DCE 2024 paper, the training set is typically O(10⁴–10⁵) graphs. Time per graph on a single thread is seconds-to-minutes depending on layout size.

**Data is therefore CPU-bound, not GPU-bound, and self-contained — zero external downloads needed.** This is the best possible outcome for a slot under risk of data blockers.

## 5. Headline metrics (to compare against)

From the Duthé 2023 abstract and the DCE 2024 companion (recalled from literature review and the repo README):

| Output | Typical reported metric | Approx. target |
|--------|-------------------------|----------------|
| Per-turbine power | R² or MAPE vs. PyWake | R² > 0.95 |
| Rotor-averaged wind speed | R² | > 0.97 |
| Effective TI | R² | > 0.90 |
| Damage-equivalent loads (DELs) | R² per channel | 0.85–0.95 |

The 2023 paper emphasizes per-turbine power and rotor-avg wind speed as primary outputs; loads (DELs) get more attention in the DCE 2024 follow-up. **For the replication, we will report whatever the trained model achieves on a held-out PyWake test set across power + rotor-avg wind speed + effective TI.**

Speed: the README claims **"~10× faster than PyWake"** — this is verifiable from inference timing.

## 6. Dependencies (from requirements.txt — to be downloaded next)

To be inspected immediately; key expected packages:
- `torch`, `torch-geometric` (PyG)
- `py-wake` (DTU PyWake)
- `numpy`, `scipy`, `pyyaml`, `tqdm`
- `matplotlib`, `seaborn`

## 7. Execution plan (high level)

1. ✅ Paper + repo identified, PAPER_NOTES.md written (this file). [Phase 1 — DONE within budget]
2. Pull `requirements.txt`, sanity-check, snapshot in this dir.
3. ssh uicgpu → `source ~/env.sh` → workspace `/data/stevens/sowfa_windfarm/`
4. Clone repo, create venv, install (PyTorch + PyG + py-wake).
5. Run `generate_graphs.py` with a modest dataset (e.g. 500 layouts × 10 inflows = 5,000 graphs) — CPU-bound, can run on a single A100 node's CPU.
6. Train default GEN-GNN config on 1× A100 (PyG is GPU-friendly; expect a few hours for 5k-graph dataset, more for larger).
7. Evaluate via `predict.py` on held-out test set; capture R²/MAPE per channel + inference timing vs. PyWake.
8. Produce REPORT.md + LaTeX PDF + STATUS_AUDIT update.

## 8. Friction risks identified

- **PyG install** can be finicky (CUDA version pinning for torch-scatter/torch-sparse). Plan: install from official PyG wheel index matching uicgpu's CUDA.
- **py-wake** install: should be straightforward via pip.
- **No external data download needed** → zero data-blocker risk. ✅
- **Sobol sampling determinism**: depends on whether the config sets a seed; will check.

---

*This file written at start of Phase 1 to commit early and avoid the "stuck-in-discovery" failure mode of the first attempt.*
