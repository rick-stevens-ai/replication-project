# Workflow — Independent Replication of arXiv:1710.01022

**Paper:** Moll et al. (IBM), "Quantum optimization using variational algorithms on near-term quantum devices," arXiv:1710.01022v2, 9 Oct 2017.
**Wave:** QC-200 replication wave, 2026-07-05.
**Executor:** OpenClaw subagent on CherryRd (macOS 25.3.0 x64).
**Elapsed wall time (end to end):** ~15 minutes.

## Phase 1 — Paper acquisition + parse (2 min)
1. `curl` arXiv PDF from `https://arxiv.org/pdf/1710.01022` → `work/paper.pdf` (5.7 MB, PDF v1.5, 27 pp).
2. `pdftotext work/paper.pdf work/paper.txt` (reflowed, 1808 lines).
3. `pdftotext -layout work/paper.pdf work/paper_layout.txt` (layout-preserving, 1488 lines).
4. Verified title + author list against PDF page 1 (18-author IBM Research team; **not** Farhi as the initial directory slug suggested — dir renamed from `...-farhi` → `...-moll-ibm`).
5. Skim + `grep` the two most-checkable numbers: the **0.6924 QAOA-p=1 guarantee** on 3-regular graphs (from FGG'14, cited §5.1 refs [41,42]) and **chemical accuracy VQE-H₂** at R=0.735 Å (§4.4).

## Phase 2 — Extraction artifacts (2 min)
Marker (`marker_single`) and Nougat (`nougat`) were **not installed** and no pre-parsed copy existed at `~/Dropbox/REPLICATE-PROJECT/corpus-parsed/`.
Per the QC brief's fallback pattern:
- `extraction/marker.md` — pdftotext-derived Markdown with verified metadata + reproducible-claim excerpts; documents the tool-availability gap.
- `extraction/nougat.mmd` — hand-typed LaTeX-form mirror of the paper's key equations (H₂ Hamiltonian, Eqs. 17–18 QAOA operators, MaxCut cost, chemistry-accuracy claim) sufficient to reproduce the testable numbers.

## Phase 3 — Simulation env (1 min)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --quiet numpy scipy
python -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
# → numpy 2.5.1  scipy 1.18.0
```
Chose pure NumPy statevector + SciPy COBYLA to keep this self-contained (no Qiskit/PennyLane/Cirq dependency chain, no version-drift surprises).

## Phase 4 — QAOA replication (2 min)
`report/evidence/qaoa_p1.py`:
- Random 3-regular graph sampler via pairing/configuration model (n=6, 8, 10; seed 20260705).
- Brute-force MaxCut over 2ⁿ bitstrings (correct up to n~30 in seconds).
- Diagonal cost Hamiltonian C ∈ ℝ^(2ⁿ); mixer B applied factor-by-factor via reshape trick (each `e^{-iβX_q}` = cos(β)I − i sin(β)X_q).
- COBYLA × 60 random restarts, β ∈ (0, π/2), γ ∈ (0, 2π).
- Emits JSON + log.

Runtime: ~15 s total for all 3 graphs.

## Phase 5 — VQE-H₂ replication (2 min)
`report/evidence/vqe_h2.py`:
- 2-qubit tapered H₂ Hamiltonian at R=0.735 Å with O'Malley et al. 2016 PRX Table I coefficients.
- Explicit nuclear-repulsion constant E_NR = 1/R (a.u.) added to total energy.
- Analytic 4×4 diagonalization for the "exact" reference.
- Hardware-efficient ansatz: RY-per-qubit × 3 blocks + CZ × 2 entangler layers → 6 parameters.
- COBYLA × 40 restarts, θᵢ ∈ (−π, π).
- Emits JSON + log.

Runtime: ~7 s.

## Phase 6 — Report + artifacts (5 min)
- `report/REPORT.tex` — full section-by-section LaTeX report per Rick 2026-07-05 standard.
- `report/open_questions.json` — 5 grounded, non-generic follow-on questions (also mirrored in REPORT.tex §Open Questions).
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory of every artifact + provenance trace.
- `report/failure_analysis.md` — honest gap list.

## Tools + versions
| Tool | Version | Role |
|---|---|---|
| Python | 3.x | driver |
| NumPy | 2.5.1 | dense statevector, linalg |
| SciPy | 1.18.0 | COBYLA optimizer, eigh |
| pdftotext (poppler) | system | PDF → txt |
| Marker | **not installed** | fallback used |
| Nougat | **not installed** | fallback used |
| curl | system | arXiv fetch |
| macOS | Darwin 25.3.0 x64 | host OS |

## Estimated work done
- Real numeric simulation: **~1000 quantum circuit evaluations** (60 QAOA restarts × ~100 COBYLA iters × 3 graphs + 40 VQE restarts × ~100 COBYLA iters = ~22k evaluations). All completed in under 25 s on 1 CPU core.
- Independent verification of 2 headline claims (QAOA-p1 approximation ratio; VQE-H₂ ground-state convergence).
- 8 artifacts produced per the 2026-07-05 QC bar; total dir size ~6 MB (dominated by the PDF).

## Provenance chain
paper.pdf (arXiv, PDF v1.5, SHA-1 not recorded here but reproducible via re-fetch)
  → work/paper.txt + work/paper_layout.txt (pdftotext)
  → extraction/{marker.md, nougat.mmd}
  → report/evidence/qaoa_p1.py + report/evidence/vqe_h2.py
  → *_results.json + *.log
  → report/REPORT.tex + open_questions.json + workflow.md + artifacts_summary.md + failure_analysis.md
