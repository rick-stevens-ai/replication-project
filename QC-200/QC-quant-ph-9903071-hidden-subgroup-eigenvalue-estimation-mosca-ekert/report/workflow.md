# Workflow — Replication of Mosca & Ekert (1998), quant-ph/9903071

## Narrative

1. **Paper resolution.** Fetched PDF from `https://arxiv.org/pdf/quant-ph/9903071`
   (201 KB, 16 pp.). Confirmed authors from the PDF: Michele Mosca (Clarendon Lab
   & Mathematical Institute, Oxford) and Artur Ekert (Clarendon Lab, Oxford), 1998.
2. **Reading + claim extraction.** Ran `pdftotext -layout` and skimmed the abstract,
   §2 (Hidden Subgroup Problem), §3 (eigenvalue-estimation view), §4 (Z_N examples),
   §5 (one-control-qubit / flying-qubit variants). Identified the six claims (C1..C6)
   listed in REPORT.tex.
3. **Environment selection.** Reused the sibling QC-200 venv at
   `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301141-shor-discrete-log-elliptic-curves-proos-zalka/venv`
   (Qiskit 2.5.0, NumPy 2.5.1, Python 3.13). No new installs needed.
4. **Implementation.** Wrote a single self-contained `work/qpe_and_hsp.py` implementing:
   - `build_qpe_circuit_phase_gate(n, phi)` — QPE on 1-qubit `diag(1, e^{2πiφ})`.
   - `build_qpe_shift_circuit(N, n_count, target_state_index)` — QPE on the cyclic
     shift `T|k>=|k+1 mod N>` for N in {6,8}, embedded in the nearest power-of-2
     Hilbert space when N is not a power of 2.
   - `hsp_period_finding_distribution(N, d, n_count)` — Fourier-view period-finding
     with `f(x)=x mod d`, hidden subgroup `d Z_N`.
   - `experiment_3` — pointwise comparison of the two circuit families plus the
     analytic identity for coset-input QPE.
5. **Execution.** One statevector run through Qiskit; total wall-clock < 15 s.
6. **Scoring.** 9 discrete pass/fail checks derived directly from the paper's
   assertions; all 9 pass.
7. **Reporting.** Wrote `report/REPORT.tex` (compiled to `REPORT.pdf`, 5 pp.), the
   five open questions (`open_questions.json`), this workflow, the artifacts
   summary, and a failure analysis.
8. **Extraction artifacts.** Marker/Nougat not installed on this host; produced
   pdftotext-based `.md` and `.mmd` fallbacks per REPLICATION_DIR_STANDARD_2026-07-05.md
   with a header noting the fallback.

## Tools & versions

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (`/usr/local/bin/python3`) | Runtime |
| Qiskit | 2.5.0 | Circuit + statevector simulation |
| NumPy | 2.5.1 | Linear algebra for shift operators + Fourier verification |
| pdftotext | Poppler (system) | PDF → text for extraction fallback |
| pdflatex | TeX Live 2026-03-01 | Compile REPORT.tex → REPORT.pdf |
| curl | system | Fetch arXiv PDF |

## LLM inference

- **None used for the numerical result** (algorithmic ground truth is exact
  algebra; no judge needed for the pass/fail checks).
- Free Argo endpoint (`localhost:44497`, key=stevens) available if a downstream
  panel judge is wanted.

## Effort estimate

- Human/agent steps: ~20 targeted tool calls.
- Wall-clock: ~5 min total (fetch + parse + implement + run + report).
- Compute: single CPU, no GPU. Qiskit statevector runs finish in <1 s each.
- LOC written: ~370 lines of Python (`work/qpe_and_hsp.py`), ~200 lines of LaTeX
  (`report/REPORT.tex`), plus supporting markdown.
- Runs executed: 1 full script execution producing `results.json`.
- Circuits built: 12 QPE circuits (3 phis × 4 n_counts for Exp.1) + 2 shift-QPE
  circuits (Exp.2) + 2 period-finding evaluations (Exp.2b/3), all statevector.

## Repro command

```bash
VENV=~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301141-shor-discrete-log-elliptic-curves-proos-zalka/venv
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9903071-hidden-subgroup-eigenvalue-estimation-mosca-ekert
$VENV/bin/python work/qpe_and_hsp.py
```
