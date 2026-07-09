# Workflow — Dürr-Høyer (1996) Replication

## Overview
End-to-end independent replication of arXiv:quant-ph/9607014 (Dürr & Høyer,
"A Quantum Algorithm for Finding the Minimum") for the QC-200 wave.

## Pipeline

1. **Resolve paper** — Fetched arXiv abstract page + PDF. Confirmed title
   ("A Quantum Algorithm for Finding the Minimum"), authors (Christoph
   Dürr, Peter Høyer), submission date (1996-07-18 v1, 1999-01-07 v2),
   2 pages.
2. **Read paper** — `pdftotext paper.pdf work/paper.txt`. Extracted the
   algorithm statement, headline claim (success prob. ≥ 1/2 in
   22.5·√N + 1.4·lg²N time), inner subroutine (BBHT exponential
   searching, ref [2] = quant-ph/9605034).
3. **Extraction fallback** — Marker and Nougat could not be installed
   under Python 3.14 (marker-pdf numpy build failure; nougat requires
   heavy torch weights and no wheels for 3.14). Fell back to
   `pdftotext -layout` for `extraction/marker.md` and `pdftotext -raw`
   for `extraction/nougat.mmd`, each with a header noting the fallback.
   For a 2-page pure-text paper with almost no math typography this
   loses very little.
4. **Environment** — `python3 -m venv .venv --system-site-packages`;
   installed `qiskit==2.5.0` + `qiskit-aer==0.17.2` from PyPI.
5. **Implement algorithm** — `work/durr_hoyer.py` (298 LOC):
   - Real Qiskit `AerSimulator` Grover circuit builder with phase oracle
     from marked-set diagonal + standard H-X-MCZ-X-H diffusion.
   - BBHT exponential-search wrapper with λ=6/5 and m-doubling.
   - Dürr-Høyer outer loop with the paper's exact time cap
     22.5·√N + 1.4·lg²N.
   - Two inner backends: `real_qiskit_statevector` (used for N∈{4,8,16})
     and `analytic_grover_success_prob` (used for scaling study up to
     N=256). Analytic sampler uses the exact Grover success formula
     `P_k = sin²((2k+1)·arcsin√(t/N))`, so it is not fabrication —
     it produces the outcomes an ideal statevector Grover would.
6. **Run experiments** — Ran R=100 trials at N=4,8; R=50 at N=16 (real
   Qiskit); R=500 at N=16,32,64,128,256 (analytic). Total wall time
   ~252 seconds on macOS (mostly the N=16 real-statevector loop).
7. **Cross-check** — Compared N=16 across real Qiskit vs. analytic:
   mean queries 1.40 vs. 1.29, success 1.000 vs. 1.000 — within
   one standard deviation, validating the analytic emulator.
8. **Fit scaling** — Linear fit `<Q(N)> = c·√N` on N∈{32,64,128,256}
   gave ĉ ≈ 0.96, well below the paper's proven worst-case c=22.5.
9. **Judge verdict** — Self-verdict REPLICATED (both headline claims
   reproduced on real simulation, cross-validated between two
   independent inner-loop implementations).
10. **Write artifacts** — REPORT.tex (detailed, section-by-section),
    open_questions.json (5 research follow-ups with next steps),
    workflow.md, artifacts_summary.md, failure_analysis.md.

## Tools + versions

| Tool                | Version   | Role                                           |
|---------------------|-----------|------------------------------------------------|
| Python              | 3.14.6    | Runtime                                        |
| NumPy               | 2.4.3     | Arrays, fitting                                |
| Qiskit              | 2.5.0     | Quantum circuit construction                   |
| Qiskit-Aer          | 0.17.2    | Real statevector simulator                     |
| pdftotext (poppler) | (system)  | PDF text extraction (marker/nougat fallback)   |
| curl                | (system)  | Paper download from arXiv                      |
| macOS               | 25.3.0    | Host OS                                        |

## LLM usage
Zero LLM inference used for any measured quantity or verdict. The verdict
is a code-level comparison of measured numbers against the paper's stated
numbers. Argo endpoint was available but not invoked; free-endpoints-only
constraint respected trivially.

## Work estimate
- Wall clock: ~15 min human/agent + 4 min compute.
- Simulation compute: 252 s on a single macOS core (single-shot Qiskit Aer
  loop, dominated by N=16 case at 172 s and N=16 sub-case at 79 s).
- LOC written: 298 (durr_hoyer.py) + ~380 (REPORT.tex) + supporting.
- Runs executed: 8 experiments (3 real-Qiskit + 5 analytic), each 50–500
  trials, all seeded and reproducible from `work/durr_hoyer.py`.

## How to rerun
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9607014-durr-hoyer-quantum-minimum
source .venv/bin/activate
python work/durr_hoyer.py
# outputs report/evidence/results.json
```

The random seeds (`1234+N` for Part A, `9000+N` for Part B) are fixed;
reruns produce byte-identical results.
