# Extraction — marker.md

**Paper:** Intertwined van-Hove Singularities as a Mechanism for Loop Current Order in Kagome Metals
**Authors:** Heqiu Li, Yong Baek Kim, Hae-Young Kee (University of Toronto / KIAS / CIFAR)
**Ref:** arXiv:2309.03288v2 [cond-mat.str-el], 2 Apr 2024
**Extraction method:** `pdftotext -layout` (interim; Marker/Nougat GPU pipeline not run in this CPU replication sandbox).

> **NOTE ON EXTRACTION PROVENANCE.** This `marker.md` is an *interim* extraction
> produced with `pdftotext -layout` (Poppler) plus this curated header, not the
> full Marker deep-learning layout model. The verbatim body text is available in
> `work/textures-loop-current-li2023.txt` and `extraction/_pdftotext.txt`. The
> companion `nougat.mmd` similarly carries a header + the pdftotext body as an
> honest stand-in for a Nougat GPU run. No text was fabricated; equations below
> are transcribed from the paper body.

## Abstract (verbatim)

Recent experiments on kagome metals AV₃Sb₅ (A=Cs,Rb,K) indicated spontaneous
time-reversal symmetry breaking in the charge density wave state in the absence
of static magnetization. The loop current order (LCO) is proposed as its cause,
but a microscopic model explaining the emergence of LCO through electronic
correlations has not been firmly established. We show that the coupling between
van-Hove singularities (vHS) with distinct mirror symmetries is a key ingredient
to generate LCO ground state. By constructing an effective model, we find that
when multiple vHS with opposite mirror eigenvalues are close in energy, the
nearest-neighbor electron repulsion favors a ground state with coexisting LCO and
charge bond order. It is then demonstrated that this mechanism applies to the
kagome metals AV₃Sb₅.

## Key physical content

- **System:** AV₃Sb₅ kagome metals, 2×2 CDW, TRSB without static magnetism.
- **Order parameter:** Δ_αβ (α,β=A,B,C sublattices), Δ_AB=Δ_BC=Δ_CA≡Δ (complex).
  Re Δ = charge bond order (CBO); Im Δ = loop current order (LCO); complex Δ = LCBO.
- **Mechanism:** two van-Hove singularities vH1, vH2 with **opposite mirror (m′)
  eigenvalues** but same m″, close in energy near the Fermi level. Their coupling
  (parameter λ, linear in k at the same M point) selects LCBO.
- **Mirror-fixed wavefunction weights (Fig.1c):** vH2 at M_C = (b, −b, 0);
  vH1 at M_C = (0, 0, b′). Symmetry coefficients s₁ = −2|b′|², s₂ = 2|b|².

## Central equations (transcribed)

**Eq.(2) — 6×6 effective patch Hamiltonian** in basis
{u1(MA),u1(MB),u1(MC),u2(MA),u2(MB),u2(MC)}:

```
        [ e1    s1 D   s1 D*  | l* k1   0      0    ]
        [ s1 D* e1     s1 D   |  0    l* k2    0    ]
        [ s1 D  s1 D*  e1     |  0     0     l* k3  ]
H_eff = [ ---------------------+-------------------- ]
        [ l k1   0      0     | e2    s2 D*  s2 D   ]
        [  0    l k2     0    | s2 D  e2     s2 D*  ]
        [  0     0     l k3   | s2 D* s2 D   e2     ]
```
with k₁ = −kx/2 + (√3/2)ky, k₂ = −kx/2 − (√3/2)ky, k₃ = kx.

**Eq.(3) — eigenvalues at the CBO⁻/LCBO minima (k=0):**
E₁ = ε₂−μ−4|b|²|Δ|, E₂=E₃ = ε₁−μ−2|b′|²|Δ|,
E₄=E₅ = ε₂−μ+2|b|²|Δ|, E₆ = ε₁−μ+4|b′|²|Δ|.

**Eq.(4) — headline free-energy difference density:**
```
f_CBO⁻ − f_LCBO
  = |λ|² k_cut⁴ |Δ| (|b|²+|b′|²)
    / [16π (2|Δ|(|b|²+|b′|²)+δε)(4|Δ|(|b|²+|b′|²)−δε)]  > 0
```
LCBO favored when **δε < 4(|b|²+|b′|²)|Δ|**.

**Eq.(6) — NN interaction mean-field decoupling** yields the Δ_αβ(1−e^{ik·d})
coupling plus the constant +2N_c|Δ_αβ|²/V.

## Figure-4 parameters (used in replication)

ε₁ = 6.16 eV, ε₂ = 6.40 eV, b = 0.52, b′ = 0.96, λk_cut = 0.1 eV, T = 90 K,
λ = 0.35 eV·a (a = 5.48 Å).
