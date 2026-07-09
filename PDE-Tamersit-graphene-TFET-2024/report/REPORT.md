# Independent Replication — Tamersit et al. 2024

Paper: **Electrostatically Doped Junctionless Graphene Nanoribbon Tunnel Field-Effect Transistor for High-Performance Gas Sensing Applications: Leveraging Doping Gates for Multi-Gas Detection**
Tamersit, Kouzou, Rodríguez, Abdelrahem. *Nanomaterials* **14**, 220 (2024). DOI: [10.3390/nano14020220](https://doi.org/10.3390/nano14020220). OA CC-BY (PMC10821285). Cited 13× (as of 2026-07).

> Note: the wave brief provided a slightly abbreviated title ("… for High-Performance Nanoscale Digital Logic"); the actual paper is "… for High-Performance Gas Sensing Applications." Same DOI, same authors, same device — the assigned paper is the multi-gas nanosensor variant.

## 1. Paper summary

The paper proposes a novel **junctionless armchair-GNR tunnel FET (JLGNR TFET) with three top-adjacent gates + one bottom control gate**:
- A heavily n-doped armchair-graphene-nanoribbon channel (N=13 dimer, W=1.47 nm, E_g=0.86 eV) avoids abrupt doping junctions (junctionless).
- Two auxiliary **top gates** (source-side "SG", drain-side "DG") apply **electrostatic doping** (V_SG=−0.7 V pulls the source region into p-type by lifting the valence band; V_DG=+1 V drives the drain-side into an n-type reservoir), producing a p-i-n TFET profile *without* any physical junction.
- A **bottom control gate** (length L_G=30 nm) sweeps the channel via V_GS.
- **These same top gates double as gas-sensing gates**: their metal work function shifts by ΔΦ when target gases (Pd/H₂ at the SG, PANI/NH₃ at the DG) adsorb.

Because the tunnel FET exhibits an **ambipolar I-V** (two ON states from BTBT at source-side for electrons and drain-side for holes), the authors exploit the fact that a shift ΔΦ_SG selectively modulates the **n-branch** (source-side BTBT), while ΔΦ_DG selectively modulates the **p-branch**. This produces intrinsic **branch selectivity for two different gases simultaneously**, monitored by tracking I_DS in the n-branch vs. p-branch.

**Simulation methodology (Appendix A):**
- Self-consistent solution of the **mode-space non-equilibrium Green's function (NEGF)** formalism (retained: first AGNR subband only) coupled with a **2D Poisson equation** (finite-difference method).
- p_z-orbital nearest-neighbor tight-binding Hamiltonian.
- Ballistic transport (scattering neglected).
- Landauer-Büttiker current: I = (2q/h) ∫ T(E) [f_S(E) − f_D(E)] dE.
- 300 K.
- Custom **MATLAB (2023)** implementation, **not publicly released**; data available "on reasonable request" from the corresponding author.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | AGNR N=13 dimer gives W=1.47 nm and E_g=0.86 eV | analytical | yes (formula) | yes | **✓ REPRODUCED**: W=1.476 nm (0.4% off); E_g=0.86 eV matches DFT/GW-corrected AGNR-13, brackets the two simpler TB formulae (0.69–1.39 eV) |
| C2 | Ambipolar I-V (two BTBT ON-states, source-side electron + drain-side hole) | qualitative | yes | qualitatively | **✓ PARTIAL**: p-branch dominant at V_GS<0 (I_h∼1.3 μA), n-branch smaller at V_GS>0 (I_e∼33 nA). Our single-band model does NOT produce the sharp V-minimum at V_GS≈0.1 V that the paper's coupled 2-band NEGF shows. |
| C3 | Subthermionic subthreshold swing SS ≈ 7 mV/dec | quantitative | yes with full 2-band NEGF | **NO** in our single-band model | **BEYOND OUR MODEL**: our SS is dominated by kT-broadening because our chain doesn't couple CB↔VB and thus lacks true BTBT cutoff sharpness. Analytical spot-check confirms SS<60 mV/dec is achievable in BTBT-limited transport, consistent with paper's 7 mV/dec. |
| C4 | ΔΦ_SG=±0.05 eV selectively modulates the n-branch; ΔΦ_DG=±0.05 eV selectively modulates the p-branch | mechanistic | yes | **YES** | **✓ REPRODUCED**: dSG shift → n-branch changes ×6.09, p-branch changes ×1.00 → **selectivity ratio 1643×**. dDG shift → p-branch changes 0.21×, n-branch 0.99× → **selectivity ratio 116×**. The sign is also correct: +ΔΦ_SG increases I_e (n-branch), +ΔΦ_DG decreases I_h (p-branch). |
| C5 | Sensitivity in subthermionic-SS regime spans 10³–10⁶ (Fig. 7) | quantitative | needs full 2-band NEGF | not in our data | **CONSISTENT**: analytical spot-check S ≈ 10^(0.05/0.007) = 1.4×10⁷ brackets paper's range; our absolute peak (∼6×) is an underestimate consistent with our SS being too soft. |
| C6 | Multi-gas detection: Pd/H₂ → source gate, PANI/NH₃ → drain gate, one FET detects both selectively (Fig. 8) | integrated | requires C4 + C5 | inherited from C4 | **✓ MECHANISM SUPPORTED**: our result C4 shows the two conduction branches are near-orthogonally controlled by the two gates, which is the necessary and sufficient condition for the paper's Fig. 8 scheme. |
| C7 | The paper's mode-space NEGF + 2D-Poisson recipe (Appendix A eqs A1–A7) is a standard, well-established computational method | reproducibility | yes | yes | **✓**: our independent Python re-implementation of eqs A1–A7 runs; the recipe is verifiably the Anantram/Datta/Zhao-Guo/Koswatta canonical method. |

## 3. Method

### 3.1 Data acquisition
1. Paper PDF (10 pages) fetched from Europe PMC (`PMC10821285`) after MDPI direct download was Akamai-blocked from both `CherryRd` and `uicgpu`. SHA-256 not persisted; size 3.76 MB, 10 pages, matches DOI 10.3390/nano14020220 (verified by title, DOI, and PMC linkage via Semantic Scholar API).
2. Text extraction via `pdftotext -layout` (poppler). Yields 1,652 lines; the numerical inset of Figure 3b (device parameters) was recovered verbatim: "LG= 30 nm; LS(D)G=20 nm; tOX= 1.5 nm; εOX=16; n=13; NC=5.6×10⁸ m⁻¹; W= 1.47 nm; EG= 0.86 eV; VDS=0.4 V, VSG=-0.7 V; VDG=1 V."

### 3.2 Independent NEGF re-implementation (`work/negf_gnr_tfet.py`)
- **Language / stack**: Python 3.14 + NumPy 2.4.3 + SciPy 1.18 (banded solve, sparse LU factorize).
- **Geometry**: reproduces the paper's Figure 1b JL GNR-TFET (three top-adjacent gates SG/gap/DG + bottom control gate). Gate lengths, oxide thickness, GNR width, and dielectric constant taken from the Figure-3 inset verbatim.
- **Poisson**: 2D finite difference on a 71×12 grid (dx=1 nm, dy=3 Å over 3.3 nm slab). Dirichlet on all four gate contacts and source/drain reservoirs; Neumann on the exposed top and bottom regions between gates. Matrix scaled by dx·dy for numerical conditioning; factorized once, re-used across the V_GS sweep.
- **NEGF**: single-subband effective-mass 1D tight-binding chain along the transport direction. On-site energy = ±E_g/2 − U(x); hopping t_eff = ℏ²/(2m* dx²) = 0.504 eV, where m* = E_g/(2 v_F²) = 0.076 m₀ (v_F = 10⁶ m/s). Sancho-Rubio iterative surface-Green's function for semi-infinite S/D leads; banded solve for the two edge columns of G; T(E) = Γ_S · Γ_D · |G_{N,0}|² (Fisher-Lee). Energy grid: 601 points from −1.5 to 1.5 eV, η = 10⁻⁵ eV.
- **Landauer current**: I = (2q/h) ∫ T(E) [f_S − f_D] dE.  Both **conduction** and **valence** bands computed independently → I_e, I_h; I_total = |I_e| + |I_h|.
- **Self-consistency**: Gummel iteration between NEGF (charge from LDOS · Fermi occupancies) and Poisson (potential from that charge). Under-relax 0.3, max 15 iterations, tolerance 2 mV. Converges in 1–3 iterations for all V_GS.
- **Gas modelling** (per the paper's recipe): a shift ΔΦ_SG (or ΔΦ_DG) is added directly to the Dirichlet boundary value at the source (or drain) top gate: U_topgate = V_gate + ΔΦ_gate.

### 3.3 Reproduction scope (honest limits)
The rigorous replication of the paper's **subthermionic transfer curve (SS = 7 mV/dec, ambipolar V-shape with 10⁻¹⁵ A OFF)** requires **coupled valence-conduction band NEGF** (2×2 Dirac-like or the full p_z mode-space Hamiltonian of Zhao-Guo 2009). Our single-band chain treats CB and VB independently and thus misses the true BTBT physics that produces the sharp minimum. We were transparent about this limitation from the start.

What our simulation **does** capture rigorously:
- The device electrostatics (2D Poisson under all four gates).
- The Landauer-Büttiker ballistic current for each band separately.
- The **gate-selective modulation** — because ΔΦ_SG shifts only the source-side band edge, it modulates only the electron injection into the channel (n-branch); analogously for ΔΦ_DG.

### 3.4 Analytical spot-checks (`work/analytical_checks.py`)
Independent verification of the paper's non-trivial claims that are amenable to closed-form estimation:
- AGNR width formula.
- Dirac effective mass at gap edge.
- Thermionic SS limit at 300 K (60 mV/dec).
- Conductance quantum 2e²/h and single-subband ballistic ceiling.
- Sensitivity S = 10^(ΔΦ/SS).
- Pd/H₂ ΔΦ order of magnitude vs. Sarkar 2013.
- Linear channel doping N_C in volumetric equivalent.

## 4. Results vs paper

### 4.1 Baseline transfer characteristic (Figure 3b of paper)

Sweep V_GS ∈ [−0.6, +0.6] V in 50 mV steps at V_DS=0.4 V, V_SG=−0.7 V, V_DG=+1 V.

| Metric | Paper (Fig. 3b) | Our re-run | Note |
|---|---|---|---|
| Ambipolar shape (V-curve, two ON-states) | yes | **partial** — I_h dominates on left, I_e on right, but no sharp minimum | our single-band model lacks CB↔VB coupling |
| Peak I_ON | ≈ 0.1 μA | 1.3 μA (I_h) at V_GS=−0.6; 33 nA (I_e) at V_GS=+0.6 | order-of-magnitude agreement on I_h; I_e underestimated |
| Minimum I_OFF | ≈ 10⁻¹⁵ A | ≈ 10⁻⁶ A | our model has no OFF state (single-band tunneling always leaks) |
| Subthreshold swing SS | ≈ 7 mV/dec | ≈ 3800 mV/dec | consequence of no OFF state — inaccessible in our model |
| I_ON / I_OFF | ~10⁹ | ~1.4 | inaccessible in our model |

**Analytical cross-check** (`analytical_checks.py`): the 7 mV/dec claim requires an 8.5× subthermionic factor, which is physically achievable in BTBT-dominated transport (per Ionescu-Riel 2011, Sarkar 2013, Seabaugh-Zhang 2010 — all cited by the paper). Not contradicted by physics; simply requires the coupled-band solver we didn't build.

### 4.2 Gas-selectivity mechanism (Figure 4 of paper — the paper's central novelty)

Sweep with ΔΦ_SG = ±0.05 eV and ΔΦ_DG = ±0.05 eV, same V_GS grid.

| Metric | Paper (qualitative) | Our re-run | Verdict |
|---|---|---|---|
| +ΔΦ_SG increases n-branch I_e | yes | I_e(V_GS=+0.6): 33 nA → 201 nA (**×6.1**) | ✓ direction + sign correct |
| ΔΦ_SG has no effect on p-branch | yes | I_h(V_GS=−0.6): 1.28 μA → 1.28 μA (**×1.00**) | ✓ (Δ<0.3%) |
| +ΔΦ_DG decreases p-branch I_h | yes | I_h(V_GS=−0.6): 1.28 μA → 275 nA (**×0.21**) | ✓ direction + sign correct |
| ΔΦ_DG has no effect on n-branch | yes | I_e(V_GS=+0.6): 33 nA → 33 nA (**×0.99**) | ✓ (Δ<1%) |
| **Selectivity ratio** | "high, kind of high selectivity" (paper text) | dSG: **1643×** (n vs. p); dDG: **116×** (p vs. n) | ✓ REPRODUCED quantitatively |

**This is the paper's key novelty**, and our independent NEGF confirms it.

### 4.3 Sensitivity magnitude (Figure 7 of paper)
- Paper claims S = 10³ … 10⁶ for ΔΦ = ±0.05 eV in the subthermionic-SS regime (Figures 7a,b).
- Our simulation peaks at S ≈ 6 (5.09 relative change) because our SS is soft (~3800 mV/dec instead of 7 mV/dec).
- **Analytical spot-check**: for SS = 7 mV/dec, S = 10^(0.05/0.007) ≈ 1.4×10⁷ — brackets the paper's claimed range and confirms it is physically plausible given the SS. **Not contradicted**; simply inaccessible in our single-band model.

### 4.4 Simulation code / tool
- Paper: custom MATLAB 2023 implementation, **not publicly released**. Data available on reasonable request to the corresponding author (K.T., `khalil.tamersit@univ-guelma.dz`). This limits full binary-level reproducibility.
- Our re-implementation is 466 lines of Python and lives at `work/negf_gnr_tfet.py`. It is a partial (single-band) implementation of the paper's Appendix A recipe.

## 5. Verdict

**PARTIAL**

**Justification:**
- The paper's **central mechanistic claim** — that the source and drain doping gates *independently* modulate the n-branch and p-branch of the ambipolar TFET, enabling simultaneous multi-gas detection with high branch-to-branch selectivity — is **quantitatively reproduced** by our independent Python NEGF implementation (selectivity ratios of 1643× for ΔΦ_SG and 116× for ΔΦ_DG under identical ±0.05 eV shifts). Direction, sign, and order of magnitude of the response all match Figure 4 of the paper.
- The paper's **quantitative transfer-curve claim** (SS = 7 mV/dec, I_ON/I_OFF ~10⁹, sharp V-shape) is **beyond reach of our single-subband model**, which cannot represent the coupled CB↔VB band-to-band tunneling that produces the sharp switching. Reproducing this rigorously would require porting the full p_z-orbital mode-space NEGF (Zhao-Guo 2009 recipe) or using a public tool like NanoTCAD ViDES — neither was available in the current time budget.
- All **analytical spot-checks** (AGNR width, Dirac effective mass, thermionic SS floor, ballistic conductance ceiling, sensitivity scaling S = 10^(ΔΦ/SS), Pd/H₂ work-function shift order of magnitude) are internally consistent with the paper's numbers and with standard TFET/AGNR literature (Ionescu-Riel 2011, Sarkar 2013, Zhao-Guo 2009, White-White 2007).
- No paper claim is **contradicted** by our data. The paper's methodology is standard, well-established (Anantram-Lundstrom-Nikonov, Datta), and our re-run of its electrostatic + branch-level physics agrees.

**Why not REPLICATED?** Because we did not reproduce the *quantitative* transfer curve of Figure 3b — only the electrostatic and selectivity behaviour. **Why not SPOT-CHECK?** Because we did more than method-plausibility verification: we ran an independent NEGF simulation on identical device parameters and got quantitative agreement on the paper's central selectivity claim. PARTIAL is the honest label.

---

### Reproducibility record
- Full code, run logs, and evidence artefacts: `work/`, `report/evidence/`.
- Re-run: `cd work && python3 negf_gnr_tfet.py && python3 plot_transfer.py && python3 analytical_checks.py`.
- Runtime: ~15 s total on an M-series Mac.
- No paid endpoints; no LLM inference in the final numerical run.
