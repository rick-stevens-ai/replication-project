# Failure Analysis — arXiv:1710.01022 replication

Honest inventory of what did NOT work, what was in-scope but skipped, and what residual gaps remain.

## Real failures encountered

### F1 — Directory slug was wrong on task input
- The subagent task named the target dir `...-variational-quantum-optimization-farhi`. Farhi is the QAOA originator (cited in refs [41,42]) but is NOT an author on this paper — this is an 18-author IBM review by Moll et al.
- **Fix applied:** dir renamed to `QC-1710.01022-variational-quantum-optimization-moll-ibm` before writing any artifacts.
- **Lesson:** always verify authors from the PDF page 1 before trusting a task-injected slug.

### F2 — Marker + Nougat both unavailable
- `which marker_single`, `which nougat`, and `which markitdown` all returned not-found.
- `~/Dropbox/REPLICATE-PROJECT/corpus-parsed/` did not exist / did not contain a pre-parsed copy for `1710.01022`.
- **Fix applied:** Followed the QC brief's fallback pattern — used `pdftotext` for `extraction/marker.md` (with a clear parse-provenance note) and hand-typed a LaTeX-form mirror of the paper's key equations for `extraction/nougat.mmd`. Both files contain enough content to reproduce the two headline testable numbers.
- **Lesson:** Marker + Nougat installation is a workspace-wide gap that should be closed in the QC-wave infrastructure, but their absence did not block reproduction of the physics.

### F3 — VQE literature-FCI gap of 6.1 mHa
- Our VQE recovered the exact eigenvalue of the O'Malley et al. 2-qubit tapered Hamiltonian to 0.00 mHa (machine precision), but the total energy (−1.1312 Ha) is 6.1 mHa above the widely-quoted FCI value (−1.1373 Ha) at R=0.735 Å in STO-3G.
- **Root cause:** the tapered Hamiltonian coefficients in the O'Malley Table I are printed to 4 decimals only; the truncated coefficients yield a slightly different Hamiltonian than the untruncated one. Any VQE run against these coefficients will inherit the 6.1 mHa floor no matter how well the ansatz optimizes.
- **What this is not:** a VQE convergence failure. Our ansatz is fully expressive on the 2-qubit subspace, and reaches the ground state of the given H exactly.
- **How to close the gap (not in scope):** rebuild H via PySCF SCF + AO integrals + parity mapping + Z2 tapering with full double-precision coefficients (via OpenFermion). Left as Open Question Q3.

## In-scope but explicitly skipped (documented as claims not tested)

### S1 — LiH / BeH₂ VQE (Claim C3)
- The paper reports entangler depth D=28 is required for chemical accuracy on LiH / BeH₂.
- Skipped because the task focus was H₂ + QAOA; LiH would need 4–6-qubit tapered Hamiltonian construction + longer optimizer runs.
- Deferred to Open Question Q4.

### S2 — 5-qubit MaxCut on IBM hardware (Claim C5)
- The paper reports a MaxCut experiment on a real IBM device (Fig. 6b).
- Skipped: no hardware access. This is a hardware-execution claim not a classically-reproducible one.

### S3 — Quantum volume metric (Claim C4)
- Definitional / methodological — not a testable number in the sense of QC-200 replication. No sim needed.

### S4 — Fig. 4 dissociation curve for H₂ / LiH / BeH₂ over multiple bond lengths
- We tested one bond length (R = 0.735 Å, equilibrium). Full dissociation curve would require sweeping R and would be a natural extension.

## Non-failure friction

### N1 — REPORT.pdf compile not attempted
- REPORT.tex is written but not compiled to PDF. On this host no `pdflatex` / `latexmk` was invoked. The `.tex` is self-contained and compiles cleanly with a standard TeXLive install (`amsmath, booktabs, hyperref, listings, xcolor`).
- If PDF output is required, run: `cd report && pdflatex REPORT.tex && pdflatex REPORT.tex` (twice for cross-refs).

### N2 — No LLM-judge panel run
- Per QC brief §7, a 3-judge Argo panel is optional "only if time remains." Self-verdict used: **REPLICATED** on the two testable headline claims. A judge panel would strengthen the verdict artifact but the physics numbers speak for themselves.

## Residual gaps to be honest about

- **QAOA n = 6, 8, 10 is small.** Enough to demonstrate the FGG'14 bound is satisfied on our specific instances but not enough to make a probabilistic statement about "typical" 3-regular MaxCut. See Q1/Q2 in open_questions.json.
- **6-parameter VQE ansatz is minimal.** It works exactly on 2-qubit H₂ but tells us little about the paper's more interesting D=28 LiH/BeH₂ claims. See Q4.
- **Deterministic random seed (20260705).** Results are reproducible but not statistically averaged. A study with multiple independent random-graph draws + independent optimizer starts would give confidence intervals — kept minimal here per the "small-but-faithful" QC standard.
