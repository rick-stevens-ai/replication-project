# Artifact Harvest

| Artifact | Source | Size | Notes |
|---|---|---|---|
| `osher_sethian_1988.pdf` | https://math.berkeley.edu/~sethian/2006/Papers/sethian.osher.88.pdf | 82 425 B, 38 pages | sha256 `508150b54de162a0cc1bb345c132e2209b706442317fced30055238f8c2c897a` — hosted by second author's home page at UC Berkeley |
| `osher_sethian_1988.txt` | `pdftotext -layout` output | 80 227 B, 1 975 lines | used for close reading & equation extraction |
| `levelset.py` | this replication | 17 kB | pure Python/NumPy implementation |
| `convergence.py` | this replication | ~0.9 kB | convergence-order helper |
| `llm_judge.py` | this replication | ~2.8 kB | LLM-judge call (Argo, free) |
| `results.json` | `python levelset.py` output | ~2 kB | per-experiment metrics |
| `C1_expanding_circle.{csv,png}` | C1 run | 6 kB / 26 kB | radius vs time |
| `C2_shrink_N{101,201,301}.csv` | C2 runs | 65/259/582 kB | full radius traces |
| `C2_shrinking_circle.png` | C2 (fine) plot | 32 kB | numerical vs exact overlay |
| `C2b_star_smoothing.csv` | C2b run | 396 kB | perimeter/area trace |
| `C2b_star_{snapshots,perimeter}.png` | C2b plots | 47 kB / 19 kB | qualitative + quantitative smoothing |
| `C3_merge.{csv,snapshots.png}` | C3 run | 3 kB / 51 kB | component count & merge snapshots |
| `llm_judge.txt` | Argo `argo:gpt-4o` @ localhost:44497 | ~1.5 kB | free-endpoint judgment |

All computation was done on the local CPU (uicgpu not required; problem
sizes ≤ 300×300 with ≤ 12 500 time steps finish in seconds each).
Python environment: `work/venv` with NumPy 2.5.1, SciPy 1.18.0,
Matplotlib 3.11.0, scikit-image 0.26.0.
