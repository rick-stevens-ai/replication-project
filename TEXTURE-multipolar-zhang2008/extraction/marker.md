# Extraction Marker — arXiv:0805.3922

## ⚠️ Task-label / paper mismatch (flagged, not fabricated)
The task directory is named `TEXTURE-multipolar-zhang2008` and the task text says
"multipolar texture." **The actual PDF (`paper.pdf`, arXiv:0805.3922v2) is a
different paper:**

> **"Magnetic field induced incommensurate resonance in cuprate superconductors"**
> Jingge Zhang, Li Cheng, Huaiming Guo, Shiping Feng.
> arXiv:0805.3922v2 [cond-mat.supr-con], 1 Sep 2008. PACS 74.25.Ha, 74.25.Nf, 74.20.Mn.

There is **no "multipolar texture"** content in this paper. It concerns the
dynamical spin response of cuprate superconductors under a uniform external
(Zeeman) magnetic field, via the kinetic-energy-driven SC mechanism in the t-J
model + charge-spin-separation (CSS) fermion-spin theory. The replication below
targets the paper that is actually present.

## Source
- `paper.pdf` (470,961 bytes) → `paper.txt` via `pdftotext -layout` (648 lines).
- No vision/PDF-credit tools needed; text layer clean.

## Central claims (as written)
1. **Zeeman branch splitting (Eq. 4):** the MF spin excitation splits into two
   branches ω_k^(1)=ω_k+2ε_B and ω_k^(2)=ω_k−2ε_B, with ε_B=gμ_B B.
2. **Dynamical structure factor (Eq. 8):** S(k,ω) has a resonance-denominator
   form in which the incoming-neutron energy enters as (ω−2ε_B).
3. **Resonance condition (Eq. 9):** peaks occur where
   W(k_c,ω)=[(ω−2ε_B)²−ω_k²−B_k ReΣ]²≈0.
4. **Field-induced commensurate→incommensurate resonance:** at B=0 the resonance
   is commensurate (at Q=[π,π]); for B large enough it splits into IC peaks with
   incommensurability δr that increases with B (Fig. 3).
5. **Two critical fields:** B_c1≈4 T (ε_B1≈0.002J) and B_c2≈10 T (ε_B2≈0.005J).
   For B>B_c2 the field is strong enough to induce IC resonance; for
   B_c1<B<B_c2 the commensurate peak only broadens.
6. **Energy selectivity / hourglass breakdown:** high-energy IC scattering
   (ω~0.7J) is robust; low/intermediate energies are strongly affected; the
   hourglass dispersion breaks down for ω<0.16J≈19 meV.

## Published parameters
- t/J = 2.5, t'/t = 0.3, J ≈ 120 meV, doping x = 0.15, T = 0.002J.
- Field↔energy: ε_B=0.01J=1.2 meV ↔ B≈20 T; 0.002J=0.24 meV ↔ 4 T;
  0.005J=0.6 meV ↔ 10 T.

## Method (full, in paper — mostly OUT OF SCOPE for minimal replication)
- t-J model + Zeeman term (Eq. 1); CSS fermion-spin decoupling C_i↑=h†_i↑ S_i⁻ etc.
- Full spin Green's function D(k,ω)=1/[D⁰⁻¹−Σ^(s)] (Eq. 3), MF D⁰ (Eq. 4).
- Spin self-energy Σ^(s) = charge-carrier bubble in the particle-particle
  channel (Eq. 6): a **double momentum sum** over p,q with d-wave gap
  Δ̄_hZ(k)=Z_hF Δ̄_h γ_k^(d), coherence weight Z_hF, and self-consistent gap
  equations (Eqs. 7a,7b). No adjustable parameters (self-consistent).

## Replication scope decision
Reproducing the self-consistent order parameters (Z_hF, Δ̄_h, α, μ, χ's) and the
double-sum Σ^(s) is a large numerical program (heavy, iterative). **Out of scope**
for a minimal analytic replication. We instead test the falsifiable *mechanism*
encoded in Eqs. (4), (8), (9): Zeeman branch splitting, the (ω−2ε_B) shift,
field-driven commensurate→IC resonance splitting, the critical-field scale, the
energy-selectivity/hourglass-breakdown scaling, and the internal consistency of
the ε_B↔B (g-factor) mapping.
