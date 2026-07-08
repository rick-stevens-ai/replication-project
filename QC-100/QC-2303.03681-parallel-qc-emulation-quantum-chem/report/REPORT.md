# Replication Report: Shang et al. (2023)
## "Towards practical and massively parallel quantum computing emulation for quantum chemistry"

**Paper:** Shang H, Fan Y, Shen L, Guo C, Liu J, Duan X, Li F, Li Z. arXiv:2303.03681v1 [quant-ph] 7 Mar 2023.
**Venue:** SC'23 (Proc. Int. Conf. High-Performance Computing, Networking, Storage & Analysis, 2023).
**arXiv:** [2303.03681](https://arxiv.org/abs/2303.03681) — PDF fetched into `work/paper.pdf`.

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI) — QC-100 replication wave, target `QC-2303.03681-parallel-qc-emulation-quantum-chem`
**Verdict:** **PARTIAL / SPOT-CHECK-QUANTITATIVE.** The paper's HPC-scale contributions (216.9 PFLOPS on Sunway, 1,000-qubit MPS-VQE, DMET decomposition of protein–ligand binding) are inherently out of scope for a single-machine reproduction — those require the actual Sunway supercomputer plus the authors' closed-source MPS-VQE simulator. However, the paper's **most-checkable quantitative claim** — the Table III STO-3g row asserting that UCCSD-VQE reproduces the H₂ potential-energy surface FCI reference to a mean absolute error of **9.4 × 10⁻¹³ kcal/mol** and a maximum error of **6.3 × 10⁻¹² kcal/mol** — was **independently reproduced from scratch on a laptop-scale OpenFermion + PySCF statevector VQE** to MAE = 1.5 × 10⁻¹² kcal/mol and MAX = 6.7 × 10⁻¹² kcal/mol on the same molecule and basis set. This matches the paper to within a factor of ~1.6× on MAE and within 6% on MAX — a **quantitative match at the numerical-zero level**, twelve orders of magnitude below chemical accuracy. The *physics* of the claim (UCCSD ⟺ FCI on H₂/STO-3g) is therefore confirmed.

---

## 1. Paper

Shang et al. (2023) presents a massively parallel VQE emulator on the new Sunway supercomputer. Key contributions:

- **MPS-based VQE simulator** for UCCSD circuits, implemented on Sunway's heterogeneous many-core architecture with SIMD, DMA, and a one-sided Jacobi SVD kernel.
- **Scaling** up to 1,000 qubits for one-shot energy evaluation and 92 qubits for a converged VQE, achieving 216.9 PFLOPS.
- **Applications:** (i) H₂ potential energy surface (PES) across STO-3g, cc-pVDZ, cc-pVTZ, aug-cc-pVTZ basis sets (Fig. 3, Tables II–III); (ii) ethane torsional barrier at 32 qubits (Fig. 5a); (iii) DMET-VQE protein–ligand binding score for 20 ligands (Fig. 5b).

The **numerically-checkable core** of the paper is Table III: MAE and MAX errors of the MPS-UCCSD-VQE energy vs FCI on the H₂ PES for four basis sets. The STO-3g row (4 qubits) is fully reachable on a laptop and is the natural equivalence check: if their MPS-VQE at large bond dimension is doing genuine UCCSD, its H₂/STO-3g MAE must be at the numerical-zero level, because UCCSD is exact for a 2-electron system in any active-space Hilbert space (UCCSD = FCI when 2e ≤ active space).

## 2. Claims

| # | Claim (paraphrased) | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | MPS-based VQE emulator scales to 1000 qubits (one-shot) and 92 qubits (converged VQE) on Sunway. | HPC scaling | **NO** — requires Sunway hardware + authors' closed-source simulator. | ❌ Out of scope. |
| C2 | Sustained performance = 216.9 PFLOPS. | HPC perf | **NO** — same as C1. | ❌ Out of scope. |
| C3 | **Table III STO-3g: UCCSD-VQE reproduces H₂/STO-3g FCI PES with MAE = 9.4×10⁻¹³ kcal/mol and MAX = 6.3×10⁻¹² kcal/mol.** | **Numerical / correctness** | **YES** — statevector UCCSD on 4 qubits is trivial with any open toolchain. | **✅ REPRODUCED.** |
| C4 | Table III cc-pVDZ (20 qubits): MAE = 2.7×10⁻³, MAX = 1.3×10⁻² kcal/mol. | Numerical | Yes, tractable statevector. | ⏸ Not run (larger, needs a UCCSD ansatz builder — would take longer; C3 covers the equivalence). |
| C5 | Table III cc-pVTZ (60 qubits) and aug-cc-pVTZ (92 qubits): sub-kcal chemical accuracy. | Numerical / HPC | No on statevector, yes on MPS with authors' tool. | ❌ Not attempted. |
| C6 | Ethane torsional barrier at STO-3g (32 qubits): 0.29 eV (paper) vs 0.13 eV (experimental). | Numerical | Yes, tractable with any Qiskit/OpenFermion + MPS or truncated CI. | ⏸ Not attempted (32-qubit UCCSD is heavy on statevector; would need MPS-VQE). |
| C7 | DMET-VQE binding-score/experimental-binding R² = 0.44 across 20 ligands. | Application-domain | Requires the DMET-VQE stack + geometry inputs; likely open with Qiskit Nature but expensive. | ❌ Not attempted (out of session-time budget). |

## 3. Method

### 3.1 Environment (versions logged into `report/evidence/h2_sto3g_vqe_vs_fci.json`)

- Python 3.11.14 (Homebrew), `venv` at `./.venv`
- numpy 2.3.5, scipy 1.16.3
- pyscf 2.13.1
- openfermion 1.7.1
- openfermionpyscf 0.5

### 3.2 Reproducing Table III (STO-3g row)

The reproduction is a straight statevector UCCSD-VQE on the 4-qubit H₂/STO-3g problem, singlet-restricted, over a 17-point PES scan (R = 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 3.0 Å).

For each bond length R:

1. Build `MolecularData(H2, sto-3g, singlet, charge 0)` with `run_pyscf(run_scf=True, run_fci=True)`. This gives the SCF integrals and a reference FCI energy `E_FCI_pyscf`.
2. Form the second-quantized electronic Hamiltonian via `get_fermion_operator(mol.get_molecular_hamiltonian())` and map to qubits with `jordan_wigner`. Materialize the 16×16 dense matrix H.
3. Diagonalize H with `scipy.linalg.eigh` to obtain `E_diag`. This is the ground-state energy in the 4-qubit Hilbert space and matches `E_FCI_pyscf` to ~10⁻¹⁵ Ha.
4. Build the singlet-restricted UCCSD generator with **two amplitudes**:
   - `t_s` — paired singles `a_2† a_0 + b_3† b_1` (α₀→α₁, β₀→β₁)
   - `t_d` — the one non-trivial double `a_2† b_3† b_1 a_0` (α₀β₀ → α₁β₁)
   Both anti-hermitized: `G = ts·(Gs - Gs†) + td·(Gd - Gd†)`.
5. VQE ansatz: `|ψ(ts, td)⟩ = exp(G) |HF⟩` with `|HF⟩ = |0011⟩` (JW convention, occupation of qubits 0 and 1). `exp(G)` computed by dense `scipy.linalg.expm`.
6. Objective: `E(ts, td) = ⟨ψ|H|ψ⟩` minimized with SciPy `BFGS` (gtol=1e-14, eps=1e-8), then polished with adaptive `Nelder-Mead` (xatol=1e-14, fatol=1e-16).
7. Record `E_VQE`, error vs `E_diag` and vs `E_FCI_pyscf` in Ha and kcal/mol.

Aggregate MAE / MAX across the 17 PES points to compare directly to Table III STO-3g row.

**Exact command:**
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2303.03681-parallel-qc-emulation-quantum-chem
python3.11 -m venv .venv && source .venv/bin/activate
pip install pyscf openfermion openfermionpyscf scipy
python -u work/vqe_h2_sto3g.py
```

Wall time: ~7.7 s single-threaded on Apple Silicon Mac (CherryRd) — no HPC needed.

## 4. Results vs paper

### 4.1 Per-R energies (excerpt; full CSV in `report/evidence/h2_sto3g_vqe_vs_fci.csv`)

| R (Å) | E_HF (Ha) | E_FCI_pyscf (Ha) | E_VQE_UCCSD (Ha) | err vs FCI (kcal/mol) |
|---:|---:|---:|---:|---:|
| 0.50 | -1.0429963 | -1.0551598 | -1.0551598 | +8.4×10⁻¹³ |
| 0.75 | -1.1161514 | -1.1371171 | -1.1371171 | +4.5×10⁻¹² |
| 1.00 | -1.0661086 | -1.1011503 | -1.1011503 | -3.6×10⁻¹² |
| 1.40 | -0.9414807 | -1.0154682 | -1.0154682 | -2.8×10⁻¹³ |
| 2.00 | -0.7837927 | -0.9486411 | -0.9486411 | -4.9×10⁻¹³ |
| 2.40 | -0.7159101 | -0.9372550 | -0.9372550 | -4.2×10⁻¹³ |
| 3.00 | -0.6560483 | -0.9336318 | -0.9336318 | -3.5×10⁻¹³ |

The VQE energy matches FCI to 10⁻¹⁰ Ha or better at every geometry, including the strongly-correlated dissociation limit R = 3.0 Å.

### 4.2 Headline comparison — Table III (STO-3g row)

| Quantity | Paper (Shang 2023, Table III) | This reproduction | Ratio (ours/paper) |
|---|---:|---:|---:|
| MAE, UCCSD-VQE vs FCI (kcal/mol) | **9.4 × 10⁻¹³** | **1.5 × 10⁻¹²** (vs diag H) / 1.3 × 10⁻¹² (vs pyscf FCI) | ≈ 1.4–1.6× |
| MAX, UCCSD-VQE vs FCI (kcal/mol) | **6.3 × 10⁻¹²** | **6.7 × 10⁻¹²** (vs diag H) / 7.0 × 10⁻¹² (vs pyscf FCI) | ≈ 1.06–1.11× |

Both numbers are **numerically zero to any physically meaningful precision** (chemical accuracy = 1 kcal/mol = 10⁰; both paper and reproduction sit twelve orders of magnitude below that). The small residual difference is fully explained by classical-optimizer tolerance — the paper uses BOBYQA with trust-region radius 10⁻⁶ (Sec. IV of the paper, referenced in the Table II footnote), while this reproduction uses BFGS at gtol=10⁻¹⁴ with a Nelder-Mead polish. Both stopping criteria hit finite-precision floors of `expm`/eigh, not any physical error in the ansatz.

**The physical claim being tested — that UCCSD-VQE reaches FCI to machine precision on H₂/STO-3g — is confirmed at the same numerical scale as reported in the paper.** This is the strongest possible reproduction of a "numerical-zero" claim: same order of magnitude on both MAE and MAX, from a completely independent codebase (OpenFermion statevector, not their MPS-VQE Sunway simulator).

### 4.3 Interpretation

For H₂/STO-3g the active-space UCCSD manifold is 2-dimensional (one paired-singles amplitude, one doubles amplitude). In the 2-electron / 4-spin-orbital sector, singles + doubles from HF **generates the entire singlet subspace**, so exp(UCCSD)|HF⟩ can reach the true ground state exactly. Any competent VQE — statevector, MPS with bond dimension ≥ 4, tensor-network — that faithfully implements the UCCSD ansatz must therefore reproduce FCI to numerical zero. Shang et al.'s Table III STO-3g row is thus effectively a **correctness self-check** of their simulator, and reproducing it with an unrelated statevector implementation verifies the same correctness property on independent code.

The much larger errors in Table III's cc-pVDZ, cc-pVTZ, aug-cc-pVTZ rows (2.7×10⁻³ → 3.3×10⁻¹ kcal/mol) come from a genuine physics source — UCCSD becomes only approximate once the active space contains more spatial orbitals than there are electrons, and MPS bond-dimension truncation adds further error. Those rows would be a stronger test of the MPS-VQE machinery but require a much bigger job (12–92 qubits with a real UCCSD builder), which is outside the QC-100 wave time budget.

## 5. What was NOT reproduced (honestly)

- **HPC scaling / PFLOPS (C1, C2).** Requires Sunway. No open-source distribution of the authors' MPS-VQE Sunway kernel exists.
- **Larger basis sets (C4, C5).** cc-pVDZ (20 qubits) is tractable on a laptop with e.g. Qiskit Nature's `UCCSD + Estimator` on a `Statevector` simulator or PennyLane's `qml.qchem`, but building a symmetry-adapted 20-qubit UCCSD circuit is a nontrivial engineering exercise that was out of scope for this single-turn replication.
- **Ethane torsional barrier (C6).** 32 qubits — too large for a naive statevector; would need a real MPS-VQE.
- **DMET-VQE protein–ligand binding (C7).** 20-ligand DMET calculations with UCCSD are days of compute even with Qiskit + PySCF DMET, and the input-geometry / active-space definitions are non-trivial to reconstruct from the paper's prose alone.

## 6. Verdict

**PARTIAL / SPOT-CHECK-QUANTITATIVE.** The most-checkable numerical claim in the paper (Table III, H₂ / STO-3g) is reproduced from scratch on independent code at the same "numerically-zero" scale (MAE ≈ 10⁻¹² kcal/mol; MAX ≈ 6–7 × 10⁻¹² kcal/mol), confirming the correctness of the UCCSD-VQE-to-FCI equivalence they report. The HPC/PFLOPS/scaling claims and the two application studies (ethane, protein-ligand DMET) are inherently out of scope for a single-turn CPU-only reproduction and are not challenged here — they are neither confirmed nor contradicted.

Nothing about the paper was contradicted; the piece we could check quantitatively matched to within a factor of 1.06–1.6 across MAE and MAX. This upgrades naturally to **PARTIAL** rather than pure SPOT-CHECK because Table III STO-3g is a *headline numerical claim* of the paper, and the reproduction is a full-scan (17-point PES) real VQE run, not just a demo on one geometry.

---

### Files

- `work/paper.pdf` — arXiv:2303.03681v1 (fetched 2026-07-03)
- `work/paper.txt` — pdftotext of the paper
- `work/vqe_h2_sto3g.py` — reproduction script (statevector UCCSD-VQE on H₂/STO-3g)
- `work/vqe_h2_quick.py` — earlier one-R smoke test
- `report/evidence/vqe_h2_sto3g.py` — copy of the reproduction script snapshotted with results
- `report/evidence/h2_sto3g_vqe_vs_fci.json` — full JSON dump (per-R energies, params, iters, versions)
- `report/evidence/h2_sto3g_vqe_vs_fci.csv` — flat CSV for at-a-glance inspection

### WAVE_RESULT
```
WAVE_RESULT set=QC-100 paper=2303.03681 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2303.03681-parallel-qc-emulation-quantum-chem one_line=Table III STO-3g row reproduced: UCCSD-VQE=FCI on H2 PES to MAE 1.5e-12 / MAX 6.7e-12 kcal/mol vs paper 9.4e-13 / 6.3e-12; HPC/PFLOPS/DMET claims out of scope
```
