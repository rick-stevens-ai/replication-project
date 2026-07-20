# Workflow — Lux et al. 2017 (arXiv:1706.06068) replication

## Pipeline
acquire (PDF present) → parse (pdftotext) → extract recipe (prepped) →
**build from-scratch physics** → run → compare → package (8 artifacts) → self-score.

## Physical system
2D noncollinear spin textures (Néel skyrmion; spin spiral for the COM branch).
Headline: at **zero spin–orbit coupling** the topological orbital magnetization
`M_tom = (1/4) χ_LP B_eff^z sgn(Δxc)(1 − 3μ²/Δxc²)` — i.e. **TOM is linear in the
scalar spin chirality** `B_eff^z = (ħ/2e) n·(∂ₓn × ∂_yn)` (Eq. 1).

## Method built
- Direct real-space diagonalization of a 2D square-lattice s–d model **with no SOC**:
  `H = −t Σ⟨ij⟩ c†c + m Σ (n·σ)`, N\'eel skyrmion texture.
- Itinerant orbital operator `L_z = ½(X v_y − Y v_x)`, `v = i[H,R]`, **center-gauged**.
- TOM = ground-state accumulated moment `Tr[P L_z P]/N_cell`, FM-subtracted.
- Scalar spin chirality: continuum finite-difference density
  `χ_c = Σ n·(∂ₓn × ∂_yn)` (varies continuously; Berg–Lüscher solid angle used as a
  quantization sanity check).
- **H1 test:** cant a fixed skyrmion collinear→full to dial χ_c; fit M_tom vs χ_c.
- **H2 test:** sweep μ across the lower band; look for the sign-changing structure.

## Tools / versions
- Physics runner: `/home/stevens/comfyui-env/bin/python` — numpy 2.3.5, scipy 1.17.0.
- Reused kernel: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (Ollie; g\"obel2024,
  arXiv:2410.00820) — `build_H`, `build_FM`, `skyrmion_field`, itinerant `L_z`.
- Extraction: `pdftotext` (poppler) — `marker`/`nougat` not installed (interim fallback).
- LaTeX: `pdflatex` not required for delivery (REPORT.tex shipped as source).

## Key parameters (coarse run)
`t=1, m=3.0, L=24, kind=neel, filling=0.06, α_R=0 (no SOC)`.
H1 canting η ∈ {0.15…1.0} at λ=3; H2 μ-grid of 11 points across the lower band.

## Effort estimate
- Physics build + debug (chirality had to switch from quantized Berg–Lüscher to
  continuous continuum-density estimator): ~1.5 h.
- Run: ~18 s wall.
- Packaging (8 artifacts): ~0.7 h.

## Reproduce
```bash
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-orbital-lux2017/work/lux2017_tom.py
# writes work/lux2017_result.json ; runtime ~18 s
```
