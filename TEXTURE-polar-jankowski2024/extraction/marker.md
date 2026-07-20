# Extraction — marker.md

**Paper:** Polarization textures in crystal supercells with topological bands
**Authors:** W. J. Jankowski, D. Bennett, A. Agarwal, G. Chaudhary, R.-J. Slager
**Ref:** arXiv:2404.16919v2 [cond-mat.mes-hall], 28 Aug 2024
**Extraction method:** `pdftotext -layout` (interim stand-in for Marker; no GPU Marker run available in this fast-replication budget). Full dump: `work/_pdftotext_full.txt`.

## Testable headline (the ONE replicated)
Twisted-Haldanium moiré supercell hosts a **real-space polar MERON texture**
with half-integer winding **Q = ±1/2** (Eq. 12, Pontryagin/Berg-Lüscher form).
Across a **topological phase transition** (Haldane mass `t2` tuned through
`|t2|≈0.43`, trivial `|C|=0` → topological `|C|=2`):
- the **magnitude** of the local polarization **drops discontinuously**,
- but the polarization **does not vanish**, and
- the **winding Q of the texture is preserved**.

## Key equations
- Eq. 5: local polarization `P_β(r_j)` from semilocal hybrid polarizations (SHPs) / HWCC flow.
- Eq. 7–8: Chern number `C` / quantized `ΔC({r_j})` from winding of HWCCs.
- Eq. 12: `Q = (1/4π) ∫ P̂·(∂ₓP̂ × ∂_y P̂) d²x` — polar-texture winding.

## Models
- Super-Haldane model (N=51 supercell + superlattice potential VSL): polarization domain + ring, `ΔC` quantized.
- Twisted Haldanium bilayer (θ≈5°): meron textures, phase diagram in (m, t2).

## Method classification
Tight-binding / Wilson-loop theory paper (`method=theory/both`). No released code.
Full HWCC/SHP first-principles pipeline is out of scope for a fast CPU run; we
replicate the **real-space polar-topology mechanism** (Eq. 12) instead.
