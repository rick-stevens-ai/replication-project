# Workflow — Independent replication of Griffiths & Niu (1996), arXiv:quant-ph/9511007

## What we replicated

The central quantitative claim of Griffiths & Niu (1996): the quantum
Fourier transform (QFT) followed by measurement can be re-implemented as
a strictly semiclassical circuit (Hadamard + measurement + classically-
conditioned single-qubit phase gates, no coherent two-qubit gates) with
the same measurement statistics.

## End-to-end workflow

1. **Fetch paper.** `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/9511007` → 95 KB, 7-page PDF (`file paper.pdf` → PDF v1.4).
2. **Extract text.** `pdftotext paper.pdf work/paper.txt` and `pdftotext -layout paper.pdf work/paper_layout.txt`.
3. **Read equations & recipe.** Confirmed via the extracted text that the paper's Fig.-2 recipe is exactly:
   - for j = n-1 → 0: Hadamard qubit j; measure qubit j; for each less-significant qubit k<j, apply single-qubit phase P(2π/2^(j-k+1)) *if the measurement outcome was 1*.
   - See Eqs. (10)–(11) for the per-box unitary and the phase-update rule φ′ = φ/2 + c/4.
4. **Environment.** Reused an existing Qiskit 2.5.0 venv (from a sibling QC-200 project). Added `pip install qiskit-aer` (0.17.2).
5. **Implement standard QFT** (from primitives; not the library `QFTGate`): H + controlled-phase in the paper's convention (`report/evidence/replicate_semiclassical_qft.py::standard_qft_circuit`).
6. **Implement semiclassical QFT** with Qiskit's dynamic-circuit `with qc.if_test((cr[cbit], 1)): qc.p(...)` classical-conditional (`report/evidence/replicate_semiclassical_qft.py::semiclassical_qft_circuit`).
7. **Sanity sweep on |x⟩ inputs.** For n=3,4, run both circuits on every computational-basis input x ∈ {0..2^n-1}, 8192 shots each, compute TVD vs analytic uniform 1/2^n. Result: all TVDs < 0.032, agree within shot noise.
8. **Discriminating sweep on periodic superposition inputs.** For (n,p) ∈ {(3,2),(3,4),(4,2),(4,4),(4,8)}, prepare `|ψ⟩ = (1/√K) Σ|k·p mod 2^n⟩` via `qc.initialize`, then run both QFT variants. Analytic post-QFT distribution is a comb; both circuits reproduce the comb peaks exactly and full-vs-semi TVD ≤ 0.011 in every case (`report/evidence/replicate_periodic_input.py`).
9. **Gate counting.** Both empirical (per circuit) and theoretical (n, n(n-1)/2). Confirmed the paper's counts up to n=8.
10. **Write report.** REPORT.tex with claims table, method, results tables, verdict, open questions. Compiled to REPORT.pdf with `pdflatex`.

## Tools / codes / versions

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (venv reused from `QC-quant-ph-0012055-multi-bit-gates-quantum-computing/venv`) | driver |
| Qiskit | 2.5.0 | circuit construction + `if_test` dynamic circuits |
| qiskit-aer | 0.17.2 | high-performance CPU statevector simulator with dynamic-circuit support |
| NumPy | latest in venv | reference DFT + TVD |
| Poppler `pdftotext` | 25.09.0 | PDF → plain text (fallback extraction) |
| TeX Live | 20260301 (`pdflatex`) | REPORT.pdf compilation |
| curl | macOS default | arXiv fetch |

**No LLM inference** was needed for this replication (pure classical simulation + analytic comparison). Argo endpoints were available but not consulted.

## Estimate of work done

- Total wall-clock time: ~35 minutes (subagent).
- LOC written: `replicate_semiclassical_qft.py` = 246 lines; `replicate_periodic_input.py` = 173 lines; REPORT.tex = 220 lines; extraction/marker.md + extraction/nougat.mmd + open_questions.json + failure_analysis.md + workflow.md + artifacts_summary.md ≈ 500 lines total docs.
- Simulator runs: 24 basis-state runs (n=3: 8; n=4: 16) × 2 variants + 5 periodic runs × 2 variants = 58 Aer simulations, each ≤ 1 second on CPU. Total simulator wall time < 30 s.
- Verifications: gate-count sanity, TVD < 0.032 (basis inputs) and < 0.011 (periodic inputs) under 24+5 cases, exact peak-set match under all 5 periodic cases.
- Report: REPORT.tex compiles cleanly with `pdflatex` to REPORT.pdf (5 pages, 218 KB).

## Reproducibility

```bash
source ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0012055-multi-bit-gates-quantum-computing/venv/bin/activate
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9511007-semiclassical-fourier-transform-griffiths-niu
python report/evidence/replicate_semiclassical_qft.py    # → report/evidence/results.json, summary.txt
python report/evidence/replicate_periodic_input.py       # → report/evidence/results_periodic.json
cd report && pdflatex -interaction=nonstopmode REPORT.tex  # → report/REPORT.pdf
```
