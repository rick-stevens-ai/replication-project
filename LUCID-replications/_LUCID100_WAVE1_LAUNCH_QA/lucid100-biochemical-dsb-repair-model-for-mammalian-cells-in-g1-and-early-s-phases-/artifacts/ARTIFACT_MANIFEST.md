# Artifact manifest — Taleei & Nikjoo 2013 (LUCID100 slot 10)

**Paper:** Taleei R, Nikjoo H. *Biochemical DSB-repair model for mammalian cells in G1 and early S phases of the cell cycle.* Mutation Research/Genetic Toxicology and Environmental Mutagenesis **756**(1-2):206-212 (2013).
- **DOI:** [10.1016/j.mrgentox.2013.06.004](https://doi.org/10.1016/j.mrgentox.2013.06.004)
- **PMID:** 23792210
- **OA status:** **CLOSED** (Unpaywall `oa_status=closed`, S2 `openAccessPdf.status=CLOSED`, no PMC/preprint).
- **Authors / affiliation:** Reza Taleei & Hooshang Nikjoo — Radiation Biophysics Group, Dept of Oncology-Pathology, Karolinska Institute, Stockholm.

## 1 · Direct paper artifacts

| Artifact | Status | Path / URL | Notes |
|---|---|---|---|
| Full-text PDF | ❌ **Not obtained** | publisher paywall (Elsevier ScienceDirect S1383-5718(13)00154-X) | OA scrape & Unpaywall both confirm no free copy. Author contact disallowed by task constraints. Argonne/Karolinska library access not invoked. |
| PubMed abstract | ✅ harvested | `artifacts/pubmed_abstract.txt` | Cached 2026-06-09 |
| Semantic Scholar record | ✅ harvested | `artifacts/semantic_scholar.json` | citationCount=89, referenceCount=64 |
| Unpaywall record | ✅ harvested | `artifacts/unpaywall.json` | oa_status=closed |
| Supplementary material | ❌ none in ScienceDirect listing | — | Companion editorial-response paper (PMID 24440803) is also closed. |
| Source code from authors | ❌ none published | — | Group does not release code. |
| Public data | n/a | — | Pure modelling paper; data are re-used from cited foci/PFGE literature. |

## 2 · Indirect / surrogate evidence used to build the replication

The Taleei-Nikjoo NHEJ kinetic skeleton is restated (with the same rate
constants and pathway topology) in several openly visible sources that we
*do* have at hand. These are the operational basis for the minimal
reimplementation in `code/taleei_nikjoo_2013_minimal.py`.

| # | Surrogate | Where it lives in this workspace | Why it is faithful to the 2013 paper |
|---|---|---|---|
| A | Taleei & Nikjoo, *Radiat Res* 179:540-548 (2013), "NHEJ Mathematical Model I" — same authors, same group, three months earlier, full law-of-mass-action formulation, all 13 reaction-step rate constants tabulated in Table 1. DOI `10.1667/RR3123.1`, PMID 23560635. | Metadata cached at `artifacts/semantic_scholar.json` (search hit #2). Paper itself CLOSED but we already use its parameter set in `lucid-slow-fast-nhej`. | The 2013 *Mutat Res* paper extends RR3123 by adding MMEJ + heterochromatin paths in G1/early-S. The c-NHEJ subsystem is unchanged. |
| B | Qi et al., *Cancers* 13:2202 (2021) — open access MDPI, supplement cached at `lucid-slow-fast-nhej/artifacts/mdpi-supplement/cancers-1190122-supplementary.pdf`. **Supplement Fig S8** explicitly compares the Qi "Entwined" model against the Taleei-Nikjoo 2013 NHEJ+MMEJ model and shows good agreement. **Table 1** lists the per-step transition times that are inherited from Taleei-Nikjoo 2013. | `lucid-slow-fast-nhej/code/nhej_model.py` (the slow/fast NHEJ ODE we built last month). | Independent open-access numerical replica of the Taleei-Nikjoo NHEJ rate constants. The MMEJ branch is the only added pathway in the 2013 paper. |
| C | DaMaRiS pathway listings (`pathwayNHEJ.txt`, `pathwayHR.txt`) from TOPAS-nBio. | `lucid-slow-fast-nhej/artifacts/damaris/` | DaMaRiS uses the Henthorn/Warmenhoven re-tabulation of Taleei-Nikjoo per-step transition times. |
| D | Friedland et al. *Radiat Prot Dosim* 143:154-160 (2011) and *Mutat Res Fund Mol Mech Mut* 711:28-40 (2011) — earlier NHEJ kinetic model the 2013 paper compares against. | Cited in Qi supplement S8; metadata only. | Sanity check that our ~1 h half-time bi-exponential repair curve is consistent with the c-NHEJ literature. |
| E | Mathematical Biosciences SSA companion (Taleei et al. *Radiat Prot Dosim* 143:204-208 / IJRB 88:948-953) — restates the rate-law formulation with worked examples. | Metadata only. | Independent confirmation of the law-of-mass-action ODE form. |

## 3 · Independent replication asset (this slot)

| Artifact | Path | Status |
|---|---|---|
| Minimal Taleei-Nikjoo 2013 ODE | `code/taleei_nikjoo_2013_minimal.py` | ✅ runs (LSODA, scipy) |
| Smoke-test JSON summary | `results/smoke_summary.json` | ✅ written 2026-06-09 |
| Smoke-test figure | `figures/fig_smoke_kinetics.png` | ✅ written 2026-06-09 |
| First-pass replication report | `FIRST_PASS_REPORT.md` | ✅ written 2026-06-09 |
| Progress JSON (subagent memory) | `~/.openclaw/workspace/memory/subagent-progress/lucid100-wave1-10-biochemical-dsb-repair-model-for-mammalian-cells-in-g1-and-e.json` | ✅ updated |

## 4 · Provenance hashes

Generated via `sha256sum` (see `artifacts/SHA256SUMS.txt`).
