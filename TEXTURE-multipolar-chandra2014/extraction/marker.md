# Extraction — arXiv:1404.5920

**Title:** Ising Quasiparticles and Hidden Order in URu2Si2
**Authors:** Premala Chandra (Rutgers), Piers Coleman (Rutgers / Royal Holloway), Rebecca Flint (Iowa State)
**Venue:** Philosophical Magazine (review/perspective on hastatic order), arXiv:1404.5920v1 [cond-mat.str-el], 23 Apr 2014.

> Extraction note: the `pdf` vision tool was unavailable (Anthropic credit + disabled plugins), so
> body text was extracted with `pdftotext -layout`. Equations below transcribed from that text dump
> and cross-checked against the surrounding prose.

## What the paper is
A perspective/review arguing that the hidden-order (HO) phase of URu2Si2 (T_HO = 17.5 K) is best
explained by **hastatic order** — a spinorial (half-integer spin, double-group) order parameter that
is the "square root of a multipole." The "multipolar texture / multipolar order" is the *competing*
class of theories (staggered charge/spin multipole density waves) that the authors contrast against.
Central experimental driver: heavy **Ising quasiparticles** in the HO state (near-perfect g-factor
anisotropy), probed by de Haas–van Alphen (dHvA) spin-zeros and upper-critical-field H_c2(θ).

## Central physical claims
1. Heavy quasiparticles in the HO phase are Ising: g(θ) = g* cos θ, isotropic-part suppressed.
2. dHvA "spin zeros" occur when Zeeman/cyclotron ratio hits half-integers → 16 spin zeros observed.
3. Ising anisotropy implies Pauli-susceptibility anisotropy χ_P^c/χ_P^⊥ > 900.
4. A tight bound on the non-Kramers doublet splitting: Δ < ½ ħω_c ⇒ Δ < 0.67 K (α orbit, m*=13 m_e, B=13 T).
5. Landau theory with spinorial OP Ψ gives an HO↔AFM spin-flop transition; the longitudinal spin-fluctuation
   gap softens as Δ_gap ∝ |Ψ0| √(Pc − P) ∝ √(T − Tc).
6. Predicted giant nonlinear-susceptibility anisotropy χ3 ∝ cos⁴θ.
7. Order-parameter fractionalization: 3-body Hubbard operator → integer-spin fermion × half-integer-spin boson.

## Key equations (transcribed)
- (1) Zeeman-split Landau levels: E_n± = (n+γ) ħω_c ∓ ½ g μ_B B.
- (2) Effective mass: m* = (ħ²/2π) ∂A/∂ε.
- (4)-(5) dHvA magnetization: M ∝ Σ_± sin(2π μ_±/ħω_c) = 2 sin(2πμ/ħω_c) cos δ.
- (6) Zeeman phase shift: δ = 2π (g μ_B B / ħω_c)(... ) = π (m*/m_e) g/2  [δ field-independent].
- (7) Spin-zero condition: α_n = 2π (Zeeman/cyclotron) = g(θ_n) m*/(2 m_e) = n + ½.
- (8) g-anisotropy bound: g_⊥/g_c < 1/30.
- (9) Ising g-factor angular law: g(θ_n) = g* cos θ_n, with g* = 2.6.
- (10) Pauli susceptibility anisotropy: χ_P(θ) = χ_P^c cos²θ, χ_P^c/χ_P^⊥ > 900.
- (11) Splitting bound: Δ < ½ ħω_c.
- (12) Numeric bound: Δ < (ħ e B)/(k_B e · 2(m*/m_e) m_e) = 0.67 K  (B=13 T, m*=13 m_e).
- (13) Ising doublet: |Γ±> = Σ_n a_n |±(J_z − 4n)>  (4ħ steps from tetragonal C4).
- (14) Ising selection rule: <Γ±|J±|Γ∓> = 0 ⇒ requires integer J_z (non-Kramers).
- (15) Γ5 non-Kramers doublet: |Γ5±> = α|J_z=±3> + β|J_z=∓1>.
- (16) Hastatic spinor OP: Ψ = (ψ↑, ψ↓)^T.
- (17) Landau free energy: f[Ψ] = α(Tc−T)|Ψ|² + β|Ψ|⁴ − γ(Ψ†σ_z Ψ)², with γ = δ(P−Pc).
- (18) AFM (P>Pc): Ψ_A ∝ (1,0), Ψ_B ∝ (0,1) — c-axis Ising, staggered.
- (19) HO (P<Pc): Ψ_A ∝ (e^{-iφ/2}, e^{iφ/2})/√2, Ψ_B ∝ (−e^{-iφ/2}, e^{iφ/2})/√2 — basal plane.
- Soft mode: Δ_gap ∝ |Ψ0| √(Pc−P); near Tc, √(Pc−P) ≈ (dPc/dTc)(T−Tc) ⇒ Δ_gap ∝ √(T−Tc).
- (20)-(24) two-channel Anderson lattice, valence-fluctuation Hamiltonian, hybridization form factors.
- (25)-(31) fractionalization / three-body contraction.

## Quantitative anchors (extractable numbers)
- T_HO = 17.5 K; ordering entropy S > (1/3) R ln 2 (text also "N S ~ ½ k_B ln2" Majorana entropy).
- g* = 2.6 (vs free-electron 2). Onsager index for α orbit: g* m*/(2 m_e) = n+½.
- m* = 13 m_e on α orbit; measured at B = 13 T.
- g_⊥/g_c < 1/30; χ_P^c/χ_P^⊥ > 900.
- Δ < 0.67 K; also Δ << 10 K (two-channel Kondo TK≈10K in Th-diluted x=0.07).
- 16 spin zeros observed (contrast: 1/band in cuprates).
- basal-plane moment predicted ~0.01 μ_B (20% mixed valence); experimental bound µ_⊥ < 0.0011 μ_B;
  other probes see static ~0.005 μ_B.
- Bulk susceptibility Ising anisotropy ≈ factor 5; Pauli-surface anisotropy > 900.
- Q = (0,0,2π/c) commensurate wavevector shared by HO and AFM.

## Chosen machine-checkable claims (for replication)
C1. **Spin-zero indexing (Eq. 7 + 9):** with g(θ)=g* cosθ and m*=13 m_e, the set of angles θ_n solving
    g* cosθ_n · m*/(2 m_e) = n+½ reproduces a discrete ladder of spin zeros; count reachable zeros and
    check g* ≈ 2.6 is what makes the c-axis Onsager index α_0 = g* m*/(2 m_e) land near a half-integer.
C2. **Δ bound (Eq. 11-12):** Δ < ½ħω_c with ω_c = eB/m*, m*=13 m_e, B=13 T ⇒ Δ < 0.67 K. Recompute in K.
C3. **dHvA spin-zero from destructive interference (Eq. 4-7):** M ∝ 2 sin(2πμ/ħω_c) cos δ with
    δ = π (m*/m_e)(g/2); show |M| envelope → 0 (cos δ = 0) exactly when δ = (n+½)π, i.e. the α_n=n+½ ladder.
C4. **Landau spin-flop + √ gap (Eq. 17-19 + soft mode):** minimize f[Ψ]; show γ sign flips OP direction
    between basal-plane (HO) and c-axis (AFM) across Pc, and the longitudinal-mode gap ∝ √(Pc−P).
C5. **χ3 ∝ cos⁴θ (Ising nonlinear susceptibility):** derive/confirm the cos⁴θ angular law from the
    Ising doublet coupling to Bz = B cosθ (χ3 anisotropy prediction).
