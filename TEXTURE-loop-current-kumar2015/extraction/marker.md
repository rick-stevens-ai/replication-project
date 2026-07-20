# Extraction — Kumar, Sun & Fradkin (2015)

**Paper:** Chiral spin liquids on the kagome lattice
**Authors:** Krishna Kumar, Kai Sun, Eduardo Fradkin
**Ref:** Phys. Rev. B 92, 094433 (2015); arXiv:1507.01278v3 [cond-mat.str-el]

## Extraction provenance
- Interim extraction via `pdftotext` (poppler) on
  `textures-loop-current-kumar2015.pdf` → `work/textures-loop-current-kumar2015.txt`.
- This `marker.md` is the marker-style structured interim; body text is the
  pdftotext output preserved in `extraction/marker_body.txt`.
- (Nougat/Marker neural OCR not run in this environment; pdftotext body is
  faithful for the equations of interest, which were verified by hand against
  the physics — see `report/failure_analysis.md`.)

## Key extracted content

### Model (Sec. II–III)
- Nearest-neighbor **XXZ Heisenberg antiferromagnet on the kagome lattice**,
  spin-1/2. Anisotropy parameter λ selects **XY regime (Jλ < 1)** vs **Ising
  regime (Jλ > 1)**.
- **Chirality-breaking term** (Eq. 3.2):
  `H_ch = h · Σ_△ χ_ijk = h · Σ_△ S_i · (S_j × S_k)`, sum over all triangles
  (two per unit cell). Breaks time-reversal explicitly.
- **External field** term `−h_ext Σ_i S_i^z`; the MAIN result is at **h_ext = 0**
  (half filling of the flux-attached fermions).

### Method
- **Flux attachment**: hard-core bosons (S±) → fermions coupled to a **kagome
  Chern-Simons gauge field**; `S^z = 1/2 − n`, boson number ↔ plaquette flux.
- Chirality term → modified hopping `J^(a)` plus an extra **Peierls phase**
  (Eq. 3.5): `φ^(a)(x) = arctan[(h/J)(1/2 − n^(a)(x))]`.
- In the **XY / pure-chirality limit J → 0**: `φ^(a) → ±π/2`, giving the
  **(2π, π/2, π/2) flux state** (Eq. 4.22) — the chiral state of Bauer et al. [25].

### Headline claim
> In the XY regime, the chirality term leads to a **chiral spin liquid even in
> the absence of a uniform magnetic field**, with effective spin Hall conductance
> **σ_xy^s = 1/2** (bosonic Laughlin ν=1/2 class).

- DM term gives a similar CSL if not too strong; ring-exchange can trigger CSL
  via spontaneous TRS breaking if its coupling is large enough. Ising regime:
  needs a strong chirality term to close the anisotropy gap first.
