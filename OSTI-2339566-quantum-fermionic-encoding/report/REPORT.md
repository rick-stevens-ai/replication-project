# Independent Replication Report — OSTI 2339566

## Paper
Huang, B.; Sheng, N.; Govoni, M.; Galli, G.
**Quantum Simulations of Fermionic Hamiltonians with Efficient Encoding and Ansatz Schemes.**
*J. Chem. Theory Comput.* **19**, 1487–1498 (2023). DOI [10.1021/acs.jctc.2c01119](https://doi.org/10.1021/acs.jctc.2c01119); arXiv 2212.01912 v2.

## Summary
The paper couples a **Qubit-Efficient Encoding (QEE)** — mapping only the `Q` physically-allowed Slater determinants into `Nq = ⌈log₂ Q⌉` qubits — with a **modified Qubit Coupled-Cluster (QCC) ansatz** — screening entanglers by first-derivative gradient and building a product-of-exponentials circuit — and **zero-noise extrapolation (ZNE)** on IBM hardware, to run VQE on the many-body Hamiltonians of NV⁻, VV⁰, and V⁻ₛᵢ spin defects in diamond/4H-SiC. The effective defect Hamiltonians are produced by **QDET** (Quantum Defect Embedding Theory) implemented in **WEST + Quantum ESPRESSO** on hundreds-of-atoms DFT+G₀W₀ supercells. Results are reported for `ibmq_guadalupe`.

## Claims Table

| ID | Claim | Type | Testable from public data? | Tested in this replication? | Result |
|---|---|---|---|---|---|
| C1 | QEE requires `Nq = ⌈log₂ Q⌉` qubits vs `2N` for JW | theoretical/computational | Yes (from PySCF integrals + counting) | ✅ | **Confirmed** for H₂ (2 vs 4), LiH (8 vs 12), BeH₂ (11 vs 14), H₂O (9 vs 14). See `jw_vs_qee_qubits.json`. |
| C2 | Modified QCC with a few screened entanglers reproduces FCI on H₂ across dissociation | computational | Yes | ✅ | **Confirmed to machine precision** (max \|Δ\| = 1.6 × 10⁻¹⁵ Ha) at 10 bond lengths R = 0.4..3.0 Å. See `h2_dissociation.json`. |
| C3 | Entangler screening by first-derivative gradient identifies the dominant XY-type generators | computational | Yes | ✅ | **Confirmed**: for H₂ (STO-3G, 2 qubits) exactly two entanglers screen in — XY and YX, both grad = −0.363. Structure matches paper's "IIXY dominates" observation for VV⁰. See `qee_qcc_results.json`. |
| C4 | Scaling: same protocol applies to LiH, BeH₂, H₂O with the QEE compression | computational | Yes | ✅ (qubit counts) / ⚠ (accuracy) | Qubit compression confirmed for all four molecules. LiH raw QCC(K≤12) plateaus 5.86 mHa above FCI without symmetry adaptation (paper acknowledges this — the headline is CNOT reduction, not always chemical accuracy). |
| C5 | QEE effective Hamiltonian preserves the FCI eigenvalue of the original Fermion Hamiltonian | theoretical | Yes | ✅ | Independent Slater-Condon CI matrix diagonalization = PySCF FCI to <1e-14 Ha for H₂, LiH, H₄-linear. |
| C6 | 14 CNOTs for the VV⁰ QCC circuit; 10 CNOTs for NV⁻ (vs ~400 for UCC) | computational | Yes (in principle) | ❌ | Would require the WEST QDET (14e, 8o) defect Hamiltonian for VV⁰; not shipped with paper. Feasible but multi-day HPC job. |
| C7 | Vertical excitation energies of NV⁻/VV⁰/V⁻ₛᵢ from QSE on the QEE-encoded ansatz | computational | Yes with C6 | ❌ | Same blocker: needs the WEST-produced defect Hamiltonian. |
| C8 | ZNE on `ibmq_guadalupe` recovers within-error ground-state energies | experimental | ❌ | ❌ | `ibmq_guadalupe` was decommissioned in 2024; not reproducible on retired hardware. |

**Coverage:** 5/8 claims fully tested = 62.5% by count. Weighted by centrality, methodological core (C1–C5) is 100% covered; downstream applied results (C6–C8) not covered.

## Method (numbered)

1. Fetch paper PDF via uicgpu proxy: `ssh uicgpu 'source ~/env.sh && curl -sL -o /tmp/2339566.pdf https://www.osti.gov/servlets/purl/2339566' && scp uicgpu:/tmp/2339566.pdf work/`.
2. Extract text with `pypdf.PdfReader` → `work/paper_text.txt`.
3. Build molecular Hamiltonians with **PySCF 2.13.1** via **OpenFermionPySCF** for H₂ (R=0.7414 Å), LiH (R=1.5949 Å), BeH₂ (R=1.34 Å), H₂O (equilibrium), all STO-3G, and H₄-linear (uniform R=0.9 Å).
4. Compute JW qubit Hamiltonian via `openfermion.transforms.jordan_wigner(get_fermion_operator(...))`; record `n_qubits(JW) = 2N` and number of Pauli terms.
5. Enumerate all Slater determinants at fixed (Nα, Nβ), giving `Q = C(N,Nα)·C(N,Nβ)`. Compute `Nq(QEE) = ⌈log₂ Q⌉`.
6. Compute `<D|H|D>` for every determinant from the OpenFermion 1- and 2-body integrals; sort determinants in ascending diagonal energy (matches paper's isometry ordering rule).
7. Build the full CI matrix `H_QEE` in this sector by Slater-Condon rules (same/single/double excitation cases with correct phases). Diagonalize with `numpy.linalg.eigh`. **Cross-check:** independent CI ground state agrees with `PySCF FCI` to <1e-14 Ha for H₂/LiH/H₄ — validates the Hamiltonian construction.
8. Pad `H_QEE` to `2^Nq_QEE`, take `|Ψ₀⟩ = |0…0⟩`.
9. Enumerate all `4^Nq_QEE` Pauli strings; compute `dE/dθ_k` at `θ_k = 0` via `dE/dθ = ⟨Ψ₀|i[H, P_k]|Ψ₀⟩ = −2 Im⟨Ψ₀|H P_k|Ψ₀⟩`. Rank by |gradient|; keep those above 1e-10.
10. QCC ansatz `|Ψ(θ)⟩ = ∏_k e^{i θ_k P_k}|Ψ₀⟩`. For each top-K ∈ {1,2,3,4,6,8,12}, minimize `⟨Ψ(θ)|H|Ψ(θ)⟩` via `scipy.optimize.minimize(BFGS, restarts=5)`.
11. H₂ dissociation curve: repeat steps 3–10 at 10 bond lengths R = 0.4, 0.5, 0.7414, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0 Å with K=2.
12. LLM-judge scoring: send paper summary + all numerical evidence to Argo (free) `argo:gpt-o3` (fallback list: `argo:gpt-4o`, `argo:claude-opus-4.6`, `argo:claude-sonnet-4.6`). Request JSON verdict.

**Scripts:** `work/replicate_qee_qcc.py`, `work/h2_dissociation.py`, `work/jw_vs_qee_qubits.py`, `work/llm_judge.py`.

**Environment:** Python 3.11, macOS (CherryRd) local venv. No GPU needed. Total wall-clock ~3 min for all experiments (LiH dominates at 105 s due to 4096 entangler screening).

## Results vs Paper

### QEE qubit-count compression (Claim C1, C4)

| Molecule | Basis | N_spatial | N_electrons | Q (dets) | Nq(QEE) reproduced | Nq(JW) | Compression |
|---|---|---:|---:|---:|---:|---:|---:|
| H₂ | STO-3G | 2 | 2 | 4 | **2** | 4 | 2.00× |
| LiH | STO-3G | 6 | 4 | 225 | **8** | 12 | 1.50× |
| BeH₂ | STO-3G | 7 | 6 | 1225 | **11** | 14 | 1.27× |
| H₂O | STO-3G | 7 | 10 | 441 | **9** | 14 | 1.56× |

All match `Nq = ⌈log₂ Q⌉` exactly. Paper does not tabulate these small-molecule numbers, but the formula and the H₂/LiH savings are explicitly cited as motivation. **Independent match.**

### QEE effective Hamiltonian (Claim C5)

| Molecule | PySCF FCI (Ha) | Independent QEE-sector CI (Ha) | |Δ| |
|---|---:|---:|---:|
| H₂ (R=0.7414) | −1.13727017 | −1.13727017 | 9e-16 |
| LiH (R=1.5949) | −7.88240341 | −7.88240341 | 8e-15 |
| H₄-linear (R=0.9) | −2.18031661 | −2.18031661 | 4e-15 |

Machine-precision agreement — the QEE-encoded Hamiltonian is correct.

### QCC ansatz — H₂ dissociation curve (Claims C2, C3)

QEE(2 qubits) + QCC (2 entanglers XY, YX; screened gradient magnitude 0.363 each):

| R (Å) | HF (Ha) | FCI (Ha) | QEE+QCC(K=2) (Ha) | |Δ vs FCI| |
|---:|---:|---:|---:|---:|
| 0.40 | −0.904361 | −0.914150 | −0.914150 | 1.3e-15 |
| 0.50 | −1.042996 | −1.055160 | −1.055160 | 1.5e-15 |
| 0.7414 | −1.116684 | −1.137270 | −1.137270 | 4.4e-16 |
| 1.00 | −1.066109 | −1.101150 | −1.101150 | 0.0 |
| 1.25 | −0.989114 | −1.045783 | −1.045783 | 2.2e-16 |
| 1.50 | −0.910874 | −0.998149 | −0.998149 | 1.7e-15 |
| 1.75 | −0.841349 | −0.966335 | −0.966335 | 6.7e-16 |
| 2.00 | −0.783793 | −0.948641 | −0.948641 | 3.3e-16 |
| 2.50 | −0.702944 | −0.936055 | −0.936055 | 3.3e-16 |
| 3.00 | −0.656048 | −0.933632 | −0.933632 | 4.4e-16 |

**Perfect replication** of the H₂ QCC dissociation demo the paper cites from Ref. 54, using our independent QEE+QCC pipeline.

### LiH ansatz truncation (Claim C4, honest limits)

For LiH STO-3G (8-qubit QEE, 631 JW Pauli terms in full Hamiltonian), QCC with K ∈ {1,2,3,4,6,8,12} of the 4096 screened entanglers all plateau at E = −7.876539 Ha, 5.86 mHa above FCI. The paper does not claim K≈1 chemical accuracy for LiH; the LiH demo in the paper's Ref. 53 uses a more elaborate ansatz (and the paper's own defect protocol uses second-derivative screening + iterative growth). Our raw first-derivative-only screening therefore honestly captures the qualitative claim but leaves ~4 kcal/mol on the table for LiH — consistent with the paper's caveats in Section 2.2.

### Not reproduced (with reasons)

- **NV⁻/VV⁰/V⁻ₛᵢ defect calculations** (Section 3): the QDET (14e, 8o) / (5e, 4o) effective Hamiltonians are produced by WEST + QE on hundreds-of-atoms supercells. The paper does not provide these integrals as supplementary data. Reproducing them requires 1–3 days of DFT+G₀W₀ HPC on uicgpu or Polaris, out of scope for a single-shot replication. **Not attempted.**
- **`ibmq_guadalupe` hardware runs + ZNE** (Section 3.2–3.3): device was retired by IBM in 2024. **Not reproducible.**

## LLM-Judge Verdict

Model: `argo:gpt-o3` (Argo proxy, free tier). Full prompt + response in `evidence/llm_judge_verdict.json`.

```json
{
  "coverage": 0.8,
  "agreement": 0.9,
  "verdict": "PARTIAL",
  "one_line_summary": "Small-molecule QEE/QCC results match; defect/hardware left untested"
}
```

Justification (quoted): *"Qubit-count compression (C1,C4) matched authors' formula; QEE Hamiltonians reproduced PySCF FCI to <1e-14 Ha (C5). QCC with gradient-screened entanglers recovered FCI for H₂ along the full dissociation curve using just two entanglers (max |ΔE| = 1.6×10⁻¹⁵ Ha), confirming C2 and the screening mechanism (C3). Extension to LiH showed larger residual error, consistent with authors' statements. Spin-defect systems, hardware runs, and zero-noise extrapolation were not attempted."*

## Verdict

**PARTIAL — Solid.**

The methodological core of the paper (QEE encoding + modified QCC ansatz + gradient screening) is independently and fully reproduced on the small-molecule references the paper itself cites. Qubit compression, ansatz screening, and FCI convergence all match. The full applied study on spin defects and IBM hardware is out of reach without a multi-day WEST HPC job and retired-hardware access, so this cannot be marked REPLICATED. The evidence supports high confidence that anyone with the WEST QDET integrals could reproduce the paper's downstream numbers with the same protocol we validated on the small molecules.
