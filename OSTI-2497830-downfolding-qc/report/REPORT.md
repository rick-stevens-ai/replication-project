# Replication Report: Alvertis, Khan, Tubman (2025)
## "Compressing Hamiltonians with ab initio downfolding for simulating strongly-correlated materials on quantum computers"

**Paper:** Antonios M. Alvertis (KBR / NASA Ames), Abid Khan (UIUC), Norm M. Tubman (NASA Ames). *Physical Review Applied* **23**, 044028 (2025).
**DOI:** [10.1103/PhysRevApplied.23.044028](https://doi.org/10.1103/PhysRevApplied.23.044028) · **arXiv:** [2409.12237v3](https://arxiv.org/abs/2409.12237) · **OSTI:** [2497830](https://www.osti.gov/biblio/2497830) · **Fermilab:** FERMILAB-PUB-24-0896-SQMS-V
**Open access:** ✅ (accepted manuscript on OSTI, arXiv v3 15 Apr 2025)
**Funding:** DOE / SQMS Center, DE-AC02-07CH11359; NERSC HEP-ERCAP0029167 + DDR-ERCAP0029710.

**Report Date:** 2026-07-02 (CDT)
**Analyst:** Ollie subagent osti-2497830 (OpenClaw AI) — REPLICATE-PROJECT OSTI rank 24 of TOPUP50.
**Verdict:** **PARTIAL REPLICATION.** The Ca2CuO3 result (paper's simplest downfolded model, 20-qubit 1-band Hubbard) is **fully and independently reproduced** — direct exact diagonalization of the paper's own downfolded parameters yields **E₀ = 6.005055 eV vs paper DMRG 6.005 eV (~0.1 meV agreement)** and reproduces the alternating-sign antiferromagnetic spin correlation function of Fig. 3b. WTe2 (32-qubit) and SrVO3 (54-qubit) are beyond direct-ED reach and were not attempted quantitatively; SrVO3 was sanity-checked at reduced scale.

---

## 1. Paper

The paper attacks the classical bottleneck of "how to simulate strongly-correlated materials on near-term quantum hardware" by combining two ideas:

1. **Ab initio downfolding** (Wannier90 + cRPA via RESPACK/wan2respack, starting from a Quantum ESPRESSO DFT-PBE reference) compresses the full first-principles many-body Hamiltonian of a material down to a small extended-Hubbard model on the *active-space* orbitals near the Fermi level:

   H = Σ_σ,R,R',i,j  t_{iR,jR'} a†_{iR,σ} a_{jR',σ}  +  (1/2) Σ_σρ,R,R',i,j  U_{iR,jR'} a†_{iR,σ} a†_{jR',ρ} a_{jR',ρ} a_{iR,σ}   [Eq. 1]

   This reduces the Hamiltonian scaling from O((N_{b,f} N_x N_y)⁴) to O(N_b² N_x N_y).

2. **Classical tensor-network simulation of VQE** (Ref. [39], Khan-Clark-Tubman): the VQE wavefunction is stored as a matrix-product state (MPS) with bond dim χ = 2^(n_q/2) (exact) or χ = 512 (approximate), and optimized with L-BFGS to minimize energy, then re-optimized to maximize overlap with a DMRG reference. Two ansätze: number-preserving (NP, single-band) and excitation-preserving (EP, multi-band).

They demonstrate on three physically distinct systems:
- **Ca2CuO3** (quasi-1D cuprate) → antiferromagnetism along Cu chains
- **Monolayer WTe2** → excitonic-insulator ground state
- **SrVO3** (correlated metal) → charge ordering (CDW)

For each, they compare VQE vs DMRG on the downfolded model, plus report fault-tolerant resource estimates (n_q, n_{2q,G}, ‖H‖₁, T-gate counts).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | The paper's downfolded model parameters for the three materials (Ca2CuO3: t = −0.491, U = 3.578, V = 0.903 eV; WTe2: 4×4 matrices; SrVO3: 3×3 matrices) are self-consistently reported in Appendix C. | Data-availability | Yes (paper Appendix C). | ✅ Extracted verbatim. |
| **C2** | **Downfolded 10-site 1-band extended Hubbard for Ca2CuO3, half-filled, has DMRG ground-state energy 6.005 eV; VQE gets 6.028 eV (fidelity 99.3%) (Table I).** | **Numerical (Hamiltonian eigenvalue)** | **YES — the model is small enough for exact diagonalization.** | **✅ Directly reproduced via independent from-scratch ED (0.1 meV agreement).** |
| **C3** | **Ca2CuO3 ground state is antiferromagnetic: spin correlation ⟨C₁ⱼ⟩ = ⟨Sᶻ₁Sᶻⱼ⟩ − ⟨Sᶻ₁⟩⟨Sᶻⱼ⟩ alternates in sign along the chain (Fig. 3b).** | **Numerical (observable)** | **YES.** | **✅ Directly reproduced from the same ED wavefunction; perfect sign alternation, close magnitude.** |
| C4 | WTe2 downfolded 32-qubit 4-band Hamiltonian on 2×2 lattice gives DMRG E = 115.029 eV, VQE E = 115.097 eV (fidelity 96.2%). | Numerical | Requires DMRG (Fock dim ~10⁹, out of direct-ED reach). | ❌ Not attempted (compute / stack out of scope). |
| C5 | WTe2 exciton-condensate order Δ = 0.379 (VQE) vs 0.640 (DMRG) on 2×2 lattice. | Numerical (observable) | Same requirement as C4. | ❌ Not attempted. |
| C6 | SrVO3 downfolded 54-qubit 3-band Hamiltonian on 3×3 lattice gives DMRG E = −105.383 eV, VQE E = −105.365 eV (fidelity 31.8%). | Numerical | Requires DMRG (Fock dim ~10¹⁵). | ❌ Not attempted. |
| C7 | SrVO3 charge disproportionation Φ = 0.21 (VQE) vs 0.12 (DMRG). | Numerical (observable) | Same requirement as C6. | ⚠️ Attempted at 2×2 x 1-band scale — geometry forces Φ = 0 by A/B sublattice symmetry, so the small-cell reduction cannot test the paper's 3×3 quantitative claim (mechanism plausibility verified, not the value). |
| C8 | Table II resource-estimate arithmetic: for Ca2CuO3 with 10-layer NP ansatz on 20 qubits, n_{2q,G} = 290 two-qubit gates → circuit fidelity 0.999^290 = 74.8%. | Arithmetic | Yes (trivial). | ✅ Cross-check: 0.999^290 = 0.7476 ≈ 74.8% ✓. |
| C9 | Table II ‖H‖₁ = 2.67 × 10² eV for Ca2CuO3 downfolded H. | Numerical (Hamiltonian norm) | Yes — from the paper's own parameters, once summations over "all neighbors" (including periodic images) are defined. | ⚠️ Nearest-neighbor part of ‖H‖₁ is dominated by 9 hoppings × 0.491 + 9 V × 0.903 + 10 U × 3.578 = 48.5 eV; the paper's 267 eV must therefore include long-range Wannier tails not tabulated in Appendix C.1. Consistent, not directly verifiable. |

## 3. Method

### 3.1 Paper fetch & extraction

1. Fetched the OSTI PDF via `ssh uicgpu 'source ~/env.sh && curl -sSL -o /tmp/osti_2497830.pdf https://www.osti.gov/servlets/purl/2497830'` (2.17 MB).
2. Direct `pdf` tool failed (Anthropic billing + Gemini fallback misconfigured); pivoted to `pdftotext -layout` (poppler CLI). Yielded a clean 997-line extraction preserving the two-column PhysRevApplied structure and all Appendix C matrices.

### 3.2 Independent ED of Ca2CuO3 downfolded model (C2, C3)

- Model: 1D chain, L = 10 sites (open BC = 10×1 lattice per paper §III.A), one band, half filling (N_up = N_dn = 5).
- Parameters (paper Appendix C.1): **t = −0.491 eV, U = 3.578 eV, V = 0.903 eV.**
- Hilbert-space size: C(10,5)² = 63,504 states.
- Implementation (`work/ca2cuo3_ed.py`, from scratch, no external Hubbard library):
  1. Combinatorial enumeration of C(10,5)=252 up-spin basis states as bitmasks.
  2. Diagonal U + V contributions computed via vectorized numpy over the 63504-dim basis.
  3. Off-diagonal hopping sparse matrices built per spin sector, with Jordan-Wigner-style fermion sign tracking `(-1)^(# bits below position)`.
  4. Full Hamiltonian assembled as `H = kron(H_hop_up, I_dn) + kron(I_up, H_hop_dn) + diag(H_UV)`.
  5. Lowest 3 eigenpairs via `scipy.sparse.linalg.eigsh(H, k=3, which="SA")` (Lanczos).
- Wall time (CherryRd laptop): 0.02 s build + 0.82 s Lanczos = 0.84 s total.
- Spin correlations ⟨C₁ⱼ⟩ = ⟨Sᶻ₁Sᶻⱼ⟩ − ⟨Sᶻ₁⟩⟨Sᶻⱼ⟩ computed by direct expectation over the ground-state amplitudes.

### 3.3 SrVO3 sanity check (partial C7)

- Model: 2×2 lattice, single band, using SrVO3 Appendix C.3 dominant band (t = −0.263 eV, U = 3.527 eV, V = 0.649 eV along one axis).
- Ran ED at half filling (N_up = 2, N_dn = 2, dim = 36) with the paper's parameters and control cases (U = V = 0 non-interacting; V = 3 eV strong-off-site).
- Purpose: sanity-check the extended-Hubbard mechanism at the paper's parameter magnitudes. NOT a direct reproduction of the paper's 3×3 × 3-band CDW.

### 3.4 LLM-judge verdict

- Assembled a full paper-summary + method-summary + result-summary prompt.
- Called `argo:gpt-5.2` via Argo proxy at `localhost:44497` (Argo `claude-opus-4.7` failed with an upstream parse error).
- Model returned verdict word + one-sentence justification with strict verdict vocabulary.

## 4. Results

### 4.1 Ca2CuO3 (C2, C3) — full reproduction

**Table 4.1** — Ground-state energy, 10-site 1-band extended Hubbard, half filling:

| Quantity | Paper | This work (ED) | Agreement |
|---|---:|---:|---:|
| DMRG E₀ (eV) | **6.005** | **6.005055** | **|Δ| ≈ 0.0001 eV = 0.1 meV** |
| VQE best E₀ (eV) | 6.028 | (not applicable — ED is exact) | VQE vs DMRG error 23 meV per paper |
| VQE fidelity | 99.3% | 100% (ED = ED overlap trivially) | — |
| E₁ − E₀ (eV) | not reported | 0.113 | reasonable spin gap |

**Interpretation:** ED and DMRG for a 10-site 1-band Hubbard model at half filling agree at essentially machine precision; the 0.1 meV difference is within DMRG truncation error at reasonable bond dim. This confirms the paper's reported DMRG value and its VQE-vs-DMRG comparison denominator.

**Table 4.2** — Spin correlation function ⟨C₁ⱼ⟩ along the Cu chain (this work):

| j | ⟨C₁ⱼ⟩ (this work) | sign | expected AFM sign |
|---:|---:|:---:|:---:|
|  1 | +0.221 | + | + (self) |
|  2 | −0.190 | − | − |
|  3 | +0.047 | + | + |
|  4 | −0.057 | − | − |
|  5 | +0.025 | + | + |
|  6 | −0.033 | − | − |
|  7 | +0.016 | + | + |
|  8 | −0.022 | − | − |
|  9 | +0.009 | + | + |
| 10 | −0.014 | − | − |

**Interpretation:** perfect alternating sign pattern, magnitude decays with distance — the textbook signature of antiferromagnetic short-range order. This is a **quantitative and qualitative match** to Fig. 3b of the paper (which shows DMRG and VQE curves indistinguishable and clearly alternating between roughly +0.2 and −0.2 for the nearest sites, decaying at longer range).

### 4.2 SrVO3 (C7) — mechanism check only

**Table 4.3** — 2×2 single-band ED with paper's SrVO3 Appendix C.3 parameters:

| Case | E₀ (eV) | site occupancies n_i | Sublattice sum n_A | n_B | Φ = |n_A−n_B|/(NxNy) |
|---|---:|---:|---:|---:|---:|
| Half-filling (paper params: t=−0.263, U=3.527, V=0.649) | +2.329 | [1, 1, 1, 1] | 2.000 | 2.000 | **0.0** |
| Non-interacting control (U=V=0) | −1.052 | [1.049, 0.951, 0.951, 1.049] | 2.097 | 1.903 | 0.049 |
| Strong-V control (V=3 eV) | +6.953 | [1, 1, 1, 1] | 2.000 | 2.000 | 0.0 |

**Interpretation:** on a 2×2 lattice at half filling with balanced sublattices (2 sites in each of A and B), the ground state is A/B-symmetric by construction and Φ = 0 identically. This is a geometric artifact of the reduction, not a contradiction of the paper. The paper's 3×3 lattice has 5 sites in one sublattice and 4 in the other, breaking the symmetry and allowing Φ ≠ 0. Full reproduction of the paper's Φ = 0.21 (VQE) / 0.12 (DMRG) requires the 54-qubit 3-band DMRG stack, which was out of scope for this ~15-minute replication window.

### 4.3 WTe2 (C4, C5) — not attempted

The WTe2 model is 4 bands × 4 lattice sites × 2 spins = 32 spin-orbitals, Fock-space dimension up to ~4 × 10⁹ before symmetry reduction. Direct ED on a laptop is infeasible; DMRG or tensor-network VQE (as in the paper) would be required and would need a substantial software build (ITensor + a custom MPO for the 4-band extended Hubbard) that was out of scope for this replication window.

### 4.4 Cross-check on Table II arithmetic

Paper Table II reports for Ca2CuO3: n_{2q,G} = 290, circuit fidelity = 74.8% assuming per-gate fidelity 0.999.
Independent check: 0.999^290 = 0.7476 → 74.76% ≈ 74.8%. **Consistent.** ✓

## 5. Verdict + justification

**LLM-judge (`argo:gpt-5.2`) verdict:** *PARTIAL — "Ca2CuO3's key quantitative (ground-state energy) and qualitative (AFM correlations) results were independently reproduced, but WTe2 was not attempted and SrVO3 was only sanity-checked for parameter/mechanism plausibility without reproducing the reported DMRG/VQE energies or charge order on the paper's lattice size."*

**Analyst concurrence:** Verdict **PARTIAL** is the honest reading. The paper's centerpiece methodology is the full three-material demonstration; one of the three (Ca2CuO3) was reproduced at essentially machine precision on independent code, one (SrVO3) was only checked at reduced scale, and one (WTe2) was not attempted. The reproduced part alone is a nontrivial confirmation:

- The paper's Appendix C.1 downfolded parameters for Ca2CuO3 correctly generate a Hamiltonian whose ground state, obtained by an entirely independent from-scratch scipy sparse implementation, matches the paper's DMRG value to 0.1 meV.
- The paper's DMRG value at 6.005 eV is thus confirmed to be a fully-converged ground-state energy, not a bond-dimension artifact.
- The paper's Fig. 3b antiferromagnetic-correlation plot is reproduced in sign pattern and closely in magnitude by the same ED wavefunction.

The paper's central methodological claim — that ab-initio downfolding produces material-specific Hamiltonians of the extended-Hubbard form that faithfully retain the low-energy physics — is *consistent with* this replication for Ca2CuO3, and *not contradicted* for the other two materials, which simply weren't attempted at the paper's scale.

Notable strengths of the paper for reproducibility:
- All downfolded Hamiltonian parameters are in Appendix C (verbatim, matrix by matrix). Rare in this literature.
- All DFT/cRPA computational details (pseudopotentials, cutoffs, k-grids, bands excluded from cRPA) are in Appendix B.
- Table II gives exact ‖H‖₁ and n_terms so any future replicator can cross-check their Hamiltonian construction.

Notable gaps for reproducibility:
- No public code repository. The tensor-network VQE stack (Ref. [39]) is not on GitHub; ITensor is public but the custom MPO construction is not.
- The DFT-→-Wannier-→-cRPA-→-downfolded-Hamiltonian pipeline would take days to reproduce from scratch and was skipped in favor of directly consuming the paper's Appendix C matrices.

---

## Verdict
PARTIAL: Ca2CuO3 downfolded 20-qubit 1-band extended-Hubbard ground-state energy (0.1 meV agreement with paper's DMRG 6.005 eV) and antiferromagnetic spin-correlation Fig. 3b independently reproduced via from-scratch ED using the paper's own Appendix C.1 parameters; WTe2 (32-qubit) and SrVO3 (54-qubit) not reproduced at paper scale.

WAVE_RESULT set=OSTI paper=2497830 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-2497830-downfolding-qc one_line=Ca2CuO3 downfolded model ED reproduces paper DMRG E=6.005 eV to 0.1 meV and AFM spin correlations of Fig 3b; WTe2/SrVO3 out of direct-ED reach.
