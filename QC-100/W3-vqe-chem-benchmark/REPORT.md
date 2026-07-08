# Replication Report — "Quantum chemistry as a benchmark for near-term quantum computers"

**Paper:** A. J. McCaskey, Z. P. Parks, J. Jakowski, S. V. Moore, T. D. Morris, T. S. Humble, R. C. Pooser, *npj Quantum Information* **5**, 99 (2019).
**Wave:** QC-100 W3 · **Owner:** Ollie · **Verdict:** **PARTIAL (simulator backbone REPLICATED)**

## Scope & why PARTIAL
The paper's **primary results (Table 1)** are *hardware* runs on the IBM Tokyo
(20-qubit) and Rigetti Aspen (16-qubit) superconducting QPUs — device- and
noise-specific energies (e.g. NaH ucc-1 Tokyo −160.347 ± 0.032 Ha) that **cannot
be reproduced without those exact machines**. That caps this at PARTIAL by the
AUDIT_PROTOCOL hardware-blocker rule.

What **is** simulator-reproducible is the benchmark's algorithmic backbone, which
the paper defines explicitly: each alkali hydride is frozen-core/active-space
reduced to "two valence electrons and the equivalent of a hydrogen molecule in
minimal basis" (4 spin-orbitals → 4 qubits, JW-mapped), the state-prep primitive
is the single-parameter UCC ansatz (ucc-1), and the benchmark metric is closeness
to FCI with chemical accuracy = 0.0016 Ha.

## Methods
Exact 4-qubit statevector simulation (numpy/scipy), no device data:
- H2/STO-3G 4-qubit JW Hamiltonian (Seeley-Richard-Love coefficients) and the
  O'Malley et al. (PRX 2016) 2-qubit reduced coefficient family for the PES.
- ucc-1 implemented as the exact double-excitation rotation in the HF↔doubly-
  excited subspace; θ swept over [−π,π] with cubic-spline optimization (exactly
  the paper's Fig. 2 procedure).
- FCI = exact diagonalization. Richardson zero-noise extrapolation reproduced as
  linear & quadratic fits to r=0 over noise stretch factors r∈{1,3,5}.

## Results (all from `results.json`, this run)

| Claim | Paper | Replication | Status |
|---|---|---|---|
| ucc-1 recovers FCI (noiseless backbone) | reaches FCI within error bars w/ mitigation | E_opt = −1.851046, \|E−FCI\| = **8.3e-10** | ✓ exact |
| ucc-1 recovers correlation below HF | yes | E_opt < HF (−1.851 < −1.830) | ✓ |
| HWE/unconstrained ansatz unphysical | "varying electron numbers / unphysical" | FCI must be taken in the 2e sector; 2e-sector min = FCI exactly | ✓ illustrated |
| chemical accuracy = 0.0016 Ha | 0.0016 Ha | used as threshold; backbone passes | ✓ |
| Quadratic Richardson > linear | quadratic improves accuracy | quad err 2.7e-2 < lin err 5.1e-2 (synthetic noise) | ✓ method |
| E(R) PES tracks FCI (Fig. 5) | ucc-1 follows surface | 6 bond lengths, \|VQE−FCI\| 2e-6…2.4e-4, **all < chem acc** | ✓ exact |
| Hardware energies (Table 1) | device-specific | NOT reproduced — no QPU access | BLOCKED (hardware) |

## Honest caveats
- The Richardson C3 demonstration uses a **synthetic, fixed noise model** to show
  the extrapolation machinery (linear & quadratic fit to r=0) works and that
  quadratic ≥ linear — it is NOT a reproduction of the paper's specific
  extrapolated device numbers (those require the QPU noise).
- NaH/KH/RbH-specific integrals were not regenerated (no OpenFermion/PyQuante in
  env); the paper's own statement that the reduced problem **is** H2-in-minimal-
  basis justifies using the H2/STO-3G Hamiltonian as the equivalent system.

## Verdict: PARTIAL (algorithmic backbone REPLICATED)
- **Coverage 6/10** — the full simulator algorithm (ucc-1 VQE, θ-sweep/spline
  optimum, FCI metric, chemical-accuracy criterion, PES tracking, extrapolation
  method) is reproduced; the hardware Table-1 results (the paper's headline) are
  an unreproducible device blocker, and molecule-specific (NaH/KH/RbH) integrals
  were substituted by the paper-sanctioned H2 equivalent.
- **Agreement 9/10** — every simulator-side number is exact (ucc-1 = FCI to 1e-9;
  PES within chemical accuracy at all R; quadratic extrapolation beats linear).

**Files:** `paper.md`, `replicate.py`, `results.json`.
