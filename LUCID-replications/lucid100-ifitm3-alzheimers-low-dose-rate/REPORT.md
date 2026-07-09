# LUCID-100 Replication Report

**Paper:** Son Y, Lee CG, Kim JS, Lee H-J. *Low-dose-rate ionizing radiation affects innate immunity protein IFITM3 in a mouse model of Alzheimer's disease.* Int J Radiat Biol 99(11):1649-1659, 2023.
**DOI:** 10.1080/09553002.2023.2211142 | **PMID:** 37162420 | **S2:** 1a97870e10d00a628c34dbe73e5a9e38c7951351
**LUCID-100 slot:** 31 (Wave 4, A-tier, score 15 — recommended demotion)
**Subagent run:** 2026-06-22, re-audit of 2026-06-09 NO-GO verdict.

## TL;DR

**Verdict: NO-GO.** This is a closed-access in vivo mouse paper (5xFAD + WT,
112-day chronic LDR exposure) with **no public dataset, no supplementary
material, no PMC mirror, no preprint, no code, and no in-silico component**
despite the master TSV mis-tag of `simulation/model replication`. The 2026-06-09
prior subagent's NO-GO was re-verified today against fresh queries to S2 (still
`openAccessPdf.status: CLOSED`), EuropePMC (`inPMC=N hasPDF=N hasSuppl=N`),
EuropePMC fullTextXML endpoint (404), Cloudflare-gated Tandfonline (HTTP 403),
Wayback Machine (no snapshot), NCBI GEO/SRA (no deposit by these authors for
this study), and bioRxiv (no preprint). All testable abstract/Results claims
remain UNTESTED because the underlying data (qPCR Ct values, IHC intensity,
behavioural scores) was never released and the figures themselves are not
accessible. No fabricated numbers; no paid endpoints used; no wet-lab access.

## 1. Data sources

| Source | Result (re-verified 2026-06-22) |
|---|---|
| Crossref / DOI redirect | 406 from sandbox |
| Tandfonline full text | HTTP 403 (Cloudflare challenge) |
| Unpaywall | `is_oa: false`, no OA locations, no embargo info — see `artifacts/unpaywall.json` |
| Semantic Scholar `openAccessPdf` | `status: CLOSED`, license `CCBYNCND` but no accessible URL (only DOI back-link). `isOpenAccess: true` is metadata-only; PDF endpoint is gated. |
| EuropePMC search | 1 hit (PMID 37162420), `inPMC=N`, `hasPDF=N`, `hasSuppl=N`, only `Subscription required` URL listed |
| EuropePMC `MED/37162420/fullTextXML` | HTTP 404 |
| PubMed | Free-article flag routes only to publisher landing |
| GEO (esearch `IFITM3 + 5xFAD + radiation`) | 0 datasets |
| GEO/SRA (esearch by author "Son Y" + IFITM3 + 5xFAD) | 0 datasets |
| bioRxiv (DOI lookup) | not indexed (no preprint) |
| Wayback Machine | no archived snapshots of Tandfonline full-text page |
| MGI references | mouse paper noted; no transgene resources or datasets attached |

**Reusable artifacts on disk:**

- `artifacts/semantic_scholar.json` — S2 metadata + abstract + tldr
- `artifacts/unpaywall.json` — OA status
- `artifacts/europepmc.json` — EuropePMC core record
- `artifacts/references.txt` — 38-reference list (wet-lab framing confirmed)
- `artifacts/MANIFEST.md`

## 2. Methods comparison

**Paper's methods (per abstract — full Methods section paywalled):**

- Animals: WT and 5xFAD transgenic mice, genotyped, n per arm not recoverable from abstract.
- Exposure: chronic low-dose-rate gamma irradiation for 112 days, cumulative doses 0, 0.1, 0.3 Gy (≈ 0.9 µGy/min average for 0.1 Gy arm; ≈ 2.7 µGy/min for 0.3 Gy arm — derived, not stated in abstract).
- Behaviour: Y-maze (working memory), open field (locomotor / anxiety).
- Molecular: APP processing markers; gliosis (Iba1, GFAP); cytokines (IL-1β, IL-6, TNF-α); IFN-γ; IFITM3 — measured by qPCR / IHC / western (specific assignment per readout not recoverable from abstract).
- Stats: not specified in abstract; almost certainly ANOVA or t-tests on group means (typical for this assay panel).

**Replication's methods:** None executed. There is no in-silico surface to
attach to: no model parameters to re-fit, no public count matrices to
re-normalize, no images to re-segment, no released code to re-run. Wet-lab
reproduction (≥ 6 months, IACUC, ~36–60 mice, low-dose-rate irradiator
access at KIRAMS-equivalent facility) is out of scope for this track. Figure
digitization is gated by the same paywall as the text.

**Substitutions:** None — no replicable computational pipeline exists to
substitute into.

## 3. Quantitative claim audit

Testable claims extractable from the public abstract (Methods + Results
quantitative numerical signal); none could be tested without paywalled
full text or the underlying data.

| # | Claim (abstract verbatim or paraphrase) | Reported value / direction | Replication test | Result |
|---|---|---|---|---|
| C1 | Chronic LDR for 112 days at cumulative 0, 0.1, 0.3 Gy applied to WT and 5xFAD mice | dosing/timing spec | n/a (design statement) | NOT TESTED — no data |
| C2 | No apparent change in non-spatial memory (Y-maze) after LDR | null effect on Y-maze score | reanalyse behaviour | NOT TESTED — scores never released; bar charts paywalled |
| C3 | No apparent change in locomotor activity (open field) after LDR | null effect on OF distance/time | reanalyse behaviour | NOT TESTED — scores never released |
| C4 | LDR did not affect APP processing markers | null effect | reanalyse qPCR/western | NOT TESTED — no ΔΔCt / band density values |
| C5 | LDR did not affect gliosis markers Iba1 and GFAP | null effect (IHC quantification) | reanalyse IHC | NOT TESTED — no per-mouse intensity values; figures paywalled |
| C6 | LDR did not affect IL-1β, IL-6, TNF-α | null effect | reanalyse qPCR | NOT TESTED — no Ct values |
| C7 | IFN-γ significantly downregulated in TG (5xFAD) mice after LDR | direction: ↓, p<0.05 | reanalyse | NOT TESTED — no per-mouse expression values |
| C8 | IFITM3 significantly decreased in TG mice at 0.1 or 0.3 Gy LDR (headline) | direction: ↓, both LDR doses, p<0.05 | reanalyse | NOT TESTED — headline claim, no underlying data |
| C9 | IFITM3 effect specific to TG genotype (not WT) | genotype × dose interaction | reanalyse with ANOVA | NOT TESTED |

**Summary:** 9 testable claims identified from abstract. **0 tested.**
All are blocked by the same artifact gap: no per-mouse measurement values
released and no figures accessible for digitisation.

## 4. Scope audit

**Paper's primary analyzable units (estimated from abstract — exact figure
count not recoverable without full text):**

- 6 experimental arms (WT/TG × 0/0.1/0.3 Gy)
- ~9 molecular readouts (APP markers, Iba1, GFAP, IL-1β, IL-6, TNF-α, IFN-γ, IFITM3, and IFN-signaling panel)
- 2 behavioural assays (Y-maze, open field)
- ~6–10 figures plus a likely supplemental panel (none indexed)

**Replication coverage:** 0 of any of the above units processed.

**Coverage:** 0/N (no analyzable unit re-derived).
Blocker is uniform across the paper: closed-access full text + no public
data + no preprint + no Wayback cache + no GEO/SRA deposit. Naming the
exact missing artifacts (per Rick's rule):

1. **Per-mouse Y-maze alternation scores** (CSV/XLSX): never released.
2. **Per-mouse open-field distance/center-time scores**: never released.
3. **Per-mouse qPCR Ct or ΔΔCt values** for APP, Iba1, GFAP, IL-1β, IL-6, TNF-α, IFN-γ, IFITM3, and the IFN-signaling panel: never released.
4. **Per-mouse western band densities** and source blots: never released.
5. **Per-mouse IHC quantification** (Iba1+/GFAP+ cell counts or intensities) and source micrographs: never released.
6. **Manuscript PDF / HTML full text** (would at least enable figure digitisation): paywalled and not OA-mirrored anywhere indexed.

## 5. What I actually ran

- Read `AUDIT_PROTOCOL.md`, `README.md`, `FIRST_PASS_REPORT.md`, `NO_GO_REPORT.md`, `PROGRESS.md`, and `artifacts/MANIFEST.md` (the "5 md staged" referenced in the task brief).
- Re-verified 2026-06-09 NO-GO with fresh API hits 2026-06-22:
  - Semantic Scholar Graph API `/paper/DOI:...?fields=openAccessPdf,externalIds,isOpenAccess,abstract,tldr` using `x-api-key` (S2 API key from macOS keychain `semantic-scholar-api-key/rick-stevens-ai`, per workspace standing rule — no anonymous S2 calls).
  - EuropePMC `/search?query=DOI:...&resultType=core` → 1 hit, `inPMC=N hasPDF=N hasSuppl=N`.
  - EuropePMC `/MED/37162420/fullTextXML` → HTTP 404.
  - Tandfonline `/doi/full/...` → HTTP 403 (Cloudflare).
  - NCBI E-utilities `esearch` for GEO/SRA by author and topic terms → 0 / no relevant deposits.
  - bioRxiv DOI lookup → not indexed.
  - Wayback Machine availability API → no snapshot.
- Did **not** run any analysis pipeline: no data to load, no model to re-fit, no figures to re-digitize.
- Did **not** attempt paywall bypass, author contact, or paid endpoints (per task constraints).
- Smoke script `scripts/smoke_scope.py` from the prior pass remains the standing watchdog — if any OA-status flag flips, it will exit non-zero and the row can be re-triaged.

## 6. Key output files

- `REPORT.md` — this report.
- `FIRST_PASS_REPORT.md` (2026-06-09) — prior scoping and verdict, still valid.
- `NO_GO_REPORT.md` (2026-06-09) — formal NO-GO with retag recommendation, still valid.
- `README.md` — slot identification + master-row retag recommendation.
- `PROGRESS.md` — step log of prior pass.
- `artifacts/semantic_scholar.json` — S2 metadata + abstract + tldr.
- `artifacts/unpaywall.json` — OA status (`is_oa: false`).
- `artifacts/europepmc.json` — EuropePMC record.
- `artifacts/references.txt` — 38-reference list.
- `artifacts/MANIFEST.md` — artifact inventory.
- `scripts/smoke_scope.py` — watchdog re-pull (S2 + Unpaywall + EuropePMC).
- `data/`, `figures/`, `notes/` — intentionally empty; no public data or figures to populate.

## 7. Honest gaps

- **Full text unread.** The abstract is the only authoritative text I have. Methods details (exact n, statistical tests, dose-rate values, IHC quantification protocol, qPCR primers) are unknown to me. My claim list is therefore abstract-derived and may miss Results-table claims that would be in the body.
- **Figures unseen.** Cannot digitize even the published summary bar charts because the publisher HTML/PDF is Cloudflare-gated.
- **No wet-lab pathway tried.** Wet-lab reproduction is intentionally out of scope for the LUCID in-silico replication track and would not be possible from this subagent context regardless.
- **No author contact.** Disallowed per task constraints; would in any case be the wrong tool for a slot the master TSV mis-tagged.
- **Master TSV retag is a recommendation, not a commit.** The retag from `simulation/model replication` → `wet-lab in vivo / no public data` and the score demotion from 15 → below Wave-4 threshold needs Rick's hand on the master file; I did not modify `LUCID100_SOLID_MASTER_QA.tsv`.
- **Sweep recommendation deferred.** Other Wave-4 rows auto-tagged `computational model / simulation` likely contain similar wet-lab misclassifications; a sweep would catch them before more subagent time is spent on them, but is out of scope for this single-paper run.

## 8. Verdict

**NO-GO.** Closed-access in vivo mouse paper, mis-tagged in master TSV as
`simulation/model replication`. There is no computational artifact to
re-run, no public data to re-analyse, and no full text to digitise. The
prior 2026-06-09 NO-GO is re-confirmed under fresh API queries on
2026-06-22. Honest scores reflect zero coverage of analyzable units and
zero quantitative claims tested — not zero effort, but zero replication
surface.

- **Coverage:** 0/10 (no analyzable unit processed; all blocked by missing artifacts named in §4)
- **Agreement:** 0/10 (no claim was testable, so no agreement or disagreement can be reported — using 0/10 by convention for "untested," not "contradicted")

Recommended next action: backfill slot 31 with the next Wave-4 candidate
that has either a code release, an open dataset, or a real mechanistic
simulation. Optionally sweep other Wave-4 rows tagged
`computational model / simulation` for the same mis-tag pattern.

---

VERDICT=NO-GO COVERAGE=0/10 AGREEMENT=0/10

Repro blockers (3-line summary):
1. Paywalled at Tandfonline (HTTP 403, Cloudflare); no PMC mirror; no Wayback snapshot; no bioRxiv preprint — full text inaccessible from the OpenClaw subagent environment.
2. No public deposit of underlying data: zero GEO/SRA hits for IFITM3 + 5xFAD + radiation or by author "Son Y" / "Yeonghoon Son"; EuropePMC reports `hasSuppl=N`; per-mouse behaviour scores, qPCR Ct values, western blot densities, and IHC quantifications never released.
3. Mis-tagged in `LUCID100_SOLID_MASTER_QA.tsv` row 75 as `simulation/model replication` — the paper has no computational model, no simulation, no code; recommend retag to `wet-lab in vivo / no public data` and demote from Wave-4 A-tier.
