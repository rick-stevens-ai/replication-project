# Workflow — arXiv:0708.1879 replication

## Overall shape
Subagent-driven, single-machine, ~30-minute end-to-end replication of the
algorithmic core of Giovannetti/Lloyd/Maccone bucket-brigade qRAM. No paid
APIs; free-only endpoint (Argo `localhost:44497`) for the LLM judge.

## Step-by-step

1. **Read the wave brief** (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`) — locked hard rules (free endpoints only, real simulation, LLM-judge scoring, 8-artifact bar, 5 open questions, WAVE_RESULT line).
2. **Set up target dir** at `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0708.1879-quantum-random-access-memory-vittorio/{work,extraction,report/evidence}`.
3. **Fetch paper**: `curl -sL https://arxiv.org/pdf/0708.1879 -o work/paper.pdf` and `pdftotext` for skim.
4. **Identify the headline claims** in ~2 min of skim: bucket-brigade tree with wait/left/right trits, Eq.(1) superposition→correlated data, O(log N) active switches vs O(N) fanout, O(N) memory footprint.
5. **Reuse an existing sibling venv** (`QC-1703.05169-bayesian-qpe-silicon/work/venv`, already had Qiskit 2.5.0). Added `qiskit-aer 0.17.2` and `pymupdf 1.28.0` via pip.
6. **First simulator attempt** iterated the *full* 2^(n+2*(2^n-1)+1)-dim statevector for n=2,3,4. At n=4 that is 2^35 amplitudes and hung — killed the run.
7. **Rewrite**: keep `FullBucketBrigadeQRAM` for n=2 (proves the register model matches) and add `ReducedBucketBrigadeQRAM(n∈{2,3,4})` using the fact that BB routing is a classical permutation on the WAIT-initialised protocol subspace. Both simulators verify per-address correctness and Eq.(1) superposition-query fidelity; the reduced version reaches N=16 without the RAM blow-up.
8. **Run**: all fidelities = 1.0, switch counts exact: 2/3/4 vs 3/7/15 for BB vs conventional for N in {4,8,16}. Wrote `scaling.json` + `bucket_brigade_run.log` + `bb_qram_n2.qasm`.
9. **Extractions** (no Marker/Nougat on host, no central corpus hit): surrogate `marker.md` (PyMuPDF per-page) + surrogate `nougat.mmd` (`pdftotext -layout`), plus `extraction/README.md` explicitly declaring the surrogate status. This follows the established convention of sibling QC-200 directories.
10. **LLM judge**: `report/evidence/llm_judge.py` -> Argo (initially `argo:claude-opus-4.8` returned 502; switched to `argo:gpt-5.4` which returned a clean JSON verdict `{h1:YES, h2:YES, h3:YES, verdict:PARTIAL}` with reasonable caveats).
11. **Write reports**: `REPORT.md` (primary), `REPORT.tex` (compiled to `REPORT.pdf` via `pdflatex`), `open_questions.json` (5 heavy-duty items), `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.

## Tools & versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.6 | driver / simulator |
| Qiskit | 2.5.0 | QuantumCircuit + Statevector |
| qiskit-aer | 0.17.2 | (available, statevector used directly here) |
| NumPy | 2.5.0 | array math |
| PyMuPDF (fitz) | 1.28.0 | Marker-surrogate extraction |
| poppler pdftotext | (macOS) | Nougat-surrogate extraction + skim text |
| pdflatex | TeX Live 2026 | REPORT.pdf compilation |
| Argo LLM proxy | :44497 | free `argo:gpt-5.4` for judging |

## Work estimate
- Read/skim brief + paper: ~3 min
- Setup + first sim attempt: ~5 min
- Rewrite with reduced subspace + rerun: ~4 min
- Extraction surrogates: ~2 min
- LLM judge (with one 502 retry): ~2 min
- Report drafting (REPORT.md + REPORT.tex + open_questions + workflow/artifacts/failure): ~10 min
- **Total wall clock: ~25 min.**

## Files touched (all inside target dir)
```
paper.pdf
work/paper.pdf, work/paper.txt, work/venv (symlink)
extraction/README.md, extraction/marker.md, extraction/nougat.mmd
report/REPORT.md, report/REPORT.tex, report/REPORT.pdf, report/open_questions.json
report/workflow.md, report/artifacts_summary.md, report/failure_analysis.md
report/evidence/bucket_brigade_qram.py
report/evidence/scaling.json
report/evidence/bucket_brigade_run.log
report/evidence/bb_qram_n2.qasm
report/evidence/llm_judge.py
report/evidence/llm_judge_result.json
report/evidence/llm_judge_stdout.log
```
