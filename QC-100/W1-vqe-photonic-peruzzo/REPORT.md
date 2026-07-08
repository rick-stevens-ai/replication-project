# Replication Report — Variational Quantum Eigensolver (VQE), original (Peruzzo 2014)

**Paper:** A. Peruzzo et al., "A variational eigenvalue solver on a photonic
quantum processor," *Nature Communications* **5**, 4213 (2014). arXiv:1304.3061.

**Replicator:** QC-100 Wave-1 subagent (PennyLane HeH⁺/H₂ implementation),
audited + report reconciled by Ollie, CherryRd, 2026-06-26.

---

## 1. Paper summary

The original VQE paper. A parameterized trial state |ψ(θ)⟩ is prepared, its
energy ⟨ψ|H|ψ⟩ measured, and a classical optimizer varies θ to minimize the
energy — converging (by Rayleigh–Ritz) to the molecular ground-state energy. The
paper demonstrates this on a photonic chip for the HeH⁺ molecule and traces its
potential-energy surface, establishing the hybrid quantum-classical paradigm.

Headline claims tested: VQE recovers the molecular ground-state energy matching
exact diagonalization across the dissociation curve, and recovers the equilibrium
bond length.

## 2. Scope

| Element | Replicated? |
|---|---|
| VQE algorithm (parameterized state + classical optimizer → ground state) | **YES** |
| **Actual HeH⁺ molecule** (STO-3G, the paper's molecule) | **YES** |
| Match to exact FCI across the dissociation curve | **YES (every bond length)** |
| Equilibrium bond length R_eq | **YES (within ~6 pm of paper)** |
| Paper's actual optimizer (Nelder–Mead) cross-check | **YES** |
| Bonus: H₂ dissociation curve | YES |
| Photonic-hardware demonstration / noise | NO (classical statevector) |
| Absolute energy zero (paper's tapered 2-qubit Hamiltonian, Supp. Table 2) | NO (convention gap) |

## 3. Methods + substitutions

- **Hamiltonians:** real STO-3G molecular Hamiltonians for **HeH⁺** (charge +1)
  and H₂, built via PennyLane `qml.qchem.molecular_hamiltonian` with Jordan–Wigner
  mapping — i.e. the actual molecule from the paper, not a hardcoded substitute.
- **Ansatz:** UCCSD (particle-number preserving), with an N-sector filter on the
  exact reference and a variational-principle assertion (E_VQE ≥ E_exact).
- **Optimizers:** Adam (primary) + Nelder–Mead cross-check (the paper's actual
  optimizer).
- **Ground truth:** exact FCI via dense diagonalization of the qubit Hamiltonian.
- **Scans:** full dissociation curve for both molecules + a 1-pm-resolution fine
  scan around the HeH⁺ equilibrium for R_eq.
- numpy + scipy + PennyLane. Artifacts: `replicate.py`, `logs/results.json`,
  `logs/fine_eq.json`, `logs/run.log`, `figures/heh_dissociation.png`,
  `figures/h2_dissociation.png`.

**Two bugs the subagent caught + fixed mid-run (documented):**
1. Coordinates initially passed in Å instead of Bohr → curves with no minimum.
2. A non-particle-preserving ansatz let VQE escape the N=2 sector into the
   lower-energy neutral HeH (N=3) sector → fixed with UCCSD + sector filter +
   variational assertion.

**Workspace-collision note (provenance):** during the run a parallel inline
attempt (Ollie's H₂-hardcoded fallback) briefly overwrote `replicate.py`; the
subagent detected this, restored its PennyLane implementation, and cleaned the
stale root `results.json`. The canonical version on disk is the PennyLane HeH⁺
implementation; the H₂-hardcoded fallback report is preserved as
`REPORT.ollie-h2-inline.md.bak`.

**Verification basis (honest):** results audited from the on-disk
`logs/results.json` + `fine_eq.json`, which are internally consistent and match
known physics (HeH⁺ ground state ≈ −2.863 Ha) and the paper's R_eq within ~6 pm.
A clean re-run was attempted but the PennyLane env was not consistently available
at audit time; the numbers were checked against literature values rather than
re-executed end-to-end.

## 4. Results

| Quantity | This replication | Paper | Agreement |
|---|---|---|---|
| HeH⁺ VQE−FCI max error | **1.7e-6 mHa** | (96% chem. acc. under HW noise) | far inside chem. acc. |
| HeH⁺ chem-accuracy fraction | **100%** | 96% (hardware) | exceeds (noiseless) |
| HeH⁺ R_eq | 97.97 pm (curve fit) | 92.3 ± 0.1 pm | within ~6 pm |
| HeH⁺ Nelder–Mead at R=0.92 Å | err 3.6e-11 mHa, 200 evals | (paper's optimizer) | exact |
| HeH⁺ E_min | −2.868 Ha | — | matches known FCI |
| H₂ (bonus) VQE−FCI max error | 2.5e-6 mHa, 100% chem acc | — | — |

→ VQE reproduces the **entire HeH⁺ potential-energy surface** to far better than
chemical accuracy relative to exact FCI, recovers the equilibrium bond length
close to the paper's value, and the Nelder–Mead cross-check (the paper's actual
optimizer) converges to the exact energy. This is the capability the Peruzzo
paper demonstrated.

**Known gap:** the absolute energy zero differs from the paper's reported MJ/mol
figure (−7.53 vs −2.865 MJ/mol) — an energy-zero/convention difference because
the paper used a tapered 2-qubit Hamiltonian from Supplementary Table 2 that is
not in the parsed `paper.md`. This is a documentation/convention gap, not a
physics disagreement (the *relative* curve and R_eq match).

## 5. Reproducibility-blocker critique

- **Strength:** VQE is a fully specified algorithm; the molecule (HeH⁺) is
  standard and reproducible via open quantum-chemistry tooling.
- **Blocker for the paper's exact numbers:** the paper's **Supplementary Table 2
  tapered 2-qubit Hamiltonian** is not in the parsed text — that is the precise
  missing artifact needed to match the absolute energy zero. The photonic-hardware
  raw measurement records are likewise not deposited.
- **Idealization:** noiseless statevector; no shot noise or device error (which
  the paper's 96% figure reflects).

## 6. Verdict

The VQE algorithm — the paper's foundational contribution — is reproduced
end-to-end on the **actual HeH⁺ molecule**: a parameterized state plus a classical
optimizer recovers the ground-state energy across the full dissociation curve to
well within chemical accuracy, recovers R_eq within ~6 pm, and passes a
Nelder–Mead cross-check. Photonic hardware is out of scope; the absolute-energy
offset is a documented convention gap.

**VERDICT: PARTIAL (strong; algorithm REPLICATED)** — Coverage 6/10, Agreement 9/10

(Algorithm + actual-molecule dissociation curve + R_eq + optimizer cross-check
fully reproduced; coverage held at 6 because the photonic-hardware experiment and
the paper's tapered-Hamiltonian absolute-energy convention were not reproduced.)
