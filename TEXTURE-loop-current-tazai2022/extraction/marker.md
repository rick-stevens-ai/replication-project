# Extraction marker — arXiv:2207.08068 (Tazai, Yamakawa, Kontani)

**Title:** Charge-loop current order and Z3 nematicity mediated by bond order fluctuations in kagome metals
**Authors:** Rina Tazai (YITP Kyoto), Youichi Yamakawa, Hiroshi Kontani (Nagoya)
**Version/date:** arXiv:2207.08068v4 [cond-mat.str-el], dated May 19 2025 (v1 July 2022)
**System:** kagome metal AV3Sb5 (A = K, Rb, Cs), single-d-orbital (b3g) tight-binding, 3 sublattices A/B/C.

## Central claim
Charge loop-current (cLC) order in kagome metals is **mediated by bond-order (BO) fluctuations**.
BO fluctuations (from Coulomb + e-ph) drive an odd-parity, TRSB particle-hole condensation:
an **imaginary** hopping modulation δt^c_ij = -δt^c_ji (pure imaginary when Hermitian) = a
spontaneous loop-current (flux) order. Coexisting 3Q BO + cLC produces Z3 nematicity and a
**giant anomalous Hall effect (AHE)**.

## Method (paper)
- Kagome TB model, t = -0.5 eV (bandwidth), t' = -0.08 eV (FS shape; results insensitive to t').
- Van Hove filling n = n_vHS; FS near vHS at k = kA, kB, kC (M points).
- BO operator with form factor g_q^{lm}(k); effective BO interaction Ĥint = -(1/N)Σ (v/2) Ô_q Ô_{-q}.
- BO susceptibility χ_g(q) = χ0_g(q)/(1 - v χ0_g(q)); Stoner factor α_BO = max v χ0_g(q); peaks at q = qn (n=1,2,3).
- cLC via **linearized DW (density-wave) equation** (Eliashberg-like): λ_q f_q^L(k) = (T/N) Σ I_q^{L,M}(k,p) {-G(p)G(p+q)} f_q^M(p); I ∝ -χ_g(k-p) (Maki-Thompson single-exchange).
- cLC transition when max_q λ_q = 1; solution is odd-parity f_q^{lm}(k-q/2) = -f_q^{ml}(-k-q/2).
- 60x60 k-mesh, T ~ 0.01, self-consistent χ_g and self-energy Σ.
- AHE: Kubo σ_μν = (1/N)Σ_k A_μν(k), intrinsic Fermi-surface Hall conductivity in 12x12 (3Q BO+cLC) folded model.

## Key numbers extracted
- t = -0.5 eV, t' = -0.08 eV.
- v = 0.7, T = 0.012 for Fig 3b eigenvalue/Stoner plot.
- α_BO* = 0.985 defines TBO.
- v* ≈ 1.03 (y=1) or v* ≈ 0.55 (y=0.5) where TcLC = TBO.
- Weak coupling (v < v*): TcLC > TBO (cLC primary). Strong coupling (v > v*): TcLC < TBO (BO+cLC nematic).
- |δt^b| = |δt^c| = 0.025; gap Δ ≈ 2√(|δt^b|²+|δt^c|²) ≈ 0.07.
- σ_H ~ 1 in units e²/ℏ (=2.4e-4 Ω⁻¹) → ~4e3 Ω⁻¹cm⁻¹ (0.6nm interlayer) → giant AHE σ_H ~ 10² Ω⁻¹cm⁻¹.
- σ_H ∝ |δt^c_ij| when γ ≪ Δ; σ_H ∝ γ⁻² when γ ≫ Δ (universal intrinsic-Hall crossover).

## Figures of merit
- Fig 3d: cLC pattern — clockwise/anticlockwise loop currents on hexagons AND triangles.
- Fig 4d/e: TcLC, TBO vs v phase diagram.
- Fig 4f: schematic phase diagram (3Q-BO C6 → BO+cLC C2 nematic → cLC).
- Fig 6a: σxy - σyx (Hall) vs damping γ.

## Extraction method
`pdftotext -layout paper.pdf paper.txt` (pdf/vision path used layout mode; a couple of embedded-image
operator warnings, text body extracted cleanly). No vision credits used.
