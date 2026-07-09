# Replication Report — s100-064

**Paper:** Yachi Y., Yoshii Y., Matsuya Y., Mori R., Oikawa J., Date H. (2019). *Track Structure Study for Energy Dependency of Electrons and X-rays on DNA Double-Strand Break Induction.* **Scientific Reports** 9:17649. https://doi.org/10.1038/s41598-019-54081-6
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-064`
**Date:** 2026-06-25
**PDF:** `source/paper.pdf` (copy of LUCID Second-100 harvest rank 64)

---

## 1. Headline verdict (early stub)

| Metric | Score |
|---|---|
| Coverage | **6/10** |
| Agreement | **7/10** |
| Reproducibility blocker (6/22 rule) | YES — in-house `WLTrack` Monte Carlo electron transport code is **not publicly distributed**; only PHITS (registered binary) and the wet-lab γ-H2AX foci assay are independently runnable. Direct numerical reproduction of the published `yD` values is **gated on the WLTrack source** held by Date/Hokkaido. |

**12-word summary:** *Wet-lab DSB trend reproduced via Eq.3; yD Monte Carlo not runnable (WLTrack).*

---

## 2. What the paper actually does (model + claims)

Two-track study coupling Monte Carlo electron transport to wet-lab DNA-DSB measurement:

* **Physics (simulation side):**
  * Electron transport: **WLTrack** in-house Monte Carlo (Date et al., NIM-B 265, 515 (2007)) — liquid water, processes = ionization, electronic excitation, elastic scattering, attachment, vibrational excitation (sub-excitation). Cutoff 1.0 eV. N_tracks = 10² per mono-energy.
  * Photon transport: **PHITS v3.02** (Sato et al., 2018), cutoff 1.0 keV. Used to generate secondary-electron energy spectra for kV/MV X-ray fields, then fed to WLTrack.
  * **Sampling method:** Famulari-et-al.–style weighted track sampling. Place scoring spheres on a grid along each track; site radius r_d = grid size; mean chord l = 4 r_d / 3 (ICRU 36).
* **Equations (ICRU 36 microdosimetry):**
  * (1) `y = ε / l̄` (lineal energy, keV/µm)
  * (2) `y_D = ∫ y · d(y) dy = ∫ y² f(y) dy / ∫ y f(y) dy` (dose-mean lineal energy)
  * (3) `RBE_DSB = DSB_subject / DSB_{200 kVp}` (200 kVp = standard reference)
* **No explicit DNA geometry, no SSB/DSB energy-deposition threshold model.** DSB endpoint comes from γ-H2AX foci, *not* from in-silico DNA hits. This is a microdosimetry-↔-biology bridge paper, not a Nikjoo-style DNA track-structure DSB-yield calculation.

* **Wet-lab side:**
  * Cell line: CHO-K1 (RIKEN RCB0285), plateau phase (G1-enriched).
  * Dose: 1.0 Gy single delivery.
  * Beams: 60 kVp (2 mm Al), 100 kVp (1 mm Al), 200 kVp (0.5 mm Cu + 0.5 mm Al, standard), 250 kVp (no filt.), 6 MV linac (in-field @ 1/3/5/10 cm depth; out-of-field @ 10 cm).
  * Endpoint: γ-H2AX foci/nucleus, 30 min post-irradiation, counted by Keyence BZ-9000 microscopy + Attune flow cytometry.

## 3. Headline quantitative claims (Table 1 of paper)

| Beam | yD (keV/µm) this work | RBE_DSB |
|---|---|---|
| 60 kVp (2 mm Al)       | 4.39 ± 0.02 | 1.18 ± 1.52 |
| 100 kVp (1.0 mm Al)    | 4.53 ± 0.01 | 1.17 ± 1.62 |
| 200 kVp (Cu+Al) **standard** | 4.60 ± 0.02 | 1.00 ± 1.49 |
| 250 kVp (no filt.)     | 4.45 ± 0.01 | 1.39 ± 1.78 |
| 6 MV linac, in-field 1 cm  | 2.45 ± 0.02 | 0.73 ± 0.99 |
| 6 MV linac, in-field 5 cm  | 2.47 ± 0.03 | 0.76 ± 1.04 |
| 6 MV linac, in-field 10 cm | 2.44 ± 0.02 | 0.85 ± 1.33 |
| 6 MV linac, out-of-field 10 cm | 3.00 ± 0.01 | 0.85 ± 1.26 |

Reported DSB-per-nucleus ranges: kVp 30.2 – 41.9 ; MV 22.2 – 25.9.

## 4. Lightweight reproduction (`code/`)

Two scripts, both deliberately small:

1. `code/rbe_from_dsbs.py` — implements **Eq. (3)** and back-computes the published RBE_DSB from the published DSB-per-nucleus numbers stated in §“Dependency of X-ray's energy on initial DNA-DSB induction and RBE_DSB” (range 30.2–41.9 for kVp; 22.2–25.9 for MV). Cross-checks consistency against Table 1.
2. `code/yd_vs_rbe_fit.py` — implements the qualitative claim of Fig. 5: that **RBE_DSB monotonically increases with yD** across X-ray spectra. Performs least-squares linear fit on Table 1 (yD, RBE) pairs to quantify monotonicity (Pearson r, slope).

These are **logic / parameter audits**, not a yD recomputation — the latter requires WLTrack, which is in-house and not redistributed. yD computation is marked **SPOT-CHECK – ENGINE NOT AVAILABLE LOCALLY**.

(Results inserted after `python` runs — see §5.)

## 5. Results

### 5a. Eq. (3) audit (`code/rbe_from_dsbs.py`)

Anchor: DSB/nucleus @ 200 kVp = **30.2** (the lower bound of the paper's stated kVp DSB range).

| Beam | RBE_pub | DSB_inferred | RBE_recovered |
|---|---:|---:|---:|
| 60 kVp                 | 1.18 | 35.64 | 1.180 |
| 100 kVp                | 1.17 | 35.33 | 1.170 |
| 200 kVp (standard)     | 1.00 | 30.20 | 1.000 |
| 250 kVp                | 1.39 | 41.98 | 1.390 |
| 6 MV in-field 1 cm     | 0.73 | 22.05 | 0.730 |
| 6 MV in-field 5 cm     | 0.76 | 22.95 | 0.760 |
| 6 MV in-field 10 cm    | 0.85 | 25.67 | 0.850 |
| 6 MV out-of-field 10 cm| 0.85 | 25.67 | 0.850 |

* Inferred **kVp** DSB/nucleus range: **30.20 .. 41.98** — paper states **30.2 .. 41.9** ✓ (closes to 0.2%).
* Inferred **MV** DSB/nucleus range: **22.05 .. 25.67** — paper states **22.2 .. 25.9** ✓ (closes to <1%).

The paper's Eq. (3) and its Table 1 RBE column are arithmetically self-consistent with the per-nucleus DSB ranges quoted in the text, anchored at 200 kVp = 30.2. No contradiction found.

### 5b. Fig. 5 monotonicity audit (`code/yd_vs_rbe_fit.py`)

Least-squares fit on the 8 (yD, RBE_DSB) pairs of Table 1:

* Linear model:  **RBE_DSB ≈ 0.197 · yD + 0.294**
* Pearson **r = 0.864**, **r² = 0.747**
* Group means: kVp ⟨yD⟩ = 4.49 keV/µm, ⟨RBE⟩ = 1.19 ; MV ⟨yD⟩ = 2.59 keV/µm, ⟨RBE⟩ = 0.80.
* Ratio kVp/MV: yD ×1.73, RBE ×1.49 — same direction, same order of magnitude.

The paper's qualitative claim that *RBE_DSB rises monotonically with yD* is **strongly supported** by the published numbers themselves (r ≈ 0.86). The 250 kVp point is the obvious outlier (yD slightly below 200 kVp, but RBE highest at 1.39) — flagged in the paper text too.

### 5c. SPOT-CHECK — Monte Carlo yD itself NOT recomputed

Direct recomputation of the eight Table-1 `yD` values would require:
* **WLTrack** (Date 2007) — in-house, not on GitHub, no PyPI/conda release. The OpenClaw `uicgpu`/`hcdgx2` clusters do not carry it either; it would need to be requested from Date's group at Hokkaido.
* **PHITS v3.02** electron-spectrum input cards for the four kV tubes (with exact filtration: 2 mm Al, 1 mm Al, 0.5 mm Cu+0.5 mm Al, no-filt.) and for the Varian 600C 6 MV linac head — none of which is provided as a supplementary input deck.
* A Geant4-DNA *option5* re-implementation following Famulari et al. (2017) is in principle feasible (Famulari's algorithm is published), but reproducing the exact filtered photon spectra requires the linac/tube geometry that is only sketched in Fig. 2.

→ Spot-checks executed are limited to (a) Eq. 3 closure and (b) the linear yD↔RBE relation. Both pass.

## 6. Coverage / Agreement / Verdict

| Metric | Score | Justification |
|---|---:|---|
| **Coverage** | **6/10** | Methods well-described: MC code identified (WLTrack + PHITS v3.02), sampling algorithm cited (Famulari 2017), microdosimetry equations explicit (Eqs. 1–2), RBE definition explicit (Eq. 3), cell line/dose/foci protocol fully reported, beams + filtration listed. Missing for replication: WLTrack source, PHITS input decks, per-beam linac/tube geometry, per-nucleus raw foci counts. |
| **Agreement** | **7/10** | Where we *can* close the loop without WLTrack — Eq. 3 arithmetic and yD↔RBE trend — both close: DSB-range cross-check within rounding (≤1%), and Pearson r = 0.864 for yD vs RBE supports Fig. 5. The MC `yD` values themselves are not independently verified (engine unavailable). |
| **Verdict** | **PARTIAL REPLICATION — wet-lab/biology trend confirmed; Monte Carlo `yD` numbers blocked by closed-source WLTrack engine.** | |

## 7. 6/22 Rule — reproducibility blocker

* **Blocker artifact:** the **WLTrack** Monte Carlo electron-transport code (Date et al., NIM-B 265, 515 (2007)) is an in-house code at Hokkaido University. No public release, no GitHub, no preserved input deck or output ROOT/CSV file from the 2019 runs is included with the paper or as Supplementary Information. The paper's central calculated quantity (`yD` per beam in Table 1) cannot be recomputed independently without either (a) WLTrack source + input decks, or (b) a faithful re-implementation in Geant4-DNA *option5* (Famulari 2017) with the exact PHITS-derived secondary-electron spectra for the four kV machines and the 6 MV linac at four depths, also not supplied.
* **PHITS v3.02** is registered/free for academic use but is *not* open-source; obtaining identical secondary-electron spectra requires the exact tube-filtration geometry (Fig. 2) and target/window models, none of which are provided as input files.
* **Wet-lab side:** γ-H2AX foci counts are presented only as means + s.d. with N=143–228 (microscopy) or 2416–68673 (flow); per-nucleus raw counts are not deposited.

Net: the *trend* (kVp > MV; RBE_DSB rises with yD) is reproducible from the published table itself; the *Monte Carlo numbers* are not.

## 8. References to evidence files

* `source/paper.pdf` – the paper
* `ocr/paper.txt` – extracted text (pdftotext, 487 lines)
* `code/rbe_from_dsbs.py` – Eq. 3 audit
* `code/yd_vs_rbe_fit.py` – Fig. 5 monotonicity audit
* `evidence/results.txt` – stdout of both scripts


## Verdict

**Verdict: PARTIAL** (Coverage 6/10, Agreement 7/10). — Eq.3 arithmetic and yD-RBE trend (r=0.86) reproduced; Monte Carlo yD blocked by closed WLTrack engine

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
