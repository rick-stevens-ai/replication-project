# Skyrmion collapse — Verga 2014 (arXiv:1409.0256v2)

> **Extraction provenance.** `marker` is **not installed** on this host
> (`which marker` → not found). This file is an **interim Marker-slot artifact**
> produced with `pdftotext` (poppler, `/usr/bin/pdftotext`). It carries the full
> readable text of the paper so the report is self-contained; it is *not* the
> layout-and-table-aware Markdown that Marker would emit. Replace with a true
> Marker run when the tool becomes available. See `report/artifacts_summary.md`.

---

## Bibliographic

- **Title:** Skyrmion collapse
- **Author:** Alberto D. Verga
- **Affiliation:** Aix-Marseille Université, IM2NP, Campus St Jérôme, service 142, 13387 Marseille, France
- **arXiv:** 1409.0256v2 [cond-mat.mes-hall], 1 Dec 2014
- **PACS:** 75.76.+j, 75.70.Kw, 75.78.-n

## Abstract (verbatim)

We investigate the topological change in a Belavin-Polyakov skyrmion under the
action of a spin-polarized current. The dynamics is described by the Schrödinger
equation for the electrons carrying the current coupled to the Landau-Lifshitz
equation for the evolution of the magnetic texture in a square lattice. We show
that the addition of an exchange dissipation term, tends to smooth the transition
from the skyrmion state to the ferromagnetic state. We demonstrate that this
topological change, in the continuum dissipationless limit, can be described as a
self-similar finite-time singularity by which the skyrmion core collapses.

## Model (as reimplemented)

The system couples:

1. **Schrödinger equation** for the itinerant electrons (spin-polarized current
   carriers) on a square lattice — the source of the spin-transfer torque (STT).
2. **Landau-Lifshitz equation** for the localized magnetic texture **S**(r,t),
   `|S| = 1`, driven by the electron spin density **s** via STT plus a
   *polarization field* (b-field). An optional exchange-dissipation term `d`
   smooths the skyrmion → ferromagnet transition.

The magnetic energy is the classical Heisenberg exchange
`H_S = (J/2) ∫ (∇S)² d²r` (lattice: `H = J Σ_<ij> (1 − Sᵢ·Sⱼ)`), with **no DMI**.

### Key closed-form results the paper states

- **Belavin-Polyakov (BP) skyrmion**, stereographic projection `w = z/λ`, has
  **exchange energy `Exc = 4πJ`** and **topological charge `Q = 1`** (core), and
  is **scale-invariant** (energy independent of size λ). *(lines 428–429)*
- Without dissipation the coupled system conserves `|S| = 1` and the topological
  charge `Q(t)` *(line 179)*. The collapse is what breaks Q conservation on the
  lattice, "by change of a single spin."
- **Self-similar collapse ansatz** near the finite-time singularity `t → t*`:
  `w = (t* − t)^(−α) f(r / (t* − t)^β)` with the size vanishing at `t*`
  *(lines 556–604)*. Dimensional balance of the driven Landau-Lifshitz equation
  fixes **α = 1, β = 1/2** *(Eq. 17)*.
- Collapse-time estimate `t* ∼ λ /(s₀ a)`, with `s₀ ∼ nₑ B_p` the electron
  spin-density × polarization scale *(line 616)*.
- The topological change toward the ferromagnetic state is correlated with the
  appearance of intense **electron b-field** structures carrying their own
  topological charge (a localized electron vortex) *(lines 304–330, 520)*.

## Full text (pdftotext extraction)

The complete linear text of the article is preserved at
`../textures-polar-verga2014.txt` (1088 lines) and the layout-preserving variant
at `_pdftotext_layout.txt` (612 lines). Section headings recovered by pdftotext:

- I. INTRODUCTION
- II. MODEL (coupled Schrödinger + Landau-Lifshitz on a square lattice)
- III. NUMERICAL RESULTS (skyrmion → FM transition, Q(t), b-field vortex)
- IV. SELF-SIMILAR COLLAPSE (continuum dissipationless limit, Eqs. 15–25)
- V. CONCLUSION

Figures (not extractable as text): Fig. 1 skyrmion initial state; Fig. 2 collapse
snapshots (t = 5912–5960 t₀); Fig. 3 Q(t) for different exchange dissipation;
Fig. 4 self-similar profile.
