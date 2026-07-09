# NO-GO REPORT — Wave 2 slot 20

**Paper:** Xiong et al. 2026, *An Ingestion-based Chronic Internal Radiation Model in C. elegans Using Americium Trichloride*. DOI `10.9734/arrb/2026/v41i52391`.

**Verdict: NO-GO for LUCID100 replication slot. RECOMMEND DEMOTE from top 100.**

## Why no-go (not "fake," just unsuitable)

The paper is real, the DOI is real, and the abstract describes a plausible (if narrowly scoped) wet-lab experiment. The problem is fit-for-purpose as a LUCID *replication* candidate:

### A. Venue credibility — DEMOTE-grade

| Signal | Observation |
|---|---|
| Publisher | **Sciencedomain International** — historically on Beall's predatory publisher lists. Pay-to-publish OA with weak/fast peer review reputation. |
| Journal | *Annual Research & Review in Biology* (ISSN 2347-565X). |
| DOAJ listed | **No** |
| Scopus indexed | **No** |
| 2-year mean citedness | **0.41** (very low for active life-sciences) |
| This article's citations | **0** (published 2026-04-28; brand new, but no preprint or follow-up traction visible either) |
| Author affiliations in OpenAlex/S2 | **None resolved** — none of the 6 authors have institutional affiliations linked in OpenAlex's authorship records. |

LUCID's top-100 slots are scarce; spending one on a single uncited paper in a predatory-adjacent venue is poor allocation when better-pedigree dose-rate / RBE / C. elegans radiotoxicology papers exist (e.g. *Radiation Research*, *IJRB*, *Mutation Research*, *Free Radical Biology and Medicine*).

### B. Replication-category mismatch

- Master TSV row tags this as `simulation/model replication`.
- Abstract describes a **purely wet-lab** study: liquid exposure with OP50 + AmCl₃, transgenic fluorescent reporter strains (CF1553, CL2166, PD4251, RW1596), behavioral and morphological assays.
- No simulation, no Monte Carlo, no dosimetric model, no code, no public data. The single quantitative dose figure (`0.748 µSv` per well) is asserted in the abstract without visible derivation.
- Replicating this would require a full **C. elegans wet lab with Am-241 licensure** — not in scope for a computational/in-silico LUCID effort.

### C. Methodological red flag

The reported single-well exposure dose of **0.748 µSv** is extraordinarily low for a chronic-toxicity study reporting `p < 0.001` reproductive-toxicity effects. For reference, ambient terrestrial background ≈ 1–2 µSv/day. Either the dose unit is misreported (µSv vs µSv/day vs µSv/hr), the dosimetry is microdosimetric to a tissue volume rather than whole-organism, or the effect attribution is questionable. Without the full Methods, this cannot be disambiguated — but it raises the bar on whether the paper is replication-worthy as-stated.

### D. Access friction

- Cloudflare bot-challenge blocks plain HTTP fetch of both landing and PDF.
- Per recovery constraints, browser/base64 transfer was not retried.
- A clean full-text would require either: a logged-in browser session passing the CF challenge (out of scope here), or institutional EZproxy that doesn't currently cover Sciencedomain titles for this site.

## Recommended QA retag

Change master TSV row 52 (rank 51):

- **From:** `KEEP: relevant and replication-plausible`
- **To:** `DEMOTE: predatory-adjacent venue (Sciencedomain Intl / ARRB); not DOAJ; not Scopus; 0 citations; wet-lab not simulation; replace with higher-pedigree alpha-LET / C. elegans radiotoxicology paper.`

And/or change `worktype` column from `simulation/model replication` → `wet-lab (out-of-scope)`.

## What a replacement might look like

Suggested replacement themes for the slot (search prompts, not specific picks):

- **Buisset-Goussen et al. (multiple, IRSN)** — C. elegans chronic gamma/alpha exposure, *Journal of Environmental Radioactivity* / *Aquatic Toxicology*. Solid IRSN dosimetry.
- **Dubois et al. 2018+ (IRSN)** — C. elegans multigenerational uranium / radionuclide effects.
- **Sakashita et al.** — C. elegans heavy-ion / alpha studies at NIRS-HIMAC, *Mutation Research* / *J Radiation Research*.
- **Maremonti et al. (NMBU CERAD)** — DBL-1/TGFβ and ROS in irradiated C. elegans, *Scientific Reports*.

Any of these would supply both dose-rate / LET signal **and** computational modeling hooks (RBE fits, ROS-kinetic models) more suitable for a LUCID replication.

## Confidence
- DOI legitimacy / paper-exists: **HIGH** (3 independent metadata sources agree).
- Venue-credibility downgrade: **HIGH** (objective DOAJ / Scopus / citation-rate signals).
- Replication-category mismatch: **HIGH** (clear from abstract alone).
- µSv methodological concern: **MEDIUM** (full Methods needed to fully adjudicate; not pursued per access/time constraints).

## Open Questions & Reproducibility Blockers

- **Verdict NO-GO — exact missing artifact:** the paper (Xiong et al. 2026, DOI 10.9734/arrb/2026/v41i52391) describes a **wet-lab Am-241 ingestion study in C. elegans with transgenic reporter strains CF1553, CL2166, PD4251, RW1596** — it contains no Monte Carlo / dosimetric model, no simulation code, no public data deposit, and no computational pipeline to re-run. The single quantitative claim available from the abstract — "0.748 µSv per well" — has no derivation in the visible text, and the full Methods PDF could not be fetched (Cloudflare bot challenge on Sciencedomain's site blocked plain HTTP; browser/base64 not retried per turn budget).
- **Replication category mismatch:** task TSV tagged this as `simulation/model replication`, but the paper is purely experimental wet-lab biology requiring Am-241 licensure, transgenic worm cultures, and behavioral/morphological assays — fundamentally out of scope for a computational LUCID slot.
- **Venue-credibility flag:** Sciencedomain International / *Annual Research & Review in Biology* (ISSN 2347-565X) is not in DOAJ, not in Scopus, has a 2-year mean citedness of 0.41, and this paper has 0 citations. None of the 6 authors have OpenAlex-resolved institutional affiliations.
- **Open question (procedural):** the master triage TSV row 52 should be retagged DEMOTE with `worktype = wet-lab (out-of-scope)` and the slot reallocated to a higher-pedigree alpha-LET / C. elegans radiotoxicology paper (Buisset-Goussen / Dubois IRSN, Sakashita NIRS-HIMAC, Maremonti CERAD).
- **Open methodological question:** even if access were obtained, the µSv-vs-µSv/day vs microdosimetric ambiguity in the abstract's "0.748 µSv" makes the reported `p < 0.001` reproductive-toxicity effect at sub-background dose suspect — what tissue volume / exposure duration is the dose actually scoped to?
