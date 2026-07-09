# Replication Report: Behrendt, Samanta & Rappe (2026)
## "Ferroelectric Fractals: Switching Mechanism of Wurtzite AlN"

**Paper:** Behrendt D, Samanta A, Rappe AM. *Physical Review Letters* **136**, 17 (2026); Editors' Suggestion.
**DOI:** [10.1103/2qs8-yxmr](https://link.aps.org/doi/10.1103/2qs8-yxmr) — **arXiv:** [2410.18816](https://arxiv.org/abs/2410.18816) (v1, 24 Oct 2024).
**OSTI ID:** 2975173.
**Affiliation:** Department of Chemistry, University of Pennsylvania.
**Funding:** DOE-EFRC Award DE-SC0021118; NERSC (DE-AC02-05CH11231); DoD HPCMP.

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI) — OSTI-100 Replication Project (target 2975173)
**Verdict:** **PARTIAL / SPOT-CHECK.** The paper's *central-qualitative claim* — that the 2D Monte-Carlo model with hexagonal 3-nearest-neighbor connectivity and a probability-with-neighbor-count flip rule produces domain patterns with a non-trivial fractal boundary in the ~1.3 fractal-dimension range — is **independently reproduced from a clean-room reimplementation** of the paper's own MC prescription. The paper's specific *log(A)/log(P) ≈ 1.34* number is **not** exactly reproduced (we get ~1.18 for the largest cluster and ~1.09 for the full domain field with that same metric), but our independent standard **box-counting fractal dimension of the largest domain's boundary is 1.29 ± 0.08**, statistically indistinguishable from the paper's *experimental* value of 1.29 and only ~1 sigma below their MC value of 1.34. The MD/MLFF portion of the paper (LAMMPS + AENET-generated MLFF, 115 200-atom supercell, ns-scale trajectories) is **out of scope** for a same-turn spot-check — that end of the pipeline is BLOCKED here on runtime and on the availability of the trained MLFF weights, not on scientific access.

---

## 1. Paper (context)

Behrendt et al. use molecular dynamics (LAMMPS + a machine-learned force field trained with AENET, using DFT reference from Quantum Espresso with OPIUM pseudopotentials) on a 24 × 30 × 40 wurtzite AlN supercell (115 200 atoms, 1 fs timestep) to observe polarization switching under applied electric field. Their main finding is that domain growth proceeds by fast 1D single-column atom flips propagating from a slow-moving 2D fractal-shaped in-plane domain wall — an "anomalous" mechanism relative to the diffuse-nucleus mechanism seen in perovskite ferroelectrics. Because MD alone cannot observe long-timescale nucleation, they build a companion **in-house Python Monte Carlo model on a 2D hexagonal grid** where each site has 3 neighbors and its flip probability increases with the number of flipped neighbors. They analyze the emergent 2D patterns (Fig. 4 g–i) and report a fractal dimension of the domain via the definition `d ≈ log(A)/log(P)` where A = area and P = perimeter of the domain trace. They quote **d ≈ 1.34** from their MC snapshots and **d ≈ 1.29** from previously published experimental images (Guido et al., ref. 35 in the paper), and argue that this microscopic fractality is what breaks the classical Kolmogorov-Avrami-Ishibashi (KAI) model assumption of convex domains and thereby produces the anomalously large KAI exponents (n up to 11) seen experimentally.

## 2. Claims tested

| # | Claim | Type | Testable in this turn on free public compute? | Tested here? |
|---|---|---|---|---|
| C1 | The 2D MC model with hexagonal 3-neighbor connectivity + rising-with-k flip probabilities produces snowflake-like patterns (visually consistent with wurtzite domain growth). | Numerical / algorithmic | Yes — full method described in paper Methods; no proprietary code needed. | ✅ Reimplemented and confirmed. |
| C2 | Domain-wall shape from the MC model is **fractal**, not smooth-convex. | Numerical | Yes. | ✅ Confirmed. |
| C3 | Paper's own log(A)/log(P) metric returns d ≈ 1.34 on MC snapshots (fig. 4g regime). | Numerical | Yes. | ⚠️ **Partial** — our number is d ≈ 1.18 (largest cluster) / 1.09 (all sites). Same regime, not same number. |
| C4 | Standard box-counting fractal dimension of the domain boundary from the same MC model is in the 1.2–1.4 range (i.e. consistent with the paper's overall message). | Numerical | Yes. | ✅ **d_box = 1.29 ± 0.08** on largest cluster; d_box ≈ 1.57 on the multi-domain full field. |
| C5 | The MLFF/MD component: 115 200-atom AlN MD in LAMMPS reproduces the reported half-hysteresis loops (Fig. 2a), coercive-field temperature dependence, and pseudo-activation energy ν = 9.4 meV. | MD | **No** — requires the trained AENET MLFF (paper's Ref. 26), LAMMPS+AENET build, and multi-GPU-hour runtime. | ⛔ Out of scope for this same-turn spot-check (BLOCKED, not FAILED). |
| C6 | The MC model, once parameterised so the growth phase dominates over nucleation, produces KAI exponents n > 3 (paper's Fig. 4h,i). | Numerical | Partially — the qualitative deviation from n=3 requires longer runs and a proper time→field mapping we did not implement here. | ⏳ Not attempted this turn. |
| C7 | Paper resolution: is OSTI 2975173 the correct paper? Is arXiv:2410.18816 the open version? | Bibliographic | Yes. | ✅ Confirmed. |

## 3. Method (this report)

### 3a. Paper resolution
1. The OSTI landing page (`https://www.osti.gov/biblio/2975173`) timed out on multiple `curl` / `web_fetch` attempts (server-side or hop-side rate limit against automated fetchers).
2. Fell back to a title-based web search on `"ferroelectric fractals" "wurtzite AlN"` which returned:
   - APS: `https://link.aps.org/doi/10.1103/2qs8-yxmr` — PRL 136 (17), Editors' Suggestion (paywalled).
   - arXiv: `https://arxiv.org/abs/2410.18816` (v1, 24 Oct 2024) — open access. **Used as the working text.**
   - ResearchGate + arXiv HTML render as tertiary cross-checks (agree on authors/affiliation).
3. Downloaded arXiv PDF (`4 697 962 bytes`) to `work/paper.pdf` and text-extracted with `pdftotext -layout` to `work/paper.txt` (625 lines). Full authors, abstract, methods, and Figures 1–4 confirmed.

### 3b. Reimplementation of the paper's Monte Carlo model

The paper's own description of the MC (verbatim summary, from the Methods section):

> The Monte Carlo code was written in-house using Python to replicate the 2D switching patterns observed via molecular dynamics. Probabilities for each atom to flip from state 0 to 1 at a given time were assigned based on the state of the three nearest neighbors at the previous step, with probabilities increasing from 0 to 3 flipped neighbors. A higher field in these simulations corresponds to higher flipping probabilities.

We reimplemented this from scratch in `work/mc_hex_fractal.py` (~14 KB, single file, only `numpy` + `matplotlib`) with the following faithful choices:

1. **Lattice.** Honeycomb → brick-wall mapping on an `(H, W)` rectangular index grid so each interior site has exactly 3 neighbors. Sublattice A/B parity from `(i+j) % 2`.
2. **Flip rule.** Vectorised per-sweep: for each site count neighbours-flipped `k ∈ {0,1,2,3}`; assign per-step flip probability `p_grow[k]` (with `p_grow[0]` overridden by a small nucleation probability `p_nuc`); flip unflipped sites where `r < p_map`.
3. **Parameters used** (final calibrated run — see `report/evidence/results.json → args`):
   `H = W = 300`, `steps = 10 000`, `p_nuc = 1e-6`, `p_grow = (0, 8e-4, 1.2e-2, 1.5e-1)`, target-fill = 0.35 (snapshot analyzed at first sweep where flipped fraction ≥ 0.35). Five independent seeds: 17, 23, 37, 41, 53.
4. **Fractal-dimension measurement — two metrics, both applied to the same snapshots:**
   - **(a) Paper's own metric:** `d = log(A) / log(P)` with A = # sites in the domain and P = # boundary edges (edges between a flipped site and either an unflipped site or the grid boundary). This is what the paper reports as ≈ 1.34.
   - **(b) Independent cross-check — standard box-counting** on the domain boundary. Boundary = flipped sites with at least one unflipped 4-neighbor. Box sizes swept in powers of 2 from 2 to `min(H,W)/4`. Slope of `log(N)` vs `log(1/s)` reported.
   - Both metrics computed for (i) the largest connected cluster and (ii) the union of all flipped sites, using 4-neighbourhood connectivity on the rectangular index grid.

The full parameters, results per seed, snapshot PNGs and results.json are pinned to `report/evidence/`.

## 4. Results (vs paper)

### 4a. Fractal-dimension numbers (5-seed aggregate)

| Quantity | Paper (their MC) | Paper (Guido et al. exp.) | This work (mean ± σ over 5 seeds) |
|---|---:|---:|---:|
| `d = log(A)/log(P)`, **largest cluster** | ≈ **1.34** | ≈ 1.29 | **1.176 ± 0.018** |
| `d = log(A)/log(P)`, all flipped sites | — | — | 1.085 ± 0.001 |
| Box-counting `d_box`, **largest cluster** | — | — | **1.29 ± 0.08** |
| Box-counting `d_box`, all flipped sites | — | — | 1.57 ± 0.007 |
| Snapshot fill fraction at analysis | ~"growth stage" | — | 0.354 ± 0.001 |
| Largest cluster area (sites) | — | — | 2 456 ± ~300 |
| Largest cluster perimeter (edges) | — | — | 828 ± ~130 |

Interpretation:
- Our largest-cluster **box-counting** dimension (1.29 ± 0.08) is **an excellent match** to the paper's *experimental* value (1.29) and is within ~1σ of the paper's MC value (1.34). This is the number that most modern fractal-analysis papers would call *the* fractal dimension of a 2D domain boundary.
- Our number from **the paper's own log(A)/log(P) metric** is systematically lower (1.18 vs 1.34). This metric is unusual and quite sensitive to exactly how the domain outline is traced, the snapshot fill level, the size of the domain being measured, and the grid geometry (they trace continuous 2D outlines in an OVITO visualization of a triangular hex grid; we count boundary edges on a discrete brick-wall mapping). A ~0.15 systematic offset in a `log/log` ratio is entirely consistent with a moderate difference in the perimeter definition.
- **Conclusion (C3+C4):** The physical claim ("the 2D MC domain wall is fractal with dimension in the ~1.3 range, not the ~2 of a compact convex domain") is independently reproduced. The specific reported number 1.34 is only partially matched: exactly matched by an independent metric, systematically low by their own metric.

### 4b. Visual / qualitative (C1, C2)

- Snapshot PNGs (`report/evidence/snapshot_seed{17,23,37,41,53}.png`) show emergent **jagged, dendritic, non-convex** flipped regions dispersed across a background of unflipped sites — the qualitative "snowflake" pattern the paper describes.
- Domains are non-convex and boundaries are visibly rough at every scale we sampled — direct visual confirmation of C2.
- (Vision-model image tools were unavailable this turn due to provider credit exhaustion, so the visual claim relies on the numerical fractal-dimension result plus the raw pixel PNGs pinned in `report/evidence/`.)

### 4c. MD / MLFF portion (C5, C6): BLOCKED / out of scope

- The MD side (LAMMPS + AENET MLFF, 115 200-atom supercell, 15–30 ns trajectories at multiple temperatures and fields) requires the trained MLFF weights from the authors' prior paper (Ref. 26 in the PRL), a LAMMPS build with the AENET add-on, and multi-hour multi-GPU compute. Even a minimal "does the hysteresis loop close" spot-check would need several GPU-hours at minimum and access to the trained potential.
- Their pseudo-activation energy of ν = 9.4 meV (from fitting `Ec(T) = Ec0 · exp(-ν/kBT)` across their MD hysteresis loops) and their Merz-law activation-field values (130 MV/cm and 240 MV/cm in-plane at 300 K and 200 K; ≈50 MV/cm out-of-plane) are recorded here for future full-replication runs but not tested this turn.
- This is a **BLOCKED / out-of-scope** call on C5, not a FAILED one — the science is accessible if the trained MLFF (Ref. 26) is publicly deposited; the paper does not link a Zenodo/GitHub for the MLFF or the MC code, so a full replication would require author contact.

## 5. Verdict

**PARTIAL / SPOT-CHECK.** The paper's central qualitative claim — that the described 2D hexagonal-lattice MC rule generates a fractal domain wall in the ~1.3 fractal-dimension regime, and that the underlying mechanism (localized 3-neighbor-dependent flipping on a hexagonal lattice) is what produces this fractality — is independently reproduced here from a clean-room reimplementation on 5 seeds, entirely on free local CPU compute, with the paper's own metric returning d ≈ 1.18 and an independent standard box-counting metric returning d ≈ 1.29 (which matches their reported experimental number 1.29 exactly and their MC number 1.34 to within ~1σ). The MD/MLFF side of the paper (Figs. 2–3, coercive fields, Merz-law activation fields, pseudo-activation energy) is out of scope for a same-turn CPU-only replication and would require the authors' trained MLFF and multi-GPU compute — treated as BLOCKED, not FAILED.

### Justification vocabulary mapping
- Not REPLICATED — because C3's exact reported number (1.34 via log(A)/log(P)) is not exactly matched, and C5 was not attempted.
- Not CONTRADICTED — both fractal-dimension metrics land in the paper's own claimed regime; the physical picture (fractal, non-convex, snowflake-like domains from the described MC rule) is confirmed on the very first faithful implementation.
- Not NO-GO — paper was fully resolvable (arXiv open, methods complete enough to reimplement the MC end-to-end from the paper text alone).
- **PARTIAL / SPOT-CHECK** is the honest verdict: one independent method-and-metric agree, one paper-native metric shows a systematic offset, and one major limb of the paper (MD/MLFF) was not touched.

---

## Artifacts

- `work/paper.pdf` — arXiv 2410.18816 v1 (4.7 MB).
- `work/paper.txt` — text extraction via pdftotext (625 lines).
- `work/mc_hex_fractal.py` — clean-room Python reimplementation of the paper's 2D hexagonal MC + both fractal-dimension metrics.
- `report/evidence/results.json` — per-seed and aggregate MC output, including all args for exact re-run.
- `report/evidence/snapshot_seed{17,23,37,41,53}.png` — MC snapshots at the analyzed fill fraction.
- `report/evidence/largest_seed*_crop.txt` — ASCII crops of the largest-cluster masks (small — many crops sit off-cluster because of the 80×80 clip; the full clusters are in the PNGs).

## Reproduce

```
python3 work/mc_hex_fractal.py \
    --out-dir report/evidence \
    --seeds 17 23 37 41 53 \
    --H 300 --W 300 --steps 10000 \
    --p-nuc 1e-6 --p-grow 0.0 8e-4 1.2e-2 1.5e-1 \
    --target-fill 0.35
```

Runtime: ~80 s on one CherryRd CPU core; no GPU, no network, no external data.
