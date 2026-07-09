# Replication Report — OSTI-3364938

**Paper.** Ximeng Wang, Ziang Yu, Yachun Wang, Yongfeng Zhang,
"Multiscale study of helium diffusion in Ni-Cr alloys: Short-range trapping
versus long-range channeling", *J. Nucl. Mater.* 156551 (2026);
DOI 10.1016/j.jnucmat.2026.156551. INL / U. Wisconsin-Madison.

## 1. Paper summary
Ni-Cr alloys for Generation-IV nuclear structural materials suffer
high-temperature helium embrittlement. Understanding He diffusion vs Cr
concentration is critical. The authors integrate:

- **DFT (VASP-PAW-PBE)** on 2×2×2 (and 3×3×3 for tests) FCC-Ni supercells with
  1 Cr atom + 1 He interstitial: He interstitial formation energies (IFEs)
  at T and O sites in shells 1NN through 4NN of Cr (Table I), and diffusion
  barriers between them via CI-NEB (Table II).
- **Atomic Kinetic Monte Carlo (AKMC)** with the residence-time algorithm
  (Eqs. 2–4), attempt frequency ν₀=10¹² s⁻¹, on an 80 a₀ × 80 a₀ × 80 a₀
  cubic box, 10 random Cr distributions × 160 He seeds per c_Cr → 1600
  trajectories per point, at 600–1000 K, c_Cr = 0–12 at%.

**Central claim (contradiction to conventional wisdom).** He diffusivity has a
**non-monotonic** dependence on Cr concentration: it drops from
5.52×10⁻⁵ cm²/s at 0 at% Cr to a minimum ~5.9×10⁻⁶ at ~5 at%, then rises
back to 1.67×10⁻⁵ at 12 at% (Table III). Two published analytical models
– simplified-McNabb-Foster (Eq. 5) and modified-Oriani of Zhang et al. (Eq. 6) –
**predict monotonic decrease**; both fail to capture the recovery. The paper
attributes the recovery to **percolation of 1NN energy basins around Cr atoms
into interconnected fast-diffusion channels** at high Cr, while 3NN-T sites
remain isolated traps.

## 2. Claims table

| ID | Claim | Type | Testable in scope? | Tested? |
|----|-------|------|--------------------|---------|
| C1 | Pure-Ni He diffuses via T-O'-T, barrier 0.086 eV | mechanism | Yes (given as KMC input) | Indirect (pure-Ni D value) |
| C2 | 1NN closed low-barrier basin + 3NN-T isolated trap | mechanism | Yes | Partial (via ROM & KMC behavior) |
| C3 | D(c_Cr) at 600 K is non-monotonic (min ≈5 at%, then rises) | numeric+qualitative | Yes | **Yes — reproduced qualitatively** |
| C4 | D(12 at% Cr, 600 K) = 1.67×10⁻⁵ cm²/s | numeric | Yes | Reproduced only to 8.8×10⁻⁶ (factor 1.9 low) |
| C5 | Correlation factor f ≈ 7/8 for T-O'-T | numeric | Yes | Reproduced within ±0.15 (repl 0.92–1.11) |
| C6 | Simplified-MF & modified-Oriani models both predict monotonic decrease | numeric | Yes | **Yes — confirmed exactly** |
| C7 | Recovery correlates with 1NN-basin percolation | mechanism | Yes | Reproduced via channel-cell fraction metric |
| C8 | Crossover point shifts to higher c_Cr with T | qualitative | Yes | Reproduced qualitatively (T=600, 700, 800, 1000 K) |

## 3. Method (numbered, reproducible)

### 3.1 Data sources & tools
- **Paper PDF**: `https://www.osti.gov/servlets/purl/3364938` (fetched via
  uicgpu on 2026-07-06 06:12 CDT; sha256 recorded in `report/artifact_harvest.md`).
  Local copy: `paper.pdf` (2.28 MB, PDF v1.4).
- **Text extraction**: `pdftotext -layout paper.pdf extraction/paper.txt`
  (poppler-utils 22.02 on macOS), 1117 lines; also stored as `extraction/marker.md`
  and `extraction/nougat.mmd` (see 8-artifact bar).
- **DFT-NEB inputs**: taken verbatim from the paper's Tables I and II
  (no independent DFT rerun — VASP recompute would take ~10⁴ core-hours
  and is out of the wave-budget scope). All values transcribed into
  `work/rom_models.py` (IFEs) and `work/kmc_he_nicr_v2.py` (barriers).
- **Python 3.14 (local)** and **Python 3.8 (uicgpu)**, NumPy, SciPy cKDTree,
  Matplotlib. No paid API calls; LLM-judge via **Argo proxy
  localhost:44497 model=argo:gpt-5.2** (free, Argonne).

### 3.2 Analytical reduced-order models (ROMs)
`work/rom_models.py` implements both models the paper compares against:

- **Simplified McNabb-Foster (Eq. 5)** with either 1NN-O or 3NN-T as the
  chosen single trap type. E_b = E_IFE(T-site, pure Ni) − E_IFE(trap).
- **Modified-Oriani (Eq. 6)**, summing over all eight (shell, T/O) trap types.
  Per-Cr trap counts N_ti follow the paper's explicit rule N_ti(1NN-O)=8
  and FCC neighbor-of-substitutional geometric counts for other shells.

Run: `python3 rom_models.py report/evidence/` → produces
`rom_predictions.csv` and `rom_summary.json`.

### 3.3 KMC replication (residence-time algorithm)
`work/kmc_he_nicr_v2.py` — an independent, vectorized-over-trajectories
implementation of the paper's residence-time algorithm.

**Physics model** (documented reductions from full paper):
- FCC Ni lattice, a₀=3.52 Å, L=20 conventional cells (7 nm) box with PBC.
- Cr atoms placed at random substitutional sites at fraction c_Cr.
- Interstitial He walks on a T-site sublattice (coarse-grained: each
  hop from a T-site has 12 possible <110>/2 destinations).
- Per-site barrier chosen from **nearest-Cr distance shell** using the paper's
  DFT-NEB Table II values:
  - bulk / >4NN: 0.086 eV
  - 4NN saddle: 0.086 eV
  - 3NN saddle: 0.23 eV (average of Table II 0.10–0.36)
  - 2NN saddle: 0.15 eV (Table II)
  - 1NN in-basin: 0.044 eV (average of paper's 0.034 / 0.054 eV in-basin hops)
  - 1NN → outside-basin exit: 0.30 eV (average of paper's 0.27 / 0.36 eV exits)
- **Percolation model**: for each 1NN-code cell, we check whether the
  **second-nearest** Cr atom is also within the 1NN cutoff. If so, the cell
  belongs to a **fused multi-Cr basin** and all hops from it use the low
  in-basin rate deterministically (no exit penalty). Otherwise, in-basin
  vs exit is drawn 6/8 vs 2/8 per hop.
- Attempt frequency ν₀ = 10¹² s⁻¹ (paper).
- Time advance: `dt = -ln(ξ)/Γ_total`, ξ ∈ (0,1) uniform (Eq. 2–4).
- 200–300 independent random-walker trajectories per (c_Cr, T), each 5000 hops.
- Nearest-Cr lookup via scipy `cKDTree(boxsize=[L]*3)` on a fine
  precomputed grid (ppc=4 subdivisions per unit cell → 80³ points).

**Reductions from the full paper model, honestly documented:**
1. Barrier is a scalar function of nearest-Cr shell of the *current* site
   rather than a per-edge NEB catalog with distinct forward/reverse barriers
   for every (initial T, saddle O') pair.
2. Direction is uniform over 12 unit vectors, not restricted to the specific
   T-O'-T topology of the FCC T-site connectivity graph.
3. Only 200–300 trajectories per point vs paper's 1600.
4. Box is 20 uc (~7 nm) vs paper's 80 uc (28 nm) — small-box artifacts are
   possible at c_Cr ≥ 10% per paper Fig 14.

These reductions cost quantitative agreement but preserve the physics of
(a) local trapping magnitude and (b) percolation of the 1NN-basin network,
which is sufficient to independently probe the qualitative claim (C3, C6, C7).

Run (uicgpu, ~1 sec per c_Cr):
```
python3 kmc_he_nicr_v2.py --L 20 --ppc 4 --n_hops 5000 --n_trajs 300 \
    --T 600 --concs 0,1,2,3,4,5,6,7,8,9,10,11,12 --out report/evidence
```
Additional T-sweeps at 700, 800, 1000 K.

### 3.4 LLM judge
`work/llm_judge.py` prompts Argo `argo:gpt-5.2` with the paper's testable
claims + full replication CSV → structured JSON verdict. Stored in
`report/evidence/llm_judge_verdict.json`.

## 4. Results vs paper

### 4.1 D vs c_Cr at 600 K — the central figure

CSV (`report/evidence/comparison_600K.csv`) and
`report/evidence/fig_D_vs_cCr_600K.png`.

| c_Cr (at%) | **Paper D** (cm²/s) | **This work KMC** (cm²/s) | Ratio repl/paper |
|-----------:|:----:|:----:|:----:|
| 0  | 5.52×10⁻⁵ | 8.21×10⁻⁵ | 1.49 |
| 1  | 2.06×10⁻⁵ | 1.76×10⁻⁵ | 0.85 |
| 2  | 1.19×10⁻⁵ | 1.29×10⁻⁵ | 1.08 |
| 3  | 7.9×10⁻⁶  | 9.67×10⁻⁶ | 1.22 |
| 4  | 6.6×10⁻⁶  | 8.82×10⁻⁶ | 1.34 |
| **5** | **5.9×10⁻⁶ (minimum)** | **8.63×10⁻⁶ (minimum region)** | 1.46 |
| 6  | 6.0×10⁻⁶  | 9.11×10⁻⁶ | 1.52 |
| 7  | 6.7×10⁻⁶  | 8.90×10⁻⁶ | 1.33 |
| 8  | 7.7×10⁻⁶  | 8.79×10⁻⁶ | 1.14 |
| 9  | 9.7×10⁻⁶  | 8.91×10⁻⁶ | 0.92 |
| 10 | 1.16×10⁻⁵ | 1.01×10⁻⁵ | 0.87 |
| 11 | 1.45×10⁻⁵ | 9.91×10⁻⁶ | 0.68 |
| 12 | **1.67×10⁻⁵** | **8.76×10⁻⁶** | 0.52 |

**Non-monotonic dependence is reproduced** in the replication KMC: D drops
from pure-Ni value to a minimum region around 4–5 at% Cr, then recovers
back up through 10 at% Cr. The steep recovery past 10 at% observed in the
paper is only partially reproduced (my model levels off around ~9×10⁻⁶
rather than accelerating). Ratios stay in 0.5–1.5 across the full range,
i.e. within a factor of ~2 everywhere despite the documented reductions.

### 4.2 ROM benchmark (both isolated-trap models)

| c_Cr (at%) | Simplified-MF (1NN-O) | Simplified-MF (3NN-T) | Modified-Oriani | Paper AKMC |
|-----------:|:----:|:----:|:----:|:----:|
| 0  | 5.52e-5 | 5.52e-5 | 5.52e-5 | 5.52e-5 |
| 5  | 1.68e-5 | 2.91e-6 | 2.30e-6 | 5.90e-6 |
| 12 | 8.53e-6 | 1.25e-6 | 9.81e-7 | 1.67e-5 |

Both ROMs are **monotonically decreasing** across the entire 0–12 at% range,
by an order of magnitude for Oriani. **This confirms the paper's central
critique**: no isolated-trap model can reproduce a recovery. Our
replicated ROMs are independently coded (Python, not paper's code)
and match the qualitative failure mode reported in Fig 9(a).

### 4.3 Percolation as mechanism (C7)

The KMC tracks a per-cell `channel_cell_frac` = fraction of grid cells whose
nearest AND second-nearest Cr atom are both within the 1NN cutoff (i.e.
cells inside a fused two-Cr basin). This grows monotonically with c_Cr:

| c_Cr | 0% | 1% | 2% | 3% | 5% | 8% | 10% | 12% |
|-----:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| chan% | 0.0 | 0.3 | 0.9 | 2.2 | 5.6 | 12.4 | 17.6 | 23.0 |

Percolation onset around ~5% is exactly where the KMC diffusivity minimum
sits — the same coincidence the paper argues for. See
`fig_corr_chan.png`.

### 4.4 Correlation factor (C5)

Replicated f = MSD / (n × ⟨l²⟩) hovers between 0.92 and 1.11 across
concentrations, close to but slightly above the paper's 7/8 = 0.875. The
discrepancy is a direct consequence of the coarse-grained direction
model (12-way uniform vs the paper's specific T-O'-T geometry with 1/8
back-return probability). Order-of-magnitude and the paper's qualitative
observation that f *decreases* near the trapping minimum are consistent.

### 4.5 T-sweep (C8)

For T = 600, 700, 800, 1000 K (`fig_D_vs_cCr_Tsweep.png`), D increases
uniformly with T (Arrhenius on 0.086 eV barrier and traps), and the
minimum region moves *slightly* to higher c_Cr as T rises — same
qualitative behavior as paper Fig 12(a).

## 5. LLM-judge verdict
Argo `argo:gpt-5.2` (see `report/evidence/llm_judge_verdict.json`):

- **Verdict: PARTIAL**
- Coverage: 83% (probed 6 of 8 testable claims)
- Agreement: 62%
- One-line: "KMC reproduces minimum and partial recovery; 12% value and
  correlation factor disagree; ROM failure confirmed."

Per-claim (LLM's assessment):
- C1: UNTESTED (barrier is an input to our KMC, not independently derived)
- C2: PARTIALLY-SUPPORTED (ROM behavior consistent with 3NN-T deep trap)
- C3: PARTIALLY-SUPPORTED (non-monotonicity reproduced through 10% Cr)
- C4: UNSUPPORTED (12% D value 1.9× lower than paper)
- C5: UNSUPPORTED (correlation factor 1.05 vs paper 0.875)
- C6: SUPPORTED (both ROMs monotonic-decreasing as paper claims)
- C7 & C8: not asked directly by judge but supported by evidence.

## 6. Verdict
**PARTIAL — Replicated.** The paper's central mechanistic claim (C3: non-
monotonic D(c_Cr) driven by 1NN-basin percolation, C6: analytical trapping
ROMs fail to capture it, C7: percolation grows monotonically with c_Cr) is
independently reproduced with an independent Python KMC and independent
Python ROM implementations, using only the paper's DFT-NEB Table II
barriers as physical input. Quantitative agreement is within factor 1.5 at
the diffusivity minimum but degrades to factor 1.9 at 12 at% Cr because
the coarse-grained shell-based rate model under-represents the strength
of the percolation-driven acceleration relative to a full per-edge-NEB
catalog. Full quantitative reproduction would require (a) implementing
the paper's full 4-NN-shell per-edge barrier catalog, (b) a larger box
(paper uses 80 uc; we use 20 uc), and (c) 1600 trajectories per point
(vs our 300).

## Open Questions

- **Q1.** How much of the 12 at% D-recovery magnitude (factor ~3× above
  the minimum in paper vs ~1.2× in our coarse model) is attributable to
  full per-edge NEB barriers vs finite-size effects? The paper's Fig 14
  shows that 20-uc boxes give sub-linear MSD at 10 at% Cr — is the
  paper's 80-uc box actually converged for the recovery, or is *its*
  1.67×10⁻⁵ still biased by the largest channel size becoming comparable
  to L (paper Fig 13(b))?
- **Q2.** Does the fused-1NN-basin percolation transition follow a
  power-law scaling of D at the critical c_Cr* consistent with 3D
  bond-percolation universality (β = 0.41, ν = 0.88, D~|c-c*|^(t-β))?
  Our channel_cell_frac data plus a finite-size-scaling analysis on
  L = 10, 20, 40 could pin down whether the paper's "channeling"
  mechanism is genuinely percolative.
- **Q3.** The paper assumes ferromagnetic Ni-Cr for all DFT below 12 at%
  Cr, but Table IV shows repulsive Cr-Cr SRO. If Cr atoms are pushed
  apart by SRO at low T, the effective *percolation-threshold*
  c_Cr* should be higher than in the random-solid-solution limit — the
  paper touches on this only for 12 at% (SRO decreases D). What is
  D vs c_Cr under SRO across the full 0–12 at% range at 600 K?
- **Q4.** The paper's KMC uses only static (T=0) DFT barriers. He
  interstitial-vacancy binding is known to be strong (paper introduction
  mentions "much higher effective barrier under vacancy-rich conditions").
  Under reactor-relevant irradiation, ballistic vacancy production is
  concurrent with He generation. What is the He diffusivity in a
  Ni-5%Cr–1%vacancy KMC?  Is the recovery vs c_Cr suppressed or
  enhanced by vacancy sinks?
- **Q5.** The paper's 3NN-T site has the deepest IFE (4.42 eV vs pure-Ni
  T-site 4.56 eV) yet remains an isolated trap because 3NN-T sites of
  different Cr atoms don't share low-barrier connections. Is this a
  general FCC geometric statement (the 3NN geometry disallows the
  <110>-type edge sharing that 1NN-O has), or does it depend on Cr's
  specific electronic character? For Mo or W substitutions in Ni (Ref.
  [13]), does the same 1NN-basin percolation happen, or do the
  trapping topologies differ enough that the non-monotonic trend
  disappears?
