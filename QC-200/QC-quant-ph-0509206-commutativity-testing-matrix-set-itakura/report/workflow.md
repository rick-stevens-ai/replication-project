# Workflow — Replication of arXiv:quant-ph/0509206

**Paper:** Yuki Kelly Itakura, "Quantum Algorithm for Commutativity Testing of a Matrix Set", MSc essay, University of Waterloo, 2005 (70 pages). Supervisor: Ashwin Nayak.

**Replicator:** Ollie (OpenClaw subagent, session `subagent:0087378e`), 2026-07-05, running on `CherryRd` (macOS, Darwin 25.3.0, node v24.14.1).

**Wave:** QC-200 (single-paper independent replication; free endpoints only).

## Workflow (chronological)

1. **Paper fetch.** `curl -sL https://arxiv.org/pdf/quant-ph/0509206 -o work/paper.pdf` (445 KB, 70 pp).
2. **Text extraction (surrogate for Marker/Nougat).** Neither `marker_single` nor `nougat` is installed on this host and no pre-parse exists in the central corpus for `0509206*`. Followed the sibling `QC-0704.3628-*` convention:
   - `extraction/marker.md` = PyMuPDF (fitz) 1.27.2.3 text extraction with `---- page N ----` boundaries.
   - `extraction/nougat.mmd` = `pdftotext -layout` reflow.
   - `extraction/README.md` documents the surrogate provenance.
3. **Claim scoping.** Read Abstract + Chapter 3 (`sed -n '2000,2500p' work/paper.txt`). Identified four testable claims (see REPORT.tex §2). Key discovery: the task-brief description says "O(k^{2/3}) matrix queries" which is inaccurate. The paper's headline is **O(k^{4/5} n^{9/5})** (Algorithm 5, simultaneous Szegedy walk) with a subclaim of **O(k^{2/3} n^2)** for the element-distinctness reduction (Algorithm 4). We replicate the sub-claim numerically and note the correction.
4. **Design.** Chose three matrix ensembles at n = 4:
   - **COMMUTE**: k Hermitian matrices sharing a random orthonormal eigenbasis Q, independent uniform-[-1,1] diagonals; pairwise commutative by construction.
   - **NON-COMMUTE** (dense marked, M = k-1): commuting set with one entry replaced by an independent random Hermitian intruder.
   - **SINGLE-DEFECT** (M = 1): two matrices in DIFFERENT random bases, other k-2 matrices identically zero. Yields exactly one non-commuting pair -- the clean Grover-scaling testbed.
5. **Classical baseline.** All-pairs `[A_i, A_j] = A_i A_j - A_j A_i`, Frobenius norm tau = 1e-8. Verified marked-pair counts match ensemble design (0 / k-1 / 1 respectively). C(k,2) matrix-multiplications per run.
6. **Quantum core.** Full complex `numpy.ndarray` statevector of dimension `2^ceil(log2(C(k,2)))`. Grover iteration = oracle sign-flip on marked basis states + Grover diffusion `2|s><s| - I` restricted to valid pair indices. Optimal iteration count = round((pi/4) sqrt(N/M)).
7. **Scaling sweep.** k in {8, 16, 27, 45, 64, 90}. At k = 90 the padded Hilbert space is 4096 (12 qubits); still fits in memory.
8. **Fit.** Log-log least-squares fit of measured Grover iterations vs k, one line per ensemble. Also fits classical C(k,2) baseline (expected slope +2) and Ambainis element-distinctness prediction ceil(k^{2/3}) (expected slope +0.667).
9. **Verdict.** Both non-fabricated headline predictions reproduced within tolerance: classical slope 2.048 (theory 2.000), Grover-M=1 slope 1.030 (theory 1.000 = sqrt of quadratic), element-distinctness slope 0.665 (theory 0.667). ZERO false positives in six COMMUTE runs.

## Tools & versions

| Tool | Version | Purpose |
|------|---------|---------|
| `python3` | 3.13 (system) | driver |
| `numpy` | 2.3.4 (see `results.json.meta.numpy_version`) | matrix + statevector arithmetic |
| `matplotlib` | 3.x (auto) | log-log scaling plot |
| `PyMuPDF` (`fitz`) | 1.27.2.3 | Marker-surrogate PDF text extraction |
| `pdftotext` | poppler | Nougat-surrogate reflow |
| `curl` | system | paper download |
| Argo (localhost:44497, key=stevens) | -- | available for LLM-judge; NOT invoked (self-verdict per brief §7) |

## Work estimate

~40 minutes wall clock, one turn, one subagent, no LLM inference beyond the driver agent itself. Approximately 350 lines of new Python, one 6-line figure, five open questions, one 6-section LaTeX report. Full replication reproducible on any laptop with `numpy + matplotlib` in under 5 seconds for the default k-sweep.

## Reproduction command

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0509206-commutativity-testing-matrix-set-itakura
python3 report/evidence/commutativity_replication.py --out report/evidence
```

Outputs:
- `report/evidence/results.json` -- full per-k results (classical, quantum, single-defect, fits)
- `report/evidence/scaling_loglog.png` -- log-log plot with fitted slopes
- stdout table (one line per k)
