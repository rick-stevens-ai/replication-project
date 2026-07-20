# Extraction (marker interim) — Li, Wang & Chen (2016)

> **Method note:** `marker` / `marker-pdf` was not available in this bounded-budget
> environment. This file is an **interim extraction** produced with `pdftotext -layout`
> as a faithful stand-in. The full raw dump is at `extraction/_raw.txt` (77,992 chars,
> 858 lines). Header + key structural content reproduced below.

---

## Paper metadata

- **Title:** Hidden multipolar orders of dipole-octupole doublets on a triangular lattice
- **Authors:** Yao-Dong Li, Xiaoqun Wang, Gang Chen
- **arXiv:** 1608.07008v1 [cond-mat.str-el], 25 Aug 2016
- **Affiliations:** Fudan University; Shanghai Jiao Tong University; Perimeter Institute

## Abstract (extracted)

Motivated by strong spin-orbit-coupled materials, the authors consider dipole-octupole
(DO) doublets on the triangular lattice, propose the most general nearest-neighbor
interaction between these local moments, and analyze the ground-state properties.
They emphasize *hidden* multipolar orders emerging from dipolar and octupolar
interactions, clarify the quantum mutual modulation between dipolar and octupolar
orders, and propose rare-earth triangular materials as candidates.

## Key model equations (extracted)

**Original model (Eq. 3):**
```
H0 = sum_<rr'> [ Jx τx τx' + Jy τy τy' + Jz τz τz' + Jyz(τy τz' + τz τy') ]
```

**Reduced model after θ-rotation about pseudospin-x (Eq. 4):**
```
H = sum_<rr'> [ Jx Tx Tx' + Jy Ty Ty' + Jz Tz Tz' ] - h sum_r [ cos θ Tz + sin θ Ty ]
   Tx = τx (OCTUPOLE),  Ty = τz sinθ + τy cosθ,  Tz = τz cosθ - τy sinθ  (both DIPOLES)
```

**Octupolar-wave dispersion (Eq. 5):**
```
ω_k = sqrt( [Jy Σ_i cos(k·a_i) - 3Jx] · [Jz Σ_i cos(k·a_i) - 3Jx] )
   a1=(1,0), a2=(-1/2, √3/2), a3=(-1/2, -√3/2)
```

## Key numerical claims (extracted, Fig. 1)

- **(b)** FDz state on Iz surface: (Jx,Jy,Jz)=(-0.5,-0.2,-1), θ=π/3, transition Td = 1.5|Jz|.
- **(c)** FO state on Ix surface: (Jx,Jy,Jz)=(-1,-0.2,-0.5), θ=π/3, transition To = 1.5|Jx|;
  susceptibility χzz shows **no divergence** despite time-reversal-breaking octupolar order.
- **(d)** Octupolar-wave excitation, same params as (c), generically **gapped**.

## Structural sections

1. Introduction (SOC + correlations; hidden order; candidate materials MgYbGaO4, RCd3P3 family, R2O2CO3)
2. Dipole-octupole doublet (Γ5+/Γ6+ 1D irreps of D3d; Jz=3n/2 wavefunctions)
3. Generic pseudospin model on triangular lattice (symmetry-allowed Eq. 3)
4. Hidden ferro-octupolar orders (FDz/FDy/FO; χzz non-divergence; octupolar wave)
5. Hidden antiferro-octupolar orders (Ox surface; 3-sublattice self-consistent MF, Eq. 6; supersolid)
6. Experimental consequences & discussion

*(See `extraction/nougat.mmd` for the equation-focused mmd rendering and `extraction/_raw.txt` for the complete text.)*
