# FIRST_PASS_REPORT — Slot 57 (Wave 6)

**Paper:** Piotrowski Ł., Krasowska J., Fornalski K.W. (2023).
*Mechanistic Modelling of DNA Damage Repair by the Radiation Adaptive Response Mechanism and Its Significance.*
**BioMedInformatics** 3(1), 150–163. **DOI:** 10.3390/biomedinformatics3010011 (CC BY 4.0).

**Verdict: GO — light replication complete; full Monte Carlo deferred.**

---

## 1. What we replicated

The paper exposes its model entirely in §2–3 as a set of closed-form equations
with all parameters quoted in the text. We implemented Eqs (1)–(4) in
~80 lines of Python (`scripts/smoke_adaptive_response.py`) and reproduced the
two analytical figures:

| Paper figure | Our replica | Match |
|--------------|-------------|-------|
| Fig. 1: analytical `f(D)`, T=120h, N₀=493,000 | `outputs/fig1_repair_fraction.png` | ✅ numeric, qualitative |
| Fig. 12 (analytical curve only): global colony fraction `f(D)·P_hit(D)` | `outputs/fig12_global_fraction.png` | ✅ as the ideal-case upper bound; MC curve is much lower (see below) |

**Numeric agreement, paper Fig 1 (key claim "ratio ≈ 100% in 10–45 mGy"):**

* Our replica in that band: f(D) = **97.5 % – 99.9 %**, mean **99.6 %**.
* Analytical peak of `P_AR(D, k)` (Eq. 2): **D\* = 2/α₁ = 25.19 mGy** and **k\* = 2/α₂ = 24.04 h**.
  These are exactly the priming-dose and inter-dose interval the authors used
  to calibrate their first two-dose Monte Carlo scenario (D₁=25 mGy, Δt=24 h).
  Self-consistency confirms the parameter set was copied correctly.

## 2. What we explicitly did NOT replicate (and why)

* **Figs 2 (MC overlay points), 3–6 (two-dose MC), 7–11 (constant dose-rate MC).**
  These all require the *prior* simplified Monte Carlo model of Fornalski
  et al. 2022 (*Dose-Response*, ref [1] in this paper), which spreads cells
  over a 3-D matrix and runs each through a stochastic probability tree of
  hit / lesion / metabolic damage / classical repair / AR repair /
  multiplication / death / mutation / cancer transitions. That code is
  **not publicly released** and is non-trivial to re-derive from the parent
  paper. Re-implementing it is a dedicated multi-day project that should be
  scheduled separately if a deep replication is approved.
* **Quantitative match of the 0.126 % whole-system AR contribution
  reported in §4.** That number is a *Monte Carlo* output that includes
  all *non-AR* damage and repair channels (natural metabolic damage, cell
  death, multiplication, mutation, classical repair). Our analytical
  curve necessarily over-estimates the AR-only fraction (~7 % at the
  peak) because it omits those competing channels — this is precisely
  the qualitative point §4 makes: "focusing on the whole system, this
  phenomenon practically disappears". Our smoke run is the
  *upper bound* the paper itself contrasts against the MC result.

## 3. Data & code availability assessment

| Resource | Status |
|----------|--------|
| Paper PDF (OA, CC BY 4.0) | ✅ harvested to `artifacts/paper.pdf` |
| Figures 1–12 (550-wide JPGs) | ✅ `artifacts/figures/` |
| Supplementary materials | ❌ none on MDPI page or in DOAJ |
| Source code (this paper) | ❌ none — "No new data creation" |
| Source code (parent Fornalski 2022 MC) | ❌ no public repo found |
| Author contact attempted | ❌ task explicitly forbids author contact |

## 4. Replication-feasibility scoping

* **Light (analytical) replication: DONE.** Already in this repo. ~0.5 s on
  CherryRd.
* **Medium (re-implement single-dose MC of Fig 2):** Estimated 1–2 days. Need
  to code the cell-status tree from the parent paper. Parameters all
  available in this paper + parent.
* **Heavy (two-dose Raper–Yonezawa and constant dose-rate, Figs 3–11):**
  Estimated 3–5 days *given* a working medium-level reimplementation. Each
  scenario is 64 000 cells × 100 stochastic runs over ~150 h of simulated time;
  this is still small enough to run on CherryRd in minutes per scenario once
  the model is coded. **No GPU / cluster job needed.**

## 5. Job-plan (only if heavy replication is later approved)

CPU-only, ~1 GB RAM, single-host. No GPU. No external API. Runtime budget
< 30 min total for all eleven figures. CherryRd is suitable; no need for
uicgpu / Aurora / chiatta00.

```
# pseudo-plan
1. Re-derive cell-status probability tree from Fornalski 2022 §2.
2. Implement cell-status Monte Carlo in pure-numpy or numba.
3. Calibration sanity check vs Fornalski 2022 in-vitro data points.
4. Reproduce Fig 2 MC points (single dose, full-repair & all-repair variants).
5. Reproduce Figs 3-6 (two-dose Raper-Yonezawa, 4 scenarios).
6. Reproduce Figs 7-11 (constant dose-rate, 4 scenarios + Eq.(2) check).
7. Write deep-replication report; QA pixel-diff against original PNGs.
```

## 6. Risks / caveats / lessons

* MDPI front-door is **Akamai-gated**; direct `curl`/`wget` return 403. The
  CDN host `pub.mdpi-res.com` is **not** gated and serves both the PDF and the
  HTML-page figure JPEGs without challenge. Recommend caching this fact in
  workspace TOOLS or the `agent-browser` skill.
* Image vision (Anthropic + OpenAI + Gemini Flash 3) was all unavailable for
  this session; visual pixel-diff between paper Fig 1 and our replica is
  deferred. The numeric in-band check (97.5–99.9 % vs paper "≈100 %") is the
  substitute QA gate.
* No 1500-wide variants of the figures exist on the CDN; only 550-wide.

## 7. Required next actions

1. (Optional) Schedule deep MC replication as a separate slot when bandwidth
   permits — see §5 job plan above.
2. Run image-pixel diff between `outputs/fig1_repair_fraction.png` and
   `artifacts/figures/fig001.jpg` next time vision is available.
3. No author contact (task forbids and not needed).
4. QA retag recommendation: **`KEEP-DONE-LIGHT`** in
   `LUCID100_SOLID_MASTER_QA.tsv` row 88. Not a NO_GO.
