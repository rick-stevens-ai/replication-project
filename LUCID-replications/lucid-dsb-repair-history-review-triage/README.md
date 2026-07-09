# LUCID Triage — Berthel et al. 2019 (DSB-repair history review)

**Verdict: NO-GO (review-only article).**

This folder is the honest-triage output for the LUCID work item targeting:

> Berthel E., Ferlazzo M.L., Devic C., Bourguignon M., Foray N.
> *What Does the History of Research on the Repair of DNA Double-Strand Breaks Tell Us? — A Comprehensive Review of Human Radiosensitivity.*
> **Int. J. Mol. Sci.** 2019, **20**(21), 5339. DOI [10.3390/ijms20215339](https://doi.org/10.3390/ijms20215339).
> Source PDF: `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/58db87da741bb417f019bddf0ff1f58ff53f7e78.pdf` (2.0 MB).

## TL;DR

- **Article type:** Narrative / historical comprehensive **Review** (MDPI explicitly labels it "Review").
- **Tables:** 0.
- **Figures:** 6 — five are schematics or re-drawings of data from prior cited references; one (Fig. 3) plots a SF2-vs-%-unrepaired-DSB scatter with two heuristic 2-parameter fits (power `y = 55.36 x^(−0.76)`, r = 0.68; inverse `y = 75/(x+0.57)`, r = 0.63). Underlying point-level data are *not* provided in this paper.
- **Original experimental data:** none.
- **Meta-analytic pooled estimates:** none.
- **Mathematical / statistical model with parameters fit in this paper:** **none beyond the two heuristic curves in Fig. 3 and the trivial `y = x + 1` overlay in Fig. 5D, neither replicable without re-digitising the figures or fetching the cited source papers.**
- **Supplementary materials:** none referenced.
- **References:** 77.

## Files

| file | purpose |
|---|---|
| `REPORT.md` | Full triage report with figure-by-figure inventory, sanity-checks of the published Fig. 3 fits, and the reasoning for NO-GO. |
| `PROGRESS.md` | Stage-by-stage progress log (hard-gated <10-min checkpoint plus final state). |
| `README.md` | This file. |

Companion progress JSON (out of folder, in the subagent shared dir):
`/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid-dsb-repair-history-review-triage.json`

## Why this is **not** wasted work

The paper is a strong scientific essay that argues for the RIANS / nucleo-shuttling model and against the "HR-or-else-NHEJ" paradigm, but it is explicitly a **synthesis** of work already published elsewhere by the same group (Foray lab, Lyon). LUCID's purpose is to validate compact quantitative artefacts; this paper carries none. Marking it NO-GO frees the next slot for a target with extractable tables, fitted models, or pooled effect sizes.

## What *would* be a legitimate follow-on

If LUCID later wants the **Fig. 3 correlation** itself replicated, the upstream targets are:

- Joubert et al. *Int. J. Radiat. Biol.* 2008 (ref [12])
- Jeggo & Kemp *Mutat. Res.* 1983 (ref [15])
- Ferlazzo et al. *Mol. Neurobiol.* 2017 (ref [30])

A replication would assemble the SF2 and DSB-repair tables from those three papers, re-fit the two models, and compare parameter estimates and r values. This is a distinct work item, not this one.
