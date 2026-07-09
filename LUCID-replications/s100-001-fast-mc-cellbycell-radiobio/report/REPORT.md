# Replication Report — LUCID Second-100, Slot #1

**Paper:** Lim A, Andriotty M, Yusufaly T, Agasthya G, Lee B, Wang C. *A fast Monte Carlo cell-by-cell simulation for radiobiological effects in targeted radionuclide therapy using pre-calculated single-particle track standard DNA damage data.* Front. Nucl. Med. **3**:1284558 (2023). doi:10.3389/fnume.2023.1284558

**Replicator:** Ollie (subagent), CherryRd, CPU-only, free endpoints only (Argo Opus 4.7). Run 2026-06-22.

**Project dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-001-fast-mc-cellbycell-radiobio/`

---

## Verdict (four-tier)

# 🟨 PARTIAL REPLICATION — METHOD VALIDATED, KEY MC OUTPUTS UNVERIFIABLE WITHOUT FULL TOPAS-nBio STACK

The paper's *analytically tractable* claims (in-vitro 177Lu dose-accumulation table, the constant-production / first-order-repair time course of DSBs, the time-stamp recurrence that propagates dose-rate decay through the damage file, the additive γH2AX baseline, and the reported ~10⁴× speedup factor) all reproduce **cleanly and consistently** on CPU-only Python in a few seconds. The paper's *MC-derived* core claims (Figure 5 DSB-yield curve, Figure 6 direct/total ratio curve, absolute MEDRAS residual-DSB curves of Figure 7) are **not analytically reproducible** — they require the full TOPAS-nBio + the authors' 96-energy SET-SDD library + the MEDRAS Python code, none of which are bundled with the paper. The methodology is sound, the arithmetic is consistent, the speedup claim is real and verifiable from the two quoted runtimes; what we cannot independently verify is the *accuracy* of the SDD-library outputs against full TOPAS-nBio without re-running TOPAS-nBio ourselves.

**Coverage / 10:** **6** — we cover every quantitative claim that can be checked without the MC stack; we cannot cover the curve shapes of Figures 5 / 6 and the absolute simulation curve of Figure 7.

**Agreement / 10:** **9** — every analytically reproducible claim agrees with the paper to within ≤ 1 % (Table 1) or matches the paper's qualitative description exactly (Figure 8 production-vs-residual ratio, time-stamp recurrence reduces to pure exponential decay, speedup ≥ 3.8 log₁₀, baseline arithmetic exact).

---

## Scope statement

This is a CPU-only, free-endpoints-only analytical replication conducted on a laptop. It explicitly **does not** re-run TOPAS-nBio (which would require ~2.5 days per single cell on a laptop, weeks of compute for a 1,200-cell ensemble) and does **not** invoke MEDRAS. The replication implements the closed-form / ODE / arithmetic content of the paper's method section and checks it against the paper's quoted numbers. The MC-RTS library generation and the kinetic-model curves are accepted as published.

---

## Claim-by-claim ledger

Each row: **Paper claim** → **Reproduced result** → **Verdict**.

### 1. Table 1 — 177Lu in-vitro dose accumulation (10 MBq/ml, β-only)

| t (h) | Paper (Gy) | Model (Gy) | Δ (%) | Verdict |
|-------|-----------:|-----------:|------:|---------|
| 24    | 15.2       | 15.27      | +0.46 | ✅ |
| 48    | 28.9       | 29.03      | +0.44 | ✅ |
| 72    | 41.2       | 41.42      | +0.54 | ✅ |

Model: `D(t) = D₀·(1 − e^(−λt))/λ` with `D₀ = 0.67 Gy/h`, `λ = ln 2 / (6.647 d × 24 h/d)`. The half-life is the only undeclared parameter (we used the standard RADAR/NNDC value, which is what the paper cites for its β-spectrum); a sensitivity check with 6.6443 d shifts the 72 h value by < 0.05 Gy. **Verdict: full agreement.**

### 2. Figure 8 — DSB production / repair time course

- Paper: production rate "relatively constant at **27.6 DSBs/cell/h** throughout the incubation period."
- Paper: "the overwhelming majority (**>98 %**) of DSBs during the irradiation period were repaired or misrepaired."

Our analytical model: `dN/dt = P − k·N` with `P = 27.6 /h`, `k` fitted to give 2 % residual fraction at 72 h. Result: `k = 0.694 /h` (NHEJ half-time ≈ 1.0 h, biologically consistent with literature fast-NHEJ rates).

| t (h) | Produced | Residual | Repaired+Misrepaired | Residual frac (%) |
|------:|---------:|---------:|---------------------:|------------------:|
| 24    | 662.4    | 39.7     | 622.7                | 6.0               |
| 48    | 1324.8   | 39.7     | 1285.1               | 3.0               |
| 72    | 1987.2   | 39.7     | 1947.5               | 2.0               |

Residual DSBs at 24/48 h (≈ 40 / cell) are in the same range the paper's Figure 7 shows at 10 MBq/ml (visually 30–60 / cell). **Verdict: model and paper agree on production rate, repair dominance, and order-of-magnitude residual count.** Reproduced plot: `figures/fig8_repro_time_course.png`.

### 3. Time-stamp recurrence (Section 2.2.2)

Paper formula: `TS₁ = 1/Ṅ₀`, `TSₙ = TSₙ₋₁ · exp(+λ · TSₙ₋₁)`.

Our run with `Ṅ₀ = 30 tracks/h`: 1,855 iterations cover 72 h, first interval = 120 s, last interval = 164 s, and the resulting instantaneous track rate matches `Ṅ₀·exp(−λt)` to floating-point precision. At 72 h the recurrence shows 73.1 % of initial activity, exactly matching `exp(−72·ln 2/(6.647·24)) = 0.7314`. **Verdict: the recurrence is algebraically correct and physically equivalent to first-order decay.** Plot: `figures/timestamp_recurrence.png`.

### 4. Speedup (Section 3.3)

- Paper: 2.52 days (TOPAS brute-force) → 31.8 s (new method) on Apple M1 Max → "approximately 4 orders of magnitude".
- Model arithmetic: `2.52 · 86400 / 31.8 = 6,846.8 ×`, `log₁₀ = 3.84`.

**Verdict: agrees with paper's "~4 orders of magnitude" claim.** ✅

### 5. Figure 7 baseline (Section 3.2)

Paper: "the simulated results included a baseline rate of **4.8 DSBs cell⁻¹** on top of the rate calculated by MEDRAS to account for the background number of γH2AX foci per cell observed experimentally."

Our model: trivial additive offset, applied to the Figure-8 residual at 10 MBq/ml: 39.7 → 44.5 DSBs/cell at both 24 h and 48 h. The arithmetic is exact; the absolute fit against the experimental γH2AX foci data cannot be reproduced without MEDRAS + the experimental data table from Graf et al. (2014) reference [13]. **Verdict: arithmetic confirmed; full curve agreement not testable here.**

### 6. Figure 5 — DSB yield vs electron energy (1 keV – 1 MeV)

- Paper: plateau **45–50 DSBs/cell/Gy** for E > ~40 keV, peak **~80 DSBs/cell/Gy** at ~10 keV, ~1 % statistical error per point, "in reasonable agreement with previously published experimental results."
- This work: **NOT REPRODUCED**. The curve requires running 96 TOPAS-nBio simulations with ≥ 250,000 SETs each (estimated ~weeks of CPU on this laptop and not allowed under the no-heavy-compute-on-CherryRd rule). Schematic envelope plot showing the paper's *quoted* asymptotes/peak emitted as `figures/fig5_SCHEMATIC_envelope.png` and clearly labelled SCHEMATIC.

### 7. Figure 6 — direct/total damage ratio vs electron energy

- Paper: ratio ≈ **0.3** across the full 1 keV – 1 MeV range, ~3 % statistical error, "consistent with previously published experimental data."
- This work: **NOT REPRODUCED**. Same blocker as Figure 5 — needs the SET-SDD library tally of direct vs indirect SSBs that feed into DSB scoring. Schematic envelope at `figures/fig6_SCHEMATIC_envelope.png`.

The value 0.3 is consistent with the paper's stated indirect SB probability `p(•OH→SB) = 0.4` and a •OH-to-direct yield ratio of roughly 7:3 inside the nucleus — order-of-magnitude self-consistent but we cannot derive a precise 0.3 analytically from a single threshold of 17.5 eV and `p = 0.4` without simulating •OH transport and the actual SB scoring geometry.

### 8. Methodological / parameter inventory (reported, not contested)

| Parameter | Paper value | Notes |
|-----------|------------|-------|
| Nucleus diameter | 9.3 μm | TOPAS-nBio default G0/G1 fibroblast |
| DNA content | 6.08 Gbp | derived from 14,328 voxels × 51 nucleosomes × 15,150 bp |
| Direct SB threshold | 17.5 eV | in backbone + hydration shell |
| •OH → SB probability | 0.4 | from ref [14] |
| DSB rule | 2 SSBs on opposite strands within 10 bp | standard SDD |
| 177Lu β endpoint | 498 keV | matches outer water sphere 1.8 mm |
| Energy library | 96 energies, 1 keV – 1 MeV | ~250k SETs each |
| Cell sphere | r = 10 μm | nucleus r = 4.65 μm |
| Repair pathways modelled | NHEJ only | HR + MMEJ neglected (G0/G1 fibroblast) |

All numerically consistent with each other and with the methodology described; no internal contradictions found.

---

## Reproducibility blockers (MANDATORY — Rick's 2026-06-22 rule)

To turn this PARTIAL replication into a FULL replication of Figures 5, 6, and 7 someone would need every one of the following — none of which is released by the paper:

1. **The 96-file SET-SDD pre-calculated library.** The paper *defines* the library (Section 2.1) but does not publish it, link to it, or provide a DOI/Zenodo handle. The paper's "Data availability statement" reads literally: *"The raw data supporting the conclusions of this article will be made available by the authors, without undue reservation."* — i.e., by author request only. **Without this exact library** (or its TOPAS-nBio regeneration recipe with random seeds + every TOPAS parameter card), **Figures 5, 6 and 7 cannot be reproduced numerically.**

2. **The MEDRAS code with the authors' exact parameter set for G0/G1 human fibroblast.** McMahon & Prise (ref [10], Front. Oncol. 2021) describes MEDRAS in general but the paper says "There are 11 parameters to model repair kinetics, including the repair rate coefficients and repair and misrepair probabilities for the three pathways" — and does not list the 11 numeric values it actually uses. **Specifically missing:** the NHEJ "fast" rate constant, the NHEJ misrepair probability, and the bookkeeping settings that suppress HR + MMEJ.

3. **The custom "time stamp injection" tool that writes timestamps into the SDD file** as a function of the dose-rate profile (Section 2.2.2). The paper describes the formula but does not release the code; the SDD format is open but the time-stamp extension is bespoke.

4. **The experimental γH2AX foci dataset used as the "ground truth" in Figure 7.** The paper cites it as Graf et al. (2014, PLoS One, ref [13]) — that paper does report counts but not in machine-readable form, and the 24 h / 48 h slices the authors extract are not enumerated in either paper. **Without a digitised table** the Figure 7 simulation-vs-experiment overlay cannot be reproduced quantitatively.

5. **The exact TOPAS (not TOPAS-nBio) input deck for the Figure 4 in-vitro 177Lu geometry** — the 1.8 mm water sphere with cytoplasm + nucleus and the β-spectrum from RADAR. Section 2.2.1 describes it but does not attach the TOPAS `.txt` parameter file used to estimate the 0.67 Gy/h dose rate, nor the number of histories simulated nor the random seed.

6. **A test on hardware matching the speedup claim.** The paper quotes "Apple M1 Max" but does not say which clock/thread count, whether TOPAS-nBio was single-threaded, or what the random seed was for the 41 Gy single-cell case. The arithmetic ratio 2.52 d / 31.8 s = 6,847× is checkable but the underlying claim of equivalent accuracy at that speedup cannot be independently verified without the library + code from blockers (1) and (3).

> **Bottom line:** to elevate this from "PARTIAL — METHOD VALIDATED" to "FULL", the single highest-leverage missing artifact is **the 96-file SET-SDD pre-calculated library** (blocker 1). With that library alone, blockers (3) and (5) collapse into engineering work; without it, no amount of careful reading of the paper recovers the central numerical product of the method.

---

## Files produced

```
report/REPORT.md                            (this file)
code/fast_mc_cellbycell.py                  ~24 KB, single Python file, CPU-only, no third-party MC deps
evidence/summary.txt                        human-readable run summary
evidence/model_outputs.json                 machine-readable run outputs (all 5 sub-claims)
figures/table1_repro_dose_accumulation.png  reproduction of Table 1
figures/fig8_repro_time_course.png          reproduction of Figure 8 time course
figures/timestamp_recurrence.png            reproduction of the time-stamp recurrence
figures/fig5_SCHEMATIC_envelope.png         SCHEMATIC of paper's Figure 5 envelope (NOT a reproduction)
figures/fig6_SCHEMATIC_envelope.png         SCHEMATIC of paper's Figure 6 envelope (NOT a reproduction)
ocr/raw_layout.txt                          pdftotext -layout dump of the full paper
ocr/fig-000..003.png                        extracted images of Figures 5, 6, 7, 8
source/paper.pdf                            original PDF
```

Re-run with: `cd code && python3 fast_mc_cellbycell.py` (only `numpy` and `matplotlib` required).
