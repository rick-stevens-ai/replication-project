# Artifacts Summary — Hayashi et al. 2005 vortex-in-NCS replication

| Artifact | Path | Description |
|---|---|---|
| Paper | `paper.pdf` | Source (arXiv:cond-mat/0510548) |
| Extraction | `extraction/marker.md` | pdftotext dump with exact equations |
| Method extract | `report/method_extract.md` | Distilled method note (given) |
| Solver | `code/hayashi2005_replication.py` | Riccati–Eilenberger two-sheet vortex solver; LDOS, current, magnetization |
| Results | `work/results.json` | Machine-readable claims + measured numbers |
| Arrays | `work/arrays.npz` | Egrid, LDOS(E,r) tot/I/II, N(0,r), N_core/far(E), Psi/Delta(r), jphi, Mr, MI/MII, control |
| Run log | `work/run.log` | Timestamped incremental log |
| Fig 1 | `figs/fig1_delta_r.png` | Pair potentials Psi(r), Delta(r) — same core radius |
| Fig 2 | `figs/fig2_ldos.png` | LDOS map + zero-bias core peak + core-vs-far two-gap DOS |
| Fig 3 | `figs/fig3_magnetization_current.png` | Radial core magnetization |M|~(g_I-g_II) + control + supercurrent + per-sheet |
| Report (src) | `report/REPORT.tex` | LaTeX source |
| Report (pdf) | `report/REPORT.pdf` | Compiled 5-page report |
| Open questions | `report/open_questions.json` | 5 questions with basis + next steps |
| Workflow | `report/workflow.md` | Step-by-step procedure |
| Failure analysis | `report/failure_analysis.md` | Limitations, pitfalls, what would break |
| Meta | `META.json` | Status + verdict |

## Headline numbers (measured)
- Pair potentials: Psi and Delta both recover (0.9 bulk) at **1.50 xi0** — same core radius.
- LDOS zero-bias core peak: **N(E=0,r) maximal at r=0** (7.92 vs 4.96 far), core LDOS peaks at **E=0**.
- Two-gap bulk: far N(E=0) sheet I (fully gapped) **0.60** vs sheet II (line-node) **4.36**.
- Supercurrent |j|~(g_I+g_II): **~0 at core**, peaks at **1.12 xi0**.
- Magnetization |M|~(g_I-g_II): peaks at **1.38 xi0**, far **~1e-17** (→0); **control (equal sheets) = 0**.

## Verdict
**PARTIAL (strong).** All four targeted observables reproduced with the paper's
exact g_I±g_II decomposition (current = sum, magnetization = difference); the
distinctive radial core magnetization peaks near the core and vanishes for equal
sheets, isolating broken inversion symmetry. Reduced fixed-profile (non-self-
consistent) order parameter → PARTIAL rather than full REPLICATED.
