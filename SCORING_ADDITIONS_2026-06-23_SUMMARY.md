# Scoring Additions Summary — 2026-06-23

3-judge LLM scoring pass over the 81 replication reports that had a REPORT but
no score in `MASTER_SCORES_2026-06-20.csv`.

## Method
- **Judges (free Argo proxy only):**
  - `argo:claude-sonnet-4.6`
  - `argo:claude-opus-4.7`
  - `argo:gpt-5`
- **Aggregation:** median of 3 for `coverage_10` and `agreement_10`; majority
  vote for `verdict` (ties → more conservative label).
- **Scoring grounded in report text only** — author self-scores ignored per
  Rick's standing rule.
- **Scorer:** `scoring/score_unscored_3judge.py` (durable, in workspace, not /tmp).
- **Runtime:** 81/81 in 5.3 min (concurrency=6, ~4 s/judge call).
- **Inputs:** `SCORE_TARGETS_LIST.txt` (81 entries).
- **Output:** `MASTER_SCORES_2026-06-23_additions.csv` (same 12 columns as
  the 06-20 master). The 06-20 master was **not** modified.

## Counts
- **Targets in list:** 81
- **Successfully scored:** 81 / 81 (100%)
- **Reports not found / stub:** 0 — every replication directory produced a
  usable report.
- **Judge-call failures:** 1 paper had **1/3** judges return an empty
  response (still aggregated cleanly from the remaining two judges, so no
  data loss):
  - `drift-flux-indoor-particles` — `argo:claude-sonnet-4.6` returned
    `no_json` (empty body). The other 2 judges agreed `PARTIAL`,
    cov 7&9 → median 8, agr 6&6 → 6. Recorded `PARTIAL 8 / 6`.

## Verdict distribution — NEW 81
| Verdict     | Count |
|-------------|------:|
| REPLICATED  |     4 |
| PARTIAL     |    30 |
| SPOT-CHECK  |    31 |
| NO-GO       |    13 |
| FAILED      |     3 |

- **Mean coverage:**   3.57 / 10
- **Mean agreement:**  5.89 / 10

The new batch is dominated by LUCID radiobiology replications (74 of 81),
which is reflected in the heavy `PARTIAL` / `SPOT-CHECK` mass — these
reports typically reproduce a subset of figures or one mechanistic claim
without re-running the full Geant4/TOPAS pipeline.

## Combined totals (152 prior + 81 new = 233)
| Verdict     | 06-20 | +06-23 |  Total |
|-------------|------:|-------:|-------:|
| REPLICATED  |    16 |      4 |     20 |
| PARTIAL     |   105 |     30 |    135 |
| SPOT-CHECK  |    22 |     31 |     53 |
| NO-GO       |     8 |     13 |     21 |
| FAILED      |     1 |      3 |      4 |
| **Total**   | **152** | **81** | **233** |

## Files
- Scorer:      `scoring/score_unscored_3judge.py`
- Run log:     `scoring/run_2026-06-23.log`
- Additions:   `MASTER_SCORES_2026-06-23_additions.csv`  (1 header + 81 rows)
- Source list: `SCORE_TARGETS_LIST.txt`
- Old master:  `MASTER_SCORES_2026-06-20.csv` (unchanged)

## Notes
- Three reports were marked `FAILED` by the panel: stub / no-substance content
  per the rubric (coverage essentially 0 with attempted-but-failed framing).
  Examples in the new batch: `LUCID-replications/lucid-friedland-stochastic-nhej-track-slot64`,
  `lucid100-flash-oxygen-repair-mechanistic-model`,
  `lucid100-friedland-stochastic-dsb-photon-ion-slot67`.
- `REPLICATED`s in the new batch:
  `spears-szeri-2004-mathieu`, `LUCID-replications/lucid-mcmahon-2016-medras-original`,
  `lucid100-doserate-cellcycle-adsc-2021`, `lucid100-epicellcom-dsb-repair-kinetics`.
- Light keyword extraction (tools / datasets / hardware) is structural, not
  judged — left blank where the report text did not mention recognizable
  tokens.
- Full per-paper judge transcripts (3 judges × 81 papers) are preserved in
  the `judge_panel_json` column of the additions CSV.
