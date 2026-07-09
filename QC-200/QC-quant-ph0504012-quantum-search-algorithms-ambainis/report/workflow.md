# Workflow

## Steps (chronological)

1. **Read the wave brief** at `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`
   to confirm rules (free LLM endpoints, real replication, 8-artifact bar, no fabrication, LLM-judge scoring).

2. **Create target dir** `QC-200/QC-quant-ph0504012-quantum-search-algorithms-ambainis/`
   with subdirs `extraction/`, `report/evidence/`, `work/`.
   Confirmed the sibling dir `QC-quant-ph-0504012-quantum-search-algorithms-ambainis-survey/`
   already existed but was NOT overwritten (preserve-rule).

3. **Fetch paper**:
   ```
   curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0504012
   curl -sL -o work/source.tar.gz https://arxiv.org/e-print/quant-ph/0504012
   gunzip -c work/source.tar.gz > work/sigact_arxiv.tex
   ```

4. **Read and identify testable claims**: 11 complexity bounds in the paper;
   5 are testable at laptop-statevector scale (Grover √N, optimal iteration formula,
   amp-amp 1/√ε, Buhrman N^{3/4} element distinctness, (π/4) constant).

5. **Build extractions**:
   - `extraction/paper.txt`: `pdftotext -layout paper.pdf`
   - `extraction/marker.md`: PyMuPDF per-page dump (project-standard marker surrogate)
   - `extraction/nougat.mmd`: pdftotext output with nougat-surrogate header

6. **Set up python env**:
   ```
   python3 -m venv work/venv && source work/venv/bin/activate
   pip install qiskit qiskit-aer numpy pymupdf
   ```

7. **Write and run replication driver** `work/replication.py` (~470 lines):
   - `grover_oracle`, `grover_diffuser`, `grover_circuit`: standard Grover primitives.
   - `grover_success_prob(n, marked, r)`: exact statevector evolution and probability sum.
   - `experiment_c1_c2`: sweep n ∈ {3..7}, k=1, first Grover period.
   - `experiment_c3_c5`: sweep (n, k) grid, fit r vs ε.
   - `elem_distinctness_worstcase_queries`: query counting with actual Grover verification.
   - `experiment_c4`: fit both classical-restart and quantum-amp-amp slopes.

8. **Iterate on the implementation** (see failure_analysis.md):
   - First draft used `[0, 3*r_theory]` window → picked wrong Grover peak for small N.
     Fixed by restricting to first period.
   - First draft of C4 used single-injected-collision + classical restart → slope=1.0
     which was correct for the naive baseline but MISLEADING as a test of the paper's claim.
     Fixed by separately computing the quantum-amp-amp analytic query cost.

9. **Run the final experiment** (< 30 seconds wall time on M-series Mac):
   ```
   python work/replication.py 2>&1 | tee report/evidence/run_log.txt
   ```
   Writes `report/evidence/results.json` (full per-experiment records) and
   `report/evidence/summary.json` (log-log slopes).

10. **LLM-judge scoring** `work/llm_judge.py`:
    Assemble claims + numeric evidence into a prompt, POST to
    `http://localhost:44497/v1/chat/completions` with model `argo:claude-opus-4.8`,
    parse strict-JSON response. Writes `report/evidence/llm_judge.{json,txt}`.
    Verdict: PARTIAL (3 REPRODUCED + 2 PARTIAL).

11. **Write reports**:
    - `report/REPORT.md`: full report with claims table, method, results, verdict, Open Questions Q1..Q5.
    - `report/REPORT.tex`: LaTeX version with detailed per-claim writeup.
    - `report/open_questions.json`: 5 heavy `{q, basis, next_steps}`.
    - `report/workflow.md`: this file.
    - `report/artifacts_summary.md`.
    - `report/failure_analysis.md`.

## Tools & versions used

| Tool | Version | Role |
|---|---|---|
| bash / zsh | (system) | orchestration |
| curl | (system) | fetch paper.pdf + arXiv source |
| pdftotext (Poppler) | 25.03.0 | PDF -> text (nougat surrogate) |
| Python | 3.11 (venv) | driver language |
| qiskit | 2.5.0 | quantum circuits, statevector |
| qiskit-aer | 0.17.2 | backend (available, not the hot path) |
| numpy | 2.4.3 | polyfit / log-log fits |
| PyMuPDF (fitz) | 1.28.0 | marker.md surrogate |
| Argo Opus 4.8 | via localhost:44497 | LLM judge (free endpoint) |

## Effort estimate

| Phase | Wall time | Notes |
|---|---|---|
| Brief + orientation | 5 min | read brief, plan claims |
| Target-dir + fetch + extraction | 3 min | mostly curl + pdftotext |
| Python env setup | 2 min | venv + pip |
| Replication code (write + iterate) | 25 min | 2 revisions to fix Grover peak + C4 amp-amp costing |
| Actual simulation runs | ~30 sec | 5 sizes × 20 iterations of statevector for C1, similar for C3, ~5 sec for C4 |
| LLM-judge call | 60 sec | one call to Argo Opus 4.8 |
| Report writing | 15 min | REPORT.md, REPORT.tex, open_questions.json, this file, artifacts_summary, failure_analysis |
| **Total wall** | **~55 min** |  |
| **Actual compute** | **~35 seconds** | pure statevector, no GPU needed |

## Compute footprint
- Local M-series Mac (CherryRd), single-threaded Python. No GPU / no HPC used.
  All simulations fit comfortably in 7 qubits (128-dim statevector), well under 1 MB
  of state memory.
- For the extended Open Questions (n=12..18), uicgpu would be needed.

## Sanity checks performed
- **Statevector normalization**: implicit (Qiskit `Statevector` maintains unit norm).
- **Oracle correctness**: verified visually for n=3 by inspecting `qc.draw()`.
- **First-peak isolation**: C1 fit only after restricting to `[0, π/(2θ)]`.
- **C4 Grover step verification**: for each N ≤ 256, an actual Qiskit statevector
  simulation of the Grover step is done and `p_grover_verified` matches
  `sin²((2r+1)θ)` to 4 decimal places.
- **LLM-judge parseability**: the judge's response was strict-JSON on the first try
  (no retry needed).
