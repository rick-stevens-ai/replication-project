# Workflow — W1-vqe-photonic-peruzzo (QC-100)

## Paper
Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor," Nat. Commun. 5, 4213 (2014). arXiv:1304.3061.

## Replication pipeline

1. **Paper ingest.** Original arXiv PDF ingested; text extracted to `paper.md` for reference. Supplementary Table 2 (tapered 2-qubit Hamiltonian) noted as absent from the parsed text — this is the source of the absolute-energy-zero convention gap.

2. **Molecule + Hamiltonian construction.** HeH+ (charge +1) at a range of bond lengths, plus H2 as a bonus, built via PennyLane `qml.qchem.molecular_hamiltonian` with the STO-3G basis and Jordan–Wigner qubit mapping. Coordinates converted from angstroms to bohr (this was the first bug caught).

3. **Ansatz.** UCCSD (Unitary Coupled-Cluster Singles and Doubles), particle-number preserving. An earlier non-particle-preserving ansatz was replaced after the run leaked into the neutral-HeH N=3 sector; the fix added an N-sector filter on the exact reference and a variational-principle assertion (E_VQE ≥ E_exact) as a runtime sanity check.

4. **Optimization.** Two independent optimizers:
   - Adam (primary, gradient-based) — used for the full dissociation-curve scans.
   - Nelder–Mead (the paper's actual optimizer) — cross-check at R = 0.92 Å for HeH+, converged to 3.6e-11 mHa in 200 evaluations.

5. **Ground-truth baseline.** Exact FCI via dense diagonalization of the same qubit Hamiltonian. This is the direct classical reference used at every bond length.

6. **Scans.**
   - Full HeH+ dissociation curve (multiple bond lengths from short-range through dissociation).
   - Full H2 dissociation curve (bonus).
   - 1-pm-resolution fine scan around the HeH+ equilibrium bond length for R_eq extraction via curve fit.

7. **Output artifacts.**
   - `replicate.py` — canonical PennyLane implementation.
   - `logs/results.json` — per-bond-length (R, E_VQE, E_FCI, error) records.
   - `logs/fine_eq.json` — fine-scan output around R_eq.
   - `logs/run.log` — runtime log.
   - `figures/heh_dissociation.png`, `figures/h2_dissociation.png`.

8. **Audit + reconciliation (Ollie, 2026-06-26).** Numbers cross-checked against literature values (HeH+ ground state ≈ −2.863 Ha; paper's R_eq = 92.3 pm). A clean re-run was attempted at audit but the PennyLane environment was not consistently available; the audit therefore relies on the on-disk JSON logs plus literature cross-check rather than a fresh end-to-end re-execution.

9. **Backfill (Kukla, 2026-07-06).** Report artifacts added: `REPORT.tex`, `open_questions.json`, `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`; extraction stub `extraction/nougat.mmd`. Top-level `REPORT.md` preserved in place.

## Provenance / cleanup notes

- A parallel inline attempt (H2-hardcoded fallback) briefly overwrote `replicate.py` during the run. The subagent detected the overwrite, restored the PennyLane HeH+ implementation, and cleaned a stale root `results.json`. The H2-hardcoded fallback report is preserved as `REPORT.ollie-h2-inline.md.bak` for provenance.

## What is deliberately out of scope

- Photonic-hardware simulation (dual-rail encoding, photon loss, post-selection statistics).
- Shot-noise / device-error models (this is a noiseless statevector replication).
- Absolute-energy match against the paper's MJ/mol figure (blocked by the missing Supp. Table 2 tapered Hamiltonian).
- Reproduction of the paper's raw hardware measurement records (not deposited).
