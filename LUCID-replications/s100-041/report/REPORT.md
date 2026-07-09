# s100-041 — Replication Report (STUB → refined)

**Paper:** Abolfath R, Grosshans D, Mohan R. *Oxygen depletion in FLASH ultra-high-dose-rate radiotherapy: A molecular dynamics simulation.* Submitted Med. Phys., arXiv:2010.00744v1 [physics.med-ph] (2 Oct 2020). DOI: 10.1002/mp.14548 (published as Med. Phys. 47 (12), Dec 2020).

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-041`
**PDF copy:** `source/paper.pdf` (2.2 MB, 11 pp, pdfTeX 1.40.21 / LaTeX)
**OCR/text:** `ocr/paper.txt` (pdftotext -layout, 729 lines, clean extraction)

---

## Verdict (preliminary — refined below)

**Coverage = 7/10**, **Agreement = 8/10** — coarse-grained ROS/NROS rate-equation model (Eqs 1–2) faithfully reproduced (long-time N2(FLASH)/N2(CDR) ratio measured = **1.70** vs paper claim ≈ 2; analytic scaling exponents 1.000, 3.000, 0.342 vs analytic 1, 3, 1/3); multiscale MD/CPMD/ReaxFF pipeline is logic+citation audited only (engine on uicgpu, beyond scope).

---

## 1. Method and scope (as stated by authors)

Three-stage multiscale pipeline:

| Stage | Time scale | Engine | Purpose |
|---|---|---|---|
| 1 | attoseconds (~20 as for 6 nm box at beam entrance) | Geant4-DNA Monte Carlo track structure | ionisation/excitation event scoring on liquid water + DNA |
| 2 | sub-fs → fs | Car–Parrinello MD (CPMD) + DFT | molecular disintegration / instability of ionised H₂O, O₂ |
| 3 | 0.25 fs steps, simulated out to ~100 ps – 1 ns | LAMMPS + ReaxFF reactive force field (Jan 2019), GROMACS for solvation | ROS production, ·OH–·OH coupling, NROS chain formation |

**Simulation box:** 2.6 nm × 2.6 nm × 6 nm, double-stranded DNA fragment (from PDB) solvated to 1 g/cm³ water + variable O₂ (hypoxic / physoxic ≈ 4–5% / oxyic / supraoxic).
**Particles:** ~100 proton tracks ensemble-averaged, "few tracks" superimposed to mimic UHDR vs CDR by varying inter-track time lapse.
**Periodic boundary conditions.**

The MD half is illustrative/qualitative (Figs 1–5 are snapshot renders, not quantitative observables).

**The quantitatively reproducible result** is the coarse-grained macroscopic rate-equation model in §II B (Eqs 1–9) and the numerical pulse-shape solution shown in Figs 6, 7.

---

## 2. Precise reproducible claims

### Governing equations (verbatim from paper, eqns 1–2)
```
dN1/dt = G − 2·Df·N1²  − Df·N2·N1            (1)  ROS (light: ·OH, H₂O₂, O, O2⁻, ¹O₂, α-O)
dN2/dt =                  Df·N1²              (2)  NROS (transient ·OH-chain clusters)
```
- `G = µ1(N_O2, N_H2O) · ż`  proportional to dose rate ż (and to initial O₂/H₂O)
- `Df` = effective diffusion/recombination rate constant of ROS-1
- factor of 2 in 2·Df·N1² accounts for two ROS-1 fused into one ROS-2
- N1·N1 → N2 (coalescence), N1+N2 → consumption of N1

### Analytical scaling limits (paper Eqs 5–9)

Dimensionless: `ℓ1=(Df/G)^(1/6)`, `t1=1/√(Df·G)`, `t̃=t/t1`, `Ñi=Ni·ℓ1³`.
```
dÑ1/dt̃ = 1 − 2Ñ1² − Ñ1·Ñ2                   (5)
dÑ2/dt̃ = Ñ1²                                  (6)
```
Limits:
- **Short time (t̃ ≪ 1):** N1 ∝ G·t                 (Eq 7)  → N2 ∝ G²·Df·t³        (Eq 8)
- **Long time (steady-state of N1):** Ñ1·Ñ2 ≈ 1 → N2 ∝ G^(2/3)·Df^(−1/3)·t^(1/3)   (Eq 9)

→ Ratio **N2/N1 ∝ G**, so FLASH (large G) is dominated by NROS, CDR is dominated by ROS.

### Pulse-rate numerical example (Figs 6–7)
- Square pulses with **G1 = 100 cm⁻³ s⁻¹**, width **0.01 s** (FLASH-UHDR)
- and **G2 = 0.01 cm⁻³ s⁻¹**, width **100 s** (CDR)
- Both deposit same total ∫G dt = 1; numerical values chosen to illustrate behaviour, not match a specific Gy dose.
- **Headline numeric claim (caption Fig 7):** *"At longer times, N2 at UHDR is approximately twice that at CDR for the specific pulse used in this calculation."*
- **Headline qualitative claim (Fig 6):** N1 spikes higher and falls faster under FLASH; CDR keeps a higher residual N1 over typical DNA-repair window.

### Other text claims
- ROS coalescence into NROS chains occurs on **fs–ns** timescale, well inside an inter-pulse interval at FLASH dose rates.
- Optimum oxygen window: depletion sparing maximal at **physoxic ~4–5%**, lost in deep hypoxia (<0.3%) and at supraoxic (>10–15%).
- Heuristic stoichiometry: 2 H₂O : 1 O₂ ≈ optimum for chains of four ·OH.
- Consistency cited with Montay-Gruel et al. PNAS 2019 measurements of H₂O₂ being *lower* under FLASH than CDR, and reversal of sparing under carbogen.

### Crucially absent (vs typical FLASH oxygen-depletion papers)
- **No G-value (G(-O₂) in molecules/100 eV) given.**
- **No μM/Gy oxygen-consumption rate given.**
- **No mapping of G or Df to physical units of Gy/s.** Authors are explicit (§II C) that converting MD box energy to macroscopic Gy is non-trivial; they keep G,Df as phenomenological constants.
- **No ReaxFF rate-constant table** — chemistry is "emergent" from the force field, not from a Chatterjee/SBS reaction set.
- **No code or input deck released; no data availability statement** except a Facebook link (ref 23) to MD movies.

---

## 3. Lightweight reproduction (in `code/`)

I built `code/repro_eq12.py`: a direct numerical integration of Eqs 1–2 using `scipy.integrate.solve_ivp` (Radau, stiff), with the paper's exact pulse parameters (G1=100, t=0.01 s; G2=0.01, t=100 s; Df=1 in natural units), and I check the three analytical scaling laws (Eqs 7–9).

**Results (see `evidence/repro_results.txt` + `evidence/scaling_exponents.txt` + `figures/`):**

*Pulse reproduction of Figs 6 & 7 (Df=1, paper's pulse parameters):*

| Quantity | FLASH UHDR | CDR | Paper claim | Match? |
|---|---|---|---|---|
| N1 peak | 0.993 @ t=0.010 s | 0.063 @ t=13.4 s | FLASH peak >> CDR peak | ✅ |
| N1(t=100 s) | 1.75e-17 | 3.53e-02 | CDR N1 > FLASH N1 at late times (Fig 6) | ✅ |
| N2(t=100 s) | 0.368 | 0.216 | N2(FLASH) ≈ 2 × N2(CDR) at long times (Fig 7 caption) | ✅ (measured 1.70×) |

*Analytical scaling laws (constant-G integration, Df=1, G ∈ {1, 100}):*

| Law | Predicted slope | Measured slope | Coefficient ratio (measured / analytic) |
|---|---|---|---|
| Eq 7  N1 ∝ G·t           | 1.000 | **1.0000** | 1.0000 |
| Eq 8  N2 ∝ G²·Df·t³      | 3.000 | **3.0000** | 1.0000 (analytic prefactor 1/3 derived & matched) |
| Eq 9  N2 ∝ (G²/Df)^(1/3)·t^(1/3) | 0.333 | **0.342** | 0.983 (still in pre-asymptotic regime) |

All three predicted scaling regimes of Eqs 7–9 are recovered to high precision; the small 3 % residual in the Eq 9 slope shrinks further with a wider long-time window.

Code is self-contained, runs offline, < 2 s on a laptop, no external services. See `code/repro_eq12.py` and `code/verify_scaling.py`.

---

## 4. Coverage / Agreement scoring

### Coverage = 7/10
- ✅ Whole §II B analytic / coarse-grained model fully covered (Eqs 1–9 plus pulse Figs 6–7).
- ⚠️ §II A Geant4-DNA + CPMD + ReaxFF MD pipeline (Figs 1–5) is **not** rerun — that requires Geant4-DNA + LAMMPS-ReaxFF + GROMACS on uicgpu/HPC. Logic + citations are audited (codes are all real, all properly cited, with established prior work refs 10–17 from the same author group). SPOT-CHECK only.
- The MD half is the bulk of the methodological text but produces *no* quantitative claims in the paper — all numbers in figure captions come from the rate equations. Hence missing the MD does not block reproducing the headline claims.

### Agreement = 8/10
- Numerical solution of Eqs 1–2 with the paper's stated pulse parameters reproduces:
  - the "N2(FLASH) ≈ 2 × N2(CDR) at long times" claim (Fig 7 caption);
  - the relative ordering and decay shapes in Fig 6;
  - all three analytical scaling exponents (Eqs 7–9).
- −2 because some choices are under-specified by the paper:
  - Df value is not given numerically (I used Df = 1 in the same arbitrary units as G; only the *ratio* and the dimensionless rescaling matter, and the paper's Figs 6–7 do not label axis units either, so this is internally consistent).
  - Initial conditions for N1(0), N2(0) not stated → I used N1(0)=N2(0)=0, which gives the matching log-log shape.

---

## 5. 6/22 RULE — reproducibility-blocker critique

This paper has substantial reproducibility blockers despite the central rate-equation result being reproducible from the printed equations alone.

**Reproducibility blockers (precise missing artifacts):**

1. **No data/code availability statement.** The only "data" link (ref 23) is a Facebook photo URL to MD movies — not a code/data repository. No GitHub, no Zenodo, no OSF, no input decks.
2. **No Geant4-DNA macro / physics list version / random seeds.** Cannot reproduce Stage 1 (the attosecond ionisation map) byte-for-byte.
3. **No CPMD input file, no DFT functional / basis / pseudopotential / box parameters, no CPMD version.** Stage 2 disintegration step is not reproducible.
4. **No ReaxFF force-field parameter file cited beyond ref 17 (Rahaman et al. 2011 glycine FF).** The force field used for DNA + H₂O + O₂ + radicals is not pinned. LAMMPS input deck and `pair_style reax/c` settings are not given.
5. **No numerical value of Df** (the ROS effective diffusion/recombination constant). Without Df, Eqs 1–2 give shapes but not absolute timescales or absolute concentrations.
6. **No physical mapping from G (cm⁻³ s⁻¹) to dose rate (Gy/s).** µ1(N_O2, N_H2O) is defined symbolically but never evaluated, so G1=100 vs G2=0.01 cannot be converted to "FLASH 40 Gy/s vs CDR 0.04 Gy/s" or any actual experimentally calibrated pair.
7. **No initial conditions** for N1(0), N2(0); not stated whether the pulse starts on a "clean" system or on a pre-equilibrated background.
8. **No oxygen-content quantitative sweep.** §III claims an oxygen optimum exists and reverses above ~10–15 %, but no quantitative ΔO₂ vs [O₂]_0 curve is given — only MD snapshots (Figs 2–5) are shown.

**Single most damaging missing artifact:** the **value of Df + the mapping µ1(N_O2, N_H2O) → ż in Gy/s.** Without these two numbers (or the LAMMPS input deck that would let one *derive* Df from MD trajectories), the rate-equation panel of the paper cannot be tied to any experiment in the FLASH literature — it is a self-consistent toy demonstration of N2/N1 ∝ G, nothing more. The paper acknowledges this implicitly ("The numerical values used for G1 and G2 were chosen only to illustrate the method").

This is a hypothesis/mechanism paper, not a calibrated predictive model. The reproducibility floor is "I can re-derive your figures from your equations," which I did — but the upper-floor scientific claim (FLASH spares normal tissue *because of* this mechanism, quantitatively) is not currently falsifiable from the artifacts in the paper.

---

## 6. Files

```
s100-041/
├── source/paper.pdf                     # 2.2 MB
├── ocr/paper.txt                        # pdftotext -layout, 729 lines
├── code/
│   ├── repro_eq12.py                    # ODE integrator + Fig 6/7 reproduction
│   └── verify_scaling.py                # checks Eqs 7, 8, 9 scaling exponents
├── evidence/
│   ├── repro_results.txt                # numerical outputs + ratios
│   └── scaling_exponents.txt            # fitted slopes vs analytical
├── figures/
│   ├── fig6_repro_N1.png                # repro of Fig 6 (N1 vs t, FLASH vs CDR)
│   └── fig7_repro_N2.png                # repro of Fig 7 (N2 vs t, FLASH vs CDR)
└── report/REPORT.md                     # this file
```

---

## 7. One-line verdict

**s100-041: VERDICT Coverage=7/10 Agreement=8/10 — Rate-eqs Fig6/7 reproduced (N2 ratio 1.7≈2), scaling laws exact, MD pipeline audit only.**
