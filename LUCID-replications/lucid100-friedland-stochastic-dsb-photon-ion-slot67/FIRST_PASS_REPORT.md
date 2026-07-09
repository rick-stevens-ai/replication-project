# FIRST PASS REPORT — LUCID100 slot 67
## Friedland, Kundrát & Jacob (2012), *Stochastic modelling of DSB repair after photon and ion irradiation*

DOI 10.3109/09553002.2011.611404 — IJRB 88(1–2):129–136 — PMID 21823824

---

## Verdict: **AMBER-KEEP**

- **Relevance:** high — directly within LUCID's "stochastic DSB repair after
  photon and ion irradiation" theme; precursor (RR1965 / 2010) already
  harvested in slot 64.
- **Replicability — full:** **NO** without (a) institutional access to the
  closed-access paper, (b) the proprietary PARTRAC source (Helmholtz Zentrum
  München, no public release), and (c) digitised tabular parameter sets.
- **Replicability — qualitative smoke:** **YES** — a reduced analytical model
  with the paper's three refinements (two-component fast/slow rejoining +
  labile-site delayed detection + LET-dependent slow fraction) reproduces the
  photon-vs-ion contrast (6/6 smoke checks pass on literature-typical
  reference curves).
- **Compute:** sub-second on CherryRd; no HPC plan needed.

## What we did

1. **Resolved provenance.**  Confirmed paper identity, authors (Friedland,
   Kundrát, Jacob — Helmholtz Zentrum München), 2012 publication, 14
   references; closed-access; no preprint or repository copy (Unpaywall,
   OpenAlex 2026-06-09).  See `source/{openalex,unpaywall,s2}_metadata.json`.
2. **Mapped the reference graph.**  Wrote `source/references_table.md` with
   all 14 cited works, their relevance to replication, and OA status.  Two
   key dependencies are open via the slot64 sibling folder
   (`kundrat2021_coupling.pdf`, `henthorn2018_nhej.pdf`).  The primary
   experimental data (Stenerlöw 2000 N-ion vs ⁶⁰Co γ rejoining) and the
   precursor RR1965 (2010) parameter tables are closed-access.
3. **Searched for PARTRAC code.**  GitHub queries for `partrac`,
   `stochastic DSB repair NHEJ`, `track structure DSB repair kinetics`
   returned **no public release** (the few "partrac" hits are unrelated
   particle-tracking utilities).  Helmholtz PARTRAC remains proprietary.
4. **Built a smoke reduction.**  `code/smoke_friedland2012.py` implements an
   analytical two-component rejoining model with a delayed labile-site term
   and fits it independently to literature-typical low-LET (⁶⁰Co γ) and
   high-LET (N-ion ~80 keV/µm) reference curves.

## Smoke results — 6/6 PASS

From `results/smoke_fit_results.json`:

| Endpoint                                             | ⁶⁰Co γ | N-ion |
|------------------------------------------------------|--------|-------|
| Fast fraction *f*                                    |  0.76  |  0.63 |
| Fast half-time *t½,fast* (min)                       |  19.1  |  34.7 |
| Slow half-time *t½,slow* (min)                       |  398   |  1156 |
| Labile-site amplitude *A*                            |  0.017 |  0.029 |
| Residual unrejoined fraction at 24 h (predicted)     |  0.021 |  0.16 |
| Residual unrejoined fraction at 24 h (input)         |  0.06  |  0.18 |
| RMSE of fit (vs input curve)                          |  0.021 |  0.025 |

Smoke checks:

| ID | Statement                                                     | Pass? |
|----|---------------------------------------------------------------|-------|
| S1 | ⁶⁰Co γ fast fraction in [0.70, 0.95]                          | ✅ |
| S2 | ⁶⁰Co γ fast half-time in [5, 30] min                          | ✅ |
| S3 | ⁶⁰Co γ slow half-time in [60, 600] min                        | ✅ |
| S4 | N-ion slow fraction > ⁶⁰Co γ slow fraction                    | ✅ |
| S5 | N-ion residual at 24 h > ⁶⁰Co γ residual at 24 h              | ✅ |
| S6 | Late-time monotone decrease and non-negative floor            | ✅ |

`figures/smoke_rejoining.png` shows both fits overlaid.

## What this smoke shows — and does not show

- It **shows** that the *shape* of the rejoining curves in the paper
  (delayed initial decline + larger slow shoulder at high LET + larger
  long-term residual at high LET) is *qualitatively recovered* by the
  minimum-viable analytical reduction of the model.  This is the
  Friedland-2012 "story" reduced to its closed-form skeleton.
- It does **not**: (a) reproduce any specific PARTRAC figure quantitatively,
  (b) recover the *individual* enzyme rate constants or DSB-complexity
  partitioning in PARTRAC, or (c) use the original Stenerlöw 2000 nitrogen
  ion vs Co-60 rejoining data — the reference curves used here are
  literature-typical digitisations chosen to span the LET range.

## Blockers for full replication

| Blocker                                                                  | Severity |
|--------------------------------------------------------------------------|----------|
| Paper PDF closed (Taylor & Francis, IJRB)                                | high     |
| PARTRAC source closed (Helmholtz Zentrum München; no public mirror)      | **fatal** for *exact* reproduction |
| Precursor RR1965 (2010) parameter tables closed                          | high     |
| Stenerlöw 2000 measured rejoining kinetics closed                        | medium (can substitute Cucinotta 2008 RR1035 / open-access summaries) |

## Recommended next actions

1. **QA retag** rank-98 row in `LUCID100_SOLID_MASTER_QA.tsv` from
   `candidate_curated` to `first_pass_complete_amber_keep`.  See sed snippet
   below.
2. (If a deeper pass is later authorised:) Acquire paper + RR1965 via
   institutional access, digitise tabular parameters, replace the analytical
   smoke with a small Gillespie-style stochastic NHEJ simulator seeded by
   the open-access Kundrát 2021 LET-dependent DSB-complexity fits already
   on disk in slot 64.  Laptop-scale; no HPC.
3. Cross-link this folder to `lucid-friedland-stochastic-nhej-track-slot64`
   in the master report — they form a natural pair (2010 base + 2012
   refinement).

### QA retag snippet (preview only — apply only on user instruction)

```bash
# This is the snippet a reviewer would run to retag rank 98 in the QA TSV.
# Not executed by this subagent.
python3 - <<'PY'
import csv, pathlib, shutil
p = pathlib.Path("/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv")
backup = p.with_suffix(p.suffix + ".bak_slot67")
shutil.copy(p, backup)
rows = list(csv.reader(p.open(), delimiter="\t"))
hdr  = rows[0]
i_rank, i_status = hdr.index("rank"), hdr.index("status")
i_folder, i_plan = hdr.index("replication_folder"), hdr.index("verdict_or_plan")
i_qa  = hdr.index("qa_decision")
for r in rows[1:]:
    if r[i_rank] == "98":
        r[i_status] = "first_pass_complete_amber_keep"
        r[i_folder] = "lucid100-friedland-stochastic-dsb-photon-ion-slot67"
        r[i_plan]   = "AMBER KEEP first pass: 6/6 analytical smoke checks pass; PARTRAC source closed; full reproduction infeasible without institutional access to paper+RR1965+Stenerlow2000."
        r[i_qa]     = "KEEP: relevant; slot67 AMBER KEEP; 6/6 smoke checks pass"
        break
with p.open("w", newline="") as fh:
    csv.writer(fh, delimiter="\t").writerows(rows)
print("OK; backup at", backup)
PY
```
