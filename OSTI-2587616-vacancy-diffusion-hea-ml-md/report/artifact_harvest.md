# Artifact harvest — OSTI 2587616

## Paper
- **PDF** — OSTI 2587616 / DOI 10.1063/5.0280842 / eScholarship uc/item/8dm7q0mf. Journal of Applied Physics 138, 074306 (2025), CC BY 4.0. Local copy: `work/paper.pdf` (2.9 MB, MD5 stable across sessions), extracted text `work/paper.txt` (98 KB).

## Data + code repository
- **`github.com/CLEANit/EvoSys-Research-Data-Code`** — MIT-licensed, 19 MB, 26 pickle files + README + LICENSE.
- Commit: `767874e3389b8e66e32af10bfc2e5033572f3eeb` ("Update README.md", 2025-08-24 19:03 EDT).
- Corresponding author: Isaac Tamblyn (isaac.tamblyn@uottawa.ca).
- Local clone: `uicgpu:~/replicate-osti-2587616/EvoSys-Research-Data-Code/`.

## Pickle inventory (26 files, cross-referenced in `report/evidence/replication_analysis.json`)

Per dataset (MD-train, MD-Base, Evo_1 = EvoSys 1-NNI, Evo_2 = EvoSys 2-NNI):
- `*_traj_all_atoms.pkl` (list, len 2, dicts of per-trajectory transition-atom sequences)
- `q_counts_*.pkl` — (N_unique,) int64
- `q_states_*.pkl` — (N_unique, 5) int64 (5-element 12-atom-ROI composition histograms)
- `q_next_atoms_*.pkl` — (N_events,) int64 (atom-type index 1..5 that filled the vacancy)
- `q_inverse_*.pkl` — (N_events,) int64 (index into `q_states_*` for the state before each transition)
- `q_first_*.pkl` — (N_unique,) int64 (first-occurrence indices)

Global:
- `q_states_all.pkl` — (1820, 5) int64 (unique compositions across all datasets)
- `q_inverse_all.pkl` — (1820,) int64
- `mapping_with_atoms_2024_05_01.pkl` — (265988, 3) int64 (pre-2024 mapping table)

## What is NOT in the release (documented in the report)
- Per-frame vacancy centroid trajectories (would enable ASD + diffusion coefficient).
- Per-event wall-clock timestamps (would enable jump rate + residence time).
- The 5,000 NEB output files (would enable Table III / Fig. 10 barrier distribution).
- Trained GCN weights (would enable exact regeneration of EvoSys trajectories).

None of these are the artifact's fault — they're a scope decision by the authors. The paper's methodology is thoroughly documented, so re-running from scratch on uicgpu (LAMMPS + PyTorch-Geometric) is feasible but out of scope for this replication pass.

## Reference software
- **LAMMPS** (paper cites Ref. 47) — Farkas EAM potential (paper Ref. 49). Not invoked in this replication.
- **OVITO** (paper Ref. 48) — used by the authors for post-processing; not needed to consume the released pickles.
- **PyTorch / PyTorch-Geometric** — implied by the paper's GraphConv layer; not needed here.

## Software used in THIS replication
- Python 3.10.12 (uicgpu system Python).
- NumPy 1.26.4, SciPy 1.13.0 (for χ², KL, entropy), Matplotlib 3.8.4 (for Fig. Table-II comparison).
- No paid APIs, no LLM inference, no compiled dependencies.

## LLM endpoints (per wave brief: free only)
- **Not invoked.** This replication is pure numerical recomputation on public data; no LLM judgment was needed to reach the numeric verdict. Had adjudication been required, Argo localhost:44497 (key=stevens) would have been the endpoint of choice.
