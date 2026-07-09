# RE-TIER (2026-06-25): VERDICT = NO-GO (hard ceiling, was SPOT-CHECK)

**Reclassified SPOT-CHECK -> NO-GO** per Rick's rule: a hard-ceiling spot-check (nothing reproducible) belongs in the NO-GO pile.

**Precise blocker (6/22 rule):** Closed Elsevier (BBRC) paper + zero data deposit. Missing artifact: paper PDF + author dose-survival spreadsheets, neither public.

---

# LUCID-100 Replication Report

**Slot:** lucid100-cho-low-dose-rate-dna-repair-deficient (Wave 3 / master rank 55, Tier A, priority 16)
**Paper:** Buglewicz DJ, Haskins JS, Haskins A, Su C, Gius D, Kato TA. *Exploring DNA repair deficient CHO cell response to low dose rate radiation.* Biochem Biophys Res Commun (BBRC) **698**: 149539 (2024).
**DOI:** [10.1016/j.bbrc.2024.149539](https://doi.org/10.1016/j.bbrc.2024.149539) · **PMID:** 38271835
**Audit run:** 2026-06-22 by Ollie subagent (LUCID-100 audit pass).
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-cho-low-dose-rate-dna-repair-deficient/`

---

## TL;DR

Direct quantitative reproduction of this paper is **impossible from public artifacts**. The BBRC paper is closed-access Elsevier (`is_oa=false`, `oa_status=closed`, zero Unpaywall OA locations, no PMC record, no preprint, no thesis copy, no data/code deposit). The brief said "Paper source staged as .pdf / .md (Marker parse) / .txt" — **no such files exist in this slot**; only OA companion papers are present. We re-verified OA status against Unpaywall + Semantic Scholar on 2026-06-22 with the same negative result as the 2026-06-09 first pass.

What we *did* build, and re-verified runs cleanly today: a closed-form **LQ + Lea-Catcheside G(λ) + NHEJ-IDRE smoke model** (`scripts/replicate_smoke.py`) anchored to the same Kato-lab OA companion (Buglewicz 2023, *Cancer Sci.*, PMC10727999) using the same CHO mutant panel (10B2 WT / 51D1 HR⁻ / V3 NHEJ⁻). It demonstrates the three qualitative central claims (acute radiosensitivity ordering, WT/HR dose-rate sparing, NHEJ inverse-dose-rate effect) and is honest that absolute LQ parameters are illustrative, not lifted from the BBRC paper.

**Verdict: SPOT-CHECK (qualitative mechanism smoke only).** 3/8 testable claims qualitatively passed via a justified-substitute model; 5/8 hard-blocked by the closed publisher and the absence of any data deposit. Cannot promote to PARTIAL/REPLICATED without the BBRC PDF or author source-data spreadsheets.

---

## 1. Data sources

### 1.1 Primary paper — **NOT AVAILABLE**
- DOI 10.1016/j.bbrc.2024.149539 — closed-access Elsevier BBRC, paywall confirmed 2026-06-22.
- **EXACT missing artifacts:**
  - The BBRC 2024 PDF or HTML full-text (gives the actual cell-line panel composition, dose-rate values in Gy/h, total doses, clonogenic counts, and any reported α/β LQ fits).
  - Any author-deposited source-data spreadsheet (clonogenic plate counts; γ-H2AX foci per cell distributions; growth-curve cell counts vs time; cell-cycle flow histograms or gates). The paper text *as visible from abstract/MeSH* does not promise a deposit, and none was found in GEO / SRA / ArrayExpress / Zenodo / Figshare / OSF / Dryad / Mendeley Data.
  - Raw γ-H2AX microscopy image stacks (almost never deposited; would be needed for any foci-counting reproducibility).
  - Methods-section dose-rate hardware details (source activity, distance, attenuation) needed to convert any reported nominal Ḋ to physical Ḋ.
  - Dylan Buglewicz CSU dissertation (would likely contain methods + extra figures); checked CSU Mountain Scholar 2026-06-09, **not found**.

### 1.2 Substitutes actually used
| Artifact | Source | Local path | Use |
|---|---|---|---|
| Buglewicz et al. 2023, *Cancer Sci.*, PMC10727999, "Carbon ion beam irradiation…" | EuropePMC OA PDF + JATS XML | `artifacts/buglewicz_cas15972_carbon_PMC.pdf`, `artifacts/buglewicz_cas15972_fullText.xml` | Same Kato lab; same panel (10B2/51D1/V3); supplies SER ratios (1.00/1.63/1.72) used to anchor relative ordering only. |
| Kato 2019, *Sci. Rep.*, PMC6467899, monoenergetic carbon-ion CHO panel | OA PDF + pdftotext dump | `artifacts/kato_2019_42600_carbon.pdf`, `.txt` | Cross-reference for CHO+xrs5 panel methodology. |
| Crossref work record (21 refs) | Crossref REST | `artifacts/crossref.json` | Reconstructed likely cell-line panel from cited methodology refs (bib6/7/8/10/11/12/14/20). |
| PubMed MeSH + author keywords | NCBI EFetch | `artifacts/pubmed.xml` | "DNA double strand break repair", "Inverse dose rate effect", "Low dose rate irradiation" — confirms IDRE-in-NHEJ is the central novel claim. |
| Semantic Scholar / Unpaywall / EuropePMC / OpenAccessButton | various REST | `artifacts/semscholar.json`, `unpaywall.json`, `europepmc.json` | All re-verified 2026-06-22: `CLOSED`/`is_oa=false`/zero OA locations. |

### 1.3 Re-verification on 2026-06-22 (today)
- Unpaywall: `is_oa=False oa_status=closed locations=0`
- Semantic Scholar `openAccessPdf.status = CLOSED`, empty URL
- OpenAccessButton: silent (no OA pointer)
- → Status unchanged from 2026-06-09 first pass.

---

## 2. Methods comparison

| Aspect | Paper (per abstract + MeSH + companion-paper methods) | This audit | Match? |
|---|---|---|---|
| Cell panel | CHO DNA-repair mutant panel (NHEJ, HR, plus likely NER / FA / PARP-axis mutants). Exact list paywalled. | 3-line illustrative subset (WT 10B2 / HR⁻ 51D1 / NHEJ⁻ V3-or-xrs5) from companion paper. | **Reduced scope.** |
| Radiation source | γ-rays at acute and LDR dose rates; exact Ḋ values paywalled. | Generic LQ + Lea-Catcheside G(λ) parameterised by dose rate (Gy/h), not a specific source. | **Method substituted** (closed-form analytical model in place of wet-lab clonogenic). |
| Survival endpoint | Clonogenic colony-formation assay; LQ fits. | LQ analytical curve only; no plate counts. | **Substitute.** |
| Dose-rate sparing model | Probably standard LQ + G(λ) or empirical curves (unread). | LQ + Lea-Catcheside G(λ) with single sublethal-repair half-time τ per line. | **Plausible match.** |
| NHEJ inverse dose-rate mechanism | Hypothesised (paper claims IDRE in repair-deficient mutants). | Added a phenomenological NHEJ α-boost term `α_eff(Ḋ) = α·(1 + φ·exp(−Ḋ/Ḋ₀))` to represent accumulated unrepaired DSBs. | **Substitute — phenomenological**, not a mechanistic recapitulation of the paper's model (which we cannot read). |
| γ-H2AX foci kinetics | Wet-lab microscopy; foci/cell vs time during sustained LDR. | **Not modeled.** | **Not attempted** — no public data to anchor parameters. |
| Cell-cycle / giant-cell formation | Flow + microscopy. | **Not modeled.** | **Not attempted.** |
| Growth inhibition / population doubling | Cell counts vs time under sustained LDR. | **Not modeled.** | **Not attempted.** |
| Stats / FDR | Unknown (paywalled). | None applied (deterministic smoke model, no replicates). | **N/A.** |

Substitution justification: with the BBRC PDF unavailable and no data deposit, the only honest options are (a) refuse all replication or (b) build a transparent qualitative smoke that exercises the named claims using OA companion data. We chose (b) and clearly label it as illustrative.

---

## 3. Quantitative claim audit

Claims enumerated from abstract + MeSH + author keywords (only publicly visible content for this paywalled paper).

| # | Claim (paraphrased) | Type | Tested? | Status | Evidence |
|---|---|---|---|---|---|
| C1 | NHEJ-deficient and HR-deficient CHO mutants are more radiosensitive than WT under acute γ. | Qualitative ordering | YES (smoke) | **SMOKE PASS** | SF(2 Gy): WT=0.7261 > HR⁻=0.5379 > NHEJ⁻=0.3198. Ordering matches PMC10727999 Table 1 SER (1.00 / 1.63 / 1.72). |
| C2 | WT and HR-deficient cells show classical dose-rate sparing. | Qualitative trend | YES (smoke) | **SMOKE PASS** | At D=4 Gy: LDR/acute SF ratio = 1.548 (WT), 1.567 (HR⁻); both > 1.2 sparing threshold. |
| C3 | NHEJ-deficient cells show an inverse dose-rate effect (LDR more lethal than acute at some Ḋ). | Qualitative trend / mechanism | YES (smoke, mechanism only) | **SMOKE PASS (mechanism only)** | NHEJ⁻ SF at acute=0.0948, SF min in LDR window=0.0451, ratio=0.476 (<<1). Magnitude/Ḋ-window vs paper is **unverifiable** without PDF. |
| C4 | LDR exposure alters cell cycle and induces giant-cell formation. | Wet-lab observation | NO | **BLOCKED — DATA** | Flow histograms + microscopy not deposited. Missing: cell-cycle gate fractions, giant-cell counts per line per Ḋ. |
| C5 | γ-H2AX foci accumulate during sustained LDR. | Wet-lab quantitative | NO | **BLOCKED — DATA** | Missing: foci-per-cell tables (mean ± SD per timepoint per Ḋ per line) and/or raw image stacks. |
| C6 | Growth inhibition / population-doubling assay shows pathway-specific LDR sensitivity. | Wet-lab quantitative | NO | **BLOCKED — DATA** | Missing: cell count vs time curves per line per Ḋ. |
| C7 | HR mutants align with responses to "major DNA damaging agents" (cross-sensitivity). | Meta-claim | NO | **BLOCKED — TEXT** | Cross-agent panel not in abstract; need Methods/Discussion text. |
| C8 | Specific dose-rate values and exact cell-line panel composition. | Factual | NO | **BLOCKED — TEXT** | Need Methods table. |

**Coverage of testable claims:** 3 / 8 attempted (37.5%); 3/3 of attempted pass qualitatively. Far below the ≥80% bar for REPLICATED.

**Tolerance note:** because the BBRC paper's actual numbers are paywalled, "agreement" for C1–C3 is *direction only* (sign of effect and ordering), not numerical tolerance. There is no honest way to compute a numerical agreement metric against unavailable target values.

---

## 4. Scope audit

Primary analyzable units in the paper (inferred from abstract + MeSH + the lab's prior companion papers — the full Methods is paywalled):

| Unit | Paper (estimate) | This audit | Coverage |
|---|---|---|---|
| CHO mutant cell lines on the panel | Likely 8–12 lines spanning NHEJ (V3, xrs5/6, XR-1), HR (51D1, irs-1/2/3), NER (UV5, UV41, UV61), XRCC1/PARP (EM9, EM-C11), and possibly FA mutants. | 3 representative lines modeled (WT, 1 HR⁻, 1 NHEJ⁻). | **~3/10 ≈ 30%** (very rough; true denominator unknown). |
| Endpoints | 4 (clonogenic survival, growth inhibition, γ-H2AX foci, cell cycle). | 1 modeled (clonogenic survival via LQ smoke). | **1/4 = 25%.** |
| Dose-rate conditions | Likely ≥3 (acute + ≥2 LDR rates). | 60-point continuous Ḋ sweep on the smoke model; the model is not anchored to the paper's actual Ḋ grid. | **N/A** (continuous vs unknown discrete). |
| Figures/Tables | Unknown (likely 4–6 figures, 1–2 tables). | 2 model figures generated (`acute_survival.png`, `dose_rate_sparing.png`). | **Cannot compute.** |

**Coverage estimate:** ≤30% of primary analyzable units (cell-lines) and 25% of endpoints. Well below the 80% bar. The 80% bar **cannot** be met with public data alone; the only path is the BBRC PDF + author spreadsheets.

---

## 5. What I actually ran

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-cho-low-dose-rate-dna-repair-deficient/
python3 scripts/replicate_smoke.py
```

Re-ran live on 2026-06-22 (CherryRd, CPU-only, ~1 s wall, no internet needed at run time). Output:

```
[C1] Acute LQ ordering at D=2 Gy:
     SF(2 Gy) WT (10B2/AA8)            = 0.7261
     SF(2 Gy) HR- (51D1)               = 0.5379
     SF(2 Gy) NHEJ- (V3/xrs5)          = 0.3198
     PASS criterion: SF(NHEJ-) < SF(HR-) < SF(WT)  -> True
[C2] Dose-rate sparing at D=4 Gy (LDR/acute SF ratio, want > 1.2):
     WT  ratio = 1.548
     HR- ratio = 1.567
     PASS: True
[C3] NHEJ- inverse dose-rate effect at D=4 Gy:
     SF acute (10 Gy/h)     = 0.0948
     SF min in LDR window   = 0.0451
     IDRE ratio (min/acute) = 0.476
     PASS criterion: ratio < 0.95 -> True
```

Also re-checked the publisher OA status today (`curl` to Unpaywall + Semantic Scholar + OpenAccessButton) and got the same closed-access answer as 2026-06-09.

---

## 6. Key output files

| Path | Description |
|---|---|
| `REPORT.md` | This file. |
| `FIRST_PASS_REPORT.md` | The 2026-06-09 first-pass reproduction matrix (kept for provenance; superseded by this REPORT.md). |
| `README.md` | Slot overview, panel reconstruction. |
| `PROGRESS.md` | Chronological 2026-06-09 work log. |
| `ARTIFACT_MANIFEST.tsv` | 19 artifact rows. |
| `scripts/replicate_smoke.py` | LQ + Lea-Catcheside G(λ) + NHEJ-IDRE smoke model (Python, ~10 KB, runs in <1 s). |
| `data/smoke_summary.json` | Pass/fail booleans + numeric SF values for C1/C2/C3. |
| `figures/acute_survival.png` | C1 acute LQ panel curves. |
| `figures/dose_rate_sparing.png` | C2/C3 SF vs Ḋ at D=4 Gy; IDRE visible for NHEJ⁻. |
| `notes/claims.md` | 8 extracted claims with reproduction status. |
| `artifacts/europepmc.json`, `semscholar.json`, `unpaywall.json`, `pubmed.xml`, `crossref.json` | Bibliographic metadata + OA-status evidence. |
| `artifacts/buglewicz_cas15972_carbon_PMC.pdf`, `buglewicz_cas15972_fullText.xml` | OA companion paper (Buglewicz 2023, *Cancer Sci.*, PMC10727999) used as panel anchor. |
| `artifacts/kato_2019_42600_carbon.pdf`, `.txt` | OA companion paper (Kato 2019, *Sci. Rep.*, PMC6467899). |
| `artifacts/sciencedirect_landing.html`, `sciencedirect_page.html` | Paywall evidence (403 on full-content fetch). |
| `artifacts/smoke_run_output.txt` | Smoke script stdout. |

---

## 7. Honest gaps

1. **No primary paper text.** Everything about claim wording, exact dose rates, cell-line panel composition, statistical methods, and reported numerical values is inferred from abstract + MeSH + companion-paper methods. There is no way to verify any quantitative claim against the actual paper from public data.
2. **3/8 claims tested, 0/8 quantitatively verified.** Claims C1–C3 pass *direction only* in a phenomenological model that uses illustrative LQ parameters, not parameters measured in the paper. We cannot report a numerical agreement tolerance.
3. **5/8 claims hard-blocked.** C4 (cell cycle), C5 (γ-H2AX foci), C6 (growth inhibition), C7 (cross-agent), C8 (panel composition/Ḋ values) all require the paywalled PDF and/or author data spreadsheets that do not exist in any public repository.
4. **Scope ≤30%.** Modeled 3 lines out of a likely 8–12; modeled 1 endpoint out of 4; no replicate structure, no statistics.
5. **NHEJ-IDRE term is phenomenological.** The `α_eff = α·(1 + φ·exp(−Ḋ/Ḋ₀))` boost is a behavior-fitting choice, not derived from the paper's actual mechanistic model (which we cannot read). Multiple mechanisms (cell-cycle redistribution, mitotic-catastrophe accumulation, repair-misligation in NHEJ-deficient backgrounds) can produce IDRE; the smoke does not distinguish among them.
6. **The brief said "Paper source staged as .pdf / .md (Marker parse) / .txt"** — this is **not true** for this slot. The orchestrator pipeline that prepares paper staging silently skipped this paper (presumably because publisher fetch failed). This audit had to operate entirely from companion-paper anchors and metadata.
7. **Worktype mislabel in master TSV.** Master originally tagged this slot `omics/signature replication`. It is **not omics** — it is wet-lab clonogenic + foci + cell cycle. The TSV was already retagged on 2026-06-09 to `wet-lab clonogenic + gamma-H2AX foci; no public data deposit`; flagging here for completeness.
8. **No author contact attempted.** Per scope rules ("Local + free tools only"; no external messages without explicit recipient/channel). Author contact would in principle unlock the source data but is out of scope.

### Reproducibility blockers — EXACT missing artifacts (per Rick's 2026-06-22 hard rule)

The dominant blocker is **DATA + TEXT**, not compute. Specifically, this slot needs:

- **The BBRC 2024 PDF (DOI 10.1016/j.bbrc.2024.149539)** or its HTML full-text. This is the single biggest blocker. Without it, claims C7/C8 are unaddressable and C1–C3 cannot be verified numerically. The publisher (Elsevier) does not provide an OA copy. No preprint, no PMC, no thesis copy located.
- **Source-data spreadsheets** for: (a) clonogenic plate counts per cell line per dose per dose-rate per replicate; (b) γ-H2AX foci counts per cell per timepoint per Ḋ per line (or raw image stacks); (c) cell counts vs time for the growth-inhibition assay; (d) flow-cytometry cell-cycle histograms or gate fractions. None of these were deposited in GEO / SRA / ArrayExpress / Zenodo / Figshare / OSF / Dryad / Mendeley Data as of 2026-06-22.
- **Methods-section dose-rate hardware details** (source isotope/activity, distance, attenuation) needed to convert nominal Ḋ to physical Ḋ for cross-lab comparison.
- **The Dylan Buglewicz CSU dissertation** (not found at Mountain Scholar), which would plausibly contain methods detail + supplementary figures.

---

## 8. Verdict

**VERDICT: SPOT-CHECK** — qualitative mechanism smoke only; quantitative reproduction blocked.

- **Coverage:** ≤30% of cell-line scope and 25% of endpoint scope (3 lines / 1 endpoint out of ~10–12 lines / 4 endpoints).
- **Claims tested:** 3 / 8 (37.5%); all 3 pass *direction only*, zero numerically verified.
- **Methods match:** justified-substitute analytical model (LQ + Lea-Catcheside G(λ) + phenomenological NHEJ α-boost); not the paper's actual methods.
- **Blocker class:** DATA + TEXT (closed-access publisher + zero data deposit).

**Coverage: 2/10.** (3 lines of ~10 modeled; 1 of 4 endpoints; no replicate structure; no statistics.)
**Agreement: 3/10.** (3 testable directional claims qualitatively reproduced; 0 numerical claims verified; can't be higher when the target numbers are paywalled.)

REPLICATED threshold (≥80% scope AND ≥80% claims) cannot be met from public artifacts. PARTIAL would require at least the paper text plus a few headline numbers (e.g. one α/β table and one SF-vs-Ḋ figure). NO-GO is too harsh — the smoke model is real, runnable, honest, and exercises the central novel claim (IDRE in NHEJ-deficient lines).

---

VERDICT=SPOT-CHECK COVERAGE=2/10 AGREEMENT=3/10

Repro-blocker summary (3 lines):
1. DATA — closed-access Elsevier BBRC paper (DOI 10.1016/j.bbrc.2024.149539): no OA mirror, no PMC, no preprint, no CSU thesis copy; this is the single biggest blocker (5 of 8 claims unaddressable, 3 of 8 only directionally testable).
2. DATA — no author-deposited source-data spreadsheets for clonogenic plate counts, γ-H2AX foci/cell distributions, growth-curve cell counts, or cell-cycle flow data in GEO/SRA/Zenodo/Figshare/OSF/Dryad/Mendeley Data (re-verified 2026-06-22).
3. PIPELINE — the orchestrator's "staged paper as .pdf/.md/.txt" step silently produced nothing for this slot; the audit had to substitute OA companion-paper anchors (PMC10727999, PMC6467899) and metadata records (Unpaywall/S2/EuropePMC/Crossref/PubMed) and an explicitly illustrative LQ+Lea-Catcheside+NHEJ-IDRE smoke model.
