# LUCID-100 Replication Report

**Paper:** Arnold AR, Chassaing B. *Maltodextrin, Modern Stressor of the Intestinal Environment.* Cellular and Molecular Gastroenterology and Hepatology 7(2):475–476, 2019.
**DOI:** 10.1016/j.jcmgh.2018.09.014
**Type:** Mini-review (commentary) — gastroenterology / mucosal immunology
**LUCID slot:** lucid100-maltodextrin-intestinal-stressor

## TL;DR
This paper is a ~2-page gastroenterology mini-review summarising published evidence that the dietary glucose-polymer food additive **maltodextrin** disturbs intestinal mucus, host–microbiota homeostasis, epithelial ER metabolism, and innate immunity, and may promote chronic intestinal inflammation (IBD). It contains **zero radiobiology content**: no ionizing radiation, no dose, no dose-rate, no LET, no DSB/repair model, no LQ parameters, no survival curve, no microdosimetric or track-structure data, no Monte Carlo. Verdict: **NO-GO — off-topic for LUCID; recommend DEMOTE from the LUCID-100 backlog.** Inclusion was a tagging / citation-graph spillover error (likely keyword collision on "stress" / "low-dose" or downstream gut-radiation citations).

## 1. Data sources
- **EuropePMC core record** — `evidence/europepmc.json` (title, authors, journal, year, DOI, MeSH).
- **EuropePMC full-text XML stub** — `evidence/fullText.xml` (16,836 bytes; section/figure structure + body prose).
- **EuropePMC HTML snapshot** — `evidence/europepmc.html`.
- **ScienceDirect publisher landing page** — `evidence/sciencedirect.html` (metadata only; PDF subscription-walled, not required for off-topic determination).
- **No deposited primary datasets** — the paper is a commentary; it generates no new data, releases no code, and references no accession numbers, repositories, or supplementary materials.
- Local + free tools only. No paid endpoints. No author contact.

## 2. Methods comparison
| Layer | Paper's "methods" | This audit's methods |
|---|---|---|
| Study type | Narrative mini-review / commentary | Metadata + full-text audit |
| Primary experiments | None (cites others' work) | N/A |
| Quantitative model | None | None to compare |
| Statistics | None reported | N/A |
| Code / data release | None | N/A |

There are no methods to reproduce. The paper synthesises prior in-vitro and mouse studies on maltodextrin → mucus thinning, *E. coli* biofilm, *Salmonella* colonisation, and ER stress in IECs, but reports no new wet-lab or in-silico procedure of its own.

## 3. Quantitative claim audit
The paper makes **no original quantitative claim** that can be tested. It transcribes/qualitatively summarises previously published observations from cited papers (Nickerson et al. 2014/2015, Laudisi et al. 2018, etc.). It has no equations, no fitted parameters, no error bars of its own, no test statistics. There is therefore nothing to numerically reproduce in this slot.

Critically for LUCID inclusion criteria — radiobiology-relevant quantitative content — the full text scores **0** on every keyword probe:

```
$ grep -iEc 'radiation|radiotherapy|gray\b|sievert|\bLET\b|\bDSB\b|clonogenic|
   linear.quadratic|ionizing|microdosimet|track.structure|radiobiol|x-ray|
   gamma.ray|proton|neutron|alpha.particle' evidence/fullText.xml
0
```

MeSH headings on the EuropePMC record: *Mucus, Animals, Inflammation, Polysaccharides, Food Additives (major), Endoplasmic Reticulum Stress (major)*. None are radiation-related.

## 4. Scope audit
**Analyzable units enumerated:** 0 radiobiology units. The paper contains 0 figures with original data, 0 tables with original data, 0 supplementary datasets, 0 code repositories, 0 dose-response curves, 0 survival assays, 0 DSB/γH2AX kinetics, 0 chromosome-aberration counts, 0 microdosimetric spectra, 0 Monte Carlo runs. The only "analyzable" content is text claims about gut biology, which are out of scope for LUCID-100.

## 5. What I actually ran
1. Confirmed EuropePMC metadata fields (`python3` JSON parse of `evidence/europepmc.json`) — title, authors, year, DOI, MeSH headings.
2. Grepped the 16.8 KB full-text XML (`evidence/fullText.xml`) for an exhaustive radiation/radiobiology keyword list (radiation, radiotherapy, gray, sievert, LET, DSB, clonogenic, linear-quadratic, ionizing, microdosimetry, track-structure, radiobiol, x-ray, gamma-ray, proton, neutron, alpha-particle): **0 hits**.
3. Inspected the cached ScienceDirect HTML landing page to confirm publisher venue and topic (gastroenterology, IBD).
4. Cross-checked the prior `NO-GO-REPORT.md`, `brief.md`, `artifact_harvest.md`, `attempt_log.md` in this slot — all four prior artifacts independently reach the same NO-GO conclusion.
5. No Python analysis scripts were created under `scripts/` and no `results/` directory was produced, because there is **nothing testable to analyze** for a radiobiology corpus. Creating empty stubs would be fabrication.

## 6. Key output files
- `REPORT.md` — this file (canonical 8-section LUCID report).
- `NO-GO-REPORT.md` — pre-existing detailed NO-GO writeup (consistent with this report).
- `brief.md` — one-paragraph relevance triage.
- `artifact_harvest.md`, `attempt_log.md` — provenance notes for the EuropePMC pulls.
- `evidence/europepmc.json` — primary metadata of record.
- `evidence/fullText.xml` — EuropePMC full-text XML used for keyword audit.
- `evidence/europepmc.html`, `evidence/sciencedirect.html` — supporting HTML snapshots.

## 7. Honest gaps
- **Publisher PDF not retrieved** (ScienceDirect subscription wall). Not blocking: the EuropePMC full-text XML is present and a 0-hit radiation-keyword grep across the entire body settles the relevance question. Buying access would not change the verdict.
- **Citation graph not mined.** If a downstream paper that cites Arnold & Chassaing 2019 covers gut-radiation interaction (e.g. radiation-induced enteritis × dietary emulsifier), that work would belong in its **own** LUCID slug, not this one.
- **No author contact** (per Rick's rule and pointless here — there is no original data to request).

## 8. Verdict
**NO-GO — off-topic for LUCID-100. Recommend DEMOTE from the LUCID-100 backlog.**

Justification: The paper is a non-radiation gastroenterology mini-review with no quantitative model, no deposited data, no figures with original data, and zero occurrences of any radiation/radiobiology term across its full text. It fails LUCID inclusion criteria on every axis (no dose, no dose-rate, no LET, no DSB/repair, no survival, no microdosimetry, no track-structure, no MC). Its presence in the LUCID-100 list is almost certainly a tagging or citation-graph spillover error. Demoting it frees the slot for a real radiobiology paper.

- **Coverage / 10:** **0** — nothing radiobiology-relevant to cover.
- **Agreement / 10:** **N/A** — no model or numbers to agree or disagree with.

---

**Repro-blocker summary (3 lines):**
1. Not data-blocked and not paywall-blocked in any meaningful sense — EuropePMC full-text XML is in hand and is sufficient to settle the relevance question.
2. The blocker is **categorical**: the paper has no radiobiology model, no dose, no DSB/repair, no LQ, no MC, no original quantitative data — there is literally nothing in the LUCID problem class to replicate.
3. Missing artifact if anyone ever wanted to "rescue" this slot: a different paper. Concretely, a radiation-relevant gut/microbiome paper (e.g. pelvic-RT enteritis dose–response, or microbiota modulation of intestinal crypt survival post-IR) — not anything from Arnold & Chassaing 2019.

VERDICT=NO-GO COVERAGE=0/10 AGREEMENT=N/A
