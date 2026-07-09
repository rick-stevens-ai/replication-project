# Workflow — QC-200 replication of arXiv:1509.02374 (Montanaro, Quantum walk speedup of backtracking algorithms)

## Timeline

| Step | Action | Elapsed |
|------|--------|---------|
| 1 | Read `QC_WAVE_BRIEF_2026-07-03.md`; scaffold target dir; fetch paper PDF from arXiv | ~1 min |
| 2 | `pdftotext` + skim key sections (Abstract, Thms 1–2, Algorithm 2, Belovs walk) to extract central testable claim | ~2 min |
| 3 | Write `replicate.py`: DPLL 3-SAT backtracking + Belovs walk operator + spectral analysis + explicit-simulation observable | ~5 min |
| 4 | Smoke run on 3 instances (T ∈ {46, 120, 522}); confirmed pipeline works, initial slope 0.36 | ~1 min |
| 5 | Write `replicate_v2.py`: broadened T-bin sweep, 5-min budget, 6 bins, fit slope + R² | ~2 min |
| 6 | Full sweep: 16 instances, T ∈ [21, 397], slope 0.374, R² 0.938 | ~3 min |
| 7 | Author `REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `extraction/{marker.md,nougat.mmd}` | ~5 min |

Total wall time: ≈ 20 min on CherryRd (macOS, single core).

## Tools + versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.13 (`/usr/local/bin/python3`) | Everything |
| NumPy | 2.4.3 | Statevector, reflection matrices, eig |
| SciPy | 1.18.0 | Available; not used in core walk |
| Poppler `pdftotext` | (system) | Paper extraction (Marker/Nougat unavailable — see failure_analysis.md) |
| curl | (system) | Fetch arXiv PDF |
| LaTeX | pdflatex (optional) | REPORT.tex → REPORT.pdf (not compiled in this run; source is authoritative) |
| Argo (via `curl`) | (not used) | No LLM inference was required for this pure-simulation replication |

## Code inventory

| File | Purpose |
|------|---------|
| `report/evidence/replicate.py` | Core: DPLL, tree builder, Belovs walk R_A / R_B, spectral analysis, explicit W^k simulation. Run once for 3-instance smoke. |
| `report/evidence/replicate_v2.py` | Scaling experiment: 16-instance sweep, log-log fit. Imports functions from `replicate.py`. |
| `report/evidence/results.json` | Output of `replicate.py` — smoke test with per-instance quantum walk metrics + explicit-simulation overlaps + fits. |
| `report/evidence/results_v2.json` | Output of `replicate_v2.py` — full scaling data: 16 (T, k_q, gap) triples + slope/intercept/R². |

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1509.02374-quantum-walk-backtracking-montanaro/report/evidence
python3 replicate.py         # ~2s, writes results.json
python3 replicate_v2.py      # 60-300s depending on how many bins fill, writes results_v2.json
```

Both scripts are deterministic given the fixed RNG seeds (`20260705`, `20260706`).

## What was NOT done

- No qubit-level gate synthesis (walk is simulated in the T-dim vertex Hilbert space, which is the natural Belovs setting; qubit encoding is orthogonal to the query-count claim).
- No implementation of the *finding* extension (recursion on subtrees per Section 2.2 of the paper); only the Algorithm-2 detection primitive.
- No test on unsatisfiable instances (would confirm the walk correctly outputs "no marked vertex" via non-detection).
- No test at T > 400 (bounded by O(T³) eig cost in a 5-minute sampler budget on 1 CPU).

## Work-effort estimate

- Wall time: ~20 min agent-time, ~5 min compute
- Human-attention-equivalent: this replication would take an experienced quantum-algorithms grad student ~2-3 focused hours to code + write up equivalently. The agent's advantage is the ability to spend most of that budget on writing rather than dispatching numpy.
