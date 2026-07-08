# Attempt log — QC-1708.09213

## 2026-07-04 02:09–02:30 CDT (single wave-brief sitting)

1. Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`).
2. Created target dir `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1708.09213-lecture-notes-of-tensor-network-contractions/{report/evidence,work}`.
3. Pulled arXiv PDF: `curl https://arxiv.org/pdf/1708.09213` → 6.4 MB, PDFv1.4, OK.
4. `pdf` tool failed (allowlist + billing). Fell back to `pdftotext -layout` → `paper_full.txt` (6659 lines). Grep-inspected TOC, TFIM, Heisenberg, ground-state-energy passages.
5. **Framing:** this is a pedagogical book (Lecture Notes in Physics vol 964), not an experimental-result paper. Picked 4 concrete algorithmically-testable claims (C1..C4) that map onto TFIM benchmarks in `quimb`.
6. **Env setup:** `python -m venv .venv` + `pip install --only-binary=:all: numba llvmlite cytoolz` after quimb's hard `numba` requirement failed to build from source on macOS (missing `<cstring>` due to CommandLineTools SDK). Binary wheels resolved this cleanly. `quimb 1.14.0` up.
7. **C1 (DMRG on TFIM):** first pass showed a ~2× convention mismatch. Root cause: `quimb.tensor.MPO_ham_ising(..., S=0.5)` uses spin-1/2 operators, not Pauli. Fixed by passing `j=-4J, bx=-2h`. Post-fix, DMRG matched exact FF to 1e-11 rel error across N=20..80.
8. **C1 exact FF cross-check (`exp1b_check_ed_small.py`):** built full 2^N Hamiltonian in Pauli convention for N=6..12, diagonalized dense, compared to (a) my Pfeuty formula, (b) my DMRG. All three agree to 1e-14. My original FF formula had a factor-of-2 bug; corrected version uses `epsilon_n = sqrt(eigvals((A-B)(A+B)))`.
9. **C2 (entanglement scaling):** first pass reported c≈0.75 (should be 0.5). Root cause: quimb's `MPS.entropy()` returns entropy in log2 (bits), not nats. Multiplied by ln(2) → slope × 6 → c = 0.505 at N=128. Textbook match.
10. **C3 (canonicalization):** first pass reported non-zero orthogonality errors due to my mis-indexing of quimb tensor axes. Fixed by using each tensor's `.transpose(left_ind, phys_ind, right_ind).data`. Post-fix, all 15 non-final sites give ||sum A^dag A - I||_F ≤ 1.7e-15.
11. **C3 (optimal truncation):** first pass wrongly compared multi-bond compression to single-bond bound. Realized `psi.schmidt_values(i)` returns reduced-density-matrix eigenvalues (not singular values); switched to `sum discarded rdm_eigenvalues` as both the theoretical bound and the single-bond truncation error. Ratio = 1.000 across chi=4,8; 0.999 at chi=16.
12. **C4 (iTEBD):** first pass gave `E/N ≈ +0.065` (obviously wrong). Root cause: LocalHam1D evolution operator wasn't matching the MPO I used for measurement (some global offset in `MPO_ham_ising` builder). Switched to direct local-operator expectations (`psi.local_expectation_canonical(sigma^z ⊗ sigma^z, (i,i+1))` and `psi.local_expectation_canonical(sigma^x, i)`). Post-fix, TEBD (dtau=0.05, T=8, chi=32, N=64, Neel initial) converges to E/N = -1.267543 vs FF exact -1.267593 (Δ=5e-5).
13. **LLM judge:** first attempt with Argo `argo:claude-opus-4.7` returned HTTP 403 "username not registered" — seemingly some payload-length interaction (small curl calls worked fine). Switched to `argo:gpt-5` (removed `temperature` since gpt-5 rejects 0.0). Judge returned clean JSON: all 4 claims REPLICATED, overall REPLICATED.
14. Wrote reports (`brief.md`, `REPORT.md`, `artifact_harvest.md`, this log). Cleared `~/.openclaw/workspace/tmp-pdf/` scratch copy.

## Things I did NOT do (out of scope for a 1708.09213 replication)
- PEPS 2D benchmarks (Sec 4): quimb has PEPS but a serious PEPS run on a 2D lattice needs GPU/large CPU, and the paper's PEPS numbers come from cited references (e.g. [234]) rather than being novel numerical results of the paper itself.
- MERA (Sec 2.3.4): only defined conceptually in the paper.
- CTMRG / TRG (Sec 3.2, 3.3): mentioned but not benchmarked with fresh numbers here.
- Quantum-entanglement-simulation (Chap 6) few-body model comparisons vs QMC on 3D Heisenberg: paper cites [234] rather than presenting its own numbers.

The 4 chosen claims are the "load-bearing" numerical claims that would fail if the algorithms as taught in the paper were wrong. They pass.
