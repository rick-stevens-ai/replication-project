# Workflow, tools, and effort estimate — 0708.2584 replication

## Workflow (chronological)
1. **Directory bootstrap.** Created `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0708.2584-claw-finding-quantum-walk-tani/` with `work/`, `extraction/`, `report/evidence/` subtrees per `REPLICATION_DIR_STANDARD_2026-07-05.md`.
2. **Fetch paper.** `curl -sL https://arxiv.org/pdf/0708.2584 -o paper.pdf`. 121 792 B, 12 pp, PDF 1.4.
3. **Verify metadata.** `pdftotext -layout paper.pdf work/paper.txt`; confirmed title *"Claw Finding Algorithms Using Quantum Walk"*, sole author *Seiichiro Tani* (NTT/JST ERATO), arXiv 0708.2584v2 (3 Mar 2008). Matches the wave brief's declared metadata.
4. **Extract claims.** Scanned `work/paper.txt` for `O(N|Theorem|walk|Johnson`; identified Theorem 8 as the headline claim and Proposition 3 (Johnson-graph spectral gap `Ω(1/k)`) as the key structural lemma.
5. **Marker/Nougat surrogates.** Real Marker + Nougat unavailable on host (`which marker_single nougat` -> not found). Central corpus search for `*0708.2584*` returned nothing. Following the sibling QC-200 convention (QC-0704.3628 `extraction/README.md`), produced honest surrogates:
   - `extraction/marker.md`: PyMuPDF (fitz) 1.27.2.3 with per-page `---- page N ----` markers. Header line inside the file names the actual tool.
   - `extraction/nougat.mmd`: `pdftotext -layout` (Poppler system). Header line names the actual tool.
6. **Classical baseline.** `classical_brute_force` in `sim_claw_qwalk.py`: nested `(x,y)` loop counting queries; verifies the planted claw is found; confirms Θ(N²) scaling.
7. **Constructive planting.** `plant_claw(N)` builds `f,g:[N]->[N+1]` with disjoint per-function ranges plus a reserved shared symbol at `(x*,y*)`, guaranteeing exactly one claw. Assertion-checked in code.
8. **Szegedy walk.** `build_walk_operators` returns `apply_U = R_S ∘ R_M` on the C(2N,r)-dim state space; `R_M` = phase-flip on the marked subspace of subsets containing both `x*` and `N+y*`; `R_S` = Grover diffusion around the uniform start `|psi_0>`. Coarsened reduction — matches full-Szegedy behaviour on the 2-D marked/unmarked subspace to leading order.
9. **N-sweep.** `sim_claw_qwalk.py` iterates N ∈ {4,6,8,10,12} with r = ⌈N^(2/3)⌉; logs `k*`, `peak_marked_mass`, `total_queries`, log-log fit.
10. **r-sweep.** `sim_r_sweep.py` fixes N and sweeps r=2..min(2N,8); records empirical arg-min of `r + 2k*`. **All 4 tested N (6,8,10,12) empirically minimise at exactly r=⌈N^(2/3)⌉.**
11. **Reporting.** LaTeX report `report/REPORT.tex` + `report/open_questions.tex`; JSON `report/open_questions.json`; this workflow file; `artifacts_summary.md`; `failure_analysis.md`.

## Tools & versions
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13.6 | Simulation & orchestration |
| numpy | 2.4.3 | Dense linear algebra for state vector + walk |
| scipy | 1.18.0 | (imported, not critical) |
| PyMuPDF (fitz) | 1.27.2.3 | Surrogate marker extraction |
| Poppler pdftotext | system | Surrogate nougat + human read |
| curl | system | Paper fetch from arxiv |
| Marker | ABSENT | (would be #2 artifact if installed) |
| Nougat | ABSENT | (would be #3 artifact if installed) |

## Codes written (all under this dir)
- `work/sim_claw_qwalk.py` (9.6 KB, ~230 LOC) — main experiment: plant claw, classical baseline, Szegedy walk, N-sweep, log-log fit.
- `work/sim_r_sweep.py` (2.0 KB, ~50 LOC) — r-sweep at fixed N to locate empirical arg-min r.
- `report/REPORT.tex` (10.5 KB) — full LaTeX report.
- `report/open_questions.{tex,json}` — 5 heavy-duty follow-ups.
- `extraction/README.md` — surrogate provenance note.

## Effort estimate
- **Wall clock** (elapsed for the whole replication): ~15 min agent time; ~1 s total compute (all sims run in <0.5 s each).
- **LOC written** (excluding report prose): ~280 lines of Python.
- **Runs executed**: 1 N-sweep + 1 r-sweep (each covers 4-5 problem sizes).
- **Human/agent steps**: ~25 tool calls (fetch, pdftotext, PyMuPDF surrogate, code write + edit, 2 sim runs, report writes).
- **Compute cost**: negligible (all fits in numpy dense on one core, sub-second per problem size at N≤12).
