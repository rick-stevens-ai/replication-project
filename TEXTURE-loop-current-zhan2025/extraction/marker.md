# Extraction marker — Zhan et al., "Loop Current Order on the Kagome Lattice"

- **arXiv:** 2506.01648v2 [cond-mat.str-el], 27 Mar 2026
- **Authors:** Jun Zhan, Hendrik Hohmann, Matteo Dürrnagel, Ruiqing Fu, Sen Zhou, Ziqiang Wang, Ronny Thomale, Xianxin Wu, Jiangping Hu
- **Extraction method:** `pdftotext -layout paper.pdf paper.txt` (1739 lines). Full text read directly (no vision/credit needed).

## Central claims
1. **Spinless kagome model at p-type Van Hove filling (µ=0)** with nonlocal density-density repulsion (V1 nn, V2 2nn). Onsite interaction absent (fermionic antisymmetry). Hamiltonian Eq.(1):
   H = −t Σ⟨ij⟩(c†_i c_j + h.c.) − µ Σ n_i + V1 Σ⟨ij⟩ n_i n_j + V2 Σ⟨⟨ij⟩⟩ n_i n_j.
2. **Sublattice interference (SI)** at the p-type VHS suppresses onsite CDW; leaves LCO, charge bond order (CBO), nematic CDW (nCDW) as main competitors.
3. **Unbiased FRG** (functional renormalization group) over all channels yields a phase diagram (Fig 2) in (V1,V2): nCDW (weak V2), **LCO (intermediate V2, strong V2 relative to V1)**, f-wave SC (strong V2), CBO (V1-dominant).
4. **2×2 (3Q) LCO** emerges as many-body ground state over a significant parameter region with strong V2. TRS-breaking.
5. **Landau free energy** (Eq.2): f⁽⁴⁾ = ½Z1|Δ|⁴ + (Z2−Z1)(Δ₁²Δ₂²+Δ₂²Δ₃²+Δ₃²Δ₁²) with Z1−Z2>0. Trilinear term vanishes by TRS breaking → favors equal-weight 3Q → enlarged 2×2 pattern. (Contrast: CBO has a nonzero trilinear term.)
6. **Electronic model with LCO** (tight-binding + imaginary bond order on 1nn & 2nn bonds) gaps the FS → **Chern insulator, quantum anomalous Hall, total Chern number C=1** (Fig 3(d), with ΔLCO_1nn=0.1t, ΔLCO_2nn=0.15t). Analogous to the Haldane model.
7. FeGe: 2×2 LCO can generate orbital magnetic moment ~0.03 µB/site.

## Machine-checkable subset (what this replication targets)
The FRG many-body flow (claims 2–4) requires a full FRG code and HPC (NHR@FAU) — NOT reproducible cheaply, and OUT OF SCOPE for a tight-binding kernel. We instead replicate the **downstream single-particle electronic-model consequences**, which are the paper's concrete falsifiable outputs:
- Claim A: bare kagome dispersion features — flat band, Dirac cone at K, VHS saddle at M, and p-type VHS at µ=0.
- Claim B: adding imaginary (loop-current) bond order to the tight-binding model **opens a full gap** at the Fermi level (Fig 3(d)).
- Claim C: the gapped LCO state is a **Chern insulator with total C=1** (Fig 3(d): "filled bands feature a total Chern number of C=1").
- Claim D: Landau quartic (Eq.2) with Z1−Z2>0 selects the **equal-weight 3Q** state over 1Q/2Q (energetics of Fig 3 discussion).
- Claim E: the LCO/imaginary-bond state breaks TRS (nonzero bond currents / plaquette flux), while the real-bond (CBO) analog does not.
