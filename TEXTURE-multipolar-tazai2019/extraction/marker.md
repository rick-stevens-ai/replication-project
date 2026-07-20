# Extraction — arXiv:1901.06213 (Tazai & Kontani 2019)

**Title:** Multipole fluctuation theory for heavy fermion systems: Application to multipole orders in CeB6
**Authors:** Rina Tazai, Hiroshi Kontani (Nagoya University)
**Dated:** 21 Jan 2019 (PRL-format letter + Supplemental Material)
**Source text:** `pdftotext -layout paper.pdf` → `extraction/paper.txt` (644 lines)

## Central claim
A 2D multiorbital periodic Anderson model (PAM) for CeB6 with a Γ8 quartet f-orbital basis.
- Within **RPA**: only odd-rank (magnetic) multipole fluctuations develop; χ_Jz is largest, with peaks
  at q≈0 (FM) and q≈Q=(π,π) (AFM). Even-rank (quadrupole) fluctuations stay small because the
  normalized Coulomb interaction U0Q for quadrupole channels is smaller than for dipole/octupole.
- Adding **Aslamazov–Larkin (AL) vertex corrections** strongly enhances the Oxy quadrupole
  susceptibility (χ_Oxy becomes the largest of all χ_Q at q=Q and q=0), driven by interference
  between (Tx,Ty) magnetic-multipole fluctuations. → explains antiferro-quadrupole order in CeB6.
- Field-induced octupole (Txyz) order under h_z explained via Γ4 = {Oxy, Txyz} mixing.

## MODEL (Supplemental Material A)
### Conduction band dispersion (Eq. S1), 2D, kz=0:
ε_k = t1(cos kx + cos ky)
    + t2[cos(kx+ky) + cos(kx−ky)]
    + t3(cos 2kx + cos 2ky)
    + t4[cos(2kx+ky)+cos(2kx−ky)+cos(2ky+kx)+cos(2ky−kx)]
    + t5[cos(2kx+2ky)+cos(2kx−2ky)]
    + E0
with (t1,t2,t3,t4,t5) = (−0.5, −0.889, 0.292, −0.229, 0.687), E0 = 1.33.

### s-f hybridization (Eq. S2 / main Eq. 2):
V_{k,f1,↑} = −A1 tsf (sin ky − i sin kx)
V_{k,f2,↑} = −A2 tsf (sin ky + i sin kx)   [main text sign convention: (sin ky + (−1)^l i sin kx)]
V_{k,fl,↓} = −(V_{k,fl,↑})*
A1 = A2 = sqrt(18/14) (set equal to avoid 2D artifact), tsf = 0.78.

### Energy unit & filling:
2|t1_ss| = 1 as energy unit. Ef = −2.0, T = 0.01, μ = −2.45.
→ nf = 0.58, ns = 0.69 (f- and s-electron numbers). [MACHINE-CHECKABLE]

### Kinetic term:
H0 = Σ ε_k c†c + Ef Σ f†f + Σ V f†c + h.c.
Green's function without self-energy Ĝf (bare bubble).

## MULTIPOLE OPERATORS (SM B, Eqs. S5–S6) — 4×4 matrices in σ⊗τ (pseudospin ⊗ orbital)
Electric (even rank):
  Γ1+: 1̂ = σ0 τ0
  Γ3+: O20 = 4.0 σ0 τz ;  O22 = 4.0 σ0 τx
  Γ4+: Oxy = −σz τy
  Γ5+: Oyz = −σx τy ; Ozx = −σy τy
Magnetic (odd rank):
  Γ2−: Jz = σz(−1.2 τ0 − 0.67 τz) ; Tzα = σz(−1.0 τ0 − 7.0 τz)
  Γ3−: Txyz = −10.0 σ0 τy
  Γ4−: Tzβ = −6.7 σz τx
  Γ5−: Jx = σx(1.2τ0 −0.34τz +0.58τx) ; Jy = σy(1.2τ0 −0.34τz −0.58τx)
       Txα = σx(τ0 −3.5τz +6.1τx) ; Tyα = σy(τ0 +3.5τz +6.1τx)
       Txβ = σx(−5.8τz −3.4τx) ; Tyβ = σy(−5.8τz +3.4τx)
Normalization (S7): Q̂/sqrt(Σ|Q_LM|²) → Q̂, so Σ|Q_LM|²=1.

## SUSCEPTIBILITY FORMALISM
Bare bubble (16×16 matrix, α=(L,L'), β=(M,M')):
  χ0_{α,β}(q) = −T Σ_k G^f_{LM}(k+q) G^f_{M'L'}(k)   [static ω=0 used for Stoner]
RPA:  χ̂(q) = φ̂(q)(1̂ − u Û0 φ̂(q))⁻¹ ,  φ̂ = χ̂0 + X̂^{AL+MT}
RPA-only: X^{AL+MT}=0 → χ̂ = χ̂0 (1 − u Û0 χ̂0)⁻¹.
Multipole susceptibility: χ_{Q,Q'}(q) = (Q⃗)† χ̂(q) Q⃗, with (Q⃗)_α = (Q̂)_{L,L'}.
Eigen equation (Stoner): u Û0 φ̂(q,0) w⃗ = α^Γ(q) w⃗ ; order when α^Γ≥1.
α_mag = max over magnetic IRs, α_el = max over electric IRs.

## Û0 (normalized Coulomb), TABLE II diagonal U0Q [MACHINE-CHECKABLE targets]
Q:      1     O20/22  Oxy/yz/zx  Txyz   Jz(x,y)  Tzα(x,y)  Tzβ(x,y)
U0Q:  −2.4    0.50    0.63       0.81   1.03     0.94      0.94
Off-diagonal U0^{Q,Q'}=0 except U0^{Jμ,Tμα}=0.58 (μ=x,y,z).
(Note: paper's TABLE II header groups quadrupole as Oxy(yz,zx)=0.63, O20(22)=0.50.)

## KEY NUMERICAL RESULTS (targets)
- RPA at u=1.08 gives α_mag=0.9; χ_Jz is largest; χ_Jz(q,0) peaks at q≈0 and q≈Q=(π,π). [Fig 2]
- With VCs: α^{Γ4}_Oxy = 0.94; χ_Oxy(q,0) becomes largest, peak at q=Q, 2nd peak q=0. [Fig 3]
- Field: Z^Txyz grows ~linearly in hz; α^Γ4 increases with hz. [Fig 5]
- Scaling: X^AL ∼ ξ² , X^MT ∼ log ξ in 2D → AL dominates for ξ≫1. AL ∝ max{ξ^{4−d},1}. [S10]

## SCOPE
- FULLY TRACTABLE (implement): band structure & Fermi surface (Fig 1), filling nf/ns, multipole
  operator matrices & normalization, Û0 diagonal structure conceptually, RPA bare bubble χ0,
  RPA multipole susceptibilities χ_Q(q,0), demonstration that magnetic (Jz) dominates in RPA and
  quadrupole stays small (the paper's core RPA claim). Stoner eigenvalues.
- HARD / OUT-OF-SCOPE for overnight: full AL/MT vertex-correction 2-loop momentum integrals
  (Eqs 7,8,11,S8,S9) — 16×16 three-point vertices Λ with double k,p sums; the actual χ_Oxy
  enhancement number 0.94 requires the full VC machinery. We implement RPA rigorously and treat
  the AL enhancement qualitatively/structurally + the analytic ξ-scaling (S10) as a check.
- Û0 full 16×16 tensor requires Slater–Condon F^k integrals + Γ8 Clebsch machinery from Ref [2];
  we reconstruct the DIAGONAL U0Q structure from the reported values and test the RPA consequence.
