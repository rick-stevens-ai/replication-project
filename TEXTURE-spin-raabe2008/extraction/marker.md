# Extraction marker — arXiv:0811.0157

- **Paper:** D. Raabe, B. Sander, M. Friák, D. Ma, J. Neugebauer,
  *Ab-initio simulation and experimental validation of beta-titanium alloys*,
  arXiv:0811.0157 (progress report, 2008-11-02). Max-Planck-Institut für Eisenforschung.
- **Extraction method:** `pdftotext -layout paper.pdf paper.txt` (805 lines). No OCR needed; PDF has a text layer.
- **Theme check:** **OFF-THEME** relative to the "Textures-100 / texture-spin" batch label. This is a
  DFT + experiment materials-design paper on biomedical β-Ti alloys (low-stiffness bone implants).
  "Texture" appears only as one of several characterized properties (crystallographic texture of cast
  samples), not the subject. Replicated the tractable reproducible computational claims anyway
  (see below) rather than marking NO-GO, because the paper contains closed-form models
  (mixing entropy, wt↔at conversion) and quantitative data claims that ARE machine-checkable.

## Key equations / numbers extracted (verbatim from text)
- Eq.(1) formation energy: `Ef^σ(Ti_x X_{1-x}) = E_tot^σ/N - x·µ_Ti(hcp) - (1-x)·µ_X(bcc)`; stable if Ef<0.
- Eq.(2) config entropy: printed as `Sconfig = kB[x ln x + (1-x) ln(1-x)]` (missing minus sign — see thermo.py note).
- Eq.(3) free energy: `Ff(x,T) = <Ef> - T·Sconfig`.
- Eq.(4) Young's modulus: `σ = (δE/δε)/(A·a0)`; E along [001] uniaxial tensile.
- T=0 β-stability onset: Ti-Nb Nb>~93 at%; Ti-Mo Mo>~25 at% (xcrit).
- Finite-T (ref = hcp↔bcc transition ~882°C) onset: Ti-Nb ~25 at% Nb; Ti-Mo drops 25→14 at% Mo.
- Single-phase bcc thresholds (Gibbs construction): ~39 at% Nb; ~36 at% Mo.
- Experimental Young's moduli (GPa, polycrystal, 3h/1200°C homogenized):
  Ti-Nb: 10at%→91.2, 20at%→75.8, 30at%→72.1. Ti-Mo: 10at%→88.4, 20at%→106.9.
  hcp-Ti reference = 114.7 GPa. Best binary Ti-30Nb → 37% stiffness drop.
- Table 1 wt%↔at% for 8 alloys (used for C4).

## What is NOT reproducible here
- The DFT total energies E_tot (VASP/GGA-PBE96, supercells) — needs a plane-wave DFT run,
  out of scope for a laptop/free-endpoint overnight job. We surrogate the energy *shape* only to
  test the entropy machinery, and label it as such.
