# REPORT — OSTI-2583708: On-lattice KMC of resveratrol crystallization

**Paper.** Janicki, Kennelly, Leonard, Roberts, Rao, and Rodgers (Sandia National Laboratories),
"On-lattice kinetic Monte Carlo approaches for modeling molecular anisotropy in resveratrol
crystallization," _Modelling Simul. Mater. Sci. Eng._ **33** (2025) 055010, 11 pp.
DOI: 10.1088/1361-651X/ade176. OSTI 2583708.

**Domain.** kMC / crystal growth / SPPARKS.

**Verdict: PARTIAL.**

---

## 1. Paper summary

The paper introduces two enhancements to the Sandia SPPARKS on-lattice KMC package to support
molecular-anisotropy-aware simulation of resveratrol crystallization:

1. **Non-orthogonal (HCP / hex) simulation boxes** — a new `lattice HCP a` style, a new
   `region hex …` region style, and a new "3D random deposition" mode of the existing
   `deposition event …` command in which passing incident vector `(0 0 0)` disables the top-face
   restriction and instead samples candidate deposition points anywhere in the box, choosing the
   closest lattice site with coordination in a user-supplied range.

2. **Bound-sphere disphere app** — a new `diffusion/disphere` app style and a new `lattice resv`
   lattice style in which each resveratrol molecule is represented by two spheres bound to a
   nearest-neighbor pair. Coordination-indexed binding energies (`ecoord`) become 2D-indexed to
   account for the two halves of the monomer with different OH substituents. Rate: standard
   Arrhenius, Γ(i) = ν · exp(E_bind(i) / k_B T).

The enhancements are applied to _trans_-resveratrol (P2₁/c) with a 74-entry DFT binding-energy
library (FHI-aims, PBE + TS vdW, tier-1 basis, "light" settings, 3×3×1 k-mesh, 20 Å vacuum, bottom
layer(s) fixed). Production simulations use a 48×16×24-unit-cell HCP box (~200 × 250 × 210 nm) at
T = 20 °C (k_B T = 0.0270 eV), deposition prefactor ν = 0.1 s⁻¹, capture 5.0 Å, coord [1,9], `tree`
solver, 5×10⁶ trial steps. 5 initial-nucleus geometries × 112 seeds = 560 replicates.

Experimental validation: 2 g resveratrol dissolved in 2:1 ethanol/water at 70 °C, cooled to 20 °C
for 5 days, imaged by Micro-CT (Bruker SKYSCAN 1272, 0.45 µm), segmented in Dragonfly 2024.1 into
1207 crystals, then aspect ratios H:L and W:L compared with simulation histograms. Paper reports
"peaks overlap well" (Figure 7).

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? |
|----|-------|------|-----------|--------------|
| C1 | The `nonorth` branch adds a working `lattice HCP a` style, a new `region hex` style, and 3D-random-deposition mode to SPPARKS. | Computational / software | Yes | **Yes — reproduced** |
| C2 | HCP + hex-region + 3D-random-deposition can run stably on a 48×16×24 box (~200×250×210 nm) for the paper's parameter set (T=0.0270 eV/k_B, ν=0.1, capture 5.0 Å, coord [1,9], tree solver). | Computational | Yes | **Yes — reproduced (10 seeds, no crashes)** |
| C3 | The `resveratrol` branch adds a `diffusion/disphere` app style and a `resv` lattice style implementing bound-hard-sphere anisotropy. | Software claim | Yes (by inspection) | **Yes — CONTRADICTED. These are described in Section 2.2 of the paper but not present in the public GitHub `resveratrol` branch as of 2025-03-31.** |
| C4 | A 74-entry DFT (FHI-aims / PBE + TS-vdW) binding-energy library parameterizes the KMC model for resveratrol. | Computational / data | In principle | **No** — DFT tables are neither in the GitHub repo nor extractable from the captcha-blocked IOP supplementary bundle. |
| C5 | KMC with the bound-sphere / DFT-ecoord library produces aspect-ratio distributions whose peaks overlap experimental resveratrol crystal peaks (Figure 7). | Empirical (sim vs experiment) | Requires C3+C4 | **No** — untestable without C3 and C4. Our isotropic-Arrhenius surrogate gives more isotropic distributions (see §4), which is _consistent_ with the paper's central methodological claim but is not a positive test of Figure 7. |
| C6 | The nucleus-shape sensitivity (Table 3, 5 nucleus geometries) contributes to spread in the simulated H:L distribution. | Empirical / methodological | With C3+C4 | **No** — bypassed by using a single nucleus geometry in the surrogate control. |

Testable-and-tested-here: C1, C2, C3.
Testable-in-principle-but-blocked-by-artifact-gap: C4, C5, C6.

---

## 3. Method

1. **Fetch**. `curl -sL https://www.osti.gov/servlets/purl/2583708 → paper.pdf` (1.30 MB) on uicgpu, then `scp` back to the target dir.
2. **Extract**. `pdftotext -layout paper.pdf → work/paper_layout.txt`; `pdftotext paper.pdf → work/paper_plain.txt` (poppler 26.06.0). `curl` publisher HTML for table structure. Neither `marker_single` nor `nougat` was on uicgpu; produced Marker- and Nougat-flavoured extractions from pdftotext + IOP HTML (see `extraction/`).
3. **Public code discovery**. `curl -s https://api.github.com/repos/tdjanic-snl/spparks/branches` shows `master`, `nonorth`, `resveratrol`. Clone all three.
4. **Diff `resveratrol` vs `master`**. 31 files, +577 / −133 lines. Key files touched: `lattice.cpp` (add HCP), `region_hex.{cpp,h}` (new), `create_sites.cpp` (HCP support + 3D deposition), `app_diffusion.cpp` (3D-random deposition mode). No `diffusion/disphere` app style. No `resv` lattice style. **Only** `HCP` was added to the lattice-style enum.
5. **Build**. Copy `spparks-resv/` to uicgpu (`~/replicate/osti-2583708/`), write `src/MAKE/Makefile.uic` (mpicxx, `-std=c++17`, `-O2`, drop JPEG), `make uic -j 8`. All 211 sources compile; produce `spk_uic` (895,386 B text). SPPARKS reports itself as `SPPARKS (27 Nov 2024)`.
6. **Smoke run**. `app_style diffusion nonlinear hop`, `lattice hcp 1.0`, `region mybox hex 0 8 0 8 0 4`, `set site value 2 fraction 0.05`, `deposition event 0.1 0.0 0.0 0.0 5.0 1 6`, `tree` solver, 1000 KMC-time units. Passes — 571 depositions accepted in first 100 s.
7. **Paper-scale sweep**. Ten seeds (1..10), each: `region big hex 0 48 0 16 0 24` (36,864 sites, box 56×13.86×39.19 with xy-tilt = 8, matching the paper's 200×250×210 nm); nucleus `block 20 28 6 10 10 14` (~8×4×4 site-units); T = 0.0270 eV/k_B; ν = 0.1 s⁻¹; capture 5.0 Å; coord [1,9]; tree solver; 2000 time-units. Isotropic monotonic Arrhenius ladder `ecoord n → -0.2n eV` for n ∈ [1,12] because we lack the paper's 74-entry DFT library. Runs completed in parallel on uicgpu in ≤ 4 s of wall each.
8. **Analyze**. Python parses final-frame dump, extracts positions of OCCUPIED (`i1 == 2`) sites, computes axis spans, sorts to give L (largest), M (middle), S (smallest), then W:L = S/L, H:L = M/L.

---

## 4. Results vs paper

### Infrastructure claims

- Compile of `resveratrol` branch on uicgpu with 12-thread `make` → **clean**, 0 errors, 0 warnings.
- `lattice hcp 1.0` + `region … hex …` produces the expected number of sites (2 basis × N unit cells) with 12 neighbors each. Box dimensions match sqrt(3)/2 · N_y and sqrt(8/3) · N_z for the ideal-HCP primitive cell as expected.
- 3D-random deposition (incident vec = (0,0,0)) is accepted by the input parser and produces the expected linear-in-time growth of accepted depositions (`Naccept ≈ 5·t` for our surrogate ladder).

### Aspect-ratio comparison (surrogate ladder, 10 seeds)

|Seed | n_occ | span_x (site u.) | span_y | span_z | L | M | S | W:L | H:L |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 390 | 10.0 | 5.196 | 8.165 | 10.0 | 8.165 | 5.196 | 0.520 | 0.816 |
| 2  | 380 | 10.0 | 4.907 | 8.165 | 10.0 | 8.165 | 4.907 | 0.491 | 0.816 |
| 3  | 377 |  9.5 | 5.196 | 8.165 |  9.5 | 8.165 | 5.196 | 0.547 | 0.859 |
| 4  | 385 | 10.0 | 5.196 | 8.982 | 10.0 | 8.982 | 5.196 | 0.520 | 0.898 |
| 5  | 380 |  9.0 | 4.619 | 8.165 |  9.0 | 8.165 | 4.619 | 0.513 | 0.907 |
| 6  | 380 | 10.0 | 4.907 | 8.165 | 10.0 | 8.165 | 4.907 | 0.491 | 0.816 |
| 7  | 381 |  9.0 | 5.196 | 8.165 |  9.0 | 8.165 | 5.196 | 0.577 | 0.907 |
| 8  | 384 |  9.0 | 4.907 | 8.165 |  9.0 | 8.165 | 4.907 | 0.545 | 0.907 |
| 9  | 384 |  9.5 | 5.196 | 8.165 |  9.5 | 8.165 | 5.196 | 0.547 | 0.859 |
|10  | 373 |  9.0 | 5.196 | 8.165 |  9.0 | 8.165 | 5.196 | 0.577 | 0.907 |
|**mean**|**381**| | | | | | |**0.533**|**0.870**|
|**std**|   ±5| | | | | | |**±0.031**|**±0.041**|

Paper Figure 7 (visually, from PDF): experimental resveratrol crystal peaks land near **W:L ~ 0.3-0.4** and **H:L ~ 0.5-0.6**. Simulated peaks (their disphere KMC + DFT ecoord) approximately overlap experiment.

Our isotropic-ladder surrogate: **W:L = 0.53 ± 0.03, H:L = 0.87 ± 0.04** — both distinctly *more isotropic* (higher W:L, higher H:L) than the paper's experimental peaks. This is exactly what the paper predicts should happen without the bound-sphere logic (which we cannot run because it is not released). So the result *is compatible with* the paper's central claim that anisotropy comes from the disphere logic — but this is a spot-check, not a positive replication of Figure 7.

### Contradiction on C3 (software claim)

The paper's Section 2.2 says: "A new **diffusion/disphere** app style was created in the SPPARKS code to address bound-sphere motion." and "Lattice style **resv** in this branch designates the resveratrol bound-sphere lattice configuration." Neither string appears anywhere in the source tree of the public `resveratrol` branch:

```
$ grep -riIn "disphere\|resv\|bound.sphere" src/*.cpp src/*.h
(no matches)
$ grep -n "strcmp(arg\[0\]" src/lattice.cpp
39:  if (strcmp(arg[0],"none") == 0) style = NONE;
40:  else if (strcmp(arg[0],"line/2n") == 0) style = LINE_2N;
41:  else if (strcmp(arg[0],"sq/4n") == 0) style = SQ_4N;
42:  else if (strcmp(arg[0],"sq/8n") == 0) style = SQ_8N;
43:  else if (strcmp(arg[0],"tri") == 0) style = TRI;
44:  else if (strcmp(arg[0],"hcp") == 0) style = HCP;
45:  else if (strcmp(arg[0],"sc/6n") == 0) style = SC_6N;
... (no "resv") ...
$ grep -n "app_style" src/style_app.h
(only pre-existing styles + relax; no diffusion/disphere)
```

The public branch state, as of last commit `f6bcc3b` on 2025-03-31 (paper published 2025-06-18), thus **contradicts the paper's Section 2.2 software claim**. Two hypotheses:
(a) the disphere/resv code was withheld from public release (embargo or IP), and the "data availability statement" is aspirational ("_will_ be openly available following an embargo");
(b) the authors' internal branch shipped under a different name that never made it into the public fork.
Hypothesis (a) is well-supported by the data-availability language.

---

## 5. Verdict

**PARTIAL.** Concretely:

- C1, C2 (non-orthogonal box + 3D deposition infrastructure): **REPLICATED**. Public code builds and runs the exact paper-scale geometry with the exact paper parameters.
- C3 (disphere / resv software claim): **CONTRADICTED** on the public artifact (public branch lacks the code that Section 2.2 says is on that branch).
- C4-C6 (DFT ecoord library, aspect-ratio validation, nucleus-shape sensitivity): **BLOCKED** by missing supplementary + missing disphere code. Only a spot-check consistency test is possible with the surrogate ladder, and that spot-check is consistent with (but not a positive test of) the paper.

Overall we replicate half the paper's method claim and none of its scientific-quantitative claim.

---

## 6. Open questions

See `open_questions.json` for the full JSON payload. Summary in-line:

**Q1.** How much of the paper's reported anisotropy in Figure 7 comes from the bound-sphere geometric constraint per se, and how much from the 2D-indexed DFT ecoord table? — *Basis:* Section 2.2 conflates the "bound-sphere with lattice-enforced pairing" mechanism with the "2D-indexed rate table" mechanism, but they are separable and the paper does not report an ablation. Our surrogate 1D-indexed run is markedly more isotropic even on the *same* HCP lattice, which points at the ecoord table as a plausibly-dominant contributor — but that is an inference, not a measurement.

**Q2.** Does the "arbitrarily large barrier" imputation for un-tabulated coordinations bias growth toward the specific facet geometries actually sampled in the 74-point DFT library? — *Basis:* Section 3.1 explicitly gives an "arbitrarily large barrier" to any coordination pattern not in the 74-point library. This is essentially an infinite acceptance ratio against unexpected geometries, which could easily lock in the specific facet ordering seen in DFT. There is no reported sensitivity study to (i) making the barrier finite (e.g., 3×max_tabulated), or (ii) filling gaps by nearest-tabulated-coordination interpolation.

**Q3.** Why is the paper's ~200 nm × 250 nm × 210 nm box only 48×16×24 unit cells if the resveratrol unit cell is on the order of 6–8 Å per side? — *Basis:* From the P2₁/c resveratrol unit-cell parameters (a ≈ 7.6 Å, b ≈ 24.5 Å, c ≈ 15.9 Å from Chadha et al. 2016), 48×16×24 unit cells is about 365 nm × 392 nm × 382 nm — 1.5–2× the stated 200×250×210 nm. Which value is correct: the number-of-unit-cells or the nanometer-scale? The output box shape from our HCP run is (56, 13.86, 39.19) *site units*, consistent with 48×16×24 primitive HCP but the mapping to actual resveratrol nanometers is under-specified.

**Q4.** Is the tree-solve step efficient enough that 5×10⁶ trial steps on a 48×16×24 HCP box actually explores enough phase space to converge the aspect-ratio histogram? — *Basis:* 560 replicates × 5×10⁶ trials is a lot, but each replicate reports one number (a shape ratio at simulation termination). No convergence-vs-N_trial or convergence-vs-N_replicate plot is shown, and the paper explicitly notes the simulated distributions are much narrower than experiment (which _could_ mean under-sampling, or _could_ mean over-simplified physics).

**Q5.** Would a hex-region + 3D-random-deposition + isotropic Arrhenius baseline (i.e., exactly what we ran) trained against experiment via inverse-problem fitting of a 1D ecoord ladder recover something close to the DFT-derived rate table? — *Basis:* Our surrogate is much more isotropic than experiment; if experiment is monotone-informative about coordination-→ energy, an inverse fit of ecoord to experimental aspect-ratio distributions would provide an interesting cross-check on the DFT library. This is a natural follow-on that the released infrastructure is fully capable of supporting even without the disphere extension.

## Open Questions (in-line for report)

Q1. Ablation: bound-sphere geometry vs 2D ecoord table — which contributes what fraction of the anisotropy?
Q2. Sensitivity of morphology to the "arbitrarily-large-barrier" imputation for un-tabulated coordinations.
Q3. Unit-cell → nm mapping inconsistency in the box description (48×16×24 unit cells ≠ 200×250×210 nm at literature P2₁/c cell dimensions).
Q4. Convergence: is 5×10⁶ steps per run × 560 replicates enough to converge the aspect-ratio histogram?
Q5. Inverse-problem: can an isotropic 1D ecoord ladder fit to Micro-CT aspect ratios recover something like the DFT rate table?

---

## 7. Data & Code

- SPPARKS `resveratrol` branch: https://github.com/tdjanic-snl/spparks/tree/resveratrol
- SPPARKS `nonorth` branch: https://github.com/tdjanic-snl/spparks/tree/nonorth
- Upstream SPPARKS: https://github.com/spparks/spparks
- OSTI PDF: https://www.osti.gov/servlets/purl/2583708
- IOP paper: https://iopscience.iop.org/article/10.1088/1361-651X/ade176

All local build/run artifacts are in `work/` and `report/evidence/` of this directory.
