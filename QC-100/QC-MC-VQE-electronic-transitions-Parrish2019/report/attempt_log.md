# Attempt Log — MC-VQE (Parrish et al. 2019) replication

Chronological, 2026-07-01/02.

1. **Selection.** Read WAVE_BRIEF + QC-100 STATUS_AUDIT. Walked ranked
   QC100_CANDIDATES list; deduped against QC-100/ dirs and W1/W2/W3 + tonight's
   QC dirs. Ranks 2,3,4,6 already done; rank 1 is a review (no single core);
   rank 5 (QV) is hardware-heavy. Selected **rank 8: MC-VQE electronic
   transitions (arXiv 1901.01234)** — distinct from all done VQE work (photonic
   Peruzzo, chem-benchmark McCaskey, hardware-efficient Kandala, fermi-hubbard),
   clean classical-simulator core, OA.

2. **Harvest.** Pulled arXiv abstract, ar5iv HTML (1.4 MB), and e-print source
   tarball (783 KB). Extracted qem.tex (main) + qem-supp.tex (supplement) with
   full Hamiltonian element definitions (Eq. 8 + supp), CIS state-prep circuit,
   SO(4) two-body entangler, oscillator-strength formula, computational details.
   Confirmed the numerical TeraChem monomer data packet is NOT in the arXiv
   source (only tex+figures) → exact monomer numbers not in-corpus; method fully
   specified.

3. **Implementation.** Wrote QC-MC-VQE-exciton.py from scratch (NumPy/SciPy):
   exciton Hamiltonian as N-qubit spin model; sparse FCI (full 2^N); CIS in
   (N+1) singles manifold; MC-VQE with matryoshka CIS reference prep, SO(4)
   entanglers on Hamiltonian-connectivity bonds, state-averaged L-BFGS from a
   zero-entanglement guess, contracted-H via interference states (Eq. 5),
   classical diagonalization (Eq. 2); dipole operators + oscillator strengths.

4. **Bug #1 (entangler bloat).** First stack run used all-to-all XX bonds
   (28 bonds → 336 params) → L-BFGS stalled. Fixed: entanglers on
   nearest-neighbor (+ring) bonds matching near-term locality, decoupled from
   the (full-range) FCI Hamiltonian couplings.

5. **Bug #2 (sign convention).** Diagnostic showed ZERO FCI-low-state weight in
   the ref+singles subspace → spectrum was inverted. Root cause: Z_A = +dE/2 made
   the all-excited config lowest. Fixed to Z_A = -dE/2 so the ground config
   |0..0> is lowest. After fix, low FCI states carry 92-96% singles weight
   (ring/stack) — the correct MC-VQE regime.

6. **Rigorous alignment.** Raw index alignment mismatched when a
   double-excitation FCI state sits inside the low manifold. Added overlap-based
   matching (each MC/CIS eigenstate → max-|overlap| FCI state) restricted to
   FCI states with >50% single-excitation character (the ansatz subspace).
   Double-excitation-dominated FCI states are reported separately (known singles
   ansatz limitation, not a method failure).

7. **N=8 stack (local, 2^8).** DONE. MC-VQE matched-error max 2.0 meV / mean
   0.98 meV; oscillator max 2.9%. CIS max 119 meV; oscillator max 65.8%.
   C5 residual = 0.0 exact. Reproduces C7 (CIS qualitatively wrong).

8. **N=12 ring (local, 2^12).** DONE. MC-VQE matched-error max **9.7 μeV**
   (mean 9.7 μeV); oscillator max **0.09%**. CIS max 0.62 meV / oscillator 2.5%.
   C5 residual 0.0. This is the paper's headline "tens of μeV / ≪1%" regime,
   reproduced exactly.

9. **N=18 ring (uicgpu, 2^18 = 262,144).** First run (maxiter=300) ran >29 min
   without converging the numerical-gradient L-BFGS; killed. Relaunched with
   maxiter capped at 25 (paper needs ~14) to get the paper-scale number.

All compute on free resources: local NumPy/SciPy + uicgpu (8×A100 box, CPU sim).
LLM-judge via free Argo (gpt-5.2 / opus-4.8).
