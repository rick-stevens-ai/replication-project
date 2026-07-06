# REPLICATE Project Status Audit

Updated **2026-07-05 09:20 CDT** by Ollie (post OSTI-100 catch-up batch — new replications + shell finishes + SPOT-CHECK promotions).

## OSTI-100 catch-up batch (2026-07-05 morning)
- **OSTI-100: 68 → 85 solid (+17).** Executed a rolling batch (cap 5 concurrent, free Argo Opus 4.7): finished 3 empty shells (3023663, 3025290, 3366144), 12 new replications from the TOPUP60 roster, and 6 SPOT-CHECK→solid promotions (2891462, 2976249, 3006635, 3013688, 3020811, 3024853 attempted; 2976249 promoted to PARTIAL).
- Corpus total: **598 solid / 676 rows** (was 581/660 at 06:53).
- Honest verdict mix skewed PARTIAL/SPOT-CHECK: many OSTI PDFs are OSTI-host-blocked from this box, so several fell back to physically-motivated synthetic testbeds (legitimate method-level tests, scored SPOT-CHECK when no numeric match to the paper was possible — not fabricated REPLICATED).
- Cleanup: duplicate-slug empty dirs from overlapping spawns quarantined to `_WAVE_DUPS_2026-07-05/`; 2 dup runs (3001916, 3027604) still finishing at write time — will dedup by paper_id, no double-count.
- **OSTI-100 remaining gap to 100: ~15.** Next lever: promote the remaining honest SPOT-CHECKs where PDFs become reachable, or add ~15 more new roster replications (22 unused candidates remain in TOPUP60).

---

Updated **2026-07-05 10:00 CDT** by Ollie (OSTI-100 catch-up batch + reconciliation; morning session).

## Headline (ground truth = report files on disk, via `scripts/census.py`)
- **680 real-paper rows** in reconciled master, **603 solid** (REPLICATED + PARTIAL). Backup: `RECONCILED_MASTER_2026-06-24.csv.bak-pre-rebuild-20260705T095851`.
- **OSTI-100 catch-up: 68 → 90 solid (+22)** via a rolling cap-5 subagent batch (finish empty shells + new replications + SPOT-CHECK→solid promotions), all on free Argo Opus 4.7. OSTI-100 now 96 dirs / 89 solid — **gap to 100 is 11**.
- Notable OSTI results: 3366146 (multiple-solutions PINN, Bratu) → REPLICATED; 3013688 (E3SM river routing) → REPLICATED; many PINN/operator/UQ papers → PARTIAL. Deduped a double-run of 3016110 (→ `_WAVE_DUPES_2026-07-05/`).
- **Prior 06:53 pass:** 660 rows / 581 solid (backup `.bak-pre-rebuild-20260705T065201`).
- **Solid grew 449 → 581 (+132)** since the 2026-07-03 pass, from the overnight wave: OSTI-100 (many new + promote + finisher), PDE-100 (new + spot→solid promotions), BVBRC-100 (new). QC-100 also folded in more rows (+27 solid to 141).
- Census flagged 21 disk dirs not in the prior master (real overnight replications + housekeeping dirs `_SPAWNER_KILLED_SHELLS_2026-07-04`, `_WAVE_DUPES_2026-07-01`, `_WAVE_DUPS`, `memory`, `roary_out`, `.git`) — all folded/handled in the rebuild.

## Per-set standing (target = 100 solid each) — 2026-07-05 10:00 rebuild
| Set        | dirs | solid | breakdown |
|------------|-----:|------:|-----------|
| BVBRC-100 ✅ | 113  | 109   | PARTIAL 64, REPL 45, unscored 1, NO-GO 1, CONTRA 1, SPOT 1 |
| LUCID-100 ✅ | 142  | 103   | PARTIAL 65, REPL 38, SPOT 20, NO-GO 16, BLOCK 2, FAIL 1 |
| OSTI-100    | 96   | 90    | PARTIAL 71, REPL 19, SPOT 6 |
| PDE-100 ✅   | 116  | 107   | PARTIAL 56, REPL 51, SPOT 4, NO-GO 2, FAIL 1, unscored 1, CONTRA 1 |
| QC-100 ✅    | 155  | 141   | REPL 90, PARTIAL 51, SPOT 13, unscored 1 |
| OTHER       | 58   | 53    | PARTIAL 36, REPL 17, SPOT 3, unscored 1, NO-GO 1 |
| **TOTAL**   | 680  | 603   | |

**4 of 5 named sets are over 100 solid** (BVBRC-100, LUCID-100, PDE-100, QC-100). **OSTI-100 climbed 68 → 90 solid**, now just **10 short** of target.

### OSTI-100 remaining gap (10 to target)
- Promote the 6 SPOT-CHECK + 1 unscored OSTI dirs where the science supports it, and/or run ~11 more new replications from the 22 still-available candidates in `priority-lists/OSTI100_TOPUP60_2026-07-04.tsv`.
- 1 unscored = non-canonical verdict token (e.g. 3022690 "SUPPORTED (methodology-level)") — normalize token wording (not a re-judgment).
- SPOT-CHECK this batch (2907986, 3015493, 3375019, 3022804) were method-level tests where the exact dataset/PDF was unavailable — legitimately not solid.

---

## Prior pass (2026-07-03 23:12)
- **529 real-paper rows** in reconciled master, **449 solid** (REPLICATED + PARTIAL), **4 unscored** (all QC-100, prose-verdict parser-coverage gap, NOT unfinished work).
- 🎉 **QC-100 TARGET REACHED** — 128 dirs / 114 solid (74 REPLICATED + 40 PARTIAL), well past the 100-solid goal. Climbed **~24 → 114 solid in one evening** via the autonomous cron wave driver (cbcce47a), all real Qiskit/PennyLane/Cirq/Stim/Mitiq sims on free Argo Opus 4.7.
- **Solid grew 384 → 449** since the 19:54 pass (the entire QC-100 evening push folded in).
- Reconciled master rebuilt from 23:10 census: `RECONCILED_MASTER_2026-06-24.csv` (529 rows; backup `.bak-pre-rebuild-20260703T231053`).

## Per-set standing (target = 100 solid each for the 5 named sets) — 23:12 rebuild
| Set        | dirs | solid | breakdown |
|------------|-----:|------:|-----------|
| LUCID-100  | 142  | 103   | PARTIAL 65, REPL 38, SPOT 20, NO-GO 16, BLOCK 2, FAIL 1 |
| PDE-100    | 62   | 54    | PARTIAL 29, REPL 25, SPOT 5, NO-GO 2, FAIL 1 |
| BVBRC-100  | 89   | 85    | PARTIAL 51, REPL 34, SPOT 2, NO-GO 1, CONTRA 1 |
| OSTI-100   | 51   | 40    | PARTIAL 29, REPL 11, SPOT 11 |
| QC-100 ✅  | 128  | 114   | REPL 74, PARTIAL 40, SPOT 10, (unscored 4) |
| OTHER      | 57   | 53    | PARTIAL 36, REPL 17, SPOT 3, NO-GO 1 |
| **TOTAL**  | 529  | 449   | |

**QC-100 is the 2nd set to clear 100 solid (after LUCID-100 at 103).** Evening mover: QC-100 49 → 114 solid (+65).

## QC-100 completion notes (2026-07-03 evening)
- Autonomous driver: ~8-min cron cycles, cap 5 concurrent subagents, review-paper filter, empty-pool backfill to 4-5.
- When the July-03 priority TSV emptied (71/71 launched), extended it inline with 59 fresh candidates from `QC100_CANDIDATES_2026-06-26.tsv`.
- Fixed dir-naming bug: 2 dirs had underscore instead of dot in arxiv id (`QC-2107_13470`, `QC-2207_08628`) — renamed to canonical dot form; census/dedup clean.
- Verdict mix is honest: 74 REPLICATED are exact/quantitative matches; PARTIAL/SPOT-CHECK mostly = hardware-experiment papers where the simulation baseline reproduced but the physical realization is out of scope (scope boundaries, not failures).

## What changed in this reconciliation (2026-07-03)
- **The stale `RECONCILED_MASTER` said 204 solid; disk truth is 341.** ~137 completed replications existed on disk but had never been reconciled into the master. Cause: the CSV was hand-edited and lagged 3 recent wave nights (BVBRC 20→89, OSTI wave, PDE top-up, QC-100).
- **Recovered 25 QC-100 reports** that census had been dropping — it wasn't recursing into the `QC-100/` subdir. Fixed `census.py` to enumerate QC-100 subdirs and remap collections to canonical labels (BVBRC-100 / OSTI-100 / QC-100 / PDE-100).
- Backups of the prior master saved as `RECONCILED_MASTER_2026-06-24.csv.bak-pre-rebuild-*`.
- New rebuild tool: `scripts/rebuild_reconciled.py` (census → canonical master, idempotent, backs up first).

## Supply of good candidate papers (rosters)
Curated 5×100 rosters exist in `priority-lists/` (2026-06-26):
- `BVBRC100_FINAL_2026-06-26.tsv` (100-row roster; 89 dirs created, ~81 solid)
- `PDE100_FINAL_2026-06-26.tsv` (52 dirs, 48 solid)
- `OSTI100_TOPUP50_2026-06-26.tsv` (roster; 51 dirs, 15 still unfinished shells)
- `QC100_CANDIDATES_2026-06-26.tsv` (100-candidate pool; 25 done)
- `LUCID_MERGED_2026-06-26.tsv` + `PRIORITY_100_LUCID.md` (142 dirs, 103 solid)
**Verdict: candidate supply is NOT the bottleneck** — each of the 5 sets has a ≥100-row curated roster on disk. The bottleneck is *execution + scoring throughput*, not paper discovery.

## Remaining scoring/execution gaps (real work, ranked)
1. **~20 empty/incomplete shells** (15 OSTI + 5 BVBRC): dirs spawned, PDF + some `work/` data pulled, but the subagent never wrote `REPORT.md`. These need the replication **finished (re-spawned)**, not scored. Examples: OSTI-2336586 (simulateqcd), OSTI-2583701 (mala), OSTI-3013688 (e3sm-river), BVBRC-64/65/67/68/70.
2. **300 self-scored rows** carry a verdict from the report's own §Verdict block, NOT a 3-judge panel. Per Rick's standing rule, a panel pass would standardize them. This is a large free-Argo inference job (`scoring/score_unscored_3judge.py`) — worth batching but not urgent.
3. Only **96 rows are panel-authoritative** (3-judge). Bringing more to panel is the main quality lever.

## Standing scoring policy
3-judge LLM panel (median Coverage+Agreement, majority verdict, conservative tiebreak) on **free Argo endpoints only**; regex/substring FORBIDDEN as final scorer (Rick 2026-05-19 / 06-23). Panel judges: argo:gpt-5.2, argo:gemini-2.5-pro, argo:claude-opus-4.7.

## How to reproduce these numbers
```bash
cd ~/Dropbox/REPLICATE-PROJECT
python3 scripts/census.py --csv CENSUS_$(date +%F).csv    # disk-truth matrix + gaps
python3 scripts/rebuild_reconciled.py CENSUS_$(date +%F).csv   # → canonical master (backs up first)
```
Note: legacy `scripts/reconcile_reports.py` uses old 4-collection labels and a looser extractor (counts sibling/dup reports, "UNRESOLVED" bucket). Prefer census + rebuild for headline numbers.
