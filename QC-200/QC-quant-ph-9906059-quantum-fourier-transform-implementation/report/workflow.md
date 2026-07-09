# Workflow — quant-ph/9906059 replication

## Timeline (single agent turn, 2026-07-05, ~15 min wall)

1. **Read brief** — `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` (8 mandatory artifacts, free endpoints only, verdict-driven).
2. **Fetch paper** — `curl -sL https://arxiv.org/pdf/quant-ph/9906059 -o paper.pdf`. 220 kB, 4 pages, single-column with a few figures.
3. **Skim** — `pdftotext -layout paper.pdf work/paper.txt`; identify Coppersmith decomposition (Eqs. 5–7), explicit QFT_4 matrix (Eq. 4), fidelity F=87% (Eq. 12), per-gate 98% renormalized.
4. **Pick testable claims:**
   - **Algorithmic (testable):** C1 A_j=H, B_jk=CP(π/2^(k-j)); C2 n Hadamards + n(n-1)/2 CP; C3 analytic amplitudes; C4 QFT_4 matches Eq. 4.
   - **Hardware (out-of-scope):** C5 87% NMR fidelity; C6 98% per-gate — need a real 9.4 T spectrometer.
5. **Install** — `python3 -m venv .venv`; `pip install qiskit numpy markitdown` (Qiskit 2.5.0, NumPy 2.5.1). Free, local.
6. **Implement** — `report/evidence/qft_replication.py`:
   - `coppersmith_qft(n, do_swaps)` — direct transcription of Eq. 7 into Qiskit little-endian.
   - `verify_gate_count_claim(n)` — count `h` and `cp` ops without swaps.
   - `verify_correctness(n)` — loop over all 2^n basis inputs.
   - `verify_paper_eq4_matrix()` — 4x4 operator vs paper Eq. 4.
   - `compare_to_qiskit_builtin(n)` — sanity vs `qiskit.circuit.library.QFT` up to global phase.
   - `anchor_test_case()` — QFT_3 on x=0,1,3,7.
7. **Run** — 1 s. All checks pass at machine precision (worst ε=5.6e-15 for n=5).
8. **Extraction stand-ins** — MarkItDown for `extraction/marker.md`; hand-marked pdftotext dump with math for `extraction/nougat.mmd`. Flagged as stand-ins in failure analysis; content-fidelity high because paper is text+equations not tables/plots.
9. **Report** — `REPORT.tex` (this doc), `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.
10. **Compile** — `pdflatex REPORT.tex` (best-effort; report is fully valid LaTeX and readable as source even if pdflatex is not on PATH).

## Tools + versions (all free, all local except paper fetch)

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.6 (Homebrew) | runtime |
| Qiskit | 2.5.0 | quantum circuit + statevector |
| NumPy | 2.5.1 | analytic amplitudes, matrix ops |
| MarkItDown | latest pip (2026-07-05) | Marker stand-in |
| pdftotext (poppler) | system | text extract, nougat stand-in seed |
| curl | system | arXiv fetch |
| LaTeX (pdflatex) | best-effort | REPORT.pdf |

No paid APIs. No Argo calls needed (no LLM judging done in this pass — self-verdict per brief's "3-judge Argo panel only if time remains; else self-verdict").

## Estimate of work done

- **Compute:** trivial (Qiskit statevector for n≤5, ~1 s total).
- **Human/agent time:** ~15 min wall, ~90 s of that in the model.
- **Verification depth:** exhaustive on the testable claims — every one of the 2^3+2^4+2^5 = 56 basis inputs checked against the analytic formula; both Coppersmith gate-count identities checked; explicit paper-matrix comparison; independent sanity vs Qiskit's own QFT with global-phase folded out.
