# Workflow — urazhdin2023 replication

**Paper:** S. Urazhdin, "Symmetry constraints on the orbital transport in solids," arXiv:2309.04442 (2023).
**Texture class:** orbital (atomic orbital angular momentum transport / crystal-field torque).
**Verdict:** REPLICATED.

## Workflow narrative
1. **Acquire** — pulled PDF from arXiv (2309.04442), validated %PDF.
2. **Extract** — `pdftotext` fallback (Marker CLI unavailable on host) → `extraction/marker.md` (23 KB, clean text; equations readable). Nougat left as stub (no GPU pass needed — paper is analytic).
3. **Method extraction** — parsed the recipe into `report/method_extract.md`: identified 5 central claims (C1-C5), all analytic / minimal tight-binding, no DFT, no data downloads.
4. **Reproduce** — `work/reproduce.py` (pure numpy + sympy), reproducing all 5 claims:
   - C1: symbolic verification of the crystal-field orbital-torque continuity relation Γz = (i/ħ)[U,L̂z] = (r×F)z = −∂U/∂φ.
   - C2: built the t2g cubic-oxide orbital-selective TB Hamiltonian; verified dispersion εm(k) = −2V Σ_{m'≠m} cos(k_{m'}a), band width 8V = 1.6 eV, and degeneracy along ki=kj.
   - C3: 2-level time evolution of a d_xz/d_yz superposition → ⟨Lz⟩ = σħ cos[t(ε2−ε1)/ħ], ⟨Lx⟩=⟨Ly⟩=0; oscillation frequency 1.934×10^14 Hz; analytic vs numeric agreement 1.5×10^-14.
   - C4: triangular-lattice Slater-Koster d-d hopping matrix elements via sympy (V_ddπ=−2/3 V_ddσ, V_ddδ=1/6 V_ddσ) → V22=1/16, V2-2=35/48, V20=−5√3/24; reversal/conserve ratio ≈136-148.
   - C5: relaxation length ~1 lattice constant (follows from C4).
5. **Figures** — `work/figs/c2_dispersion.png`, `work/figs/c3_oscillation.png`.
6. **Report** — this 8-artifact set.

## Tools / codes / versions
- Python 3 (CherryRd), numpy, sympy, matplotlib. No GPU, no cluster.
- `pdftotext` (poppler) for text extraction.

## Effort estimate
- Compute: **minutes** on a single CPU core (all closed-form / small matrices).
- Human/agent: ~1 replication session (acquire → extract → reproduce → report).
- No convergence tuning, no data acquisition, no HPC allocation used.
