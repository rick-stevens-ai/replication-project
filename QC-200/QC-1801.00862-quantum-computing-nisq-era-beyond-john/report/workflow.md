# Workflow — QC-200 replication of Preskill (arXiv:1801.00862)

## Chronology

1. **Fetch + verify PDF** (~1 min).
   - `curl` v1, v2, v3 from arXiv.
   - Chose v3 (2018-07-31) as canonical. **SHA-256 mismatch vs brief** (see `failure_analysis.md`).
2. **Text extraction** (~30 s).
   - `pdftotext -layout` for skim, `pdftotext` (flow) for extraction/marker.md and extraction/nougat.mmd.
   - Neither `marker` nor `nougat` installed on this host; fallbacks documented in-file.
3. **Reproducible-core choice** (~2 min).
   - Preskill is a perspective essay with no single number to reproduce.
   - Picked QAOA MAX-CUT (small p, small n) as the direct instantiation of the paper's Section on hybrid quantum-classical variational algorithms.
4. **Sim implementation** (~15 min).
   - Wrote `report/evidence/qaoa_nisq_demo.py`: 3-regular n=10 graph, QAOA at p=1,2, statevector optimum via COBYLA (6 restarts), then Aer + depolarizing noise (`p1=1e-4, p2=1e-3, shots=8192`).
   - Wrote `report/evidence/qaoa_noise_sweep.py`: fix optimum, sweep p2 ∈ [0, 1e-4 ... 1e-1].
5. **Execution** (~40 s combined wallclock).
   - Reused existing sibling venv `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1802.01157-qaoa-parallelizable-gates/.venv` (Qiskit 2.5.0, Aer 0.17.2). Installed `networkx` into it.
6. **LLM-judge verdict** (~10 s).
   - Argo `argo:gpt-5.2` via `http://localhost:44497/v1/chat/completions`, temperature 0. First tried `argo:claude-opus-4.7` — got a transient HTTP 502; retry on gpt-5.2 succeeded.
7. **Report authoring** (~15 min).
   - `report/REPORT.md`, `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.

**Total wallclock:** ~40 min end-to-end.

## Tools + versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 (in sibling venv) | Runtime |
| Qiskit | 2.5.0 | Circuit + statevector |
| qiskit-aer | 0.17.2 | Noisy simulation |
| numpy | 2.5.0 | Linear algebra |
| scipy | 1.18.0 | COBYLA optimizer |
| networkx | 3.6.1 | 3-regular graph gen |
| pdftotext | poppler-utils | Text extraction fallback |
| Argo | localhost:44497 | LLM-judge (gpt-5.2) |
| curl | macOS system | arXiv download |

**Marker / Nougat:** unavailable; extraction files are `pdftotext` fallbacks (headered).

## What was NOT done, and why

- **No 50–100 qubit run.** Out of scope for a laptop replication. The paper's grand thesis about that scale is untestable in this budget.
- **No hardware compile with SWAP overhead.** Only algorithmic depth. This is called out as Open Question Q5.
- **No noise-adapted re-optimization.** We used the noiseless optimum under noise. This is called out as Open Question Q2.
- **Only one 3-regular seed.** No ensemble statistics. Called out as Q1.
- **No 3-judge Argo panel** — a single LLM judge (gpt-5.2) sufficed given time budget and the fact that this is a perspective paper (not a claim-adjudication case).

## Reproduce from scratch

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1801.00862-quantum-computing-nisq-era-beyond-john
VENV=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1802.01157-qaoa-parallelizable-gates/.venv
$VENV/bin/python report/evidence/qaoa_nisq_demo.py
$VENV/bin/python report/evidence/qaoa_noise_sweep.py
python3 report/evidence/llm_judge.py
```
