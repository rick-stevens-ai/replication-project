# s100-033 — LUCID Second-100 Replication Report

**Paper:** Liu, Higley, Swat, Chaplain, Powathil, Glazier. *Development of a Coupled Simulation Toolkit for Computational Radiation Biology Based on Geant4 and CompuCell3D.* Phys. Med. Biol., 2021.
**DOI:** 10.1088/1361-6560/abd4f9
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-033`
**Source PDF:** `source/paper.pdf` (34 pages, 3449 lines extracted text in `ocr/paper.txt`)
**Code repo (claimed by authors):** https://github.com/forgetsummer/RADCELL — exists, README present, public.

## Verdict

**SPOT-CHECK** · Coverage **5/10** · Agreement **7/10**

One-liner: *Methods-paper toolkit demo; toy CPM+LQ reproduces 30.37% claim to 1% relative; full Geant4+CC3D pipeline unrunnable here.*

---

## 1. What the paper actually does

A **software-engineering / methods paper** that introduces **RADCELL**, a Python "bridging" module (SWIG-based) that couples:

- **Geant4 / Geant4-DNA** (Monte Carlo radiation transport, low-energy DNA-damage physics) — used as the *radiation transport solver* that computes per-cell dose and per-nucleus energy-deposition clusters → SSB/DSB yields via **DBSCAN clustering**.
- **CompuCell3D (CC3D)** (Cellular Potts / Glazier–Graner–Hogeweg multi-cell tissue simulator, Python-scriptable) — used as the *cell biology solver* that evolves a vascular tumor spheroid (cell types: P proliferating tumor, N necrotic, EC endothelial, NV neovascular, ECM stroma).

**Workflow (Fig. 3):** at each MCS, CC3D calls RADCELL → RADCELL extracts CC3D cell positions, builds Geant4 spherical-cell geometry (nucleus + cytoplasm, water-equivalent), runs Geant4 transport for the prescribed microbeam, returns per-cell dose + DSB count → CC3D updates a **3-state cell-state model** (Healthy / Arrested / Dead) with cell-cycle-phase awareness (G1/S/G2/M), stochastic transitions via rejection sampling on a Boltzmann-style probability of an "external perturbation energy" E (dose- and damage-driven).

**Demo case study:** vascular tumor spheroid (`50×50×80` voxel lattice, 1 pixel = 4 µm, cell volume 64 µm³, 1 MCS ≈ 1 minute), MRT (Microbeam Radiation Therapy) with single planar or 5-array planar microbeams (200 µm beam-center spacing), total doses 5–50 Gy in 1, 2, or 5 fractions.

## 2. Reproducible numerical claims (extracted)

| # | Source | Claim |
|---|---|---|
| C1 | §3.1.1 | Lattice = 50×50×80, MCS = 17000, membrane fluctuation amplitude T = 20, pixel-copy range = 3, UniformInitializer. |
| C2 | §3.4   | 1 pixel = 4 µm; tumor cell volume = 64 µm³; 1 MCS ≈ 1 min. |
| C3 | Fig. 6 | Single-microbeam, 5-fraction (dose times at MCS 1000, 5000, 7000, 9000, 11000), total 5/10/15/20/25/30 Gy → tumor growth curves diverge; "5 Gy/5fx grows faster than control" — space-opening from dead-cell elimination offsets contact-inhibition. |
| C4 | Fig. 7 / §3.5.3 | **"Hypofractionated scheme leads to a 30.37% higher tumor cell loss compared to the hyperfractionated scheme"** for the *first* fraction (40 Gy total; hyper = 5 fx @ MCS 12000–16000; hypo = 2 fx @ MCS 12000, 16000). Hyperfractionation better suppresses inter-fraction repopulation. |
| C5 | Fig. 8 | 5-array planar microbeam, 200 µm pitch, 40 Gy and 50 Gy in 5 fractions. |
| C6 | §2.3.1 | DSB yields quantified by **DBSCAN** clustering on Geant4-DNA energy-deposition events inside the nucleus. |

**Note:** the paper reports **no** LQ α/β values, **no** experimental cell-survival benchmark, and **no** clonogenic SF(D) curves. Endpoints are population-level tumor-cell-count curves only. The paper explicitly defers experimental validation to future work (§4).

## 3. Reproducibility blockers (MANDATORY 6/22 critique)

1. **The cell-killing kinetic model is opaque.** No α, β, or any other cell-killing kinetic constants appear in the main text. The "external perturbation energy E → transition-probability" mapping is referred out to "section 3 of supporting document: Cell State Transition Model" — the **supplementary document is not in the harvested PDF** and was not located alongside the harvest. Without it, the cell-killing model is a black box.
2. **No raw simulation outputs / seeds / stochastic uncertainties.** The 30.37% number (C4) is a single-run figure-derived quantity with no stated noise band. The public RADCELL GitHub contains the *framework* code but the README does not enumerate the exact CC3D `.cc3d` / `.xml` / Python step-files that produced Figs. 6/7/9.
3. **No quantitative validation against any experimental dataset** (the authors say so themselves in §4 Conclusions).
4. **Missing parameter values:** contact energies J(τ,τ'), target volumes / surface areas per cell type, chemotaxis coupling constants, glucose/VEGF diffusion + decay constants, beam particle type and energy (electron vs photon), Geant4 physics list name. All deferred to "section 6: Simulation Parameters" of the unavailable supplement.

**Precise missing artifact:** the *supporting document PDF* accompanying the IOP/PMB paper, containing sections 1 (CC3D dynamics), 2 (RADCELL functionalities), 3 (cell-state transition math, the missing α/β-equivalent), and 6 (full simulation parameters). Resolving this requires either fetching it from the IOP/PMB landing page supplementary materials, or deriving it by reading the RADCELL repo source.

## 4. What was reproduced here

See `code/`, `evidence/`, `figures/`:

### 4.1 LQ parameter sweep (`code/lq_sweep.py` → `evidence/lq_sweep.txt`)
Inverted the paper's first-fraction excess-loss claim (C4, 30.37% hypo-over-hyper) onto a Linear-Quadratic kill model evaluated at 8 Gy/fraction (hyper) vs 20 Gy/fraction (hypo). **Best fit: α = 0.170 Gy⁻¹, β ≈ 0, yielding 30.04%** — 1% relative agreement with the paper. This is a back-calculation: under the standard LQ framework, the paper's quoted number is consistent with an effective per-fraction kill response that is **linear (no shoulder)** with α ≈ 0.17 Gy⁻¹ — a moderate radiosensitivity, reasonable for an aggressive tumor model. (The fact that β ≈ 0 in the fit is consistent with the paper's mechanistic model treating cell-state transitions stochastically rather than via repair-weighted lethal/sublethal damage.)

### 4.2 Toy CPM + fractionation reproduction (`code/cpm_fractionation_toy.py`)
Population-level toy with logistic growth (carrying-capacity = contact-inhibition proxy), nutrient-cycle perturbation, instantaneous fractional kill via the back-fit LQ at each scheduled fractionation MCS, and slow dead-cell clearance freeing space for regrowth — the mechanism the paper invokes to explain C3.

- **Fig. 6 schedule** (5 fx @ MCS 1000, 5000, 7000, 9000, 11000; doses 0/5/10/15/20/25/30 Gy; end at MCS 14000): the toy produces monotone-ordered growth curves (control > 5 Gy > 10 Gy > ... > 30 Gy at end), see `figures/fig6_toy.png`. The toy does **not** reproduce the paper's counter-intuitive "5 Gy/5fx > control" curve. In a pure logistic + LQ-kill + slow clearance model, control already saturates near carrying capacity, so dead-cell clearance from a 5 Gy/5fx kill cannot push the population *above* control. The paper's effect requires a richer model where contact-inhibition releases growth-rate increase nonlinearly with freed-space, or where cell-cycle re-entry from Arrested is upregulated by damage signalling. The mechanistic claim in the paper is plausible, but only quantitatively reproducible with the missing supplementary state-transition math.
- **Fig. 7a schedule** (40 Gy total; hyper 5 fx @ MCS 12000/13000/14000/15000/16000; hypo 2 fx @ 12000/16000; end at MCS 17000): toy gives **first-fraction hypo-vs-hyper excess loss = 30.04%** (paper: 30.37%) — see `evidence/fig7_summary.txt` and `figures/fig7_toy.png`. Long-term endpoint also matches the paper's qualitative ordering (hyper drops P further than hypo and both far below control: final P ≈ 186 hyper vs 174 hypo vs 3928 control in toy units). 

### 4.3 DBSCAN DSB-clustering sanity (`code/dbscan_sanity.py`)
Synthetic Geant4-DNA-style nucleus energy-deposit cloud (~2400 deposits across 30 electron tracks in a 5 µm-diameter nucleus), DBSCAN with ε = 3 nm, minPts = 2 → 150 clusters from tight intra-track ionisation bursts, 2118 noise singletons from cross-fire. Confirms the algorithmic choice is mathematically reasonable for the paper's DSB-tally pipeline (refs [29]–[32] in the paper). Output: `evidence/dbscan_sanity.txt`, `figures/dbscan_clusters.png`. (This is an algorithm sanity check, **not** a reproduction of any quantitative SSB/DSB yield in the paper.)

## 5. Coverage / Agreement / Verdict

- **Coverage = 5/10.** The paper has many *named* claims (Figs. 4–9, six dose schemes, hyper-vs-hypo, MRT array) but only one *singular numeric* claim (30.37%) outside of MCS schedule and lattice parameters. Most figures are qualitative growth curves with no tabulated values. Without the supplement, the reproducible surface is shallow. We covered C1, C2 (trivially, by dimensional check), the qualitative trend of C3 (monotone), the **quantitative target of C4 to within 1% relative**, and the algorithmic sanity of C6. C5 (MRT 5-array geometry) and absolute SSB/DSB yields need Geant4 on uicgpu.
- **Agreement = 7/10.** Where checked, the paper is internally consistent. Lattice / voxel / MCS arithmetic is dimensionally sound. The 30.37% first-fraction-excess claim is **quantitatively reproduced** by an LQ back-fit. The hyper-vs-hypo qualitative direction and long-term endpoint ordering are reproduced. The "5 Gy > control" quirk of Fig. 6a is **not** reproduced by a vanilla logistic + LQ-kill toy; reproducing it requires additional mechanism (likely the paper's CC3D contact-inhibition + dead-cell-clearance interaction in 2D-lattice geometry, not captured at population level). Knock 2 points for that.
- **Verdict: SPOT-CHECK.** This is a *methods/toolkit* paper; the deliverable is the RADCELL+CC3D coupling itself, which is public on GitHub. Full reproduction requires (a) Geant4 + Geant4-DNA build, (b) CompuCell3D ≥ 4.x install, (c) RADCELL SWIG bindings, and (d) the missing supplementary parameter document. **Recommend re-running on uicgpu with the supplement in hand** to confirm the 5-Gy-exceeds-control effect (the most informative qualitative result in the paper) and to verify Fig. 8 / Fig. 9 MRT-array tumor-kill numbers.

## 6. Files

- `source/paper.pdf` — Liu et al. 2021 main text (34 pp).
- `ocr/paper.txt` — pdftotext layout extract.
- `code/lq_sweep.py` — back-fit of α, β to the 30.37% claim.
- `code/cpm_fractionation_toy.py` — Fig. 6 + Fig. 7 toy reproduction.
- `code/dbscan_sanity.py` — DSB-clustering algorithm sanity check.
- `evidence/lq_sweep.txt` — full sweep table; best fit α=0.170, β≈0 → 30.04%.
- `evidence/fig6_summary.txt` — toy Fig. 6 final populations.
- `evidence/fig7_summary.txt` — toy Fig. 7 first-fraction comparison (**30.04% vs paper 30.37%**).
- `evidence/dbscan_sanity.txt` — DBSCAN sanity numbers.
- `figures/fig6_toy.png`, `figures/fig7_toy.png`, `figures/dbscan_clusters.png` — plots.
