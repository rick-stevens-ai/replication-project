# Artifact Harvest

| Artifact | Source | Size | Notes |
|---|---|---|---|
| OSTI OA PDF (3374709.pdf) | https://www.osti.gov/servlets/purl/3374709 | 3.90 MB | PDF v1.4; fetched via `ssh uicgpu` proxy (CherryRd times out on osti.gov). eScholarship perma: escholarship.org/uc/item/8xt682g7 |
| 3374709.txt | `pdftotext` on the OA PDF | 13,891 words | Full extracted text; used to pull Eqs. 5–18 and Table I parameters |

## Extracted key equations (verbatim from text)
- **Eq. 9-10 (SIPIC field operator):** `[L_ii' + (C_SI·Δt²·qp²/(4·eps0·mp))·∇Si·∇Si'] φ_i' = Q_i/eps0`, reducing (barycentric shape fns) to Laplacian multiplied by `(1 + C_SI·ωpe²·Δt²/4)`.
- **Eq. 12 (paper's kappa):** `κ = 1/(1 + C_SI·ωpe²·Δt²/4)`, with `eps_SI = eps0·κ` (Eq. 11) and `ω² = ωp²/κ` (Eq. 13).
- **Eq. 16 (stated result — the down-shift):** `ωpr_SI = √(nr·Zr²·e²/(mr·eps_SI))`, i.e. plasma mode reduced by factor `1/√(1 + C_SI·ωpe²·Δt²/4)`.
- **Eq. 17/18 (Bohm–Gross, physical & SIPIC-modified):** `ω² = ωpe² + (3/2)vth²k²` → `ω² = (ωpe_SI)² + (3/2)vth²k²`.

## Table I (plasma dispersion problem)
- Plasma density n = 1e10 m⁻³ (`10^r`); Te = 20 eV; Ti = 5 eV
- Δx = a·λ_De ; **C_SI = 4** ; Ncell = 1024/a ; Nppc = 500a ; ion mass = 250 mₑ
- Numerical factor **a ∈ {0.5, 1, 2, 4, 8}**
- (Convention note: Table I lists `Δt = 2a/ωpe` i.e. ωpe·Δt = 2a, while Sec. III.A prose
  states `Δt·ωpe = a/2`. These are mutually inconsistent in the paper. The Eq. 16
  down-shift depends only on the product `ωpe·Δt`, so the replication sweeps a full 16×
  range of that product to cover both conventions.)

## No proprietary data / no external code used
- The paper's numbers were produced by WarpX + Aleph (both open, but not required here).
  This replication re-derives the analytic verification target from the paper's equations
  and reproduces it with a self-contained ~180-line NumPy PIC. No proprietary data needed.
