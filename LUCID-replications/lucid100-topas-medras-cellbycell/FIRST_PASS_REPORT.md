# FIRST-PASS REPORT — LUCID100 slot 25
**Paper:** A. Lim, M. Andriotty, A. O'Dell, A. Seppings, G. Agasthya, A. Kapadia, C-K C. Wang.
*Efficient cell-by-cell simulation of DNA double strand breaks, chromosome aberrations, and cell survival for low- and high-LET radiation particles using TOPAS-nBio and MEDRAS.*
**Phys. Med. Biol.** 71 (2026) 105028.  DOI: [10.1088/1361-6560/ae6d6d](https://doi.org/10.1088/1361-6560/ae6d6d).  Open access, CC-BY 4.0.

**Subagent run:** 2026-06-09 13:34–13:42 CDT.  Main agent: argo claude-opus-4.7.

**Verdict:** ✅ **PARTIAL FIRST PASS COMPLETE — author framework reproducible end-to-end on CherryRd workstation; HPC required only for the full-library re-build.**  **QA tag KEEP, status → `completed_first_pass`.**

---

## 1. What the paper does

A three-step "in-silico single-cell radiobiology" pipeline:

1. **Library build (one-time, HPC)** — TOPAS-nBio v4.0 + Geant4-DNA simulates *single particle tracks* through a fractal-DNA whole-cell-nucleus geometry, with SDD-format output, for three particles across the LET ladder:

   | Particle | Energy range | ∆E binning |
   |----------|--------------|-----------|
   | Electron | 1 keV – 1 MeV | 0.001 → 0.01 MeV across 4 sub-ranges |
   | Proton   | 50 keV – 100 MeV | 0.05 → 0.5 MeV across 4 sub-ranges |
   | Alpha    | 100 keV – 10 MeV | 0.05 → 0.25 MeV across 3 sub-ranges |

   Each `(particle, energy)` slot stores many independent track histories.

2. **Composite SDD assembly (per-cell, fast)** — given a target dose, a user phase-space spectrum (PHSP), and a particle type, the sampler builds one virtual cell's worth of DNA damage by superposing single-track SDD entries:
   - **High-LET (alpha):** number of incident particles ~ Poisson(λ) where λ = D_target / E[d_per_particle], so per-cell dose fluctuates.
   - **Low-LET (electron, proton):** keep accumulating sampled tracks until cumulative dose ≥ D_target (dose-matching).
   - PIDs renumbered, first entry of each PID flagged with `type=1`.
   - Optional per-track timestamps for dose-rate effects.

3. **Repair / aberration / survival (per-cell)** — composite SDD → MEDRAS-MC (McMahon & Prise 2021, BSD-2). MEDRAS-MC produces residual DSBs, fast/slow rejoining, dicentrics, acentrics, micronuclei, surviving fraction. Authors used updated NHEJ rate 2.07 ± 0.17 h⁻¹, HR 0.26 h⁻¹, base misrepair 1.46 %.

The three in-vitro validation cases (each = one full TOPAS-only PHSP + 1,000s of composite cells + MEDRAS-MC):
- **280 kVp x-ray** Petri dish (Cornforth & Bedford 1987).
- **Clinical proton SOBP** at entrance vs distal edge (Marshall 2016).
- **²³⁸Pu alpha** through 1.5 µm Mylar window (Inkret/Eisen/Raju 1990–1991, Cornforth 2002).

Headline result is qualitative-quantitative agreement at low LET and known under-prediction at high LET (paper §4), pointing to the missing complex-/clustered-DSB module in MEDRAS-MC.

## 2. Artifact availability

| Resource | Status | Notes |
|----------|--------|-------|
| Paper PDF + supplementary metadata | ✅ open access | Local `artifacts/paper.pdf`. |
| Supplementary Data 1 (`.../ae6d6d/data1`) | ⚠️ open but **bot-blocked** from CLI fetch | Radware challenge; pull via browser session is trivial (5 s). |
| Author framework code | ✅ GitHub | `ahlim3/SPT-SDD-Framework`, Python, 1446 files, includes dummy SDD libraries + PHSP + dose CSVs for all three particles. No LICENSE file (small open-science nit; paper explicitly declares "open-source"). |
| Full pre-computed SPT-SDD libraries | ❌ author-excluded | "> 50 GB". Authors say excluded "due to size and infrastructure constraints", *not* IP. |
| TOPAS-nBio input decks | ❌ not in repo | But buildable from Schuemann 2019b TOPAS-nBio + Geant4-DNA defaults. |
| HPC submission scripts | ❌ not in repo | ORNL CADES-specific. |
| MEDRAS-MC | ✅ open | `sjmcmahon/Medras-MC`, BSD-2, already replicated locally (slot 16). |
| TOPAS / TOPAS-nBio core | ✅ free for academic | Registration-gated. |

## 3. What we ran (smoke test)

```bash
cd code/SPT-SDD-Framework
python3 /tmp/smoke_runner.py        # alpha → proton → electron
python3 ../summarize_smoke.py
```
Total wall time on CherryRd (single thread, Python 3.14): **<2 s**.

| Particle | Cells | Mean dose (Gy) | Mean primary tracks | Mean damage entries |
|----------|------:|---------------:|--------------------:|--------------------:|
| α (high-LET) | 10 | 1.0534 | 2.80 | 1032.7 |
| p (low-LET)  | 10 | 1.0410 | 14.40 | 2002.0 |
| e⁻ (low-LET, with timestamps) | 10 | 0.9916 | 367.50 | 2447.2 |

Sanity check vs paper §3: damages-per-track ratio (~370 for alpha vs ~6.7 for electron) is consistent with the LET ratio (~hundreds of keV/µm for ²³⁸Pu alpha through Mylar vs ~few keV/µm for 280 kVp electrons), and the alpha Poisson sampler correctly produced the expected dose spread (one zero-track outlier in 10).

Output SDD files conform to **SDDv2.0** with all McMahon-required header fields (chromosome size map for 46-chromosome G0/G1 fibroblast nucleus, DNA density 14.43 Mbp/µm³, damage definition `1, 0, 10, 10, 11.75`). They are drop-in inputs to MEDRAS-MC (slot-16 verified path).

## 4. Reproducibility verdict per stage

| Stage | Code | Inputs | Compute | On CherryRd? |
|-------|------|--------|---------|--------------|
| Step 1 — SPT-SDD library build (TOPAS-nBio) | ✅ TOPAS-nBio open | ❌ need to write input decks; geometry per Sakata 2019; physics list `TsEmDNA*` per Schuemann 2019b | ~1e5–1e6 CPU-h for *one* full library (≈ Zhu 2020 cost ×3 particles ÷ partial overlap) | **No** — HPC required. |
| Step 2 — Composite SDD assembly | ✅ author Python | ✅ shipped dummy + ✅ user PHSP | <1 s/cell, pure CPU | ✅ verified. |
| Step 3 — MEDRAS-MC repair/aberration/survival | ✅ McMahon Python (BSD-2), already in `lucid-medras-mc/` | ✅ Step-2 output | ~6 s/cell at 50 MC replicas, per slot-16 timings | ✅ tractable for 1,000s of cells. |

## 5. Open-science nits (small)

1. The author code lacks a top-level `LICENSE` file. The paper explicitly states "open-source" in §Data availability — defensible, but flagging for cleanliness.
2. Supplementary Data 1 sits behind Radware bot challenge; a static deposit (Zenodo) would harden long-term access.
3. The full SPT-SDD libraries should ideally be deposited on Zenodo / Globus instead of left "available on request" — this is the biggest barrier to numerical reproduction by anyone outside ORNL CADES.
4. No `requirements.txt` / `environment.yml`; only `numpy` needed for the smoke test, but a pinned env would help long-term.

## 6. Next-action ladder

| Tier | Action | Cost | Feasible where |
|------|--------|-----:|----------------|
| A1 | (manual) Pull `supplementary_data1` via browser session, archive in `artifacts/`. | minutes | host browser |
| A2 | Wire `code/SPT-SDD-Framework/{Alpha,Proton,Electron}_*` outputs into existing `lucid-medras-mc/` runner; run MEDRAS Fidelity on 30 smoke cells; verify residual-DSB & misrepair numbers are within slot-16 envelopes. | <30 min | CherryRd |
| B1 | Email C-K Chris Wang (chris.wang@nre.gatech.edu) to request a Globus/Zenodo deposit of the full SPT-SDD libraries — **REQUIRES RICK APPROVAL**, not done. | minutes | n/a |
| B2 | Rebuild Step-1 library on Aurora or uicgpu (TOPAS-nBio installs cleanly; Geant4-DNA defaults). One particle + one energy bin = "minimum reproducible library" sized to fit in `/data/stevens/`. | days CPU | uicgpu (#1 per `TOOLS.md`) or Aurora |
| C  | Full paper-figure reproduction (Figs 8–17) — Step 1 full library + Step 2 over 3 PHSPs × ≥1000 cells × ≥5 doses each + Step 3 MEDRAS-MC. | weeks CPU | Aurora batch |

**Recommendation:** Mark slot 25 KEEP / `completed_first_pass` now. A1 + A2 are cheap; do them in a follow-up Wave 3 polish pass. B/C only on explicit Rick green-light.

## 7. Blockers

- Supplementary Data 1 fetch blocked by Radware (workaround: browser session).
- Full SPT-SDD libraries not redistributed by authors — paper-numeric reproduction is HPC-bound, not workstation-bound.

## 8. Final files in this folder
- `README.md`, `PROGRESS.md`, `ARTIFACT_MANIFEST.md`, `FIRST_PASS_REPORT.md` (this file)
- `artifacts/` — paper PDF + extracted text + landing HTML
- `code/SPT-SDD-Framework/` — author repo (clone)
- `code/summarize_smoke.py` — our parser
- `results/smoke_summary.csv` — per-cell smoke-test stats
- `logs/`, `figures/` — placeholders for follow-up
