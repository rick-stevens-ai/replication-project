# NO-GO Report — Park et al. 2024, *Int J Mol Med*

## Paper / Authors / Venue
- **Title:** Predictive DNA damage signaling for low-dose ionizing radiation.
- **Authors:** Park JI, Jung SY, Song KH, Lee DH, Ahn J, Hwang SG, Jung IS, Lim DS, Song JY (KIRAMS / collaborators).
- **Venue:** *International Journal of Molecular Medicine* (2024).
- **DOI:** 10.3892/ijmm.2024.5380

## Claim(s) tested
**None — paper is a wet-lab biomarker + drug-screen study with no released model or numerical dataset.**

For the record, the paper's main claims are:
1. ATM, CHK2, p53 and γH2AX are activated dose-dependently after γ-irradiation of HuT 78 and IM-9 human lymphoid lines and of human PBMCs (western blot).
2. Cinobufagin (an ATM/CHK2 activator) increases bone-marrow cell counts in sub-lethally irradiated mice and slightly extends survival in lethally irradiated mice (not statistically significant).
3. BML-277 (CHK2 inhibitor) reduces radiation-induced p-CHK2 and γH2AX and mitigates apoptosis in cell culture.
4. These molecules are proposed as candidate radiation-response biomarkers.

None of these claims has a released computational model, parameter table, code, or omics dataset attached.

## Method (this report)
1. Read EuropePMC core record (`evidence/europepmc.json`) — full abstract, author list, journal/year/DOI confirmed.
2. Read EuropePMC open-access full-text XML (`evidence/fullText.xml`, 99 KB) — confirmed wet-lab methods (western blot, FACS, mouse survival).
3. String-searched the XML for accessions, model parameters, and code references:
   - 0 GEO / SRP / PRJNA / PRJEB / E-MTAB accessions.
   - 0 mentions of ODE / rate constant / Monte Carlo / track-structure / LQ-fit in a modelling sense.
   - No supplementary data table announcements; no GitHub/Zenodo URLs.
4. Decision: NO-GO for computational replication.

## Results vs Paper
| Item | Paper content | LUCID-relevant content |
|---|---|---|
| Quantitative model | None | None to replicate |
| Rate constants / parameters | None published in machine-readable form | None |
| Code repository | Not cited | N/A |
| Omics deposition | None | N/A |
| Western-blot band intensities | In figures; no underlying table | Re-digitising would be circular |
| Mouse survival curves | Reported (n small; effect not significant) | Could be re-tested for log-rank p but no underlying CSV; not a *computational* model replication |

## Verdict
**NO-GO — no computational replication target.** This is a small wet-lab biomarker discovery + in vivo radioprotection screen. There is no model, no rate-constant set, no openly-released dataset, and no analysis code to re-run. A figure-digitisation pass would just re-eyeball the authors' own bar charts and would not constitute independent computational validation.

## Coverage / 10
**0 / 10** — no computational claims to cover.

## Agreement / 10
**N/A** — no model to compare.

## Resources used
- EuropePMC public REST API (already cached in `evidence/`).
- ~2 minutes of CPU and a handful of grep calls to scan the XML.
- No GPU, no cloud, no paid endpoint, no author contact.

## Tools / Datasets / Hardware
- Python 3 + grep on `fullText.xml`.
- Local CPU on CherryRd subagent runtime.

## Limitations
- If a future LUCID batch focuses on **biomarker dose-response curve digitisation** (vs computational model replication), Park et al. 2024 figures could be revisited; that is out of scope for this batch.
- We did not retrieve the publisher-side PDF (would be the same content; full text is already in EuropePMC).

## Gates
- ≤10-min writeup: ✅
- Final verdict (REPLICATED/PARTIAL/SPOT-CHECK/NO-GO/BLOCKED): **NO-GO** ✅
- Coverage/Agreement: N/A (consistent with NO-GO) ✅
- No author contact: ✅
- No paid endpoints: ✅
