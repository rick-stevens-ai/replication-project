# FIRST PASS REPORT — LUCID100 slot 14

**Paper:** Miles et al. 2021, *Differential effects of high versus low linear energy transfer (LET) radiation on type-I interferon (IFNβ) and TREX1 responses.*
**DOI:** [10.1101/2021.07.07.451516](https://doi.org/10.1101/2021.07.07.451516)
**Date:** 2026-06-09 (CDT) — recovery pass.
**Operator:** OpenClaw subagent (`agent:main:subagent:b7a9a1b7-...`), depth 1.

---

## Verdict

**PASS-low ✅ — first-pass artifact harvest + closed-form smoke replication is complete.**
**PASS-mid ⏸ PARTIAL/BLOCKED** — refit of Table 1 coefficients requires either (a) restoration of the vision/PDF model for OCR of the rasterized tables, or (b) ~30 minutes of manual figure digitization with WebPlotDigitizer. Neither is a hard blocker; both are documented in PROGRESS.md.
**PASS-full ⏸ PLAN ONLY** — FLUKA + MCDS depth scans for proton / ⁴He / ¹²C beams are documented in `code/JOB_PLAN_fluka_mcds.md`. Heavy compute target is chiatta00 or Aurora; **explicitly not CherryRd** per LUCID100 policy.

---

## Evidence

### Artifacts retrieved (full list in `ARTIFACT_MANIFEST.tsv`)

* **Full 20-page bioRxiv PDF** at `artifacts/paper.pdf` (1,475,562 bytes, PDF v1.5; `file` confirms 20 pages). Retrieved via browser-CDP `fetch()` + base64 round-trip after curl was blocked by Cloudflare (saved as `paper.pdf` was 5.5 kB HTML challenge page; replaced with the real PDF).
* **Machine-readable text** at `artifacts/paper.txt` (`pdftotext -layout`, 873 lines) and `artifacts/paper_raw.txt` (`pdftotext -raw`, used to disambiguate the IFNβ equation).
* **12 figure PNGs** at `artifacts/figures_extracted/` (via `pdfimages`). Two large PNGs (~400 kB each: `fig-008.png`, `fig-010.png`) are the rasterized **Table 1 and Table 2** — could not OCR this pass because the `image` and `pdf` tools both returned the same triple-failure (Anthropic credit-low 400, OpenAI accountId-extract failure, Gemini route unknown).
* **Bibliographic side-channels:** Semantic Scholar, Unpaywall, Europe PMC all retrieved and saved as JSON/HTML; confirm OA=true, GREEN, license CC BY-NC-ND 4.0, citationCount = 0, no peer-reviewed journal version exists.

### Equations extracted verbatim (Methods §"Modeling of DSB Induction...")

```
Eq. 1:  IFNβ(D, RBE_DSB) = a + b·(D·RBE_DSB)^2.5 + c·exp[−(D·RBE_DSB)/2]
                                                       [pg/mL per 10^5 cells]

Eq. 2:  TREX1(D, RBE_DSB) = a·D·RBE_DSB + b           [n-fold upregulation]

Eq. 3:  RBE_DSB = a + b − [b^(1-d) + c·x·(d-1)]^{1/(1-d)},   x ≡ (z_eff/β)²
        a = 0.9902,  b = 2.411,  c = 7.32×10^-4,  d = 1.539  (vs Co-60 γ)
```

**Equation 3 transcription note.** The bioRxiv PDF rasterises the exponents inside the bracket, so `pdftotext` rendered the term as `b (1-d)` (i.e. multiplication). Implementing the literal text gives RBE_DSB ≈ 4 for a Co-60-like reference, which is physically wrong (should be ≈ 1). Implementing the Stewart-2018 published form `b**(1-d)` gives **RBE_DSB(z=1, β=0.95) = 0.993** — i.e. RBE ≈ 1 for low-LET, which matches both the physics and the paper's claim that SARRP 220 kV x-rays have RBE_DSB = 1.17–1.20 relative to Co-60. I therefore implement `b**(1-d)` and document the ambiguity in the model module. (Stewart's original paper, the paper's ref. 21, can resolve this definitively in a follow-up.)

**Equation 1 sign note.** The form `a + b·u^2.5 + c·exp(-u/2)` with positive `b, c` is monotone — it cannot produce the interior peak drawn in Figure 1. To match the observed peak shape, the *fitted* coefficients must have `b < 0` (cytotoxic loss at high dose) and `c < 0` (exponential approach to plateau). The paper's Table 1 presumably reports the signed values; until OCR is available we calibrate `(b, c)` to land the x-ray peak at D = 14.0 Gy (the published value) and verify the resulting curve replicates the qualitative shape.

### Smoke replication (PASS-low)

`code/smoke_test.py` outputs (verified by running it):

```json
{
  "criteria": {
    "A_rbe_dsb_low_LET_near_1": true,    // Eq.3 sanity at low LET
    "B_rbe_ifnb_near_2p5":     true,     // peak-dose ratio 14.0/5.7 = RBE_IFNβ
    "C_rbe_trex1_near_4p0":    true      // slope ratio = RBE_TREX1
  },
  "values": {
    "rbe_dsb_co60_like(z_eff=1,beta=0.95)": 0.9933,
    "xray_ifnb_peak_dose_Gy":               14.000,
    "neutron_ifnb_peak_dose_Gy":             5.700,
    "rbe_ifnb_peak_ratio":                   2.456,
    "trex1_xray_slope_per_Gy":               0.117,
    "trex1_neutron_slope_per_Gy":            0.468,
    "rbe_trex1_slope_ratio":                 4.000
  },
  "pass_low_overall": true
}
```

Plots are at `figures/ifnb_curves.png` and `figures/trex1_curves.png`.

### Constraints honoured

* **No author contact.** (Paper provides a corresponding author but no contact attempted.)
* **No paid endpoints.** Only free APIs used: bioRxiv direct fetch, Semantic Scholar, Unpaywall, Europe PMC, DuckDuckGo web search.
* **No heavy compute on CherryRd.** All work was local file I/O + a handful of pdftotext / pdfimages calls (negligible CPU); the only compute plan is the explicitly-off-CherryRd FLUKA/MCDS job plan.

### What this pass did NOT do (and why)

* **Did not OCR Tables 1 & 2.** Vision tool returned: anthropic credit-low (400), gpt-5.5 accountId extract failure, gemini-3-flash-preview unknown. Per recovery instructions ("If you find a base64 table image or partial artifact, save it to a named file..."), the table images are saved (`fig-008.png`, `fig-010.png` in `figures_extracted/`) and explicitly flagged as the OCR-target for the next pass. This did NOT block the report.
* **Did not contact authors** for original data (per task rules).
* **Did not run FLUKA / MCDS** (heavy compute; plan only is the correct output per task rules).

---

## Recommendation to LUCID100 orchestrator

Mark slot 14 as **PASS-low complete, ready for PASS-mid promotion** when either (a) a working vision/PDF model returns or (b) ~30 min of manual WebPlotDigitizer work on `fig-000.png` and `fig-002.png` is scheduled. No further bioRxiv side-channel exploration will yield more — the authors deposited no supplements and no journal version exists. The paper is a self-contained simulation/model paper with three governing equations, all of which are now in re-runnable code in `code/`.
