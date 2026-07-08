# Workflow, Tools & Effort Estimate — Replication of arXiv:2606.30402

**Paper:** *Quantum Computations on Fusion Blanket Molten Salts*, Das, Pinheiro Dos Santos,
Bhowmik, … Motta, Merz, Beck (IBM Quantum / ORNL / Cleveland Clinic / Michigan State),
arXiv:2606.30402v1, 29 Jun 2026.

**Replicator:** Ollie (OpenClaw agent) on Argonne/home compute, 2026-07-08.

---

## 1. What the paper does (one paragraph)

FLiBe (2LiF–BeF₂) molten salt is the leading blanket material for breeding/recovering
tritium in D–T fusion reactors. Predicting tritium speciation needs accurate correlated
ground-state energies of representative molten-salt clusters. The authors take 21–23-atom
clusters from DFT-AIMD/MLFF trajectories, partition each Hartree–Fock reference with the
**Embedded-Wavefunction (EWF)** method (a DMET-rooted, IAO-localized, MP2-BNO-bath
atom-centered fragmentation, one fragment per atom, in Vayesta), and solve each fragment
Hamiltonian either classically (FCI/CCSD/TCI-8) or on **IBM quantum hardware** (`ibm_boston`,
Heron r3) via **extended sample-based quantum diagonalization (ext-SQD)** using a LUCJ ansatz
(ffsim + Qiskit). Central results: ext-SQD reproduces FCI fragment energies to **0.3 kcal/mol
MAD / 0.7 kcal/mol max**; the dominant error is **fragment construction** (embedding), which
shifts conformational energies by **11–12 kcal/mol** and tritium binding energies by
**~110 kcal/mol** relative to full-molecule methods; all 9 sampled clusters are
single-reference (T1 = 0.014–0.016); tritium binding energies span **−134 to −380 kcal/mol**.

## 2. Reproducibility assessment (before any compute)

| Ingredient | Available to us? | Consequence |
|---|---|---|
| Exact 9 AIMD/MLFF cluster geometries | **No** (not deposited; from private VASP/CP2K trajectories) | Cannot reproduce exact energy numbers; must build our own valid clusters |
| IBM `ibm_boston` Heron-r3 QPU | **No** (no IBM Quantum hardware access) | ext-SQD simulated classically (statevector sampler + selected-CI) |
| PySCF / Vayesta / Qiskit / ffsim / qiskit-addon-sqd | **Yes** (open source) | Full EWF + SQD-simulation pipeline reproducible |
| DFT ladder (PBE-D3, hybrids), RHF/MP2/CCSD, FCI | **Yes** | Full-molecule + fragment reference ladder reproducible |
| DLPNO-CCSD(T) (ORCA) | Optional | Substituted with canonical CCSD + DFT ladder as the full-molecule reference |

**Replication philosophy:** because the exact snapshots are unavailable, this is a
**methodological / qualitative-claims replication**, not a bit-for-bit numeric reproduction.
We reproduce the *pipeline* and test whether the paper's *structural claims* hold on
independently constructed FLiBe clusters of identical stoichiometry, charge, spin and
coordination chemistry.

## 3. Workflow (as executed)

1. **Paper ingestion** — PDF pulled, text extracted (pdftotext -layout; Marker/Nougat as
   available), full methods/SI read; all systems, thresholds, basis, active-space rules,
   and claim numbers transcribed.
2. **Cluster generation** (`build_clusters.py`, ASE) — built chemically valid seed
   geometries for the three systems:
   - System 1 FLiBe: **Li₆Be₃F₁₂** (21 atoms, q=0, singlet)
   - System 2a FLiBeF⁻: **[Li₆Be₃F₁₃]⁻** (22 atoms, q=−1, singlet)
   - System 2b FLiBeTF: **Li₆Be₃F₁₃T** (23 atoms, q=0, singlet); **T modeled as ¹H (protium)** —
     identical electronic structure; E_bind removes T as a bare T⁺/H⁺ nucleus (zero electronic energy).
   Chemistry enforced: tetrahedral BeF₄ motifs, 1 BeF₂ : 2 LiF stoichiometry, F–T–F bridge,
   and the anion sharing the FLiBeTF heavy-atom coordinates minus the proton (exactly the
   paper's E_bind construction). 9 conformers per system via ~0.15 Å thermal rattling to
   emulate finite-T AIMD sampling. **Verified:** RHF on Li₆Be₃F₁₂ in 6-31+G* yields **378 AOs**,
   matching the paper's reported 378 AOs exactly (396 for the anion, 398 for FLiBeTF — the paper
   reports 396/398 for the 22/23-atom systems).
3. **Full-molecule ladder** (`run_ladder.py` / `run_one.py`, PySCF) — per conformer:
   RHF, MP2, CCSD (+ **T1 diagnostic**), and DFT ladder **PBE-D3** (the AIMD functional),
   **B3LYP**, **PBE0**, all in 6-31+G(d) with density fitting + robust convergence
   (level-shift → Newton SOSCF fallbacks for the diffuse ionic basis).
4. **EWF fragmentation + fragment solvers** (`run_ewf_frag.py`, Vayesta + PySCF + ffsim +
   qiskit-addon-sqd) — per conformer: RHF → EWF with **IAO fragmentation, one fragment per
   atom, MP2 BNO bath, threshold η = 1×10⁻⁵** (paper value). Each fragment Hamiltonian
   (via `RClusterHamiltonian.to_pyscf_mf()`) solved by **CCSD**, **FCI** (when the determinant
   space is tractable), and **simulated ext-SQD** (genuine LUCJ-ansatz sampling on a
   statevector simulator + qiskit-addon-sqd subspace diagonalization for M ≤ 16 orbitals;
   selected-CI subspace — the classical analogue of ext-SQD — for larger fragments). Solver
   dispatch mirrors the paper's M ≥ 13 → SQD boundary.
5. **Analysis** (`analyze.py`) — assembles T1 table, conformational relative energies,
   tritium binding energies per method, fragment-level SQD-vs-FCI agreement (MAD/max), and
   the EWF-vs-full-molecule embedding offset. Compared against the paper's reported bands.

## 4. Tools & codes used (with versions)

| Tool | Version | Role |
|---|---|---|
| PySCF | 2.13.1 | RHF/MP2/CCSD/FCI/DFT, integrals |
| pyscf-dispersion | 1.5.0 | DFT-D3(BJ) dispersion |
| Vayesta | 1.0.1 | EWF/DMET fragmentation, IAO, MP2 BNO bath |
| Qiskit | 2.5.0 | quantum SDK (transpilation primitives) |
| qiskit-addon-sqd | 0.12.1 | sample-based quantum diagonalization (subspace solve) |
| ffsim | 0.0.80 | LUCJ ansatz, fermionic statevector sampling |
| qiskit-aer | 0.17.2 | statevector simulation backend |
| ASE | 3.29.0 | geometry construction / XYZ IO |
| NumPy / SciPy | 2.3.0 / 1.17.1 | numerics |
| Python | 3.11.11 | runtime (venv `~/flibe-repl/.venv` on uicgpu) |
| poppler pdftotext | (system) | interim text extraction |

**Compute host:** uicgpu (8× A100 80 GB, 2 TB RAM; CPU-bound electronic-structure here).

## 5. Effort estimate

- **Agent/human steps:** ~1 working session; paper ingestion, 5 Python modules
  (~750 LOC total: build_clusters 8.5 KB, run_ladder 5 KB, run_ewf_frag 7 KB, run_one, analyze),
  environment build (pyscf/vayesta/qiskit stack from scratch incl. Vayesta from GitHub),
  API reverse-engineering for Vayesta 1.0.1 fragment integrals, and iterative debugging of
  SCF convergence + parallel launch harness.
- **Compute:** 27 conformers × (RHF+MP2+CCSD+3×DFT) ≈ full-molecule ladder + 27 conformers
  × EWF (up to ~22 fragments each, solved 3 ways) on uicgpu CPU cores, 4-way conformer
  parallelism. Wall-clock on the order of several hours; ~500 s/conformer for the ladder
  without CCSD, longer with DF-CCSD on 378–398 AO.
- **Runs executed:** 3 systems × 9 conformers = 27 full-molecule ladder jobs + 27 EWF jobs;
  hundreds of individual fragment FCI/CCSD/SQD-sim solves.
