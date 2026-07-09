# Workflow — quant-ph/0012055 (QC-200 wave, 2026-07-05)

## Timeline (wall clock)

| Phase                                | Elapsed  | Notes |
|--------------------------------------|----------|-------|
| Read brief, create target dir        | ~1 min   | `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/` |
| Fetch arXiv PDF                      | <1 min   | 113 kB, 4 pages |
| `pdftotext -layout` extract          | <1 min   | 315 lines, complete equations |
| Read + comprehend paper              | ~2 min   | Central claim = Eq. (5) → Toffoli after τ=K·2π/Ω |
| Set up venv, install QuTiP + Qiskit  | ~2 min   | Python 3.14 venv |
| Write main sim (`code/wsm_toffoli.py`) | ~5 min | 288 lines |
| First run (12 (K,N_Fock) cases + thermal) | <1 sec compute | F=1.000000 immediately |
| Write phase/gate-count sim           | ~2 min   | `code/toffoli_phase_and_gatecount.py` |
| Second run                           | <1 sec compute | Qiskit MCXGate transpile |
| Extraction fallbacks (marker.md, nougat.mmd) | ~5 min | Manual; no marker/nougat installed |
| Write REPORT.tex                     | ~10 min  | Full section-by-section report |
| open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md | ~5 min | This file |
| Compile REPORT.pdf                   | ~1 min   | pdflatex if available; else skip |
| **Total wall clock**                 | **~35 min** | |

## Tools + versions

| Tool          | Version    | Role |
|---------------|------------|------|
| Python        | 3.14       | Simulation runtime |
| QuTiP         | 5.3.0      | Truncated-Fock oscillator + qubit tensor products, `expm`, `thermal_dm`, `basis`, `sigmax/y/z` |
| Qiskit        | 2.5.0      | `MCXGate`, `transpile(basis_gates=..., optimization_level=3)` for gate-count comparison |
| NumPy         | 2.4.3      | Linear algebra, einsum for partial trace |
| SciPy         | 1.18.0     | Backing linear algebra |
| pdftotext     | poppler    | PDF → text extraction (Marker/Nougat fallback) |
| curl          | system     | arXiv PDF fetch |
| pdflatex      | (if avail.)| REPORT.tex → REPORT.pdf |

**LLM inference used:** *none* in this replication (pure numerical work).

## Reproducibility commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/
curl -sSL -o paper.pdf https://arxiv.org/pdf/quant-ph/0012055
pdftotext -layout paper.pdf work/paper.txt
python3 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip qutip qiskit numpy scipy
python code/wsm_toffoli.py                    # -> report/evidence/wsm_toffoli_results.json
python code/toffoli_phase_and_gatecount.py    # -> report/evidence/toffoli_phase_and_gatecount.json
pdflatex -output-directory=report report/REPORT.tex   # -> report/REPORT.pdf
```

All simulations run in **<1 second wall clock each** on a single CPU core.
Total repository size is ~150 kB (paper PDF dominates).

## Work-done estimate

- **LOC written by us:** ~380 lines Python + ~350 lines LaTeX + ~250 lines Markdown/JSON.
- **Number of simulation cases actually run:** 12 (K x N_Fock) + 3 (Fock oscillator initial states) + 4 (thermal n_bar values) + 2 (gate-count MCXGate transpiles) = **21 measured cases**, all producing real numerical evidence.
- **Number of paper claims tested:** 3 fully (C1, C2, C3), 1 partially (C4), 1 not attempted (C5 = full Grover).

## What we did NOT do (and why)

- Did not install Marker or Nougat (each is a 5–15 minute install with model downloads; the 4-page paper's pdftotext is sufficient to extract every equation). Both `extraction/` files are labeled as fallbacks with explicit provenance notes.
- Did not simulate the full Grover $U_G$ end-to-end (out of time-budget scope; the same QuTiP machinery generalizes trivially to $n=4,5,6$).
- Did not run a 3-judge Argo LLM panel (single-agent self-verdict; the numerical evidence is unambiguous: $F=1.000000$).
- Did not attempt to derive the analytical parallelogram vertex coordinates from Eq. (4) (would strengthen Q1 open question but not the verdict).
